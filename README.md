# Decision Agent Simulator

A small grid-world simulator where an agent makes decisions using utility-based
scoring and constraints. The project focuses on decision logic correctness,
simulation reliability, and evaluation through batch metrics and tests.

## Purpose
The project is designed as a portfolio-quality example demonstrating
decision logic design, simulation reliability, and test-driven development.

## Features
- Actions: move / wait / recharge
- GridWorld with obstacles and danger areas
- Valid action filtering based on constraints
- Utility-based scoring and explainable action selection
- Single-run simulation with structured results (RunResult)
- Batch simulations with aggregated metrics (success rate, averages, failure reasons)
- Demo script for running batch simulations and viewing metrics
- Automated tests using pytest
- JSON map loader + validation


## Project structure
```
src/decision_agent_sim/
  env.py
  state.py
  actions.py
  decision.py
  simulator.py
  metrics.py
  map_loader.py
tests/
  test_env.py
  test_decision.py
  test_simulator.py
  test_loader.py
examples/
  run_demo.py
  maps/
    simple.json
    medium.json
```
- `env.py` and `state.py` define the world and agent state.
- `actions.py` describes available actions and movement directions.
- `decision.py` validates actions, scores them, and selects the optimal one.
- `simulator.py` runs step-by-step simulations of agent behavior.
- `metrics.py` aggregates results from multiple simulation runs.
- The test suite verifies constraints, decision behavior, energy handling,
  and simulation outcomes.

## Installation & run
```
python -m venv .venv
# activate venv
pip install -e ".[dev]"
pytest
python examples/run_demo.py
```

## Example metrics
```
success_rate: 0.76
avg_steps: 6.2
avg_energy_remaining: 37.8
failure_distribution:
   dead: 9
   max_steps: 12
```
## Testing
    
The project includes automated tests ensuring correctness, constraint
handling, and reliability of the decision system.

Covered aspects:
- Action constraints (movement boundaries, obstacles, energy limits)
- Decision preferences (choosing progress over waiting, avoiding danger)
- Energy model correctness (WAIT and RECHARGE behavior)
- Simulation outcomes and failure reasons

Tests are implemented using pytest.

Run all tests:
```
pytest
```
## Design decisions

- `is_alive` is implemented as a property derived from `energy`.
  This avoids inconsistent states such as `energy = 0` while `is_alive = True`
  and simplifies testing.

- Step counting is handled locally inside `run_simulation` rather than stored
  in `AgentState`. This keeps the decision logic independent from execution
  metrics and improves separation of responsibilities.

## Roadmap

- Map visualization
- Command-line interface (CLI) for running simulations
- Separate metrics for successful runs only
- Optional CI integration
- Optional learning-based agent (reinforcement learning baseline)

