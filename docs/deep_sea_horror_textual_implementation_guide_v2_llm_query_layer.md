# Deep Sea Horror Terminal Game

## Textual Implementation Guide v2.0

**Document Type:** Technical implementation guide  
**Target Framework:** Textual (Python TUI)  
**Project Scope:** Fixed 12-turn horror MVP with bounded LLM narration and one-query-per-turn interaction

---

## 1. Purpose

This document translates the revised project direction into a practical implementation plan for a Textual-based build.

The new version keeps the original strengths of the project:

- horror-first presentation
- fixed authored run
- data-driven content
- small UI surface area
- one main gameplay screen
- deterministic resource and condition logic

It adds one carefully bounded feature layer:

- LLM-generated scene narration
- one brief in-fiction query response per turn
- free-text commitment input that collapses into the same 4 canonical actions

The most important architectural rule is still:

> Keep all gameplay truth in plain Python. Use the LLM for language, not rules.

---

## 2. High-Level Recommendation

For this version, the safest architecture is:

**data-driven content + deterministic game engine + bounded narration layer + thin Textual UI shell**

That means:

- authored turn data still lives in content files
- turn resolution still lives in engine files
- LLM calls are isolated in a narration layer
- widgets render state and collect text input, but do not decide outcomes
- the controller remains the only boundary between UI and game logic

This keeps the project testable and prevents the language layer from silently taking over the rules.

---

## 3. Core Architectural Rules

### 3.1 Engine truth is absolute

The engine owns:

- turn order
- resources
- active conditions
- strong vs partial vs wrong resolution
- acute penalties
- win/loss checks
- SCAN-specific diagnostic power
- query limits

The LLM must never alter any of these.

### 3.2 The LLM is a bounded presentation service

The LLM may:

- render the current turn into atmospheric prose
- answer one brief in-fiction query per turn
- classify free text into `QUERY` or `COMMITMENT`
- classify commitment text into one canonical action
- render deterministic aftermath text

The LLM must not:

- invent new actions
- invent new hidden conditions
- decide success
- reveal hidden truth that has not been exposed
- continue the turn as an open-ended conversation

### 3.3 One controller boundary

The UI should talk to exactly one high-level object, such as `GameController`.

The UI should not know:

- whether a turn was narrated by the LLM or fallback text
- how intent classification works internally
- how conditions escalate
- how penalties resolve

### 3.4 The run must survive LLM failure

The game must remain fully playable if the model:

- times out
- returns invalid JSON
- misclassifies input with low confidence
- is temporarily unavailable

Fallback behavior is required, not optional.

---

## 4. Revised System Shape

A practical system boundary for this build looks like this:

```text
Textual UI
  -> GameController
      -> TurnFlow / Resolver / Conditions / Deck
      -> NarrationService
          -> SceneBuilder
          -> QueryResponder
          -> IntentParser
          -> AftermathWriter
          -> SchemaValidator
          -> FallbackText
```

### Data flow summary

1. Engine advances turn and exposes deterministic state.
2. Narration layer turns that state into a bounded scene packet.
3. LLM renders scene text or fallback text is used.
4. Player enters either a query or a commitment.
5. Intent parser classifies the input.
6. If query: one brief answer is returned, then the turn continues.
7. If commitment: input is mapped to one of 4 actions.
8. Engine resolves the action deterministically.
9. Narration layer renders aftermath from the resolved outcome.
10. UI refreshes the screen.

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
      scene_panel.py
      ai_panel.py
      input_panel.py
      log_panel.py
      overlay_panel.py
      status_bar.py

    engine/
      __init__.py
      controller.py
      state.py
      models.py
      resolver.py
      turn_flow.py
      conditions.py
      formatting.py
      queries.py

    narration/
      __init__.py
      client.py
      scene_builder.py
      prompts.py
      schemas.py
      parser.py
      responder.py
      fallback.py

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
      test_intent_parser.py
      test_query_limits.py
      test_narration_schemas.py
      test_fallback_mode.py
      test_determinism.py
