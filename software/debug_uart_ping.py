#!/usr/bin/env python3
"""
DEBUG: Pi ↔ ESP32 UART Connectivity Test
----------------------------------------
Run this to verify serial communication is working.
Expected output:
  Sent: HELLO
  Received: ESP32 ACK: HELLO

If you see "No response", check:
  1. Wiring: Pi GPIO14→ESP32 GPIO16, Pi GPIO15→ESP32 GPIO17, GND↔GND
  2. Permissions: sudo usermod -a -G dialout,uucp aldard + logout/login
  3. Port: Try /dev/ttyS0 if /dev/serial0 fails
"""
import serial
import time
import sys

def test_uart_connection(port='/dev/serial0', baud=115200):
    """Test UART communication with ESP32"""
    try:
        ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # Stabilize connection
        
        # Send test message
        message = "HELLO\n"
        ser.write(message.encode('utf-8'))
        print(f"Sent: {message.strip()}")
        
        # Wait for response
        time.sleep(0.5)
        
        # Read and display response
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            print(f"Received: {response}")
            return "ESP32 ACK" in response
        else:
            print("Received: (No response from ESP32)")
            return False
            
    except serial.SerialException as e:
        print(f"❌ Serial Error: {e}")
        print("💡 Tip: Check wiring and run 'sudo usermod -a -G dialout,uucp aldard'")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
    finally:
        try:
            ser.close()
        except:
            pass

if __name__ == "__main__":
    print("🔌 Testing Pi ↔ ESP32 UART connection...")
    success = test_uart_connection()
    sys.exit(0 if success else 1)