from enum import Enum
from dataclasses import dataclass
from typing import Optional, Literal

class Direction(Enum):
    NORTH = (0,-1)
    SOUTH = (0,1)
    WEST = (-1,0)
    EAST = (1,0)

@dataclass(frozen=True)
class Action:
    kind: Literal["MOVE","WAIT","RECHARGE"]
    direction: Optional[Direction] = None

def move(direction: Direction) -> Action:
    return Action(kind="MOVE", direction=direction)
def wait() -> Action:
    return Action(kind="WAIT")
def recharge() -> Action:
    return Action(kind="RECHARGE")

