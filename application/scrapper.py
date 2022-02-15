import requests, operator, json
from bs4 import BeautifulSoup
from application import db
from .models import Knowledge
import re

def page_reading(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    title = soup.find(id='firstHeading').text #soup.title.text
    content = soup.find(id='content').text
    allWords = content.lower()
    allWords = re.sub("[^a-z0-9A-Zàâäéèêëïîôöùûüÿç]+", " ", allWords)
    return allWords, title

def word_counting(text):
    counts = dict()
    words = text.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def get_json_tree(url):
    page, title = page_reading(url)
    word_count = word_counting(page)
    sorted_r = dict(sorted(word_count.items(), key=operator.itemgetter(1),reverse=True))
    json_result = json.dumps(sorted_r,ensure_ascii=False)
    return json_result, page, title

def put_into_db(url,json_tree,page,title):
    if db.session.query(Knowledge.id).filter_by(url=url).first() is None:
        new_Knowledge = Knowledge(url=url,json_tree=json_tree,raw_text=page,title=title)
        db.session.add(new_Knowledge)
        db.session.commit()
    else:
        print("Nice try !")

# def getTextFromUrl(url : str, nbChars : int):
#     res = requests.get(url)
#     html_page = res.content
#     soup = BeautifulSoup(html_page, 'html.parser')
#     allWords = ''
#     for strPiece in soup.stripped_strings:
#         allWords += ' ' + strPiece.lower()
#     allWords = re.sub("[^a-z0-9A-Zàâäéèêëïîôöùûüÿç]+", " ", allWords)
#     # allWords = re.sub(r"""[!?".<>(){}@%&*/[/]""", "", allWords)
#     # smallerWordsRemoved = ''
#     # for word in allWords.split(' '):
#     #     if(len(word) > (nbChars - 1)):
#     #         smallerWordsRemoved += ' ' + word
#     return allWords