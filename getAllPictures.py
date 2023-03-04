import os
import requests
from bs4 import BeautifulSoup

url = ''

folder_path = 'images'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

images = soup.find_all('img')

for i, img in enumerate(images):
    img_url = img.get('src')
    response = requests.get(img_url)
    open(f'{folder_path}/img{i}.jpg', 'wb').write(response.content)
