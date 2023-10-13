import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.drawing.image import Image
import os

# Function to scrape product information (product name and GTIN code) and extract the image using XPath
def scrape_product_info(url, worksheet, current_row=2, current_depth=0):
    if current_depth > max_depth:
        return current_row

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product name from the specific location
        product_name_element = soup.find('h1', {'class': 'product-title', 'itemprop': 'name'})
        if product_name_element:
            product_name = product_name_element.text.strip()
            worksheet[f'A{current_row}'] = product_name

        # Extract the GTIN code from the specific location
        gtin_code_element = soup.find('span', {'itemprop': 'gtin13'})
        if gtin_code_element:
            gtin_code = gtin_code_element.text.strip()
            worksheet[f'B{current_row}'] = gtin_code

        # Locate and extract the image using XPath
        image_element = soup.find('img', {'xpath': '/html/body/main/div/div[2]/div[1]/div[2]/form/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div/div/picture/img'})
        if image_element:
            image_url = image_element['src']

            # Download and insert the image
            filename = f'image_{current_row - 2}.jpg'
            filepath = os.path.join(download_folder, filename)
            response = requests.get(image_url, stream=True)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            worksheet[f'C{current_row}'] = Image(filepath)

    # Find links to subpages and recursively scrape them
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        subpage_links = soup.find_all('a', href=True)

        for link in subpage_links:
            subpage_url = link['href']
            if subpage_url.startswith(initial_url):
                # Recursively scrape subpages
                current_row = scrape_product_info(subpage_url, worksheet, current_row, current_depth + 1)

    return current_row

if __name__ == "__main":
    initial_url = 'https://www.nodna.de/Robots-Vehicles'
    max_depth = 3  # Set the maximum depth for subpage exploration

    download_folder = 'downloaded_product_images'
    os.makedirs(download_folder, exist_ok=True)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Product Data'

    worksheet['A1'] = 'Product Name'
    worksheet['B1'] = 'GTIN Code'
    worksheet['C1'] = 'Image'

    # Perform the recursive search for product information
    final_row = scrape_product_info(initial_url, worksheet)

    # Save the Excel workbook
    excel_file_path = 'product_data.xlsx'
    workbook.save(excel_file_path)
    print(f"Data and images saved to '{excel_file_path}'.")
