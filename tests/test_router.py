from unittest import mock

import azure.functions as func
from freezegun import freeze_time

from forwarder.adapters.elasticsearch import ShipperManager
from forwarder.adapters.eventhub import Router


@freeze_time("2023-03-12 09:47:52.039684+00:00")
def test_router():
    # metadata = {
    #     "SequenceNumberArray": [
    #         59
    #     ],
    #     "PartitionContext": {
    #         "FullyQualifiedNamespace": "whatever.servicebus.windows.net",
    #         "EventHubName": "azurelogs",
    #         "ConsumerGroup": "$Default",
    #         "PartitionId": "2"
    #     },
    #     "PropertiesArray": [
    #         {}
    #     ],
    #     "OffsetArray": [
    #         "616008"
    #     ],
    #     "PartitionKeyArray": [],
    #     "SystemPropertiesArray": [
    #         {
    #             "x-opt-sequence-number": 59,
    #             "x-opt-offset": 616008,
    #             "x-opt-enqueued-time": "2023-03-13T01: 25: 02.25+00: 00",
    #             "SequenceNumber": 59,
    #             "Offset": 616008,
    #             "PartitionKey": None,
    #             "EnqueuedTimeUtc": "2023-03-13T01: 25: 02.25"
    #         }
    #     ],
    #     "EnqueuedTimeUtcArray": [
    #         "2023-03-13T01: 25: 02.25"
    #     ]
    # }

    # The patching of the `elasticsearch.helpers.bulk` method is not working,
    # and I don't get why.
    #
    # However, I found a working solution on stackoverflow:
    # https://stackoverflow.com/questions/63602105/how-to-mock-elasticsearch-helpers-bulk
    with mock.patch(
        "elasticsearch.Elasticsearch.bulk", mock.MagicMock()
    ) as bulk:
        router = Router({}, ShipperManager("http://whatever:9200", "whatever"))

        events = [
            func.EventHubEvent(
                body=b'{"records": [{"foo": "bar"}, {"foo": "baz"}]}',
                # trigger_metadata=metadata,
            )
        ]
        context = mock.MagicMock()

        router.dispatch(events, context)

        bulk.assert_called_once_with(
            operations=[
                b'{"create":{"_index":"logs-generic-default"}}',
                b'{"event":{"kind":"event"},"cloud":{"provider":"azure"},"agent":{"name":"forwarder","type":"azure-function"},"message":"{\\"foo\\": \\"bar\\"}","azure-eventhub":{},"tags":["preserve_original_event","parse_message"],"@timestamp":"2023-03-12T09:47:52.039684+00:00"}',
                b'{"create":{"_index":"logs-generic-default"}}',
                b'{"event":{"kind":"event"},"cloud":{"provider":"azure"},"agent":{"name":"forwarder","type":"azure-function"},"message":"{\\"foo\\": \\"baz\\"}","azure-eventhub":{},"tags":["preserve_original_event","parse_message"],"@timestamp":"2023-03-12T09:47:52.039684+00:00"}',
            ],
        )
