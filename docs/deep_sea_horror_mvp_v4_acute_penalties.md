# Deep Sea Horror Terminal Game

## Hackathon MVP Spec v4.0

**Document Type:** Hackathon MVP game spec  
**Target Build Window:** 18 hours  
**Target Platform:** Desktop terminal or browser-based terminal UI  
**Genre:** Text-based survival horror  
**Target Session Length:** 5 to 10 minutes

---

## 1. High Concept

**One-sentence pitch**  
A 12-turn terminal survival horror game where the player manages a failing deep-sea submarine, interprets ambiguous sensor readouts, and survives long enough for rescue while ongoing failures, acute shocks, and an increasingly untrustworthy AI make every choice feel unsafe.

**Player fantasy**  
The player is trapped inside a damaged vessel with no visual contact with the outside world. They survive by reading partial system data, distorted comms, recurring external contact, and increasingly suspect guidance from the onboard AI.

---

## 2. Design Goals

This version of the spec is optimized for an 18-hour hackathon build, but it prioritizes horror over clarity.

### Primary goals

1. **Horror-first decision making**  
   The player should often feel unsure which action is actually correct.

2. **Resource triage under pressure**  
   Ongoing multi-turn conditions and authored acute penalties should make the submarine feel like it is failing faster than the player can fully control.

3. **Fast implementation**  
   The build must still be finishable inside the time limit with a scripted deck and a small amount of authored state.

4. **Strong atmosphere from text alone**  
   The build should work with plain text, no sound, no animation, and no advanced UI.

5. **Difficulty over readability**  
   The game is allowed to feel harsh, partially unreadable, and occasionally unfair, as long as the rules are authored and consistent enough to learn over repeated runs.

---

## 3. Non-Negotiable Scope

This is the exact MVP scope.

### Included

- 1 intro screen
- 1 gameplay loop
- 12 fixed turns
- 4 player actions
- 4 visible resources
- 4 internal problem classes
- 3 authored persistent condition arcs plus 1 contamination overlay arc
- mixed-symptom readouts after the tutorial
- authored acute penalties on most late turns
- 3 AI reliability states
- 1 win ending
- 1 generic loss ending
- terminal-style HUD and turn readout

### Explicitly cut

- free text parser
- branching narrative routes
- map navigation
- inventory systems
- crew simulation
- combat
- repair minigames
- save/load
- procedural event generation
- real-time typing pressure
- multiple endings
- lore log collection systems
- extra UI modes beyond the main terminal screen
- probabilistic AI truth simulation
- large dynamic status system beyond the authored conditions listed in this spec

### Scope rule

If a feature is not required to make the 12-turn run playable from start to finish, it is out of scope.

---

## 4. Core Experience

The game creates tension through:

- low-information decision making
- accumulating passive pressure
- persistent multi-turn resource drains
- authored acute penalties on high-pressure turns
- mixed symptoms that point toward more than one possible action
- an AI that shifts from helpful to incomplete to sometimes wrong
- concise, high-contrast terminal presentation

The player should feel trapped, underinformed, and increasingly behind.

---

## 5. Build Strategy

This MVP should be built as a **fully scripted 12-turn run**, not a simulation sandbox.

### Why

A fixed run is easier to:

- implement
- tune
- test
- polish
- demo repeatedly during a hackathon

### Implementation rule

Use a predefined turn deck stored as data.  
Do not randomize event order in the MVP.

Persistent conditions are also authored in the deck.  
Do not build a general procedural status engine.

Acute penalties are also authored in the deck.  
Do not build a generic reaction-combo system.

---

## 6. Win and Loss Conditions

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

## 7. Starting Values

Lock the starting values now so implementation and tuning stay stable.

- **Oxygen:** 42
- **Battery:** 40
- **Hull:** 50
- **Threat:** 18

These values assume persistent drains, authored acute penalties, and some wrong guesses.

---

## 8. Core Resources

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

## 9. Internal Problem Classes

The game still uses four internal problem classes for implementation and balancing.

- **STRUCTURAL**
- **PURSUIT**
- **POWER**
- **CONTAMINATION**

### Important presentation rule

After the tutorial, these category labels are **not shown to the player**.  
The player only sees readouts, AI lines, resource changes, and terse aftermath.

---

## 10. AI Reliability System

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

## 11. Player Actions

The player has exactly four actions.

Each action must keep one clear identity.

### 11.1 SCAN

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

### 11.2 REPAIR

**Role:** stabilize structural failure  
**Cost:** none

**Base effect:**

- **Hull +8** on a strong match
- **Hull +4** on a partial match

**Strongest against:** **STRUCTURAL** persistent conditions and acute hull pressure

### 11.3 SILENT

**Role:** reduce threat and suppress external attention  
**Cost:** none

**Base effect:**

- **Threat -8** on a strong match
- **Threat -4** on a partial match

**Strongest against:** **PURSUIT**

**Special role:**

- suppresses the current turn's Pursuit drain on a strong match
- does not permanently remove the final Pursuit arc

### 11.4 REROUTE

**Role:** preserve oxygen at battery cost  
**Cost:** Battery -8

**Base effect:**

- **Oxygen +8** on a strong match
- **Oxygen +4** on a partial match

**Strongest against:** **POWER** drains and acute life-support instability

### Action identity rule

- **SCAN = diagnose**
- **REPAIR = structure**
- **SILENT = threat / suppression**
- **REROUTE = oxygen / power**

No action should take over another action's core job.

---

## 12. Passive Turn Pressure

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

## 13. Persistent Condition Model

This version adds a small authored condition layer.

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
- causes one or more readouts or AI lines to become unreliable
- removed by **SCAN** on authored turns

### Arc limits

