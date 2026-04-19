# Deep Sea Horror Terminal Game

## Hackathon MVP Spec v5.0

**Document Type:** Hackathon MVP game spec  
**Target Build Window:** 18 hours  
**Target Platform:** Desktop terminal or browser-based terminal UI  
**Genre:** Text-based survival horror  
**Target Session Length:** 8 to 15 minutes

---

## 1. High Concept

**One-sentence pitch**  
A 12-turn terminal survival horror game where the player manages a failing deep-sea submarine, types short in-fiction commands or questions, and survives long enough for rescue while an increasingly untrustworthy AI turns every piece of language into a possible trap.

**Player fantasy**  
The player is trapped inside a damaged vessel with no visual contact with the outside world. They survive by reading partial system data, distorted comms, recurring external contact, and suspect AI guidance, then expressing intent in their own words inside the fiction.

---

## 2. Design Goals

This version of the spec keeps the game hackathon-sized, but adds a bounded LLM layer to deepen textual immersion without handing game logic to the model.

### Primary goals

1. **Horror-first reading**  
   The player should spend time reading and interpreting unstable language, not just pressing one of four obvious buttons.

2. **Expressive but bounded input**  
   The player should be able to type natural-language actions and brief in-fiction questions, but the underlying action space must remain small and testable.

3. **Deterministic rules underneath expressive prose**  
   The engine, not the LLM, owns all hidden state, resource math, strong/partial/wrong resolution, and win/loss checks.

4. **Fast implementation**  
   The build must still be finishable within the hackathon by keeping the turn deck fixed and the LLM interface tightly constrained.

5. **Difficulty over readability**  
   The game is allowed to feel harsh, ambiguous, and occasionally unfair, as long as the underlying authored rules are stable enough to learn.

---

## 3. Non-Negotiable Scope

This is the exact MVP scope.

### Included

- 1 intro screen
- 1 gameplay loop
- 12 fixed turns
- 4 canonical player actions
- bounded free-text player input
- 1 brief in-fiction query response per turn
- 4 visible resources
- 4 internal problem classes
- 3 authored persistent condition arcs plus 1 contamination overlay arc
- mixed-symptom readouts after the tutorial
- authored acute penalties on most late turns
- 3 AI reliability states
- LLM-generated scene text grounded in authored turn facts
- deterministic intent classification into the 4 canonical actions
- authored fallback text and explicit action selection if LLM output fails
- 1 win ending
- 1 generic loss ending
- terminal-style HUD and turn readout

### Explicitly cut

- unbounded multi-turn conversation within a single turn
- LLM-owned game logic
- LLM-authored hidden state changes
- procedural event generation that changes turn order or core outcomes
- branching narrative routes
- map navigation
- inventory systems
- crew simulation
- combat
- repair minigames
- save/load
- real-time typing pressure
- multiple endings
- lore log collection systems
- extra UI modes beyond the main terminal screen
- probabilistic AI truth simulation
- large dynamic status systems beyond the authored conditions listed in this spec

### Scope rule

If a feature is not required to make the 12-turn run playable from start to finish with deterministic resolution underneath expressive text, it is out of scope.

---

## 4. Core Experience

The game creates tension through:

- low-information decision making
- accumulating passive pressure
- persistent multi-turn resource drains
- authored acute penalties on high-pressure turns
- mixed symptoms that point toward more than one possible action
- brief player questions that can reveal texture but not guaranteed truth
- an AI that shifts from helpful to incomplete to sometimes wrong
- concise, high-contrast terminal presentation
- player-authored intent expressed in natural language

The player should feel trapped, underinformed, and increasingly behind, while also feeling like they are speaking inside the world rather than clicking obvious menu verbs.

---

## 5. Build Strategy

This MVP should still be built as a **fully scripted 12-turn run**, not a simulation sandbox.

### Why

A fixed run is easier to:

- implement
- tune
- test
- polish
- demo repeatedly during a hackathon
- keep deterministic even with an LLM presentation layer

### Implementation rule

Use a predefined turn deck stored as data.  
Do not randomize event order in the MVP.

Persistent conditions are authored in the deck.  
Do not build a general procedural status engine.

Acute penalties are authored in the deck.  
Do not build a generic reaction-combo system.

The LLM may render the scene and classify input, but it must do so from structured engine state and authored turn facts only.

---

## 6. LLM Role and Boundaries

This version uses an LLM as a **presentation and intent layer**, not as the source of truth for rules.

### The LLM is responsible for

