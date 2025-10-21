import schedule
import time
import sys
import json
import os
from datetime import datetime

from constants.LOCATIONS import LOCATIONS

sys.path.insert(
    1, "C://Users//ryanh//code//projects//canucksTix//libs//marketplace-api"
)
import MarketplaceAPI

SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Gets C:\Users\ryanh\code\projects\canucksTix\src
PROJECT_ROOT = os.path.dirname(
    SCRIPT_DIR
)  # Gets C:\Users\ryanh\code\projects\canucksTix
DATA_DIR = os.path.join(
    PROJECT_ROOT, "tests", "data"
)  # Gets C:\Users\ryanh\code\projects\canucksTix\tests\data


def scrape_listings():
    print(f"\nRunning scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for n in range(0, len(LOCATIONS)):
        lat = LOCATIONS[n]["latitude"]
        lon = LOCATIONS[n]["longitude"]
        name = LOCATIONS[n]["name"]
        query = "canucks"

        result = MarketplaceAPI.handleSearch(lat, lon, query)

        # writing result to file
        os.makedirs(DATA_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(DATA_DIR, f"listings_{timestamp}_{name}.json")

        with open(filename, "w") as f:
            json.dump(result, f, indent=2)


def main():
    print("starting marketplace scraper")
    schedule.every(5).minutes.do(scrape_listings)
    scrape_listings()
    while True:
        schedule.run_pending()
        time.sleep(150)


if __name__ == "__main__":
    main()
