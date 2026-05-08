# Looks up a person across public directories in France, UK, and Brazil.
# France : Pages Blanches (pagesjaunes.fr)  — full address + phone
# UK     : 192.com                          — name + area + electoral-roll year
# Brazil : no free public directory available (telelistas.net is offline)
#
# Uses Playwright for both sources because results are JS-rendered.
# Falls back gracefully if a source is unreachable or returns nothing.

import re
from urllib.parse import quote, quote_plus

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

PW_TIMEOUT = 20000   # ms — page navigation
NI_TIMEOUT = 8000    # ms — networkidle wait

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

FR_URL = "https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={name}&ou="
UK_URL = "https://www.192.com/people/search/?firstname={first}&surname={last}"

MAX_RESULTS  = 5
FR_SKIP      = {"Voir le plan", "Afficher le N°"}


# ── shared ───────────────────────────────────────────────────────────────────

def _pw_fetch(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(extra_http_headers=HEADERS)
        page.goto(url, timeout=PW_TIMEOUT, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=NI_TIMEOUT)
        except Exception:
            pass
        html = page.content()
        browser.close()
    return html


# ── France ───────────────────────────────────────────────────────────────────

def _fr_address(card) -> str:
    div = card.select_one(".bi-address")
    if not div:
        return "N/A"
    parts = [t.strip() for t in div.find_all(string=True, recursive=True)
             if t.strip() and t.strip() not in FR_SKIP]
    return " ".join(parts) or "N/A"


def _fr_phone(card) -> str:
    div = card.select_one(".number-contact")
    if not div:
        return "N/A"
    match = re.search(r'0\d(?:[\s.\-]?\d{2}){4}', div.get_text(" ", strip=True))
    return match.group(0).strip() if match else "N/A"


def _lookup_france(full_name: str) -> list[dict]:
    try:
        html = _pw_fetch(FR_URL.format(name=quote_plus(full_name)))
    except Exception:
        return []
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for card in soup.select("li[class*='bi']")[:MAX_RESULTS]:
        tag = card.select_one("h3")
        name = tag.get_text(strip=True) if tag else None
        if name:
            results.append({"name": name, "address": _fr_address(card), "phone": _fr_phone(card)})
    return results


# ── UK ───────────────────────────────────────────────────────────────────────

def _lookup_uk(first: str, last: str) -> list[dict]:
    url = UK_URL.format(first=quote(first), last=quote(last))
    try:
        html = _pw_fetch(url)
    except Exception:
        return []
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for card in soup.select("li.ont-people-premium-result-item")[:MAX_RESULTS]:
        name_tag = card.select_one(".test-name")
        addr_tag = card.select_one(".test-address")
        er_tag   = card.select_one(".test-er-years")
        name = name_tag.get_text(strip=True) if name_tag else None
        if name:
            results.append({
                "name": name,
                "area": addr_tag.get_text(strip=True) if addr_tag else "N/A",
                "er":   er_tag.get_text(strip=True)   if er_tag   else "N/A",
            })
    return results


# ── output ───────────────────────────────────────────────────────────────────

def _section(title: str, lines: list[str]) -> str:
    return f"[{title}]\n" + "\n".join(lines)


def lookup_fullname(full_name: str) -> str:
    parts = full_name.strip().split()
    if len(parts) < 2:
        raise ValueError('Full name must be "First Last" — e.g., "Jean Dupont"')

    first = parts[0]
    last  = " ".join(parts[1:])

    header = (
        f"Full Name:  {full_name}\n"
        f"First:      {first}\n"
        f"Last:       {last}\n"
    )

    sections = []

    # France
    fr = _lookup_france(full_name)
    if fr:
        lines = []
        for i, r in enumerate(fr, 1):
            lines += [f"  Result {i}:", f"    Name:    {r['name']}",
                      f"    Address: {r['address']}", f"    Phone:   {r['phone']}"]
            if i < len(fr):
                lines.append("")
        sections.append(_section("France — Pages Blanches", lines))
    else:
        sections.append(_section("France — Pages Blanches", ["  No results found."]))

    # UK
    uk = _lookup_uk(first, last)
    if uk:
        lines = []
        for i, r in enumerate(uk, 1):
            lines += [f"  Result {i}:", f"    Name:    {r['name']}",
                      f"    Area:    {r['area']}", f"    ER:      {r['er']}"]
            if i < len(uk):
                lines.append("")
        lines += ["", "  * Full address requires a free account at 192.com"]
        sections.append(_section("UK — 192.com", lines))
    else:
        sections.append(_section("UK — 192.com", ["  No results found."]))

    # Brazil
    sections.append(_section(
        "Brazil",
        ["  No free public directory available — telelistas.net is offline."]
    ))

    return header + "\n" + "\n\n".join(sections)
