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
