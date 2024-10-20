# IoT Monitoring System with MQTT

This project provides a simple IoT monitoring system that simulates temperature readings, door lock status, and reacts to specific conditions by issuing commands such as locking the door or turning on the fan. The system is implemented using Python and MQTT for communication.

## Table of Contents
- [System Overview](#system-overview)
- [Installation](#installation)
- [Topics and Subscriptions](#topics-and-subscriptions)
- [Message Structure](#message-structure)
- [Command Structure](#command-structure)
- [Usage](#usage)
  
## System Overview
This project consists of two devices:
1. **Device 1**: Simulates sensor data (temperature and door lock status) and publishes the data to MQTT topics.
2. **Device 2**: Monitors the sensor data and issues commands when specific conditions are met:
   - **Lock the door** if multiple failed attempts occur on the smart lock.
   - **Turn on the fan** if the temperature exceeds 40°C.

Additionally, a simple **User Interface** is provided for monitoring the system by subscribing to all relevant topics and displaying the messages in a tabular format.

## Installation

To get started with this project, you'll need to install the required Python packages. 

### Required Packages
- `paho-mqtt`: For MQTT communication between devices.
- `tabulate`: For displaying data in a table format in the command-line interface (CLI).

### Commands to Install Dependencies

```
pip install paho-mqtt tabulate
```

## Topics and Subscriptions

### Topics Subscribed to by Device 2 and Monitoring Client:

| Topic | Description |
|-------|-------------|
| `<103819717>/temperature` | Publishes temperature data from Device 1. |
| `<103819717>/door` | Publishes door lock status and failed attempts from Device 1. |
| `<103819717>/commands/door` | Device 2 issues door lock commands (e.g., lock the door). |
| `<103819717>/commands/temperature` | Device 2 issues temperature-related commands (e.g., turn on the fan). |
| `public` | Can be used for general purpose/public messages. |

### Topics Published by Device 1:

| Topic | Description |
|-------|-------------|
| `<103819717>/temperature` | Publishes temperature readings every 5 seconds. |
| `<103819717>/door` | Publishes the door lock status (locked or failed) and number of failed attempts every 5 seconds. |

### Topics Published by Device 2:

| Topic | Description |
|-------|-------------|
| `<103819717>/commands/door` | Publishes commands to lock the door if multiple failed attempts are detected. |
| `<103819717>/commands/temperature` | Publishes commands to turn on the fan if the temperature exceeds 40°C. |

## Message Structure

### Temperature Message (Published by Device 1)
This message is published to `<103819717>/temperature`.

```json
{
  "sensor": "temperature",
  "value": 45.3,
  "unit": "°C",
  "timestamp": 1632767820.123456
}
```

- **sensor**: Type of sensor (temperature).
- **value**: Current temperature value (in degrees Celsius).
- **unit**: Unit of measurement for the temperature (°C).
- **timestamp**: UNIX timestamp of when the reading was generated.

### Door Lock Message (Published by Device 1)
This message is published to `<103819717>/door`.

```json
{
  "sensor": "door",
  "status": "failed",  // Can be 'locked' or 'failed'
  "attempts": 3,
  "timestamp": "2024-10-17 14:12:45"
}
```

- **sensor**: Type of sensor (door lock).
- **status**: Status of the door lock attempt (`locked` or `failed`).
- **attempts**: Number of attempts to lock the door.
- **timestamp**: Human-readable timestamp of the event.

## Command Structure

### Door Command (Published by Device 2)
This message is published to `<103819717>/commands/door` when Device 2 detects multiple failed door lock attempts.

```json
{
  "action": "lock_door",
  "failed_attempts": 3
}
```

- **action**: Command action (`lock_door`).
- **failed_attempts**: Number of failed attempts before the command was triggered.

### Temperature Command (Published by Device 2)
This message is published to `<103819717>/commands/temperature` when the temperature exceeds 40°C.

```json
{
  "action": "turn_on_fan",
  "temperature": 42.5
}
```

- **action**: Command action (`turn_on_fan`).
- **temperature**: Current temperature that triggered the command.

## Usage

### Device 1: Simulating Temperature and Door Lock Status
Device 1 simulates sensor data and publishes it to the respective topics. To start Device 1, run:

```bash
python device1.py
```

This will:
- Simulate temperature readings between 20°C and 50°C.
- Simulate door lock attempts (both successful and failed).
- Publish this data to `<103819717>/temperature` and `<103819717>/door` topics every 5 seconds.

### Device 2: Monitoring and Issuing Commands
Device 2 subscribes to the temperature and door status updates, and issues commands based on predefined conditions. To start Device 2, run:

```bash
python device2.py
```

This will:
- Monitor the temperature and door lock status.
- Issue a command to lock the door if there are 3 or more failed lock attempts.
- Issue a command to turn on the fan if the temperature exceeds 40°C.

### Monitoring Client: User Interface
The monitoring client provides a simple CLI-based user interface to display messages in real time. It subscribes to all relevant topics and displays the data in a tabular format.

To start the monitoring client, run:

```bash
python monitor.py
```

This will:
- Display temperature and door updates in a table.
- Show issued commands when conditions are met.

### Example Output in Monitoring Client:

```
[Received Message]: From topic '<103819717>/temperature'

Sensor       Value    Unit    Timestamp          
Temperature  42.35    °C      2024-10-17 14:12:45

[Received Message]: From topic '<103819717>/door'

Sensor  Status  Attempts  Timestamp          
Door    failed  3         2024-10-17 14:12:45

[Command Issued]: Door Action - lock_door, Details: {'action': 'lock_door', 'failed_attempts': 3}
```