# Deep Sea Horror Terminal Game

## 12-Turn Event Deck v6.0

**Companion direction for Hackathon MVP Spec v5.0, revised for bounded LLM scene narration, one-query-per-turn interaction, costly partial successes, and deterministic action resolution**

This document defines a revised 12-turn sequence for the MVP.
The run is still fixed and should be implemented as authored data, not generated procedurally.

This revision makes four intentional changes:

- each turn now defines **scene facts for LLM narration**, not just static readout lines
- the player may ask **one brief in-fiction question per turn** before committing
- commitment input is still collapsed into the same **4 canonical actions**
- the LLM may deepen atmosphere, but it must never own the rules

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
- Each turn may answer **one** brief player query from exposed facts only.
- Query answers must not reveal the hidden strong action.

---

## 2. LLM Scene and Query Rules

### Scene generation rule

For each turn, the LLM should generate a short scene block using:

- required scene facts
- misleading facts
- carryover condition facts
- AI line seed

The generated block should feel specific, but must not invent new mechanical truth.

### Query handling rule

Each turn may answer one player question.

The answer should:

- be brief
- stay in-world
- reuse currently exposed facts
- preserve uncertainty
- stop before the turn becomes a conversation loop

### Diagnostic boundary rule

If a player asks for diagnosis rather than description, the answer should stay uncertain unless the player commits to **SCAN**.

Examples of diagnostic questions:

- `is this coming from outside?`
- `what system is actually failing?`
- `is the voice real?`
- `where is the signal originating?`

These questions may receive suggestive language, but not hidden truth.

### Fallback rule

Each turn must define fallback scene lines and fallback aftermath lines so the run remains playable with no successful LLM calls.

---

## 3. AI State Schedule

- **Turns 1 to 4:** Stable
- **Turns 5 to 8:** Degraded
- **Turns 9 to 12:** Corrupted

---

## 4. Persistent Condition Arc Overview

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
- **Effect:** one scene implication, query answer implication, or AI meaning becomes unreliable while active
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

## 5. Acute Penalty Schedule

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

## 6. Commitment Classification Rule

The player may type many phrasings, but engine resolution still accepts only one of four canonical actions.

### Useful commitment examples

- **SCAN:** inspect, check, trace, verify, isolate the signal, examine the channel
- **REPAIR:** patch, brace, seal, reinforce, weld, stabilize the seam
- **SILENT:** shut down, go quiet, hold still, damp output, suppress sound
- **REROUTE:** redirect power, reroute life support, shift load, move current, rebalance circuits

### Important guardrail

The LLM may paraphrase player intent, but it must not create hybrid actions such as:

- scan and reroute together
- repair while running silent as one choice
- interrogate the AI as a fifth action

If the player types a mixed or unclear command, the system should fall back rather than improvise a new rules path.

---

## 7. Turn Deck Overview Table

| Turn | AI State | Hidden State (dev only) | Acute Penalty | Strong Action | Query Behavior | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Stable | None | None | REPAIR | brief environmental clarification only | Teach REPAIR and basic free-input flow. |
| 2 | Stable | None | None | SILENT | brief sound / proximity clarification only | Teach SILENT and external threat. |
| 3 | Stable | None | None | SCAN | diagnostic questions stay uncertain unless committed | Teach SCAN as diagnosis, not generic questioning. |
| 4 | Stable | None | None | REROUTE | system-status questions may describe recycler strain | Teach REROUTE and battery cost. |
| 5 | Degraded | Leak stage 1 active | None | REPAIR | query may expose structural texture, not certainty | Introduce persistent structural damage and mixed symptoms. |
| 6 | Degraded | Signal Contamination begins; Leak may persist | Hull -4 | SCAN, or REPAIR if Leak still active | query answer may itself feel suspect | First real triage turn with ambiguity and punishment. |
| 7 | Degraded | Power Bleed stage 1 begins; contamination may persist | Oxygen -4 | REROUTE | query may describe load symptoms, not isolate source | Push oxygen pressure and overlapping signals. |
| 8 | Degraded | Power Bleed may escalate; contamination may persist | Battery -4 | REROUTE | query may reinforce the wrong fear if contamination remains | Intentional AI misread during life-support panic. |
| 9 | Corrupted | Pursuit stage 1 begins; contamination may still persist | Threat +6 | SILENT, SCAN only as risky greed play | query must not puncture pursuit ambiguity | Start the final oppressive arc. |
| 10 | Corrupted | Pursuit stage 1 continues | Threat +6 | SILENT | query may emphasize local structure while real danger remains pursuit | Tempt REPAIR without making the turn feel random. |
| 11 | Corrupted | Pursuit escalates to stage 2 | Threat +8 | SILENT | query may describe airflow and second breathing pattern | Escalate pressure and misdirect toward REROUTE. |
| 12 | Corrupted | Pursuit stage 2 continues | Threat +8 | SILENT | query should heighten dread, not explain it | End on suppression rather than clarity. |

