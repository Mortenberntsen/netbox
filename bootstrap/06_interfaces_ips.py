import csv
import os
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt som miljøvariabel")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

with open("data/interfaces_ips.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        device = nb.dcim.devices.get(name=row["hostname"])
        if not device:
            print(f"❌ Fant ikke device: {row['hostname']}")
            continue

        # Interface
        interface = nb.dcim.interfaces.get(
            device_id=device.id,
            name=row["interface"]
        )

        if not interface:
            interface = nb.dcim.interfaces.create(
                device=device.id,
                name=row["interface"],
                type=row["interface_type"]
            )
            print(f"✔ Opprettet interface {row['interface']} på {row['hostname']}")
        else:
            print(f"↺ Interface finnes allerede: {row['interface']} på {row['hostname']}")

        # IP-adresse
        ip = nb.ipam.ip_addresses.get(address=row["ip"])
        if ip:
            print(f"↺ IP finnes allerede: {row['ip']}")
            continue

        nb.ipam.ip_addresses.create(
            address=row["ip"],
            assigned_object_type="dcim.interface",
            assigned_object_id=interface.id,
            status="active"
        )

        print(f"✔ Tildelte IP {row['ip']} til {row['hostname']}")
