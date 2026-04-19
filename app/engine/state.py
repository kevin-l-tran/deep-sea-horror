from dataclasses import dataclass, field
from typing import Optional

from app.engine.models import AIState, ActiveConditions, Resources, TurnCard


STARTING_OXYGEN = 42
STARTING_BATTERY = 40
STARTING_HULL = 50
STARTING_THREAT = 18
TOTAL_TURNS = 12


def _aftermath_lines_factory() -> list[str]:
    return []


@dataclass(slots=True)
class GameState:
    """Mutable run state for the fixed 12-turn scenario."""

    turn_index: int = 0
    rescue_eta: int = TOTAL_TURNS
    resources: Resources = field(
        default_factory=lambda: Resources(
            oxygen=STARTING_OXYGEN,
            battery=STARTING_BATTERY,
            hull=STARTING_HULL,
            threat=STARTING_THREAT,
        )
    )
    ai_state: AIState = AIState.STABLE
    conditions: ActiveConditions = field(default_factory=ActiveConditions)
    current_turn_card: Optional[TurnCard] = None
    current_readouts: list[str] = field(
        default_factory=_aftermath_lines_factory)
    last_scan_result_type: Optional[str] = None
    log: list[str] = field(default_factory=_aftermath_lines_factory)
    game_over: bool = False
    win: bool = False

    def sync_for_turn(self, turn_card: TurnCard) -> None:
        self.current_turn_card = turn_card
        self.current_readouts = list(turn_card.readouts)
        self.ai_state = turn_card.ai_state
        self.rescue_eta = max(0, TOTAL_TURNS - turn_card.turn)

    def clamp_resources(self) -> None:
        self.resources.clamp()

    def check_loss(self) -> bool:
        if self.resources.oxygen <= 0:
            self.game_over = True
            self.win = False
            return True
        if self.resources.hull <= 0:
            self.game_over = True
            self.win = False
            return True
        if self.resources.threat >= 100:
            self.game_over = True
            self.win = False
            return True
        return False

    def check_win(self) -> bool:
        if self.turn_index >= TOTAL_TURNS and not self.game_over:
            self.game_over = True
            self.win = True
            return True
        return False


def build_new_game_state() -> GameState:
    return GameState()
