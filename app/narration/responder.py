from typing import Protocol

from app.engine.models import Action, ResolutionResult, TurnCard
from app.engine.state import GameState
from app.narration.fallback import answer_query, narrate_aftermath, render_scene


class NarrationResponder(Protocol):
    def narrate_scene(self, state: GameState, turn_card: TurnCard) -> str: ...

    def answer_query(self, state: GameState,
                     turn_card: TurnCard, text: str) -> str: ...

    def narrate_aftermath(
        self,
        turn_card: TurnCard,
        action: Action,
        result: ResolutionResult,
    ) -> str: ...


class FallbackNarrationResponder:
    def narrate_scene(self, state: GameState, turn_card: TurnCard) -> str:
        return render_scene(turn_card)

    def answer_query(self, state: GameState, turn_card: TurnCard, text: str) -> str:
        return answer_query(state, turn_card, text)

    def narrate_aftermath(
        self,
        turn_card: TurnCard,
        action: Action,
        result: ResolutionResult,
    ) -> str:
        return narrate_aftermath(turn_card, action, result)
