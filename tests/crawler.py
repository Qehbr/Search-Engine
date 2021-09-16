#
# Stack Overflow Questions scraper
#


# libraries
import json
import requests
from bs4 import BeautifulSoup


def fetch(url):
    # getting response from given URL
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Given URL: "%s" is not available' % url)
        return
    # getting all content from the page
    content = BeautifulSoup(response.text, 'lxml')
    # treating the links
    links = content.findAll('a', {'class': 'question-hyperlink'})
    trashQuestionsLinks = content.findAll('a', {'class': 'js-gps-track'})
    for link in trashQuestionsLinks:
        try:
            links.remove(link)
        except ValueError:
            continue

    # getting descriptions for the links
    description = content.findAll('div', {'class': 'excerpt'})

    # creating questions with appropriate data
    for index in range(0, len(links)):
        question = {
            'title': links[index].text.strip(),
            'url': links[index]['href'],
            'description': description[index].text.strip().replace('\n', '')
        }
        # print question with json
        print(index, json.dumps(question, indent=2))


# variables
start_url = 'https://stackoverflow.com/questions?tab=newest&pagesize=50'
# get maximum number of pages on stackoverflow
res = requests.get(start_url)
content = BeautifulSoup(res.text, 'lxml')
pageNumber = int(content.findAll('a', {'class': 'js-pagination-item'})[4].text)
# loop through all pages and fetch each of them
for index in range(0, pageNumber):
    print("Page Number: " + str(index) + "\n")
    fetch(start_url+"&page="+str(index))
