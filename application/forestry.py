from networkx import Graph

def dict_word_occurence_to_tree(dict_tree):
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