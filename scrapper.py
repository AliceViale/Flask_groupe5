import requests
import re
from bs4 import BeautifulSoup

def getTextFromUrl(url : str):
    """Scraps text from a given url and return a string of text only."""
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    allWords = ''

    for strPiece in soup.stripped_strings:
        allWords += ' ' + strPiece.lower()

    allWords = re.sub("[^a-zA-Zàâäéèêëïîôöùûüÿç]+", " ", allWords)

    smallerWordsRemoved = ''

    for word in allWords.split(' '):
        if(len(word) > 2):
            smallerWordsRemoved += ' ' + word

    return smallerWordsRemoved

# print(getTextFromUrl('https://fr.wikipedia.org/wiki/R%C3%A9cepteur_sensoriel'))


