#!/usr/bin/env python3
# Entry point for the passive OSINT CLI tool.
# Parses the user's flag (-fn, -ip, -u), routes to the correct module,
# prints the result, and saves it to output/result.txt (incrementing if needed).

import argparse
import sys
import requests

from modules.ip_lookup import lookup_ip
from modules.username import lookup_username
from modules.fullname import lookup_fullname
from modules.phone import lookup_phone
from output import save_result

BANNER = "Welcome to passive v1.0.0"

OPTIONS = """OPTIONS:
    -fn         Search with full-name
    -ip         Search with ip address
    -u          Search with username
    -ph         Search with phone number"""


def build_parser():
    # Only one flag allowed per run; all three are mutually exclusive
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"{BANNER}\n\n{OPTIONS}",
        add_help=True,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-fn", metavar="FULL_NAME",    help="Search by full name")
    group.add_argument("-ip", metavar="IP_ADDRESS",  help="Search by IP address")
    group.add_argument("-u",  metavar="USERNAME",    help="Search by username")
    group.add_argument("-ph", metavar="PHONE",       help="Search by phone number (include country code, e.g. +33612345678)")
    return parser


def main():
    parser = build_parser()

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
        elif args.ph:
            result = lookup_phone(args.ph)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection or host unreachable.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out — the server took too long to respond.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Network error — {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(result)
    filename = save_result(result)
    print(f"Saved in {filename}")


if __name__ == "__main__":
    main()
