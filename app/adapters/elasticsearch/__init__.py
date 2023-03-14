import dataclasses
import datetime
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from app.models import Event


DEFAULT_INDEX_OR_DATASTREAM = "logs-azure.eventhub-esf"


class ShipperManager:
    """The ShipperManager is a context manager for Shipper"""

    def __init__(self, endpoint: str, api_key: str, es: Elasticsearch = None, index_or_datastream = DEFAULT_INDEX_OR_DATASTREAM) -> None:
        self.client = es if es else Elasticsearch(endpoint, api_key=api_key)
        self.index_or_datastream = index_or_datastream
        self.shipper = None

    def __enter__(self):
        self.shipper = Shipper(
            self.client,
            self.index_or_datastream,
        )
        return self.shipper

    def __exit__(self, exc_type, exc_value, traceback):
        self.shipper.flush()

    @classmethod
    def from_environment(self) -> "ShipperManager":
        """Create a Shipper from environment variables"""
        return ShipperManager(
            endpoint=os.environ["ELASTICSEARCH_ENDPOINT"],
            api_key=os.environ["ELASTICSEARCH_API_KEY"],
            index_or_datastream=os.environ["ELASTICSEARCH_INDEX_OR_DATASTREAM", DEFAULT_INDEX_OR_DATASTREAM],
        )


class Shipper:
    """The Shipper sends events to Elasticsearch"""

    def __init__(self, es: Elasticsearch, index_or_datastream = "logs-azure.eventhub-esf") -> None:
        self.client = es
        self.actions = []
        self.index_or_datastream = index_or_datastream

    def info(self):
        """Get information about the Elasticsearch cluster"""
        return self.client.info()

    def send(self, event: Event, index_or_datastream: str = None) -> None:
        """Send an event to Elasticsearch"""
        now = datetime.datetime.now(datetime.timezone.utc)

        event["@timestamp"] = now.isoformat()

        self.actions.append({
            "_index": index_or_datastream if index_or_datastream else self.index_or_datastream,
            "_op_type": "create",
            "_source": event,
        })

        if len(self.actions) >= 100:
            self.flush()

    def flush(self):
        """Flush the buffer to Elasticsearch"""
        if len(self.actions) > 0:
            successfull, failed = bulk(self.client, self.actions)
            print(successfull, failed)
            self.actions = []
