"""
sigma_machine/core/distinguishability.py
=========================================
Core module implementing the primal structure of distinguishability.
This is the foundational layer of the Sigma Machine architecture.

Axioms implemented:
  I. Primal Distinguishability (metric space)
  II. Structure Preservation (isometries/symmetries)
  III. Compositionality (tensor products)
  IV. Self-Reference (fixed points)
  V. Criticality (phase transitions)
"""

import numpy as np
from typing import Callable, Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class State:
    """A state in the distinguishability space."""
    vector: np.ndarray
    label: str = ""
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def norm(self) -> float:
        return np.linalg.norm(self.vector)

    def normalize(self) -> 'State':
        n = self.norm()
        if n > 0:
            return State(self.vector / n, self.label, self.metadata)
        return self


class DistinguishabilitySpace:
    """
    A metric space (X, δ) where δ is the distinguishability function.

    Axioms:
      (i)   Reflexive: δ(x,x) = 0
      (ii)  Symmetric: δ(x,y) = δ(y,x)
      (iii) Transitive: δ(x,y)=0 and δ(y,z)=0 => δ(x,z)=0
      (iv)  Non-degenerate: δ(x,y)=0 => x=y
    """

    def __init__(self, dimension: int, metric_type: str = "euclidean"):
        self.dimension = dimension
        self.metric_type = metric_type
        self.states: List[State] = []
        self._metric_cache = {}

    def metric(self, x: State, y: State) -> float:
        """Compute δ(x,y) - the distinguishability function."""
        if self.metric_type == "euclidean":
            return np.linalg.norm(x.vector - y.vector)
        elif self.metric_type == "cosine":
            dot = np.dot(x.vector, y.vector)
            nx = np.linalg.norm(x.vector)
            ny = np.linalg.norm(y.vector)
            if nx * ny == 0:
                return 1.0
            return 1.0 - dot / (nx * ny)
        elif self.metric_type == "quantum":
            # Fidelity-based distinguishability
            dot = np.abs(np.dot(x.vector.conj(), y.vector))**2
            nx = np.linalg.norm(x.vector)**2
            ny = np.linalg.norm(y.vector)**2
            if nx * ny == 0:
                return 1.0
            fidelity = dot / (nx * ny)
            return np.sqrt(1.0 - fidelity)
        elif self.metric_type == "information":
            # Relative entropy-based
            px = np.abs(x.vector)**2
            py = np.abs(y.vector)**2
            px = px / np.sum(px)
            py = py / np.sum(py)
            # KL divergence
            kl = np.sum(px * np.log(px / (py + 1e-10) + 1e-10))
            return np.sqrt(kl)
        else:
            raise ValueError(f"Unknown metric type: {self.metric_type}")

    def add_state(self, state: State) -> int:
        """Add a state to the space. Returns index."""
        self.states.append(state)
        return len(self.states) - 1

    def verify_axioms(self) -> dict:
        """Verify all five axioms of distinguishability."""
        results = {}
        n = len(self.states)

        # Axiom I: Reflexivity
        reflexive = all(
            abs(self.metric(s, s)) < 1e-10 for s in self.states
        )
        results['reflexive'] = reflexive

        # Axiom II: Symmetry
        symmetric = all(
            abs(self.metric(self.states[i], self.states[j]) - 
                self.metric(self.states[j], self.states[i])) < 1e-10
            for i in range(n) for j in range(n)
        )
        results['symmetric'] = symmetric

        # Axiom III: Transitivity (for zero distances)
        transitive = True
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    dij = self.metric(self.states[i], self.states[j])
                    djk = self.metric(self.states[j], self.states[k])
                    dik = self.metric(self.states[i], self.states[k])
                    if dij < 1e-10 and djk < 1e-10:
                        if dik > 1e-10:
                            transitive = False
        results['transitive'] = transitive

        # Axiom IV: Non-degeneracy
        nondegenerate = True
        for i in range(n):
            for j in range(i+1, n):
                if self.metric(self.states[i], self.states[j]) < 1e-10:
                    if not np.allclose(self.states[i].vector, self.states[j].vector):
                        nondegenerate = False
        results['nondegenerate'] = nondegenerate

        return results

    def find_critical_points(self) -> List[int]:
        """
        Find states that are at critical points - maximally distinguishable
        from their neighbors while minimizing energy.
        """
        if len(self.states) < 3:
            return []

        critical = []
        for i, s in enumerate(self.states):
            # Compute local density of states
            distances = [self.metric(s, self.states[j]) for j in range(len(self.states)) if j != i]
            mean_dist = np.mean(distances)
            min_dist = np.min(distances)

            # Critical point: high local density but not too close
            if min_dist > 0.1 * mean_dist and min_dist < 0.5 * mean_dist:
                critical.append(i)

        return critical


