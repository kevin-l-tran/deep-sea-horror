# Deep Sea Horror Terminal Game

## 12-Turn Event Deck v5.0

**Companion direction for Hackathon MVP v4.0, revised for costly partial successes and tighter SCAN usage**

This document defines a revised 12-turn sequence for the MVP.
The run is still fixed and should be implemented as authored data, not generated procedurally.

This revision makes three intentional changes:

- late-game bait actions should usually produce a **costly partial success** instead of a total null result
- **SCAN matters strongly on a small number of authored turns**, rather than being a broadly useful fallback
- polish remains explicitly out of scope until the full run is playable and tuned once

---

## 1. Deck Rules

- Turns 1 to 4 act as the tutorial.
- The deck is fixed.
- Internal problem classes are for implementation only.
- After Turn 4, the player should not see category labels.
- Persistent conditions are authored and limited.
- Acute penalties are authored and limited.
- AI guidance becomes incomplete and then sometimes wrong.
- The last four turns should feel oppressive, not fair.
- Tutorial AI should be readable, but should not explicitly name the answer.
- Most late bait turns should still let the player affect **something real**, even when they misread the core danger.
- SCAN should feel decisive on only a few authored turns, not like a generic truth button.

---

## 2. AI State Schedule

- **Turns 1 to 4:** Stable
- **Turns 5 to 8:** Degraded
- **Turns 9 to 12:** Corrupted

---

## 3. Persistent Condition Arc Overview

### Arc A: Leak

- **Introduced:** Turn 5
- **Stage 1 drain:** Hull -3 at start of turn while active
- **Stage 2 drain:** Hull -5 at start of turn while active
- **Primary clear action:** REPAIR
- **Escalates on:** Turn 6 if not cleared on Turn 5
- **Ends after:** Turn 6

### Arc B: Signal Contamination

- **Introduced:** Turn 6
- **Direct drain:** none by default
- **Effect:** one readout or AI implication becomes unreliable while active
- **Primary clear action:** SCAN
- **Escalation:** if still active at start of Turn 9, apply Threat +3 once
- **Ends after:** Turn 9 if not cleared earlier

### Arc C: Power Bleed

- **Introduced:** Turn 7
- **Stage 1 drain:** Oxygen -3 at start of turn while active
- **Stage 2 drain:** Oxygen -5 at start of turn while active
- **Primary clear action:** REROUTE
- **Escalates on:** Turn 8 if not cleared on Turn 7
- **Ends after:** Turn 8

### Arc D: Pursuit

- **Introduced:** Turn 9
- **Stage 1 drain:** Threat +5 at start of turn while active
- **Stage 2 drain:** Threat +8 at start of turn while active
- **Primary counter action:** SILENT
- **Special rule:** SILENT suppresses the current turn's Pursuit drain on a strong match, but does not permanently remove the arc
- **Escalates on:** Turn 11
- **Ends after:** Turn 12 rescue resolution

---

## 4. Acute Penalty Schedule

These penalties are resolved after the player acts.

- **Turn 1:** none
- **Turn 2:** none
- **Turn 3:** none
- **Turn 4:** none
- **Turn 5:** none
- **Turn 6:** Hull -4
- **Turn 7:** Oxygen -4
- **Turn 8:** Battery -4
- **Turn 9:** Threat +6
- **Turn 10:** Threat +6
- **Turn 11:** Threat +8
- **Turn 12:** Threat +8

Strong matches cancel the acute penalty.
Partial matches and wrong reads still take it unless the turn notes explicitly say otherwise.

---

## 5. Costly Partial Success Rule

This deck uses a stricter late-game interpretation of partial and wrong reads.

### General rule

On late bait turns, the player should usually still affect the subsystem they reacted to.

Examples:

- a bad **REPAIR** may still steady the hull briefly while failing to address the real source of danger
- a bad **REROUTE** may still improve oxygen briefly while making no meaningful progress against pursuit
- a risky **SCAN** may clarify one fact while still leaving the player exposed to the actual penalty

### Purpose

The player should feel:

- underinformed
- pressured
- punished for misreading
- but not completely disconnected from the fiction of their own action

The game should feel cruel, not random.

---

## 6. SCAN Priority Rule

SCAN is intentionally narrow in this revision.

