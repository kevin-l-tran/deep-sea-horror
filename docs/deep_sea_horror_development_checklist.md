# Deep Sea Horror Terminal Game

## Development Checklist

A practical implementation checklist for the Textual hackathon MVP.

---

## 0. Scope Lock

### Must keep
- [ ] Fixed 12-turn run only
- [ ] 1 intro screen
- [ ] 1 gameplay screen
- [ ] 1 end screen
- [ ] 4 player actions: SCAN, REPAIR, SILENT, REROUTE
- [ ] 4 visible resources: oxygen, battery, hull, threat
- [ ] Authored persistent condition arcs only
- [ ] Authored acute penalties only
- [ ] Data-driven deck
- [ ] Horror-first presentation

### Must cut
- [ ] No procedural event generation
- [ ] No parser / free-text commands
- [ ] No map or inventory system
- [ ] No repair minigames
- [ ] No branching narrative routes
- [ ] No dynamic AI trust simulation
- [ ] No extra gameplay modes beyond the main HUD
- [ ] No heavy polish until the run is fully playable

---

## 1. Project Bootstrap

- [ ] Create project root and Python package structure
- [ ] Add `pyproject.toml`
- [ ] Add `README.md`
- [ ] Create app folders:
  - [ ] `app/screens/`
  - [ ] `app/widgets/`
  - [ ] `app/engine/`
  - [ ] `app/content/`
  - [ ] `app/effects/`
  - [ ] `app/tests/`
- [ ] Add `__init__.py` files where needed
- [ ] Install / configure Textual
- [ ] Confirm app launches to a placeholder screen

---

## 2. Core Engine Models

### `engine/models.py`
- [ ] Define `Action` enum
- [ ] Define `AIState` enum
- [ ] Define any outcome / resolution enums needed
- [ ] Define `AcutePenalty` model or equivalent
- [ ] Define `TurnCard` model

### `engine/state.py`
- [ ] Define `Resources`
- [ ] Define `ActiveConditions`
- [ ] Define `GameState`
- [ ] Keep state intentionally small
- [ ] Confirm state supports only authored deck requirements

### Starting values and constants
- [ ] Oxygen starts at 42
- [ ] Battery starts at 40
- [ ] Hull starts at 50
- [ ] Threat starts at 18
- [ ] Threat stage label helper exists

---

## 3. Content Layer

### `content/actions.py`
- [ ] Define SCAN cost: battery -4
- [ ] Define REPAIR base effect
- [ ] Define SILENT base effect
- [ ] Define REROUTE cost: battery -8
- [ ] Define full vs partial action values
- [ ] Preserve action identity boundaries

### `content/text.py`
- [ ] Write intro text
- [ ] Write win text
- [ ] Write generic loss text
- [ ] Add fallback aftermath text if needed

### `content/deck.py`
- [ ] Add all 12 turns as authored data
- [ ] Add readouts for every turn
- [ ] Add AI state for every turn
- [ ] Add AI line for every turn
- [ ] Add strong action for every turn
- [ ] Add acute penalties for turns 6 to 12
- [ ] Add optional SCAN output entries
- [ ] Add partial / bait outcome notes where needed
- [ ] Add terse aftermath lines
- [ ] Keep category labels hidden after turn 4
- [ ] Keep SCAN high-value mainly on turns 3, 6, and 9

---

## 4. Condition Logic

### `engine/conditions.py`
- [ ] Implement leak stage logic
- [ ] Implement power bleed stage logic
- [ ] Implement pursuit stage logic
- [ ] Implement contamination flag logic
- [ ] Implement condition escalation rules
- [ ] Implement condition clear / suppress rules
- [ ] Ensure no more than authored conditions are used

### Required authored arcs
- [ ] Leak arc works across turns 5 to 6
- [ ] Signal contamination arc works across turns 6 to 9
- [ ] Power bleed arc works across turns 7 to 8
- [ ] Pursuit arc works across turns 9 to 12

---

## 5. Turn Flow

### `engine/turn_flow.py`
- [ ] Apply start-of-turn passive pressure
- [ ] Oxygen -2 every turn
- [ ] Threat +2 every turn
- [ ] Apply active condition drains after passive pressure
- [ ] Load current turn card
- [ ] Expose current readouts and AI line
- [ ] Advance turn count correctly
- [ ] Resolve rescue on survival through turn 12
- [ ] Check immediate loss after resolution

