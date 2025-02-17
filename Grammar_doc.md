
# Documentation: DAG-Ready Grover Grammar

## 1. Overview

This grammar is designed to automatically generate valid quantum circuits that follow a Grover-style workflow:

1. Initialization (creating a quantum circuit, optionally applying initial gates).

2. HadamardAll (applying Hadamard gates to all qubits).

3. One or more Grover Iterations, each consisting of:

    • OracleBlock: A configurable “oracle” phase with user-defined gates or “mark” patterns.

    • DiffuserBlock: A diffuser phase that typically amplifies the marked states.

4. Measurement at the end.

Beyond the basic Grover steps, the grammar allows for single-qubit, multi-qubit, and parameterized gates. It enforces a directed, acyclic structure (DAG) by ensuring:
 • No backward references or cycles.
 • Distinct qubits for multi-qubit gates to avoid invalid calls like qc.cx(1,1).

## 2. Why “DAG-Ready”?

1. Qiskit’s Internal Representation
 • Qiskit constructs a Directed Acyclic Graph (DAG) internally when you build circuits gate-by-gate.
 • As long as you do not reference gates “out of order” or reuse qubits in a way that creates cycles, each circuit resolves to a valid DAG.
2. No Duplicate Qubits for Multi-Qubit Gates
 • The grammar enumerates <TwoDistinctQubits> and <ThreeDistinctQubits> explicitly, ensuring calls like qc.cx(1,1) (where the control and target are the same qubit) cannot occur.
3. Forward-Only Flow
 • The grammar organizes gates in a strict sequence: Initialize → HadamardAll → GroverIterations → Measure.
 • No production rule allows going back to earlier steps, preventing cycles or “rewinding time.”

## 3. Grammar Structure

```bnf
<Program> ::= <Initialize> <HadamardAll> <GroverIterations> <Measure>

<Initialize> ::= "qc = QuantumCircuit(3, 3)\n"

<HadamardAll> ::= "qc.h(0)\n"
                  "qc.h(1)\n"
                  "qc.h(2)\n"

<GroverIterations> ::= <GroverIteration>
                     | <GroverIteration> <GroverIterations>

<GroverIteration> ::= <OracleBlock> <DiffuserBlock>

<OracleBlock> ::= "## Begin Oracle\n"
                  <Oracle>
                  "## End Oracle\n"

<Oracle> ::= <OracleGateList>

<OracleGateList> ::= <OracleGate>
                   | <OracleGate> <OracleGateList>

<OracleGate> ::= <Mark111>
               | <Mark001>
               | <SingleQubitGate>
               | <TwoQubitGate>
               | <ThreeQubitGate>
               | <ParameterizedGate>

<Mark111> ::= "qc.ccx(0,1,2)\n"

<Mark001> ::= "qc.x(0)\n"
              "qc.x(1)\n"
              "qc.ccx(0,1,2)\n"
              "qc.x(0)\n"
              "qc.x(1)\n"

<DiffuserBlock> ::= "## Begin Diffuser\n"
                    <Diffuser>
                    "## End Diffuser\n"

<Diffuser> ::= <DiffuserGateList>

<DiffuserGateList> ::= <DiffuserGate>
                     | <DiffuserGate> <DiffuserGateList>

<DiffuserGate> ::= "qc.h(0)\n"
                 | "qc.h(1)\n"
                 | "qc.h(2)\n"
                 | "qc.x(0)\n"
                 | "qc.x(1)\n"
                 | "qc.x(2)\n"
                 | "qc.h(2)\n"
                 | "qc.cx(0,2)\n"
                 | "qc.cx(1,2)\n"
                 | "qc.h(2)\n"
                 | "qc.x(0)\n"
                 | "qc.x(1)\n"
                 | "qc.x(2)\n"
                 | "qc.h(0)\n"
                 | "qc.h(1)\n"
                 | "qc.h(2)\n"
                 | <SingleQubitGate>
                 | <TwoQubitGate>
                 | <ThreeQubitGate>
                 | <ParameterizedGate>

<Measure> ::= "qc.measure(0, 0)\n"
              "qc.measure(1, 1)\n"
              "qc.measure(2, 2)\n"

<SingleQubitGate> ::=
    "qc.x(" <QubitSingle> ")\n"
  | "qc.y(" <QubitSingle> ")\n"
  | "qc.z(" <QubitSingle> ")\n"
  | "qc.h(" <QubitSingle> ")\n"
  | "qc.s(" <QubitSingle> ")\n"
  | "qc.sdg(" <QubitSingle> ")\n"
  | "qc.t(" <QubitSingle> ")\n"
  | "qc.tdg(" <QubitSingle> ")\n"
  | "qc.id(" <QubitSingle> ")\n"

<TwoQubitGate> ::=
    "qc.cx(" <TwoDistinctQubits> ")\n"
  | "qc.cy(" <TwoDistinctQubits> ")\n"
  | "qc.cz(" <TwoDistinctQubits> ")\n"
  | "qc.swap(" <TwoDistinctQubits> ")\n"
  | "qc.iswap(" <TwoDistinctQubits> ")\n"

<ThreeQubitGate> ::=
    "qc.ccx(" <ThreeDistinctQubits> ")\n"
  | "qc.cswap(" <ThreeDistinctQubits> ")\n"

<ParameterizedGate> ::=
    "qc.rx(" <Angle> "," <QubitSingle> ")\n"
  | "qc.ry(" <Angle> "," <QubitSingle> ")\n"
  | "qc.rz(" <Angle> "," <QubitSingle> ")\n"
  | "qc.u(" <Angle> "," <Angle> "," <Angle> "," <QubitSingle> ")\n"
  | "qc.rxx(" <Angle> "," <TwoDistinctQubits> ")\n"
  | "qc.ryy(" <Angle> "," <TwoDistinctQubits> ")\n"
  | "qc.rzz(" <Angle> "," <TwoDistinctQubits> ")\n"
  | "qc.rzx(" <Angle> "," <TwoDistinctQubits> ")\n"

<QubitSingle> ::= "0" | "1" | "2"

<TwoDistinctQubits> ::=
    "0,1" | "1,0"
  | "0,2" | "2,0"
  | "1,2" | "2,1"

<ThreeDistinctQubits> ::=
    "0,1,2" | "0,2,1"
  | "1,0,2" | "1,2,0"
  | "2,0,1" | "2,1,0"

<Angle> ::=
    "0"
  | "np.pi/4"
  | "np.pi/2"
  | "np.pi"
  | "3*np.pi/2"
  | "2*np.pi"
  | "0.5"
  | "1.3"
  | "2.7"
  | "0.314"
  | "1.5708"
  | "3.1415"
```

