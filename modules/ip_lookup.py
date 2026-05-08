# Looks up geolocation and ISP info for a given IP address.
# Uses the free ip-api.com JSON endpoint — no API key required.
# Private/reserved ranges (loopback, RFC1918, etc.) are handled locally
# without hitting the API, since ip-api.com rejects them.

import ipaddress
import requests

API_URL = "http://ip-api.com/json/{ip}"
TIMEOUT = 10


def _classify_reserved(ip: str) -> str | None:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return None
    if addr.is_loopback:
        return "Loopback"
    if addr.is_private:
        return "Private network"
    if addr.is_link_local:
        return "Link-local"
    if addr.is_multicast:
        return "Multicast"
    if addr.is_reserved:
        return "Reserved"
    return None


def lookup_ip(ip: str) -> str:
    # Handle reserved ranges before hitting the API
    kind = _classify_reserved(ip)
    if kind:
        return (
            f"ISP:          N/A ({kind} address)\n"
            f"City:         N/A\n"
            f"City Lat/Lon: N/A"
        )

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
