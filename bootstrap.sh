#!/bin/bash
set -e

echo "🚀 Starter NetBox bootstrap"

# Last miljøvariabler hvis .env finnes
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ -z "$NETBOX_API_TOKEN" ]; then
  echo "❌ NETBOX_API_TOKEN er ikke satt"
  exit 1
fi

echo "🐳 Forutsetter at NetBox allerede kjører"



echo "⏳ Venter på NetBox API..."
until curl -s http://localhost:8000/api/ > /dev/null; do
  sleep 3
done

echo "✅ NetBox API er klar"

python3 bootstrap/01_sites.py
python3 bootstrap/02_device_roles.py
python3 bootstrap/03_device_types.py
python3 bootstrap/04_prefixes.py
python3 bootstrap/05_devices.py
python3 bootstrap/06_interfaces_ips.py

echo "🎉 Bootstrap ferdig – NetBox er klar!"
