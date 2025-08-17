# BNF Grammar for Grover's Algorithm Circuit Evolution (Qiskit)

## Overview

This BNF (Backus-Naur Form) grammar defines the structure for evolving quantum circuits that implement Grover's search algorithm using IBM Qiskit. The grammar ensures syntactically valid quantum circuits while providing sufficient flexibility for the evolutionary algorithm to discover optimal implementations on IBM quantum hardware.

## Grammar Structure

### Core Components

The grammar follows the canonical structure of Grover's algorithm:

```
Program → Initialize → Hadamard Superposition → Grover Iterations → Measurement
```

### 1. **Program Structure** (`<Program>`)

The top-level rule that defines the complete quantum circuit:

- **Initialize**: Creates a 3-qubit quantum circuit with 3 classical bits
- **HadamardAll**: Applies Hadamard gates for uniform superposition
- **GroverIterations**: Executes one or more Grover iterations
- **Measure**: Maps quantum measurements to classical bits

### 2. **Initialization Phase** (`<Initialize>`, `<HadamardAll>`)

```python
qc = QuantumCircuit(3, 3)  # 3 qubits, 3 classical bits
qc.h(0)
qc.h(1)
qc.h(2)
```

Creates equal superposition state |+++⟩ across all 3 qubits.

### 3. **Grover Iterations** (`<GroverIterations>`, `<GroverIteration>`)

Recursive structure allowing 1 or more iterations, each containing:

- **Oracle Block**: Phase marking of target state
- **Diffuser Block**: Inversion about average operation

### 4. **Oracle Block** (`<OracleBlock>`)

```python
## Begin Oracle
[Evolvable gate sequences]
## End Oracle
```

- Placeholder region for problem-specific oracle
- Oracle implementation is **injected dynamically** based on target state
- Optional variations allow evolution to explore optimizations

### 5. **Diffuser Block** (`<DiffuserBlock>`)

Implements the amplitude amplification operator:

- Standard diffuser sequence (fixed structure)
- Optional additional gates for evolutionary optimization

## Gate Set

### Single-Qubit Gates

- **Pauli Gates**: `x`, `y`, `z`, `id` (identity)
- **Hadamard**: `h`
- **Phase Gates**: `s`, `sdg` (S†), `t`, `tdg` (T†)
- **Rotation Gates**: `rx(θ)`, `ry(θ)`, `rz(θ)`
- **Universal Gate**: `u(θ, φ, λ)` - general unitary

### Two-Qubit Gates

- **Controlled Pauli**: `cx` (CNOT), `cy`, `cz`
- **Swap Operations**: `swap`, `iswap`
- **Parameterized**: `rxx(θ)`, `ryy(θ)`, `rzz(θ)`, `rzx(θ)`

### Three-Qubit Gates

- **Toffoli**: `ccx` (controlled-controlled-X)
- **Fredkin**: `cswap` (controlled-swap)

## Parameterization

### Rotation Angles (`<Angle>`)

Predefined angle values optimized for quantum algorithms:

- **Rational multiples of π**: 0, π/4, π/2, π, 3π/2, 2π
- **Decimal approximations**: 0.5, 1.3, 2.7
- **Common constants**: 0.314 (≈π/10), 1.5708 (≈π/2), 3.1415 (≈π)

### Qubit Specifications

- **Single Qubit** (`<QubitSingle>`): 0, 1, or 2
- **Two Distinct Qubits** (`<TwoDistinctQubits>`): All permutations of 2 qubits
- **Three Distinct Qubits** (`<ThreeDistinctQubits>`): All permutations of 3 qubits

## Evolution Strategy

### What Evolves

- Number and composition of Grover iterations
- Gate sequences in oracle variations
- Additional optimization gates after diffuser
- Choice and ordering of parameterized gates

### What Remains Fixed

- Circuit initialization (3 qubits, 3 classical bits)
- Initial Hadamard superposition
- Core diffuser structure (inversion about average)
- Final measurement mapping

## Usage in Grammatical Evolution

1. **Genome Mapping**: Integer codons are decoded to Qiskit instructions via grammar rules
2. **Oracle Injection**: Problem-specific oracle replaces placeholder during evaluation
3. **Fitness Evaluation**: Circuits assessed for:
   - Accuracy (probability of finding marked state)
   - Efficiency (gate count, circuit depth)
   - IBM hardware compatibility (transpilation cost)

## Example Generated Circuit

```python
qc = QuantumCircuit(3, 3)

# Create superposition
qc.h(0)
qc.h(1)
qc.h(2)

# Grover iteration 1
## Begin Oracle
[Target-specific oracle gates injected here]
## End Oracle

## Begin Diffuser
qc.h(0)
qc.h(1)
qc.h(2)
qc.x(0)
qc.x(1)
qc.x(2)
qc.h(2)
qc.cx(0,2)
qc.cx(1,2)
qc.h(2)
qc.x(0)
qc.x(1)
qc.x(2)
qc.h(0)
qc.h(1)
qc.h(2)
# Optional evolved gates
qc.rz(np.pi/4, 1)
## End Diffuser

# Measurement
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)
```

## Design Rationale

### Why This Structure?

1. **IBM Compatibility**: Native Qiskit syntax for seamless execution
2. **Hardware Optimization**: Gate set matches IBM quantum processors
3. **Modular Design**: Clear separation of algorithm components
4. **Evolution-Friendly**: Balance between structure and flexibility

### Key Differences from Cirq Version

- **Syntax**: Qiskit's method-based API vs Cirq's object-based
- **Gate Names**: `sdg`/`tdg` instead of `S**-1`/`T**-1`
- **Universal Gate**: Includes `u(θ,φ,λ)` for general single-qubit operations
- **Measurement**: Direct qubit-to-bit mapping syntax

### Trade-offs

- **Fixed Architecture**: Preserves Grover's algorithm structure
- **3-Qubit Limitation**: Optimized for near-term quantum devices
- **Discrete Angles**: Predetermined values for faster convergence

## Extending the Grammar

To adapt for different scenarios:

1. **More Qubits**: Modify initialization and update qubit indices
2. **Different Algorithm**: Replace diffuser with algorithm-specific operations
3. **Custom Gates**: Add IBM-specific native gates (e.g., `ecr`, `sx`)
4. **Continuous Parameters**: Replace discrete angles with continuous optimization

## Hardware Considerations

### IBM Quantum Processors

- **Native Gate Set**: Optimized for IBM's basis gates (CX, ID, RZ, SX, X)
- **Transpilation**: Grammar output is transpiled to hardware-native gates
- **Connectivity**: Two-qubit gates respect device topology after transpilation

### Noise Adaptation

- Evolution can discover noise-resilient implementations
- Optional gates allow for error mitigation strategies
- Gate count optimization reduces decoherence effects

## Notes

- Generates valid Qiskit Python code
- Compatible with IBM Quantum simulators and hardware
- Designed for use with GRAPE grammatical evolution library
- Oracle injection enables problem-specific customization
- Supports both `ibmq_qasm_simulator` and real quantum backends
