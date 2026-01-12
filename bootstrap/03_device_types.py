import os
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("NETBOX_API_TOKEN er ikke satt som miljøvariabel")

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

# Sørg for at Manufacturer finnes
manufacturer = nb.dcim.manufacturers.get(name="Generic")
if not manufacturer:
    manufacturer = nb.dcim.manufacturers.create(
        name="Generic",
        slug="generic"
    )
    print("✔ Opprettet manufacturer: Generic")
else:
    print("↺ Manufacturer finnes allerede: Generic")

DEVICE_TYPES = [
    "Generic Server",
    "Generic PC",
    "Generic Laptop",
    "Generic Router",
]

for model in DEVICE_TYPES:
    existing = nb.dcim.device_types.get(model=model)
    if existing:
        print(f"↺ Device type finnes allerede: {model}")
        continue

    nb.dcim.device_types.create(
        model=model,
        slug=model.lower().replace(" ", "-"),
        manufacturer=manufacturer.id,
    )

    print(f"✔ Opprettet device type: {model}")
