See [SETUP.md](SETUP.md#audit) for instructions on how to run the automated audit script.

---

## General Questions — Answers

### Is the student able to explain clearly the used investigative methods?

Yes. Three distinct methods are used depending on the flag:

- **`-ip`** — A single HTTP GET request is sent to the free `ip-api.com` JSON endpoint. The response includes the city, region, country, ISP, and geographic coordinates. No API key or authentication is required.
- **`-u`** — For most platforms (GitHub, Reddit, TikTok, LinkedIn) a standard HTTP GET is issued to the profile URL; an HTTP 200 confirms the account exists and a 404 confirms it does not. For JavaScript-heavy platforms (Twitter/X, Instagram, Pinterest) a Playwright headless Chromium browser loads the page fully before the result is evaluated.
- **`-fn`** — Both Pages Blanches (France) and 192.com (UK) build their search results entirely in JavaScript, so a raw HTTP request would return an empty page. Playwright navigates to the search URL, waits for the DOM to settle, and then BeautifulSoup parses the rendered HTML to extract names, addresses, and phone numbers.

All three methods rely exclusively on public sources — no login, no scraping of private data, and no direct contact with the target.

---

### Is the student able to explain clearly what OSINT means?

Yes. OSINT stands for **Open Source Intelligence** — collecting information about a target using only publicly available sources, with no direct interaction with the target system. Sources include public directories, social media, DNS records, IP geolocation databases, and government registries. It is typically the first phase of a penetration test: the more that is known about a target before any active probing begins, the more precise and effective the rest of the engagement becomes. It is also entirely passive — the target has no way to detect that reconnaissance is taking place.

---

### Is the student able to explain clearly how his program works?

Yes. The program is invoked from the terminal as `passive` followed by exactly one flag and its argument:

```
passive -fn "Jean Dupont"
passive -ip 8.8.8.8
passive -u "@someuser"
```

Internally:

1. `passive.py` parses arguments with `argparse` using a mutually exclusive group, so only one flag is accepted per run.
2. The matching lookup function is called: `lookup_ip()`, `lookup_username()`, or `lookup_fullname()`.
3. The function fetches data from its source(s), parses the response, and returns a formatted result string.
4. The result is printed to the terminal.
5. `output.py` writes the result to `output/result.txt`. If that file already exists, it increments the suffix (`result2.txt`, `result3.txt`, …) until a free filename is found, so no previous result is ever overwritten.

Files that must be inside your repository:

- Your program source code.

- A README.md file, which clearly explains how to use the program.

###### Are the required files present?

##### Ask the student to present his program to you by doing 3 tests

###### Is the information entered as an argument a full name, an IP address, and a username?

##### Try flag "-fn" with the following command `passive -fn "Jean Dupont"`

###### Does the program display the address, and the telephone number for the full name entered?

##### Try flag "-ip" with the following command `passive -ip 127.0.0.1`

###### Does the program display the ISP, and position for the entered IP address?

##### Try flag "-u" with the following command `passive -u "@user01"`

###### Does the program check if the user entered is present in is present in at least 5 social networks?

###### Does the program retrieve this information from a public source?

###### Does the program save the result of each command in a result.txt file?

###### If the result.txt file already exists is a new file created?

---

## Audit Results

| Check | Status | Notes |
|---|---|---|
| `passive` command works | ✅ | Installed via `pip install -e .` |
| README.md present and clear | ✅ | Installation + all 3 usage examples documented |
| Source code present | ✅ | `passive.py`, `output.py`, `modules/` |
| `-fn "Jean Dupont"` shows address + phone | ✅ | 5 results with full address and phone from Pages Blanches |
| `-ip 127.0.0.1` shows ISP + position | ✅ | Loopback handled gracefully — N/A with explanation |
| `-u "@user01"` checks 5+ social networks | ✅ | Checks 7 platforms |
| Results from public sources | ✅ | ip-api.com, Pages Blanches, 192.com, direct URL probing |
| Saves to result.txt | ✅ | Written to `output/result.txt` after every run |
| Creates result2.txt if result.txt exists | ✅ | `output.py` increments suffix until a free filename is found |

---

## Verbal Question Prep

### What does OSINT mean?

OSINT stands for **Open Source Intelligence** — the practice of collecting information about a target using only publicly available sources, without any direct interaction with the target system. Sources include public directories, social media platforms, DNS records, IP geolocation databases, and government registries. It is the first and longest phase of a penetration test because the more you know about a target before touching it, the more precise and effective the rest of the engagement is.

---

### What investigative methods did you use?

| Module | Method | Source |
|--------|--------|--------|
| `-ip` | HTTP GET to a geolocation API | ip-api.com (free, no key) |
| `-u` | HTTP HEAD/GET + Playwright headless browser | Direct URL probing per platform |
| `-fn` | Playwright headless browser + HTML scraping | Pages Blanches (France), 192.com (UK) |

- **IP lookup**: a single API call to `ip-api.com/json/{ip}` returns city, ISP, country, and coordinates in JSON — no authentication needed.
- **Username check**: for simple platforms (GitHub, Reddit, TikTok, LinkedIn) a plain HTTP GET is enough — a 200 means the profile exists, a 404 means it does not. For JavaScript-rendered platforms (Twitter/X, Instagram, Pinterest) we use Playwright (headless Chromium) to fully load the page before checking its content or final URL.
- **Full name lookup**: both Pages Blanches and 192.com render their search results via JavaScript, so a plain HTTP request returns an empty shell. Playwright navigates to the search URL, waits for the page to finish loading, and then BeautifulSoup parses the rendered HTML to extract names, addresses, and phone numbers.

---

### How does the program work?

1. The user runs `passive` with one of three flags: `-fn`, `-ip`, or `-u`, followed by the search value.
2. `passive.py` uses `argparse` with a mutually exclusive group — only one flag is allowed per run.
3. Based on the flag, it calls the matching module: `lookup_ip()`, `lookup_username()`, or `lookup_fullname()`.
4. The module fetches data from its source(s), parses the response, and returns a formatted string.
5. The result is printed to the terminal and passed to `output.py`, which saves it to `output/result.txt` — or `result2.txt`, `result3.txt`, and so on if previous files already exist.
6. The program exits cleanly, with specific error messages for network timeouts, bad input, or unreachable hosts.

---

## General Questions — Answers

### Is the student able to explain clearly the used investigative methods?

Yes. Three distinct methods are used depending on the flag:

- **`-ip`** — A single HTTP GET request is sent to the free `ip-api.com` JSON endpoint. The response includes the city, region, country, ISP, and geographic coordinates. No API key or authentication is required.
- **`-u`** — For most platforms (GitHub, Reddit, TikTok, LinkedIn) a standard HTTP GET is issued to the profile URL; an HTTP 200 confirms the account exists and a 404 confirms it does not. For JavaScript-heavy platforms (Twitter/X, Instagram, Pinterest) a Playwright headless Chromium browser loads the page fully before the result is evaluated.
- **`-fn`** — Both Pages Blanches (France) and 192.com (UK) build their search results entirely in JavaScript, so a raw HTTP request would return an empty page. Playwright navigates to the search URL, waits for the DOM to settle, and then BeautifulSoup parses the rendered HTML to extract names, addresses, and phone numbers.

All three methods rely exclusively on public sources — no login, no scraping of private data, and no direct contact with the target.

---

### Is the student able to explain clearly what OSINT means?

Yes. OSINT stands for **Open Source Intelligence** — collecting information about a target using only publicly available sources, with no direct interaction with the target system. Sources include public directories, social media, DNS records, IP geolocation databases, and government registries. It is typically the first phase of a penetration test: the more that is known about a target before any active probing begins, the more precise and effective the rest of the engagement becomes. It is also entirely passive — the target has no way to detect that reconnaissance is taking place.

---

### Is the student able to explain clearly how his program works?

Yes. The program is invoked from the terminal as `passive` followed by exactly one flag and its argument:

```
passive -fn "Jean Dupont"
passive -ip 8.8.8.8
passive -u "@someuser"
```

Internally:

1. `passive.py` parses arguments with `argparse` using a mutually exclusive group, so only one flag is accepted per run.
2. The matching lookup function is called: `lookup_ip()`, `lookup_username()`, or `lookup_fullname()`.
3. The function fetches data from its source(s), parses the response, and returns a formatted result string.
4. The result is printed to the terminal.
5. `output.py` writes the result to `output/result.txt`. If that file already exists, it increments the suffix (`result2.txt`, `result3.txt`, …) until a free filename is found, so no previous result is ever overwritten.