Key Elements:

• Initialize
Creates a 3-qubit, 3-classical-bit circuit (qc = QuantumCircuit(3, 3)).

• HadamardAll
Applies qc.h(0), qc.h(1), and qc.h(2) to place all qubits in superposition.

• GroverIterations
Consists of one or more <GroverIteration> blocks, each containing:

    • OracleBlock – Typically an oracle identifying “marked” states.
    • DiffuserBlock – A sequence amplifying those marked states.
    • OracleGateList / DiffuserGateList
    Allows multiple gates, including single, two-qubit, three-qubit, or parameterized gates.

• Mark111 / Mark001
Pre-built oracles for common Grover demonstrations.

• Measure

Measures qubits into their respective classical bits.

• Distinct Qubits
Multi-qubit gates are chosen from <TwoDistinctQubits> and <ThreeDistinctQubits>, preventing invalid duplicates like (1,1).

 • Parameterized Gates
Includes gates like rx(θ), u(θ,ϕ,λ), rxx(θ), etc. The <Angle> nonterminal enumerates specific angles or constants.

## 4. How It Works in Practice

1. Grammar → Phenotype
An evolutionary algorithm or grammar-based generator produces a string (phenotype) that matches the rules.

2. Parsing to a QuantumCircuit
The code is executed in Python, building a Qiskit QuantumCircuit. Because each gate is listed in a valid single-line format (e.g., qc.cx(0,1)), Qiskit can parse it properly.

3. Execution / Simulation
Once constructed, you can run the circuit on a simulator or real quantum hardware. Qiskit sees it as a DAG, which can be transpiled and optimized.

## 5. Why This Matters

 • Automated Circuit Synthesis
By capturing both the structure (Grover’s iteration approach) and the variability (multiple gate types, parameterized angles, distinct qubits), the grammar enables large-scale exploration of quantum circuits—while maintaining correctness (valid Qiskit DAG).

• Ensuring Acyclic Graphs
The grammar never references future or backward time steps, guaranteeing a forward-only circuit that Qiskit interprets as a DAG with no cycles.

• Expandable
To scale up, you can:

    • Add more angles or gates.
    • Increase qubit count in <Initialize>.
    • Introduce more advanced structures (e.g., attribute grammars for floating angles).

## 6. Conclusion

This DAG-Ready Grover Grammar provides a template for generating valid quantum circuits that adhere to a Grover-like flow. By enforcing distinct qubit arguments and a strictly forward sequence of gates, it ensures each circuit can be represented as a directed acyclic graph in Qiskit, preventing runtime errors and invalid gate calls.

Use this grammar to explore quantum evolutionary algorithms, automated circuit discovery, and experiments in optimization or noise-resilience, all while retaining a core Grover logic that can be readily extended or specialized for new research directions.
