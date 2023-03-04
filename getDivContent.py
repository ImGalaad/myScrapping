from bs4 import BeautifulSoup
import requests

url = ''

response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

div_class = ''

matching_div = soup.find('div', class_=div_class)

print(matching_div.contents)
