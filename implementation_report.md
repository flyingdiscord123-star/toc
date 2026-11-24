# CommonsSim Implementation Report

## 1. Project Overview

CommonsSim is a modular, multi-agent shared-resource simulation. It combines a React/TypeScript frontend, a FastAPI backend, and a Python simulation engine.

The implementation models:

- Heterogeneous agents with wealth and sustainability preferences.
- A renewable shared resource pool.
- Candidate extraction actions.
- Quota governance.
- Controlled exploration.
- SVO-based utility evaluation.
- Gradient-based learning of agent preferences.
- Trust, memory, metrics, and network observations.

Tax functionality is not part of the current implementation.

## 2. Architecture

### Frontend

The frontend is implemented with React and Vite in `frontend/src/`.

- `pages/Simulation.tsx` owns the active configuration and simulation result.
- `components/simulation/SimulationForm.tsx` renders the configuration controls.
- `types/simulation.ts` defines frontend request and response types.
- `services/api.ts` sends configuration to the backend.
- `components/simulation/ResultsPanel.tsx` renders metrics and charts.

### Backend

The backend is a FastAPI application.

- `api/main.py` creates the application and enables CORS.
- `api/schemas.py` validates request fields.
- `api/routes.py` converts requests into simulation dataclasses and serializes results.
- `config/simulation_config.py` defines the central Python configuration models.

### Simulation engine

The engine is divided into modular packages:

- `simulation.py`: constructs and owns the simulation components.
- `engine/simulator.py`: executes rounds.
- `environment/`: manages resource stock and regeneration.
- `agents/`: manages agent state, decisions, observations, and learning.
- `network/`: creates the interaction graph and observations.
- `governance/`: evaluates quota rules and produces action outcomes.
- `learning/`: implements learning algorithms.
- `trust/`: maintains trust relationships.
- `metrics/`: records per-round and final metrics.

## 3. Utility Function

The active utility function is `SVOUtilityFunction`, defined in `agents/utility/aggregator.py`. `LinearUtilityFunction` is an alias for this implementation.

### Wealth utility

For a candidate extraction `x`, the implementation first clamps the extraction against the current resource stock:

```text
feasible x = min(max(x, 0), available stock)
wealth fraction = feasible x / maximum capacity
wealth utility = wealth fraction ^ 0.92
```

The exponent `0.92` creates concave wealth utility, so additional extraction produces diminishing marginal benefit.

### Sustainability utility

The implementation calculates projected stock after extraction and regeneration:

```text
post-extraction stock = available stock - feasible x
projected stock = post-extraction stock * (1 + regenerationRate / 100)
stock fraction = clamp(projected stock / maximum capacity, 0, 1)
sustainability utility = stock fraction ^ 0.85
```

The exponent `0.85` makes sustainability utility concave and increases the cost of depleted resource states.

### Character weighting

Each agent has a mutable Social Value Orientation angle, `theta`, in radians:

```text
wealth weight = cos(theta)
sustainability weight = sin(theta)
```

The final utility is:

```text
U(x) =
    cos(theta) * wealth utility
  + sin(theta) * sustainability utility
```

Initial character angles are:

- Greedy: `0` radians, favoring immediate wealth.
- Cooperative: `64` degrees, providing a stronger sustainability weight.
- Risk-averse: `67` degrees, currently the highest initial sustainability orientation.

The angle is mutable during learning, while `initialTheta` remains fixed as the profile anchor.

## 4. Exploration

Exploration is implemented in `agents/policies/utility_maximization.py`.

### Candidate generation

The policy generates 41 evenly spaced candidate extraction amounts from zero to a cap:

```text
reserve = reserveFraction * maximumCapacity
stock-cap = harvestFraction
          * max(availableStock - reserve, 0)
          / numAgents

candidate cap = min(stock-cap, quotaLimit)
```

When no stock and capacity are provided, the policy falls back to the quota limit.

The default values are:

- `harvestFraction = 0.05`
- `reserveFraction = 0.05`
- `numCandidates = 41`

### Candidate ranking

The policy evaluates every candidate using the utility function and sorts candidates from highest to lowest utility.

### Exploration behavior