---

## 8. Per-Turn Scene Packets and Query Notes

Each turn below defines the authored facts the LLM may use. The LLM should render them flexibly, but it must stay inside these bounds.

### Turn 1

**AI state:** Stable  
**Hidden state:** None  
**Acute penalty:** None  
**Strong action:** REPAIR

**Required scene facts**
- localized hull stress warning
- frame seam under pressure
- interior vibration concentrated in one place

**Misleading facts**
- none beyond mild generic tension

**Query answer facts**
- the sub feels stable except for one stressed seam
- no external visibility
- the vibration is local, not global

**Diagnostic boundary**
- do not say `this is a structural event`
- do not say `repair is correct`

**Commitment hint examples**
- `patch the seam`
- `brace that section`
- `seal the frame`

**Fallback scene lines**
- `Localized hull stress warning.`
- `A narrow vibration runs through the frame seam.`
- `AI: Localized hull stress detected at frame seam.`

**Fallback aftermath tone**
- `The plates settle a little.`
- `The seam stops answering back.`

---

### Turn 2

**AI state:** Stable  
**Hidden state:** None  
**Acute penalty:** None  
**Strong action:** SILENT

**Required scene facts**
- metallic scraping along the outer hull
- something outside is closing or keeping pace
- the noise reacts to movement or systems output

**Misleading facts**
- the scraping can briefly sound like loose internal metal

**Query answer facts**
- the sound is outside-facing in feel, not visibly confirmed
- the motion is intermittent, not a clean impact sequence
- the compartment itself remains physically intact

**Diagnostic boundary**
- do not say what is outside
- do not imply that shutting down will definitely work

**Commitment hint examples**
- `shut down everything loud`
- `go quiet`
- `hold still and damp output`

**Fallback scene lines**
- `Metallic scraping drags along the outer hull.`
- `Something keeps pace just beyond the plates.`
- `AI: External acoustic contact closing on outer hull.`

**Fallback aftermath tone**
- `The sound falls back, then returns farther off.`
- `The hull stops answering every movement.`

---

### Turn 3

**AI state:** Stable  
**Hidden state:** None  
**Acute penalty:** None  
**Strong action:** SCAN

**Required scene facts**
- garbled crew voice on an internal channel
- signal origin unclear
- channel integrity uncertain

**Misleading facts**
- voice phrasing feels familiar enough to tempt trust

**Query answer facts**
- the voice is audible but not locatable from exposed facts
- the channel opens irregularly
- no visual confirmation accompanies the voice

**Diagnostic boundary**
- any question like `is it real?` or `where is it coming from?` should remain uncertain
- meaningful diagnosis is gated behind SCAN

**Commitment hint examples**
- `trace the channel`
- `check where that voice is coming from`
- `scan the signal`

**Fallback scene lines**
- `A garbled crew voice stutters across an internal channel.`
- `The message does not hold one shape long enough to trust.`
- `AI: Signal origin unclear. Channel integrity uncertain.`

**Fallback aftermath tone**
- `Voice print mismatch.`
- `The channel narrows, but does not reassure.`

---

### Turn 4

**AI state:** Stable  
**Hidden state:** None  
**Acute penalty:** None  
**Strong action:** REROUTE

**Required scene facts**
- oxygen recycler stutter
- life-support load instability
- electrical strain spreading across one subsystem

**Misleading facts**
- the hardware may sound physically damaged even though the primary danger is system load

**Query answer facts**
- airflow remains present but uneven
- the issue feels cyclical, not catastrophic yet
- the recycler is slipping under load

**Diagnostic boundary**
- do not reveal exact subsystem failure class
- do not say battery-for-oxygen tradeoff explicitly

**Commitment hint examples**
- `reroute life support`
- `shift load to keep air moving`
- `move power into the recycler`

**Fallback scene lines**
- `The oxygen recycler stutters mid-cycle.`
- `Load drift spreads through life support.`
- `AI: Life-support instability spreading across recycler load.`

**Fallback aftermath tone**
- `Airflow evens out for a moment.`
- `The recycler catches, then keeps breathing.`

---

### Turn 5

**AI state:** Degraded  
**Hidden state:** Leak stage 1 active; start-of-turn Hull -3  
**Acute penalty:** None  
**Strong action:** REPAIR

