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
      ┌───────────────┼──────────────────────────────┐
      │               │             │                │
  Wealth     Sustainability      Trust       Compliance
                      │
                    Risk
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

Agents currently perform utility maximization.

For each timestep the agent:

1. Observes its environment
2. Generates candidate actions
3. Evaluates each action
4. Selects the action with maximum utility

---

## Utility Function

Utility is represented as a weighted combination of independent behavioural objectives.

Current utility components are:

- Wealth
- Sustainability
- Trust
- Compliance
- Risk

Each character type possesses its own preference weights over these components.

The modular design allows new utility dimensions to be introduced without modifying the decision-making algorithm.

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

Current implementation:

- NoLearning

The simulator architecture is designed to support future adaptive learning algorithms without modifying the surrounding system.

---

## Metrics

Metrics collected every simulation round include:

- Remaining resource level
- Average agent wealth
- Total wealth
- Average trust
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

Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install networkx
```

Run the integration simulation

```bash
python3 -m example.integration_test
```

Run the smoke test

```bash
python3 -m example.smoke_test
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

## Adaptive Learning

Current utility weights are fixed.

Future work will investigate learning algorithms that allow agents to adapt their behavioural preferences over time, including:

- Reinforcement Learning
- Bayesian Updating
- Evolutionary Learning

Learning will modify **agent preferences**, not governance policies.

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