Each agent decision follows this process:

1. Select the highest-ranked candidate.
2. Generate a random number using the agent's seeded random generator.
3. If the number exceeds `explorationProbability`, return the highest-ranked candidate.
4. If exploration occurs, consider the upper 50% of ranked candidates below the best candidate.
5. Exclude alternatives with lower utility than the no-harvest candidate.
6. Randomly select from the remaining worthwhile alternatives.
7. Return the best candidate if no worthwhile alternative exists.

Exploration is therefore bounded and still utility-guided. It does not select arbitrary extraction amounts. Each agent receives a deterministic seed derived from the network random seed and agent ID.

## 5. Gradient Learning

Gradient learning is implemented by `SVOGradientLearning` in `learning/gradient_utility.py`.

The default configuration is:

- `learningRate = 0.01`
- `anchorLambda = 0.20`

### Learning experience

After an action, the engine creates a learning experience containing:

- Pre-action observation.
- Selected action.
- Predicted utility.
- Chosen wealth utility.
- Chosen sustainability utility.
- Realized reward.
- Maximum capacity used for normalization.
- Character profile.

### Update rule

The implementation first computes normalized realized reward and prediction error:

```text
realized normalized = realizedReward / normalizationCapacity
prediction error = realized normalized - predictedUtility
```

It then computes the analytical gradient of utility with respect to `theta`:

```text
gradient =
    -sin(theta) * chosenWealthUtility
  + cos(theta) * chosenSustainabilityUtility
```

The provisional angle is:

```text
new theta =
    theta
  + learningRate
  * predictionError
  * gradient
```

The result is clamped to the valid range:

```text
theta = clamp(new theta, 0, pi/2)
```

Finally, baseline anchoring is applied:

```text
theta =
    (1 - anchorLambda) * clampedTheta
  + anchorLambda * initialTheta
```

Lower angles increasingly favor wealth. Higher angles increasingly favor sustainability.

The `anchorLambda` parameter prevents learned preferences from drifting fully away from the agent's original character profile.

## 6. Quota Governance

Quota governance consists of a rule and a mechanism adapter.

### Quota rule

`governance/rules/quota_rule.py` implements `QuotaRule`.

It rejects an action when:

```text
requested extraction > quotaLimit
```

The rule returns an allowed result or a violation reason in the form:

```text
Extraction exceeds quota (<quotaLimit>)
```

### Quota mechanism

`governance/mechanisms/quota.py` adapts the rule engine result into the simulation's `ActionOutcome`.

For a violation, it sets:

- `approved_extraction = 0`
- `net_resources_received = 0`
- `compliant = False`
- `violation_reason` to the quota explanation

The agent receives no resources from a rejected extraction.

### Construction

`simulation.py` registers both `QuotaRule` and `QuotaMechanism` when `quotaEnabled` is true.

The quota limit is also passed into:

- Agent candidate generation.
- Agent observations.

This means policy decisions are quota-aware while the mechanism remains a final governance check.

## 7. Resource Environment

### Resource pool

`environment/resource_pool.py` stores:

- Initial resource quantity.
- Maximum capacity.
- Available resource quantity.
- Resource regeneration model.

Extraction removes the minimum of the approved request and available stock:

```text
actual extraction = min(requested extraction, available stock)
available stock -= actual extraction
```

Negative extraction requests are rejected.

### Linear regeneration

`environment/resource_model.py` implements linear percentage regeneration:

```text
new stock =
    current stock * (1 + regenerationRate / 100)
new stock = min(new stock, maximumCapacity)
```

Regeneration occurs after every complete round, after all agents have acted.

## 8. Agent Interaction

### Observation

`network/observer.py` constructs an `AgentObservation` containing:

- Round number.
- Resource snapshot.
- Maximum capacity.
- Regeneration rate.
- Quota limit.
- Neighbor observations.

A neighbor observation includes neighbor ID, wealth, and alive status.

The API currently creates a complete graph, so every agent can observe every other agent.

### Decision

An agent:

1. Receives its observation.
2. Generates candidate extraction amounts.
3. Evaluates candidates using the active utility function.
4. Optionally explores an alternative candidate.
5. Sends the selected action to the governance mechanism.
6. Extracts the approved amount.
7. Records the outcome.
8. Updates learning and trust.

