import os
from setuptools import setup
from setuptools.command.develop import develop

ABOUT_MD = """\
# passive.egg-info — What is this folder?

This folder is **auto-generated** by `pip install -e .` and is **not written by hand**.
It is recreated every time that command is run, so do not edit files here directly.
`ABOUT.md` is the only exception — it is written by the post-install hook in `setup.py`.

---

## What is it for?

`passive.egg-info` is Python's packaging metadata folder.
It is the bridge between the raw source files (`passive.py`, `modules/`, etc.)
and the `passive` terminal command. Without it, `pip` and Python's import
system would not know this project exists as an installable package.

---

## Files

| File | Purpose |
|------|---------|
| `PKG-INFO` | Package identity card — name, version, description, Python requirement, dependencies. Copied from `pyproject.toml`. |
| `SOURCES.txt` | Full list of source files that belong to the package (`passive.py`, `output.py`, `modules/`, etc.). |
| `top_level.txt` | Tells Python which top-level modules to import: `passive` and `output`. |
| `entry_points.txt` | Maps the `passive` terminal command to `passive:main` — this is what makes `passive --help` work in the shell. |
| `requires.txt` | Runtime dependencies (`requests`). Mirrors `pyproject.toml`. |
| `dependency_links.txt` | Empty — would contain custom package index URLs if needed. |
| `ABOUT.md` | This file. Written by the post-install hook in `setup.py`. |

---

## Key file — entry_points.txt

```
[console_scripts]
passive = passive:main
```

This single entry is what registers `passive` as a shell command.
It tells pip: *"when the user types `passive`, call the `main()` function in `passive.py`."*
Without it, you would have to run `python3 passive.py` every time.
"""


class PostDevelop(develop):
    def run(self):
        develop.run(self)
        about_path = os.path.join("passive.egg-info", "ABOUT.md")
        if os.path.isdir("passive.egg-info"):
            with open(about_path, "w") as f:
                f.write(ABOUT_MD)
            print(f"  Created {about_path}")


setup(cmdclass={"develop": PostDevelop})
