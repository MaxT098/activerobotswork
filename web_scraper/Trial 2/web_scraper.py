import requests
from bs4 import BeautifulSoup
import openpyxl
import os

# Function to scrape product information (product name and GTIN code)
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

if __name__ == "__main__":
    initial_url = 'https://www.nodna.de/Robot-Arms-Grippers'
    max_depth = 3  # Set the maximum depth for subpage exploration

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Product Data'

    worksheet['A1'] = 'Product Name'
    worksheet['B1'] = 'GTIN Code'

    # Perform the recursive search for product information
    final_row = scrape_product_info(initial_url, worksheet)

    # Save the Excel workbook
    excel_file_path = 'product_data.xlsx'
    workbook.save(excel_file_path)
    print(f"Data saved to '{excel_file_path}'.")
