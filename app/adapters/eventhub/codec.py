import json

from typing import List

from app.models import Event


class AzureLogsCodec:
    """Azure Logs Codec"""

    def encode(self, events: List[Event]) -> bytes:
        """Packs a list of events into an Azure Event Hub message body."""
        return json.dumps({
            "records": [event.message for event in events]
        }).encode("utf-8")

    def decode(self, body: bytes) -> List[str]:
        """Unpacks Azure Event Hub message body into a list of records."""
        _body = json.loads(body)
        return [json.dumps(record) for record in _body["records"]]
