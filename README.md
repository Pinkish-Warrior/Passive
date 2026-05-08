# passive

A passive OSINT CLI tool for gathering publicly available information from a full name, IP address, or username.

---

## Requirements

- Python 3.8+
- [Playwright](https://playwright.dev/python/) Chromium browser (for full-name and username lookups)

---

## Installation

```bash
# 1. Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright's Chromium browser
playwright install chromium

# 4. Register the `passive` command and generate egg-info documentation
python setup.py develop
```

---

## Usage

```
passive --help

Welcome to passive v1.0.0

OPTIONS:
    -fn         Search with full-name
    -ip         Search with ip address
    -u          Search with username
```

### Full name lookup (`-fn`)

Searches public directories in France (Pages Blanches) and the UK (192.com Electoral Roll).

```
passive -fn "Jean Dupont"

First:      Jean
Last:       Dupont

[France — Pages Blanches]
  Result 1:
    Name:    Dupont Jean
    Address: 7 r du Progrès 75016 Paris
    Phone:   01 23 45 67 89

[UK — 192.com]
  Result 1:
    Name:    Jean Dupont
    Area:    London, Greater London, W1...
    ER:      ER2024-26

Saved in result.txt
```

### IP address lookup (`-ip`)

Returns the ISP, city, country, and coordinates for any public IP address.
Private and reserved ranges (loopback, RFC1918, etc.) are handled gracefully.

```
passive -ip 127.0.0.1

ISP:          N/A (Loopback address)
City:         N/A
City Lat/Lon: N/A

Saved in result2.txt
```

```
passive -ip 8.8.8.8

ISP:          Google LLC
City:         Ashburn, United States
City Lat/Lon: (39.03) / (-77.5)

Saved in result3.txt
```

### Username lookup (`-u`)

Checks whether a username exists across 7 platforms. Leading `@` is optional.

```
passive -u "@user01"

Username: @user01

  [yes]           https://github.com/user01
  [yes]           https://www.reddit.com/user/user01
  [yes]           https://twitter.com/user01
  [no]            https://www.tiktok.com/@user01
  [yes]           https://www.pinterest.com/user01
  [yes]           https://www.instagram.com/user01
  [no]            https://www.linkedin.com/in/user01

Saved in result4.txt
```

---

## Output files

Results are saved automatically to the `output/` folder:

| Run | File |
|-----|------|
| 1st | `output/result.txt` |
| 2nd | `output/result2.txt` |
| 3rd | `output/result3.txt` |
| … | … |

---

## Platforms checked (`-u`)

| Platform | Method |
|----------|--------|
| GitHub | HTTP GET |
| Reddit | JSON API (`/about.json`) |
| Twitter/X | Playwright |
| TikTok | HTTP GET |
| Pinterest | Playwright |
| Instagram | Playwright |
| LinkedIn | HTTP GET |

---

## Notes

- The full-name module uses Playwright (headless Chromium) because both Pages Blanches and 192.com render results via JavaScript.
- 192.com shows name + area only; a full address requires a free account on their site.
- No API keys are required for any feature.

---

> These methods are for educational purposes only. Only use this tool against targets you have explicit permission to research.
