import csv
import io
import re
import urllib.request
import zipfile

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_FILE = "ssa-baby-names.csv"

# Browser-like headers so the SSA server does not block the request with HTTP 403
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ssa.gov/oact/babynames/limits.html",
}


def main():
    req = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        # Read the downloaded zip file directly in memory
        zip_bytes = io.BytesIO(response.read())

    with zipfile.ZipFile(zip_bytes) as zf, open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["year", "name", "sex", "count"])

        # Process each yearly file (e.g., yob1880.txt) in chronological order
        for filename in sorted(zf.namelist()):
            match = re.fullmatch(r"yob(\d{4})\.txt", filename)
            if not match:
                continue
            year = match.group(1)

            with zf.open(filename) as raw_file:
                text_file = io.TextIOWrapper(raw_file, encoding="utf-8")
                for row in csv.reader(text_file):
                    if row:
                        writer.writerow([year, row[0], row[1], row[2]])


if __name__ == "__main__":
    main()
