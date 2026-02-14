from pathlib import Path
import json
from typing import Any

from decision_agent_sim.env import GridWorld

def load_gridworld_from_json(path:str | Path) -> GridWorld:
    with open(path, encoding="utf-8-sig") as json_file:
        data = json.load(json_file)

    width: int = data["width"]
    height: int = data["height"]

    start_pos = _parse_pos(data["start"], field="start")
    goal = _parse_pos(data["goal"], field="goal")

    obstacles_raw =  data.get("obstacles",[])
    obstacles: set[tuple[int,int]] = {_parse_pos(pos,field="obstacles item") for pos in obstacles_raw}

    danger_raw = data.get("danger",{})
    danger: dict[tuple[int,int], int] = {}
    for key, value_str in danger_raw.items():
        x_str, y_str = key.split(",")
        x = int(x_str)
        y = int(y_str)
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"Danger [{x},{y}] out of bounds")

        try:
            value = int(value_str)
        except TypeError:
            raise ValueError("Danger value must be an integer")
        danger[x, y] = value

    if width <= 0 or height <= 0:
        raise ValueError("The width and height values must be greater than zero")

    if not (0 <= start_pos[0] < width and 0 <= start_pos[1] < height):
        raise ValueError("Start position out of bounds")

    if not (0 <= goal[0] < width and 0 <= goal[1] < height):
        raise ValueError("Goal position out of bounds")

    for obstacle in obstacles:
        if not (0 <= obstacle[0] < width and 0 <= obstacle[1] < height):
            raise ValueError(f"Obstacle [{obstacle[0]},{obstacle[1]}] out of bounds")


    return GridWorld(
        width=width,
        height=height,
        start_pos=start_pos,
        goal=goal,
        obstacles=obstacles,
        danger=danger)
def _parse_pos(value: Any, *, field:str) -> tuple[int, int]:
    if not (isinstance(value, list) or isinstance(value, tuple)) or len(value) != 2:
        raise ValueError(f"{field} must be [x, y]")
    x, y = value
    return int(x), int(y)