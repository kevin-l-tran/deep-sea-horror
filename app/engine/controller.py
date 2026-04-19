from app.engine.models import Action, InputKind, TurnCard
from app.engine.state import GameState, build_new_game_state
from app.engine.turn_flow import prepare_current_turn, resolve_current_turn
from app.narration.fallback import looks_like_query
from app.narration.responder import FallbackNarrationResponder, NarrationResponder


class GameController:
    def __init__(self, narration: NarrationResponder | None = None) -> None:
        self.state: GameState = build_new_game_state()
        self.narration: NarrationResponder = narration or FallbackNarrationResponder()

    def new_game(self) -> GameState:
        self.state = build_new_game_state()
        return self.start_turn()

    def get_state(self) -> GameState:
        return self.state

    def get_current_turn(self) -> TurnCard:
        return prepare_current_turn(self.state)

    def start_turn(self) -> GameState:
        turn_card = prepare_current_turn(self.state)

        if self.state.game_over:
            self.state.narration.current_scene_text = ""
            return self.state

        self.state.narration.current_scene_text = self.narration.narrate_scene(
            self.state,
            turn_card,
        )
        return self.state

    def submit_action(self, action: Action) -> GameState:
        if self.state.game_over:
            raise ValueError("Cannot choose an action after the game is over.")

        turn_card = prepare_current_turn(self.state)
        if self.state.game_over:
            return self.state

        result = resolve_current_turn(self.state, action)

        self.state.narration.last_input_kind = InputKind.COMMITMENT
        self.state.narration.interpreted_action = action
        self.state.narration.interpretation_confidence = 1.0

        self.state.log.extend(result.log_lines)

        self.state.narration.last_aftermath_text = self.narration.narrate_aftermath(
            turn_card,
            action,
            result,
        )

        if not self.state.game_over:
            self.start_turn()

        return self.state

    def submit_text(self, text: str) -> GameState:
        if self.state.game_over:
            raise ValueError("Cannot submit text after the game is over.")

        turn_card = prepare_current_turn(self.state)
        if self.state.game_over:
            return self.state

        stripped = text.strip()

        if not stripped:
            self.state.log.append(
                "Input unclear. Rephrase or choose [1] SCAN [2] REPAIR [3] SILENT [4] REROUTE."
            )
            self.state.narration.last_input_kind = InputKind.UNKNOWN
            return self.state

        if looks_like_query(stripped):
            response = self.narration.answer_query(self.state, turn_card, stripped)
            self.state.log.append(response)
            return self.state

        # temporary: explicit fallback until commitment parsing exists
        self.state.log.append(
            "Commitment parsing not wired yet. Use [1] SCAN [2] REPAIR [3] SILENT [4] REROUTE."
        )
        self.state.narration.last_input_kind = InputKind.COMMITMENT
        return self.state