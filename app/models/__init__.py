from typing import Any, Dict
# from typing import Optional
# from dataclasses import dataclass


# @dataclass
# class Agent:
#     name: str
#     type: str
#     id: Optional[str] = None
#     version: Optional[str] = None


# @dataclass
# class EventHub:
#     event_hub: str
#     consumer_group: str
#     partition_id: str
#     # sequence_number: int
#     # offset: int
#     # enqueued_time: str


# @dataclass
# class Event:
#     agent: Agent
#     message: Optional[str] = None
#     event_hub: Optional[EventHub] = None
    
Event = Dict[str, Any]