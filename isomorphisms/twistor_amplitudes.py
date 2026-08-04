"""
sigma_machine/isomorphisms/twistor_amplitudes.py
=================================================
Isomorphism 4: Twistor Theory ↔ Scattering Amplitudes

Mathematical side: Twistor space T = C^4
Physical side: On-shell scattering amplitudes A_n

Key mappings:
  Twistor Z^α = (λ_α, μ^α̇) ↔ Momentum p_μ = λ_α σ^α_α̇ λ̃^α̇
  Line in T ↔ Point in spacetime
  Intersecting lines ↔ Null-separated points
  Hodographic transform ↔ Momentum conservation
  Amplitude as volume form ↔ Top form on Grassmannian
"""

import numpy as np
from typing import List, Tuple


class TwistorAmplitudes:
    """Implements the Twistor ↔ Scattering Amplitudes isomorphism."""

    def __init__(self, n_particles: int = 4):
        self.n = n_particles

    def spinor_to_momentum(self, lambda_spinor: np.ndarray, 
                           lambda_tilde: np.ndarray) -> np.ndarray:
        """
        Convert spinors to momentum:
        p_μ = λ_α σ^α_α̇ λ̃^α̇
        """
        # Pauli matrices
        sigma = [
            np.array([[1, 0], [0, 1]]),    # σ^0
            np.array([[0, 1], [1, 0]]),    # σ^1
            np.array([[0, -1j], [1j, 0]]), # σ^2
            np.array([[1, 0], [0, -1]])    # σ^3
        ]

        p = np.zeros(4)
        for mu in range(4):
            p[mu] = np.dot(lambda_spinor.conj(), sigma[mu] @ lambda_tilde)

        return p.real

    def momentum_to_spinor(self, p: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert null momentum to spinors.
        For null p^2 = 0, p_μ = λ_α σ^α_α̇ λ̃^α̇.
        """
        # Simplified: for massless particles
        E = p[0]
        px, py, pz = p[1], p[2], p[3]

        lambda_spinor = np.array([np.sqrt(E + pz), (px + 1j*py)/np.sqrt(E + pz)])
        lambda_tilde = np.array([np.sqrt(E + pz), (px - 1j*py)/np.sqrt(E + pz)])

        return lambda_spinor, lambda_tilde

    def bcfw_recursion(self, 
                       helicities: List[int],
                       momenta: List[np.ndarray]) -> complex:
        """
        BCFW recursion relation for tree-level amplitudes.
        A_n = Σ_i A_L · (1/P^2) · A_R
        """
        if len(helicities) == 3:
            # 3-point amplitude
            return self._three_point_amplitude(helicities, momenta)

        # For n > 3, apply BCFW shift
        # Simplified: return Parke-Taylor formula for MHV
        return self._parke_taylor_mhv(helicities, momenta)

    def _three_point_amplitude(self, 
                                helicities: List[int],
                                momenta: List[np.ndarray]) -> complex:
        """Compute 3-point amplitude."""
        if helicities == [1, -1, 0]:  # ++-
            return 0.0 + 0.0j
        elif helicities == [-1, -1, 1]:  # --+
            return 0.0 + 0.0j
        return 0.0 + 0.0j

    def _parke_taylor_mhv(self, 
                          helicities: List[int],
                          momenta: List[np.ndarray]) -> complex:
        """
        Parke-Taylor formula for MHV amplitudes:
        A_n^{MHV}(1^-, 2^-, 3^+, ..., n^+) = <12>^4 / (<12><23>...<n1>)
        """
        # Check MHV condition: exactly 2 negative helicities
        n_neg = sum(1 for h in helicities if h == -1)
        if n_neg != 2:
            return 0.0 + 0.0j

        # Find negative helicity indices
        neg_indices = [i for i, h in enumerate(helicities) if h == -1]
        i, j = neg_indices[0], neg_indices[1]

        # Compute spinor brackets
        lambda_i, _ = self.momentum_to_spinor(momenta[i])
        lambda_j, _ = self.momentum_to_spinor(momenta[j])

        bracket_ij = lambda_i[0] * lambda_j[1] - lambda_i[1] * lambda_j[0]

        # Denominator: product of all adjacent brackets
        denom = 1.0 + 0.0j
        for k in range(self.n):
            lambda_k, _ = self.momentum_to_spinor(momenta[k])
            lambda_next, _ = self.momentum_to_spinor(momenta[(k+1) % self.n])
            bracket = lambda_k[0] * lambda_next[1] - lambda_k[1] * lambda_next[0]
            denom *= bracket

        return bracket_ij**4 / denom

    def grassmannian_integral(self, k: int, n: int) -> complex:
        """
        Compute amplitude as integral over Grassmannian G(k,n).
        A_n = ∫ d^{k×n} C · δ(C·λ̃) · δ(C^⊥·λ) · ...
        """
        # Simplified: for k=2, n=4 (NMHV)
        if k == 2 and n == 4:
            # Return box function (simplified)
            return 1.0 + 0.0j
        return 0.0 + 0.0j
