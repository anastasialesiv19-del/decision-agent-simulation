from decision_agent_sim.env import manhattan_distance
from decision_agent_sim.state import AgentState, move_agent


def test_manhattan_distance():
    a = (0, 0)
    b = (1, 1)

    assert manhattan_distance(a, b) == 2


def test_is_alive():
    state = AgentState(position=(0, 0), energy=0)

    new_state = move_agent(state, 0, 0)

    assert new_state.is_alive is False
