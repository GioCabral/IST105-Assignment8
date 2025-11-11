from django.shortcuts import render
from .forms import NetworkForm
import re, random, datetime, pymongo

client = pymongo.MongoClient("mongodb://172.31.88.168:27017/")
db = client["networkdb"]
leases = db["leases"]

def validate_mac(mac):
    return re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", mac)

def generate_ipv4():
    return f"192.168.1.{random.randint(2, 254)}"

def generate_ipv6(mac):
    parts = mac.split(":")
    eui64 = f"2001:db8::{'%02x%02x:ff:fe%02x%02x:%02x%02x' % tuple(int(x,16) for x in parts)}"
    return eui64

def home(request):
    if request.method == "POST":
        form = NetworkForm(request.POST)
        if form.is_valid():
            mac = form.cleaned_data["mac_address"]
            dhcp = form.cleaned_data["dhcp_version"]
            if not validate_mac(mac):
                return render(request, "network/result.html", {"error": "Invalid MAC format"})

            ip = generate_ipv4() if dhcp == "DHCPv4" else generate_ipv6(mac)
            record = {
                "mac_address": mac,
                "dhcp_version": dhcp,
                "assigned_ip": ip,
                "lease_time": "3600 seconds",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            leases.insert_one(record)
            return render(request, "network/result.html", {"record": record})
    else:
        form = NetworkForm()
    return render(request, "network/form.html", {"form": form})

def view_leases(request):
    records = list(leases.find({}, {"_id": 0}))
    return render(request, "network/leases.html", {"records": records})
