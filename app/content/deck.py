from app.engine.models import (
    AIState,
    Action,
    AcutePenalty,
    ConditionChanges,
    PartialOutcome,
    TurnCard,
)


DECK: list[TurnCard] = [
    TurnCard(
        turn=1,
        readouts=["Localized hull stress warning."],
        ai_state=AIState.STABLE,
        ai_line="Localized hull stress detected at frame seam.",
        strong_action=Action.REPAIR,
        strong_aftermath={
            Action.REPAIR: ["Pressure drop slowed."]
        },
        purpose_note="Teach hull recovery and the event-response format.",
    ),
    TurnCard(
        turn=2,
        readouts=["Metallic scraping along outer hull."],
        ai_state=AIState.STABLE,
        ai_line="External acoustic contact closing on outer hull.",
        strong_action=Action.SILENT,
        strong_aftermath={
            Action.SILENT: ["External contact fell back, then returned."]
        },
        purpose_note="Teach threat control and establish external danger.",
    ),
    TurnCard(
        turn=3,
        readouts=["Garbled crew voice on internal channel."],
        ai_state=AIState.STABLE,
        ai_line="Signal origin unclear. Channel integrity uncertain.",
        strong_action=Action.SCAN,
        scan_result="Voice print mismatch. Internal source not confirmed.",
        strong_aftermath={
            Action.SCAN: [
                "Channel source remains external to verified crew logs."]
        },
        purpose_note="Teach SCAN as diagnosis rather than as a truth button.",
    ),
    TurnCard(
        turn=4,
        readouts=["Oxygen recycler stutter."],
        ai_state=AIState.STABLE,
        ai_line="Life-support instability spreading across recycler load.",
        strong_action=Action.REROUTE,
        strong_aftermath={
            Action.REROUTE: ["Recycler output stabilizing."]
        },
        purpose_note="Teach battery-for-oxygen tradeoff.",
    ),
    TurnCard(
        turn=5,
        readouts=[
            "Forward seam ticks under load.",
            "Condensation gathers beneath port handrail.",
        ],
        ai_state=AIState.DEGRADED,
        ai_line="Frame pressure wandering. Air loss may only be the symptom.",
        strong_action=Action.REPAIR,
        scan_result="Pressure differential isolated near the forward seam.",
        condition_changes=ConditionChanges(start_leak_stage=1),
        partial_outcomes={
            Action.SCAN: PartialOutcome(
                aftermath_lines=[
                    "Pressure differential isolated near the forward seam."]
            )
        },
        strong_aftermath={
            Action.REPAIR: [
                "The seam steadies, though the hull keeps talking."]
        },
        purpose_note="Introduce persistent structural damage and mixed symptoms.",
    ),
    TurnCard(
        turn=6,
        readouts=[
            "An internal voice repeats your last breath.",
            "Deck plating answers half a second late.",
        ],
        ai_state=AIState.DEGRADED,
        ai_line="One of these sounds belongs to us. I am not certain which.",
        strong_action=Action.SCAN,
        acute_penalty=AcutePenalty(resource="hull", amount=-4),
        scan_result="Archive mismatch detected. Something is reusing the channel.",
        condition_changes=ConditionChanges(
            set_contamination_active=True,
            clear_leak_after_turn=True,
        ),
        partial_outcomes={
            Action.REPAIR: PartialOutcome(
                resource_deltas={"hull": 4},
                aftermath_lines=["The plating holds. The voice does not stop."]
            )
        },
        strong_aftermath={
            Action.SCAN: ["Archive mismatch confirmed. Channel contamination thins."],
        },
        purpose_note="First triage turn with ambiguity, carryover damage, and acute punishment.",
    ),
    TurnCard(
        turn=7,
        readouts=[
            "Recycler cycle lengthening.",
            "Sonar return repeats at impossible distance.",
        ],
        ai_state=AIState.DEGRADED,
        ai_line="Load is slipping between circuits. The echo may be borrowing it.",
        strong_action=Action.REROUTE,
        acute_penalty=AcutePenalty(resource="oxygen", amount=-4),
        scan_result="Auxiliary bus load irregularity detected. Echo source unresolved.",
        condition_changes=ConditionChanges(start_power_bleed_stage=1),
        partial_outcomes={
            Action.SCAN: PartialOutcome(
                aftermath_lines=[
                    "The load problem sharpens. The echo remains unresolved."]
            )
        },
        strong_aftermath={
            Action.REROUTE: ["Recycler output stabilizing."]
        },
        purpose_note="Push oxygen pressure and overlapping symptoms.",
    ),
    TurnCard(
        turn=8,
        readouts=[
            "Aux relay housing too hot to touch.",
            "Aft knocking syncs with fan slowdown.",
        ],
        ai_state=AIState.DEGRADED,
        ai_line="Quiet may preserve what remains.",
        strong_action=Action.REROUTE,
        acute_penalty=AcutePenalty(resource="battery", amount=-4),
        scan_result="Diagnostic confidence degraded. Fault origin not isolated.",
        condition_changes=ConditionChanges(clear_power_bleed_after_turn=True),
        partial_outcomes={
            Action.SILENT: PartialOutcome(
                resource_deltas={"threat": -4},
                aftermath_lines=[
                    "The knocking softens. The recycler still slips."]
            )
        },
        strong_aftermath={
            Action.REROUTE: ["The relay cools. The recycler stops dragging."]
        },
        purpose_note="Intentional AI misread during life-support panic plus battery shock.",
    ),
    TurnCard(
        turn=9,
        readouts=[
            "Outer hull contact repeats in your own rhythm.",
            "Channel opens before you touch it.",
        ],
        ai_state=AIState.CORRUPTED,
        ai_line="Answer softly. It already knows the loud parts.",
        strong_action=Action.SILENT,
        acute_penalty=AcutePenalty(resource="threat", amount=6),
        scan_result="External contact confirmed. Channel state remains unreliable.",
        condition_changes=ConditionChanges(
            start_pursuit_stage=1),
        partial_outcomes={
            Action.SCAN: PartialOutcome(
                clear_contamination=True,
                aftermath_lines=[
                    "The channel narrows. The contact closes anyway."]
            )
        },
        strong_aftermath={
            Action.SILENT: ["Something outside adjusts to the silence."]
        },
        purpose_note="Start the final oppressive arc and punish greed harder.",
    ),
    TurnCard(
        turn=10,
        readouts=[
            "Aft plates bow inward, then release.",
            "Two knocks answer the pump cycle.",
        ],
        ai_state=AIState.CORRUPTED,
        ai_line="Mend the shape. Do not feed the sound.",
        strong_action=Action.SILENT,
        acute_penalty=AcutePenalty(resource="threat", amount=6),
        scan_result="Structural strain reduced locally. Rhythm source unchanged.",
        partial_outcomes={
            Action.REPAIR: PartialOutcome(
                resource_deltas={"hull": 4},
                aftermath_lines=["The plates settle. The knocking keeps pace."]
            )
        },
        strong_aftermath={
            Action.SILENT: ["External contact fell back, then returned."]
        },
        purpose_note="Deliberately tempt REPAIR during a pursuit turn.",
    ),
    TurnCard(
        turn=11,
        readouts=[
            "Every active line carries a second breathing pattern.",
            "Distance to contact: unchanged.",
        ],
        ai_state=AIState.CORRUPTED,
        ai_line="Keep the air moving. Keep it from settling.",
        strong_action=Action.SILENT,
        acute_penalty=AcutePenalty(resource="threat", amount=8),
        scan_result="Airflow variance corrected. Second pattern persists across all lines.",
        condition_changes=ConditionChanges(
            start_pursuit_stage=2),
        partial_outcomes={
            Action.REROUTE: PartialOutcome(
                resource_deltas={"oxygen": 4},
                aftermath_lines=[
                    "Airflow improves for a moment. The second breathing pattern remains."]
            )
        },
        strong_aftermath={
            Action.SILENT: [
                "The breathing pattern loses the room for a moment."]
        },
        purpose_note="Escalate pressure and misdirect toward REROUTE.",
    ),
    TurnCard(
        turn=12,
        readouts=[
            "Impact pattern matches internal footfall.",
            "External latch pressure increasing.",
        ],
        ai_state=AIState.CORRUPTED,
        ai_line="If we stop hearing it, it will hear us first.",
        strong_action=Action.SILENT,
        acute_penalty=AcutePenalty(resource="threat", amount=8),
        scan_result="Contact remains outside. Pattern matching has become non-local.",
        partial_outcomes={
            Action.REPAIR: PartialOutcome(
                resource_deltas={"hull": 4},
                aftermath_lines=[
                    "Something steadies inside. The latch pressure does not."]
            ),
            Action.REROUTE: PartialOutcome(
                resource_deltas={"oxygen": 4},
                aftermath_lines=[
                    "Something steadies inside. The latch pressure does not."]
            ),
        },
        strong_aftermath={
            Action.SILENT: ["Something outside adjusts to the silence."]
        },
        purpose_note="End on suppression, not resolution.",
    ),
]


def get_turn(turn_number: int) -> TurnCard:
    return DECK[turn_number - 1]
