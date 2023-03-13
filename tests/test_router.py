import azure.functions as func
from unittest import mock

from freezegun import freeze_time

from app.adapters.eventhub import Router
from app.adapters.elasticsearch import Shipper


@freeze_time("2023-03-12 09:47:52.039684+00:00")
def test_router():
    # The patching of the `elasticsearch.helpers.bulk` method is not working,
    # and I don't get why. 
    # 
    # However, I found a working solution on stackoverflow:
    # https://stackoverflow.com/questions/63602105/how-to-mock-elasticsearch-helpers-bulk
    with mock.patch("elasticsearch.Elasticsearch.bulk", mock.MagicMock()) as bulk:

        router = Router(
            Shipper("http://whatever:9200", "whatever")
        )

        events = [func.EventHubEvent(body=b'{"records": [{"foo": "bar"}, {"foo": "baz"}]}')]

        router.dispatch(events)

        bulk.assert_called_once_with(
            operations=[
                b'{"create":{"_index":"zmoog-esf-logs"}}',
                b'{"@timestamp":"2023-03-12T09:47:52.039684+00:00","message":"{\\"foo\\": \\"bar\\"}"}',
                b'{"create":{"_index":"zmoog-esf-logs"}}',
                b'{"@timestamp":"2023-03-12T09:47:52.039684+00:00","message":"{\\"foo\\": \\"baz\\"}"}'
            ]
        )
