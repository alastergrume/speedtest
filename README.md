# Internet Speed Test

The script makes 10 sequential requests to a given URL (for example, a large image),
waits for each response to download completely and prints the average request time, the total downloaded data and the speed.

## Requirements

Python 3.8 or newer. No external dependencies.

## Usage

```bash
git clone https://github.com/<your-username>/speedtest.git
cd speedtest
python speedtest.py https://proof.ovh.net/files/10Mb.dat
```

Any direct link to a large file or image will do. The larger the file, the more accurate the result.

The number of requests can be changed with `-c`:

```bash
python speedtest.py https://proof.ovh.net/files/10Mb.dat -c 5
```

## Example output

```
Speed test: https://proof.ovh.net/files/10Mb.dat, requests: 10

Request  1/10: 10.49 MB in 1.214 s (8.64 MB/s)
Request  2/10: 10.49 MB in 1.187 s (8.83 MB/s)
...
Request 10/10: 10.49 MB in 1.171 s (8.95 MB/s)

Summary
  Successful requests:  10 of 10
  Average request time: 1.181 s
  Total downloaded:     104.86 MB
  Speed, MB/s:          8.88
```

## How the result is calculated

- **Request time** — from sending the request to receiving the last byte of the response.
- **Total downloaded** — the sum of bytes actually received across all successful requests.
- **Speed** — total downloaded data divided by total download time, in megabytes per second (1 MB = 1,000,000 bytes).

Failed requests (timeout, dropped connection, 4xx or 5xx response) are printed to the console and excluded from the summary.

## Project structure

```
speedtest/
├── speedtest.py   # entry point: requests, timing, output
├── cli.py         # command-line arguments
└── models.py      # data models: Measurement and Summary
```
