from __future__ import annotations

from app.content.actions import (
    apply_action_cost,
    can_afford_action,
    format_resource_delta_line,
    get_action_spec,
    get_partial_effect,
)
from app.engine.models import (
    Action,
    OutcomeTier,
    PartialOutcome,
    ResolutionResult,
    TurnCard,
)
from app.engine.state import GameState


GENERIC_WRONG_AFTERMATH: dict[Action, list[str]] = {
    Action.SCAN: ["The return clarifies nothing you can use."],
    Action.REPAIR: ["The correction holds locally, and nowhere else."],
    Action.SILENT: ["You cut noise. Something keeps pace anyway."],
    Action.REROUTE: ["Load shifts. The real failure stays with you."],
}


GENERIC_PARTIAL_AFTERMATH: dict[Action, list[str]] = {
    Action.SCAN: ["The signal narrows, but certainty does not."],
    Action.REPAIR: ["The plating holds for the moment."],
    Action.SILENT: ["The contact falls back, but not far enough."],
    Action.REROUTE: ["The load steadies, but does not stay that way."],
}


def resolve_action(state: GameState, turn_card: TurnCard, action: Action) -> ResolutionResult:
    """Resolve one authored player action against the current turn.

    The resolver mutates `state.resources` immediately and performs direct
    condition clears that are intrinsic to the action itself, such as clearing an
    active leak with a strong REPAIR.
    """

    if state.game_over:
        raise ValueError("Cannot resolve an action after the game is over.")

    if not can_afford_action(state.resources, action):
        raise ValueError(f"Insufficient battery for {action.name}.")

    state.last_scan_result_type = None

    result = ResolutionResult(outcome=OutcomeTier.WRONG)
    cost_paid = apply_action_cost(state.resources, action)
    if cost_paid:
        result.log_lines.append(format_resource_delta_line("battery", -cost_paid))

    if action == turn_card.strong_action:
        result.outcome = OutcomeTier.STRONG
        _apply_strong_resolution(state, turn_card, action, result)
    elif action in turn_card.partial_outcomes:
        result.outcome = OutcomeTier.PARTIAL
        _apply_partial_resolution(state, turn_card, action, result)
    else:
        _apply_wrong_resolution(state, turn_card, action, result)

    state.clamp_resources()
    return result


def _apply_strong_resolution(
    state: GameState,
    turn_card: TurnCard,
    action: Action,
    result: ResolutionResult,
) -> None:
    spec = get_action_spec(action)

    if spec.full_effect_resource is not None and spec.full_effect_amount:
        _apply_resource_delta(state, spec.full_effect_resource, spec.full_effect_amount)

    if action is Action.REPAIR and state.conditions.leak_stage > 0:
        state.conditions.leak_stage = 0
    elif action is Action.REROUTE and state.conditions.power_bleed_stage > 0:
        state.conditions.power_bleed_stage = 0
    elif action is Action.SILENT and state.conditions.pursuit_stage > 0:
        refunded_drain = _pursuit_drain_for_stage(state.conditions.pursuit_stage)
        _apply_resource_delta(state, "threat", -refunded_drain)
        result.suppress_pursuit_drain = True
    elif action is Action.SCAN and state.conditions.contamination_active:
        result.clear_contamination = True

    result.acute_penalty_canceled = True

    if action is Action.SCAN and turn_card.scan_result:
        state.last_scan_result_type = "useful"
        result.log_lines.append(turn_card.scan_result)

    aftermath = turn_card.strong_aftermath.get(action)
    if aftermath:
        result.log_lines.extend(aftermath)


def _apply_partial_resolution(
    state: GameState,
    turn_card: TurnCard,
    action: Action,
    result: ResolutionResult,
) -> None:
    authored = turn_card.partial_outcomes[action]

    if authored.resource_deltas:
        _apply_resource_deltas(state, authored)
    else:
        resource, amount = get_partial_effect(action)
        if resource is not None and amount:
            _apply_resource_delta(state, resource, amount)

    if authored.clear_contamination and state.conditions.contamination_active:
        result.clear_contamination = True

    if authored.suppress_pursuit_drain and state.conditions.pursuit_stage > 0:
        refunded_drain = _pursuit_drain_for_stage(state.conditions.pursuit_stage)
        _apply_resource_delta(state, "threat", -refunded_drain)
        result.suppress_pursuit_drain = True

    if action is Action.SCAN:
        state.last_scan_result_type = "partial"

    aftermath = authored.aftermath_lines or GENERIC_PARTIAL_AFTERMATH[action]
    result.log_lines.extend(aftermath)


def _apply_wrong_resolution(
    state: GameState,
    turn_card: TurnCard,
    action: Action,
    result: ResolutionResult,
) -> None:
    if action is Action.SCAN and turn_card.scan_result:
        state.last_scan_result_type = "corrupted"
        result.log_lines.append(turn_card.scan_result)

    aftermath = turn_card.wrong_aftermath.get(action, GENERIC_WRONG_AFTERMATH[action])
    result.log_lines.extend(aftermath)


def _apply_resource_deltas(state: GameState, outcome: PartialOutcome) -> None:
    for resource, amount in outcome.resource_deltas.items():
        _apply_resource_delta(state, resource, amount)


def _apply_resource_delta(state: GameState, resource: str, amount: int) -> None:
    if resource == "oxygen":
        state.resources.oxygen += amount
        return
    if resource == "battery":
        state.resources.battery += amount
        return
    if resource == "hull":
        state.resources.hull += amount
        return
    if resource == "threat":
        state.resources.threat += amount
        return
    raise ValueError(f"Unknown resource: {resource}")


def _pursuit_drain_for_stage(stage: int) -> int:
    if stage >= 2:
        return 8
    if stage == 1:
        return 5
    return 0
