import requests
import re
from bs4 import BeautifulSoup

def getTextFromUrl(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    output = ''

    for string in soup.stripped_strings:
        output += ' ' + string.lower()

    output = re.sub("[^a-zA-Zàâäéèêëïîôöùûüÿç]+", " ", output)

    smallerWordsRemoved = ''

    for word in output.split(' '):
        if(len(word) > 2):
            smallerWordsRemoved += ' ' + word

    return smallerWordsRemoved

# print(getTextFromUrl('https://fr.wikipedia.org/wiki/R%C3%A9cepteur_sensoriel'))


