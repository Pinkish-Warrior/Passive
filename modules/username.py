# Checks whether a username exists across multiple social platforms.
# requests-based for most platforms; Playwright (headless Chromium) for JS-heavy ones.

import multiprocessing
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

TIMEOUT = 10  # seconds (requests)
PW_TIMEOUT = 15000  # milliseconds (Playwright)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# method: "requests" or "playwright"
PLATFORMS = [
    {
        "name":       "GitHub",
        "url":        "https://github.com/{}",
        "probe_url":  "https://github.com/{}",
        "method":     "requests",
        "not_found":  ["Not Found"],
    },
    {
        "name":       "Reddit",
        "url":        "https://www.reddit.com/user/{}",
        "probe_url":  "https://www.reddit.com/user/{}/about.json",
        "method":     "requests",
        "not_found":  [],
    },
    {
        "name":        "Twitter/X",
        "url":         "https://twitter.com/{}",
        "probe_url":   "https://twitter.com/{}",
        "method":      "playwright",
        "not_found":   [],
        "not_found_title": ["profile / x"],  # generic title = account doesn't exist
    },
    {
        "name":       "TikTok",
        "url":        "https://www.tiktok.com/@{}",
        "probe_url":  "https://www.tiktok.com/@{}",
        "method":     "requests",
        "not_found":  ['"statusCode":10202', "couldn't find this account"],
    },
    {
        "name":        "Pinterest",
        "url":         "https://www.pinterest.com/{}",
        "probe_url":   "https://www.pinterest.com/{}",
        "method":      "playwright",
        "not_found":   [],
        "not_found_title": [],  # URL check handles it: ?show_error=true
    },
    {
        "name":        "Instagram",
        "url":         "https://www.instagram.com/{}",
        "probe_url":   "https://www.instagram.com/{}",
        "method":      "playwright",
        "not_found":   [],
        "not_found_title": ["profile isn't available"],
    },
    {
        "name":       "LinkedIn",
        "url":        "https://www.linkedin.com/in/{}",
        "probe_url":  "https://www.linkedin.com/in/{}",
        "method":     "requests",
        "not_found":  [],
    },
]


def _probe_requests(platform: dict, username: str) -> tuple[str, str, str]:
    url = platform["url"].format(username)
    probe_url = platform["probe_url"].format(username)
    try:
        r = requests.get(probe_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 404:
            return platform["name"], url, "no"
        if r.status_code == 200:
            body = r.text.lower()
            if any(hint.lower() in body for hint in platform["not_found"]):
                return platform["name"], url, "no"
            return platform["name"], url, "yes"
        return platform["name"], url, f"unknown ({r.status_code})"
    except requests.RequestException:
        return platform["name"], url, "error"


LOGIN_WALL_PATTERNS = [
    "twitter.com/i/flow/login",
    "x.com/i/flow/login",
    "x.com/i/flow/signup",
    "accounts.instagram.com/login",
    "instagram.com/accounts/login",
    "pinterest.com/login",
]

NOT_FOUND_URL_PATTERNS = [
    "pinterest.com/?show_error=true",
]


def _probe_playwright_page(browser, platform: dict, username: str) -> tuple[str, str, str]:
    # Accepts a shared browser instance — avoids re-launching Chromium per probe
    url = platform["url"].format(username)
    try:
        page = browser.new_page(extra_http_headers=HEADERS)
        try:
            page.goto(url, timeout=PW_TIMEOUT, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass  # some SPAs never reach networkidle
            final_url = page.url.lower()
            if any(pattern in final_url for pattern in LOGIN_WALL_PATTERNS):
                return platform["name"], url, "requires auth"
            if any(pattern in final_url for pattern in NOT_FOUND_URL_PATTERNS):
                return platform["name"], url, "no"
            title = page.title().lower()
            if any(hint.lower() in title for hint in platform.get("not_found_title", [])):
                return platform["name"], url, "no"
            body = page.content().lower()
            if any(hint.lower() in body for hint in platform["not_found"]):
                return platform["name"], url, "no"
            return platform["name"], url, "yes"
        finally:
            page.close()
    except Exception:
        return platform["name"], url, "error"


def _pw_worker(result_queue, pw_platforms, username):
    pw_results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for p in pw_platforms:
                name, url, status = _probe_playwright_page(browser, p, username)
                pw_results[name] = (url, status)
            browser.close()
    except Exception:
        pass
    result_queue.put(pw_results)


def lookup_username(username: str) -> str:
    username = username.lstrip("@")

    results = {}

    # Run requests-based probes in parallel
    requests_platforms = [p for p in PLATFORMS if p["method"] == "requests"]
    with ThreadPoolExecutor(max_workers=len(requests_platforms)) as executor:
        futures = {executor.submit(_probe_requests, p, username): p["name"] for p in requests_platforms}
        for future in as_completed(futures):
            name, url, status = future.result()
            results[name] = (url, status)

    # Run Playwright probes in a child process — multiprocessing allows a hard
    # terminate/kill if Playwright hangs at the OS level, which threads cannot do.
    pw_platforms = [p for p in PLATFORMS if p["method"] == "playwright"]
    if pw_platforms:
        q = multiprocessing.Queue()
        proc = multiprocessing.Process(
            target=_pw_worker, args=(q, pw_platforms, username), daemon=True
        )
        proc.start()
        proc.join(timeout=90)
        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=3)
            if proc.is_alive():
                proc.kill()

        try:
            pw_results = q.get_nowait()
        except Exception:
            pw_results = {}

        for p in pw_platforms:
            url = p["url"].format(username)
            results[p["name"]] = pw_results.get(p["name"], (url, "error"))

    lines = [f"Username: @{username}\n"]
    for p in PLATFORMS:
        url, status = results[p["name"]]
        tag = f"[{status}]"
        lines.append(f"  {tag:<14} {url}")

    return "\n".join(lines)
