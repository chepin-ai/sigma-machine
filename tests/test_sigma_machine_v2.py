"""
sigma_machine/tests/test_sigma_machine_v2.py
=============================================
v2.0 Test suite with comprehensive coverage.
"""

import json
import numpy as np
import pytest
from sigma_machine.core import (
    State, DistinguishabilitySpace, SpaceConfig,
    Symmetry, Composition, SelfReference, Criticality,
    EuclideanMetric, QuantumMetric,
    DistinguishabilityError, StateDimensionError, ConfigurationError,
    SigmaMachine, MachineConfig, ComputationResult,
    IsomorphismComposer
)


class TestSpaceConfig:
    def test_valid_config(self):
        config = SpaceConfig(dimension=10, metric_type="quantum")
        assert config.dimension == 10
        assert config.metric_type == "quantum"

    def test_invalid_dimension(self):
        with pytest.raises(ConfigurationError):
            SpaceConfig(dimension=0)

    def test_invalid_metric(self):
        with pytest.raises(ConfigurationError):
            SpaceConfig(metric_type="invalid")


class TestState:
    def test_creation(self):
        s = State(np.array([1.0, 0.0]), "test")
        assert s.dimension == 2
        assert s.label == "test"

    def test_normalize(self):
        s = State(np.array([3.0, 4.0]))
        n = s.normalize()
        assert pytest.approx(n.norm(), 1.0)

    def test_serialization(self):
        s = State(np.array([1.0, 2.0]), "orig", {"key": "val"})
        d = s.to_dict()
        s2 = State.from_dict(d)
        assert np.allclose(s.vector, s2.vector)
        assert s.label == s2.label


class TestDistinguishabilitySpace:
    def test_axiom_verification(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=3))
        for i in range(5):
            space.add_state(State(np.random.randn(3), f"s{i}"))

        results = space.verify_axioms()
        assert results["reflexive"] is True
        assert results["symmetric"] is True
        assert results["weak_transitive"] is True
        assert results["nondegenerate"] is True
        assert results["all_passed"] is True

    def test_quantum_metric(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2, metric_type="quantum"))
        s1 = space.add_state(State(np.array([1.0, 0.0]), "|0>"))
        s2 = space.add_state(State(np.array([0.0, 1.0]), "|1>"))

        d = space.metric(space.get_state(s1), space.get_state(s2))
        assert d > 0  # Orthogonal states are distinguishable

    def test_dimension_mismatch(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        with pytest.raises(StateDimensionError):
            space.add_state(State(np.array([1.0, 2.0, 3.0])))

    def test_distance_matrix(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        for i in range(4):
            space.add_state(State(np.random.randn(2)))

        D = space.compute_distance_matrix()
        assert D.shape == (4, 4)
        assert np.allclose(np.diag(D), 0, atol=1e-10)

    def test_json_serialization(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        space.add_state(State(np.array([1.0, 0.0]), "s1"))

        json_str = space.to_json()
        space2 = DistinguishabilitySpace.from_json(json_str)
        assert len(space2) == len(space)


class TestSymmetry:
    def test_preservation(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        for i in range(5):
            space.add_state(State(np.random.randn(2)))

        # Rotation by 90 degrees
        theta = np.pi / 2
        R = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        sym = Symmetry(lambda x: R @ x, "rotation")

        assert sym.verify_preservation(space, n_tests=20)

    def test_composition(self):
        s1 = Symmetry(lambda x: x * 2, "scale2")
        s2 = Symmetry(lambda x: x + 1, "add1")
        s3 = s1.compose(s2)

        result = s3.apply(State(np.array([1.0])))
        assert np.allclose(result.vector, np.array([4.0]))  # (1+1)*2 = 4


class TestSelfReference:
    def test_fixed_point(self):
        # Simple contraction: f(x) = 0.5 * x
        def f(x):
            return 0.5 * x

        x0 = np.array([1.0, 2.0])
        x_fp, iters, conv = SelfReference.fixed_point_iteration(f, x0)

        assert conv is True
        assert np.allclose(x_fp, np.array([0.0, 0.0]), atol=1e-6)

    def test_bounded_depth(self):
        # Function that doesn't converge
        def f(x):
            return x + 0.1

        x0 = np.array([0.0])
        x_fp, iters, conv = SelfReference.fixed_point_iteration(f, x0, max_depth=3)

        assert conv is False  # Should not converge


class TestCriticality:
    def test_order_parameter(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        for i in range(10):
            space.add_state(State(np.random.randn(2)))

        op = Criticality.order_parameter(space, beta=1.0)
        assert op >= 0

    def test_find_critical_beta(self):
        space = DistinguishabilitySpace(SpaceConfig(dimension=2))
        for i in range(10):
            space.add_state(State(np.random.randn(2)))

        beta_c = Criticality.find_critical_beta(space)
        assert 0.1 <= beta_c <= 2.0


class TestIsomorphismComposer:
    def test_registration(self):
        comp = IsomorphismComposer()
        comp.register("test1", lambda x: x * 2, ["test2"])
        assert "test1" in comp._isomorphisms

    def test_compose(self):
        comp = IsomorphismComposer()
        comp.register("a", lambda x: x + 1, ["b"])
        comp.register("b", lambda x: x * 2, ["c"])
        comp.register("c", lambda x: x - 3, ["a"])

        result, path = comp.compose("a", "c", 5)
        assert path == ["a", "b", "c"]
        assert result == 9  # (5+1)*2-3 = 9


class TestSigmaMachine:
    def test_initialization(self):
        machine = SigmaMachine(MachineConfig(n_modes=10))
        assert machine.config.n_modes == 10
        assert len(machine.space) == 0

    def test_zero_detection(self):
        machine = SigmaMachine(MachineConfig(n_modes=5))
        zeros = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351])
        machine.configure_for_riemann_zeros(zeros)

        detected = machine.detect_zeros((3.0, 7.0), n_points=500)
        assert len(detected) > 0

    def test_transmission_bounds(self):
        machine = SigmaMachine(MachineConfig(n_modes=3))
        zeros = np.array([14.1347, 21.0220, 25.0109])
        machine.configure_for_riemann_zeros(zeros)

        T = machine.transmission(3.5, pump_power=1.0)
        assert 0 <= T <= 1

    def test_run_tasks(self):
        machine = SigmaMachine(MachineConfig(n_modes=5))

        # Test various tasks
        result = machine.run("zeta_computation", {"omega": 3.5, "pump_power": 1.0})
        assert isinstance(result, ComputationResult)
        assert result.converged

        result = machine.run("gue_sampling", {"n_samples": 100, "n_pbits": 50})
        assert result.output.shape == (100, 50)

    def test_result_serialization(self):
        result = ComputationResult(
            output=np.array([1.0, 2.0]),
            computation_time=1.0,
            energy_cost=0.1,
            information_gain=0.5,
            critical_parameter=1.0,
            converged=True
        )

        json_str = result.to_json()
        result2 = ComputationResult.from_json(json_str)
        assert np.allclose(result.output, result2.output)

    def test_config_file(self):
        config = MachineConfig(n_modes=50, parallel=False)
        config.to_file("/tmp/test_config.json")

        config2 = MachineConfig.from_file("/tmp/test_config.json")
        assert config2.n_modes == 50
        assert config2.parallel is False

    def test_cache(self):
        machine = SigmaMachine(MachineConfig(cache_results=True))
        params = {"omega": 3.5, "pump_power": 1.0}

        r1 = machine.run("zeta_computation", params)
        r2 = machine.run("zeta_computation", params)

        # Second call should be cached
        assert len(machine._result_cache) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
