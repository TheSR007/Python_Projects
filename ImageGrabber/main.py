import requests
from io import BytesIO
from PIL import Image 

def download_and_save_image(url, local_filename):
    response = requests.get(url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(local_filename)
        print(f"Image saved as {local_filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

for img in range(1,165):
    download_and_save_image(f'url to img{img}',f'{img}.jpg')