### High-value SCAN turns

- **Turn 3:** tutorial diagnosis
- **Turn 6:** primary resolution of Signal Contamination
- **Turn 9:** risky greed play only if Signal Contamination is still active and the player wants to remove it under pursuit pressure

### Low-value SCAN turns

- **Turns 5, 7, 8, 10, 11, 12:** SCAN may produce flavor, partial truth, or corrupted confirmation, but should not usually become the dominant answer

### Implementation intent

If the player reaches for SCAN outside its authored high-value turns, it should usually help them understand the situation only a little, and too late.

---

## 7. Turn Deck Table

| Turn | Player-Facing Readouts | AI State | AI Line | Hidden Condition State (dev only) | Acute Penalty | Strong Action (dev only) | Notable Partial / Bait Outcome | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Localized hull stress warning. | Stable | Localized hull stress detected at frame seam. | None | None | REPAIR | Partial REPAIR still helps Hull. | Teach hull recovery and the event-response format without explicitly naming the answer. |
| 2 | Metallic scraping along outer hull. | Stable | External acoustic contact closing on outer hull. | None | None | SILENT | Partial SILENT lowers some Threat but does not fully shake contact. | Teach threat control and establish external danger without explicit instruction. |
| 3 | Garbled crew voice on internal channel. | Stable | Signal origin unclear. Channel integrity uncertain. | None | None | SCAN | Partial SCAN reveals doubt, not certainty. | Teach SCAN as diagnosis rather than as a truth button. |
| 4 | Oxygen recycler stutter. | Stable | Life-support instability spreading across recycler load. | None | None | REROUTE | Partial REROUTE helps Oxygen but costs full Battery. | Teach battery-for-oxygen tradeoff without a direct recommendation line. |
| 5 | Forward seam ticks under load. / Condensation gathers beneath port handrail. | Degraded | Frame pressure wandering. Air loss may only be the symptom. | Leak stage 1 active. Start-of-turn Hull -3. | None | REPAIR | SCAN gives a useful structural clue, but no direct stabilization. | Introduce persistent structural damage and mixed symptoms. |
| 6 | An internal voice repeats your last breath. / Deck plating answers half a second late. | Degraded | One of these sounds belongs to us. I am not certain which. | Signal Contamination begins. Leak escalates to stage 2 if unresolved. | Hull -4 | SCAN, or REPAIR if Leak is still active | REPAIR can still buy Hull briefly, but contamination remains. | First real triage turn: ambiguity, carryover damage, and immediate punishment. |
| 7 | Recycler cycle lengthening. / Sonar return repeats at impossible distance. | Degraded | Load is slipping between circuits. The echo may be borrowing it. | Power Bleed stage 1 begins. Signal Contamination may still be active. Start-of-turn Oxygen -3. | Oxygen -4 | REROUTE | SCAN may clarify load irregularity, but usually too weak to justify cost. | Push oxygen pressure and overlapping symptoms. |
| 8 | Aux relay housing too hot to touch. / Aft knocking syncs with fan slowdown. | Degraded | Quiet may preserve what remains. | Power Bleed escalates to stage 2 if unresolved. Signal Contamination may still be active. Start-of-turn Oxygen -5. | Battery -4 | REROUTE | SILENT is an atmospheric bait that may reduce Threat slightly, but life-support remains the real issue. | Intentional AI misread during life-support panic plus one authored battery shock. |
| 9 | Outer hull contact repeats in your own rhythm. / Channel opens before you touch it. | Corrupted | Answer softly. It already knows the loud parts. | Pursuit stage 1 begins. Start-of-turn Threat +5. If Contamination still active, apply extra Threat +3 once. | Threat +6 | SILENT, SCAN only if contamination still active and risk is worth it | SCAN can clear contamination if present, but does not stop the pursuit penalty. | Start the final oppressive arc and punish greed harder. |
| 10 | Aft plates bow inward, then release. / Two knocks answer the pump cycle. | Corrupted | Mend the shape. Do not feed the sound. | Pursuit stage 1 continues. Start-of-turn Threat +5. Structural-feeling symptom is a feint. | Threat +6 | SILENT | REPAIR gives small Hull relief, but the knocking keeps pace and Threat still rises. | Deliberately tempt REPAIR during a pursuit turn without making the turn feel arbitrary. |
| 11 | Every active line carries a second breathing pattern. / Distance to contact: unchanged. | Corrupted | Keep the air moving. Keep it from settling. | Pursuit escalates to stage 2. Start-of-turn Threat +8. | Threat +8 | SILENT | REROUTE gives a brief Oxygen bump, but the second breathing pattern remains and Threat still spikes. | Escalate pressure and deliberately misdirect toward REROUTE. |
| 12 | Impact pattern matches internal footfall. / External latch pressure increasing. | Corrupted | If we stop hearing it, it will hear us first. | Pursuit stage 2 continues. Start-of-turn Threat +8. | Threat +8 | SILENT | REPAIR or REROUTE may still steady one failing resource, but neither prevents the final external pressure. | End on sustained pressure rather than clarity. |

