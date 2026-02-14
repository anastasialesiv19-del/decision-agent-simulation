from decision_agent_sim.actions import Action
from decision_agent_sim.env import GridWorld
from decision_agent_sim.simulator import run_simulation, apply_action
from decision_agent_sim.state import AgentState
from decision_agent_sim.metrics import run_batch


def test_simulation_reaches_goal_on_simple_map():
    env = GridWorld(width=3, height=3, start_pos=(0, 0), goal=(2, 2), obstacles=set())
    state = AgentState(position=(0, 0), energy=50)

    result = run_simulation(env, state)

    assert result.success
    assert result.failure_reason is None
    assert result.steps_taken > 0
    assert result.energy_remaining >= 0

def test_batch_metrics_have_expected_keys():
    envs: list[GridWorld] = [
        GridWorld(width=3, height=3, start_pos=(0, 0), goal=(2, 2), obstacles=set()),
        GridWorld(width=5, height=4, start_pos=(0, 0), goal=(1, 2), obstacles={(1,1)}),
        GridWorld(width=5, height=6, start_pos=(1, 2), goal=(3, 5), obstacles=set(), danger={(1,3): 100}),
    ]
    metrics = run_batch(envs)

    assert "success_rate" in metrics
    assert "avg_steps" in metrics
    assert "avg_energy_remaining" in metrics
    assert "failure_distribution" in metrics
    assert isinstance(metrics["failure_distribution"], dict)

def test_waiting_uses_energy():
    state = AgentState(position=(0, 0), energy=50)
    action = Action(kind="WAIT")
    new_state = apply_action(state,  action)

    assert new_state.energy == state.energy - 1

def test_energy_increase_of_only_20():
    state = AgentState(position=(0, 0), energy=10)
    action = Action(kind="RECHARGE")
    new_state = apply_action(state, action)

    assert (new_state.energy - state.energy) == 20

def test_recharge_caps_at_100():
    state = AgentState(position=(0, 0), energy=95)
    new_state = apply_action(state, Action(kind="RECHARGE"))
    assert new_state.energy == 100

