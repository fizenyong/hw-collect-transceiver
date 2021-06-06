# hw-collect-transceiver
Python script to collect optical module installed on Huawei S switch, and to parse into formatted csv file for asset tracking.

## Framework
Script created using:
* nornir: Inventory management and task multi-threading
* netmiko: SSH connection to device
* getpass: Prompt for device password at runtime
* TextFSM: CLI parsing to structured format
* ntc_template: TextFSM templates
* tqdm: Progress bar of task
* colorama: Print colored text to terminal
* csv: Write data to csv format

## Getting Started
1. Install dependency
```sh
pip install -r requirements.txt
```
2. Add the textfsm template definition and header to site-package ntc_templates
3. Create logs folder
```sh
mkdir -p logs
```

## How To Use
1. Set up device in `inventory/hosts.yaml`
```yaml
AD-MDF-AS-S5731-STACK-01:
  groups:
    - Test
  hostname: 192.168.1.1
```
2. Set up device details in `inventory/groups.yaml`
```yaml
Test:
  username: admin
  platform: huawei
```
3. Run the script
```
python ssh-collect-transceiver.py
python parse-transceiver.py
```

## Supported Device
Huawei VRP5 network devices. Tested on 300+ devices of:
* Huawei S5731-S of V200R019
* Huawei S5731-H of V200R019
* Huawei S6730-H of V200R019
* Huawei S12700E of V200R019

## How It Works
1. Establish SSH connection to devices
2. Send command `display transceiver` to get optical module information
3. Parse the CLI output to csv formatted file

## Device CLI Logging
Raw CLI stream output saved at logs folder
