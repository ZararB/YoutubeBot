# some helper functions that the spiders use to parse html/get the values from nested dictionaries/lists
# TODO N rename class
def search_dict(partial, key):
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        for i in partial:
            for o in search_dict(i, key):
                yield o


def find_value(html, key, separator='"'):
    pos_begin = html.find(key) + len(key)
    pos_end = html.find(separator, pos_begin)
    return html[pos_begin: pos_end]

