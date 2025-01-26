from qiskit import QuantumCircuit
from qiskit.circuit import Gate

# Simplified Oracle Gate
def create_oracle_gate():
    """
    Create an oracle gate as a composite QuantumCircuit.
    Marks the state |111> as an example.
    """
    qc = QuantumCircuit(3, name="oracle")
    # Example for |111>: Apply NOT gates to flip to |000>, then phase flip.
    qc.x(0)
    qc.x(1)
    qc.x(2)
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)
    qc.x(0)
    qc.x(1)
    qc.x(2)
    return qc.to_gate(label="Oracle Gate")

# Simplified Reflection (Diffusion Operator)
def create_reflection_gate():
    """
    Create a Grover reflection gate (diffusion operator) as a composite QuantumCircuit.
    """
    qc = QuantumCircuit(3, name="reflection")
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.x(0)
    qc.x(1)
    qc.x(2)
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)
    qc.x(0)
    qc.x(1)
    qc.x(2)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    return qc.to_gate(label="Reflection Gate")

# Define gates globally
oracle_gate = create_oracle_gate()
reflection_gate = create_reflection_gate()

# Parse Circuit
def parse_circuit(code: str) -> QuantumCircuit:
    """
    Parse a string containing Python code for constructing a QuantumCircuit.
    Ensures the string is executed in a controlled environment.
    Args:
        code (str): Python code representing a QuantumCircuit.
    Returns:
        QuantumCircuit: The constructed quantum circuit.
    """
    exec_globals = {
        "QuantumCircuit": QuantumCircuit,
        "oracle_gate": oracle_gate,
        "reflection_gate": reflection_gate,
    }

    try:
        print("[DEBUG] Executing Code:\n", code)
        exec(code, exec_globals)
        qc = exec_globals.get("qc")
        if not isinstance(qc, QuantumCircuit):
            raise ValueError("No valid QuantumCircuit found in the generated code.")
        return qc

    except Exception as e:
        print(f"[Parse Error] Circuit Code:\n{code}")
        raise ValueError(f"Error while parsing circuit: {e}")