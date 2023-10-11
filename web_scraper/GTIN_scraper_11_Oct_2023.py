import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage you want to scrape
url = "https://www.nodna.de/Nexus-Robot-2WD-mobile-Arduino-robotics-car-10004"  # Replace with the actual URL

# Send an HTTP GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <span> elements with itemprop="gtin13"
    gtin_spans = soup.find_all('span', itemprop='gtin13')
    
    # Create a list to store GTIN code and name pairs
    gtin_name_pairs = []
    
    for span in gtin_spans:
        # Extract the GTIN code
        gtin_code = span.text
        
        # Find the closest <span> element with itemprop="name"
        name_span = span.find_previous('span', itemprop='name')
        
        if name_span:
            # Extract the name
            name = name_span.text
            
            # Append the GTIN code and name to the list
            gtin_name_pairs.append([name, gtin_code])
    
    # Export the data to a CSV file
    with open('gtin_data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'GTIN Code'])
        csv_writer.writerows(gtin_name_pairs)
    
    print("Data exported to gtin_data.csv")
else:
    print("Failed to fetch the webpage")
