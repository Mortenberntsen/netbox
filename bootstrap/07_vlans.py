import csv
import os
import pynetbox

NETBOX_URL = "http://localhost:8000"
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

with open("data/vlans.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        site = nb.dcim.sites.get(slug=row["site"].lower())
        if not site:
            print(f"❌ Mangler site for VLAN {row['vid']} ({row['name']})")
            continue

        existing = nb.ipam.vlans.get(
            vid=int(row["vid"]),
            site_id=site.id
        )

        if existing:
            print(f"↺ VLAN finnes allerede: {row['vid']} ({row['name']})")
            continue

        nb.ipam.vlans.create(
            vid=int(row["vid"]),
            name=row["name"],
            site=site.id,
            status="active",
            description=row.get("description", "")
        )

        print(f"✔ VLAN opprettet: {row['vid']} ({row['name']})")

