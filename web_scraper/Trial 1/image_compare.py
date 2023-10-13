import pandas as pd
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
import requests
from io import BytesIO

def preprocess_image(image_url, target_size=(75, 75)):
    # Download the image from the URL
    response = requests.get(image_url)
    image_content = response.content
    
    # Load the image using OpenCV from the downloaded content
    image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)
    
    # Resize the image to the target size
    image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    
    # Convert the image to grayscale for certain comparison methods
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Normalize the image pixels to values between 0 and 1
    normalized_image = grayscale_image / 255.0
    
    return normalized_image

def compare_images(image1, image2):
    # Calculate the Structural Similarity Index (SSIM) between two images
    similarity_score, _ = ssim(image1, image2, data_range=1.0, full=True)
    return similarity_score

def main():
    # Replace 'your_csv_file.csv' with the actual path to your CSV file
    csv_file_path = 'export_magento.csv'
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Create lists to store the results
    image_pair_list = []
    similarity_score_list = []
    highlight_list = []
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Get the URLs to the two images from the second column
        image_url1 = row[1]  # Assuming URLs are in the second column (index 1)
        image_url2 = row[2]  # Assuming the second URL is in the third column (index 2)
        
        # Preprocess the images and compare them
        image1 = preprocess_image(image_url1)
        image2 = preprocess_image(image_url2)
        similarity_score = compare_images(image1, image2)
        
        # Store the results in lists
        image_pair_list.append((image_url1, image_url2))
        similarity_score_list.append(similarity_score)
        
        # Check if similarity is below 0.7 (70% threshold) and mark for highlighting
        if similarity_score < 0.7:
            highlight_list.append("Yes")
        else:
            highlight_list.append("No")
    
    # Create a DataFrame with the results
    result_df = pd.DataFrame({
        'Image Pair': image_pair_list,
        'Similarity Score': similarity_score_list,
        'Highlight': highlight_list
    })
    
    # Output the DataFrame to a CSV file
    result_df.to_csv('image_similarity_results.csv', index=False)

if __name__ == "__main__":
    main()
