# Deep Sea Horror Terminal Game

## Textual Implementation Guide

**Document Type:** Technical implementation guide  
**Target Framework:** Textual (Python TUI)  
**Project Scope:** Fixed 12-turn horror MVP for an 18-hour hackathon

---

## 1. Purpose

This document translates the current project direction into a practical implementation plan for a Textual-based build.

The main goal is to keep the app structure simple enough to finish during the hackathon while preserving the project's core strengths:

- horror-first presentation
- ambiguous decision-making
- fixed authored run
- low UI surface area
- one main gameplay screen
- data-driven content

The most important architectural rule is:

> Keep the game rules in plain Python and use Textual only as the presentation layer.

---

## 2. High-Level Recommendation

For this project, the best architecture is:

**data-driven content + pure game engine + thin Textual UI shell**

That means:

- authored turn data lives in content files
- turn resolution logic lives in engine files
- widgets render current state but do not decide outcomes
- screens only coordinate input, display, and screen transitions

This is the safest way to avoid mixing gameplay rules with widget callbacks.

---

## 3. Why Textual Fits This Project

A Textual build is a good match because the MVP already has:

- one primary HUD screen
- a fixed 12-turn run
- four actions
- terse readouts and AI lines
- little need for complex navigation
- a terminal-first aesthetic

The UI can remain narrow and focused:

- intro screen
- gameplay screen
- end screen
- optional corruption overlay

That makes the interface achievable without building a large widget system.

---

## 4. Core Architectural Rules

### 4.1 Keep gameplay logic out of widgets

Widgets should:

- show resource values
- show turn text
- show actions
- show aftermath logs
- render corruption effects

Widgets should not:

- apply drains
- resolve strong vs partial vs wrong actions
- decide turn outcomes
- mutate persistent conditions directly
- determine win/loss

### 4.2 Keep the deck data-driven

The 12-turn run should be stored as authored data.

Do not hardcode turn logic into screen methods.

### 4.3 Use one controller boundary

The UI should talk to exactly one high-level object, such as `GameController`.

This gives the UI a simple contract:

- create a new game
- ask for current turn data
- submit one action
- get updated state back

### 4.4 Build one screen well instead of many views poorly

The gameplay experience should live almost entirely in one screen.

Do not spend hackathon time building multiple HUD modes, popout menus, or alternate navigation flows.

---

## 5. Recommended Project Layout

```text
project_root/
  pyproject.toml
  README.md

  app/
    __init__.py
    main.py
    app.tcss

    screens/
      __init__.py
      intro_screen.py
      game_screen.py
      end_screen.py

    widgets/
      __init__.py
      header_bar.py
      resource_panel.py
      readout_panel.py
      ai_panel.py
      action_panel.py
      log_panel.py
      overlay_panel.py

    engine/
      __init__.py
      controller.py
      state.py
      models.py
      resolver.py
      turn_flow.py
      conditions.py
      formatting.py

    content/
      __init__.py
      actions.py
      deck.py
      text.py

    effects/
      __init__.py
      corruption.py

    tests/
      test_turn_flow.py
      test_conditions.py
      test_resolution.py
      test_deck_integrity.py
```

---

## 6. File Responsibilities

## 6.1 `main.py`

Owns the Textual app entrypoint.

Responsibilities:

- define the `App` subclass
- register key bindings if needed
- load global CSS
- push the intro screen on startup

This file should stay very small.

---

## 6.2 `screens/`

### `intro_screen.py`

Responsibilities:

- show title
- show short intro text
- allow start
- optionally allow quit

### `game_screen.py`

Responsibilities:

- compose the gameplay layout
- route action input to the controller
- refresh widgets from state
- trigger overlay effects
- move to end screen when game ends

This should be the main screen and the center of the UI.

### `end_screen.py`

Responsibilities:

- show win/loss outcome
- show brief final summary or recent log lines
- allow restart or quit

---

## 6.3 `widgets/`

Use a small number of coarse widgets rather than many tiny widgets.

### `header_bar.py`
Shows:

- current turn
- rescue ETA

### `resource_panel.py`
Shows:

- oxygen
- battery
- hull
- threat
- threat stage label

### `readout_panel.py`
Shows:

- current sensor lines
- comms lines
- mixed symptoms

### `ai_panel.py`
Shows:

- current AI line
- optional AI-state styling

### `action_panel.py`
Shows:

- four actions
- battery costs where relevant
- key hints

### `log_panel.py`
Shows:

- aftermath lines
- recent turn results
- brief system messages

### `overlay_panel.py`
Shows:

- corruption flashes
- fake warnings
- duplicated text
- brief interruption screens

---

## 6.4 `engine/`

This is where the real game lives.

### `state.py`
Contains the main state dataclasses.

### `models.py`
Contains shared models and enums.

Examples:

- `Action`
- `AIState`
- `TurnCard`
- `AcutePenalty`
- `Resources`
- `ActiveConditions`
- `Outcome`

### `resolver.py`
Contains action resolution logic.

Responsibilities:

- determine strong vs partial vs wrong resolution
- apply action effects
- apply battery costs
- determine aftermath text