```

---

## 6. File Responsibilities

## 6.1 `main.py`

Owns the Textual app entrypoint.

Responsibilities:

- define the `App` subclass
- load global CSS
- push the intro screen on startup
- create any shared services if you want app-level dependency wiring

Keep this file small.

---

## 6.2 `screens/`

### `intro_screen.py`

Responsibilities:

- show title and intro text
- explain the input model briefly
- allow start
- optionally allow quit

### `game_screen.py`

Responsibilities:

- compose the gameplay layout
- show current scene text
- accept free-text input
- show whether query budget is still available
- route input to the controller
- refresh widgets from returned state
- show fallback indicators only if useful for debugging
- move to end screen when the game ends

This remains the main screen and the center of the UI.

### `end_screen.py`

Responsibilities:

- show win/loss outcome
- show a brief final summary
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

### `scene_panel.py`
Shows:

- current narrated scene block
- any brief query response
- current visible readouts when fallback text is active

### `ai_panel.py`
Shows:

- current AI line or AI-highlighted sentence within the scene block
- optional AI-state styling

### `input_panel.py`
Shows:

- one text box
- submit hint
- fallback hotkey hints for explicit actions
- a short line such as `QUERY AVAILABLE` or `COMMITMENT REQUIRED`

### `log_panel.py`
Shows:

- aftermath lines
- recent turn results
- system messages such as `Input unclear. Use 1-4 or rephrase.`

### `status_bar.py`
Shows:

- whether query budget is spent
- whether fallback text is active
- whether the last interpretation was `QUERY` or `COMMITMENT`

### `overlay_panel.py`
Shows:

- corruption flashes
- false alerts
- duplicated text
- brief interruption banners

---

## 6.4 `engine/`

This remains the true game layer.

### `models.py`
Contains shared models and enums.

Examples:

- `Action`
- `AIState`
- `InputKind`
- `ResolutionTier`
- `TurnCard`
- `AcutePenalty`
- `Resources`
- `ActiveConditions`
- `NarrationMode`

### `state.py`
Contains the main state dataclasses.

### `resolver.py`
Contains action resolution logic.

Responsibilities:

- determine strong vs partial vs wrong resolution
- apply action effects
- apply battery costs
- apply acute penalties when not canceled
- select deterministic aftermath facts

### `turn_flow.py`
Contains turn progression logic.

Responsibilities:

- apply passive pressure
- apply persistent condition drains
- set up current turn packet
- enforce query limit reset per turn
- advance turn count
- check win/loss

### `conditions.py`
Owns condition-specific helpers.

Responsibilities:

- leak stage logic
- power bleed stage logic
- pursuit suppression rules
- contamination flags
- query contamination behavior flags if needed

### `queries.py`
Owns query-related engine rules.

Responsibilities:

- track one-query-per-turn usage
- distinguish descriptive questions from diagnostic boundaries
- provide any engine-side hint flags for allowed answers

### `controller.py`
Provides the clean API used by the UI.

### `formatting.py`
Contains helpers for player-facing display values.

Examples:

- threat label conversion
- system banners
- fallback notices for debug mode

---

## 6.5 `narration/`

This folder isolates all model-facing logic.

### `client.py`
Single place for model calls.

Responsibilities:

- send prompt payloads
- enforce timeouts
- return raw responses
- never leak model details into game logic

### `scene_builder.py`
Builds structured prompt/context from `GameState + TurnCard + visible facts`.

Responsibilities:

- gather required scene facts
- gather misleading facts
- gather carryover condition facts
- gather query budget state
- gather forbidden claims

### `prompts.py`
Stores prompt templates for:

- scene narration
- input classification
- query response
- aftermath narration

### `schemas.py`
Defines strict validated shapes for every model response.

### `parser.py`
Maps player free text into:

- `QUERY`
- `COMMITMENT`

and, for commitments:

- `SCAN`
- `REPAIR`
- `SILENT`
- `REROUTE`

### `responder.py`
High-level service wrapper used by the controller.

Responsibilities:

- narrate scene
- answer query
- classify input
- narrate aftermath
- trigger fallback paths on failure

### `fallback.py`
Contains authored fallback scene and aftermath rendering.

This file is mandatory. It is what keeps the project shippable.

---

## 6.6 `content/`

This folder still holds all authored content.

### `actions.py`
Define action identity and baseline values.

### `deck.py`
Define the fixed 12-turn sequence.

Each entry should now contain:

- turn number
- AI state
- acute penalty
- strong action
- required scene facts
- misleading facts
- query answer facts
- diagnostic boundary notes
- optional scan result
- optional partial outcome notes
- fallback scene lines
- fallback aftermath lines
- purpose note

### `text.py`
Store:

- intro text
- win text
- loss text
- generic clarification messages
- generic fallback messages

---

## 7. Revised Core Data Model

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


class InputKind(Enum):
    QUERY = auto()
    COMMITMENT = auto()
    UNKNOWN = auto()


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
    ai_state: AIState
    strong_action: Action
    acute_penalty: dict | None = None
    required_scene_facts: list[str] = field(default_factory=list)
    misleading_facts: list[str] = field(default_factory=list)
    query_answer_facts: list[str] = field(default_factory=list)
    forbidden_claims: list[str] = field(default_factory=list)
    fallback_scene_lines: list[str] = field(default_factory=list)
    fallback_aftermath_lines: dict[Action, list[str]] = field(default_factory=dict)
    scan_result: str | None = None


@dataclass
class QueryState:
    used_this_turn: bool = False
    last_query: str | None = None
    last_query_response: str | None = None


@dataclass
class NarrationState:
    current_scene_text: str = ""
    last_aftermath_text: str = ""
    fallback_used: bool = False
    last_input_kind: InputKind | None = None
    interpreted_action: Action | None = None
    interpretation_confidence: float = 0.0


@dataclass
class GameState:
    turn_index: int
    rescue_eta: int
    resources: Resources
    conditions: ActiveConditions
    query: QueryState = field(default_factory=QueryState)
    narration: NarrationState = field(default_factory=NarrationState)
    game_over: bool = False
    win: bool = False
    log: list[str] = field(default_factory=list)
```

