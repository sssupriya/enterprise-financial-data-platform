from datetime import datetime, date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LANDING_ROOT = PROJECT_ROOT / "data" / "landing"


def get_landing_path(channel, business_date):
    """
    Return a landing-zone file path for a channel and business date.

    Example:
    data/landing/upi/2026/07/01/upi_20260701_153045.csv
    """

    if isinstance(business_date, str):
        business_date = datetime.strptime(
            business_date,
            "%Y-%m-%d"
        ).date()

    if not isinstance(business_date, date):
        raise ValueError(
            "business_date must be a date or YYYY-MM-DD string"
        )

    channel = channel.lower()

    output_dir = (
        LANDING_ROOT
        / channel
        / business_date.strftime("%Y")
        / business_date.strftime("%m")
        / business_date.strftime("%d")
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    run_timestamp = datetime.now().strftime("%H%M%S")

    filename = (
        f"{channel}_"
        f"{business_date.strftime('%Y%m%d')}_"
        f"{run_timestamp}.csv"
    )

    return output_dir / filename