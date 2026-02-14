from decision_agent_sim.env import GridWorld
from decision_agent_sim.simulator import run_simulation
from decision_agent_sim.state import AgentState


DEFAULT_ENERGY = 50

def run_batch(envs: list[GridWorld], runs_per_env: int = 10) -> dict:
    total_runs: int = 0
    success_count: int = 0
    sum_steps: int = 0
    sum_energy: int = 0
    failure_distribution: dict[str, int] = {}

    if not envs or runs_per_env <= 0:
        raise ValueError("No environments or number of runs found.")

    for env in envs:
        for _ in range(runs_per_env):
            initial_state = AgentState(position=env.start_pos, energy=DEFAULT_ENERGY)
            result = run_simulation(env, initial_state)
            sum_steps += result.steps_taken
            sum_energy += result.energy_remaining
            if result.success:
                success_count += 1
            else:
                if result.failure_reason is None:
                    raise RuntimeError("run_simulation returned success=False but failure_reason=None")
                failure_distribution[result.failure_reason]  = failure_distribution.get(result.failure_reason, 0) + 1
            total_runs += 1

    success_rate = success_count / total_runs
    avg_steps = sum_steps / total_runs
    avg_energy_remaining = sum_energy / total_runs

    return {
        "success_rate": success_rate,
        "avg_steps": avg_steps,
        "avg_energy_remaining": avg_energy_remaining,
        "failure_distribution": failure_distribution
    }



