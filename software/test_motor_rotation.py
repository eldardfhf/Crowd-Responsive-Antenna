import serial
import time

def rotate_to_angle(angle):
    """Send rotation command to ESP32"""
    try:
        ser = serial.Serial('/dev/serial0', 115200, timeout=1)
        command = f"ROTATE {angle}\n"
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")
        
        time.sleep(2)
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"Received: {response}")
        
        ser.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

print("🔄 Testing motor rotation...")
print("Motor should rotate to 90°, 180°, 270°, then 0°")
print("-" * 50)

angles = [90, 180, 270, 0]

for angle in angles:
    print(f"\nRotating to {angle}°...")
    if rotate_to_angle(angle):
        print(f"✅ Rotation to {angle}° complete")
    else:
        print(f"❌ Rotation to {angle}° failed")
    time.sleep(1)

print("\n" + "=" * 50)
print("✅ Test complete!")