# Virtual Gas Meter for Home Assistant

## Overview

The **Virtual Gas Meter** is a Home Assistant integration designed to track gas consumption. It supports two operating modes:

1. **Boiler/Furnace Tracking Mode**: Estimates gas consumption based on boiler runtime and average gas usage rate. Users can periodically enter real meter readings to improve accuracy.

2. **Monthly Bill Entry Mode**: Simple tracking by entering gas meter readings from your utility bills. Ideal for users who want to track usage without a smart boiler sensor.

The integration supports both **metric (m³)** and **imperial (CCF)** unit systems.

## Features

- **Dual Operating Modes**: Choose between boiler tracking or simple bill entry
- **Unit System Support**: Works with metric (m³) or imperial (CCF) units
- **Virtual Gas Meter Calculation**: Estimates gas consumption using time-based calculations (boiler mode)
- **Sensor Integration**: Creates Home Assistant sensors to track gas usage
- **Manual Data Entry**: Enter real gas meter readings from utility bills
- **Historical Data Tracking**: Stores consumption history with cumulative totals
- **JSON-based Storage**: Uses Home Assistant's native storage system
- **UI-based Configuration**: Easy setup through Home Assistant's integration flow

## Installation

### Install via HACS (Recommended)
1. **Ensure HACS is installed** in your Home Assistant instance.
2. **Add the Custom Repository:**
   - Open HACS in Home Assistant.
   - Navigate to `Integrations` and click the three-dot menu.
   - Select `Custom Repositories`.
   - Add the repository URL: `https://github.com/lukepatrick/virtual_gas_meter`.
   - Choose `Integration` as the category and click `Add`.
3. **Download the Integration:**
   - Search for `Virtual Gas Meter` in HACS and download it.
   - Restart Home Assistant to apply changes.

### Manual Installation
1. Download the repository as a ZIP file and extract it.
2. Copy the `custom_components/gas_meter` folder into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

### Adding the Integration
1. Navigate to **Settings** > **Devices & Services**.
2. Click **"Add Integration"** and search for `Virtual Gas Meter`.
3. **Step 1 - Basic Setup:**
   - Select your **Unit System**: Metric (m³) or Imperial (CCF)
   - Select your **Operating Mode**: Boiler/Furnace Tracking or Monthly Bill Entry
4. **Step 2 - Mode-specific Setup:**
   - **Boiler Tracking**: Select your boiler switch entity, enter average gas consumption per hour, and optionally enter current meter reading
   - **Bill Entry**: Optionally enter your current meter reading
5. Click **"Submit"**.

### Sensors Created

#### Bill Entry Mode
- **Gas Consumption Data**: Displays your gas readings and tracks cumulative usage

#### Boiler Tracking Mode
- **Gas Consumption Data**: Displays your gas readings and tracks cumulative usage
- **Consumed Gas**: Real-time estimated gas consumption based on boiler runtime
- **Gas Meter Latest Update**: Timestamp of last meter reading
- **Heating Interval**: Tracks boiler "on" time since last update

## Services

### `gas_meter.enter_bill_reading`
**For Bill Entry Mode** - Enter a gas meter reading from your utility bill.

- **Fields:**
  - `billing_date`: The billing date or meter reading date
  - `meter_reading`: The meter reading value in your configured unit (m³ or CCF)

- **Service Call Example:**
  ```yaml
  service: gas_meter.enter_bill_reading
  data:
    billing_date: "2025-11-01"
    meter_reading: 1234.56
  ```

### `gas_meter.trigger_gas_update`
**For Boiler Tracking Mode** - Update the virtual gas meter with a real meter reading to improve accuracy.

- **Why use this?**
  - The virtual gas meter **estimates** gas consumption using the average rate
  - By entering real readings, the system **adjusts** the average gas consumption for better accuracy
  - If no real readings are provided, the virtual gas meter relies on the initial average entered during setup

