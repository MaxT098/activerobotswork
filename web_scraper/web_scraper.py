import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.drawing.image import Image
import os

def scrape_skus_and_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    skus = []
    images = []

    # Assuming the SKUs are present in elements with a specific class, adjust the class name accordingly
    sku_elements = soup.find_all('span', class_='related-product-sku')
    for element in sku_elements:
        skus.append(element.text.strip())

    # Assuming the images are present in <img> tags with a specific class, adjust the class name accordingly
    image_elements = soup.find_all('img', class_='product-image-photo')
    for element in image_elements:
        image_url = element['src']
        images.append(image_url)

    return skus, images

if __name__ == "__main__":
    # Replace 'https://example.com/products' with the actual URL of the website you want to scrape
    url_to_scrape = 'https://www.active-robots.com/robot-shop.html'
    skus, image_urls = scrape_skus_and_images(url_to_scrape)

    # Create a folder to save the downloaded images
    download_folder = 'downloaded_images'
    os.makedirs(download_folder, exist_ok=True)

    # Download images and store local paths in a list
    local_image_paths = []
    for i, image_url in enumerate(image_urls):
        filename = f'image_{i + 1}.jpg'
        filepath = os.path.join(download_folder, filename)
        response = requests.get(image_url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        local_image_paths.append(filepath)

    # Create an Excel workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Product Data'

    worksheet['A1'] = 'SKU'
    worksheet['B1'] = 'Image'

    for row, (sku, local_image_path) in enumerate(zip(skus, local_image_paths), start=2):
        worksheet[f'A{row}'] = sku

        img = Image(local_image_path)

        worksheet.column_dimensions['B'].width = 30
        worksheet.row_dimensions[row].height = img.height

        worksheet.add_image(img, f'B{row}')

    # Save the Excel workbook
    excel_file_path = 'product_data.xlsx'
    workbook.save(excel_file_path)
    print(f"Data and images saved to '{excel_file_path}'.")

