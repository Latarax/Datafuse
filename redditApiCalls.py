import praw

# setting up reddit api
reddit = praw.Reddit(client_id='htRyDsppzn0qLg',
                     client_secret='unJNN6CZtD510Dxe6GqF9ELrnGU',
                     user_agent='web app:redditScraper 1.0 by /u/Latarax')

# confirm that reddit api has connected
print(reddit.read_only)


def redditApiCalls(query):
    result_counter = 0
    website_urls = []

    # iterating through results of search query
    for submission in reddit.subreddit('all').search(query=query, time_filter='week', sort='top', limit=50):
        # break the loop if 3 valid submissions are found
        if result_counter == 3:
            break
        # skipping results that dont have an external url
        if submission.is_self:
            continue
        # skip image submissions and specific articles
        elif url_title_checker(submission):
            continue
        # print title and url for filtered results and increment
        else:
            print(submission.title)
            print(submission.url)
            website_urls.append(submission.url)
            result_counter += 1

    return website_urls


def url_title_checker(submission):
    if 'imgur' in submission.url or 'redd.it' in submission.url or 'i.reddituploads' in submission.url or '.jpg' in submission.url or '.gif' in submission.url or 'gfycat' in submission.url or 'TIL' in submission.title or 'media.discord' in submission.url or 'clips.twitch' in submission.url or 'youtu.be' in submission.url or 'twitter' in submission.url:
        return True
    else:
        return False
