from application import create_app
from flask import render_template
from application.scrapper import put_into_db, get_json_tree
from application.forestry import dict_word_occurence_to_tree
import json

app = create_app()
app.app_context().push()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

url = 'https://fr.wikipedia.org/wiki/Belzébuth'

json_tree, page = get_json_tree(url)
put_into_db(url,json_tree,page)

json_tree_dict = json.loads(json_tree)

tree = dict_word_occurence_to_tree(json_tree_dict)
print(tree)

# if __name__ == '__main__':
#     app.run(debug=True)