### Shared resource interaction

Agents act sequentially. Earlier agents reduce the available stock before later agents decide. Every successful extraction increases that agent's wealth.

The current implementation does not add removed resources to a public fund or redistribute resources.

## 9. Round Lifecycle

`engine/simulator.py` executes each round as follows:

1. Snapshots the environment.
2. Orders agents with `SequentialScheduler`.
3. Builds an observation for each agent.
4. Selects an action using utility and exploration.
5. Applies quota governance.
6. Extracts actual stock from the resource pool.
7. Updates agent wealth.
8. Evaluates utility.
9. Creates an experience and records it in memory.
10. Updates trust.
11. Updates the agent's SVO angle through gradient learning.
12. Regenerates the resource pool.
13. Increments the round number.
14. Records round metrics.

The run returns when the configured number of rounds is reached.

With `rounds = 0`, no agent actions or round metrics are executed.

## 10. Trust and Metrics

Trust is maintained by `trust/trust_engine.py`. After each action, the engine updates a trust interaction using the agent's compliance status:

- Compliant action: successful interaction.
- Quota violation: unsuccessful interaction.

`metrics/collector.py` stores immutable round records containing:

- Round number.
- Resource level.
- Average and total wealth.
- Average trust.
- Quota violations.
- Successful extraction count.
- Average harvest for greedy, cooperative, and risk-averse agents.

## 11. API Configuration

The frontend sends:

- Agent count and population percentages.
- Initial resources.
- Regeneration rate.
- Number of rounds.
- Quota enabled state.
- Quota limit.
- Exploration probability.

The API additionally maps the request into:

- Complete network topology.
- SVO-gradient learning.
- The agent and environment dataclasses.
- The configured decision and quota settings.

Backend validation enforces:

- Agent population percentages sum to 100.
- Quota limit is between 0 and 100.
- Rounds are between 0 and 100.
- Exploration probability is between 0 and 1.
- Agent count is positive.

## 12. Execution Data Flow

```text
User Input
  -> Frontend Configuration
  -> POST /api/simulations
  -> Pydantic Validation
  -> Core Dataclass Configuration
  -> Simulation.initialize()
  -> Environment and Agent Construction
  -> Agent Observation
  -> Utility Ranking
  -> Exploration
  -> Quota Validation
  -> Resource Extraction
  -> Gradient Learning
  -> Trust and Metrics Updates
  -> Resource Regeneration
  -> JSON Result
  -> React Charts
```

## 13. Important Files

- `frontend/src/pages/Simulation.tsx`: active frontend state.
- `frontend/src/components/simulation/SimulationForm.tsx`: configuration UI.
- `frontend/src/components/simulation/ResultsPanel.tsx`: result UI.
- `frontend/src/services/api.ts`: Axios API client.
- `api/schemas.py`: request validation.
- `api/routes.py`: API orchestration.
- `config/simulation_config.py`: central configuration.
- `simulation.py`: component construction.
- `engine/simulator.py`: round execution.
- `agents/utility/aggregator.py`: SVO utility implementation.
- `agents/policies/utility_maximization.py`: ranking and exploration.
- `agents/character.py`: SVO profiles.
- `learning/gradient_utility.py`: theta gradient learning.
- `governance/rules/quota_rule.py`: quota rule.
- `governance/mechanisms/quota.py`: quota outcome adaptation.
- `environment/resource_pool.py`: shared resource storage.
- `environment/resource_model.py`: linear regeneration.
- `network/observer.py`: neighborhood observations.
- `metrics/collector.py`: metrics history.

## 14. Current Assumptions

- API-created simulations use complete-network topology.
- Agents act sequentially.
- Initial agent wealth is zero.
- The active utility exponents are fixed at 0.92 and 0.85.
- The active governance mechanism is quota.
- Exploration candidates are limited to highly ranked alternatives.
- Learning updates an SVO angle after each action.
- No tax, subsidy, or redistribution mechanism is active.
- Resource regeneration is linear and capped at maximum capacity.
- A final resource level above 12% of initial resources is considered sustained.
