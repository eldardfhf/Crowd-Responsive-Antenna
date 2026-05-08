#include <AccelStepper.h>

// ✅ CRITICAL: All pin definitions MUST be at the top
#define STEP_PIN 18
#define DIR_PIN 19
#define MS1_PIN 25
#define MS2_PIN 26
#define MS3_PIN 23

// Create stepper instance (STEP/DIR mode)
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
  // ✅ CRITICAL: Stabilize pins FIRST to prevent power-up jitter
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);   // Hold STEP firmly LOW
  digitalWrite(DIR_PIN, LOW);    // Hold DIR firmly LOW

  // Configure microstepping pins (1/16 step = smoothest)
  pinMode(MS1_PIN, OUTPUT);
  pinMode(MS2_PIN, OUTPUT);
  pinMode(MS3_PIN, OUTPUT);
  digitalWrite(MS1_PIN, HIGH);
  digitalWrite(MS2_PIN, HIGH);
  digitalWrite(MS3_PIN, HIGH);

  // Initialize UART for Pi communication
  Serial2.begin(115200, SERIAL_8N1, 16, 17);

  // Configure stepper movement
  stepper.setMaxSpeed(500);
  stepper.setAcceleration(250);

  Serial2.println("ESP32 Ready - Control Pins Stabilized");
}

void loop() {
  if (Serial2.available()) {
    String msg = Serial2.readStringUntil('\n');
    msg.trim();  // Remove whitespace/newline

    if (msg.startsWith("ROTATE ")) {
      int angle = msg.substring(7).toInt();
      rotateTo(angle);
      Serial2.println("ROTATED");
    }
    else if (msg == "HELLO") {
      Serial2.println("ESP32_ACK: HELLO");
    }
    else if (msg == "POWER OFF") {
      Serial2.println("POWER OFF ACKNOWLEDGED");
    }
  }
}

void rotateTo(int targetAngle) {
  // 200 steps/rev * 16 microsteps = 3200 steps/rev = 360°
  long steps = map(targetAngle, 0, 360, 0, 3200);
  
  stepper.moveTo(steps);
  
  // Run until target is reached
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}