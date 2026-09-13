# MedNet-Sentinel-Splunk

A simulated hospital security monitoring project demonstrating SOC detection of a multi-stage insider/device compromise using **Splunk Search Processing Language (SPL)**.

## Project Overview

This project simulates a realistic healthcare network and generates mock security logs (network firewall, IAM authentication, and EHR access) to demonstrate how Splunk can be used to detect and correlate a **three-stage security attack chain** against a hospital:

1. **Rogue IoT Device Beacon** — A rogue medical device on the hospital network beacons out to an external command-and-control IP.
2. **Compromised Nurse Credentials** — A nurse's account logs in from an anomalous overseas location with MFA bypassed (Zero-Trust violation).
3. **EHR Data Exfiltration** — The compromised account performs a massive bulk export of electronic health records.

## Folder Structure

```
MedNet-Sentinel-Splunk/
├── searches/                  # Splunk SPL query files
│   ├── iot_beacon_detection.spl
│   ├── compromised_mfa_login.spl
│   └── ehr_data_exfiltration.spl
├── reports/
│   └── screenshots/           # Placeholder for Splunk query result screenshots
├── mock_data/                 # Simulated log files (generated, matched to screenshots)
│   ├── network_firewall.log
│   ├── iam_auth.log
│   └── ehr_access.log
├── generate_hospital_logs.py  # Script to regenerate the mock logs
├── reset.sql                  # SQL to reset the lab database (if applicable)
└── README.md
```

## How to Use

### 1. Generate the mock logs

```bash
python generate_hospital_logs.py
```

This creates the three log files in the `mock_data/` folder. The existing logs in this repo are **frozen on purpose** — they match the query results in the screenshots, so do not regenerate them unless you intend to re-take the screenshots.

### 2. Load the data into Splunk

Upload each log file in `mock_data/` into Splunk and assign the following index names so the SPL queries match:

| Log File                | Splunk Index    |
| ----------------------- | --------------- |
| `network_firewall.log`  | `hospital_net`  |
| `iam_auth.log`          | `hospital_iam`  |
| `ehr_access.log`        | `hospital_ehr`  |

### 3. Run the SPL searches

Each file in `searches/` is a ready-to-run Splunk search. Open the search app, paste the query, and run against the appropriate index (sub-second time range).

## Detection Queries (Attack Chain)

### Stage 1 — Rogue IoT Device Beacon
```spl
index="hospital_net" action="ALERT_EXTERNAL_BEACON" | table _time, src_ip, mac_address, dest_ip, bytes_transferred
```
📌 **What it detects:** A rogue IoT device (`10.20.4.99`, MAC `EE:FF:AA:BB:CC:DD`) beaconing large amounts of data (~85 KB/event) to an external IP `198.51.100.45` outside the hospital network.

### Stage 2 — Compromised MFA Login
```spl
index="hospital_iam" status="success" mfa_status="BYPASSED" | table _time, user_id, user_role, src_ip, geo_location
```
📌 **What it detects:** The nurse account `nurse_jdoe_2` logging in successfully from an unknown overseas location (`203.0.113.42`) with MFA bypassed — a classic Zero-Trust / Impossible Travel anomaly.

### Stage 3 — EHR Data Exfiltration
```spl
index="hospital_ehr" action="BULK_EXPORT" | stats sum(records_viewed_count) as total_records_stolen by user_id
```
📌 **What it detects:** The same compromised account `nurse_jdoe_2` rapidly viewing a massive number of patient records. The summed output shows **450 records stolen** — a critical data breach magnitude.

## Lab / Simulated Environment

This repo contains mock data only. It is intended for:
- Cyber security training & SOC analyst practice
- Detecting & correlating multi-stage attack chains
- Demonstrating Zero-Trust and IoT security monitoring concepts
- Building Splunk dashboards and alerts based on realistic healthcare data

## Disclaimer

All IP addresses, MAC addresses, user IDs, and patient records are **simulated/fictional** and generated for educational purposes only. No real patient data is used.

## License

Educational use only.
