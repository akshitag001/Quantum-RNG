# generator.py

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

def generate_bits(n=1):
    """
    Generate n quantum random bits using a single qubit circuit.
    """
    simulator = AerSimulator()
    qc = QuantumCircuit(1, 1)
    bits = []
    for _ in range(n):
        qc.h(0)          # Hadamard gate creates superposition
        qc.measure(0, 0)
        simulator = AerSimulator()
        job = simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        bit = int(list(counts.keys())[0])
        bits.append(bit)
    return bits

def random_int(low=0, high=1):
    """
    Generate a random integer between low and high using quantum bits.
    """
    n_bits = (high - low).bit_length()
    while True:
        bits = generate_bits(n_bits)
        val = sum([b*(2**i) for i, b in enumerate(bits)])
        if low <= val <= high:
            return val

def random_array(size=10, low=0, high=1):
    """
    Generate an array of quantum random numbers.
    """
    return [random_int(low, high) for _ in range(size)]

