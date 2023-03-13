from typing import List

import azure.functions as func

from app.adapters.eventhub import Router
from app.adapters.elasticsearch import Shipper


router = Router(Shipper.from_environment())


def main(events: List[func.EventHubEvent], context: func.Context):
     router.dispatch(events, context)
