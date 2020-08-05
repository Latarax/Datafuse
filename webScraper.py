from bs4 import BeautifulSoup
import requests

# class blueprint for a news card, which will display the title and first few sentences, and url of an article
class News_Card:
    def __init__(self, title, content, url):
        self.title = title
        self.content = content
        self.url = url

    def display(self):
        print(f"Title of article: {self.title}")
        print(f"Content of article: {self.content}")
        print(f"Url of article: {self.url}")



def webScraper(website_urls, query, num_results):

    # headers to bypass website not allowing scraping
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)    AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/41.0.2227.1 Safari/537.36'}

    cards = [News_Card("","","") for i in range(num_results)]
    cards2Display = [[] for i in range(num_results)]
    card_count = 0

    # testing scraping on one of the results from reddit
    for url in website_urls:
        source = requests.get(url, headers = headers) .text
        soup = BeautifulSoup(source, 'lxml')
        cards[card_count].url = url
        cards[card_count].title = ""
        cards[card_count].content = ""
        
        for match in soup.find_all('h1'):
            if query.lower() in match.text.lower():
                cards2Display[card_count].insert(0, match.text)
                cards[card_count].title = match.text
                break

        if not cards2Display[card_count]:
            cards2Display[card_count].insert(0, f"{query.capitalize()} Article")            

        for match in soup.find_all('p'):
            if len(match.text) > 134:
                cards2Display[card_count].insert(1, match.text)
                cards[card_count].content = match.text   
                break     
        
        cards2Display[card_count].insert(2, url)
        card_count += 1

        
    for card in cards:
        card.display()
        
    return cards2Display