### Loss conditions
- [ ] Loss on oxygen reaching 0
- [ ] Loss on hull reaching 0
- [ ] Loss on threat reaching 100
- [ ] Battery at 0 does not cause immediate loss

### Order validation
- [ ] Turn order is fixed and implemented in engine code
- [ ] UI does not perform gameplay sequencing directly

---

## 6. Action Resolution

### `engine/resolver.py`
- [ ] Apply SCAN battery cost even on bad reads
- [ ] Apply REROUTE battery cost even on bad reads
- [ ] Resolve strong match behavior
- [ ] Resolve partial match behavior
- [ ] Resolve wrong read behavior
- [ ] Cancel acute penalty on strong match
- [ ] Keep acute penalty on partial match
- [ ] Keep acute penalty on wrong read
- [ ] Support authored deck exceptions where needed
- [ ] Generate terse aftermath lines

### Specific behavior checks
- [ ] REPAIR strongly handles structural pressure
- [ ] SILENT strongly handles pursuit / threat pressure
- [ ] REROUTE strongly handles oxygen / power pressure
- [ ] SCAN diagnoses but does not become a generic truth button
- [ ] Costly partial successes exist on late bait turns

---

## 7. Game Controller Boundary

### `engine/controller.py`
- [ ] Implement `new_game()`
- [ ] Implement `get_current_turn()`
- [ ] Implement `choose_action(action)`
- [ ] Keep UI interaction limited to controller methods
- [ ] Return updated state cleanly after each action
- [ ] Keep controller as the only gameplay boundary for Textual

---

## 8. Minimal Non-UI Play Test Harness

- [ ] Add a simple terminal / stdout harness for engine testing
- [ ] Print current turn data
- [ ] Allow quick manual action selection
- [ ] Verify full 12-turn run without Textual widgets
- [ ] Use this harness to debug resolution before UI work

---

## 9. Textual App Shell

### `main.py`
- [ ] Create Textual app entrypoint
- [ ] Load global CSS / TCSS
- [ ] Register key bindings if needed
- [ ] Push intro screen on startup

### Screens
- [ ] Build `intro_screen.py`
- [ ] Build `game_screen.py`
- [ ] Build `end_screen.py`

### Screen flow
- [ ] Intro starts a new run
- [ ] Game screen handles action input
- [ ] End screen shows win or loss
- [ ] Restart works from end screen
- [ ] Quit works cleanly

---

## 10. Core Widgets

### `widgets/header_bar.py`
- [ ] Show current turn
- [ ] Show rescue ETA

### `widgets/resource_panel.py`
- [ ] Show oxygen
- [ ] Show battery
- [ ] Show hull
- [ ] Show threat
- [ ] Show threat stage label

### `widgets/readout_panel.py`
- [ ] Show current sensor / comms lines
- [ ] Support mixed-symptom presentation

### `widgets/ai_panel.py`
- [ ] Show AI line
- [ ] Show AI-state styling if desired

### `widgets/action_panel.py`
- [ ] Show 4 actions
- [ ] Show battery costs where relevant
- [ ] Show key hints for 1 / 2 / 3 / 4

### `widgets/log_panel.py`
- [ ] Show recent aftermath lines
- [ ] Show brief system messages

### `widgets/overlay_panel.py`
- [ ] Reserve space / mechanism for corruption overlays

---

## 11. Game Screen Wiring

### `screens/game_screen.py`
- [ ] Create controller on mount
- [ ] Start a new game on mount or on entry
- [ ] Render current state
- [ ] Bind `1` to SCAN
- [ ] Bind `2` to REPAIR
- [ ] Bind `3` to SILENT
- [ ] Bind `4` to REROUTE
- [ ] Refresh the full screen after each action
- [ ] Transition to end screen when `game_over` is true

### Important UI discipline
- [ ] Widgets render only
- [ ] Widgets do not apply drains
- [ ] Widgets do not decide outcome quality
- [ ] Widgets do not mutate persistent conditions directly
- [ ] Gameplay logic stays out of widget callbacks

