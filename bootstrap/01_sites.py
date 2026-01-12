import csv
import os
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt som miljøvariabel")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

with open("data/sites.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        existing = nb.dcim.sites.get(slug=row["slug"])
        if existing:
            print(f"↺ Finnes allerede: {row['name']}")
            continue

        nb.dcim.sites.create(
            name=row["name"],
            slug=row["slug"],
            description=row.get("description", ""),
            status="active"
        )

        print(f"✔ Opprettet site: {row['name']}")