### `turn_flow.py`
Contains turn progression logic.

Responsibilities:

- apply passive pressure
- apply persistent condition drains
- advance turn count
- update AI state if needed
- check win/loss

### `conditions.py`
Owns condition-specific helpers.

Responsibilities:

- leak stage logic
- power bleed stage logic
- pursuit suppression rules
- contamination flags

### `controller.py`
Provides the clean API used by the UI.

### `formatting.py`
Contains helpers for turning raw values into player-facing display values.

Examples:

- threat label conversion
- UI display strings
- meter formatting

---

## 6.5 `content/`

This folder should hold all authored content.

### `actions.py`
Define action identity and baseline values.

Examples:

- SCAN cost and purpose
- REPAIR base benefit
- SILENT base benefit
- REROUTE base benefit

### `deck.py`
Define the fixed 12-turn sequence.

Each entry should contain:

- turn number
- readouts
- AI state
- AI line
- active condition changes
- acute penalty
- strong action
- optional scan output
- optional partial outcome notes
- aftermath text

### `text.py`
Store:

- intro text
- win text
- loss text
- generic fallback phrases

---

## 6.6 `effects/`

### `corruption.py`
Keep visual-effect decisions centralized.

This file should not directly render anything.

Instead, it should translate game state into presentation flags.

Examples:

- no corruption effect
- warning flash
- false alert overlay
- brief duplicate-line mode
- mild jitter
- severe tint state

This keeps horror presentation from leaking across every widget file.

---

## 7. Core Data Model

A minimal model layout could look like this:

```python
from dataclasses import dataclass, field
from enum import Enum, auto


class Action(Enum):
    SCAN = auto()
    REPAIR = auto()
    SILENT = auto()
    REROUTE = auto()


class AIState(Enum):
    STABLE = auto()
    DEGRADED = auto()
    CORRUPTED = auto()


@dataclass
class Resources:
    oxygen: int
    battery: int
    hull: int
    threat: int


@dataclass
class ActiveConditions:
    leak_stage: int = 0
    power_bleed_stage: int = 0
    pursuit_stage: int = 0
    contamination_active: bool = False


@dataclass
class TurnCard:
    turn: int
    readouts: list[str]
    ai_state: AIState
    ai_line: str
    strong_action: Action
    acute_penalty: dict | None = None
    scan_result: str | None = None
    aftermath: dict[Action, str] = field(default_factory=dict)


@dataclass
class GameState:
    turn_index: int
    rescue_eta: int
    resources: Resources
    conditions: ActiveConditions
    game_over: bool = False
    win: bool = False
    log: list[str] = field(default_factory=list)
```

This is intentionally small.

Add fields only when they support the authored deck directly.

---

## 8. Recommended Controller API

The UI should only talk to a controller object.

Example shape:

```python
class GameController:
    def new_game(self) -> GameState:
        ...

    def get_current_turn(self) -> TurnCard:
        ...

    def choose_action(self, action: Action) -> GameState:
        ...
```

### Recommended `choose_action()` flow

1. read current turn card
2. apply action cost
3. resolve strong, partial, or wrong result
4. apply acute penalty if not canceled
5. append aftermath text
6. clamp resource values
7. check loss state
8. advance turn or end game
9. return updated state

This keeps `GameScreen` simple and predictable.

---

## 9. Turn Flow Order

Use a strict turn order and do not vary it casually.

### Recommended order

1. start turn
2. apply passive pressure
3. apply active condition drains
4. load current turn card
5. render readouts and AI line
6. wait for player action
7. resolve action
8. apply acute penalty if needed
9. append aftermath text
10. clamp values
11. check immediate loss
12. advance to next turn or resolve rescue

This order should exist in engine code, not inside UI callbacks.

---

## 10. UI Composition Recommendation

A strong single-screen layout would look like this:

```text
+-----------------------------------------------------------+
| TURN 07/12           RESCUE ETA: 5                        |
+-------------------------+---------------------------------+
| OXYGEN   24             | READOUTS                        |
| BATTERY  24             | Recycler cycle lengthening.     |
| HULL     39             | Sonar return repeats...         |
| THREAT   34 (NEARBY)    |                                 |
+-------------------------+---------------------------------+
| AI                                                        |
| Load is slipping between circuits...                      |
+-----------------------------------------------------------+
| ACTIONS: [1] SCAN  [2] REPAIR  [3] SILENT  [4] REROUTE    |
+-----------------------------------------------------------+
| LOG / AFTERMATH                                           |
| Battery -8. Recycler output stabilizing.                  |
| Echo still present.                                       |
+-----------------------------------------------------------+
```

### Layout priorities

- keep all critical state visible at once
- avoid navigation between panels
- keep action selection immediate
- keep aftermath visible but compact
- preserve terminal readability even during corruption effects

---

## 11. Input Recommendation

Use very simple keyboard controls.

### Recommended bindings

- `1` = SCAN
- `2` = REPAIR
- `3` = SILENT
- `4` = REROUTE
- `q` = quit
- `r` = restart on end screen

