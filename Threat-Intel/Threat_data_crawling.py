import requests
from bs4 import BeautifulSoup

# Function to crawl and scrape web pages
def crawl_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract and process relevant threat intelligence data from the soup object
            # For example, you can find IOCs (Indicators of Compromise) like IP addresses, domains, hashes, etc.
            # and store them in a list or database for further analysis.

            # Example: Extract IP addresses from the page
            ip_addresses = []
            for element in soup.find_all('span', class_='ip-address'):
                ip_addresses.append(element.text.strip())

            return ip_addresses

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Main function to initiate the web crawler
def main():
    # List of URLs to crawl (threat intelligence sources)
    urls = [
        "https://www.malwarebytes.com/blog/category/threat-intelligence",
        "https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/?sort-by=newest-oldest&date=any",
        "https://www.crowdstrike.com/blog/category/threat-intel-research/"
        "https://redcanary.com/topic/threat-intelligence/"
        "https://www.talosintelligence.com/"
        "https://www.spamhaus.org/"
        # Add more URLs as needed
    ]

    threat_intelligence_data = []

    for url in urls:
        data = crawl_page(url)
        if data:
            threat_intelligence_data.extend(data)

    # Print or process the collected threat intelligence data
    print("Threat Intelligence Data:")
    print(threat_intelligence_data)

if __name__ == "__main__":
    main()