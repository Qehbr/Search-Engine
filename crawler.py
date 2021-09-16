#
# Simple Web Crawler
#

# Libraries
import json
import requests
from bs4 import BeautifulSoup

# starting url to crawl
start_url = 'https://quotes.toscrape.com'
# depth to go
depth = 2
# array of data crawled
crawledData = []
# tags that will be stored
textTags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']


#
# crawl function
#
def crawl(url, depth):
    # perform http get request
    try:
        print('Crawling URL: "%s" on depth: "%d" ' % (url, depth))
        response = requests.get(url)
    except:
        print('Failed to perform HTTP GET request on "%s"\n' % url)
        return

    # get page in content variable
    content = BeautifulSoup(response.text, 'lxml')

    # get description from the site from allowed tags above in textTags variable
    description = ""
    try:
        for tag in content.findAll():
            if tag.name in textTags:
                description += tag.text.strip().replace('\n', ' ')
    except:
        pass

    # get title from the site
    try:
        title = content.find('title').text
    except:
        title = ""

    # create result object containing data
    result = {
        'url': url,
        'title': title.strip().replace('\n', ''),
        'description': description.strip().replace('\n', '')
    }

    # add it to crawledData array
    crawledData.append(result)

    # if depth is exhausted
    if depth == 0:
        return

    # get all links
    links = content.findAll('a')
    # crawl each link
    for link in links:

        try:
            if 'http' in link['href']:
                crawl(link['href'], depth - 1)
        except KeyError:
            pass
    return


# calling crawl function with given depth
crawl(start_url, depth)

# TODO tempoorarily writing crawled data to JSON file
with open('data.json', 'w') as json_file:
    fileContent = ''
    for entry in crawledData:
        fileContent += json.dumps(entry, indent=2)
    json_file.write(fileContent)
    print("Success! Length of crawled data", len(crawledData))
