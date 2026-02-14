from dataclasses import dataclass, replace


@dataclass(frozen=True)
class AgentState:
    position: tuple[int, int]
    energy: int

    @property
    def is_alive(self) -> bool:
        return self.energy > 0


def move_agent(state: AgentState, dx: int, dy: int) -> AgentState:
    if not state.is_alive:
        return state
    return replace(
        state,
        position=(state.position[0] + dx, state.position[1] + dy),
        energy=state.energy - 1
    )
