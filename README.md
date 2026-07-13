# Quantum Chess

A Streamlit chess demo that scores legal moves with classical heuristics and optionally samples among them using **Qiskit Aer–simulated** circuits. Built for CQHack25 as an educational quantum + games prototype—not a competitive engine or hardware quantum solver.

## Problem

Move selection in chess is a combinatorial decision problem. This project explores how small quantum circuits (run on a local simulator) can sit on top of classical evaluation to produce a sampled move and a probability distribution—useful for teaching Qiskit and quantum-inspired sampling, not for Elo-competitive play.

## Architecture / approach

```
Streamlit UI (Play | Move Analysis)
  → classical move / board scoring (python-chess + heuristics)
  → method-specific path:
       QAOA-like | True Quantum Walk (Aer) | classical graph “walk” | amplitude sample
  → often amplitude_sample(top_k scores) → move + probability map
```

| UI label | What the code actually does |
|----------|-----------------------------|
| **QAOA** | Aer circuit: H → RZ(γ·score) → RX(β) → measure; γ,β grid `{0.5,1.0,1.5}`; one qubit per legal move. Classical scores first. Not full variational QAOA / combinatorial encoding. |
| **True Quantum Walk** | Aer circuit with coin/position qubits; graph built classically. Shift operator is effectively a stub—demo H/CX, not a full graph-conditioned coined walk. |
| **Quantum Walk (Intelligent)** | Classical NetworkX move tree; score ≈ mean(heuristic × √degree). May try true walk then fall back. |
| **Quantum Grover** | **Not Grover.** Classical quality scores → `amplitude_sample` (prepare √scores, measure). No oracle, no diffusion. |

All quantum execution uses **local Aer** (`qasm_simulator`). Every path has a **classical fallback** on exception. Play mode uses `"true_quantum_walk"`.

## Key engineering decisions

| Decision | Why (as implemented) |
|----------|----------------------|
| Classical eval → quantum sampling | Chess evaluation stays classical; circuits mainly sample among pre-scored moves |
| Aggressive try/except → classical | Demo stays usable if circuits fail or blow up |
| Shallow depth (~2) + top_k ≈ 8 | Keeps Aer circuit size and move graphs tractable |
| Streamlit + SVG boards | Fast dual UI (vs AI / FEN analysis) for a hackathon |

## Tech stack

From `requirements.txt` (lower bounds):

| Package | Spec |
|---------|------|
| streamlit | ≥1.28.0 |
| python-chess | ≥1.9.0 |
| qiskit | ≥0.44.0 |
| qiskit-aer | ≥0.12.0 |
| networkx | ≥3.0 |
| numpy / pandas / matplotlib | as listed |

No IBM Quantum Runtime / hardware backend.

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations / what I'd improve

- Aer simulation only—no hardware, no measured quantum advantage, no Elo evaluation.
- “Grover” naming is misleading; implement real amplitude amplification or rename the UI.
- True walk’s graph-conditioned shift is incomplete; finish or document as a toy circuit.
- Filename `grover_move_selector.py` is a multi-method router—clarify package layout.
- Formal pytest suite / pinned Qiskit versions would improve reproducibility.
