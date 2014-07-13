import medievia.item.item_summary
from google.appengine.api import search

_main_index = "item_search_1"


def update_indexes():
    print "\nAttempting to delete search index..."
    _delete_all_in_index(_main_index)
    print "Delete index successful.\n"

    print "Attempting to update search index...\n"
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


def _delete_all_in_index(index_name):
    """Delete all the docs in the given index."""
    doc_index = search.Index(name=index_name)

    # looping because get_range by default returns up to 100 documents at a time
    while True:
        # Get a list of documents populating only the doc_id field and extract the ids.
        document_ids = [document.doc_id
                        for document in doc_index.get_range(ids_only=True)]
        if not document_ids:
            break
        # Delete the documents for the given ids from the Index.
        doc_index.delete(document_ids)


def run_search(query_string):
    print "Attempting search: {0}".format(query_string)
    index = search.Index(name=_main_index)

    query = search.Query(query_string, options=search.QueryOptions(limit=1000))

    results = index.search(query)

    items = []
    for result in results:
        # convert search indexed documents into model objects
        item = medievia.item.get_item(result.doc_id)
        items.append(item)

    print "Found {0} result(s).".format(results.number_found)
    return items


def index_count():
    index = search.Index(name=_main_index)
    query = search.Query(" ", options=search.QueryOptions(limit=1000, returned_fields="name",
                                                          number_found_accuracy=1000))
    return index.search(query).number_found


def run_new_search(query_string):
    return medievia.item.item_summary.ItemSummary.query(
        medievia.item.item_summary.ItemSummary.search_terms.IN(query_string.split())).fetch(100)


def browse_all():
    return medievia.item.item_summary.ItemSummary.query().fetch(1000)