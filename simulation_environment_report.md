# Simulation Environment Report

## 1. High-Level Architecture

CommonsSim contains a React/TypeScript frontend and a Python/FastAPI backend.

### Frontend

- `frontend/src/pages/Simulation.tsx` owns the current `SimulationConfig` and run state.
- `frontend/src/components/simulation/SimulationForm.tsx` provides population, resource, governance, and decision-policy controls.
- `frontend/src/types/simulation.ts` defines request and response types.
- `frontend/src/services/api.ts` sends a configuration to `POST /api/simulations`.
- `frontend/src/components/simulation/ResultsPanel.tsx` renders final metrics and per-round charts.

### Backend

- `api/main.py` creates the FastAPI application and CORS policy.
- `api/schemas.py` validates and maps JSON fields to Pydantic models.
- `api/routes.py` converts API models into dataclass configuration and serializes simulation results.
- `config/simulation_config.py` contains the central configuration dataclasses.

### Simulation engine

- `simulation.py` constructs the complete component graph for a run.
- `engine/simulator.py` executes the round loop.
- `environment/` manages the shared renewable stock.
- `agents/` manages observations, characters, states, memories, decisions, and learning.
- `network/` builds the interaction graph and agent observations.
- `governance/` evaluates quota rules and adapts rule results to action outcomes.
- `learning/` implements and creates learning algorithms.
- `trust/` maintains and updates pairwise trust.
- `metrics/` records round-level and final metrics.

### Communication flow

```text
React controls
  -> SimulationConfig
  -> POST /api/simulations
  -> Pydantic validation
  -> Python configuration dataclasses
  -> component construction
  -> round execution
  -> JSON result
  -> React charts and metric cards
```

## 2. Implemented Simulation Configuration

### Environment

- `rounds`: 0–100 backend rounds. The frontend default is 50.
- `initialResources`: initial shared resource amount.
- `maximumCapacity`: maximum resource pool capacity.
- `regenerationRate`: percentage increase in post-harvest stock per round.
- `harvestFraction`: fraction used to derive the stock-aware per-agent candidate cap.
- `reserveFraction`: reserve portion of capacity excluded before choosing candidate actions.

### Agent population

- `numAgents`: number of agents.
- `greedyPercentage`: population percentage assigned the greedy profile.
- `cooperativePercentage`: population percentage assigned the cooperative profile.
- `riskAversePercentage`: population percentage assigned the risk-averse profile.
- The three percentages must sum to 100.
- `explorationProbability`: 0–1 probability of choosing an alternative ranked action.

### Governance

- `quotaEnabled`: enables or disables quota governance.
- `quotaLimit`: maximum extraction per agent action, constrained to 0–100.

### Network

- `topology`: complete, ring, random, small-world, or scale-free.
- The current API path and graph implementation use the complete topology.
- `averageDegree`, `rewiringProbability`, and `randomSeed` are retained configuration fields.

### Learning

- `learningAlgorithm`: implementation selected from the learning factory.
- `learningRate`: step size for the SVO gradient update.
- `anchorLambda`: strength of updating toward the character's initial SVO angle.

The API currently constructs `SVOGradientLearning` with defaults of 0.01 learning rate and 0.20 anchor lambda.

## 3. Utility Function Implementation

The active utility implementation is `SVOUtilityFunction`, also exported as `LinearUtilityFunction`, in `agents/utility/aggregator.py`.

### Wealth component

For an extraction amount `x`, current stock `S`, and capacity `C`:

```text
feasible x = min(max(x, 0), S)
W = (feasible x / C) ^ 0.92
```

The wealth exponent of 0.92 makes the component concave, giving diminishing marginal utility for larger harvests. The value is always clamped to the 0–1 range.

### Sustainability component

The implementation projects resource stock immediately after extraction and linear regeneration:

```text
post-extraction stock = S - feasible x
projected stock = post-extraction stock * (1 + regenerationRate / 100)
stock fraction = clamp(projected stock / C, 0, 1)
Sustainability = stock fraction ^ 0.85
```

The exponent 0.85 is also concave. It rewards leaving more projected stock, especially when depletion is severe.

### Social value orientation weighting

The character stores a mutable angle `theta` between 0 and `pi/2`. The weights are:

```text
wealth weight = cos(theta)
sustainability weight = sin(theta)
```