---

## 12. Deck Hookup and Validation

- [ ] Confirm all 12 turns render correctly in UI
- [ ] Confirm AI state schedule is correct
- [ ] Turns 1 to 4: Stable
- [ ] Turns 5 to 8: Degraded
- [ ] Turns 9 to 12: Corrupted
- [ ] Confirm all acute penalties fire on the intended turns
- [ ] Confirm all persistent condition arcs begin and end correctly
- [ ] Confirm late bait turns produce the intended costly partials
- [ ] Confirm turn 12 resolves to rescue if player survives

---

## 13. Tests

### `tests/test_deck_integrity.py`
- [ ] Deck has exactly 12 turns
- [ ] Every turn has a strong action
- [ ] Every turn has an AI state
- [ ] Acute penalties are valid
- [ ] Aftermath references are present

### `tests/test_resolution.py`
- [ ] Action costs apply correctly
- [ ] Strong match cancels acute penalty
- [ ] Partial match keeps acute penalty
- [ ] Wrong read gets expected limited effect
- [ ] Late authored partials behave correctly

### `tests/test_conditions.py`
- [ ] Leak drain escalates correctly
- [ ] Power bleed drain escalates correctly
- [ ] Pursuit suppression behaves correctly
- [ ] Contamination clears on authored turns

### `tests/test_turn_flow.py`
- [ ] Passive drain order is correct
- [ ] Condition drains happen at correct time
- [ ] Turn advancement works
- [ ] Win triggers on final survival
- [ ] Loss triggers at the correct thresholds

---

## 14. Tuning Pass

- [ ] Play at least one mostly-correct run
- [ ] Play at least one intentionally bad run
- [ ] Check that late game feels oppressive, not random
- [ ] Check that tutorial teaches all 4 actions cleanly
- [ ] Check that SCAN feels narrow and risky later
- [ ] Check that battery pressure feels real but not instantly fatal
- [ ] Check that aftermath text avoids explicit judgment labels
- [ ] Check that end-state values roughly land in the target band on competent play

### Competent-play target band
- [ ] Oxygen roughly 14 to 26
- [ ] Battery roughly 8 to 16
- [ ] Hull roughly 20 to 36
- [ ] Threat roughly 40 to 68

---

## 15. Effects and Styling (Last)

### `effects/corruption.py`
- [ ] Translate game state into presentation flags only
- [ ] Keep effect logic centralized

### Optional overlay states
- [ ] none
- [ ] warning_flash
- [ ] false_alert
- [ ] ghost_text
- [ ] mild_jitter
- [ ] severe_tint

### Restraint rules
- [ ] Do not add effects until the full run is playable
- [ ] Do not hide critical gameplay info too aggressively
- [ ] Do not build a general animation framework
- [ ] Stop after one or two effective corruption effects

---

## 16. Final Demo Checklist

- [ ] Intro, gameplay, and ending all work in sequence
- [ ] Full run can be completed without crashes
- [ ] Win path works
- [ ] Loss path works
- [ ] Inputs are responsive
- [ ] The main HUD is readable
- [ ] Threat label updates correctly
- [ ] Late turns feel harsher than early turns
- [ ] AI becomes visibly less trustworthy over time
- [ ] The build is demoable in under 10 minutes

---

## 17. Nice-to-Have Only If Everything Above Is Done

- [ ] Slight panel flash on acute penalty
- [ ] Mild corrupted text overlay on late turns
- [ ] One extra corrupted line before turn 12
- [ ] Slight screen tint shift by AI state
- [ ] Cleaner typography / spacing polish

---

## Recommended Execution Order

1. Core models and state
2. Actions data and starting constants
3. 12-turn deck data
4. Condition logic
5. Turn flow
6. Resolver
7. Controller
8. Non-UI play harness
9. Textual gameplay screen
10. Intro / end screens
11. Tests and tuning
12. Effects last

---

## Stop Rules

Stop adding features and ship once these are true:
- [ ] Full 12-turn run works end to end
- [ ] Win/loss conditions are correct
- [ ] Late-game pressure feels strong
- [ ] UI is stable enough to demo
- [ ] No core scope violations were introduced
