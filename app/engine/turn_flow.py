from app.content.deck import get_turn
from app.content.actions import format_resource_delta_line
from app.engine.conditions import apply_active_condition_drains, apply_resource_delta
from app.engine.models import Action, OutcomeTier, ResolutionResult, TurnCard
from app.engine.resolver import resolve_action
from app.engine.state import GameState, TOTAL_TURNS


PASSIVE_OXYGEN_DRAIN = -2
PASSIVE_THREAT_GAIN = 2
TURN_NINE_CONTAMINATION_SPIKE = 3


def current_turn_number(state: GameState) -> int:
    return state.turn_index + 1


def prepare_current_turn(state: GameState) -> TurnCard:
    """Prepare and cache the current turn, applying all start-of-turn pressure.

    This function is idempotent for the active turn. Calling it again before the
    player acts returns the already-prepared turn card without reapplying drains.
    """

    if state.game_over:
        raise ValueError("Cannot prepare a turn after the game is over.")

    turn_number = current_turn_number(state)
    if turn_number > TOTAL_TURNS:
        raise ValueError("There are no more turns to prepare.")

    if state.current_turn_card is not None and state.current_turn_card.turn == turn_number:
        return state.current_turn_card

    turn_card = get_turn(turn_number)
    _apply_turn_start_condition_changes(state, turn_card)
    _apply_passive_pressure(state)
    apply_active_condition_drains(state)
    _apply_turn_nine_contamination_spike(state, turn_card)
    state.sync_for_turn(turn_card)
    state.clamp_resources()
    state.check_loss()
    return turn_card


def resolve_current_turn(state: GameState, action: Action) -> ResolutionResult:
    turn_card = prepare_current_turn(state)

    if state.game_over:
        raise ValueError(
            "Cannot resolve an action: the run ended during turn preparation."
        )

    result = resolve_action(state, turn_card, action)
    finalize_turn(state, turn_card, result)
    return result


def finalize_turn(state: GameState, turn_card: TurnCard, result: ResolutionResult) -> None:
    if turn_card.acute_penalty and not result.acute_penalty_canceled:
        apply_resource_delta(
            state, turn_card.acute_penalty.resource, turn_card.acute_penalty.amount)
        state.log.append(
            format_resource_delta_line(
                turn_card.acute_penalty.resource,
                turn_card.acute_penalty.amount,
            )
        )

    if result.clear_contamination:
        state.conditions.contamination_active = False

    state.log.extend(result.log_lines)
    _apply_end_of_turn_cleanup(state, turn_card, result)
    state.clamp_resources()

    if state.check_loss():
        return

    state.turn_index += 1
    state.current_turn_card = None
    state.current_readouts = []
    state.check_win()


def _apply_turn_start_condition_changes(state: GameState, turn_card: TurnCard) -> None:
    changes = turn_card.condition_changes

    if changes.start_leak_stage is not None:
        state.conditions.leak_stage = changes.start_leak_stage

    if changes.start_power_bleed_stage is not None:
        state.conditions.power_bleed_stage = changes.start_power_bleed_stage

    if changes.start_pursuit_stage is not None:
        state.conditions.pursuit_stage = changes.start_pursuit_stage

    if changes.set_contamination_active is not None:
        state.conditions.contamination_active = changes.set_contamination_active


def _apply_passive_pressure(state: GameState) -> None:
    state.resources.oxygen += PASSIVE_OXYGEN_DRAIN
    state.resources.threat += PASSIVE_THREAT_GAIN


def _apply_turn_nine_contamination_spike(state: GameState, turn_card: TurnCard) -> None:
    if turn_card.turn == 9 and state.conditions.contamination_active:
        state.resources.threat += TURN_NINE_CONTAMINATION_SPIKE


def _apply_end_of_turn_cleanup(
    state: GameState,
    turn_card: TurnCard,
    result: ResolutionResult,
) -> None:
    if turn_card.turn == 5 and state.conditions.leak_stage > 0 and result.outcome is not OutcomeTier.STRONG:
        state.conditions.leak_stage = 2

    if (
        turn_card.turn == 7
        and state.conditions.power_bleed_stage > 0
        and result.outcome is not OutcomeTier.STRONG
    ):
        state.conditions.power_bleed_stage = 2

    if turn_card.condition_changes.clear_leak_after_turn:
        state.conditions.leak_stage = 0

    if turn_card.condition_changes.clear_power_bleed_after_turn:
        state.conditions.power_bleed_stage = 0

    if turn_card.turn >= 9:
        state.conditions.contamination_active = False
