# Architecture Overview

## Layer Structure

```
┌─────────────────────────────────────────┐
│  L5: CRITICALITY (Optimization)        │
│  Order parameter, susceptibility,       │
│  phase transition detection             │
├─────────────────────────────────────────┤
│  L4: PHYSICAL COMPUTATION               │
│  SigmaMachine, parallel execution,      │
│  hardware backends                      │
├─────────────────────────────────────────┤
│  L3: ISOMORPHISM COMPOSER               │
│  BFS pathfinding, commutative           │
│  diagram verification                   │
├─────────────────────────────────────────┤
│  L2: STRUCTURE PRESERVATION             │
│  Symmetry operations, unitary           │
│  transformations                        │
├─────────────────────────────────────────┤
│  L1: DISTINGUISHABILITY CORE            │
│  State, DistinguishabilitySpace,        │
│  MetricFunction                         │
└─────────────────────────────────────────┘
```

## Design Patterns

- **Registry Pattern**: MetricFunction registry for extensible metrics
- **Composer Pattern**: IsomorphismComposer for composing correspondences
- **Strategy Pattern**: Configurable backends (NMR, ion trap, superconducting, MNN)
- **Observer Pattern**: Logging and progress reporting
