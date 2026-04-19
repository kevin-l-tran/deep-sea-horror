from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class Action(Enum):
    """The four player actions available every turn."""

    SCAN = auto()
    REPAIR = auto()
    SILENT = auto()
    REROUTE = auto()


class AIState(Enum):
    """Authored AI reliability phase for the current turn."""

    STABLE = auto()
    DEGRADED = auto()
    CORRUPTED = auto()


class ConditionType(Enum):
    """Internal-only condition taxonomy. Do not show after the tutorial."""

    LEAK = auto()
    POWER_BLEED = auto()
    PURSUIT = auto()
    SIGNAL_CONTAMINATION = auto()


class OutcomeTier(Enum):
    """Resolution strength for the chosen action on a turn."""

    STRONG = auto()
    PARTIAL = auto()
    WRONG = auto()


def _resource_deltas_factory() -> dict[str, int]:
    return {}


def _aftermath_lines_factory() -> list[str]:
    return []


def _partial_outcomes_factory() -> dict[Action, "PartialOutcome"]:
    return {}


def _aftermath_map_factory() -> dict[Action, list[str]]:
    return {}


@dataclass(slots=True)
class Resources:
    oxygen: int
    battery: int
    hull: int
    threat: int

    def clamp(self) -> None:
        self.oxygen = max(0, min(100, self.oxygen))
        self.battery = max(0, min(100, self.battery))
        self.hull = max(0, min(100, self.hull))
        self.threat = max(0, min(100, self.threat))


@dataclass(slots=True)
class ActiveConditions:
    """Only the authored arcs that exist in the fixed deck."""

    leak_stage: int = 0
    power_bleed_stage: int = 0
    pursuit_stage: int = 0
    contamination_active: bool = False


@dataclass(slots=True)
class AcutePenalty:
    """One-turn authored penalty, canceled only by a strong match."""

    resource: str
    amount: int


@dataclass(slots=True)
class ConditionChanges:
    """State changes applied when the turn is prepared or resolved."""

    start_leak_stage: Optional[int] = None
    start_power_bleed_stage: Optional[int] = None
    start_pursuit_stage: Optional[int] = None
    set_contamination_active: Optional[bool] = None
    clear_leak_after_turn: bool = False
    clear_power_bleed_after_turn: bool = False


@dataclass(slots=True)
class PartialOutcome:
    """Author-authored costly-partial behavior for a specific action."""

    resource_deltas: dict[str, int] = field(
        default_factory=_resource_deltas_factory)
    clear_contamination: bool = False
    aftermath_lines: list[str] = field(
        default_factory=_aftermath_lines_factory)


@dataclass(slots=True)
class TurnCard:
    """Authored content and resolution hints for a single turn."""

    turn: int
    readouts: list[str]
    ai_state: AIState
    ai_line: str
    strong_action: Action
    acute_penalty: Optional[AcutePenalty] = None
    scan_result: Optional[str] = None
    condition_changes: ConditionChanges = field(
        default_factory=ConditionChanges)
    partial_outcomes: dict[Action, PartialOutcome] = field(
        default_factory=_partial_outcomes_factory)
    strong_aftermath: dict[Action, list[str]] = field(
        default_factory=_aftermath_map_factory)
    wrong_aftermath: dict[Action, list[str]] = field(
        default_factory=_aftermath_map_factory)
    purpose_note: str = ""


@dataclass(slots=True)
class ResolutionResult:
    outcome: OutcomeTier
    log_lines: list[str] = field(default_factory=_aftermath_lines_factory)
    acute_penalty_canceled: bool = False
    clear_contamination: bool = False


@dataclass(slots=True)
class ActionSpec:
    name: str
    battery_cost: int
    full_effect_resource: Optional[str]
    full_effect_amount: int
    partial_effect_amount: int
    strongest_against: ConditionType
