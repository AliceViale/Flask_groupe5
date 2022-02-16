import requests
import re
from bs4 import BeautifulSoup

def getTextFromUrl(url : str, nbChars : int):
    """Scraps text from a given url and returns a string of text only words of nbChars length."""
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    allWords = ''

    for strPiece in soup.stripped_strings:
        allWords += ' ' + strPiece.lower()

    allWords = re.sub("[^a-zàâäéèêëïîôöùûüÿç]+", " ", allWords)

    smallerWordsRemoved = ''

    for word in allWords.split(' '):
        if(len(word) > (nbChars - 1)):
            smallerWordsRemoved += ' ' + word

    return smallerWordsRemoved

# print(getTextFromUrl('https://fr.wikipedia.org/wiki/R%C3%A9cepteur_sensoriel', 6))


