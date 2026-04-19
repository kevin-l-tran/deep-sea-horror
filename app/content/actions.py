from __future__ import annotations

from app.engine.models import Action, ActionSpec, ConditionType, Resources


ACTION_SPECS: dict[Action, ActionSpec] = {
    Action.SCAN: ActionSpec(
        name="SCAN",
        battery_cost=4,
        full_effect_resource=None,
        full_effect_amount=0,
        partial_effect_amount=0,
        strongest_against=ConditionType.SIGNAL_CONTAMINATION,
    ),
    Action.REPAIR: ActionSpec(
        name="REPAIR",
        battery_cost=0,
        full_effect_resource="hull",
        full_effect_amount=8,
        partial_effect_amount=4,
        strongest_against=ConditionType.LEAK,
    ),
    Action.SILENT: ActionSpec(
        name="SILENT",
        battery_cost=0,
        full_effect_resource="threat",
        full_effect_amount=-8,
        partial_effect_amount=-4,
        strongest_against=ConditionType.PURSUIT,
    ),
    Action.REROUTE: ActionSpec(
        name="REROUTE",
        battery_cost=8,
        full_effect_resource="oxygen",
        full_effect_amount=8,
        partial_effect_amount=4,
        strongest_against=ConditionType.POWER_BLEED,
    ),
}


def get_action_spec(action: Action) -> ActionSpec:
    return ACTION_SPECS[action]


def get_action_cost(action: Action) -> int:
    return ACTION_SPECS[action].battery_cost


def can_afford_action(resources: Resources, action: Action) -> bool:
    return resources.battery >= get_action_cost(action)


def get_full_effect(action: Action) -> tuple[str | None, int]:
    spec = get_action_spec(action)
    return spec.full_effect_resource, spec.full_effect_amount


def get_partial_effect(action: Action) -> tuple[str | None, int]:
    spec = get_action_spec(action)
    return spec.full_effect_resource, spec.partial_effect_amount


def apply_action_cost(resources: Resources, action: Action) -> int:
    """Apply the battery cost for an action and return the cost paid.

    This mutates the provided resources object. Callers should validate that the
    action is affordable before applying the cost.
    """

    cost = get_action_cost(action)
    if cost:
        resources.battery -= cost
    return cost


def format_resource_delta_line(resource: str, amount: int) -> str:
    label = resource.replace("_", " ").title()
    sign = "+" if amount > 0 else ""
    return f"{label} {sign}{amount}."
