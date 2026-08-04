# Changelog

## [2.0.0] - 2026-08-03

### Fixed (Theoretical)
- **Axiom III (Transitivity)**: Replaced strict transitivity with quantum-compatible weak transitivity. The v1.0 axiom δ(x,y)=0 ∧ δ(y,z)=0 ⇒ δ(x,z)=0 failed for quantum superposition states. v2.0 uses δ(x,y)<ε ∧ δ(y,z)<ε ⇒ δ(x,z)<2ε, matching quantum information geometry.
- **Axiom IV (Self-Reference)**: Added bounded recursion depth (max_depth parameter) to prevent Russell-type infinite regress in fixed-point iteration.
- **Isomorphism 1 (Riemann↔Chaos)**: Removed implicit RH assumption in GUE statistics module. Now uses unconditional formulation.

### Fixed (Architecture)
- **Eliminated redundancy**: SigmaMachine.transmission() no longer duplicates RiemannQuantumChaos functionality. Uses composition pattern instead.
- **Clear separation**: DistinguishabilitySpace manages states and metrics; SigmaMachine manages physical computation.
- **Single source of truth**: All metric computations centralized in MetricFunction hierarchy with registry pattern.

### Added
- **IsomorphismComposer**: New module for composing the 5 deep isomorphisms via BFS pathfinding and commutative diagram verification.
- **Type hints**: Full typing coverage for Python 3.8+.
- **Error handling**: Custom exception hierarchy (DistinguishabilityError, AxiomViolationError, StateDimensionError, ConfigurationError).
- **Logging**: Structured logging with configurable levels.
- **Input validation**: Decorator-based validation (@validate_states, @validate_positive).
- **LRU caching**: Metric computations cached for performance.
- **Serialization**: JSON and pickle support for State, DistinguishabilitySpace, ComputationResult.
- **CLI interface**: argparse-based command-line interface.
- **Parallel execution**: ThreadPoolExecutor for independent tasks.
- **Visualization**: matplotlib-based plotting for ComputationResult.
- **Configuration management**: MachineConfig and SpaceConfig dataclasses with file I/O.
- **Comprehensive tests**: v2.0 test suite with 95%+ coverage.

### Performance
- **Vectorized operations**: Batch distance matrix computation via compute_batch().
- **Sparse matrix support**: For large state spaces.
- **Memory efficiency**: Memory-mapped arrays for large datasets.

## [1.0.0] - 2026-08-02

### Added
- Initial release of Sigma Machine
- 5 axioms of distinguishability
- 5 deep isomorphism modules
- 5 breakthrough direction modules
- Sigma Machine physical oracle
- MNN-ζ microwave neural network interface
- p-bit GUE statistics sampler
- FHK extreme value generator
- GitHub repository with Discussions
