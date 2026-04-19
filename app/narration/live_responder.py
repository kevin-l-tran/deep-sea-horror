import json
import re
from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from app.engine.models import Action, ResolutionResult, TurnCard
from app.engine.state import GameState
from app.narration.fallback import (
    answer_query as fallback_answer_query,
    narrate_aftermath as fallback_narrate_aftermath,
    render_scene as fallback_render_scene,
)
from app.narration.scene_builder import build_scene_packet

import logging
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class SceneResponse(BaseModel):
    scene_text: str = Field(min_length=1, max_length=700)


class QueryResponse(BaseModel):
    response_text: str = Field(min_length=1, max_length=350)


class AftermathResponse(BaseModel):
    aftermath_text: str = Field(min_length=1, max_length=300)


class GeminiNarrationResponder:
    """
    Fast ship path:
    - Gemini for scene/query/aftermath wording
    - existing fallback functions for any failure
    - no commitment parsing here yet
    """

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        temperature_scene: float = 0.7,
        temperature_query: float = 0.35,
        temperature_aftermath: float = 0.4,
        api_key: str | None = None,
    ) -> None:
        self.client = genai.Client(
            api_key=api_key) if api_key else genai.Client()
        self.model = model
        self.temperature_scene = temperature_scene
        self.temperature_query = temperature_query
        self.temperature_aftermath = temperature_aftermath

    def close(self) -> None:
        self.client.close()

    def narrate_scene(self, state: GameState, turn_card: TurnCard) -> str:
        packet = build_scene_packet(state, turn_card)

        payload = {
            "turn": packet.turn,
            "ai_state": state.ai_state.name,
            "resources": {
                "oxygen": state.resources.oxygen,
                "battery": state.resources.battery,
                "hull": state.resources.hull,
                "threat": state.resources.threat,
            },
            "required_scene_facts": packet.required_scene_facts,
            "misleading_facts": packet.misleading_facts,
            "carryover_condition_facts": packet.carryover_condition_facts,
            "query_available": packet.query_available,
            "forbidden_claims": packet.forbidden_claims,
            "ai_line_seed": packet.ai_line_seed,
        }

        system_instruction = (
            "You are the narration layer for a fixed 12-turn survival horror game. "
            "Write only the final scene prose. No preamble, no markdown, no labels. "
            "Use only the supplied facts. "
            "Do not invent mechanics, diagnoses, future outcomes, entities, or sensors. "
            "Do not recommend actions. Do not name internal rule labels. "
            "Write 3 to 5 short sentences."
        )

        try:
            text = self._generate_text(
                system_instruction,
                json.dumps(payload, indent=2),
                temperature=0.6,
                max_output_tokens=512,
            )
            if self._bad_scene_or_query_text(text):
                raise ValueError("scene text violated guardrails")
            state.narration.fallback_used = False
            return text
        except Exception:
            logger.exception(
                "Scene narration fallback on turn %s", turn_card.turn)
            state.narration.fallback_used = True
            return fallback_render_scene(turn_card)

    def answer_query(self, state: GameState, turn_card: TurnCard, text: str) -> str:
        if state.query.used_this_turn:
            return "You have already spent your one query for this turn."

        packet = build_scene_packet(state, turn_card)

        payload = {
            "turn": turn_card.turn,
            "ai_state": state.ai_state.name,
            "player_question": text,
            "query_answer_facts": list(turn_card.query_answer_facts),
            "required_scene_facts": packet.required_scene_facts,
            "carryover_condition_facts": packet.carryover_condition_facts,
            "forbidden_claims": list(turn_card.forbidden_claims),
            "diagnostic_boundary": (
                "If the question asks for hidden diagnosis, source confirmation, or true cause, "
                "stay uncertain and descriptive."
            ),
        }

        system_instruction = (
            "Answer one brief in-fiction player question. "
            "Write only the final answer. No preamble, no markdown. "
            "Use only supplied facts. Stay descriptive, uncertain, and non-directive. "
            "Do not reveal hidden truth. Do not recommend actions. "
            "Write 1 to 3 short sentences."
        )

        try:
            response_text = self._generate_text(
                system_instruction,
                json.dumps(payload, indent=2),
                temperature=0.3,
                max_output_tokens=256,
            )
            if self._bad_scene_or_query_text(response_text):
                raise ValueError("query text violated guardrails")

            state.query.used_this_turn = True
            state.query.last_query = text
            state.query.last_query_response = response_text
            state.narration.last_input_kind = None
            state.narration.fallback_used = False
            return response_text
        except Exception:
            logger.exception(
                "Answer query fallback on turn %s", turn_card.turn)
            state.narration.fallback_used = True
        return fallback_answer_query(state, turn_card, text)

    def narrate_aftermath(
        self,
        turn_card: TurnCard,
        action: Action,
        result: ResolutionResult,
    ) -> str:
        payload = {
            "turn": turn_card.turn,
            "action": action.name,
            "outcome": result.outcome.name,
            "deterministic_log_lines": list(result.log_lines),
            "strong_action": turn_card.strong_action.name,
            "scan_result": turn_card.scan_result,
            "fallback_aftermath_lines": turn_card.fallback_aftermath_lines.get(action, []),
        }

        system_instruction = (
            "Write terse aftermath prose for a deterministic survival horror turn. "
            "Write only the final aftermath text. No preamble, no markdown. "
            "Use only supplied facts. "
            "Do not add mechanics, hidden causes, or strategy advice. "
            "Do not say whether the player was correct. "
            "Write 1 to 2 short sentences."
        )

        try:
            text = self._generate_text(
                system_instruction,
                json.dumps(payload, indent=2),
                temperature=0.3,
                max_output_tokens=128,
            )
            if self._bad_aftermath_text(text):
                raise ValueError("aftermath text violated guardrails")
            return text
        except Exception:
            logger.exception(
                "Aftermath narration fallback on turn %s", turn_card.turn)
            return fallback_narrate_aftermath(turn_card, action, result)

    def _generate_text(
        self,
        system_instruction: str,
        user_prompt: str,
        *,
        temperature: float,
        max_output_tokens: int,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )

        cand = response.candidates[0] if response.candidates else None
        logger.info("Gemini raw response: %r", response.text)
        logger.info(
            "finish_reason=%r finish_message=%r token_count=%r usage=%r",
            getattr(cand, "finish_reason", None),
            getattr(cand, "finish_message", None),
            getattr(cand, "token_count", None),
            response.usage_metadata,
        )

        text = (response.text or "").strip()
        if not text:
            raise ValueError("Gemini returned no text")

        return text

    def _bad_scene_or_query_text(self, text: str) -> bool:
        lowered = text.lower()

        hard_bans = (
            "you should",
            "i recommend",
            "recommended action",
            "best action",
            "correct action",
            "choose ",
            "pick ",
            "repair now",
            "scan now",
            "reroute now",
            "go silent",
            "silent running",
            "structural event",
            "pursuit",
            "power bleed",
            "signal contamination",
        )

        return any(phrase in lowered for phrase in hard_bans)

    def _bad_aftermath_text(self, text: str) -> bool:
        lowered = text.lower()
        hard_bans = (
            "you should",
            "correct choice",
            "wrong action",
            "best action",
            "recommended action",
        )
        return any(phrase in lowered for phrase in hard_bans)
