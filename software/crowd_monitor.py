import subprocess
import serial
import time
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create logs directory
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def get_device_count():
    """Count devices in your specific IP range"""
    try:
        result = subprocess.run(
            ['sudo', 'nmap', '-sn', '-T2', '-PE', '192.168.1.100-199'],
            capture_output=True, text=True
        )
        return result.stdout.count("Nmap scan report")
    except Exception as e:
        print(f"Error getting device count: {e}")
        return 0

def rotate_to_angle(angle):
    """Send rotation command to ESP32"""
    try:
        ser = serial.Serial('/dev/serial0', 115200, timeout=1)
        command = f"ROTATE {angle}\n"
        ser.write(command.encode())
        ser.close()
        print(f"Rotated to {angle}°")
        time.sleep(0.5)
    except Exception as e:
        print(f"Rotation error: {e}")

def main():
    print('🚀 Crowd Monitor Started')
    print('Network: Smart | Threshold: 4 devices')
    print('-' * 40)
    
    while True:
        count = get_device_count()
        print(f'\n📱 Devices: {count}')
        
        if count >= 4:
            print('🚨 CROWD DETECTED!')
            
            best_angle = 0
            best_count = 0
            
            for angle in [0, 90, 180, 270]:
                rotate_to_angle(angle)
                time.sleep(2)
                
                new_count = get_device_count()
                print(f'  Angle {angle}°: {new_count} devices')
                
                if new_count > best_count:
                    best_count = new_count
                    best_angle = angle
            
            print(f'🎯 Best direction: {best_angle}°')
            rotate_to_angle(best_angle)
            time.sleep(30)
        else:
            rotate_to_angle(0)
            time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n⏹️ Stopped by user.')