from collections.abc import Iterable

from app.content.actions import get_action_cost
from app.engine.models import AIState, Action


def threat_label(threat: int) -> str:
    """Return the authored threat-stage label for a numeric threat value."""

    clamped = max(0, min(100, threat))

    if clamped <= 19:
        return "DISTANT"
    if clamped <= 39:
        return "NEARBY"
    if clamped <= 59:
        return "ATTACHED"
    if clamped <= 79:
        return "BREACHING"
    return "INSIDE"


def format_threat(threat: int) -> str:
    """Format threat as a numeric value plus stage label."""

    return f"{threat} ({threat_label(threat)})"


def format_resource_name(resource: str) -> str:
    """Format an internal resource key for HUD display."""

    return resource.replace("_", " ").upper()


def format_resource_line(resource: str, value: int) -> str:
    """Format one resource line for the HUD."""

    return f"{format_resource_name(resource)}: {value}"


def format_ai_state(ai_state: AIState) -> str:
    """Format the AI state for display or styling hooks."""

    return ai_state.name.upper()


def format_action_name(action: Action) -> str:
    """Format one action enum for player-facing display."""

    return action.name.upper()


def format_action_line(action: Action) -> str:
    """Format one action for the action panel."""

    name = format_action_name(action)
    cost = get_action_cost(action)

    if cost > 0:
        return f"[{name}] cost {cost} battery"
    return f"[{name}]"


def format_action_lines(actions: Iterable[Action] | None = None) -> list[str]:
    """Format multiple actions for display in a menu or panel."""

    action_iterable = actions if actions is not None else Action
    return [format_action_line(action) for action in action_iterable]


def format_turn_line(turn_number: int, total_turns: int) -> str:
    """Format the current turn counter."""

    return f"TURN {turn_number:02d}/{total_turns:02d}"


def format_rescue_eta_line(rescue_eta: int) -> str:
    """Format the rescue ETA line."""

    unit = "TURN" if rescue_eta == 1 else "TURNS"
    return f"RESCUE ETA: {rescue_eta} {unit}"


def format_turn_header(turn_number: int, total_turns: int, rescue_eta: int) -> str:
    """Format a two-line header block."""

    return "\n".join(
        [
            format_turn_line(turn_number, total_turns),
            format_rescue_eta_line(rescue_eta),
        ]
    )
