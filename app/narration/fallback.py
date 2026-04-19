from app.engine.models import Action, InputKind, ResolutionResult, TurnCard
from app.engine.state import GameState

QUESTION_PREFIXES = (
    "what", "where", "why", "how", "who",
    "is", "are", "do", "does", "did", "can",
    "should", "could", "would", "will"
)

DIAGNOSTIC_CUES = (
    "actually", "really", "origin", "source", "real", "diagnosis", "failing", "causing"
)


def render_scene(turn_card: TurnCard) -> str:
    if turn_card.fallback_scene_lines:
        return "\n".join(turn_card.fallback_scene_lines)

    lines: list[str] = []
    lines.extend(turn_card.readouts[:2])
    if turn_card.ai_line:
        lines.append(f"AI: {turn_card.ai_line}")
    return "\n".join(lines)


def answer_query(state: GameState, turn_card: TurnCard, text: str) -> str:
    if state.query.used_this_turn:
        return "You have already spent your one query for this turn."

    lowered = text.strip().lower()
    facts = turn_card.query_answer_facts or turn_card.readouts

    if any(cue in lowered for cue in DIAGNOSTIC_CUES):
        response = "You get no clean certainty from the noise around you."
    else:
        response = " ".join(
            facts[:2]) if facts else "The sub answers only with the same unstable signs."

    state.query.used_this_turn = True
    state.query.last_query = text
    state.query.last_query_response = response
    state.narration.last_input_kind = InputKind.QUERY
    state.narration.fallback_used = True
    return response


def narrate_aftermath(turn_card: TurnCard, action: Action, result: ResolutionResult) -> str:
    authored = turn_card.fallback_aftermath_lines.get(action)
    if authored:
        return " ".join(authored)

    return " ".join(result.log_lines)


def looks_like_query(text: str) -> bool:
    stripped = text.strip().lower()
    if not stripped:
        return False
    if stripped.endswith("?"):
        return True
    return any(stripped.startswith(prefix + " ") for prefix in QUESTION_PREFIXES)
