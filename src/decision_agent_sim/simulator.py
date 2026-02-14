from dataclasses import dataclass, replace

from decision_agent_sim.actions import Action
from decision_agent_sim.decision import choose_action
from decision_agent_sim.env import GridWorld
from decision_agent_sim.state import AgentState, move_agent


@dataclass
class RunResult:
    success: bool
    steps_taken: int
    energy_remaining: int
    failure_reason: str | None


def run_simulation(env: GridWorld, initial_state: AgentState, max_steps: int = 100) -> RunResult:
    state = initial_state
    steps = 0
    while state.is_alive and steps < max_steps and state.position != env.goal:
        chosen_action, _ = choose_action(state, env)
        state = apply_action(state, chosen_action)
        steps += 1

    if state.position == env.goal:
        return RunResult(success=True, steps_taken=steps, energy_remaining=state.energy, failure_reason=None)
    elif not state.is_alive:
        return RunResult(success=False, steps_taken=steps, energy_remaining=state.energy, failure_reason="dead")
    elif steps >= max_steps:
        return RunResult(success=False, steps_taken=steps, energy_remaining=state.energy, failure_reason="max_steps")
    raise RuntimeError("Simulation ended without success, death, or max_steps condition.")

def apply_action(state: AgentState, action: Action) -> AgentState:
    match action.kind:
        case "WAIT":
            return replace(state, energy=state.energy - 1)
        case "RECHARGE":
            return replace(state, energy=min(100, state.energy + 20))
        case "MOVE":
            if action.direction is None:
                raise ValueError("Move action must have a direction.")
            dx, dy = action.direction.value
            return move_agent(state, dx, dy)
        case _:
            raise ValueError(f"Unknown action kind: {action.kind!r}")
