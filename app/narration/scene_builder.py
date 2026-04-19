from dataclasses import dataclass, field

from app.engine.models import TurnCard
from app.engine.state import GameState


def _string_list_factory() -> list[str]:
    return []


@dataclass(slots=True)
class ScenePacket:
    turn: int
    ai_line_seed: str
    required_scene_facts: list[str] = field(
        default_factory=_string_list_factory)
    misleading_facts: list[str] = field(default_factory=_string_list_factory)
    carryover_condition_facts: list[str] = field(
        default_factory=_string_list_factory)
    query_available: bool = True
    forbidden_claims: list[str] = field(default_factory=_string_list_factory)


def build_scene_packet(state: GameState, turn_card: TurnCard) -> ScenePacket:
    carryover: list[str] = []

    if state.conditions.leak_stage > 0:
        carryover.append("Structural stress remains active.")
    if state.conditions.power_bleed_stage > 0:
        carryover.append("Life-support load remains unstable.")
    if state.conditions.pursuit_stage > 0:
        carryover.append("External contact is still pacing the vessel.")
    if state.conditions.contamination_active:
        carryover.append("One implication in the room may be misleading.")

    return ScenePacket(
        turn=turn_card.turn,
        ai_line_seed=turn_card.ai_line,
        required_scene_facts=list(turn_card.required_scene_facts),
        misleading_facts=list(turn_card.misleading_facts),
        carryover_condition_facts=carryover,
        query_available=not state.query.used_this_turn,
        forbidden_claims=list(turn_card.forbidden_claims),
    )
