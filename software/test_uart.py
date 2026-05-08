import serial
import time

print("Testing UART communication...")

try:
    ser = serial.Serial('/dev/serial0', 115200, timeout=1)
    time.sleep(2)
    
    ser.write(b"HELLO\n")
    time.sleep(0.5)
    
    response = ser.readline().decode('utf-8').strip()
    print(f"Response: {response}")
    
    if "ESP32_ACK" in response:
        print("✅ ESP32 communication working!")
    else:
        print("❌ No response from ESP32")
    
    ser.close()
except Exception as e:
    print(f"Error: {e}")