This is still intentionally small.

Add state only when it directly supports:

- engine determinism
- query enforcement
- fallback handling
- UI rendering

---

## 8. Input and Query Model

The player can type free-form text, but the controller must place every input into exactly one of these buckets:

### 8.1 Query

Examples:

- `what is around me`
- `what changed`
- `where is that sound coming from`
- `what does the AI mean`

Rules:

- each turn allows at most one query response
- the answer must be brief and in-world
- the answer must only use exposed facts
- the answer must not reveal hidden truth that belongs to SCAN or to engine state
- once the query is spent, the player must commit

### 8.2 Commitment

Examples:

- `patch the seam`
- `kill the noise and stay still`
- `trace the signal`
- `reroute life support`

Rules:

- commitment text must resolve to exactly one canonical action
- mixed commitments should not generate hybrid rules
- if interpretation is unclear, fallback should request rephrase or explicit hotkey input

### 8.3 Unknown or ambiguous input

Examples:

- `maybe`
- `do something`
- `I don't know`

Rules:

- do not let the model improvise an action
- return a short clarification message
- offer explicit action hotkeys if needed

---

## 9. Recommended Schemas

Use strict validated outputs for every model call.

### 9.1 Scene narration schema

```python
{
  "scene_text": "string"
}
```

### 9.2 Input classification schema

```python
{
  "input_kind": "QUERY | COMMITMENT | UNKNOWN",
  "confidence": 0.0,
  "reason": "string"
}
```

### 9.3 Commitment interpretation schema

```python
{
  "action": "SCAN | REPAIR | SILENT | REROUTE",
  "confidence": 0.0,
  "reason": "string"
}
```

### 9.4 Query response schema

```python
{
  "response_text": "string"
}
```

### 9.5 Aftermath narration schema

```python
{
  "aftermath_text": "string"
}
```

### Important validation rule

Reject and fall back if:

- required keys are missing
- the action enum is invalid
- the response includes forbidden claims
- the query response is too long
- the model tries to give advice like `you should repair`

---

## 10. Controller API Recommendation

The UI should talk only to a controller object.

Example shape:

```python
class GameController:
    def new_game(self) -> GameState:
        ...

    def get_current_turn(self) -> TurnCard:
        ...

    def start_turn(self) -> GameState:
        ...

    def submit_text(self, text: str) -> GameState:
        ...

    def choose_action_fallback(self, action: Action) -> GameState:
        ...
```

### Recommended `submit_text()` flow

1. classify the input as query, commitment, or unknown
2. if query:
   - check query budget
   - generate brief query response or fallback response
   - update state without resolving the turn
   - return
3. if commitment:
   - map input to one canonical action
   - resolve action deterministically
   - narrate aftermath or fallback aftermath
   - clamp values
   - check loss state
   - advance turn or end game
   - return
4. if unknown:
   - return clarification message
   - do not advance turn