---

## 8. Turn Notes and Resolution Flags

### Turns 1 to 4: readable tutorial pass

The player learns all four actions in a controlled order:

1. REPAIR
2. SILENT
3. SCAN
4. REROUTE

These turns should be readable and low-ambiguity, but the AI should not literally tell the player what button to press.

### Turn 5

- Set `leak_stage = 1` before start-of-turn drains.
- Strong action: `REPAIR`.
- `SCAN` should reveal a useful structural clue, but should not clear the condition.
- `SILENT` may slightly reduce Threat if desired by your action model, but it should feel irrelevant here.
- If the player does not use `REPAIR`, set `leak_stage = 2` for Turn 6.

### Turn 6

- Set `signal_contamination_active = true` before readouts.
- If `leak_stage` is still active, apply its start-of-turn drain before showing text.
- Acute penalty: `Hull -4` unless the player gets a strong match.
- Strong action is normally `SCAN`, but unresolved Leak should still hurt enough that `REPAIR` feels tempting.
- Successful `SCAN` clears `signal_contamination_active` at end of turn.
- `REPAIR` on this turn should still restore some Hull, but it must not clear contamination.
- If `leak_stage` remains unresolved after this turn, clear the flag anyway and keep only the damage already taken. Do not let the Leak arc continue past Turn 6.

### Turn 7

- Set `power_bleed_stage = 1` before start-of-turn drains.
- Strong action: `REROUTE`.
- Acute penalty: `Oxygen -4` unless the player gets a strong match.
- If `signal_contamination_active` is still true, one readout or implication should be false.
- `SCAN` should provide only partial confirmation here and should not feel like the best play unless the player is still obsessing over contamination.
- If the player does not use `REROUTE`, set `power_bleed_stage = 2` for Turn 8.

### Turn 8

- If `power_bleed_stage` is active, apply its drain before text.
- AI line is intentionally misleading here.
- Strong action remains `REROUTE`.
- Acute penalty: `Battery -4` unless the player gets a strong match.
- `SILENT` may reduce Threat a little on a partial, but should clearly fail to solve the actual life-support problem.
- If `signal_contamination_active` is still true, SCAN may return corrupted or incomplete data.
- Clear `power_bleed_stage` after this turn whether solved or not. Keep the damage already applied.

### Turn 9

- Set `pursuit_stage = 1` before start-of-turn drains.
- If `signal_contamination_active` is still true at start of turn, apply an extra one-time `Threat +3`, then keep contamination active unless the player clears it with SCAN.
- Strong action is `SILENT`.
- Acute penalty: `Threat +6` unless the player gets a strong match.
- `SCAN` is still available, but should feel like a risky greed play rather than the obvious answer.
- If `SCAN` is used and contamination is active, it may clear contamination, but the player should still suffer the acute pursuit penalty unless your action logic explicitly grants only a partial interaction.

### Turn 10

- Pursuit remains the real problem.
- Structural-feeling text exists specifically to bait `REPAIR`.
- Strong action: `SILENT`.
- Acute penalty: `Threat +6` unless the player gets a strong match.
- `REPAIR` should give a small but real Hull benefit on this turn.
- The aftermath should make it clear that the player stabilized the plates, but failed to address what was following them.

### Turn 11

