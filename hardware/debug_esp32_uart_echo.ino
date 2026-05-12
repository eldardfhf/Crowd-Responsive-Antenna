#include <AccelStepper.h>

// Pin Definitions
#define STEP_PIN 18
#define DIR_PIN 19
#define MS1_PIN 25
#define MS2_PIN 26
#define MS3_PIN 23

// Create stepper instance
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
  // Stabilize pins to prevent jitter
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);

  // Configure microstepping (1/16 step)
  pinMode(MS1_PIN, OUTPUT);
  pinMode(MS2_PIN, OUTPUT);
  pinMode(MS3_PIN, OUTPUT);
  digitalWrite(MS1_PIN, HIGH);
  digitalWrite(MS2_PIN, HIGH);
  digitalWrite(MS3_PIN, HIGH);

  // Initialize UART for Pi communication (115200 baud)
  Serial2.begin(115200, SERIAL_8N1, 16, 17);
  
  // USB Serial for debugging
  Serial.begin(115200);

  // Configure stepper
  stepper.setMaxSpeed(500);
  stepper.setAcceleration(250);

  delay(1000);
  Serial.println("✅ ESP32 Ready - Listening for ROTATE commands");
  Serial2.println("ESP32_READY");
}

void loop() {
  // Check for incoming commands from Pi
  if (Serial2.available()) {
    String msg = Serial2.readStringUntil('\n');
    msg.trim();  // Remove whitespace
    
    Serial.print("📥 Received from Pi: ");
    Serial.println(msg);
    
    // Handle ROTATE command
    if (msg.startsWith("ROTATE ")) {
      // Extract angle number
      int angle = msg.substring(7).toInt();
      
      Serial.print("🔄 Rotating to ");
      Serial.print(angle);
      Serial.println("°...");
      
      // Perform rotation
      rotateTo(angle);
      
      // Send acknowledgment back to Pi
      Serial2.println("ROTATED");
      Serial.println("✅ Sent: ROTATED");
    }
    // Handle HELLO command (for testing)
    else if (msg == "HELLO") {
      Serial2.println("ESP32_ACK: HELLO");
      Serial.println("Sent: ESP32_ACK: HELLO");
    }
    // Handle unknown commands
    else {
      Serial2.println("UNKNOWN_COMMAND");
      Serial.print("⚠️ Unknown command: ");
      Serial.println(msg);
    }
  }
}

void rotateTo(int targetAngle) {
  // Calculate steps: 200 steps/rev * 16 microsteps = 3200 steps/rev
  long steps = map(targetAngle, 0, 360, 0, 3200);
  
  stepper.moveTo(steps);
  
  // Run until target is reached
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
  
  Serial.print("   Motor reached ");
  Serial.print(targetAngle);
  Serial.println("°");
}