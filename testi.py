from application.scrapper import get_json_tree, put_into_db

url = 'https://fr.wikipedia.org/wiki/Lucifer'

json_tree = get_json_tree(url)

print(json_tree)

put_into_db(url,json_tree)