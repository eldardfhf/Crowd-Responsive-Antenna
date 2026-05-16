#!/usr/bin/env python3
"""
Antenna System using arp-scan (ultra-fast)
"""
import subprocess
import serial
import time

POWERBEAM_IP = "192.168.1.102"
CROWD_THRESHOLD = 4
SCAN_ANGLES = [0, 90, 180, 270]

def get_device_count():
    """Count devices using arp-scan - takes ~2 seconds"""
    try:
        result = subprocess.run(
            ['sudo', 'arp-scan', '--localnet', '-q'],
            capture_output=True, text=True, timeout=10
        )
        # Count unique IPs (exclude header/footer lines)
        lines = result.stdout.strip().split('\n')
        ip_count = sum(1 for line in lines if line.startswith('192.168.1.'))
        return max(0, ip_count - 2)  # Subtract router + Pi
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
        return 0

def get_signal_strength():
    """Measure signal via ping"""
    try:
        result = subprocess.run(
            ['ping', '-c', '2', '-W', '1', POWERBEAM_IP],
            capture_output=True, text=True, timeout=5
        )
        if 'avg' in result.stdout:
            parts = result.stdout.split('avg')[1].split('=')[1].split('/')
            avg_ping = float(parts[1].strip())
            signal_score = max(0, 100 - avg_ping * 2)
            return signal_score, avg_ping
    except:
        pass
    return 50, 0

def rotate_to_angle(angle):
    """Rotate motor"""
    try:
        ser = serial.Serial('/dev/serial0', 115200, timeout=2)
        time.sleep(1)
        ser.write(f"ROTATE {angle}\n".encode())
        time.sleep(3)
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            ser.close()
            return "ROTATED" in response
        ser.close()
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def find_best_direction():
    """Scan all directions"""
    print("\n🔍 Scanning directions...")
    print("-" * 50)
    
    results = {}
    
    for angle in SCAN_ANGLES:
        print(f"\n📡 {angle}°...")
        
        if rotate_to_angle(angle):
            time.sleep(2)
            devices = get_device_count()
            signal, ping = get_signal_strength()
            
            # Score calculation
            device_score = min(100, (devices / 10) * 100)
            total_score = (device_score * 0.7) + (signal * 0.3)
            
            results[angle] = {'devices': devices, 'score': total_score}
            print(f"   📱 {devices} devices | 📶 {signal:.0f}/100 | 🎯 {total_score:.1f}")
    
    if not results:
        return 0
    
    best = max(results, key=lambda x: results[x]['score'])
    print(f"\n🏆 BEST: {best}° ({results[best]['devices']} devices)")
    return best

def main():
    print("🚀 Fast Antenna System (arp-scan)")
    print("-" * 50)
    
    current_angle = 0
    
    try:
        while True:
            count = get_device_count()
            print(f"\n⏰ {time.strftime('%H:%M:%S')} | 📱 {count} devices")
            
            if count >= CROWD_THRESHOLD:
                print(f"🚨 CROWD! ({count} ≥ {CROWD_THRESHOLD})")
                best = find_best_direction()
                
                if best != current_angle:
                    print(f"🔄 Rotating to {best}°...")
                    if rotate_to_angle(best):
                        current_angle = best
                        print(f"   ✅ At {best}°")
                
                time.sleep(30)
            else:
                print(f"🟢 Normal ({count} < {CROWD_THRESHOLD})")
                if current_angle != 0:
                    rotate_to_angle(0)
                    current_angle = 0
                time.sleep(10)
    
    except KeyboardInterrupt:
        print("\n⏹️ Stopped")
        rotate_to_angle(0)

if __name__ == '__main__':
    main()