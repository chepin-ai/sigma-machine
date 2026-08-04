"""
sigma_machine/tests/test_sigma_machine.py
==========================================
Test suite for the Sigma Machine.
"""

import numpy as np
import pytest
from sigma_machine.core import (
    State, DistinguishabilitySpace, Symmetry,
    Composition, SelfReference, Criticality,
    SigmaMachine
)
from sigma_machine.isomorphisms import RiemannQuantumChaos


class TestDistinguishabilitySpace:
    def test_axioms(self):
        space = DistinguishabilitySpace(3, "euclidean")
        for i in range(5):
            v = np.random.randn(3)
            space.add_state(State(v, f"s{i}"))

        results = space.verify_axioms()
        assert results['reflexive']
        assert results['symmetric']
        assert results['transitive']
        assert results['nondegenerate']

    def test_metric(self):
        space = DistinguishabilitySpace(2, "euclidean")
        s1 = space.add_state(State(np.array([1, 0]), "s1"))
        s2 = space.add_state(State(np.array([0, 1]), "s2"))

        d = space.metric(space.states[s1], space.states[s2])
        assert abs(d - np.sqrt(2)) < 1e-10


class TestSigmaMachine:
    def test_initialization(self):
        machine = SigmaMachine(n_modes=10)
        assert machine.n_modes == 10
        assert machine.space.dimension == 10

    def test_zero_detection(self):
        machine = SigmaMachine(n_modes=5)
        zeros = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351])
        machine.configure_for_riemann_zeros(zeros)

        detected = machine.detect_zeros((3.0, 7.0), n_points=500)
        assert len(detected) > 0

    def test_transmission(self):
        machine = SigmaMachine(n_modes=3)
        zeros = np.array([14.1347, 21.0220, 25.0109])
        machine.configure_for_riemann_zeros(zeros)

        T = machine.transmission(3.5, pump_power=1.0)
        assert 0 <= T <= 1


class TestRiemannQuantumChaos:
    def test_zeros(self):
        rqc = RiemannQuantumChaos(n_zeros=10)
        assert len(rqc.gamma_zeros) == 10
        assert abs(rqc.gamma_zeros[0] - 14.1347) < 1e-4

    def test_gue_statistics(self):
        rqc = RiemannQuantumChaos(n_zeros=50)
        spacings = np.diff(rqc.gamma_zeros)
        stats = rqc.compute_gue_statistics(spacings)

        assert 'variance' in stats
        assert stats['variance'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
