from pathlib import Path
import json
import pytest
from decision_agent_sim.map_loader import load_gridworld_from_json

def test_correct_loader():
    root = Path(__file__).resolve().parents[1]
    simple_path = root / "examples" / "maps" / "simple.json"
    medium_path = root / "examples" / "maps" / "medium.json"

    simple_env = load_gridworld_from_json(simple_path)
    medium_env = load_gridworld_from_json(medium_path)

    assert simple_env.width == 5
    assert simple_env.height == 5
    assert simple_env.start_pos == (0, 0)
    assert simple_env.goal == (4, 4)
    assert (1, 0) in simple_env.obstacles
    assert simple_env.danger.get((3, 3), 0) == 5

    assert medium_env.width == 12
    assert medium_env.height == 12
    assert medium_env.start_pos == (0, 0)
    assert medium_env.goal == (5, 10)
    assert medium_env.danger.get((3, 3), 0) == 3


def make_test_map() -> dict:
    base_map: dict = {
        "width": 5,
        "height": 5,
        "start": [2, 2],
        "goal": [1, 4],
        "obstacles": [],
        "danger": {}
    }
    return base_map

def write_temp_map(tmp_path: Path, tmp_map: dict) -> Path:
    bad_map_path = tmp_path / "tmp_map.json"
    with open(bad_map_path, "w", encoding="utf-8") as f:
        json.dump(tmp_map, f)
    return bad_map_path

def test_zero_width_map(tmp_path):
    map_data = make_test_map()

    map_data["width"] = 0

    json_path = write_temp_map(tmp_path, map_data)

    with pytest.raises(ValueError):
        load_gridworld_from_json(json_path)

def test_loader_fails_when_start_out_of_bounds(tmp_path):
    map_data = make_test_map()

    map_data["start"] = [99,99]

    json_path = write_temp_map(tmp_path, map_data)

    with pytest.raises(ValueError):
        load_gridworld_from_json(json_path)

def test_false_parsing_danger_key(tmp_path):
    map_data = make_test_map()

    map_data["danger"] = {"a,3": 5}

    json_path = write_temp_map(tmp_path, map_data)

    with pytest.raises(ValueError):
        load_gridworld_from_json(json_path)

def test_false_parsing_danger_value(tmp_path):
    map_data = make_test_map()

    map_data["danger"] = {"3,3": "asd"}

    json_path = write_temp_map(tmp_path, map_data)

    with pytest.raises(ValueError):
        load_gridworld_from_json(json_path)


