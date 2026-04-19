from typing import Mapping

from app.engine.state import GameState


LEAK_STAGE_1_DRAIN = -3
LEAK_STAGE_2_DRAIN = -5

POWER_BLEED_STAGE_1_DRAIN = -3
POWER_BLEED_STAGE_2_DRAIN = -5

PURSUIT_STAGE_1_DRAIN = 5
PURSUIT_STAGE_2_DRAIN = 8


def apply_resource_delta(state: GameState, resource: str, amount: int) -> None:
    """Apply a delta to one authored resource on the mutable game state."""

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


def apply_resource_deltas(state: GameState, deltas: Mapping[str, int]) -> None:
    """Apply multiple authored resource deltas."""

    for resource, amount in deltas.items():
        apply_resource_delta(state, resource, amount)


def leak_drain_for_stage(stage: int) -> int:
    """Return the authored hull drain for the current leak stage."""

    if stage >= 2:
        return LEAK_STAGE_2_DRAIN
    if stage == 1:
        return LEAK_STAGE_1_DRAIN
    return 0


def power_bleed_drain_for_stage(stage: int) -> int:
    """Return the authored oxygen drain for the current power-bleed stage."""

    if stage >= 2:
        return POWER_BLEED_STAGE_2_DRAIN
    if stage == 1:
        return POWER_BLEED_STAGE_1_DRAIN
    return 0


def pursuit_drain_for_stage(stage: int) -> int:
    """Return the authored threat gain for the current pursuit stage."""

    if stage >= 2:
        return PURSUIT_STAGE_2_DRAIN
    if stage == 1:
        return PURSUIT_STAGE_1_DRAIN
    return 0


def apply_active_condition_drains(state: GameState) -> None:
    """Apply all start-of-turn persistent-condition pressure."""

    leak_drain = leak_drain_for_stage(state.conditions.leak_stage)
    if leak_drain:
        apply_resource_delta(state, "hull", leak_drain)

    power_bleed_drain = power_bleed_drain_for_stage(state.conditions.power_bleed_stage)
    if power_bleed_drain:
        apply_resource_delta(state, "oxygen", power_bleed_drain)

    pursuit_drain = pursuit_drain_for_stage(state.conditions.pursuit_stage)
    if pursuit_drain:
        apply_resource_delta(state, "threat", pursuit_drain)