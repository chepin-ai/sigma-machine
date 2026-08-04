# Sigma Machine

## Universal Computational Architecture for the Isomorphism Principle

[![CI](https://github.com/chepin-ai/sigma-machine/actions/workflows/ci.yml/badge.svg)](https://github.com/chepin-ai/sigma-machine/actions)
[![Docs](https://github.com/chepin-ai/sigma-machine/actions/workflows/docs.yml/badge.svg)](https://chepin-ai.github.io/sigma-machine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is Sigma Machine?

The **Sigma Machine** is a universal computational architecture implementing the **Isomorphism Principle** — the meta-theory that **mathematics, physics, and computation are three representations of the same underlying structure: distinguishability**.

$$\text{Math}(\Sigma) \cong \text{Phys}(\Sigma) \cong \text{Comp}(\Sigma)$$

---

## The Five Axioms

| Axiom | Name | Mathematical | Physical | Computational |
|-------|------|-------------|----------|---------------|
| I | Primal Distinguishability | Metric space | Measurement | Bit comparison |
| II | Structure Preservation | Isometry | Symmetry | Reversible gate |
| III | Compositionality | Tensor product | Entanglement | Parallel execution |
| IV | Self-Reference | Gödel fixed point | Observer | Self-reproducing code |
| V | Criticality | RH / NP-complete | Phase transition | Edge of chaos |

---

## The Five Deep Isomorphisms

1. **[Riemann Zeros ↔ Quantum Chaos](theory/isomorphisms.md#riemann-quantum-chaos)** — Berry-Keating, Montgomery-Odlyzko, Yakaboylu, Wei
2. **[Langlands Program ↔ QFT](theory/isomorphisms.md#langlands-qft)** — Kapustin-Witten, Geometric Langlands, S-duality
3. **[NCG ↔ Standard Model](theory/isomorphisms.md#ncg-sm)** — Connes spectral triple, gauge group unification
4. **[Twistor Theory ↔ Scattering Amplitudes](theory/isomorphisms.md#twistor-amplitudes)** — BCFW, Amplituhedron, Grassmannian
5. **[Information Theory ↔ Thermodynamics](theory/isomorphisms.md#info-thermo)** — Landauer, Jarzynski, Bekenstein-Hawking

---

## Quick Start

```python
from sigma_machine import SigmaMachine, MachineConfig
import numpy as np

# Initialize
config = MachineConfig(n_modes=20, parallel=True, cache_results=True)
machine = SigmaMachine(config)

# Configure for Riemann zeros
zeros = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351])
machine.configure_for_riemann_zeros(zeros)

# Detect transmission nulls
detected = machine.detect_zeros((3.0, 7.0))
print(f"Detected {len(detected)} nulls")

# Run universal task
result = machine.run("criticality", {})
print(result.summary())
```

---

## Installation

```bash
git clone https://github.com/chepin-ai/sigma-machine.git
cd sigma-machine
pip install -e .
```

---

## Architecture

```
Sigma Machine v2.0
├── L1: Distinguishability Core
│   ├── State (vector + metadata)
│   ├── DistinguishabilitySpace (metric space with weak transitivity)
│   └── MetricFunction (euclidean, cosine, quantum, information)
├── L2-L3: Isomorphism Composer
│   ├── Registers 5 deep isomorphisms
│   ├── Finds composition paths (BFS)
│   └── Verifies commutative diagrams
├── L4: Physical Computation
│   ├── SigmaMachine (universal oracle)
│   ├── Parallel execution (ThreadPoolExecutor)
│   └── Hardware backends (Qiskit, Cirq, MNN)
└── L5: Criticality Optimization
    ├── Order parameter computation
    ├── Susceptibility analysis
    └── Phase transition detection
```

---

## Research Roadmap

| Phase | Timeline | Goals |
|-------|----------|-------|
| **Foundation** | 2026-2028 | Reproduce Wei DQPT, build MNN-ζ prototype |
| **Scaling** | 2028-2032 | 1000 zeros, Yakaboylu in circuit QED |
| **Integration** | 2032-2040 | Hybrid systems, Lean 4 verification |
| **Revolution** | 2040+ | Physical demonstration of RH |

---

## Citation

```bibtex
@software{sigma_machine_2026,
  title = {Sigma Machine v2.0: Universal Computational Architecture},
  author = {Sigma Machine Research Group},
  year = {2026},
  version = {2.0.0},
  url = {https://github.com/chepin-ai/sigma-machine}
}
```

---

## License

[MIT License](https://github.com/chepin-ai/sigma-machine/blob/main/LICENSE)
