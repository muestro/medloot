import medievia.item
from google.appengine.api import search

_main_index = "item_search_1"


def update_indexes():
        print "Attempting to update search index..."
        index = search.Index(name=_main_index)

        items = medievia.item.get_items()
        count = 0
        for item in items:
            fields = [
                search.TextField(name="name", value=item.name),
                search.TextField(name="keyword", value=" ".join(item.keywords))
            ]

            print "Indexing item: {0} : {1} : {2}".format(item.key().id_or_name(), item.name, " ".join(item.keywords))
            doc = search.Document(doc_id=str(item.key()), fields=fields)

            try:
                index.put(doc)
                count += 1
            except search.Error:
                print "Error adding index."
        print "Finished adding to index. Total documents: {0}".format(count)

def run_search(query):
    print "Attempting search: {0}".format(query)
    index = search.Index(name=_main_index)
    results = index.search(query)

    items = []
    for result in results:
        # convert search indexed documents into model objects
        item = medievia.item.get_item(result.doc_id)
        items.append(item)

    print "Found {0} result(s).".format(results.number_found)
    return items