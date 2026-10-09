#!/usr/bin/env python3
"""Download speed test: N sequential requests to a single URL.

Example:
    python3 speedtest.py https://proof.ovh.net/files/10Mb.dat
"""

import http.client
import sys
import time
import urllib.request
from typing import List

from cli import parse_args
from models import BYTES_IN_MB, Measurement, Summary

CHUNK_SIZE = 64 * 1024
USER_AGENT = "speedtest-script/1.0"
# Applies to each network operation (connecting, waiting for the next chunk),
# not to the whole download, so a slow but steady transfer is never cut off.
TIMEOUT_S = 30


def fetch(url: str) -> Measurement:
    """Download the whole response and time it from sending the request to the last byte."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            # Ask intermediate caches not to serve a stored copy.
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    size = 0
    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            size += len(chunk)
    return Measurement(size_bytes=size, duration_s=time.perf_counter() - start)


def run(url: str, count: int) -> Summary:
    """Make `count` sequential requests and print the result of each one."""
    measurements: List[Measurement] = []
    failed = 0
    width = len(str(count))

    for number in range(1, count + 1):
        prefix = f"Request {number:>{width}}/{count}:"
        try:
            measurement = fetch(url)
        except (OSError, http.client.HTTPException) as error:
            # OSError covers URLError, HTTPError, timeouts and dropped connections.
            failed += 1
            print(f"{prefix} error — {error}")
            continue

        measurements.append(measurement)
        print(
            f"{prefix} {measurement.size_bytes / BYTES_IN_MB:.2f} MB "
            f"in {measurement.duration_s:.3f} s ({measurement.speed_mb_per_s:.2f} MB/s)"
        )

    return Summary(measurements=measurements, failed=failed)


def print_summary(summary: Summary) -> None:
    total = summary.successful + summary.failed
    print()
    print("Summary")
    rows = [
        ("Successful requests:", f"{summary.successful} of {total}"),
        ("Average request time:", f"{summary.average_time_s:.3f} s"),
        ("Total downloaded:", f"{summary.total_bytes / BYTES_IN_MB:.2f} MB"),
        ("Speed, MB/s:", f"{summary.speed_mb_per_s:.2f}"),
    ]
    width = max(len(label) for label, _ in rows)
    for label, value in rows:
        print(f"  {label:<{width}} {value}")


def main() -> int:
    args = parse_args()
    print(f"Speed test: {args.url}, requests: {args.count}\n")

    try:
        summary = run(args.url, args.count)
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130

    if summary.successful == 0:
        print("\nAll requests failed, the speed cannot be calculated.", file=sys.stderr)
        return 1

    print_summary(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
