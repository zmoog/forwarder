import dataclasses
import datetime
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from forwarder.models import Event


class ShipperManager:
    """The ShipperManager is a context manager for Shipper"""

    def __init__(self, endpoint: str, api_key: str) -> None:
        self.client = Elasticsearch(endpoint, api_key=api_key)
        self.shipper = None

    def __enter__(self):
        self.shipper = Shipper(
            self.client,
        )
        return self.shipper

    def __exit__(self, exc_type, exc_value, traceback):
        # this is just a POC, so we don't care about errors ¯\_(ツ)_/¯
        self.shipper.flush()

    @classmethod
    def from_environment(self) -> "ShipperManager":
        """Create a Shipper from environment variables"""
        return ShipperManager(
            endpoint=os.environ["ELASTICSEARCH_ENDPOINT"],
            api_key=os.environ["ELASTICSEARCH_API_KEY"],
        )


class Shipper:
    """The Shipper sends events to Elasticsearch"""

    def __init__(
        self,
        es: Elasticsearch,
    ) -> None:
        self.client = es
        self.actions = []

    def info(self):
        """Get information about the Elasticsearch cluster"""
        return self.client.info()

    def send(self, event: Event, index_or_datastream: str = None) -> None:
        """Send an event to Elasticsearch"""
        now = datetime.datetime.now(datetime.timezone.utc)

        event["@timestamp"] = now.isoformat()

        self.actions.append(
            {
                "_op_type": "create",
                "_index": index_or_datastream,
                "_source": event,
            }
        )

        if len(self.actions) >= 100:
            self.flush()

    def flush(self):
        """Flush the buffer to Elasticsearch"""
        if len(self.actions) > 0:
            successfull, failed = bulk(self.client, self.actions)
            # this is just a POC, so we don't care about failed events ¯\_(ツ)_/¯
            print(successfull, failed)
            self.actions = []
