from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from app.engine.controller import GameController
from app.engine.formatting import (
    format_action_line,
    format_ai_state,
    format_rescue_eta_line,
    format_threat,
    format_turn_line,
)
from app.engine.models import Action
from app.engine.state import TOTAL_TURNS


class GameScreen(Screen):
    BINDINGS = [
        ("1", "scan", "Scan"),
        ("2", "repair", "Repair"),
        ("3", "silent", "Silent"),
        ("4", "reroute", "Reroute"),
        ("q", "quit_app", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.controller = GameController()
        self.status_message = ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Vertical(id="shell"):
            with Horizontal(id="top_row"):
                yield Static(id="header_panel")
                yield Static(id="resource_panel")
                yield Static(id="readout_panel")

            yield Static(id="ai_panel")
            yield Static(id="action_panel")
            yield Static(id="status_panel")
            yield Static(id="log_panel")

        yield Footer()

    def on_mount(self) -> None:
        self.controller.new_game()
        self.controller.get_current_turn()
        self.refresh_from_state()

    def action_scan(self) -> None:
        self._handle_action(Action.SCAN)

    def action_repair(self) -> None:
        self._handle_action(Action.REPAIR)

    def action_silent(self) -> None:
        self._handle_action(Action.SILENT)

    def action_reroute(self) -> None:
        self._handle_action(Action.REROUTE)

    def action_quit_app(self) -> None:
        self.app.exit()

    def _handle_action(self, action: Action) -> None:
        try:
            self.controller.choose_action(action)
            self.status_message = ""
        except ValueError as exc:
            self.status_message = str(exc)
            self.refresh_from_state()
            return

        state = self.controller.get_state()

        # After a resolved turn, prepare the next one before repainting.
        if not state.game_over:
            self.controller.get_current_turn()

        self.refresh_from_state()

    def refresh_from_state(self) -> None:
        state = self.controller.get_state()

        if not state.game_over and state.current_turn_card is None:
            self.controller.get_current_turn()
            state = self.controller.get_state()

        turn_number = min(state.turn_index + 1, TOTAL_TURNS)

        header_text = "\n".join(
            [
                " DEEP-SEA HORROR // SUBSYSTEM VIEW",
                format_turn_line(turn_number, TOTAL_TURNS),
                format_rescue_eta_line(state.rescue_eta),
            ]
        )

        resource_text = "\n".join(
            [
                " STATUS",
                f" OXYGEN : {state.resources.oxygen}",
                f" BATTERY: {state.resources.battery}",
                f" HULL   : {state.resources.hull}",
                f" THREAT : {format_threat(state.resources.threat)}",
            ]
        )

        readouts = state.current_readouts or ["No active readouts."]
        readout_text = " READOUTS\n" + "\n".join(f" {line}" for line in readouts)

        ai_line = state.current_turn_card.ai_line if state.current_turn_card else ""
        ai_text = "\n".join(
            [
                f" AI [{format_ai_state(state.ai_state)}]",
                f" {ai_line}" if ai_line else " ---",
            ]
        )

        action_text = "\n".join(
            [
                " ACTIONS",
                f" [1] {format_action_line(Action.SCAN)}",
                f" [2] {format_action_line(Action.REPAIR)}",
                f" [3] {format_action_line(Action.SILENT)}",
                f" [4] {format_action_line(Action.REROUTE)}",
            ]
        )

        if state.game_over:
            status_text = " STATUS\n RESCUE ARRIVED." if state.win else " STATUS\n VESSEL LOST."
        elif self.status_message:
            status_text = f" STATUS\n {self.status_message}"
        else:
            status_text = " STATUS\n Awaiting command."

        recent_log = state.log[-8:] if state.log else ["No recent output."]
        log_text = " LOG\n" + "\n".join(f" {line}" for line in recent_log)

        self.query_one("#header_panel", Static).update(header_text)
        self.query_one("#resource_panel", Static).update(resource_text)
        self.query_one("#readout_panel", Static).update(readout_text)
        self.query_one("#ai_panel", Static).update(ai_text)
        self.query_one("#action_panel", Static).update(action_text)
        self.query_one("#status_panel", Static).update(status_text)
        self.query_one("#log_panel", Static).update(log_text)