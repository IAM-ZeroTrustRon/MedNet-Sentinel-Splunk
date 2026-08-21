import csv
import random
import sys
from datetime import datetime, timedelta

# Ensure UTF-8 output so the ✅ emoji prints correctly on Windows (cp1252 console)
sys.stdout.reconfigure(encoding='utf-8')

def generate_logs():
    print("Generating simulated hospital security logs...")

    # 1. Network Firewall Logs (Medical IoT Focus)
    firewall_file = "mock_data/network_firewall.log"
    with open(firewall_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["_time", "src_ip", "mac_address", "dest_ip", "dest_port", "bytes_transferred", "action"])
        
        base_time = datetime.now() - timedelta(hours=6)
        
        # Normal medical devices (Infusion Pumps, Patient Monitors)
        for i in range(150):
            t = base_time + timedelta(minutes=i*2)
            ip = f"10.20.4.{random.randint(10, 50)}"
            mac = f"00:1A:2B:3C:4D:{random.randint(10, 99)}"
            writer.writerow([t.isoformat(), ip, mac, "10.20.1.100", 443, random.randint(500, 2000), "ALLOW"])

        # Rogue IoT Device injecting malicious traffic at 2:00 AM
        rogue_time = base_time + timedelta(hours=3)
        for i in range(30):
            t = rogue_time + timedelta(seconds=i*30)
            writer.writerow([t.isoformat(), "10.20.4.99", "EE:FF:AA:BB:CC:DD", "198.51.100.45", 443, 85000, "ALERT_EXTERNAL_BEACON"])

    # 2. IAM Authentication Logs (Privileged Access / Zero Trust Focus)
    iam_file = "mock_data/iam_auth.log"
    with open(iam_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["_time", "user_id", "user_role", "src_ip", "geo_location", "mfa_status", "action", "status"])

        for i in range(50):
            t = base_time + timedelta(minutes=i*7)
            writer.writerow([t.isoformat(), f"nurse_jdoe_{random.randint(1,5)}", "Nurse", "10.20.5.15", "Philadelphia, US", "VERIFIED", "login", "success"])

        # Compromised Nurse Account logging in from an anomalous overseas location
        compromised_time = rogue_time + timedelta(minutes=10)
        writer.writerow([compromised_time.isoformat(), "nurse_jdoe_2", "Nurse", "203.0.113.42", "Unknown, Overseas", "BYPASSED", "login", "success"])

    # 3. EHR Access Logs (Simulating the Healthcare Breach)
    ehr_file = "mock_data/ehr_access.log"
    with open(ehr_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["_time", "user_id", "patient_record_id", "action", "records_viewed_count"])

        # Normal clinical viewing pattern (1-2 records at a time)
        for i in range(40):
            t = base_time + timedelta(minutes=i*5)
            writer.writerow([t.isoformat(), "nurse_jdoe_1", f"PRN-{random.randint(10000, 10050)}", "VIEW", 1])

        # Massive data exfiltration spike by the compromised account
        exfil_time = compromised_time + timedelta(minutes=5)
        for i in range(1, 451):
            t = exfil_time + timedelta(seconds=i*2)
            writer.writerow([t.isoformat(), "nurse_jdoe_2", f"PRN-{20000 + i}", "BULK_EXPORT", i])

    print("✅ Success! Mock logs generated in the /mock_data folder:")
    print(" - mock_data/network_firewall.log")
    print(" - mock_data/iam_auth.log")
    print(" - mock_data/ehr_access.log")

if __name__ == "__main__":
    generate_logs()