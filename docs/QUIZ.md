# Phase 1 — Knowledge Check


### Q1 — argparse

**Why do we use `add_mutually_exclusive_group(required=True)` in argparse instead of three separate `add_argument()` calls?**

- [ ] A. To make the `--help` output look nicer
- [✅] B. To prevent using `-fn`, `-ip`, and `-u` at the same time, and force the user to always pick one
- [ ] C. Because argparse doesn't support optional arguments otherwise
- [ ] D. To automatically generate the OPTIONS banner

---

### Q2 — output.py

**Why does `output.py` use a `while` loop instead of just checking if `result.txt` exists once?**

- [ ] A. Because `os.path.exists()` only works on the first call
- [ ] B. To avoid overwriting `result.txt` if two processes run at the same time
- [ ] C. Because Python requires a loop to create files
- [✅] D. Because `result2.txt`, `result3.txt`... might also already exist from previous runs

---

### Q3 — pyproject.toml

**What is the purpose of `pyproject.toml` and `pip3 install -e .` in this project?**

- [ ] A. It compiles the Python files into a binary
- [ ] B. It pins the exact version of every dependency
- [✅] C. It registers `passive` as a system command so it runs from anywhere in the terminal
- [ ] D. It is only needed for publishing to PyPI

---

---

### Q4 — venv

**Why did we create a `venv/` folder instead of installing the project directly on the system Python?**

- [✅] A. To keep project dependencies isolated from the system Python and avoid conflicts
- [ ] B. Because Python 3 cannot run without a virtual environment
- [ ] C. Because pip doesn't work outside a venv on any OS
- [ ] D. To make the project run faster

---

### Q5 — ModuleNotFoundError

**Why did `passive --help` fail with `ModuleNotFoundError: No module named 'passive'` even after running `pip install -e .`?**

- [ ] A. Because `passive.py` had a syntax error
- [ ] B. Because the venv was not activated at the time
- [✅] C. Because `pyproject.toml` was missing the `py-modules` declaration so setuptools didn't know about `passive.py`
- [ ] D. Because `passive.py` needs to be renamed to `__main__.py`

---

### Q6 — CLI vs script

**What is the difference between running `python3 passive.py --help` and `passive --help`?**

- [ ] A. There is no difference — both run the exact same code
- [✅] B. `python3 passive.py` runs the file directly; `passive` is a system command installed into PATH by pip — but both require the venv to be active
- [ ] C. `passive --help` runs faster because it is compiled
- [ ] D. `python3 passive.py` only works inside the project folder; `passive --help` works everywhere without a venv

---

# Phase 2 — Username Module Quiz

---

### Q7 — venv activation

**What command activates the virtual environment in this project?**

- [ ] A. `venv activate`
- [✅] B. `source venv/bin/activate`
- [ ] C. `python venv start`
- [ ] D. `activate venv/bin`

---

### Q8 — Soft 404

**What is a "soft 404"?**

- [ ] A. A server error that crashes the app
- [✅] B. A page that returns HTTP 200 but shows a "not found" message
- [ ] C. A redirect to a login page
- [ ] D. A timeout from a slow server

---

### Q9 — Reddit false positives

**Why did Reddit return `yes` for a fake username in our first attempt?**

- [ ] A. Reddit doesn't have user profiles
- [ ] B. We used the wrong URL
- [✅] C. Reddit returns HTTP 200 even for non-existent users on the profile page
- [ ] D. Our User-Agent was blocked

---

### Q10 — Reddit fix

**How did we fix Reddit's false positives?**

- [ ] A. Switched to Playwright
- [ ] B. Added a longer timeout
- [✅] C. Used the `/user/{}/about.json` API endpoint which returns a real 404
- [ ] D. Checked the page title

---

### Q11 — Why Playwright

**Why did we add Playwright for Twitter/X, Instagram, and Pinterest?**

- [ ] A. They require an API key
- [✅] B. They are JavaScript-rendered SPAs — plain HTTP GET only returns an empty HTML shell
- [ ] C. They block all requests without a browser
- [ ] D. They use IPv6 only

---

### Q12 — Playwright threading error

**What error did we get when running Playwright inside a `ThreadPoolExecutor`?**

- [ ] A. `ModuleNotFoundError`
- [ ] B. `TimeoutError`
- [✅] C. `'str' object is not callable`
- [ ] D. `ConnectionRefusedError`

---

### Q13 — Root cause

**What was the root cause of that error?**

- [ ] A. Wrong import
- [✅] B. `page.url` is a property, not a method — we called it as `page.url()`
- [ ] C. Playwright wasn't installed
- [ ] D. The thread pool was too small

---

### Q14 — networkidle

**Why does `networkidle` cause Twitter/X to always `[error]`?**

- [ ] A. Twitter blocks Playwright
- [ ] B. Twitter requires login to load
- [✅] C. Twitter constantly fires background requests so the page never reaches "idle"
- [ ] D. Our timeout was too short

---

### Q15 — Pinterest not found

**How do we detect a Pinterest "not found" without checking the body?**

- [ ] A. Pinterest returns a 404 status code
- [✅] B. Pinterest redirects to `pinterest.com/?show_error=true`
- [ ] C. Pinterest title says "Page not found"
- [ ] D. Pinterest returns status 999

---

### Q16 — LinkedIn 999

**What does LinkedIn's `unknown (999)` status mean?**

- [ ] A. The user exists but their profile is private
- [ ] B. Our request timed out
- [✅] C. LinkedIn actively blocks scrapers with a non-standard 999 anti-bot response
- [ ] D. LinkedIn is down

