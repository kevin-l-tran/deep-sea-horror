from app.engine.models import Action, TurnCard
from app.engine.state import GameState, build_new_game_state
from app.engine.turn_flow import prepare_current_turn, resolve_current_turn


class GameController:
    def __init__(self) -> None:
        self.state: GameState = build_new_game_state()

    def new_game(self) -> GameState:
        self.state = build_new_game_state()
        return self.state

    def get_state(self) -> GameState:
        return self.state

    def get_current_turn(self) -> TurnCard:
        return prepare_current_turn(self.state)

    def choose_action(self, action: Action) -> GameState:
        if self.state.game_over:
            raise ValueError("Cannot choose an action after the game is over.")
        
        resolve_current_turn(self.state, action)
        return self.state