import requests
import os

# Changables
base_url = "https://image.slidesharecdn.com/url_pdf-{}-2048.jpg" # Update the url (I am using 2048 quality)
output_folder = "downloaded_images"
pdf_filename = "output.pdf"
num_images = 841  # Number of images to download

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Downloading images
for i in range(1, num_images + 1):
    img_path = os.path.join(output_folder, f"{i}.png")
    
    # Checking if the image already exists
    if os.path.exists(img_path):
        print(f"{img_path} already exists. Skipping download.")
        continue  # Skip to the next image if it exists

    url = base_url.format(i)
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Downloaded: {img_path}")
    else:
        print(f"Failed to download image {i}: {response.status_code}")
