# BNF Grammar for Grover's Algorithm Circuit Evolution (Cirq)

## Overview

This BNF (Backus-Naur Form) grammar defines the structure for evolving quantum circuits that implement Grover's search algorithm using Google Cirq. The grammar ensures syntactically valid quantum circuits while providing enough flexibility for the evolutionary algorithm to discover optimal implementations.

## Grammar Structure

### Core Components

The grammar is organized into a hierarchical structure that mirrors Grover's algorithm:

```
Program → Initialize → Hadamard Superposition → Grover Iterations → Measurement
```

### 1. **Program Structure** (`<Program>`)

The top-level rule that defines the complete quantum circuit:

- **Initialize**: Creates the circuit object
- **HadamardAll**: Applies Hadamard gates to create superposition
- **GroverIterations**: Executes one or more Grover iterations
- **Measure**: Measures all qubits

### 2. **Initialization Phase** (`<Initialize>`, `<HadamardAll>`)

```python
circuit = cirq.Circuit()
circuit.append(cirq.H(qubits[0]))
circuit.append(cirq.H(qubits[1]))
circuit.append(cirq.H(qubits[2]))
```

Creates equal superposition across all 3 qubits.

### 3. **Grover Iterations** (`<GroverIterations>`, `<GroverIteration>`)

Can generate 1 or more iterations, each containing:

- **Oracle Block**: Marks the target state
- **Diffuser Block**: Amplifies marked state amplitude

### 4. **Oracle Block** (`<OracleBlock>`)

```
## Begin Oracle
[Evolvable gate sequences]
## End Oracle
```

- Placeholder for problem-specific oracle
- The actual oracle is **injected dynamically** during evolution
- Contains optional variations for exploration

### 5. **Diffuser Block** (`<DiffuserBlock>`)

Implements the inversion-about-average operation:

- Standard diffuser implementation (fixed)
- Optional additional gates for optimization

## Gate Set

### Single-Qubit Gates

- **Pauli Gates**: X, Y, Z, I
- **Hadamard**: H
- **Phase Gates**: S, S†, T, T†
- **Rotation Gates**: Rx(θ), Ry(θ), Rz(θ)

### Two-Qubit Gates

- **Controlled Gates**: CNOT, CZ
- **Swap Gates**: SWAP, ISWAP
- **Parameterized**: XX, YY, ZZ

### Three-Qubit Gates

- **Toffoli**: CCX
- **Controlled Swap**: CSWAP
- **Controlled-Controlled-Z**: CCZ

## Parameterization

### Rotation Angles (`<Angle>`)

Predefined angles for rotation gates:

- Common fractions of π: 0, π/4, π/2, π, 3π/2, 2π
- Decimal values: 0.5, 1.3, 2.7, 0.314, 1.5708, 3.1415

### Exponent Fractions (`<AngleFraction>`)

For parameterized two-qubit gates:

- Values: 0.25, 0.5, 1, 1.5, 2, 0.1, 0.4, 0.85

## Evolution Strategy

### What Evolves

- Number of Grover iterations
- Additional gates in oracle variations
- Optional gates after the diffuser
- Gate parameters and combinations

### What Remains Fixed

- Initial superposition (Hadamard on all qubits)
- Core diffuser structure
- Measurement on all qubits
- Oracle markers for injection

## Usage in Grammatical Evolution

1. **Genome → Phenotype**: The grammar maps integer codons to circuit instructions
2. **Oracle Injection**: The placeholder oracle is replaced with problem-specific implementation
3. **Fitness Evaluation**: Generated circuits are tested for:
   - Correctness (finding marked state)
   - Efficiency (gate count, depth)
   - Hardware compatibility

## Example Generated Circuit

```python
circuit = cirq.Circuit()
# Initial superposition
circuit.append(cirq.H(qubits[0]))
circuit.append(cirq.H(qubits[1]))
circuit.append(cirq.H(qubits[2]))

# Grover iteration 1
## Begin Oracle
[Oracle gates injected here]
## End Oracle

## Begin Diffuser
circuit.append(cirq.H(qubits[0]))
circuit.append(cirq.H(qubits[1]))
circuit.append(cirq.H(qubits[2]))
circuit.append(cirq.X(qubits[0]))
# ... (standard diffuser)
circuit.append(cirq.H(qubits[2]))
# Optional: evolved gates
circuit.append(cirq.T(qubits[1]))
## End Diffuser

# Measurement
circuit.append(cirq.measure(qubits[0], key='q0'))
circuit.append(cirq.measure(qubits[1], key='q1'))
circuit.append(cirq.measure(qubits[2], key='q2'))
```

## Design Rationale

### Why This Structure?

1. **Modularity**: Clear separation between oracle and diffuser
2. **Flexibility**: Optional gates allow evolution to discover optimizations
3. **Validity**: Grammar ensures all generated circuits are syntactically correct
4. **Hardware-Ready**: Gate set compatible with Google quantum processors

### Trade-offs

- **Fixed Structure**: Maintains Grover's algorithm skeleton
- **Limited Qubits**: Currently supports 3-qubit circuits
- **Predetermined Angles**: Uses common angle values rather than continuous optimization

## Extending the Grammar

To adapt for different algorithms or qubit counts:

1. Modify `<QubitIndex>` range for different qubit numbers
2. Adjust `<HadamardAll>` and `<Measure>` sections
3. Replace `<StandardDiffuser>` with algorithm-specific operations
4. Add new gate types as needed

## Notes

- The grammar generates Cirq-specific Python code
- Compatible with Google's Sycamore gateset after transpilation
- Designed for grammatical evolution with GRAPE library
- Oracle injection happens post-generation for problem-specific marking
