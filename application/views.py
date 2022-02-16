# from crypt import methods
from flask import Blueprint, render_template, request, Flask, jsonify, abort, make_response
import validators
from . import db
from .models import Knowledge
from .scrapper import get_json_tree, put_into_db
from flask_restful import Api, Resource, reqparse, fields, marshal

# Début du code du site de test

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
    url_query = Knowledge.query.with_entities(Knowledge.url).order_by(Knowledge.id)
    url_list = []
    for url in url_query:
        url_list.append(url[0])
    title_query = Knowledge.query.with_entities(Knowledge.title).order_by(Knowledge.id)
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

# Debut du code de l'API REST

tree_fields = {
    'id' : fields.Integer,
    'url' : fields.String,
    'title' : fields.String,
    'json_tree' : fields.String,
    'raw_text' : fields.String
}

class TreeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str)
        self.reqparse.add_argument('idtree', type=int)
        super(TreeAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        url = args['url']
        print(url)
        returnMessage = ""
        if validators.url(url):
            if "wikipedia.org" in url:
                json_tree, page, title = get_json_tree(url)
                put_into_db(url,json_tree,page, title)
                returnMessage = f"Page {title} succesfully parsed."
            else:
                returnMessage = "We only parse 'wikipedia.org' pages."
        else:
            returnMessage = "This is not a valid url."
        return {'message' : returnMessage}

    def get(self):
        args = self.reqparse.parse_args()
        url = args['url']
        json_result, page, title = get_json_tree(url)
        return { 'url' : url, 'json' : json_result }

    def put(self, id):
        # task = [task for task in tasks if task['id'] == id]
        # if len(task) == 0:
        #     abort(404)
        # task = task[0]
        # args = self.reqparse.parse_args()
        # for k, v in args.items():
        #     if v is not None:
        #         task[k] = v
        # return {'task': marshal(task, task_fields)}
        return ""

    def delete(self):
        args = self.reqparse.parse_args()
        url = args['url']
        db.session.query(Knowledge).filter(Knowledge.url == url).delete()
        db.session.commit()
        returnMessage = f"Url '{url}' successfully deleted."
        return {'message' : returnMessage}


