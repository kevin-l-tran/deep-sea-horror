from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Input, Static

from app.engine.controller import GameController
from app.engine.formatting import format_ai_state, format_threat
from app.engine.models import Action
from app.engine.state import TOTAL_TURNS
from app.narration.live_responder import GeminiNarrationResponder
from app.narration.responder import FallbackNarrationResponder

import logging
logger = logging.getLogger(__name__)


class CommandInput(Input):
    class Hotkey(Message):
        def __init__(self, action: Action) -> None:
            self.action = action
            super().__init__()

    KEY_TO_ACTION = {
        "1": Action.SCAN,
        "2": Action.REPAIR,
        "3": Action.SILENT,
        "4": Action.REROUTE,
    }

    def on_key(self, event: events.Key) -> None:
        action = self.KEY_TO_ACTION.get(event.key)
        if action is not None:
            event.prevent_default()
            event.stop()
            self.post_message(self.Hotkey(action))


class GameScreen(Screen):
    BINDINGS = [
        ("q", "quit_app", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        try:
            narration = GeminiNarrationResponder()
        except Exception:
            logger.exception(
                "Failed to initialize Gemini narration responder; using fallback responder."
            )
            narration = FallbackNarrationResponder()

        self.controller = GameController(narration=narration)
        self.status_message = ""
        self.state = self.controller.get_state()

    def compose(self) -> ComposeResult:
        with Vertical(id="shell"):
            yield Static(id="meta")
            yield Static(id="scene")
            yield Static(id="log")
            yield CommandInput(
                placeholder="Type a question or an action...",
                id="command",
            )

    def on_mount(self) -> None:
        self.state = self.controller.new_game()
        self.refresh_from_state()
        self._focus_command_input()

    def on_command_input_hotkey(self, message: CommandInput.Hotkey) -> None:
        self._handle_action(message.action)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        event.input.value = ""

        if not text:
            self.status_message = "Input unclear. Rephrase or use 1-4."
            self.refresh_from_state()
            self._focus_command_input()
            return

        try:
            self.state = self.controller.submit_text(text)
        except ValueError as exc:
            self.status_message = str(exc)
            self.refresh_from_state()
            self._focus_command_input()
            return

        self.status_message = ""
        self.refresh_from_state()
        self._focus_command_input()

    def action_quit_app(self) -> None:
        self.app.exit()

    def _handle_action(self, action: Action) -> None:
        try:
            self.state = self.controller.submit_action(action)
        except ValueError as exc:
            self.status_message = str(exc)
            self.refresh_from_state()
            self._focus_command_input()
            return

        self.status_message = ""
        self.refresh_from_state()
        self._focus_command_input()

    def _focus_command_input(self) -> None:
        command = self.query_one(CommandInput)
        if not self.state.game_over and not command.disabled:
            command.focus()

    def refresh_from_state(self) -> None:
        self.state = self.controller.get_state()
        state = self.state

        turn_number = min(state.turn_index + 1, TOTAL_TURNS)
        ai_text = format_ai_state(state.ai_state)
        threat_text = format_threat(state.resources.threat)

        query_text = "QUERY OPEN" if not state.query.used_this_turn else "COMMITMENT REQUIRED"

        fallback_text = "FALLBACK" if state.narration.fallback_used else "PRIMARY"

        if state.game_over:
            status_text = "RESCUE ARRIVED." if state.win else "VESSEL LOST."
        elif self.status_message:
            status_text = self.status_message
        else:
            status_text = "AWAITING INPUT."

        meta_text = "\n".join(
            [
                f"TURN {turn_number:02d}/{TOTAL_TURNS:02d}  ETA {state.rescue_eta:02d}  AI {ai_text}",
                f"O2 {state.resources.oxygen:02d}  BAT {state.resources.battery:02d}  HULL {state.resources.hull:02d}  THREAT {threat_text}",
                f"{query_text}  MODE {fallback_text}",
                "[1] SCAN  [2] REPAIR  [3] SILENT  [4] REROUTE",
                status_text,
            ]
        )

        narrated_scene = state.narration.current_scene_text.strip()
        if narrated_scene:
            scene_text = narrated_scene
        else:
            readouts = state.current_readouts or ["No active readouts."]
            ai_line = state.current_turn_card.ai_line if state.current_turn_card else ""
            parts = ["\n".join(readouts)]
            if ai_line:
                parts.append(f"AI: {ai_line}")
            scene_text = "\n\n".join(parts)

        lines: list[str] = []
        seen: set[str] = set()

        def add_line(line: str) -> None:
            cleaned = line.strip()
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                lines.append(cleaned)

        if state.query.last_query_response:
            add_line(f"> {state.query.last_query_response}")

        if state.narration.last_aftermath_text:
            add_line(state.narration.last_aftermath_text)

        for line in state.log[-5:]:
            add_line(line)

        log_text = "\n".join(lines or ["No recent output."])

        self.query_one("#meta", Static).update(meta_text)
        self.query_one("#scene", Static).update(scene_text)
        self.query_one("#log", Static).update(log_text)

        command = self.query_one(CommandInput)
        command.disabled = state.game_over
        command.placeholder = (
            "Run complete. Press q to quit."
            if state.game_over
            else "Type a question or an action..."
        )