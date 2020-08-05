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
    time_filter = request.form['time-filter'].lower()
    num_results = int(request.form['result-amount'])
    print(f"Time Filter: {time_filter}")
    print(f"Result Amount: {num_results}")
    website_urls = redditApiCalls(query, time_filter, num_results)
    cards2Display = webScraper(website_urls, query, num_results)

    return render_template('info.html', cards2Display=cards2Display)


if __name__ == '__main__':
    app.run(debug=True)