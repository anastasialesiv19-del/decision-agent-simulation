from decision_agent_sim.actions import Direction, recharge, move
from decision_agent_sim.decision import get_valid_actions, choose_action
from decision_agent_sim.env import GridWorld
from decision_agent_sim.state import AgentState

def test_move_into_obstacle_is_not_valid():
    env = GridWorld(width=3, height=3, start_pos=(0,0), goal =(2,2), obstacles={(1, 0)})
    state = AgentState(position=(0, 0), energy=50)

    decision = get_valid_actions(state, env)

    assert move(Direction.EAST) not in decision


def test_move_out_of_bounds_is_not_valid():
    env = GridWorld(width=3, height=3, start_pos=(0,0), goal =(2,2), obstacles=set())
    state = AgentState(position=(0, 0), energy=50)

    decision = get_valid_actions(state, env)

    assert move(Direction.WEST) not in decision
    assert move(Direction.NORTH) not in decision


def test_recharge_not_allowed_at_full_energy():
    env = GridWorld(width=3, height=3, start_pos=(0,0), goal =(2,2), obstacles=set())
    state = AgentState(position=(0, 0), energy=100)

    decision = get_valid_actions(state, env)

    assert recharge() not in decision


def test_dead_agent_has_no_actions():
    env = GridWorld(width=3, height=3, start_pos=(0,0), goal =(2,2), obstacles=set())
    state = AgentState(position=(0, 0), energy=0)

    decision = get_valid_actions(state, env)

    assert decision == []


def test_choose_action_prefers_move_towards_goal():
    env = GridWorld(width=3, height=3, start_pos=(0, 0), goal=(2, 0), obstacles=set())
    state = AgentState(position=(0, 0), energy=50)
    chosen_action, explanation = choose_action(state, env)

    assert chosen_action.kind == "MOVE"
    assert chosen_action.direction == Direction.EAST


def test_choose_action_prefers_recharge_when_energy_low():
    env = GridWorld(width=3, height=3, start_pos=(0, 0), goal=(2, 2), obstacles=set())
    state = AgentState(position=(0, 0), energy=10)
    chosen_action, explanation = choose_action(state, env)

    assert chosen_action.kind == "RECHARGE"


def test_choose_action_avoids_danger_when_possible():
    env = GridWorld(width=3, height=3, start_pos=(0, 0), goal=(1, 1), obstacles=set(), danger={(1,0): 100})
    state = AgentState(position=(0, 0), energy=50)
    chosen_action, explanation = choose_action(state, env)

    assert chosen_action.kind == "MOVE"
    assert chosen_action.direction != Direction.EAST