- generating atmospheric pre-action scene text from the current engine state and current turn packet
- generating brief in-fiction answers to player queries
- interpreting player free-text input into one of the 4 canonical actions or into a query classification
- generating post-resolution aftermath text from the deterministic engine result
- preserving AI voice and environmental tone

### The LLM is not responsible for

- determining hidden conditions
- deciding strong vs partial vs wrong resolution
- changing resources
- inventing new actions
- changing turn order
- changing authored condition arcs
- deciding win or loss
- revealing hidden truth that the engine has not exposed

### Validation rule

The engine only accepts two kinds of validated model output:

1. **classified input type**
   - `QUERY`
   - `COMMITMENT`

2. **canonical action label**
   - `SCAN`
   - `REPAIR`
   - `SILENT`
   - `REROUTE`

All resource changes and state transitions happen after deterministic engine resolution.

### Failure rule

If the LLM times out, fails validation, or returns unusable output, the game must fall back to:

- authored scene text
- authored aftermath text
- explicit action buttons or hotkeys

The run must remain fully playable without successful LLM output.

---

## 7. Win and Loss Conditions

### Win condition

Survive through the end of **Turn 12**.

Each turn displays:

`RESCUE ETA: X TURNS`

### Loss conditions

The player loses immediately if any of the following are true after resolution:

- **Oxygen = 0**
- **Hull = 0**
- **Threat = 100**

### Important battery rule

**Battery reaching 0 is not an instant loss.**

Battery only gates battery-powered actions.

---

## 8. Starting Values

Lock the starting values now so implementation and tuning stay stable.

- **Oxygen:** 42
- **Battery:** 40
- **Hull:** 50
- **Threat:** 18

These values assume persistent drains, authored acute penalties, one brief query per turn at most, and some wrong guesses.

---

## 9. Core Resources

The player always sees four resources.

- **Oxygen**: 0 to 100
- **Battery**: 0 to 100
- **Hull**: 0 to 100
- **Threat**: 0 to 100

### Threat stage labels

Threat is stored numerically but shown with a label.

- **0 to 19:** Distant
- **20 to 39:** Nearby
- **40 to 59:** Attached
- **60 to 79:** Breaching
- **80 to 100:** Inside

The HUD should show both the number and the label.

---

## 10. Internal Problem Classes

The game still uses four internal problem classes for implementation and balancing.

- **STRUCTURAL**
- **PURSUIT**
- **POWER**
- **CONTAMINATION**

### Important presentation rule

After the tutorial, these category labels are **not shown to the player**.  
The player only sees scene text, readouts, AI lines, resource changes, and terse aftermath.

---

## 11. AI Reliability System

The AI has three discrete states.

- **Stable**
- **Degraded**
- **Corrupted**

### MVP behavior

In this version:

- **Stable** AI is readable, but not an explicit answer key
- **Degraded** AI is incomplete, overconfident, or misses context
- **Corrupted** AI may be wrong, manipulative, or fixated on the wrong symptom

### Turn schedule

- **Turns 1 to 4:** Stable
- **Turns 5 to 8:** Degraded
- **Turns 9 to 12:** Corrupted

### Important scope rule

Do **not** implement a probabilistic hidden trust model.  
AI reliability is authored per turn in the deck.

---

## 12. Player Actions

The player has exactly four canonical actions.

Each action must keep one clear identity.

### 12.1 SCAN

**Role:** diagnose under uncertainty  
**Cost:** Battery -4

**Base effect:**

- reveals one additional diagnostic line
- may clarify the current condition, partially clarify it, or return corrupted data depending on the authored turn

**Strongest against:** **CONTAMINATION**

**Special role:**

- can clear the Signal Contamination overlay on authored turns
- does **not** guarantee truth in late-game corrupted turns
- does **not** provide generic stat mitigation unless the deck explicitly says so
- should feel like a risky information play, not a truth button

### 12.2 REPAIR

**Role:** stabilize structural failure  
**Cost:** none

**Base effect:**

- **Hull +8** on a strong match
- **Hull +4** on a partial match

**Strongest against:** **STRUCTURAL** persistent conditions and acute hull pressure

### 12.3 SILENT

**Role:** reduce threat and suppress external attention  
**Cost:** none

**Base effect:**

- **Threat -8** on a strong match
- **Threat -4** on a partial match

**Strongest against:** **PURSUIT**

**Special role:**

- suppresses the current turn's Pursuit drain on a strong match
- does not permanently remove the final Pursuit arc