---

# Phase 3 — Bonus, Multiprocessing & Verbal Prep

---

### Q17 — phonenumbers library

**Why does the `-ph` module not need an API key or internet connection?**

- [ ] A. It calls a free government API that doesn't require authentication
- [ ] B. It reads from the SIM card registry
- [✅] C. The `phonenumbers` library ships with a bundled offline database of carrier and region data
- [ ] D. It uses the phone's GPS to detect location

---

### Q18 — Phone number format

**Why does `passive -ph "0612345678"` fail while `passive -ph "+33612345678"` works?**

- [ ] A. The `-ph` flag only accepts numbers with more than 10 digits
- [✅] B. `phonenumbers.parse()` requires a country code to know which numbering plan to use — without it, it raises `NumberParseException`
- [ ] C. The `+` sign is required by the terminal, not the library
- [ ] D. French numbers are not supported

---

### Q19 — Threading vs multiprocessing

**Why did we switch from `threading.Thread` to `multiprocessing.Process` to fix the Playwright hang?**

- [ ] A. Threads are slower than processes on macOS
- [ ] B. Playwright doesn't support threads at all
- [✅] C. Playwright's internal asyncio threads are non-daemon and prevent Python from exiting — a process can be hard-killed with `terminate()`, a thread cannot
- [ ] D. The `threading` module is deprecated in Python 3.14

---

### Q20 — daemon=True

**What does `daemon=True` do when set on a `multiprocessing.Process`?**

- [ ] A. It makes the process run with administrator privileges
- [ ] B. It makes the process run silently without any output
- [✅] C. It ensures the child process is automatically killed if the parent process exits, preventing zombie processes
- [ ] D. It runs the process in the background on a separate CPU core only

---

### Q21 — proc.terminate() vs proc.kill()

**Why do we call `proc.terminate()` first and only call `proc.kill()` if the process is still alive?**

- [✅] A. `terminate()` sends SIGTERM which allows the process to clean up gracefully; `kill()` sends SIGKILL which forces an immediate stop with no cleanup
- [ ] B. `kill()` is slower than `terminate()`
- [ ] C. `terminate()` only works on Linux, `kill()` works on macOS
- [ ] D. Both do the same thing — the second call is just a safety net

---

### Q22 — Sequential file naming

**What would happen if `output.py` used `if` instead of `while` to check for existing files?**

- [ ] A. Nothing — `if` and `while` behave the same way here
- [ ] B. The file would never be created
- [✅] C. It would only skip one existing file — if both `result.txt` and `result2.txt` exist, it would overwrite `result2.txt`
- [ ] D. Python would raise a `FileExistsError`

---

### Q23 — Playwright timeout not firing

**Why can Playwright's `page.goto(timeout=15000)` fail to stop a hang even though the timeout is set?**

- [ ] A. The timeout parameter is ignored by Playwright on macOS
- [ ] B. 15 seconds is too short for modern websites
- [✅] C. The timeout is implemented in JavaScript/Node.js — if the underlying OS or network blocks at a lower level (DNS, TCP handshake), the Python layer never receives the signal
- [ ] D. The timeout only applies to the first page load, not redirects

---

### Q24 — OSINT definition (verbal)

**What does OSINT stand for and why is it the first phase of a penetration test?**

- [ ] A. Open System Intelligence — because it maps the network topology before attacking
- [ ] B. Online Source Investigation — because it gathers credentials before testing
- [✅] C. Open Source Intelligence — because the more publicly available information you gather before touching the target, the more precise and effective the rest of the engagement is
- [ ] D. Offensive Security Intelligence — because it identifies vulnerabilities in public APIs

---

### Q25 — Why Playwright for Pages Blanches

**Why does the full-name module use Playwright instead of `requests` for Pages Blanches and 192.com?**

- [ ] A. Both sites require a login that Playwright handles automatically
- [ ] B. The sites block requests without a real browser header
- [✅] C. Both sites render their search results via JavaScript — a plain HTTP GET returns an empty HTML shell with no results
- [ ] D. Playwright is faster than requests for French websites

---

### Q26 — BeautifulSoup role

**What is BeautifulSoup's role in the `-fn` module, and what does Playwright do that makes it necessary?**

- [ ] A. BeautifulSoup fetches the page; Playwright parses it
- [✅] B. Playwright navigates to the page and returns the fully rendered HTML; BeautifulSoup then parses that HTML to extract names, addresses, and phone numbers
- [ ] C. BeautifulSoup handles JavaScript; Playwright handles static HTML
- [ ] D. Playwright is only used as a fallback when BeautifulSoup fails

---

### Q27 — `requires auth` status

**What does `[requires auth]` mean in the `-u` output, and how is it detected?**

- [ ] A. The platform returned a 403 HTTP status code
- [ ] B. The platform's API rejected our User-Agent header
- [✅] C. Playwright detected a redirect to a login URL (e.g. `twitter.com/i/flow/login`) — the user might exist but the platform demands a login before showing the profile
- [ ] D. The username contains special characters that triggered a security check

---

### Q28 — No directory for Brazil

**Why does the `-fn` module return no results for Brazil?**

- [ ] A. Brazilian law prohibits scraping public directories
- [ ] B. Brazil has no public phone directories at all
- [ ] C. telelistas.net is fully offline and unreachable
- [✅] D. There is no freely scrapable public person directory for Brazil — telelistas.net now redirects and blocks scrapers, and ddd.telelistas.net is a DDD area code lookup, not a person search

---
