import argparse
import csv
import re
import requests
from collections import Counter
from datetime import datetime


def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.text.splitlines()

def process_log_data(log_data):
    image_extensions = re.compile(r'.*\.(jpg|gif|png)$', re.IGNORECASE)
    browser_patterns = {
        "Firefox": re.compile(r"Firefox", re.IGNORECASE),
        "Chrome": re.compile(r"Chrome", re.IGNORECASE),
        "Safari": re.compile(r"Safari", re.IGNORECASE),
        "Internet Explorer": re.compile(r"MSIE|Trident", re.IGNORECASE)
    }
    total_requests = 0
    image_requests = 0
    browser_counter = Counter()
    hourly_hits = Counter()
    reader = csv.reader(log_data)
    for row in reader:
        total_requests += 1
        path, timestamp, user_agent, status, size = row
        if image_extensions.match(path):
            image_requests += 1
        for browser, pattern in browser_patterns.items():
            if pattern.search(user_agent):
                browser_counter[browser] += 1
                break
        hour = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").hour
        hourly_hits[hour] += 1
        print(row)
    image_percentage = (image_requests / total_requests) * 100
    print(f"Image requests account for {image_percentage:.2f}% of all requests.")
    most_popular_browser = browser_counter.most_common(1)[0][0]
    print(f"The most popular browser is: {most_popular_browser}")
    print("\nHits per hour:")
    for hour, hits in sorted(hourly_hits.items()):
        print(f"Hour {hour:02d} has {hits} hits")
    


def main(url):
    print(f"Running main with URL = {url}...")
    log_data = download_file(url)
    process_log_data = download_file(url)
    print(f"Downloaded {len(log_data)} lines of log data.")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
