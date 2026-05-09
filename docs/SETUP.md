# Setup Guide

Step-by-step instructions to install and run the passive OSINT tool from scratch.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or higher |
| pip | bundled with Python |
| Internet connection | required at runtime |

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd passive
```

### 2. Create the virtual environment

```bash
python3 -m venv venv
```

This creates an isolated Python environment inside the `venv/` folder so project dependencies do not conflict with your system Python.

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

Your terminal prompt will change to show `(venv)` — this means the environment is active.
You must activate it every time you open a new terminal session.

To deactivate when you are done:

```bash
deactivate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

Installs:

| Package | Version | Used for |
|---------|---------|----------|
| `requests` | 2.33.1 | IP lookup, username HTTP probing |
| `playwright` | 1.59.0 | JS-rendered page scraping (username + full name) |
| `beautifulsoup4` | 4.14.3 | HTML parsing for full name results |
| `phonenumbers` | latest | Phone number validation, carrier, and location lookup |

### 5. Install the Playwright browser

```bash
playwright install chromium
```

Downloads a headless Chromium browser used by the `-u` and `-fn` modules.
This only needs to be done once.

### 6. Register the `passive` command

```bash
python setup.py develop
```

Registers `passive` as a terminal command within the active venv.
Also auto-generates `passive.egg-info/ABOUT.md` with documentation about the packaging folder.

### 7. Verify the installation

```bash
passive --help
```

Expected output:

```
Welcome to passive v1.0.0

OPTIONS:
    -fn         Search with full-name
    -ip         Search with ip address
    -u          Search with username
```

---

## Usage

### Phone number lookup

Returns carrier, location, type, and validity for a phone number.
The number must include the country code.

```bash
passive -ph "+33612345678"
```

```
Phone:    +33 6 12 34 56 78
Valid:    yes
Type:     mobile
Country:  FR
Location: France
Carrier:  SFR

Saved in output/result.txt
```

### Full name lookup

Searches public directories in France (Pages Blanches) and the UK (192.com).

```bash
passive -fn "Jean Dupont"
```

```
Full Name:  Jean Dupont
First:      Jean
Last:       Dupont

[France — Pages Blanches]
  Result 1:
    Name:    Dupont Jean
    Address: 8 r Victor Hugo 61570 Mortrée
    Phone:   09 86 16 54 22
  ...

[UK — 192.com]
  Result 1:
    Name:    Jean Dupont
    Area:    London, Greater London, W13...
    ER:      ER2024-26
  ...

Saved in output/result.txt
```

### IP address lookup

Returns ISP, city, country, and coordinates for a public IP address.
Private and reserved IPs (e.g. `127.0.0.1`) are handled gracefully.

```bash
passive -ip 8.8.8.8
```

```
ISP:          Google LLC
City:         Ashburn, United States
City Lat/Lon: (39.03) / (-77.5)

Saved in output/result.txt
```

```bash
passive -ip 127.0.0.1
```

```
ISP:          N/A (Loopback address)
City:         N/A
City Lat/Lon: N/A

Saved in output/result.txt
```

### Username lookup

Checks whether a username exists across 7 social platforms.
The leading `@` is optional.

```bash
passive -u "@user01"
```

```
Username: @user01

  [yes]            https://github.com/user01
  [yes]            https://www.reddit.com/user/user01
  [yes]            https://twitter.com/user01
  [no]             https://www.tiktok.com/@user01
  [yes]            https://www.pinterest.com/user01
  [yes]            https://www.instagram.com/user01
  [no]             https://www.linkedin.com/in/user01

Saved in output/result.txt
```

---

## Output files

Every result is saved automatically to the `output/` folder.
If a file already exists the suffix is incremented — no results are ever overwritten.

```
output/result.txt     ← first run
output/result2.txt    ← second run
output/result3.txt    ← third run
...
```

---

## Project structure

```
passive/
├── passive.py          ← CLI entry point
├── output.py           ← result file writer
├── setup.py            ← registers the passive command + post-install hook
├── pyproject.toml      ← package metadata
├── requirements.txt    ← pip dependencies
├── modules/
│   ├── ip_lookup.py    ← -ip handler
│   ├── username.py     ← -u handler
│   └── fullname.py     ← -fn handler
├── output/             ← saved results (auto-created)
├── docs/
│   ├── SETUP.md        ← this file
│   ├── PLANNING.md     ← implementation plan
│   ├── PASSIVE.md      ← project specification
│   ├── AUDIT.md        ← audit checklist + answers
│   └── QUIZ.md         ← knowledge check
└── passive.egg-info/   ← auto-generated packaging metadata
    └── ABOUT.md        ← explains the egg-info folder
```

---

## Audit

Run the automated audit script to verify every check from `docs/AUDIT.md` passes:

```bash
source venv/bin/activate && bash audit.sh
```

The script checks:
- All required files are present
- The `passive` command is registered and `--help` shows the correct banner
- `-ip 127.0.0.1` returns ISP and City Lat/Lon fields
- Sequential file naming works (no result file is overwritten)
- `-u "@user01"` checks at least 5 social platforms
- `-fn "Jean Dupont"` displays an address and phone number

Output is colour-coded — green `[PASS]` / red `[FAIL]` — with a summary at the end.
The Playwright sections (`-u` and `-fn`) take 30–60 seconds each.

---

## Common issues

| Problem | Cause | Fix |
|---------|-------|-----|
| `command not found: passive` | venv not active or step 6 skipped | Run `source venv/bin/activate` then `python setup.py develop` |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `playwright._impl._errors.Error` | Chromium not installed | Run `playwright install chromium` |
| `-fn` returns no results | Name not in the directory | Normal — most people are not listed in public phone books |
| `-ip` returns N/A | Private or reserved IP address | Use a public IP (e.g. `8.8.8.8`) for a full lookup |
