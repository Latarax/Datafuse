import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/41.0.2227.1 Safari/537.36'}

source = requests.get('https://www.nbcnews.com/news/us-news/woman-who-called-michelle-obama-ape-sentenced-jail-defrauding-fema-n1012936', headers = headers).text

soup = BeautifulSoup(source, 'lxml')

for match in soup.find_all('p'):
    print(match.text)
    print()