### 12.4 REROUTE

**Role:** preserve oxygen at battery cost  
**Cost:** Battery -8

**Base effect:**

- **Oxygen +8** on a strong match
- **Oxygen +4** on a partial match

**Strongest against:** **POWER** drains and acute life-support instability

### Canonical action rule

Player wording may vary, but the underlying action space remains exactly four actions.

- **SCAN = diagnose**
- **REPAIR = structure**
- **SILENT = threat / suppression**
- **REROUTE = oxygen / power**

No typed input should produce a fifth real action.

---

## 13. Input Model and Query Boundary

This version supports two input lanes.

### 13.1 Commitment input

The player types a natural-language action attempt.

Examples:

- `patch the seam`
- `check the channel`
- `kill the noise and hold still`
- `reroute life support`

The system must classify commitment input into exactly one canonical action.

### 13.2 Query input

The player types a brief in-fiction question.

Examples:

- `what is around me?`
- `what changed?`
- `what do i hear?`
- `what does the AI mean?`

The system may answer with a short scene-grounded response.

### Query rules

- The player may receive **at most one query response per turn**.
- Query responses must be **brief**.
- Query responses may only use **currently exposed facts** from the scene packet and active state.
- Query responses must not reveal hidden condition labels, strong actions, or future deck state.
- Query responses must not expand into open-ended dialogue.

### Diagnostic boundary rule

If a player question would require true diagnosis rather than descriptive narration, the response must either:

- remain uncertain, or
- require the player to commit to **SCAN** for meaningful diagnosis

### Anti-stall rule

After one answered query, the player must commit to an action.  
The game should not support indefinite pre-action questioning.

### Confidence fallback rule

If commitment input cannot be cleanly mapped to a canonical action with sufficient confidence, the game should:

1. show a short ambiguous-response line, and then
2. fall back to explicit action hotkeys or buttons for that turn

Do not start an unlimited clarification loop.

---

## 14. Passive Turn Pressure

At the start of every turn, apply:

- **Oxygen -2**
- **Threat +2**

### Important rule

Do **not** apply passive battery drain in the MVP.

Battery pressure should come from:

- SCAN cost
- REROUTE cost
- one or two authored battery shocks in the deck

---

## 15. Persistent Condition Model

This version keeps a small authored condition layer.

### Important scope rule

There is **not** a fully dynamic status system.  
Only the authored conditions in the fixed deck exist.

### Condition set

#### Leak

- structural condition
- start-of-turn drain while active: **Hull -3**
- escalated drain: **Hull -5**
- removed by **REPAIR**

#### Power Bleed

- power / life-support condition
- start-of-turn drain while active: **Oxygen -3**
- escalated drain: **Oxygen -5**
- removed by **REROUTE**

#### Pursuit

- external threat condition
- start-of-turn drain while active: **Threat +5**
- escalated drain: **Threat +8**
- strongly countered by **SILENT**
- cannot be permanently removed during the final arc

#### Signal Contamination

- information-corruption overlay
- no direct resource drain by default
- causes one or more scene lines, query answers, or AI implications to become unreliable
- removed by **SCAN** on authored turns

### Arc limits

- Only **4 authored condition arcs** exist in the MVP.
- Only **2 conditions** may be active at once.
- All condition behavior is authored in the deck.

---

## 16. Acute Penalty Model

This version keeps a second pressure layer on top of passive drain and persistent conditions.

### Definition

An **acute penalty** is a one-turn authored consequence attached to the current turn.

Examples:

- **Hull -4**
- **Oxygen -4**
- **Battery -4**
- **Threat +6**

### Purpose

Acute penalties make the current situation feel immediate even when a persistent condition is already active.

They should:

- increase fear
- punish hesitation and misreads
- prevent late turns from feeling solvable through slow optimization

### Scope rule

Do not create random acute penalties.  
Every acute penalty is authored per turn in the deck.

---

## 17. Resolution Model

This system must remain exact, small, and easy to implement even with free-text input.

### Phase order

1. Render current HUD state
2. Apply passive turn pressure
3. Apply any active persistent-condition drains
4. Build a structured scene packet from authored turn data and current engine state
5. Generate scene text from the scene packet or fall back to authored scene lines
6. Accept one player input
7. Classify the input as `QUERY` or `COMMITMENT`
8. If `QUERY`, generate one brief answer from exposed facts only, then return to input once
9. If `COMMITMENT`, classify input into one canonical action
10. Resolve the action against the authored current-turn logic
11. Apply or cancel the authored acute penalty based on result
12. Generate aftermath text from deterministic outcome or fall back to authored aftermath
13. Clamp values and check end state

