"""
sigma_machine.core
==================
v2.0 Core modules for the Sigma Machine architecture.

Modules:
    distinguishability: Axioms I-V with quantum weak transitivity
    sigma_machine: Universal physical oracle with IsomorphismComposer
"""

from .distinguishability import (
    State, DistinguishabilitySpace, SpaceConfig,
    Symmetry, Composition, SelfReference, Criticality,
    MetricFunction, EuclideanMetric, CosineMetric, QuantumMetric, InformationMetric,
    DistinguishabilityError, AxiomViolationError, StateDimensionError, ConfigurationError,
    validate_states, validate_positive
)

from .sigma_machine import (
    SigmaMachine, MachineConfig, ComputationResult,
    IsomorphismComposer,
    main_cli
)

__all__ = [
    # Distinguishability
    "State", "DistinguishabilitySpace", "SpaceConfig",
    "Symmetry", "Composition", "SelfReference", "Criticality",
    "MetricFunction", "EuclideanMetric", "CosineMetric", "QuantumMetric", "InformationMetric",
    "DistinguishabilityError", "AxiomViolationError", "StateDimensionError", "ConfigurationError",
    "validate_states", "validate_positive",
    # Sigma Machine
    "SigmaMachine", "MachineConfig", "ComputationResult",
    "IsomorphismComposer",
    "main_cli"
]