The final utility is:

```text
U(x) = cos(theta) * W(x) + sin(theta) * Sustainability(x)
```

Initial character profiles are:

- Greedy: 0 radians.
- Cooperative: 64 degrees.
- Risk-averse: 67 degrees.

The `Character.initial_theta` is immutable and is used as an anchor by gradient learning. Character theta is mutable and can adapt over rounds.

## 4. Candidate Generation and Exploration

Candidate actions are implemented in `agents/policies/utility_maximization.py`.

The implementation creates 41 evenly spaced extraction amounts from zero through a cap:

```text
reserve = reserveFraction * maximumCapacity
per-agent stock cap =
    harvestFraction * max(availableStock - reserve, 0) / numAgents
candidate cap = min(per-agent stock cap, quotaLimit)
```

When stock and capacity are not supplied, the policy falls back to the quota limit. Each action is evaluated with the SVO utility function and then sorted in descending utility.

### Exploration algorithm

On every decision:

1. Select the highest-utility candidate as the default action.
2. Draw a random value for the configured exploration probability.
3. If no exploration occurs, return the default action.
4. If exploration occurs, find the top 50% of candidates excluding the best action.
5. Exclude candidates whose utility is below the no-harvest candidate's utility.
6. Randomly choose one of the remaining worthwhile alternatives.
7. If no worthwhile alternative exists, retain the highest-utility action.

Exploration therefore adds bounded stochastic variation rather than replacing utility maximization. It uses a seed-specific `random.Random` instance, with the seed assigned by agent ID in the default simulation construction.

## 5. Gradient Learning Implementation

Gradient learning is implemented in `learning/gradient_utility.py` using `SVOGradientLearning`.

For each agent experience:

```text
realized = realizedReward / normalizationCapacity
prediction error = realized - predictedUtility
gradient = -sin(theta) * chosenW + cos(theta) * chosenS
new theta = theta + learningRate * prediction error * gradient
new theta = clamp(new theta, 0, pi/2)
anchored theta =
    (1 - anchorLambda) * clamped theta
    + anchorLambda * initialTheta
```

The learning update therefore moves the SVO angle within the valid range:

- Lower theta favors wealth.
- Higher theta favors sustainability.

The prediction error compares normalized realized reward with the utility predicted for the chosen action. The analytical gradient differentiates the weighted utility expression with respect to theta. `anchorLambda` prevents learned preferences from drifting arbitrarily far from the original character profile.

During simulator execution, the learning experience includes:

- the pre-action observation;
- the chosen action;
- predicted utility;
- chosen wealth and sustainability values;
- normalized realized reward;
- maximum capacity used for normalization;
- the character profile.

After each round action, `agent.learning_model.update(...)` applies this update.

## 6. Quota Governance Implementation

Quota governance is implemented as a rule plus a mechanism adapter.

### Quota rule

`governance/rules/quota_rule.py` rejects an action if:

```text
requested extraction > quotaLimit
```

The returned `RuleResult` contains `allowed=False` and a human-readable quota violation reason.

### Mechanism adapter

`governance/mechanisms/quota.py` applies the rule through `RuleEngine` and transforms the canonical `ActionOutcome` when extraction violates the quota:

- `approved_extraction = 0`
- `net_resources_received = 0`
- `compliant = False`
- `violation_reason` receives the quota rule reason

The violation is counted in round metrics and recorded as unsuccessful compliance for trust updates.

### Construction

`simulation.py` registers `QuotaRule` and `QuotaMechanism` only when `quotaEnabled` is true. The quota limit is also passed into the candidate-generation policy, so normal API runs usually generate actions no larger than the quota.

The mechanism remains a defense against actions above the configured limit.

## 7. Environment Lifecycle and Round Execution

1. `Simulation.initialize()` builds the resource model, pool, environment, graph, agents, governance pipeline, trust engine, scheduler, and metrics collector.
2. `Simulator.run()` repeats for `rounds` iterations.
3. The engine snapshots the environment.
4. Agents are ordered by `SequentialScheduler`.
5. `ObservationBuilder` supplies resource stock, quota limit, and complete-network neighbor observations.
6. Each agent chooses an extraction action.
7. Governance modifies the action outcome if necessary.
8. The resource pool extracts only the approved amount that is physically available.
9. Actual income is added to agent wealth.
10. Utility and a learning experience are computed.
11. Experience is stored in memory and gradient learning is applied.
12. Trust is updated.
13. After all agents act, the environment applies linear regeneration and increments the round.
14. Round metrics are recorded.

