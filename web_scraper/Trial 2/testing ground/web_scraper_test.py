import requests
from bs4 import BeautifulSoup

# Function to scrape product information (product name, GTIN code, and image URL)
def scrape_product_info(url):
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product name
        product_name_element = soup.find('h1', {'class': 'product-title', 'itemprop': 'name'})
        if product_name_element:
            product_name = product_name_element.text.strip()
            print(f"Product Name: {product_name}")

        # Extract the GTIN code
        gtin_code_element = soup.find('span', {'itemprop': 'gtin13'})
        if gtin_code_element:
            gtin_code = gtin_code_element.text.strip()
            print(f"GTIN Code: {gtin_code}")

        # Locate and extract the image URL using XPath
        image_element = soup.find('img', {'xpath': '/html/body/main/div/div[2]/div[1]/div[2]/form/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div/div/picture/img'})
        if image_element:
            image_url = image_element['src']
            print(f"Image URL: {image_url}")

if __name__ == "__main":
    print("Script started")
    
    initial_url = 'https://www.nodna.de/Nexus-Robot-2WD-mobile-Arduino-robotics-car-10004'

    # Scrape product information for the single webpage
    scrape_product_info(initial_url)
