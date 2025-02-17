from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate, RGate
import numpy as np

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
        'UGate': UGate,
        'RGate': RGate,
        'np':np
    }

    try:
        # print("[DEBUG] Executing Code:\n", code)
        exec(code, exec_globals)
        qc = exec_globals.get("qc")
        if not isinstance(qc, QuantumCircuit):
            raise ValueError("No valid QuantumCircuit found in the generated code.")
        return qc

    except Exception as e:
        print(f"[Parse Error] Circuit Code:\n{code}")
        raise ValueError(f"Error while parsing circuit: {e}")