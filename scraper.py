import requests
from bs4 import BeautifulSoup

req = requests.get(
    'https://www.nseindia.com/market-data/top-gainers-loosers/index.html')
soup = BeautifulSoup(req.content, 'html.parser')

# with open('https://www.nseindia.com/market-data/top-gainers-loosers') as html_file:
#     content = html_file.read()
#     print(content)

print(soup.prettify())
