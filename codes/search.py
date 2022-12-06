from bplustree import BPlusTree
import pandas as pd

def Search(aim, index=None, value=None, tree=None):
    """
    aim: aim of search
    index: index of our data table, default: range(len(value))
    value: value list
    tree: build a b+tree first and use it to accelerate, if we need freq search
    return: a list of index, empty if not found
    """
    if aim.isdigit():
        aim = int(aim)
    if type(aim) is str and ('-' in aim or '/' in aim):
        aim = pd.Timestamp(aim).strftime('%Y-%m-%d %H:%M:%S')
    if tree:
        return tree.retrieve(aim)
    elif value is not None:
        res = []
        if index is None:
            index = list(range(len(value)))
        for i in range(len(value)):
            if value[i] == aim:
                res.append(index[i])
    else:
        raise "value and B empty"
    return res



def Search_from_to(tree, _from, _to):
    """
	tree: b+tree
	from: start time
	to: end time
	"""
    if ':' in _from:
        _from = pd.Timestamp(_from).strftime('%Y-%m-%d %H:%M:%S')
        _to = pd.Timestamp(_to).strftime('%Y-%m-%d %H:%M:%S')
        if _from > _to:
            return []
        res = []
        timelist = pd.date_range(_from, _to, freq='S').to_list()
        for time in timelist:
            tmp = Search(aim=str(time), tree=tree)
            if tmp:
                res += tmp
    else:
        res = tree.search_range(float(_from), float(_to), tree.root)
    return res