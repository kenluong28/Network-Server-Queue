# M/M/1 and M/M/1/K Queue Simulation

## Overview
This project is part of ECE 358: Computer Networks at the University of Waterloo. It involves the simulation of M/M/1 and M/M/1/K queues to analyze queuing behavior in computer networks. The objective is to study the impact of queueing on network delay and packet loss.

## Details

### Objective
- Implement a Discrete Event Simulator (DES) for M/M/1 and M/M/1/K queues.
- Analyze the effect of various parameters on network delay and packet loss.
- Use statistical methods to evaluate the stability of the simulation results.

### Queue Models
M/M/1 Queue:
- Infinite buffer size.
- Packets arrive following a Poisson process.
- Service times follow an exponential distribution.
- No packet loss.

M/M/1/K Queue:
- Finite buffer size K.
- Packets arriving to a full queue are dropped.
- Packet loss probability PLOSS is computed.

## Installation and Dependencies

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Matplotlib (for graph visualization)
- NumPy (for statistical computations)

To install dependencies:
```
pip install numpy matplotlib
```

## Usage

### Running the Simulation

To execute the queue simulation, navigate to the project directory and run:
```
python lab1.py
```
Alternatively, use the Makefile:
```
make run
```
### Expected Output

The script generates:
- Performance Metrics: E[N] (Average queue size), PLOSS (Packet loss probability), PIDLE (Proportion of time the system is idle).
- Graphs illustrating the performance of M/M/1 and M/M/1/K queues as a function of system utilization (ρ).

## Questions Addressed in the Lab
Questions Addressed in the Lab
1. Generate and analyze 1000 exponential random variables.
2. Simulate the M/M/1 queue, analyzing E[N] and PIDLE as a function of ρ.
3. Extend the simulator to M/M/1/K and compute packet loss probability.
4. Compare the performance of different buffer sizes (K=10, 25, 50).