This keeps `GameScreen` simple and predictable.

---

## 11. Turn Flow Order

Use a strict turn order and do not vary it casually.

### Recommended order

1. start turn
2. apply passive pressure
3. apply active condition drains
4. load current turn card
5. build scene packet from deterministic state
6. generate scene text or fallback scene text
7. render scene and wait for player input
8. if player uses query and query is available:
   - answer briefly
   - return to input state
9. when player commits, classify commitment into canonical action
10. resolve action
11. apply acute penalty if needed
12. append aftermath text
13. clamp values
14. check immediate loss
15. advance to next turn or resolve rescue

This order should live in engine/controller code, not in widget callbacks.

---

## 12. Scene Packet Design

Each turn should be narrated from a structured packet, not from raw game state dumps.

A useful packet shape:

```python
{
  "turn": 7,
  "ai_state": "DEGRADED",
  "required_scene_facts": [
    "recycler cycle lengthening",
    "sonar return repeats at impossible distance"
  ],
  "misleading_facts": [
    "echo may seem like the main problem"
  ],
  "carryover_condition_facts": [
    "oxygen drain ongoing from power bleed"
  ],
  "query_budget_available": True,
  "forbidden_claims": [
    "do not say the true source is confirmed",
    "do not recommend an action"
  ],
  "ai_line_seed": "Load is slipping between circuits. The echo may be borrowing it."
}
```

### Why this matters

The prompt should not ask the LLM to invent a scene from scratch.
It should ask the LLM to phrase a constrained packet of facts.

That keeps tone flexible while preserving determinism.

---

## 13. Query Response Rules

The query system should preserve immersion without becoming the optimal strategy.

### Required behavior

A query response should be:

- short
- descriptive
- grounded in exposed facts
- uncertain where diagnosis would require SCAN
- non-directive

### Good query response pattern

- one sentence about the environment
- one sentence about a noticeable system or sound
- optional one sentence of ambiguity

### Bad query response pattern

- explicit strategic advice
- hidden diagnoses
- mechanical labels such as `this is a pursuit turn`
- long back-and-forth prompting the player to keep asking questions

### Recommended hard rule

Exactly one query response per turn.

---

## 14. Fallback and Failure Strategy

Fallback design is part of the main architecture.

### Trigger fallback when

- model call times out
- schema validation fails
- forbidden claims appear
- confidence is too low on commitment mapping
- response is too long or too chatty

### Fallback behaviors

#### Fallback scene
Use `fallback_scene_lines` from the turn deck.

#### Fallback query response
Use a generic constrained line such as:

- `The sub answers only with the same unstable signs.`
- `You get no clean certainty from the noise around you.`

#### Fallback commitment clarification
Use:

- `Input unclear. Rephrase or choose [1] SCAN [2] REPAIR [3] SILENT [4] REROUTE.`

#### Fallback aftermath
Use authored aftermath lines tied to the resolved action.

### Build discipline rule

Never block the turn because of narration failure.

---

## 15. Textual-Specific Guidance

## 15.1 Keep the UI narrow

The app still does not need many screens.

A small layout is enough:

- intro screen
- one gameplay screen
- end screen

## 15.2 Use one text input path

Do not build separate modes for query entry and action entry.

Use one input box and let the controller decide whether the player typed a query or a commitment.

## 15.3 Keep fallback actions visible

Even with free text, keep explicit action hotkeys visible:

- `1` = SCAN
- `2` = REPAIR
- `3` = SILENT
- `4` = REROUTE

This protects the demo and keeps testing fast.

## 15.4 Handle latency cleanly

LLM calls may take time. The UI should:

- disable duplicate submits while one call is active
- show a brief `PROCESSING...` or `LISTENING...` state
- avoid complex spinners or animation systems
- fail fast into fallback text

## 15.5 Prefer short model timeouts

For a hackathon build, faster mediocre narration is better than elegant stalls.

If a model call is slow, use fallback and continue.

---

## 16. Sample GameScreen Flow

A good gameplay screen can still follow a simple pattern:

```python
class GameScreen(Screen):
    def on_mount(self) -> None:
        self.controller = GameController()
        self.state = self.controller.new_game()
        self.state = self.controller.start_turn()
        self.refresh_from_state()

    def on_input_submitted(self, text: str) -> None:
        self.state = self.controller.submit_text(text)
        self.refresh_from_state()
        if self.state.game_over:
            self.app.push_screen(EndScreen(self.state.win, self.state.log))

    def on_key(self, event: events.Key) -> None:
        hotkey_map = {
            "1": Action.SCAN,
            "2": Action.REPAIR,
            "3": Action.SILENT,
            "4": Action.REROUTE,
        }
        if event.key in hotkey_map:
            self.state = self.controller.choose_action_fallback(hotkey_map[event.key])
            self.refresh_from_state()
```

### `refresh_from_state()` should

- update header
- update resources
- update scene text
- update AI styling
- update query availability indicator
- update log
- update overlay state
- update any debug fallback flags if desired

It should not make gameplay decisions.

---

## 17. Recommended Build Order

This is the safest order for the revised scope.

### Phase 1: Engine first

1. implement `GameState`
2. implement `TurnCard`
3. implement passive pressure
4. implement active condition drain logic
5. implement action resolution
6. implement win/loss checks
7. implement query budget tracking

Do this without Textual imports and without real model calls.

### Phase 2: Fallback-first narration path

8. create scene packet builder
9. create fallback scene renderer
10. create fallback query responder
11. create fallback aftermath renderer
12. connect the controller to a fully playable no-LLM loop

At this point the game should already be shippable.

### Phase 3: Intent parsing layer

13. add input classification schema
14. add commitment-to-action mapping
15. keep hotkey fallback active
16. test ambiguous inputs heavily

### Phase 4: Live narration layer

17. add scene narration call
18. add one-query response call
19. add aftermath narration call
20. add timeout and schema validation

### Phase 5: UI integration

21. add text input box
22. add query availability indicator
23. add processing state
24. confirm the whole 12-turn run works with and without the model

### Phase 6: Effects last

25. add corruption overlay
26. add one or two visual distortions
27. stop adding systems

---

## 18. Testing Priorities

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
- query budget resets per turn
- turn advancement works
- rescue/win condition triggers on final survival

### `test_intent_parser.py`
Check:

- varied phrasings map to the correct action
- noisy phrasings return `UNKNOWN` when needed
- mixed-action phrasings do not produce hybrid actions

### `test_query_limits.py`
Check:

- one query is allowed per turn
- second query does not produce another rich answer
- diagnostic questions stay uncertain when they should

### `test_narration_schemas.py`
Check:

- all scene outputs validate
- all query outputs validate
- all aftermath outputs validate
- forbidden claims are detected

### `test_fallback_mode.py`
Check:

- game remains fully playable if every model call fails
- explicit action hotkeys always work
- fallback scene and aftermath text render correctly

### `test_determinism.py`
Check:

- the same engine state and same interpreted action always produce the same resource result
- narration changes wording only, never mechanics

---

## 19. Styling Guidance

Keep styling simple and hostile-looking.

### Recommended visual priorities

- strong panel borders
- readable spacing
- subdued palette
- threat label emphasized more than other stats
- corruption overlays used sparingly
- text input clearly visible but not dominant

### Avoid

- elaborate CSS experiments
- separate chat-style transcript panes
- sprawling command history systems
- large layout rewrites after the input loop works

A clean terminal look is still better than a flashy half-finished one.

---

## 20. Scope Protection Rules

During the hackathon, do not add any of the following unless the full 12-turn run is already complete and playable with and without the narration layer:

- open-ended multi-turn dialogue with the LLM
- dynamic procedural deck generation
- LLM-owned hidden truth
- dynamic AI trust simulation
- free-text puzzle parsing beyond action mapping
- separate UI modes for questions versus actions
- large memory or lore systems
- advanced animation frameworks
- effect-heavy transitions every turn

The project wins by shipping a complete oppressive run with bounded expressive input, not by partially shipping an AI dungeon.

---

## 21. Final Recommendation

The right implementation strategy for this revised project is:

- build the full deterministic engine first
- keep the deck and authored outcomes in data
- add a fallback-only free-text loop before live model calls
- let the LLM narrate scenes, answer one brief query, and classify commitment text
- never let the LLM own rules, state, or outcomes
- keep one gameplay screen
- keep hotkey fallback visible at all times
- add polish only after the full run works end to end

In practical terms, the architecture should stay:

> **small, data-driven, testable, and language-rich on the surface only**

That is the best fit for a Textual-based deep-sea horror hackathon MVP with bounded LLM interaction.
