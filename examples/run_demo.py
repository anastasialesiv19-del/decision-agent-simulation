from decision_agent_sim.map_loader import load_gridworld_from_json
from decision_agent_sim.metrics import run_batch
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    simple_path = root / "examples" / "maps" / "simple.json"
    medium_path = root / "examples" / "maps" / "medium.json"

    simple_env = load_gridworld_from_json(simple_path)
    medium_env = load_gridworld_from_json(medium_path)

    results = run_batch([simple_env, medium_env], 20)

    print(results)

if __name__ == "__main__":
        main()