# Looks up geolocation and ISP info for a given IP address.
# Uses the free ip-api.com JSON endpoint — no API key required.

import requests

API_URL = "http://ip-api.com/json/{ip}"
TIMEOUT = 10


def lookup_ip(ip: str) -> str:
    response = requests.get(API_URL.format(ip=ip), timeout=TIMEOUT)
    response.raise_for_status()

    data = response.json()

    if data.get("status") == "fail":
        raise ValueError(f"Could not resolve IP: {data.get('message', 'unknown error')}")

    isp     = data.get("isp", "N/A")
    city    = data.get("city", "N/A")
    country = data.get("country", "N/A")
    lat     = data.get("lat", "N/A")
    lon     = data.get("lon", "N/A")

    return (
        f"ISP:          {isp}\n"
        f"City:         {city}, {country}\n"
        f"City Lat/Lon: ({lat}) / ({lon})"
    )
