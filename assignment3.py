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
    line_counter = 0

    chrome_counter = 0
    safari_counter = 0
    msie_counter = 0
    ffox_counter = 0
    for row in csv_data:
        line_counter += 1
        path_to_file = row[0]
        datetime_accessed = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        browser = row[2]
        print(f"Path = {path_to_file} | Hour accessed = {datetime_accessed.hour} | Browser = {browser}")
        if path_to_file.endswith("jpg"):
            image_counter += 1

        if browser.find("Chrome") != -1:
            chrome_counter += 1

    percent_images = image_counter / line_counter * 100
    print(f"Image requests account for {percent_images}% of all requests")
    
    
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
    