**Required scene facts**
- forward seam ticks under load
- condensation gathers beneath the port handrail
- pressure feels local but the air hints at broader instability
- active leak arc should appear in prose

**Misleading facts**
- condensation can suggest oxygen or temperature trouble instead of hull trouble

**Query answer facts**
- the ticking clusters near the forward seam
- moisture is accumulating inside, but source remains indirect
- the compartment feels tighter, not yet openly flooding

**Diagnostic boundary**
- do not confirm `leak`
- do not say `repair now or it escalates`

**Commitment hint examples**
- `seal the forward seam`
- `brace the frame`
- `patch the pressure point`

**Fallback scene lines**
- `Forward seam ticks under load.`
- `Condensation gathers beneath the port handrail.`
- `AI: Frame pressure wandering. Air loss may only be the symptom.`

**Fallback aftermath tone**
- `Pressure drop slowed.`
- `The seam still watches the room.`

---

### Turn 6

**AI state:** Degraded  
**Hidden state:** Signal Contamination begins; Leak escalates to stage 2 if unresolved  
**Acute penalty:** Hull -4  
**Strong action:** SCAN, or REPAIR if Leak is still active and the player accepts contamination risk

**Required scene facts**
- an internal voice repeats the player's last breath
- deck plating answers half a second late
- contamination now affects one implication or query answer
- unresolved leak pressure should still be felt if present

**Misleading facts**
- the plating response makes REPAIR feel tempting
- the repeated breath makes the AI feel less trustworthy

**Query answer facts**
- something in the channel is reusing recent sound
- the room feels slightly out of sync with the player's own movement
- if leak persists, local structure still feels stressed

**Diagnostic boundary**
- query answers may themselves feel suspect
- do not confirm whether the voice is internal, external, or recorded unless the player commits to SCAN

**Commitment hint examples**
- `trace the channel`
- `check the archive mismatch`
- `brace the plates` (tempting partial)

**Fallback scene lines**
- `An internal voice repeats your last breath.`
- `Deck plating answers half a second late.`
- `AI: One of these sounds belongs to us. I am not certain which.`

**Fallback aftermath tone**
- strong SCAN: `Archive mismatch detected. Something is reusing the channel.`
- bad REPAIR: `The plating holds. The voice does not stop.`

---

### Turn 7

**AI state:** Degraded  
**Hidden state:** Power Bleed stage 1 begins; contamination may still be active; start-of-turn Oxygen -3  
**Acute penalty:** Oxygen -4  
**Strong action:** REROUTE

**Required scene facts**
- recycler cycle lengthening
- sonar return repeats at impossible distance
- load drift touches life support
- if contamination persists, one implication should point the wrong way

**Misleading facts**
- the echo strongly tempts SCAN
- the impossible distance makes the scene feel external rather than systemic

**Query answer facts**
- airflow timing is lengthening
- the repeated return feels wrong but not necessarily primary
- the room is breathing less efficiently than before

**Diagnostic boundary**
- do not isolate the echo as the root cause
- questions about the echo should remain unresolved unless the player commits to SCAN, which is still not the best play here

**Commitment hint examples**
- `reroute support power`
- `shift load into life support`
- `move current off the failing bus`

**Fallback scene lines**
- `Recycler cycle lengthening.`
- `A sonar return repeats at impossible distance.`
- `AI: Load is slipping between circuits. The echo may be borrowing it.`

**Fallback aftermath tone**
- `Recycler output stabilizing.`
- `The echo does not explain itself.`

---

### Turn 8

**AI state:** Degraded  
**Hidden state:** Power Bleed may escalate to stage 2; contamination may still be active; start-of-turn Oxygen -5 if escalated  
**Acute penalty:** Battery -4  
**Strong action:** REROUTE

**Required scene facts**
- auxiliary relay housing is too hot to touch
- aft knocking syncs with fan slowdown
- life-support strain is real and worsening
- the AI line should misdirect toward quiet

**Misleading facts**
- the knocking makes SILENT feel plausible
- contamination may make the misleading interpretation feel more convincing

**Query answer facts**
- the fan is lagging with the knocking rhythm
- the relay heat is immediate and physical
- the compartment feels starved rather than breached

**Diagnostic boundary**
- do not say the relay heat is the whole answer
- do not say `quiet is wrong`

**Commitment hint examples**
- `move power off the hot relay`
- `reroute around the failing bus`
- `stabilize life support load`
- `go quiet` (tempting bad input)

**Fallback scene lines**
- `Aux relay housing too hot to touch.`
- `Aft knocking syncs with fan slowdown.`
- `AI: Quiet may preserve what remains.`

