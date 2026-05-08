/**
 * DEBUG: ESP32 UART Echo for Pi Communication Test
 * ------------------------------------------------
 * Upload this to ESP32 to enable simple ping/pong testing with Raspberry Pi.
 * 
 * Wiring:
 *   Pi GPIO 14 (TX) → ESP32 GPIO 16 (RX)
 *   Pi GPIO 15 (RX) → ESP32 GPIO 17 (TX)
 *   Pi GND          → ESP32 GND
 * 
 * Usage:
 *   1. Upload this code to ESP32 via Arduino IDE
 *   2. Run software/debug_uart_ping.py on Pi
 *   3. Expected: "Sent: HELLO" → "Received: ESP32 ACK: HELLO"
 * 
 * Serial Monitor (115200 baud) shows debug output for troubleshooting.
 */

#define RXD2 16  // ESP32 RX pin (connects to Pi TX)
#define TXD2 17  // ESP32 TX pin (connects to Pi RX)

void setup() {
  // Initialize USB serial for debugging
  Serial.begin(115200);
  
  // Initialize UART2 for Pi communication
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
  
  delay(1000);  // Let connections stabilize
  Serial.println("✅ ESP32 Ready - Listening on Serial2 (GPIO 16/17)");
}

void loop() {
  // Check for messages from Pi
  if (Serial2.available()) {
    // Read the message (up to newline)
    String msg = Serial2.readStringUntil('\n');
    
    // Echo back to Pi with acknowledgment
    Serial2.println("ESP32 ACK: " + msg);
    
    // Print to USB Serial Monitor for debugging
    Serial.print("📥 From Pi: ");
    Serial.println(msg);
    Serial.print("📤 Reply: ESP32 ACK: ");
    Serial.println(msg);
  }
}