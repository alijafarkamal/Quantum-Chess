import numpy as np
from math import ceil, log2
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def amplitude_sample(scores, shots=512):
    arr = np.array(scores, dtype=float)
    arr = np.maximum(0, arr)
    if arr.sum() == 0:
        arr = np.ones_like(arr)
    amps = np.sqrt(arr)
    amps = amps / np.linalg.norm(amps)
    m = len(amps)
    n_qubits = int(ceil(log2(m)))
    dim = 2**n_qubits
    
    padded = np.zeros(dim, dtype=complex)
    padded[:m] = amps
    
    qc = QuantumCircuit(n_qubits)
    qc.initialize(padded, qc.qubits)
    qc.measure_all()
    
    backend = Aer.get_backend('aer_simulator')
    t = transpile(qc, backend)
    result = backend.run(t, shots=shots).result()
    counts = result.get_counts()
    
    hist = {}
    for bitstr, c in counts.items():
        idx = int(bitstr[::-1], 2)
        if idx < m:
            hist[idx] = hist.get(idx, 0) + c
    
    total = sum(hist.values())
    probs = {k: v/total for k,v in hist.items()}
    return probs, hist 