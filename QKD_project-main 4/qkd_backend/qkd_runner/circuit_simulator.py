# qkd_backend/qkd_runner/circuit_simulator.py
import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def text_to_bits(text):
    return [int(b) for c in text for b in bin(ord(c))[2:].zfill(8)]

def random_bases(n):
    return [random.choice(['+', 'x']) for _ in range(n)]

def run_circuit_simulator(message, shots=1024):
    bits = text_to_bits(message)
    n = len(bits)
    alice_bases = random_bases(n)
    bob_bases = random_bases(n)

    qc = QuantumCircuit(n, n)
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 'x':
            qc.h(i)
    for i in range(n):
        if bob_bases[i] == 'x':
            qc.h(i)
        qc.measure(i, i)

    try:
        qasm_str = qc.qasm()
    except Exception:
        qasm_str = ""

    sim = AerSimulator()
    job = sim.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    counts_int = {str(k): int(v) for k, v in counts.items()}

    matched_positions = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    total = 0
    errors = 0
    step_details = []
    for bitstring, freq in counts_int.items():
        bob_bits = [int(b) for b in bitstring[::-1]]
        for i in matched_positions:
            alice_bit = bits[i]
            bob_bit = bob_bits[i] if i < len(bob_bits) else None
            mismatch = (bob_bit is None) or (bob_bit != alice_bit)
            total += freq
            if mismatch:
                errors += freq
            step_details.append({
                "bitstring": bitstring,
                "freq": int(freq),
                "qubit": i,
                "alice_bit": int(alice_bit),
                "bob_bit": (int(bob_bit) if bob_bit is not None else None),
                "basis": alice_bases[i],
                "mismatch": bool(mismatch)
            })
    qber = (errors / total * 100) if total > 0 else 0.0

    return {
        "qasm": qasm_str,
        "counts": counts_int,
        "qber": round(qber, 2),
        "steps": step_details
    }
