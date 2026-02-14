from decision_agent_sim.actions import Action, Direction, wait, recharge, move
from decision_agent_sim.env import GridWorld, manhattan_distance
from decision_agent_sim.state import AgentState


def get_valid_actions(state: AgentState, env: GridWorld) -> list[Action]:
    if not state.is_alive:
        return []

    actions: list[Action] = [wait()]

    if state.energy < 100:
        actions.append(recharge())

    x, y = state.position

    for direction in Direction:
        dx, dy = direction.value
        new_x = x + dx
        new_y = y + dy
        new_pos = (new_x, new_y)
        if 0 <= new_x < env.width and 0 <= new_y < env.height and new_pos not in env.obstacles:
            actions.append(move(direction))

    return actions


def score_action(state: AgentState, env: GridWorld, action: Action) -> float:
    match action.kind:
        case "WAIT":
            return -1
        case "RECHARGE":
            return 10 if state.energy < 20 else -5
        case "MOVE":
            direction = action.direction
            if direction is None:
                raise ValueError("Move action must have a direction.")
            new_position = (state.position[0] + direction.value[0], state.position[1] + direction.value[1])
            old_distance = manhattan_distance(state.position, env.goal)
            new_distance = manhattan_distance(new_position, env.goal)
            return (5 if new_distance < old_distance else -3) - (env.danger.get(new_position, 0))
        case _:
            raise ValueError(f"Unknown action kind: {action.kind!r}")


def choose_action(state: AgentState, env: GridWorld) -> tuple[Action, dict]:
    valid_actions = get_valid_actions(state, env)
    if valid_actions == []:
        raise ValueError("No valid actions found.")

    alternatives = []
    best_action = valid_actions[0]
    best_score = score_action(state, env, valid_actions[0])
    for action in valid_actions:
        score = score_action(state, env, action)
        alternatives.append((action, score))
        if score > best_score:
            best_score = score
            best_action = action
    explanation = {
         "chosen_action": best_action,
         "chosen_score": best_score,
         "alternatives": alternatives
    }
    return best_action, explanation