**Fallback aftermath tone**
- bad SILENT: `The knocking softens. The recycler still slips.`
- strong REROUTE: `The relay cools slightly. The air keeps moving.`

---

### Turn 9

**AI state:** Corrupted  
**Hidden state:** Pursuit stage 1 begins; contamination may still persist; start-of-turn Threat +5; contamination adds one-time Threat +3 if still active  
**Acute penalty:** Threat +6  
**Strong action:** SILENT; SCAN only as a risky greed play if contamination still active

**Required scene facts**
- outer hull contact repeats in the player's own rhythm
- a channel opens before the player touches it
- pursuit pressure is now the real danger
- contamination may still color interpretation

**Misleading facts**
- open channel tempts SCAN
- matching rhythm makes the threat feel informational rather than external

**Query answer facts**
- the contact is pacing response and movement
- the channel behavior is premature and unwelcome
- the compartment feels listened to

**Diagnostic boundary**
- do not reveal whether contamination is still active
- do not explain that SILENT is correct
- if asked `what wants me?`, stay atmospheric and uncertain

**Commitment hint examples**
- `kill the noise`
- `shut everything down and hold still`
- `trace the channel` (risky greed play)

**Fallback scene lines**
- `Outer hull contact repeats in your own rhythm.`
- `The channel opens before you touch it.`
- `AI: Answer softly. It already knows the loud parts.`

**Fallback aftermath tone**
- bad SCAN: `The channel narrows. The contact closes anyway.`
- strong SILENT: `Something outside adjusts to the silence.`

---

### Turn 10

**AI state:** Corrupted  
**Hidden state:** Pursuit stage 1 continues; start-of-turn Threat +5  
**Acute penalty:** Threat +6  
**Strong action:** SILENT

**Required scene facts**
- aft plates bow inward then release
- two knocks answer the pump cycle
- pursuit remains the real danger
- structural-feeling symptom is a deliberate feint

**Misleading facts**
- the bowing plates make REPAIR feel urgent and plausible

**Query answer facts**
- local structure is under strain, but the rhythm is interactive
- the knocks answer ongoing system behavior rather than random stress
- the room feels watched through its own machinery

**Diagnostic boundary**
- do not say the structure is secondary
- do not identify pursuit directly

**Commitment hint examples**
- `go quiet`
- `damp the pump and hold still`
- `brace the plates` (costly partial)

**Fallback scene lines**
- `Aft plates bow inward, then release.`
- `Two knocks answer the pump cycle.`
- `AI: Mend the shape. Do not feed the sound.`

**Fallback aftermath tone**
- bad REPAIR: `The plates settle. The knocking keeps pace.`
- strong SILENT: `The rhythm loses one step, then circles wider.`

---

### Turn 11

**AI state:** Corrupted  
**Hidden state:** Pursuit escalates to stage 2; start-of-turn Threat +8  
**Acute penalty:** Threat +8  
**Strong action:** SILENT

**Required scene facts**
- every active line carries a second breathing pattern
- distance to contact remains unchanged
- pursuit escalation is severe
- the AI line should make REROUTE feel plausible

**Misleading facts**
- breathing imagery strongly tempts an oxygen-centered interpretation

**Query answer facts**
- the second pattern rides across all active systems
- airflow is present but wrong in feel
- the outside presence is not retreating

**Diagnostic boundary**
- do not say `this is not an oxygen problem`
- do not reveal that REROUTE is only a costly partial

**Commitment hint examples**
- `hold silent`
- `cut output and wait`
- `keep the air moving` (tempting bad input)

**Fallback scene lines**
- `Every active line carries a second breathing pattern.`
- `Distance to contact: unchanged.`
- `AI: Keep the air moving. Keep it from settling.`

**Fallback aftermath tone**
- bad REROUTE: `Airflow improves for a moment. The second breathing pattern remains.`
- strong SILENT: `The extra breath thins, but does not forgive.`

---

### Turn 12

**AI state:** Corrupted  
**Hidden state:** Pursuit stage 2 continues; start-of-turn Threat +8  
**Acute penalty:** Threat +8  
**Strong action:** SILENT

**Required scene facts**
- impact pattern matches internal footfall
- external latch pressure is increasing
- the final turn should feel like internal and external boundaries are collapsing
- pursuit remains unresolved until rescue

**Misleading facts**
- latch pressure tempts REPAIR
- internal footfall echo can tempt REROUTE or SCAN as a search for explanation

