# CommonsSim
### A Modular Multi-Agent Simulator for Studying Governance in the Tragedy of the Commons

## Overview

CommonsSim is a research-oriented simulation framework for studying how **externally imposed governance mechanisms** influence the behaviour of heterogeneous utility-maximizing agents competing over a shared renewable resource.

The project is inspired by the classic **Tragedy of the Commons**, but instead of assuming perfectly rational agents or emergent institutions, CommonsSim models agents with configurable preferences, trust dynamics, and (future) adaptive learning operating under **exogenous governance**.

The simulator has been designed from the ground up to be modular, allowing individual components such as governance policies, utility models, learning algorithms, and trust systems to evolve independently.

---

# Research Motivation

Many real-world commons problems—groundwater extraction, fisheries, forests, carbon emissions, cloud computing resources—are governed through externally imposed regulations such as taxes, quotas, fines, or subsidies.

This project asks:

- Which governance mechanisms produce sustainable outcomes?
- How do heterogeneous agent preferences affect policy effectiveness?
- Can adaptive agents learn behaviours that improve long-term sustainability?
- How does trust interact with governance and resource usage?

Rather than designing agents that invent institutions, CommonsSim assumes that governance is provided externally and studies how agents respond to it.

---

# Current Architecture

```
                 Simulation
                      │
      ┌───────────────┴────────────────┐
      │                                │
 Environment                      Interaction Network
      │                                │
      └───────────────┬────────────────┘
                      │
              Observation Builder
                      │
                      ▼
                    Agent
                      │
      ┌───────────────┼────────────────┐
      │               │                │
   Memory      Decision Policy     Learning
                      │
                      ▼
          Utility Maximization Policy
                      │
                      ▼
              Utility Function
                      │
      ┌───────────────┼────────────────┐
      │               │                │
    Gain       Sustainability        Risk
                      │
         Ranked Top-K with exploration
                      │
                      ▼
                Selected Action
                      │
                      ▼
               Governance Engine
                      │
                      ▼
              Environment Update
                      │
                      ▼
              Metrics Collection
```

---

# Current Features

## Environment

- Renewable shared resource pool
- Configurable regeneration model
- Resource extraction
- Capacity constraints

---

## Agents

Every agent consists of:

- Character profile
- Internal state
- Memory
- Utility function
- Decision policy
- Learning module

Current character archetypes include:

- Greedy
- Cooperative
- Risk Averse
- Opportunistic

---

## Decision Making

Agents evaluate evenly spaced harvest candidates between zero and a
stock-dependent, type-blind per-capita cap, rank those actions by utility,
and select the best action except for controlled exploration.

The decision policy:

1. Observes its environment
2. Generates 41 harvest candidates from `0` through the per-capita cap,
   additionally bounded by the quota when enabled
3. Evaluates and ranks every candidate
4. Selects the best action with probability `1 - exploration_probability`
5. Otherwise samples uniformly from the next-best half of candidates, but only
   among actions whose utility is at least as high as taking no harvest; if
   none qualify, it selects the best action

`exploration_probability` is configurable from 0 to 1 and defaults to 0.25.
When the network configuration has a random seed, each agent's decisions are
reproducible from that seed.

---

## Utility Function

Utility uses two capacity-normalized components:

- Wealth: `W(a) = (feasible_harvest / capacity) ** 0.92`
- Sustainability:
  `S(a) = (min(capacity, max(0, stock - harvest + regeneration)) / capacity) ** 0.85`

The shared score is `U(a) = cos(theta) * W(a) + sin(theta) * S(a)`.
Greedy, Cooperative, and Risk-Averse profiles use baseline angles of 0°, 64°,
and 67° respectively. The same utility and type-blind harvest cap apply to
every agent; only the SVO angle differs.

Regeneration is a percentage of the post-harvest stock each round:
`next_stock = min(capacity, stock_after_harvest * (1 + regeneration_rate / 100))`.
For example, a 2% rate adds 20 units to a stock of 1,000, or 10 units to a
stock of 500, before the capacity limit is applied.

---

## Governance

Current implementation:

- Rule Engine
- Rule Registry
- Quota Rule

Governance is **exogenous**.

Agents respond to governance policies but do not create or negotiate institutions.

---

## Trust

Current implementation includes:

- Trust Matrix
- Linear Trust Update
- Trust Engine

Trust evolves independently of governance and will later influence decision making.

---

## Learning

API simulations use `SVOGradient` learning by default. Each agent updates its
SVO angle after every round using the chosen Wealth and Sustainability scores,
with a learning rate of `0.01` and baseline-anchor strength of `0.20`.
Other simulation configurations may still select `NoLearning`.

Learning adapts agent preferences; it does not change governance policies.

---

## Metrics

Metrics collected every simulation round include:

- Remaining resource level
- Average agent wealth
- Total wealth
- Average trust
- Average realized harvest for Greedy, Cooperative, and Risk-Averse agents
- Successful extractions
- Governance violations

---

# Repository Structure

```
agents/
config/
engine/
environment/
governance/
learning/
metrics/
network/
trust/
example/
simulation.py
```

---

# Running the Simulator

Create and activate a virtual environment (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

Start the backend API from the repository root

```powershell
python -m uvicorn api.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`.

In a second terminal, start the frontend

```powershell
cd frontend
npm install
npm run dev
```

Run the integration simulation directly

```powershell
python -m example.integration_test
```

Run the smoke test

```powershell
python -m example.smoke_test
```

Run the architecture test

```bash
python3 -m example.simulation_test
```

---

# Current Project Status

## Completed

- Modular simulator architecture
- Renewable environment model
- Utility-maximizing agents
- Modular utility framework
- Governance engine
- Trust engine
- Metrics collection
- End-to-end integration tests

---

# Future Work

## Other Learning Algorithms

Future work may add other algorithms for adapting agent preferences, such as:

- Reinforcement Learning
- Bayesian Updating
- Evolutionary Learning

---

## Governance Policies

Current implementation supports quota-based regulation.

Future governance mechanisms include:

- Resource taxation
- Progressive taxation
- Fines for over-extraction
- Subsidies for cooperative behaviour
- Adaptive quota systems
- Reward-based incentive schemes

These policies remain externally imposed throughout the simulation.

---

## Richer Utility Models

Future work includes:

- Better normalization of utility components
- Context-aware utility evaluation
- Additional behavioural objectives
- Adaptive utility weights

---

## Trust Dynamics

Future trust models will investigate:

- Reputation systems
- Trust decay
- Forgiveness
- Indirect trust
- Trust-based cooperation

---

## Experimental Evaluation

The simulator will be used to compare governance mechanisms using metrics such as:

- Resource sustainability
- Collective welfare
- Policy compliance
- Trust evolution
- Governance effectiveness
- Long-term resource availability

---

# Long-Term Vision

CommonsSim aims to become a flexible experimental platform for studying the interaction between:

- Utility-maximizing agents
- Externally imposed governance
- Renewable shared resources
- Adaptive learning
- Trust dynamics

The goal is to provide a reusable framework for exploring how different governance mechanisms influence long-term sustainability and collective behaviour in common-pool resource systems.

---

# License

MIT License