import argparse
import urllib.request
import datetime
import csv
import io


def downloadData(url):
    
    with urllib.request.urlopen(url) as response:
        response = response.read().decode("utf-8")

    return response

def processData(file_content):
    csv_data = csv.reader(io.StringIO(file_content))
    image_counter = 0
    total_requests = 0
    line_counter = 0

    browser_counter = {
        "Chrome": 0,
        "Firefox": 0,
        "Safari": 0,
        "MSIE": 0
    }

    hourly_hits = {}

    for row in csv_data:
        line_counter += 1
        path_to_file = row[0]
        datetime_accessed = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        browser = row[2]
        print(f"Path = {path_to_file} | Hour accessed = {datetime_accessed.hour} | Browser = {browser}")

    if path_to_file.endswith(("jpg", "gif", "png")):
            image_counter += 1

    if "Chrome" in browser:
            browser_counter["Chrome"] += 1
    elif "Firefox" in browser:
            browser_counter["Firefox"] += 1
    elif "Safari" in browser:
            browser_counter["Safari"] += 1
    elif "MISIE" in browser or "Trident" in browser:
            browser_counter["MISIE"] += 1

    hour = datetime_accessed.hour
    if hour not in hourly_hits:
            hourly_hits[hour] = 0
    hourly_hits[hour] += 1
    

    percent_images = image_counter / line_counter * 100
    print(f"Image requests account for {percent_images:.2f}% of all requests")

    most_popular_browser = max(browser_counter, key=browser_counter.get)
    print(f"The most popular browser is: {most_popular_browser}")

    print("\nHits per hour (sorted by hit count):")
    for hour, hits in sorted(hourly_hits.items(), key=lambda x: x[1], reverse=True):
        print(f"Hour {hour:02d} has {hits} hits")
    
    
def main(url):
    print(f"Running main with URL = {url}...")
    url_data = downloadData(url)
    processData(url_data)
   
    
if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
