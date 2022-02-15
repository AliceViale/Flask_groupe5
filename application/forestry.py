from networkx import Graph
from scrapper import get_json_tree

url = 'https://fr.wikipedia.org/wiki/Lucifer'
json_tree_dict = dict(get_json_tree(url))
tree = Graph(json_tree_dict)