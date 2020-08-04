'''
This program (so far) uses the PRAW api and scrapes reddit for relevant results for search queries. 
'''
from redditApiCalls import redditApiCalls
from webScraper import webScraper
from flask import Flask, render_template, request
import praw
import requests

app = Flask(__name__)

# setting up reddit api
reddit = praw.Reddit(client_id = 'htRyDsppzn0qLg',
                     client_secret = 'unJNN6CZtD510Dxe6GqF9ELrnGU',
                     user_agent = 'web app:redditScraper 1.0 by /u/Latarax')

# confirm that reddit api has connected
print(reddit.read_only)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def info():
    # grabbing the user query from the html form
    query = request.form['query']
    website_urls = redditApiCalls(query)
    cards2Display = webScraper(website_urls, query)

    return render_template('info.html', cards2Display=cards2Display)


if __name__ == '__main__':
    app.run(debug=True)