- Only **4 authored condition arcs** exist in the MVP.
- Only **2 conditions** may be active at once.
- All condition behavior is authored in the deck.

---

## 14. Acute Penalty Model

This version adds a second pressure layer on top of passive drain and persistent conditions.

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

## 15. Resolution Model

This system must be exact, small, and easy to implement.

### Phase order

1. Render status
2. Apply passive turn pressure
3. Apply any active persistent-condition drains
4. Present current readouts
5. Show AI line
6. Get player action
7. Resolve action against the authored current turn logic
8. Apply or cancel the authored acute penalty based on result
9. Clamp values and check end state

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

## 16. Readout Structure

After the tutorial, each turn should present **mixed symptoms**.

### Rule

A late-game turn should usually include:

- 2 short sensor or comms lines
- at least 1 symptom that points toward the primary hidden condition
- at least 1 symptom that could be interpreted as something else

### Important presentation rule

Do **not** show the internal category label after Turn 4.

### SCAN rule

SCAN should become less definitive after the tutorial.

- midgame SCAN often returns partial truth
- contaminated turns may mix useful data with misleading implications
- corrupted late-game SCAN may confirm one fact while failing to make the correct action obvious

---

## 17. Tutorial Structure

The first four turns still teach the core verbs.

- **Turn 1:** readable structural problem -> teaches REPAIR
- **Turn 2:** readable external contact -> teaches SILENT
- **Turn 3:** readable false signal -> teaches SCAN
- **Turn 4:** readable life-support instability -> teaches REROUTE

### Important update

The tutorial should be readable, but the AI should **not** explicitly name the answer.

Do not use phrasing such as:

- `Recommend repair.`
- `Recommend silent running.`
- `Recommend active scan.`
- `Recommend power reroute.`

The player should learn by associating symptoms, actions, and aftermath rather than following a tutorial hint system.

After Turn 4, clarity drops sharply.

---

## 18. AI Dialogue Budget

### Tutorial budget

Turns 1 to 4 can use direct, readable AI lines.

### Late-game budget

Turns 5 to 12 should use authored per-turn lines.  
Do **not** force the late game into one reusable line per problem type.

### Reason

The late game should feel specific, unstable, and harder to pattern-match.

---

## 19. HUD and UX Requirements

The UI can still be minimal, but it must now preserve ambiguity.

### Show

- turn number
- rescue ETA
- oxygen
- battery
- hull
- threat value and stage label
- current sensor / comms readouts
- current AI line
- available actions

### Do not show after Turn 4

- event category labels
- best-action hints
- explicit correctness labels such as `Correct response`

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

### Dread rule

Late-game aftermath text should reinforce that the player acted, but did not regain full control.

---

## 20. Turn Structure Example

```text
TURN 07/12
RESCUE ETA: 5 TURNS
OXYGEN: 24
BATTERY: 24
HULL: 39
THREAT: 34 (NEARBY)

RECYCLER: Cycle length increasing.
SONAR: Return pulse repeats at impossible distance.

AI: Load is slipping between circuits. The echo may be borrowing it.

ACTIONS:
[SCAN] cost 4 battery
[REPAIR]
[SILENT]
[REROUTE] cost 8 battery

> reroute

Battery -8.
Recycler output stabilizing.
Echo still present.
```

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
- `game_over`
- `win`

Recommended condition subfields:

- `leak_stage`
- `power_bleed_stage`
- `pursuit_stage`

Recommended authored-turn fields:

- `acute_penalty`
- `aftermath_lines`

Optional fields:

- `last_scan_result_type`
- `current_readouts`

Do not add more state than needed to support the authored deck.

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

### Deck turn data

Each turn entry should define:

- turn number
- player-facing readouts
- AI state
- AI line
- active condition changes
- acute penalty if any
- strong action
- partial action notes if needed
- optional SCAN result text
- optional terse aftermath text
- purpose note

### Recommendation

Keep the deck data-driven so the content and balance values can be tuned in one place.

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

### 3. Actions

- SCAN
- REPAIR
- SILENT
- REROUTE

### 4. Acute penalties

- add authored acute-penalty resolution
- ensure strong match cancels it
- ensure partial and wrong reads still take it

### 5. Fixed event deck

- script all 12 turns
- connect readouts, AI lines, conditions, acute penalties, and SCAN outputs

### 6. Presentation

- intro text
- terse aftermath text
- win screen
- loss screen
- simple terminal formatting

### 7. Optional polish

Only after the build is fully playable:

- subtle text effects
- ambient sound
- one extra corrupted line before Turn 12

---

## 25. Balance Check

Use this only as a rough sanity check during implementation.

### Competent-play target band

A player who makes mostly strong reads, but not a perfect run, should finish roughly near:

- **Oxygen:** 14 to 26
- **Battery:** 8 to 16
- **Hull:** 20 to 36
- **Threat:** 40 to 68

The late game should feel survivable, but not comfortable.

---

## 26. Success Criteria

The MVP succeeds if:

- the player learns the four actions in the first four turns
- the late game becomes noticeably harder to interpret
- persistent drains and acute penalties make the sub feel progressively more doomed
- SCAN feels like a tense diagnostic gamble instead of a guaranteed answer
- the AI feels readable early and suspect late
- the run completes in under 10 minutes
- the team can build, test, and demo it within the hackathon window

---

## 27. Final Build Definition

This spec defines a strict hackathon-sized horror game:

> A fully scripted 12-turn terminal survival horror game where the player manages oxygen, battery, hull, and threat inside a damaged deep-sea submarine, learns four actions through a short readable tutorial, then spends the back half of the run triaging authored persistent failures, authored acute penalties, mixed-symptom readouts, and an increasingly unreliable AI until rescue arrives.
