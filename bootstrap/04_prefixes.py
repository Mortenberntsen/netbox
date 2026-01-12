import csv
import os
import pynetbox

NETBOX_URL = "http://localhost:8000"
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

with open("data/prefixes.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        site = nb.dcim.sites.get(slug=row["site"].lower())

        role = nb.ipam.roles.get(name=row["role"])
        if not role:
            role = nb.ipam.roles.get(slug=row["role"].lower())

        if not site or not role:
            print(
                f"❌ Mangler site/role for {row['prefix']} "
                f"(site={row['site']}, role={row['role']})"
            )
            continue

        existing = nb.ipam.prefixes.get(prefix=row["prefix"])
        if existing:
            print(f"↺ Prefix finnes allerede: {row['prefix']}")
            continue

        nb.ipam.prefixes.create(
            prefix=row["prefix"],
            site=site.id,
            role=role.id,
            status="active",
            description=row.get("description", "")
        )

        print(f"✔ Prefix opprettet: {row['prefix']}")
