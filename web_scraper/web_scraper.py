import requests
from bs4 import BeautifulSoup
import csv
import os
import urllib.request

def scrape_skus_and_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    skus = []
    images = []

    # Assuming the SKUs are present in elements with a specific class, adjust the class name accordingly
    sku_elements = soup.find_all('span', class_='sku')
    for element in sku_elements:
        skus.append(element.text.strip())

    # Assuming the images are present in <img> tags with a specific class, adjust the class name accordingly
    image_elements = soup.find_all('img', class_='thumbnail-image')
    for element in image_elements:
        image_url = element['src']
        images.append(image_url)

    return skus, images

if __name__ == "__main__":
    # Replace 'https://example.com/products' with the actual URL of the website you want to scrape
    url_to_scrape = 'https://example.com/products'
    skus, images = scrape_skus_and_images(url_to_scrape)

    # Create a CSV file and write the data to it
    csv_file_path = 'product_data.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['SKU', 'Image URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for sku, image_url in zip(skus, images):
            writer.writerow({'SKU': sku, 'Image URL': image_url})

    print(f"Data saved to '{csv_file_path}'.")

