# Hardware Wiring Guide

## ESP32 ↔ A4988 Connections
| ESP32 Pin | A4988 Pin |
|-----------|-----------|
| GPIO 18   | STEP      |
| GPIO 19   | DIR       |
| GPIO 25   | MS1       |
| GPIO 26   | MS2       |
| GPIO 23   | MS3       |
| 3.3V      | RESET     |
| 3.3V      | SLEEP     |
| 3.3V      | VCC       |
| GND       | GND       |

## A4988 ↔ NEMA 17 Motor
| A4988 Pin | Motor Wire |
|-----------|------------|
| 1A        | Red        |
| 1B        | Green      |
| 2A        | Blue       |
| 2B        | Black      |

## Power Connections
- VMOT → 12V+ (external supply)
- GND → 12V- (and Pi GND)
- 100µF capacitor across VMOT and GND

## Pi ↔ ESP32 UART
| Pi GPIO | ESP32 Pin |
|---------|-----------|
| GPIO 14 | GPIO 16 (RX) |
| GPIO 15 | GPIO 17 (TX) |
| GND     | GND       |