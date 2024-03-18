from time import time

from invenio_search import current_search_client
from invenio_search.utils import prefix_index


class Persistency:
    def __init__(self):
        self._search_client = current_search_client
        self._index = prefix_index("fts_persistency")

    def insert_transfer(self, id):
        now = time()
        self._search_client.index(
            index=self._index, id=id, body={"submitted": now}, refresh=True
        )

    def ack_transfer(self, id):
        now = time()
        self._search_client.update(
            self._index, id, body={"doc": {"ack": now}}, refresh=True
        )

    def get_transfers(self):
        ids = []
        result = self._search_client.search(
            index=self._index,
            _source=False,
            body={"query": {"bool": {"must_not": [{"exists": {"field": "ack"}}]}}},
        )
        for doc in result["hits"]["hits"]:
            ids.append(doc["_id"])
        return ids