For `rounds = 0`, the lifecycle performs no round actions or metrics collection and returns the initial resource state.

## 8. Resource Pool and Resource Dynamics

`ResourcePool.extract()` removes the smaller of the approved amount and the stock currently available. Negative extraction requests are rejected.

`LinearResourceModel.regenerate()` applies:

```text
new stock = current stock * (1 + regenerationRate / 100)
new stock = min(new stock, maximumCapacity)
```

Resource sustainability depends on extraction across every agent versus post-round regeneration.

The API labels the result sustained when final resource stock is greater than 12% of initial stock. Otherwise it labels the result collapsed.

## 9. Agent Interaction

Each agent receives:

- round number;
- current resource snapshot;
- maximum capacity;
- regeneration rate;
- quota limit;
- neighbor wealth and alive status.

Agents use this observation to rank extraction candidates. Neighbor observations currently come from the complete graph. The actual common-pool interaction occurs when each agent sequentially extracts from the shared `ResourcePool`; later agents observe the stock remaining after earlier actions.

The system does not implement tax collection or redistribution.

## 10. Data Flow

```text
User Input
  -> Frontend Configuration
  -> API Request Validation
  -> Simulation Dataclass Configuration
  -> Agent and Environment Construction
  -> Utility Evaluation
  -> Exploration
  -> Quota Governance
  -> Resource Extraction
  -> Gradient Learning
  -> Trust and Metrics Updates
  -> JSON Results
  -> React Visualizations
```

## 11. Important Implementation Files

- `frontend/src/pages/Simulation.tsx`: frontend run state.
- `frontend/src/components/simulation/SimulationForm.tsx`: frontend controls.
- `frontend/src/components/simulation/ResultsPanel.tsx`: frontend visualization.
- `frontend/src/services/api.ts`: HTTP integration.
- `api/schemas.py`: API validation.
- `api/routes.py`: API orchestration and result serialization.
- `config/simulation_config.py`: configuration contract.
- `simulation.py`: component construction.
- `engine/simulator.py`: execution loop.
- `agents/utility/aggregator.py`: active SVO utility function.
- `agents/character.py`: personality profiles and mutable SVO angle.
- `agents/policies/utility_maximization.py`: candidate generation and exploration.
- `learning/gradient_utility.py`: analytical SVO gradient update.
- `governance/rules/quota_rule.py`: quota validation.
- `governance/mechanisms/quota.py`: quota outcome adaptation.
- `environment/resource_pool.py`: stock extraction.
- `environment/resource_model.py`: regeneration strategy.
- `network/observer.py`: neighbor observation assembly.
- `metrics/collector.py`: round history.

## 12. Extension Points

### Utility functions

Implement or subclass `UtilityFunction` and replace `SVOUtilityFunction` in `Simulation._utility_function`. Add configurable exponents or new utility components through `agents/utility/`.

### Learning algorithms

Implement `LearningAlgorithm.update()` and reset behavior, then register the implementation in `learning/factory.py` and `LearningAlgorithm`.

### Quota rules

Implement a new `Rule` or `GovernanceMechanism`, then register it in `Simulation.initialize()`. API schemas and frontend controls can be added when configuration is needed.

### Exploration

Change ranking, top-k selection, fallback behavior, or random-source construction in `UtilityMaximizationPolicy`. The existing `explorationProbability` configuration is already propagated to this policy.

### Resource models

Implement `ResourceModel.regenerate()` and construct it in `Simulation.initialize()` instead of `LinearResourceModel`.

## 13. Current Assumptions

- API simulations use complete graph topology.
- There are 41 ranked candidate extraction actions per decision.
- SVO utility uses fixed wealth exponent 0.92 and sustainability exponent 0.85.
- Quota is the active governance mechanism.
- Exploration is only applied to candidates ranked below the current best.
- Learning uses realized reward, predicted utility, and analytical theta gradient.
- Agent wealth starts at zero.
- Agents act sequentially.
- Trust is updated after each action.
- Resource regeneration is linear and capped.
- Sustainability status is a fixed 12% final-stock threshold in the API.
