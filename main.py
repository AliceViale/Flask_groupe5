from application import create_app
from flask import render_template
from application.scrapper import get_json_tree, put_into_db
from networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import json

app = create_app()
app.app_context().push()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


def to_tree(dict_tree):
    tree=Graph()
    all_tuple = list(dict_tree.items())
    fifo = []
    fifo.append(all_tuple[1])
    fifo.append(all_tuple[2])
    tree.add_node(all_tuple[0])
    tree.add_node(all_tuple[1])
    tree.add_node(all_tuple[2])
    tree.add_edge(all_tuple[0],all_tuple[1])
    tree.add_edge(all_tuple[0],all_tuple[2])
    for t in range(3,len(all_tuple)):
        fifo.append(all_tuple[t])
        if len(list(tree.neighbors(fifo[0]))) >= 3:
            trash = fifo.pop(0)
        tree.add_node(all_tuple[t])
        tree.add_edge(fifo[0],all_tuple[t])
    return tree

url = 'https://fr.wikipedia.org/wiki/Lucifer'

json_tree = get_json_tree(url)
put_into_db(url,json_tree)

json_tree_dict = json.loads(json_tree)

tree = to_tree(json_tree_dict)
print(nx.is_tree(tree))

nx.draw(tree)
plt.show()

# if __name__ == '__main__':
#     app.run(debug=True)