import argparse
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a full day of banking data"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--mobile-count",
        type=int,
        default=20000,
        help="Number of mobile transactions"
    )

    parser.add_argument(
        "--atm-count",
        type=int,
        default=100,
        help="Number of ATM transactions"
    )

    return parser.parse_args()


def generate_day(date, mobile_count, atm_count):

    print(f"Generating full day of banking data: {date}")

    print("\n--- MOBILE ---")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "generators.mobile",
            "--date",
            date,
            "--count",
            str(mobile_count)
        ],
        check=True
    )

    print("\n--- ATM ---")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "generators.atm",
            "--date",
            date,
            "--count",
            str(atm_count)
        ],
        check=True
    )

    print("\n================================")
    print(f"Full day generation completed: {date}")
    print("================================")


if __name__ == "__main__":

    args = parse_args()

    generate_day(
        args.date,
        args.mobile_count,
        args.atm_count
    )