Avoid mouse-heavy interaction and avoid deep focus-management work unless it comes for free.

---

## 12. Textual-Specific Guidance

## 12.1 Keep widget count modest

The app does not need many tiny widgets.

A few larger widgets are enough.

This is better for:

- speed of implementation
- easier refresh logic
- less cross-widget state churn
- fewer places for visual bugs

## 12.2 Batch screen updates after a turn

When one action resolves, multiple visible elements change at once.

Update them as one coherent screen refresh rather than as a visible chain of individual updates.

## 12.3 Do not build an animation framework

If you use effects, keep them small and authored.

Good candidates:

- brief opacity pulse
- panel flash
- screen tint
- slight offset shake
- temporary overlay banner

Avoid generalized animation systems or many concurrent moving parts.

## 12.4 Keep gameplay logic synchronous

The turn-resolution path should be fast and local.

Do not introduce asynchronous complexity for the main loop unless there is a real need.

---

## 13. Corruption Effects Plan

Textual can support atmospheric horror effects, but they should be narrowly scoped.

### Recommended approach

Keep corruption logic in two places only:

- `effects/corruption.py` decides the current presentation state
- `widgets/overlay_panel.py` renders it

### Example overlay states

- `none`
- `warning_flash`
- `false_alert`
- `ghost_text`
- `mild_jitter`
- `severe_tint`

### Important rule

Do not hide critical gameplay information behind effects so aggressively that the game becomes unreadable to test.

The effect should increase dread, not destroy implementation stability.

---

## 14. Sample GameScreen Flow

A good gameplay screen should follow this pattern:

```python
class GameScreen(Screen):
    def on_mount(self) -> None:
        self.controller = GameController()
        self.state = self.controller.new_game()
        self.refresh_from_state()

    def handle_action(self, action: Action) -> None:
        self.state = self.controller.choose_action(action)
        self.refresh_from_state()
        if self.state.game_over:
            self.app.push_screen(EndScreen(self.state.win, self.state.log))
```

### `refresh_from_state()` should:

- update header
- update resources
- update readouts
- update AI panel
- update log
- update overlay mode
- update any screen-level style flags

It should not make gameplay decisions.

---

## 15. Recommended Build Order

This is the safest order for a hackathon.

### Phase 1: Engine first

1. implement `GameState`
2. implement `TurnCard`
3. implement passive pressure
4. implement active condition drain logic
5. implement action resolution
6. implement win/loss checks

Do this without Textual imports.

### Phase 2: Single-screen UI

7. create `GameScreen`
8. render a static test turn
9. connect state to widgets
10. connect `1` to `4` keys to action handling
11. show aftermath log updates

### Phase 3: Full deck hookup

12. load the 12-turn deck
13. confirm all turn cards render
14. confirm all resolution paths work
15. test all condition arcs and acute penalties

### Phase 4: Start/end flow

16. add intro screen
17. add end screen
18. add restart flow

### Phase 5: Effects last

19. add corruption overlay
20. add one or two tint/jitter effects
21. stop adding systems

---

## 16. Testing Priorities

Even for a hackathon, a few direct tests are worth it.

### `test_resolution.py`

Check:

- action costs apply correctly
- strong action cancels acute penalty
- partial action keeps acute penalty
- wrong action gives expected limited effect

### `test_conditions.py`

Check:

- leak drain escalates correctly
- power bleed drain escalates correctly
- pursuit suppression behaves correctly
- contamination flags clear on authored turns

### `test_turn_flow.py`

Check:

- passive drain order is correct
- condition drains happen at correct time
- turn advancement works
- rescue/win condition triggers on final survival

### `test_deck_integrity.py`

Check:

- deck has exactly 12 turns
- every turn has a strong action
- AI state exists for each turn
- acute penalties are valid
- all aftermath references are present

These tests are enough to protect the engine from accidental breakage during late UI work.

---

## 17. Styling Guidance

Keep styling simple and consistent.

### Recommended visual priorities

- strong panel borders
- readable spacing
- subdued main palette
- threat label emphasized more than other stats
- corrupted overlays used sparingly

### Avoid

- elaborate CSS experiments
- many distinct visual themes
- large layout rewrites after the core loop works
- polish that slows iteration on turn logic

A clean terminal look is better than a half-finished flashy one.

---

## 18. Scope Protection Rules

During the hackathon, do not add any of the following unless the full 12-turn run is already complete and playable:

- alternate gameplay screens
- large reactive dialogue systems
- free-text command parsing
- inventory or map systems
- dynamic procedural deck generation
- dynamic AI trust simulation
- advanced animation frameworks
- effect-heavy transitions between every turn

The project wins by shipping a complete oppressive run, not by partially shipping a larger game.

---

## 19. Final Recommendation

The right implementation strategy for this project is:

- build the full engine first
- keep the deck and authored outcomes in data
- let Textual handle layout, input, and atmosphere
- use one gameplay screen
- centralize corruption effects
- add polish only after the run works from start to finish

In practical terms, the architecture should stay:

> **small, data-driven, testable, and hostile-looking**

That is the best fit for a Textual-based deep-sea horror hackathon MVP.
