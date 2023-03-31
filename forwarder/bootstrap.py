from forwarder.adapters.elasticsearch import ShipperManager
from forwarder.adapters.eventhub import Router


def from_environment() -> Router:
    """Create a router from environment variables."""
    return Router(
        {
            "activitylogs": "logs-azure.activitylogs-esf",
        },
        ShipperManager.from_environment(),
    )
