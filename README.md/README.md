# Crowd-Responsive Antenna System

A Raspberry Pi + ESP32 system that detects WiFi device crowds and automatically rotates a directional antenna toward them.

## Features
- 📡 Detects devices connecting to Tenda "Smart" router
- 🔄 Automatically rotates stepper motor to optimal direction
- 📊 Logs all events for analysis
- ⚡ Power management with automatic shutdown

## Hardware
- Raspberry Pi 3
- ESP32 Dev Module
- A4988 Stepper Driver
- NEMA 17 Motor
- Tenda "Smart" Router

## Quick Start
1. Upload `hardware/esp32_code.ino` to ESP32
2. Run `python3 software/crowd_monitor.py`
3. Connect 4+ devices to trigger crowd detection

## Network Configuration
- Router SSID: Smart
- Password: aldard2004
- IP Range: 192.168.1.100-199
- Threshold: 4 devices

## Author
Eldard

## 🔧 Troubleshooting

### UART Communication Issues
If the motor isn't responding or crowd detection seems stuck:

1. **Test Pi ↔ ESP32 connection**:
   ```bash
   python3 software/debug_uart_ping.py