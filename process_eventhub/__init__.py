from typing import List

import azure.functions as func

from forwarder import bootstrap

router = bootstrap.from_environment()


def main(events: List[func.EventHubEvent], context: func.Context):
    router.dispatch(events, context)
