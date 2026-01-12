import csv
import os
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt som miljøvariabel")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

with open("data/devices.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        site = nb.dcim.sites.get(name=row["site"])
        role = nb.dcim.device_roles.get(name=row["role"])
        device_type = nb.dcim.device_types.get(model=row["type"])

        if not site or not role or not device_type:
            print(f"❌ Mangler site/role/type for {row['hostname']}")
            continue

        existing = nb.dcim.devices.get(
            name=row["hostname"],
            site_id=site.id
        )

        if existing:
            print(f"↺ Finnes allerede: {row['hostname']}")
            continue

        nb.dcim.devices.create(
            name=row["hostname"],
            site=site.id,
            role=role.id,
            device_type=device_type.id,
            serial=row["serial"],
            status="active",
            comments=f"OS: {row['os']} | {row['comment']}"
        )

        print(f"✔ Opprettet {row['hostname']}")
