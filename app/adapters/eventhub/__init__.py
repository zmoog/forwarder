from typing import List

import azure.functions as func

from app.adapters.elasticsearch import Shipper
from app.models import Event
from .codec import AzureLogsCodec


class Router:
    """Routes events from Azure Event Hub to Elasticsearch"""
    
    def __init__(self, shipper: Shipper, codec = AzureLogsCodec()) -> None:
        self.shipper = shipper
        self.codec = codec

    def dispatch(self, events: List[func.EventHubEvent]) -> None:
        with self.shipper as _shipper:
            for event in events:
                # logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))

                # TODO: unpack event and send to shipper
                records = self.codec.decode(event.get_body())

                for record in records:
                    _shipper.send(Event(message=record))
