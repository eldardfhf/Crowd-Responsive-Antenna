#!/usr/bin/env python3
"""
Smart Antenna System
====================
Detects crowd density and points the Ubiquiti PowerBeam 
in the direction with the strongest signal and most devices.
"""

import subprocess
import serial
import time
import sys

# --- CONFIGURATION ---
POWERBEAM_IP = "192.168.1.103"  # Update if you set a static IP
CROWD_THRESHOLD = 4             # Trigger rotation if devices >= 4
SCAN_ANGLES = [0, 90, 180, 270] # Directions to check

def get_device_count():
    """
    Count devices using arp-scan.
    Much faster than nmap and won't timeout.
    """
    try:
        # Run arp-scan silently
        result = subprocess.run(
            ['sudo', 'arp-scan', '--localnet', '-q'], 
            capture_output=True, text=True, timeout=10
        )
        
        # Count lines that look like IP addresses (exclude headers)
        count = 0
        for line in result.stdout.split('\n'):
            if line.strip().startswith('192.168.1.'):
                count += 1
        
        # Subtract known static devices (Router + Pi + PowerBeam) to get "Clients"
        # Adjust this number if needed
        clients = max(0, count - 3) 
        return clients
    except Exception as e:
        print(f"   ⚠️ Count error: {e}")
        return 0

def get_signal_strength():
    """
    Measure signal quality by pinging the PowerBeam.
    Lower ping = Better signal/connection.
    """
    try:
        result = subprocess.run(
            ['ping', '-c', '2', POWERBEAM_IP], 
            capture_output=True, text=True, timeout=3
        )
        
        if 'avg' in result.stdout:
            # Extract average ping time (e.g., "time=2.5 ms")
            parts = result.stdout.split('avg')[1].split('=')[1].split('/')
            avg_ping = float(parts[1].strip())
            
            # Convert to score: Lower ping is better
            # <10ms is perfect (100), >100ms is bad (0)
            score = max(0, 100 - (avg_ping * 2))
            return score, avg_ping
    except:
        pass
    return 50, 0  # Default medium score

def rotate_to_angle(angle):
    """Send command to ESP32 to rotate motor."""
    try:
        ser = serial.Serial('/dev/serial0', 115200, timeout=2)
        time.sleep(1) # Wait for connection
        command = f"ROTATE {angle}\n"
        ser.write(command.encode())
        
        # Wait for motor to finish moving
        # Since your motor moves ~170deg per step, give it extra time
        time.sleep(4) 
        
        # Check for response
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            ser.close()
            return "ROTATED" in response or "ACK" in response
        ser.close()
        return True
    except Exception as e:
        print(f"    Rotation Error: {e}")
        return False

def find_best_direction():
    """
    Scan all angles, calculate a score based on 
    (Device Count + Signal Strength), and return the best angle.
    """
    print("\n🔍 SCANNING DIRECTIONS...")
    print("-" * 50)
    
    results = {}
    
    for angle in SCAN_ANGLES:
        print(f"\n📡 Testing {angle}°...")
        
        # Rotate motor
        if not rotate_to_angle(angle):
            continue
            
        # Give signal time to stabilize
        time.sleep(2)
        
        # Measure
        devices = get_device_count()
        signal_score, ping = get_signal_strength()
        
        # SCORING ALGORITHM
        # Weight: 60% Crowd Size, 40% Signal Strength
        device_score = min(100, (devices / 10) * 100) # Normalize to 100
        total_score = (device_score * 0.6) + (signal_score * 0.4)
        
        results[angle] = {
            'devices': devices,
            'signal': signal_score,
            'score': total_score
        }
        
        print(f"   👥 Devices: {devices}")
        print(f"    Signal Score: {signal_score:.0f}/100 (Ping: {ping:.1f}ms)")
        print(f"   🎯 Total Score: {total_score:.1f}/100")

    # Find the winner
    if not results:
        return 0 # Default to 0 if scan fails
    
    best_angle = max(results, key=lambda x: results[x]['score'])
    best_data = results[best_angle]
    
    print("\n" + "=" * 50)
    print(f"🏆 BEST DIRECTION: {best_angle}°")
    print(f"   Reason: {best_data['devices']} devices + High signal")
    print("=" * 50)
    
    return best_angle

def main():
    print("🚀 SMART ANTENNA SYSTEM STARTED")
    print(f"Target: {POWERBEAM_IP} | Threshold: {CROWD_THRESHOLD} devices")
    print("-" * 50)
    
    current_angle = 0
    
    try:
        while True:
            # Check current crowd size
            count = get_device_count()
            timestamp = time.strftime("%H:%M:%S")
            
            print(f"\n⏰ [{timestamp}] Devices Connected: {count}")
            
            if count >= CROWD_THRESHOLD:
                print("🚨 CROWD DETECTED! Searching for best angle...")
                
                best = find_best_direction()
                
                # Rotate to the winner if not already there
                if best != current_angle:
                    print(f"\n🔄 MOVING to best angle {best}°...")
                    rotate_to_angle(best)
                    current_angle = best
                    print(f"   ✅ Antenna locked at {best}°")
                
                # Stay pointed at crowd for a while before re-checking
                print("⏳ Holding position (monitoring)...")
                time.sleep(15)
                
            else:
                print("🟢 Normal traffic. Keeping Home position.")
                # If we are looking away, return to home (0)
                if current_angle != 0:
                    print("   🔄 Returning to 0°...")
                    rotate_to_angle(0)
                    current_angle = 0
                
                # Check every 10 seconds
                time.sleep(10)

    except KeyboardInterrupt:
        print("\n\n⏹️ SYSTEM SHUTDOWN")
        rotate_to_angle(0)

if __name__ == "__main__":
    main()