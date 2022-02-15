from flask import Blueprint, render_template, request
import validators
from . import db
from .models import Knowledge
from .scrapper import get_json_tree, put_into_db

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
def home():
    data = request.form
    if request.method == 'POST':
        url = data.get('url')
        if url is not None:
            if validators.url(url):
                if "wikipedia.org" in url:
                    json_tree, page, title = get_json_tree(url)
                    put_into_db(url,json_tree,page, title)
        if data.get('banish') is not None:
            clear_db()
        if data.get('revoke') is not None:
            remove_url(data.get('revoke'))
    url_list, title_list = get_url_list()
    nb_url = len(url_list)
    return render_template('home.html', title_list=title_list, url_list=url_list, nb_url=nb_url)

def get_url_list():
    url_query = Knowledge.query.with_entities(Knowledge.url)
    url_list = []
    for url in url_query:
        url_list.append(url[0])
    title_query = Knowledge.query.with_entities(Knowledge.title)
    title_list = []
    for title in title_query:
        title_list.append(title[0])
    return url_list, title_list

def clear_db():
    db.session.query(Knowledge).delete()
    db.session.commit()

def remove_url(url):
    db.session.query(Knowledge).filter(Knowledge.url == url).delete()
    db.session.commit()