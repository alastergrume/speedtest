"""Command-line argument parsing and validation."""

import argparse
import urllib.parse

DEFAULT_COUNT = 10


def http_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise argparse.ArgumentTypeError(
            f"expected an http:// or https:// URL, got: {value}"
        )
    return value


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected an integer, got: {value}") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="speedtest.py",
        description=(
            "Measures download speed: makes several sequential requests to a URL "
            "and reports the average request time, total downloaded data and speed."
        ),
    )
    parser.add_argument("url", type=http_url, help="URL of a large file or image")
    parser.add_argument(
        "-c",
        "--count",
        type=positive_int,
        default=DEFAULT_COUNT,
        metavar="INT",
        help=f"requests count (default: {DEFAULT_COUNT})",
    )
    return parser


def parse_args() -> argparse.Namespace:
    return build_parser().parse_args()
