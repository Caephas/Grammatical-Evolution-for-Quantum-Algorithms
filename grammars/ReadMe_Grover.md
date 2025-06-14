# Grover Circuit Grammar Specification

---

## 1. Top-level Skeleton

```bnf
<Program> ::= <Initialize> <HadamardAll> <GroverIterations> <Measure>
```

**Why this order?**

1. Allocate qubits & classical bits (cannot do anything before that).
2. Put the register in an equal superposition – Grover’s prerequisite.
3. Run an arbitrary number of oracle → diffuser pairs (left flexible).
4. Measure last so additional gates can be inserted anywhere above without touching read-out logic.

---

## 2. Initialization

```bnf
<Initialize> ::= "qc = QuantumCircuit(3, 3)\n"
```

- Hard-coding 3 qubits keeps the rest of the grammar readable (no variable-length qubit lists).
- Classical register mirrors the quantum size → one-line, noise-free mapping in Qiskit.

---

## 3. Superposition Block

```bnf
<HadamardAll> ::= "qc.h(0)\n" "qc.h(1)\n" "qc.h(2)\n" 
```

- Separate literals (three lines) let an optimiser or human comment out a single Hadamard if they want to break uniformity, instead of rewriting an entire gate list.

---

## 4. Iteration Engine

```bnf
<GroverIterations> ::= <GroverIteration> | <GroverIteration> <GroverIterations>
<GroverIteration>  ::= <OracleBlock> | <DiffuserBlock>

```

- Tail recursion keeps the grammar short.
- We deliberately don’t force the pattern oracle → diffuser because evolutionary search occasionally finds useful “mutations” (e.g., two diffusers in a row can act as a global phase). If strict pairing is needed then wrap both blocks in a single non-terminal `<GroverPair>`.

---

## 5. Oracle Block

```bnf
<OracleBlock> ::= "## Begin Oracle\n" <OptionalOracleVariations> "## End Oracle\n"
```

- Sentinel comments give humans and parsers an unambiguous anchor.
- `<OptionalOracleVariations>` can be empty – so the grammar still produces valid circuits when you only want to test the diffuser.
- The gate vocabulary is a small subset (same list used in the diffuser) to keep search space realistic – real oracles rarely need exotic multi-qubit blocks beyond `CCX` and parameterised rotations.

---

## 6. Diffuser Block

### 6.1 Wrapper

```bnf
<DiffuserBlock> ::= "## Begin Diffuser\n" <StandardDiffuser> <OptionalGates> "## End Diffuser\n"
```

- Fixed header/footer mirrors the oracle for symmetry and easy regex parsing.
- `<OptionalGates>` lets you tack on error-mitigation pulses or benchmarking gates after the canonical diffuser.

### 6.2 Canonical Diffuser

```bnf
<StandardDiffuser> ::= H-X sandwich → H(2) CX CX H(2) → uncompute X → final H

```

```bnf
<StandardDiffuser> ::=
    h(0) h(1) h(2)      ; prepare Hadamard basis
    x(0) x(1) x(2)      ; translate mean to |111⟩
    h(2)                ; turn upcoming CXs into CZs
    cx(0,2) cx(1,2)     ; phase-flip |111⟩ (CCZ)
    h(2)                ; undo the pre-rotation
    x(0) x(1) x(2)      ; uncompute the translation
    h(0) h(1) h(2)      ; return to computational basis
```

- This 17-gate sequence is the text-book inversion-about-mean for 3 qubits.
- Hard-coding it guarantees algorithmic correctness while still letting you extend it via `<OptionalGates>`.

 • Why the apparent repetition?

- The first H–X pair sets up the reflection plane.
- The middle h(2) → cx cx → h(2) implements a controlled-Z that flips only |111⟩.
- The second X–H pair uncomputes the setup, leaving qubits back in the computational basis so the next Grover iteration and the final measurement behave correctly.
- Any missing mirror would either flip the wrong axis or leave the register in a rotated basis, breaking algorithmic correctness.
- Hard-coding the diffuser guarantees the algorithm works, while ```<OptionalGates> ```still lets you extend or tweak the block when experimenting.

---

## 7. Gate Vocabularies

| Non-terminal         | Typical use           | Design guard-rail                                |
|----------------------|------------------------|---------------------------------------------------|
| `<SingleQubitGate>`  | Clifford & T gates     | Operates on one of the enumerated qubits         |
| `<TwoQubitGate>`     | CX, CZ, SWAP, iSWAP    | Only distinct qubit pairs; no `cx(0,0)`          |
| `<ThreeQubitGate>`   | CCX, CSWAP             | Same distinct-ness protection                    |
| `<ParameterizedGate>`| Axis rotations & `u`   | Angles from finite set (see §8) for hashability  |

---

## 8. Angles

```bnf
<Angle> ::= "0" | "np.pi/4" | "np.pi/2" | … | "3.1415"
```

- Finite catalogue makes circuits hashable and speeds up genetic-algorithm duplicate detection.
- Includes the usual Clifford multiples of π plus a few arbitrary reals so search can break Clifford symmetry when needed.

---

## 9. Distinct-Qubit Enumerations

```bnf
<TwoDistinctQubits>  ::= "0,1" | "1,0" | …  
<ThreeDistinctQubits> ::= "0,1,2" | "0,2,1" | …
```

- Enumeration is verbose but bullet-proof – parsers don’t have to evaluate “are all indices different?”
- It also pre-computes every legal permutation so the grammar itself encodes the no-duplicate-target constraint.

---

## 10. Measurement Block

```bnf
<Measure> ::= qc.measure(i, i) for i = 0..2
```

- One-to-one qubit-to-bit mapping keeps the downstream classical post-processing trivial (`counts.most_common()` on shot data).
- Locked to the very end: ensures any added gates appear before measurement, never after.

---

## 11. Why Comments Around Blocks?

1. Tooling friendly – IDE plugins or scripts can do `split('## Begin Oracle')`.
2. Human orientation – anyone scanning a generated circuit immediately spots algorithmic sections.
3. Round-trip safety – you can regenerate an oracle only, splice it back in, and keep the rest of the file untouched.

---

## 12. Known Trade-Offs

| Trade-off                    | Reason it’s Acceptable                                                  |
|------------------------------|--------------------------------------------------------------------------|
| Hard-coded to 3 qubits       | Keeps grammar short for tutorial & proof-of-concept; can be templated   |
| Oracle/diffuser order flexible | Fosters search creativity; easy to tighten if strictness is needed     |
| Finite angle list            | Greatly reduces search space; expandable or swappable with `<Float>`    |
