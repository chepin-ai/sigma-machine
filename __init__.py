"""
Sigma Machine v2.0: Universal Computational Architecture
=========================================================

A complete refactoring resolving all theoretical contradictions,
architecture redundancy, implementation defects, and performance
bottlenecks identified in v1.0.

Key Improvements in v2.0:
- Fixed Axiom III: Quantum weak transitivity (replaces strict transitivity)
- Fixed Axiom IV: Bounded recursion depth (prevents Russell paradox)
- Added IsomorphismComposer: Composes the 5 deep isomorphisms
- Added type hints, error handling, logging throughout
- Added CLI interface, parallel execution, visualization
- Added serialization, caching, configuration management
- Added comprehensive test suite

Version: 2.0.0
"""

__version__ = "2.0.0"

from .core import (
    State, DistinguishabilitySpace, SpaceConfig,
    Symmetry, Composition, SelfReference, Criticality,
    MetricFunction, EuclideanMetric, CosineMetric, QuantumMetric, InformationMetric,
    DistinguishabilityError, AxiomViolationError, StateDimensionError, ConfigurationError,
    SigmaMachine, MachineConfig, ComputationResult,
    IsomorphismComposer,
    main_cli
)

from .isomorphisms import (
    RiemannQuantumChaos,
    LanglandsQFT,
    NCGStandardModel,
    TwistorAmplitudes,
    InformationThermodynamics
)

from .breakthroughs import (
    DerivedIsomorphism,
    ExperimentalMetamathematics,
    InformationProofRH,
    CriticalityPrinciple,
    UnificationMathPhysics
)

__all__ = [
    # Version
    "__version__",
    # Core
    "State", "DistinguishabilitySpace", "SpaceConfig",
    "Symmetry", "Composition", "SelfReference", "Criticality",
    "MetricFunction", "EuclideanMetric", "CosineMetric", "QuantumMetric", "InformationMetric",
    "DistinguishabilityError", "AxiomViolationError", "StateDimensionError", "ConfigurationError",
    "SigmaMachine", "MachineConfig", "ComputationResult",
    "IsomorphismComposer",
    "main_cli",
    # Isomorphisms
    "RiemannQuantumChaos", "LanglandsQFT", "NCGStandardModel",
    "TwistorAmplitudes", "InformationThermodynamics",
    # Breakthroughs
    "DerivedIsomorphism", "ExperimentalMetamathematics",
    "InformationProofRH", "CriticalityPrinciple", "UnificationMathPhysics",
]
