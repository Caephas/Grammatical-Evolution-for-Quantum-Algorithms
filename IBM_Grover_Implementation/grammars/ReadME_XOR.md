# BNF Grammar for Deutsch's Algorithm Circuit Evolution (Qiskit)

## Overview

This BNF (Backus-Naur Form) grammar defines the structure for evolving quantum circuits that implement Deutsch's algorithm using IBM Qiskit. Deutsch's algorithm is a fundamental quantum algorithm that determines whether a binary function f: {0,1} → {0,1} is constant (always returns same value) or balanced (returns 0 for one input and 1 for the other) using only a single function evaluation.

## Grammar Structure

### Core Components

The grammar follows the canonical structure of Deutsch's algorithm:

```
Program → Initialize → Setup → Oracle → Final Processing → Measurement
```

### 1. **Program Structure** (`<Program>`)

The top-level rule defines the complete quantum circuit with:

- **Initialize**: Creates a 2-qubit circuit (1 input qubit, 1 ancilla)
- **InitialSetupSequence**: Prepares superposition and phase kickback setup
- **OraclePlaceholder**: Marks where the oracle will be injected
- **FinalSetupSequence**: Applies final Hadamard for interference
- **Measure**: Measures only the input qubit (qubit 0)

### 2. **Circuit Initialization** (`<Initialize>`)

```python
qc = QuantumCircuit(2, 1)  # 2 qubits, 1 classical bit
```

- **Qubit 0**: Input/query qubit
- **Qubit 1**: Ancilla qubit (for phase kickback)
- **Classical bit 0**: Stores measurement result

### 3. **Initial Setup Sequence** (`<InitialSetupSequence>`)

Three-step preparation process:

**Step 1** (`<InitialSetupStep1>`): Ancilla preparation

- Default: `qc.x(1)` - Prepares |1⟩ state
- Alternative: Other single-qubit gates for exploration

**Step 2** (`<InitialSetupStep2>`): Ancilla superposition

- Default: `qc.h(1)` - Creates |−⟩ = (|0⟩ - |1⟩)/√2
- Alternative: Other gates for variation

**Step 3** (`<InitialSetupStep3>`): Input superposition

- Default: `qc.h(0)` - Creates |+⟩ = (|0⟩ + |1⟩)/√2
- Alternative: Other gates for exploration

### 4. **Oracle Placeholder** (`<OraclePlaceholder>`)

```python
# ORACLE_INSERTION_POINT
```

- Marks where the problem-specific oracle will be injected
- Oracle implements the unknown function f(x)
- Different oracles for constant vs balanced functions

### 5. **Final Setup Sequence** (`<FinalSetupSequence>`)

```python
qc.h(0)  # Hadamard on input qubit
```

- Applies interference to extract global property
- Alternatives allow evolutionary optimization

### 6. **Optional Barriers** (`<OptionalBarrier>`)

- Can insert `qc.barrier()` for visual separation
- Helps with circuit visualization and optimization boundaries

## Gate Set

### Single-Qubit Gates on Input (Qubit 0)

- **Pauli/Clifford**: `x`, `h`, `s`, `sxdg` (SX†)
- **T gates**: `t`, `tdg` (T†)
- **Rotations**: `rx(π/2)`, `ry(π/4)`
- **Phase gates**: `p(π/4)`, `u1(π/3)`

### Single-Qubit Gates on Ancilla (Qubit 1)

- Same gate set as input qubit
- Applied to qubit 1 instead of qubit 0
- Allows independent evolution of both qubit preparations

## Algorithm Theory

### How Deutsch's Algorithm Works

1. **Initialization**:
   - Input qubit in |0⟩
   - Ancilla in |1⟩

2. **Superposition Creation**:
   - Input → |+⟩ = (|0⟩ + |1⟩)/√2
   - Ancilla → |−⟩ = (|0⟩ - |1⟩)/√2

3. **Oracle Application**:
   - Applies Uf|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
   - Phase kickback: |x⟩|−⟩ → (-1)^f(x)|x⟩|−⟩

4. **Interference**:
   - Final Hadamard on input qubit
   - Constructive/destructive interference reveals f's property

5. **Measurement**:
   - Measure qubit 0
   - Result 0 → f is constant
   - Result 1 → f is balanced

## Oracle Types (Injected Dynamically)

### Constant Functions

- **f(x) = 0**: Identity (no operation)
- **f(x) = 1**: Pauli-X on ancilla

### Balanced Functions

- **f(x) = x**: CNOT (control: input, target: ancilla)
- **f(x) = NOT(x)**: X on input, then CNOT

## Evolution Strategy

### What Evolves

- Variations in setup sequences (while maintaining algorithm structure)
- Presence of barriers for organization
- Alternative gate choices for state preparation
- Gate parameters for rotations

### What Remains Fixed

- 2-qubit structure (1 input, 1 ancilla)
- Oracle injection point
- Single measurement on input qubit
- Basic algorithm flow

## Example Generated Circuit

```python
qc = QuantumCircuit(2, 1)

# Initial setup
qc.x(1)      # Ancilla to |1⟩
qc.h(1)      # Ancilla to |−⟩
qc.h(0)      # Input to |+⟩

qc.barrier()  # Optional

# ORACLE_INSERTION_POINT
# [Oracle gates injected here during evaluation]

qc.barrier()  # Optional

# Final processing
qc.h(0)      # Interference

# Measurement
qc.measure(0, 0)
```

## Design Rationale

### Why This Structure?

1. **Algorithm Fidelity**: Preserves Deutsch's algorithm logic
2. **Minimal Circuit**: Only 2 qubits needed (optimal)
3. **Evolution Space**: Allows exploration while maintaining correctness
4. **Clear Separation**: Oracle injection point is unambiguous

### Grammar Features

- **Modular Design**: Each phase is clearly separated
- **Fixed Oracle Point**: Ensures oracle is placed correctly
- **Flexible Gates**: Allows discovery of equivalent preparations
- **Single Measurement**: Only measures the relevant qubit

### Trade-offs

- **Limited Flexibility**: Core structure is fixed
- **2-Qubit Only**: Specific to Deutsch's algorithm
- **Discrete Parameters**: Uses fixed rotation angles

## Usage in Grammatical Evolution

1. **Genome Decoding**: Integer codons map to grammar productions
2. **Oracle Injection**: Problem-specific oracle inserted at placeholder
3. **Fitness Evaluation**:
   - Correctness: Properly distinguishes constant/balanced
   - Efficiency: Minimal gate count
   - Robustness: Performance under noise


## Key Insights

### Algorithm Characteristics

- **Quantum Advantage**: Single oracle query vs classical requirement of 2
- **Deterministic**: Always gives correct answer (in ideal case)
- **Foundation**: Basis for more complex algorithms like Deutsch-Jozsa, Simon's, Shor's

### Evolution Benefits

- Can discover equivalent but more efficient implementations
- May find noise-resilient variations
- Explores gate cancellations and optimizations

## Notes

- Generates valid Qiskit Python code
- Compatible with all IBM Quantum backends
- Designed for GRAPE grammatical evolution framework
- Oracle injection enables testing all four possible functions
- Demonstrates quantum parallelism and interference principles
