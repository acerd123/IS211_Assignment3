import argparse
import urllib.request
import datetime


def downloadData(url):
    
    with urllib.request.urlopen(url) as response:
        response = response.read().decode("utf-8")

    return response

def main(url):
    print(f"Running main with URL = {url}...")
    url_data = downloadData(url)
    print(url_data)
   
    
if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
