'''
This program (so far) uses the PRAW api and scrapes reddit for relevant results for search queries. 
'''

import praw
import requests
from bs4 import BeautifulSoup

# headers to bypass website not allowing scraping
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/41.0.2227.1 Safari/537.36'}

# setting up reddit api
reddit = praw.Reddit(client_id = 'htRyDsppzn0qLg',
                     client_secret = 'unJNN6CZtD510Dxe6GqF9ELrnGU',
                     user_agent = 'web app:redditScraper 1.0 by /u/Latarax')

# confirm that reddit api has connected
print(reddit.read_only)
print(reddit.user.me())

# this is an increment variable to limit amount of results
count = 0


# iterating through results of search query
for submission in reddit.subreddit('all').search(query='obama', time_filter='all', sort='top', limit=50):
    if count == 3:
        break
    # skipping results that dont have an external url
    if submission.is_self:
        continue
    # skip image submissions (hard coded method)
    elif 'imgur' in submission.url or 'redd.it' in submission.url or 'i.reddituploads' in submission.url or '.jpg' in submission.url:
        continue
    # print title and url for filtered results and increment
    else:
        print(submission.title)
        print(submission.url)
        count += 1
'''
# testing scraping on one of the results from reddit
source = requests.get('https://thehill.com/homenews/administration/432871-trump-nixes-public-report-on-drone-strike-deaths', headers = headers).text

soup = BeautifulSoup(source, 'lxml')

sample_text = []

for match in soup.find_all('h1'):
    print(match.text)
    sample_text.append(match.text)




# for match in soup.find_all('p'):
#     if len(match.text) < 200:
#         continue
#     else:
#         print(match.text)
#         print()

'''