**Query answer facts**
- something outside is testing entry pressure
- interior movement no longer feels safely separate from exterior contact
- the vessel feels one sound away from being opened

**Diagnostic boundary**
- do not explain what the contact is
- do not reveal that suppression, not repair, is the final answer

**Commitment hint examples**
- `hold quiet`
- `cut everything and stay still`
- `secure the latch` (tempting bad input)

**Fallback scene lines**
- `Impact pattern matches internal footfall.`
- `External latch pressure increasing.`
- `AI: If we stop hearing it, it will hear us first.`

**Fallback aftermath tone**
- bad REPAIR or REROUTE: `Something steadies inside. The latch pressure does not.`
- strong SILENT: `The pressure waits at the threshold. Then the rescue ping arrives.`

---

## 9. Recommended Query Response Guidance Table

Use these as tone guides, not as literal mandatory lines.

| Turn | Query theme | Response guidance |
| --- | --- | --- |
| 1 | `what is around me?` | emphasize one stressed seam and a mostly intact compartment |
| 2 | `what do i hear?` | emphasize scraping outside and reaction to movement |
| 3 | `where is the voice coming from?` | admit uncertainty and imply SCAN-level diagnosis is needed |
| 4 | `what changed?` | describe uneven airflow and recycler strain |
| 5 | `where is the pressure worst?` | suggest the forward seam without naming the hidden class |
| 6 | `is that my voice?` | stay uncertain and contaminated in tone |
| 7 | `is the echo outside?` | refuse clean isolation; describe both echo and load drift |
| 8 | `what is failing first?` | describe heat and fan slowdown without declaring the true subsystem |
| 9 | `what is around me?` | emphasize pacing contact and invasive channel behavior |
| 10 | `what is making the knocks?` | describe interactive rhythm, not the answer |
| 11 | `why does it sound like breathing?` | describe cross-system pattern, preserve dread |
| 12 | `what is at the latch?` | describe pressure and testing behavior, never identify the entity |

---

## 10. Recommended SCAN Output Table

These remain optional implementation helpers.

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

## 11. Recommended Aftermath Lines

Use terse aftermath instead of correctness labels.

### Specific costly-partial aftermaths

- **Turn 6 REPAIR instead of SCAN:** `The plating holds. The voice does not stop.`
- **Turn 8 bad SILENT:** `The knocking softens. The recycler still slips.`
- **Turn 9 bad SCAN:** `The channel narrows. The contact closes anyway.`
- **Turn 10 bad REPAIR:** `The plates settle. The knocking keeps pace.`
- **Turn 11 bad REROUTE:** `Airflow improves for a moment. The second breathing pattern remains.`
- **Turn 12 bad REPAIR or REROUTE:** `Something steadies inside. The latch pressure does not.`

### General tone rule

The text should imply that the player affected the situation, but did not make it safe.

---

## 12. Implementation Notes

### Recommended data shape per turn

Each turn entry should contain:

- `turn`
- `ai_state`
- `ai_line_seed`
- `required_scene_facts`
- `misleading_facts`
- `query_answer_facts`
- `forbidden_claims`
- `active_condition_changes`
- `acute_penalty`
- `strong_action`
- `optional_partial_outcomes`
- `optional_scan_result`
- `fallback_scene_lines`
- `fallback_query_lines`
- `fallback_aftermath_lines`
- `purpose_note`

### Important implementation rule

Do not shuffle this deck in the MVP.

### Important presentation rule

Do not surface `STRUCTURAL`, `PURSUIT`, `POWER`, or `CONTAMINATION` labels to the player after Turn 4.

### Important interaction rule

The player may ask one in-fiction question per turn, but the response must not become a hidden hint system that bypasses SCAN or deck-authored ambiguity.

---

## 13. Build Discipline Note

This revision does **not** add open-ended LLM game-mastering.

It only adds:

- bounded scene narration
- bounded query responses
- deterministic commitment classification
- authored fallback text

Do not add any of the following during the hackathon unless the full 12-turn run is already fully playable and tuned once:

- unlimited back-and-forth dialogue per turn
- dynamic AI trust logic
- procedural truth generation
- extra reactive branches
- ambient polish layers before fallback mode works

---

## 14. Reference Tuning Notes

This version should feel:

- Turns 1 to 4: readable and slightly exploratory
- Turns 5 to 8: tense, denser, and increasingly contradictory
- Turns 9 to 12: oppressive, invasive, and hard to read cleanly

### Sanity target

A competent run should often look bad by the end:

- low oxygen
- strained battery
- damaged hull
- high but survivable threat

The player should feel that they had room to ask what the room was doing, but not enough room to talk their way out of the turn.
