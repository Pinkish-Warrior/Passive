#!/bin/bash
# Automated audit checker for the passive OSINT tool.
# Mirrors every check in docs/AUDIT.md and reports PASS / FAIL.
# Run from the project root with the venv active:
#   source venv/bin/activate && bash audit.sh

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
FAIL=0

pass() { echo -e "  ${GREEN}[PASS]${NC} $1"; ((PASS++)); }
fail() { echo -e "  ${RED}[FAIL]${NC} $1"; ((FAIL++)); }
section() { echo -e "\n${YELLOW}${BOLD}── $1 ──${NC}"; }

# ── 1. Required files ─────────────────────────────────────────────────────────

section "Required files"

for f in passive.py README.md output.py modules/ip_lookup.py modules/username.py modules/fullname.py; do
    if [ -f "$f" ]; then
        pass "$f present"
    else
        fail "$f missing"
    fi
done

# ── 2. passive command ────────────────────────────────────────────────────────

section "passive command"

if ! command -v passive &>/dev/null; then
    fail "passive command not found — run: python setup.py develop"
else
    pass "passive registered in PATH"

    help_out=$(passive --help 2>&1)

    if echo "$help_out" | grep -q "Welcome to passive v1.0.0"; then
        pass "--help shows banner"
    else
        fail "--help missing banner"
    fi

    if echo "$help_out" | grep -qE "\-fn|\-ip|\-u"; then
        pass "--help shows all three flags"
    else
        fail "--help missing one or more flags"
    fi
fi

# ── 3. -ip 127.0.0.1 ─────────────────────────────────────────────────────────

section "Flag -ip  (passive -ip 127.0.0.1)"

ip_out=$(passive -ip 127.0.0.1 2>&1)

if echo "$ip_out" | grep -q "ISP:"; then
    pass "ISP field present"
else
    fail "ISP field missing"
fi

if echo "$ip_out" | grep -q "City Lat/Lon:"; then
    pass "City Lat/Lon field present"
else
    fail "City Lat/Lon field missing"
fi

if echo "$ip_out" | grep -q "Saved in"; then
    pass "result file saved"
else
    fail "result file not saved"
fi

# ── 4. Sequential file naming ─────────────────────────────────────────────────

section "Sequential file naming"

before=$(ls output/ 2>/dev/null | wc -l)
passive -ip 1.1.1.1 &>/dev/null
mid=$(ls output/ 2>/dev/null | wc -l)
passive -ip 8.8.8.8 &>/dev/null
after=$(ls output/ 2>/dev/null | wc -l)

if [ "$mid" -gt "$before" ] && [ "$after" -gt "$mid" ]; then
    pass "new file created on each run — no overwrite"
else
    fail "sequential naming not working"
fi

# ── 5. -u "@user01" ───────────────────────────────────────────────────────────

section "Flag -u  (passive -u \"@user01\")"
echo "  note: Playwright is loading pages — this may take ~30s"

u_out=$(passive -u "@user01" 2>&1)

platform_count=$(echo "$u_out" | grep -cE "\[(yes|no|error|requires auth|unknown)")

if [ "$platform_count" -ge 5 ]; then
    pass "$platform_count platforms checked (≥5 required)"
else
    fail "only $platform_count platform(s) checked — need at least 5"
fi

if echo "$u_out" | grep -q "Saved in"; then
    pass "result file saved"
else
    fail "result file not saved"
fi

# ── 6. -fn "Jean Dupont" ──────────────────────────────────────────────────────

section "Flag -fn  (passive -fn \"Jean Dupont\")"
echo "  note: Playwright is loading pages — this may take ~30s"

fn_out=$(passive -fn "Jean Dupont" 2>&1)

if echo "$fn_out" | grep -q "Address:"; then
    pass "address displayed"
else
    fail "address not displayed"
fi

if echo "$fn_out" | grep -q "Phone:"; then
    pass "phone number displayed"
else
    fail "phone number not displayed"
fi

if echo "$fn_out" | grep -q "Saved in"; then
    pass "result file saved"
else
    fail "result file not saved"
fi

# ── Summary ───────────────────────────────────────────────────────────────────

TOTAL=$((PASS + FAIL))

echo -e "\n${YELLOW}${BOLD}── Summary ──${NC}"
echo -e "  Passed : ${GREEN}${BOLD}$PASS${NC} / $TOTAL"

if [ "$FAIL" -gt 0 ]; then
    echo -e "  Failed : ${RED}${BOLD}$FAIL${NC} / $TOTAL"
    echo -e "\n  ${RED}${BOLD}Audit FAILED${NC} — fix the issues above and re-run."
    exit 1
else
    echo -e "\n  ${GREEN}${BOLD}All checks passed.${NC}"
    exit 0
fi
