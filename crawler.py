#
# Surfearch Web Crawler module
#

# Libraries
import json
import requests
from bs4 import BeautifulSoup
import pymongo


class Crawler():
    # Connecting to database
    print("Connecting to database")
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://<username>:<password>@<dbname>.awgu4.mongodb.net/<dbname>?retryWrites=true&w=majority")
        db = client.searchResults
        print("Sucessfully connected to database")
    except Exception:
        print('Error connection to database')

    # array of data crawled
    searchResults = []
    # tags that will be stored
    # TODO use tags
    # textTags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    textTags = ['p']

    #
    # crawl function
    #

    def crawl(self, url, depth):
        # perform http get request
        try:
            print('Crawling URL: "%s" on depth: "%d" ' % (url, depth))
            response = requests.get(
                url, headers={'user-agent': 'search-engine-crawler'})
        except:
            print('Failed to perform HTTP GET request on "%s"\n' % url)
            return

        # get page in content variable
        content = BeautifulSoup(response.text, 'lxml')

        # get description from the site from allowed tags above in textTags variable
        description = ""
        try:
            for tag in content.findAll():
                if tag.name in self.textTags:
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

        # add it to searchResults array
        self.searchResults.append(result)

        # if depth is exhausted
        if depth == 0:
            return

        # get all links
        links = content.findAll('a')
        # crawl each link
        for link in links:

            try:
                if 'http' in link['href']:
                    self.crawl(link['href'], depth - 1)
            except KeyError:
                pass
    
    # Print array of searchResults 
    def printData(self):
        # for entry in self.searchResults:
        #     print(entry)
        # print("\nSuccess! Nubmer of entries scraped", len(self.searchResults))

        for entry in self.db.searchResults.find({'$text':{'$search':'Quotes to Scrape'}}):
            print(entry)

    # Insets results to database 
    def insertResults(self):
        searchResults = self.db.searchResults
        searchResults.insert_many(self.searchResults)
        searchResults.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT),

        ], name='searchResults')