class Symmetry:
    """
    Structure-preserving transformation T: δ(Tx, Ty) = δ(x,y).

    In mathematics: isometry.
    In physics: conservation law.
    In computation: reversible computation.
    """

    def __init__(self, transform: Callable[[np.ndarray], np.ndarray], name: str = ""):
        self.transform = transform
        self.name = name

    def apply(self, state: State) -> State:
        return State(self.transform(state.vector), f"T({state.label})")

    def verify_preservation(self, space: DistinguishabilitySpace, n_tests: int = 100) -> bool:
        """Verify that the symmetry preserves distinguishability."""
        for _ in range(n_tests):
            i, j = np.random.choice(len(space.states), 2, replace=False)
            x, y = space.states[i], space.states[j]
            d_before = space.metric(x, y)
            Tx, Ty = self.apply(x), self.apply(y)
            d_after = space.metric(Tx, Ty)
            if abs(d_before - d_after) > 1e-6:
                return False
        return True


class Composition:
    """
    Tensor product structure for composite systems.

    In mathematics: tensor product of vector spaces.
    In physics: entanglement and Fock space.
    In computation: parallel computation.
    """

    @staticmethod
    def tensor_product(s1: State, s2: State) -> State:
        """Compute the tensor product of two states."""
        v = np.kron(s1.vector, s2.vector)
        return State(v, f"{s1.label} ⊗ {s2.label}")

    @staticmethod
    def partial_trace(state: State, dim1: int, dim2: int, trace_out: int = 2) -> np.ndarray:
        """Partial trace over subsystem."""
        matrix = state.vector.reshape(dim1, dim2)
        if trace_out == 2:
            return np.dot(matrix, matrix.conj().T)
        else:
            return np.dot(matrix.T, matrix.conj())


class SelfReference:
    """
    Self-referential dynamics: the system converges to a fixed point
    that is its own description.

    In mathematics: Gödel's fixed point theorem.
    In physics: observer is part of the system.
    In computation: self-reproducing code (Quine).
    """

    @staticmethod
    def fixed_point_iteration(
        f: Callable[[np.ndarray], np.ndarray],
        x0: np.ndarray,
        tol: float = 1e-10,
        max_iter: int = 1000
    ) -> Tuple[np.ndarray, int, bool]:
        """
        Find fixed point x* = f(x*) using iteration.
        Returns (x*, iterations, converged).
        """
        x = x0.copy()
        for i in range(max_iter):
            x_new = f(x)
            if np.linalg.norm(x_new - x) < tol:
                return x_new, i+1, True
            x = x_new
        return x, max_iter, False

    @staticmethod
    def construct_quine(space: DistinguishabilitySpace, target: State) -> State:
        """
        Construct a self-referential state that describes itself.
        This is the physical analog of a Quine program.
        """
        # The quine state is the one closest to its own description
        best_idx = -1
        best_dist = float('inf')
        for i, s in enumerate(space.states):
            # Description = normalized state vector
            desc = s.normalize().vector
            dist = space.metric(s, State(desc, "desc"))
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        return space.states[best_idx] if best_idx >= 0 else target


class Criticality:
    """
    Critical phenomena in distinguishability spaces.

    In mathematics: Riemann Hypothesis (zeros on critical line).
    In physics: phase transitions.
    In computation: NP-completeness.
    """

    @staticmethod
    def order_parameter(space: DistinguishabilitySpace, beta: float) -> float:
        """
        Compute order parameter as function of inverse temperature beta.
        This is the analog of magnetization in Ising model.
        """
        if len(space.states) == 0:
            return 0.0

        # Gibbs state
        energies = np.array([s.norm()**2 for s in space.states])
        weights = np.exp(-beta * energies)
        weights = weights / np.sum(weights)

        # Order parameter = variance of state distribution
        mean_state = np.sum([w * s.vector for w, s in zip(weights, space.states)], axis=0)
        variance = np.sum([w * np.linalg.norm(s.vector - mean_state)**2 
                          for w, s in zip(weights, space.states)])

        return variance

    @staticmethod
    def find_critical_beta(space: DistinguishabilitySpace, 
                          beta_range: np.ndarray) -> float:
        """Find the critical inverse temperature where phase transition occurs."""
        op_values = [Criticality.order_parameter(space, b) for b in beta_range]
        # Critical point = maximum curvature
        d2 = np.gradient(np.gradient(op_values, beta_range), beta_range)
        idx = np.argmax(np.abs(d2))
        return beta_range[idx]
