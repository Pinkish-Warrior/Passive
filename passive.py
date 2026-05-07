#!/usr/bin/env python3
# Entry point for the passive OSINT CLI tool.
# Parses the user's flag (-fn, -ip, -u), routes to the correct module,
# prints the result, and saves it to output/result.txt (incrementing if needed).

import argparse
import sys
from modules.ip_lookup import lookup_ip
from modules.username import lookup_username
from modules.fullname import lookup_fullname
from output import save_result

BANNER = "Welcome to passive v1.0.0"

OPTIONS = """
OPTIONS:
    -fn         Search with full-name
    -ip         Search with ip address
    -u          Search with username
"""


def build_parser():
    # Only one flag allowed per run; all three are mutually exclusive
    parser = argparse.ArgumentParser(
        description=BANNER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=OPTIONS,
        add_help=True,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-fn", metavar="FULL_NAME", help="Search by full name")
    group.add_argument("-ip", metavar="IP_ADDRESS", help="Search by IP address")
    group.add_argument("-u", metavar="USERNAME", help="Search by username")
    return parser


def main():
    parser = build_parser()

    # Show help when no arguments are passed
    if len(sys.argv) == 1:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    try:
        if args.ip:
            result = lookup_ip(args.ip)
        elif args.u:
            result = lookup_username(args.u)
        elif args.fn:
            result = lookup_fullname(args.fn)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(result)
    filename = save_result(result)
    print(f"Saved in {filename}")


if __name__ == "__main__":
    main()
