from typing import Any, Dict, List

import azure.functions as func

from forwarder.adapters.elasticsearch import ShipperManager
from forwarder.settings import DEFAULT_INDEX_OR_DATASTREAM

from .codec import AzureLogsCodec


class Router:
    """Routes events from Azure Event Hub to Elasticsearch"""

    def __init__(
        self,
        routes: Dict[str, str],
        shipper_manager: ShipperManager,
        codec=AzureLogsCodec(),
    ) -> None:
        self.routes = routes
        self.shipper_manager = shipper_manager
        self.codec = codec

    def dispatch(
        self, events: List[func.EventHubEvent], context: func.Context
    ) -> None:
        """Dispatches events to the appropriate shipper"""
        with self.shipper_manager as _shipper:
            for event in events:
                # logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
                # print("metadata", event.__trigger_metadata)
                eventhub_details = _extract_eventhub_details(event)
                eventhub_name = eventhub_details.get("eventhub", "unknown")

                # find the index or datastream to send to based on the eventhub name
                index_or_datastream = self.routes.get(
                    eventhub_name, DEFAULT_INDEX_OR_DATASTREAM
                )

                # TODO: unpack event and send to shipper
                records = self.codec.decode(event.get_body())

                for record in records:
                    _shipper.send(
                        {
                            "event": {
                                "kind": "event",
                            },
                            "cloud": {
                                "provider": "azure",
                            },
                            "agent": {
                                "name": "forwarder",
                                "type": "azure-function",
                            },
                            "message": record,
                            "azure-eventhub": eventhub_details,
                            "tags": [
                                "preserve_original_event",
                                "parse_message",
                            ],
                        },
                        index_or_datastream,
                    )


def _extract_eventhub_details(event: func.EventHubEvent) -> Dict[str, Any]:
    """Extracts event hub details from an event"""
    if not event.metadata:
        return {}

    partition_context = event.metadata.get("PartitionContext", {})

    return {
        "eventhub": partition_context.get("EventHubName", "unknown"),
        "consumer_group": partition_context.get("ConsumerGroup", "unknown"),
        "enqueued_time": event.metadata["EnqueuedTimeUtcArray"][0],
        "sequence_number": event.metadata["SequenceNumberArray"][0],
        "offset": int(event.metadata["OffsetArray"][0]),
    }