### Strong match

- cancel the acute turn penalty if one is present
- apply the action's full base effect
- clear or suppress the relevant persistent condition if the deck says it can

### Partial match

- the acute penalty still applies
- apply **half** of the action's base effect, rounded down
- condition is not removed unless the deck explicitly says it is suppressed

### Wrong read

- the acute penalty still applies
- the action gives **no** base benefit except deck-authored exceptions
- battery costs are still paid for SCAN and REROUTE

### Design intent

The player should be punished for misreading the situation.  
The game is allowed to feel unfair as long as the rules are consistent enough to learn over repeated runs.

---

## 18. Scene Composition and Query Rules

After the tutorial, each turn should present a **layered scene packet** rather than only two isolated readouts.

### Late-turn scene composition target

A late-game turn should usually include:

- 1 direct symptom line
- 1 misleading or cross-signal line
- 1 carryover line from an active condition if present
- 1 AI line or paraphrase
- 1 contradictory or suspicious detail

This content may be rendered dynamically by the LLM, but it must come from authored turn facts.

### Scene packet fields

Each authored turn should define:

- `required_facts`
- `misleading_facts`
- `query_answer_facts`
- `forbidden_claims`
- `strong_action`
- `acute_penalty`
- `scan_result`
- `fallback_scene_lines`
- `fallback_aftermath_lines`

### Query-answer rule

Query answers should be descriptive, not adjudicative.

Good query response style:

- describe sound, motion, condensation, lighting, console behavior
- restate uncertainty in-world
- reveal texture

Bad query response style:

- name hidden condition classes
- recommend the correct action
- reveal strong-action truth
- expose future turn consequences

### SCAN boundary

Questions that amount to `tell me the actual diagnosis` must not reveal what SCAN is supposed to gate.

---

## 19. Tutorial Structure

The first four turns still teach the core verbs.

- **Turn 1:** readable structural problem -> teaches REPAIR
- **Turn 2:** readable external contact -> teaches SILENT
- **Turn 3:** readable false signal -> teaches SCAN
- **Turn 4:** readable life-support instability -> teaches REROUTE

### Tutorial update

The tutorial should also teach the shape of the free-input layer.

By the end of Turn 4, the player should understand that:

- they may phrase actions in their own words
- they may ask one brief in-fiction question per turn
- the system will not chat indefinitely
- SCAN is the real diagnostic commitment action

### Important rule

The AI should still **not** explicitly name the answer.

Do not use phrasing such as:

- `Recommend repair.`
- `Recommend silent running.`
- `Recommend active scan.`
- `Recommend power reroute.`

The player should learn through symptoms, prose, and aftermath.

---

## 20. HUD and UX Requirements

The UI can still be minimal, but it must now support free-text play cleanly.

### Show

- turn number
- rescue ETA
- oxygen
- battery
- hull
- threat value and stage label
- current scene text
- current AI line
- input prompt
- available fallback hotkeys for the 4 canonical actions
- recent query response or aftermath log

### Do not show after Turn 4

- event category labels
- best-action hints
- explicit correctness labels such as `Correct response`
- model confidence or parser internals

### Input UX rule

The screen should always support a clean fallback path.

If free-text interpretation fails, the player must still be able to continue the run immediately using explicit action hotkeys.

### Outcome presentation rule

End each turn with terse aftermath, not judgment.

Good examples:

- `Pressure drop slowed.`
- `External contact fell back, then returned.`
- `Recycler output stabilizing.`
- `Channel contamination persists.`
- `The plates settle. The knocking does not.`

Bad examples:

- `Correct response.`
- `Wrong action.`
- `Best choice identified.`

---

## 21. Story Scope

Narrative stays thin and atmospheric.

### Intro

- the player wakes inside a damaged submarine
- external visibility is unavailable
- rescue is delayed
- something may be outside

### Midgame

- faults stop feeling isolated
- the AI becomes incomplete and then actively suspect
- readouts begin to conflict with one another
- immediate shocks begin to stack with longer failures
- the player starts questioning the scene in their own words

### Ending

- **1 win ending:** rescue reaches the vessel
- **1 loss ending:** the vessel is lost

Do not build a branching narrative layer into the MVP.

---

## 22. Technical State Model

Required fields:

