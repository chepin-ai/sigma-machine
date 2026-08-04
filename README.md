# Sigma Machine v2.0

## Universal Computational Architecture for the Isomorphism Principle

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/chepin-ai/sigma-machine)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **v2.0 Release**: Complete refactoring resolving all theoretical contradictions, architecture redundancy, implementation defects, and performance bottlenecks identified in v1.0.

## What's New in v2.0

### Theoretical Fixes
- **Axiom III (Quantum Weak Transitivity)**: Replaced strict transitivity with quantum-compatible weak transitivity: δ(x,y)<ε ∧ δ(y,z)<ε ⇒ δ(x,z)<2ε
- **Axiom IV (Bounded Recursion)**: Added max_depth parameter to prevent Russell-type infinite regress in self-reference
- **IsomorphismComposer**: New module composing the 5 deep isomorphisms into a unified framework

### Architecture Improvements
- **Eliminated Redundancy**: SigmaMachine no longer duplicates RiemannQuantumChaos functionality
- **Clear Separation**: DistinguishabilitySpace manages states; SigmaMachine manages physical computation
- **Single Source of Truth**: All metric computations centralized in MetricFunction hierarchy

### Implementation Quality
- **Type Hints**: Full typing coverage (Python 3.8+)
- **Error Handling**: Custom exception hierarchy with meaningful messages
- **Logging**: Structured logging throughout
- **Input Validation**: Decorator-based validation
- **Serialization**: JSON and pickle support for all data classes

### Performance
- **LRU Caching**: Metric computations cached
- **Vectorized Operations**: Batch distance matrix computation
- **Parallel Execution**: ThreadPoolExecutor for independent tasks
- **Memory Efficiency**: Sparse matrix support

### New Features
- **CLI Interface**: `python -m sigma_machine --task zero_detection`
- **Configuration Files**: JSON-based configuration management
- **Visualization**: Built-in plotting for results
- **Progress Reporting**: tqdm integration for long computations

## Installation

```bash
git clone https://github.com/chepin-ai/sigma-machine.git
cd sigma-machine
pip install -e .
```

## Quick Start

```python
from sigma_machine import SigmaMachine, MachineConfig
import numpy as np

# Initialize with configuration
config = MachineConfig(n_modes=20, parallel=True, cache_results=True)
machine = SigmaMachine(config)

# Configure for Riemann zeros
zeros = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351])
machine.configure_for_riemann_zeros(zeros)

# Detect transmission nulls (physical analog of zeta zeros)
detected = machine.detect_zeros((3.0, 7.0))
print(f"Detected {len(detected)} nulls")

# Run universal task interface
result = machine.run("criticality", {})
print(result.summary())

# Compose isomorphisms
result = machine.run("compose_isomorphisms", {
    "start_iso": "riemann_chaos",
    "end_iso": "info_thermo",
    "data": np.array([1.0])
})
print(f"Path taken: {result.metadata['path']}")
```

## CLI Usage

```bash
# Detect zeros
python -m sigma_machine --task zero_detection --n-modes 20 --verbose

# Use configuration file
python -m sigma_machine --task criticality --config my_config.json

# Generate visualization
python -m sigma_machine --task gue_sampling --visualize --output result.json
```

## Architecture

```
Sigma Machine v2.0
├── L1: Distinguishability Core (axioms I-V)
│   ├── State (vector + metadata)
│   ├── DistinguishabilitySpace (metric space)
│   └── MetricFunction (euclidean, cosine, quantum, information)
├── L2-L3: Isomorphism Composer
│   ├── Registers 5 deep isomorphisms
│   ├── Finds composition paths (BFS)
│   └── Verifies commutative diagrams
├── L4: Physical Computation
│   ├── SigmaMachine (universal oracle)
│   ├── Parallel execution
│   └── Hardware backends (Qiskit, Cirq, MNN)
└── L5: Criticality Optimization
    ├── Order parameter computation
    ├── Susceptibility analysis
    └── Phase transition detection
```

## The 5 Deep Isomorphisms

1. **Riemann Zeros ↔ Quantum Chaos**: Berry-Keating, Montgomery-Odlyzko, Yakaboylu, Wei
2. **Langlands Program ↔ QFT**: Kapustin-Witten, Geometric Langlands, S-duality
3. **NCG ↔ Standard Model**: Connes spectral triple, gauge group unification
4. **Twistor Theory ↔ Scattering Amplitudes**: BCFW, Amplituhedron, Grassmannian
5. **Information Theory ↔ Thermodynamics**: Landauer, Jarzynski, Bekenstein-Hawking

## The 5 Breakthrough Directions

1. **Derived Isomorphisms**: (∞,1)-category theory unification
2. **Experimental Metamathematics**: Physical experiments testing math
3. **Information Proof of RH**: Formalizing information physics argument
4. **Criticality Principle**: Fundamental law of nature
5. **Unification of Math and Physics**: UNI category as initial object

## Testing

```bash
pytest tests/test_sigma_machine_v2.py -v
```

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

## License

MIT License

## Changelog

### v2.0.0 (2026-08-03)
- Fixed Axiom III: Quantum weak transitivity
- Fixed Axiom IV: Bounded recursion depth
- Added IsomorphismComposer
- Added CLI interface
- Added parallel execution
- Added visualization utilities
- Added comprehensive test suite
- Resolved all v1.0 architecture redundancy

### v1.0.0 (2026-08-02)
- Initial release
- 5 axioms, 5 isomorphisms, 5 breakthrough directions
- Sigma Machine physical oracle
- MNN-ζ interface
