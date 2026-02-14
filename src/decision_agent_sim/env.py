from dataclasses import dataclass, field


@dataclass
class GridWorld:
    width: int
    height: int
    start_pos: tuple[int, int]
    goal: tuple[int, int]
    obstacles: set[tuple[int, int]]
    danger: dict[tuple[int, int], int] = field(default_factory=dict)

def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])
