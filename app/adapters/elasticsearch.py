import dataclasses
import datetime
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from app.models import Event


class Shipper:

    def __init__(self, endpoint: str, api_key: str, es: Elasticsearch = None, index_or_datastream = "logs-azure.eventhub-esf") -> None:
        self.endpoint = endpoint
        self.api_key = api_key
        self.actions = []
        self.index_or_datastream = index_or_datastream
        self.client = es if es else Elasticsearch(endpoint, api_key=self.api_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()

    def info(self):
        """Get information about the Elasticsearch cluster"""
        return self.client.info()

    def send(self, event: Event) -> None:
        """Send an event to Elasticsearch"""
        now = datetime.datetime.now(datetime.timezone.utc)

        event["@timestamp"] = now.isoformat()

        self.actions.append({
            "_index": self.index_or_datastream,
            "_op_type": "create",
            "_source": event,
        })

        if len(self.actions) >= 100:
            self.flush()

    def flush(self):
        """Flush the buffer to Elasticsearch"""
        if len(self.actions) > 0:
            print(bulk(self.client, self.actions))
            self.actions = []

    @classmethod
    def from_environment(self) -> "Shipper":
        """Create a Shipper from environment variables"""
        return Shipper(
            endpoint=os.environ["ELASTICSEARCH_ENDPOINT"],
            api_key=os.environ["ELASTICSEARCH_API_KEY"],
        )
        