- Set `pursuit_stage = 2` before start-of-turn drains.
- AI line should sound persuasive enough that `REROUTE` feels plausible.
- Strong action: `SILENT`.
- Acute penalty: `Threat +8` unless the player gets a strong match.
- `REROUTE` should give a brief Oxygen benefit on this turn, but the external danger remains unaffected.
- This is a costly partial-success turn, not a dead-null turn.

### Turn 12

- Pursuit remains active until rescue.
- Strong action: `SILENT`.
- Acute penalty: `Threat +8` unless the player gets a strong match.
- Wrong late actions may still steady one resource briefly, but should not interrupt the final pressure arc.
- End on suppression, not resolution.

---

## 9. Recommended SCAN Output Table

These lines are optional implementation helpers. Use them if you want SCAN to feel authored instead of generic.

| Turn | If SCAN is used | Result Type |
| --- | --- | --- |
| 3 | Voice print mismatch. Internal source not confirmed. | Useful |
| 5 | Pressure differential isolated near the forward seam. | Useful but narrow |
| 6 | Archive mismatch detected. Something is reusing the channel. | High-value / useful |
| 7 | Auxiliary bus load irregularity detected. Echo source unresolved. | Partial |
| 8 | Diagnostic confidence degraded. Fault origin not isolated. | Corrupted / partial |
| 9 | External contact confirmed. Channel state remains unreliable. | Risky but useful if contamination persists |
| 10 | Structural strain reduced locally. Rhythm source unchanged. | Low-value partial |
| 11 | Airflow variance corrected. Second pattern persists across all lines. | Low-value partial |
| 12 | Contact remains outside. Pattern matching has become non-local. | Corrupted |

---

## 10. Recommended Aftermath Lines

Use terse aftermath instead of correctness labels. These are optional helpers for preserving dread.

### General rule

The text should imply that the player affected the situation, but did not make it safe.

### Specific costly-partial aftermaths

- **Turn 6 REPAIR instead of SCAN:** `The plating holds. The voice does not stop.`
- **Turn 8 bad SILENT:** `The knocking softens. The recycler still slips.`
- **Turn 9 bad SCAN:** `The channel narrows. The contact closes anyway.`
- **Turn 10 bad REPAIR:** `The plates settle. The knocking keeps pace.`
- **Turn 11 bad REROUTE:** `Airflow improves for a moment. The second breathing pattern remains.`
- **Turn 12 bad REPAIR or REROUTE:** `Something steadies inside. The latch pressure does not.`

### Additional tone examples

- `Pressure drop slowed.`
- `External contact fell back, then returned.`
- `Recycler output stabilizing.`
- `Channel contamination persists.`
- `The relay cools. The rhythm does not.`
- `Something outside adjusts to the silence.`

---

## 11. Implementation Notes

### Recommended data shape per turn

Each turn entry should contain:

- `turn`
- `readouts`
- `ai_state`
- `ai_line`
- `active_condition_changes`
- `acute_penalty`
- `strong_action`
- `optional_partial_outcomes`
- `optional_scan_result`
- `optional_aftermath_lines`
- `purpose_note`

### Important implementation rule

Do not shuffle this deck in the MVP.

### Important presentation rule

Do not surface `STRUCTURAL`, `PURSUIT`, `POWER`, or `CONTAMINATION` labels to the player after Turn 4.

### Important tuning rule

On late bait turns, prefer authored partial outcomes over a generic all-or-nothing wrong-action result.

---

## 12. Build Discipline Note

This revision does **not** add new systems.

It only changes authored resolution behavior and wording priorities.

Do not add any of the following during the hackathon unless the full 12-turn run is already fully playable and tuned once:

- flicker effects
- text delay effects
- extra reactive branches
- dynamic AI trust logic
- procedural event variants
- ambient polish layers

If time remains after the run is complete, add polish last.

---

## 13. Reference Tuning Notes

This version is intentionally harsher than a readable puzzle game, but slightly less binary than a pure fail-state trap.

### Expected feel

- Turns 1 to 4: readable
- Turns 5 to 8: tense and overlapping
- Turns 9 to 12: oppressive and hard to read cleanly

### Sanity target

A competent run should often look bad by the end:

- low oxygen
- strained battery
- damaged hull
- high but survivable threat

The player should often feel that they chose against the wrong fear, but still bought a few seconds somewhere else.

That is the intended mood.
