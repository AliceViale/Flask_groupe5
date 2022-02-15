import requests, operator, json
from bs4 import BeautifulSoup
from application import db
from .models import Knowledge
import re

# def page_reading(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content,features="html.parser")
#     link = soup.stripped_strings
#     return link

def page_reading(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    allWords = ''
    for strPiece in soup.stripped_strings:
        allWords += ' ' + strPiece.lower()
    allWords = re.sub("[^a-z0-9A-Zàâäéèêëïîôöùûüÿç]+", " ", allWords)
    return allWords

def word_counting(text):
    counts = dict()
    words = text.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

# def word_count_merging(dict1, dict2):
#     merged = dict1.copy()
#     for key,value in dict2.items():
#         if key in merged.keys():
#             merged[key] += value
#         else:
#             merged[key] = value
#     return merged

# def full_page_word_counts(url):
#     page = page_reading(url)
#     final_count = dict()
#     for t in page:
#         word_count = word_counting(t)
#         final_count = word_count_merging(final_count,word_count)
#     return final_count

# def get_json_tree(url):
#     result = full_page_word_counts(url)
#     sorted_r = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
#     json_result = json.dumps(sorted_r,ensure_ascii=False)
#     return json_result

def get_json_tree(url):
    result = word_counting(page_reading(url))
    sorted_r = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
    json_result = json.dumps(sorted_r,ensure_ascii=False)
    return json_result

def put_into_db(url,json_tree):
    if db.session.query(Knowledge.id).filter_by(url=url).first() is None:
        new_Knowledge = Knowledge(url=url,json_tree=json_tree)
        db.session.add(new_Knowledge)
        db.session.commit()
    else:
        print("Nice try !")

# def getTextFromUrl(url : str): #, nbChars : int):
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