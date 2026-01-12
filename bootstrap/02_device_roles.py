import os
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt som miljøvariabel")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

ROLES = [
    "Client",
    "Laptop",
    "Network",
    "Router",
    "Server",
    "Workstation",
]

for role_name in ROLES:
    existing = nb.dcim.device_roles.get(name=role_name)
    if existing:
        print(f"↺ Role finnes allerede: {role_name}")
        continue

    nb.dcim.device_roles.create(
        name=role_name,
        slug=role_name.lower().replace(" ", "-"),
    )

    print(f"✔ Opprettet role: {role_name}")