- **Fields:**
  - `datetime`: Timestamp for the gas reading (format: `YYYY-MM-DD HH:MM`)
  - `consumed_gas`: Gas meter reading in your configured unit (m³ or CCF)

- **Service Call Example:**
  ```yaml
  service: gas_meter.trigger_gas_update
  data:
    datetime: "2025-02-12 15:51"
    consumed_gas: 4447.816
  ```

### `gas_meter.read_gas_actualdata_file`
Reads and refreshes the stored gas meter data.

- **Service Call Example:**
  ```yaml
  service: gas_meter.read_gas_actualdata_file
  ```

## Data Storage

Gas consumption data is stored in Home Assistant's `.storage` directory as `gas_meter_data` (JSON format). Data is always stored internally in cubic meters (m³) for consistency, and converted to your display unit automatically.

## Code Overview

The integration consists of the following files:

| File | Description |
|------|-------------|
| `__init__.py` | Integration setup, service registration, and data persistence |
| `sensor.py` | Sensor entities for gas tracking |
| `config_flow.py` | UI-based configuration flow |
| `unit_converter.py` | Unit conversion utilities (m³ ↔ CCF) |
| `datetime_handler.py` | Date/time parsing and conversion |
| `file_handler.py` | JSON-based storage using Home Assistant Store |
| `gas_consume.py` | Gas consumption record management |
| `const.py` | Constants and default values |
| `manifest.json` | Integration metadata |
| `services.yaml` | Service definitions |
| `translations/en.json` | UI translations |

## Dashboard Examples

### Bill Entry Mode - Simple Dashboard
```yaml
type: vertical-stack
title: Gas Meter
cards:
  - type: entities
    entities:
      - entity: sensor.gas_consumption_data
  - type: markdown
    title: Gas Readings History
    content: >
      {% set readings = state_attr('sensor.gas_consumption_data', 'records') %}
      {% if readings %}
        {% for record in readings | reverse %}
        - {{ record.datetime }}: {{ record.consumed_gas }} (cumulative: {{ record.consumed_gas_cumulated }})
        {% endfor %}
      {% else %}
        No gas meter data available.
      {% endif %}
```

### Boiler Tracking Mode - Full Dashboard

#### Virtual Gas Meter Data Section
```yaml
type: vertical-stack
cards:
  - type: entities
    entities:
      - entity: sensor.consumed_gas
      - entity: sensor.gas_meter_latest_update
      - entity: sensor.heating_interval_2
title: Virtual Gas Meter
```

#### Enter Actual Gas Meter Data Section
For detailed boiler tracking dashboard setup including automations and helpers, see the [Boiler Tracking Dashboard Guide](docs/boiler-dashboard.md).

## Usage

### Bill Entry Mode
1. Configure the integration with "Monthly Bill Entry" mode
2. When you receive your utility bill, use **Developer Tools → Services → gas_meter.enter_bill_reading**
3. Enter the billing date and meter reading
4. View your consumption history in the Gas Consumption Data sensor

### Boiler Tracking Mode
1. Configure the integration with "Boiler/Furnace Tracking" mode
2. Select your boiler switch entity
3. Monitor real-time estimated consumption via the "Consumed Gas" sensor
4. Periodically enter real meter readings to improve accuracy

## Upgrading from v1.x

Version 2.0 introduces several changes:
- **Data Migration**: Existing pickle-based storage is automatically migrated to JSON
- **New Config Flow**: You may need to reconfigure the integration to access new features
- **Unit Selection**: Imperial (CCF) units are now supported

## Support & Issues

For any issues or feature requests, please visit the [GitHub Issue Tracker](https://github.com/lukepatrick/virtual_gas_meter/issues).

## Credits

This project is a fork of the original [Virtual Gas Meter](https://github.com/Elbereth7/virtual_gas_meter) by [@Elbereth7](https://github.com/Elbereth7).

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues in the GitHub repository.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
