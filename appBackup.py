'''
This program (so far) uses the PRAW api and scrapes reddit for relevant results for search queries. 
'''

from flask import Flask, render_template, request
import praw
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

 # headers to bypass website not allowing scraping
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)    AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/41.0.2227.1 Safari/537.36'}

# setting up reddit api
reddit = praw.Reddit(client_id = 'htRyDsppzn0qLg',
                     client_secret = 'unJNN6CZtD510Dxe6GqF9ELrnGU',
                     user_agent = 'web app:redditScraper 1.0 by /u/Latarax')

# confirm that reddit api has connected
print(reddit.read_only)

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


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def info():
    # count is an increment variable to limit amount of results
    count = 0
    website_urls = []
    sample_text = []

    # grabbing the user query from the html form
    query = request.form['query']
    
    # iterating through results of search query
    # all, day, month, week, year
    for submission in reddit.subreddit('all').search(query=query,     time_filter='week', sort='top', limit=50):
        # break the loop if 3 valid submissions are found
        if count == 3:
            break
        # skipping results that dont have an external url
        if submission.is_self:
            continue
        # skip image submissions (hard coded method)
        elif 'imgur' in submission.url or 'redd.it' in submission.url or    'i.reddituploads' in submission.url or '.jpg' in submission.url or '.gif' in submission.url or 'gfycat' in submission.url or 'TIL' in submission.title or 'media.discord' in submission.url or 'clips.twitch' in submission.url:
            continue
        # print title and url for filtered results and increment
        else:
            print(submission.title)
            print(submission.url)
            website_urls.append(submission.url)
            count += 1

    cards = [News_Card("","","") for i in range(3)]
    cards2Display = [[] for i in range(3)]
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


    return render_template('info.html', cards2Display=cards2Display)


if __name__ == '__main__':
    app.run(debug=True)