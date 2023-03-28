import json
import logging
from typing import List


class AzureLogsCodec:
    """Azure Logs Codec"""

    def encode(self, events: List[str]) -> bytes:
        raise NotImplementedError

    def decode(self, body: bytes) -> List[str]:
        """Unpacks Azure Event Hub message body into a list of records."""
        logging.info("Decoding Azure Event Hub message body: %s", body)
        try:
            _body = json.loads(body)
            return [json.dumps(record) for record in _body["records"]]
        except (KeyError, json.JSONDecodeError) as e:
            # fallback to decoding the body as a single string record
            logging.error("Error decoding Azure Event Hub message body: %r", e)
            return [body.decode("utf-8")]
