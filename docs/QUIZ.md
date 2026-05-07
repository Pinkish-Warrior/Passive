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
