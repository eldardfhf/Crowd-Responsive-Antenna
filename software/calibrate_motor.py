#!/usr/bin/env python3
"""
Motor Calibration Test
Tests actual rotation at key angles
"""
import serial
import time

def test_rotation(angle):
    """Test rotation to specific angle"""
    try:
        ser = serial.Serial('/dev/serial0', 115200, timeout=2)
        time.sleep(1)
        
        print(f"\n➡️ Testing {angle}°...")
        command = f"ROTATE {angle}\n"
        ser.write(command.encode())
        
        time.sleep(5)  # Give motor time to complete
        
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"   ✅ Response: {response}")
        
        ser.close()
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

print("🔧 MOTOR CALIBRATION TEST")
print("=" * 50)
print("\nThis test will rotate the motor to specific angles.")
print("MANUALLY verify the rotation matches the command.\n")

input("Press Enter to start...")

# Test key angles
test_angles = [
    (0, "Home position"),
    (90, "Quarter turn (should be 90°)"),
    (180, "Half turn (should be opposite)"),
    (270, "Three-quarter turn"),
    (360, "Full rotation (back to start)"),
    (0, "Back to home")
]

for angle, description in test_angles:
    test_rotation(angle)
    print(f"   📝 {description}")
    input("   Press Enter when ready for next angle...")

print("\n" + "=" * 50)
print("✅ Calibration test complete!")
print("\nDid the motor rotate to the correct positions?")
print("- If YES: System is calibrated correctly")
print("- If NO: Check microstepping wiring (MS1/MS2/MS3)")