- `turn_index`
- `oxygen`
- `battery`
- `hull`
- `threat`
- `ai_state`
- `active_conditions`
- `signal_contamination_active`
- `query_used_this_turn`
- `last_player_input`
- `interpreted_input_type`
- `interpreted_action`
- `fallback_used`
- `game_over`
- `win`

Recommended condition subfields:

- `leak_stage`
- `power_bleed_stage`
- `pursuit_stage`

Recommended authored-turn fields:

- `scene_packet`
- `acute_penalty`
- `aftermath_lines`

Optional fields:

- `last_scan_result_type`
- `current_scene_text`
- `last_query_response`

Do not add more state than needed to support the authored deck and bounded query system.

---

## 23. Data Structure Recommendation

Store the game as simple data.

### Actions data

Each action should define:

- name
- battery cost
- full base effect
- partial base effect
- strongest problem class
- input hint examples

### Deck turn data

Each turn entry should define:

- turn number
- AI state
- AI line seed
- required scene facts
- misleading scene facts
- query answer facts
- forbidden claims
- active condition changes
- acute penalty if any
- strong action
- partial action notes if needed
- optional SCAN result text
- optional terse aftermath text
- fallback scene block
- fallback query block
- purpose note

### Recommendation

Keep the deck data-driven so both balance values and LLM-facing facts can be tuned in one place.

---

## 24. Recommended Implementation Order

### 1. Core loop

- create game state
- render HUD
- implement 12-turn progression
- add win/loss checks

### 2. Passive pressure and conditions

- implement passive oxygen and threat pressure
- implement authored condition drains
- implement condition clear / suppress logic

### 3. Actions and deterministic resolution

- SCAN
- REPAIR
- SILENT
- REROUTE
- strong / partial / wrong resolution

### 4. Fallback-only presentation

- authored scene text
- authored aftermath text
- explicit action hotkeys
- full playthrough without LLM calls

### 5. LLM presentation layer

- build scene packet formatter
- build one-query-per-turn handling
- classify `QUERY` vs `COMMITMENT`
- classify commitment to canonical action
- validate outputs strictly

### 6. Fixed event deck

- script all 12 turns
- connect scene facts, AI lines, conditions, acute penalties, and SCAN outputs
- add fallback scene and aftermath blocks per turn

### 7. Presentation polish

Only after the build is fully playable:

- corruption overlays
- minor text effects
- one extra corrupted line before Turn 12

---

## 25. Testing Priorities

### Core deterministic tests

Check:

- action costs apply correctly
- strong action cancels acute penalty
- partial action keeps acute penalty
- wrong action gives expected limited effect
- condition escalation behaves correctly
- turn advancement works
- rescue/win condition triggers on final survival

### LLM boundary tests

Check:

- commitment phrases map to one of the four canonical actions
- question-like inputs map to `QUERY`
- query answers never reveal hidden condition labels or strong actions
- one-query-per-turn enforcement works
- fallback mode keeps the run fully playable when the LLM fails
- identical engine state plus identical interpreted action yields identical resource results

---

## 26. Balance Check

Use this only as a rough sanity check during implementation.

### Competent-play target band

A player who makes mostly strong reads, but not a perfect run, should finish roughly near:

- **Oxygen:** 12 to 24
- **Battery:** 6 to 16
- **Hull:** 18 to 34
- **Threat:** 42 to 72

The late game should feel survivable, but not comfortable.

### Session pacing target

A first playthrough with one brief query on several turns should usually land closer to **8 to 15 minutes**, not one minute.

---

## 27. Success Criteria

The MVP succeeds if:

- the player learns the four actions in the first four turns
- the player understands that they may ask one brief question per turn
- the late game becomes noticeably harder to interpret
- persistent drains and acute penalties make the sub feel progressively more doomed
- SCAN feels like a tense diagnostic gamble instead of a guaranteed answer
- free-text input reliably collapses to one of the four canonical actions
- the LLM-generated prose increases reading time and immersion without changing deterministic balance
- the run remains fully playable through fallback text and explicit action hotkeys
- the team can build, test, and demo it within the hackathon window

---

## 28. Final Build Definition

This spec defines a strict hackathon-sized horror game:

> A fully scripted 12-turn terminal survival horror game where the player manages oxygen, battery, hull, and threat inside a damaged deep-sea submarine, reads LLM-rendered but engine-grounded scene text, may ask one brief in-fiction question per turn, commits to one of four canonical actions using natural language, and survives by navigating authored persistent failures, authored acute penalties, mixed-symptom scenes, and an increasingly unreliable AI until rescue arrives.
