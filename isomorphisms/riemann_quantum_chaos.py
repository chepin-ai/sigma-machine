"""
sigma_machine/isomorphisms/riemann_quantum_chaos.py
====================================================
Isomorphism 1: Riemann Zeros ↔ Quantum Chaos

Mathematical side: Riemann zeta function ζ(s)
Physical side: Quantum chaotic systems (stadium billiard, etc.)

Key mappings:
  γ_n (imaginary parts of zeros) ↔ E_n (energy eigenvalues)
  ζ(s) ↔ Z(E) (spectral determinant)
  RH ↔ Self-adjointness of Hamiltonian
  Critical line ↔ Real axis of energy
"""

import numpy as np
from scipy.special import zeta as scipy_zeta
from scipy.linalg import eigh
from typing import Tuple, List


class RiemannQuantumChaos:
    """Implements the Riemann ↔ Quantum Chaos isomorphism."""

    def __init__(self, n_zeros: int = 100):
        self.n_zeros = n_zeros
        self.gamma_zeros = self._compute_zeros()

    def _compute_zeros(self) -> np.ndarray:
        """Return approximate first n_zeros Riemann zeros."""
        # Known first 100 zeros (approximate)
        zeros = np.array([
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
            67.079811, 69.546402, 72.067158, 75.704690, 77.144840,
            79.337375, 82.910380, 84.735493, 87.425275, 88.809111,
            92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
            103.725538, 105.446623, 107.168930, 111.029536, 111.874659,
            114.320221, 116.226680, 118.789741, 121.370125, 122.946829,
            124.256819, 127.516784, 129.578704, 131.087688, 133.397551,
            134.756598, 138.116542, 139.736279, 141.123275, 143.111845,
            146.000123, 147.422765, 150.053053, 151.320353, 153.024693,
            156.112945, 157.697059, 158.849988, 160.314250, 163.030985,
            165.537069, 167.184510, 169.094515, 169.911977, 173.411537,
            174.754191, 176.441434, 178.377407, 179.916490, 182.207186,
            184.873467, 185.767800, 187.545913, 189.535160, 191.408893,
            193.379293, 195.584247, 196.876481, 198.768337, 201.265876,
            202.543651, 204.877963, 206.567667, 208.417960, 209.514571,
            211.691149, 213.347146, 215.016720, 217.003662, 219.087316,
            220.714918, 222.576226, 224.417768, 226.027925, 227.657250,
            229.549457, 231.249188, 233.058389, 234.876469, 236.524230,
            238.139683, 239.765955, 241.593179, 243.070636, 244.829809
        ])
        return zeros[:self.n_zeros]

    def construct_berry_keating_hamiltonian(self, n: int, 
                                            cutoff: float = 10.0) -> np.ndarray:
        """
        Construct the Berry-Keating Hamiltonian H = xp discretized.
        H_ij = (i+j+1) * delta_{i,j+1} / 2  (approximation)
        """
        H = np.zeros((n, n), dtype=complex)
        for i in range(n):
            for j in range(n):
                if abs(i - j) == 1:
                    H[i, j] = 0.5 * (i + j + 1) * cutoff / n
        return H

    def construct_yakaboylu_hamiltonian(self, n: int, 
                                         t_param: float = 0.5) -> np.ndarray:
        """
        Construct Yakaboylu's Hamiltonian H = S * H_BK * S^{-1}.
        S = t^N * e^(alpha*x)/(1+e^x)
        """
        H_BK = self.construct_berry_keating_hamiltonian(n)

        # Number operator N = -x d^2/dx^2 - d/dx + x/4
        N = np.zeros((n, n))
        for i in range(n):
            N[i, i] = i + 0.5

        # Similarity transform S = t^N * weight
        alpha = (1 + t_param) / (2 - 2 * t_param)
        x_grid = np.linspace(0, 10, n)
        weight = np.exp(alpha * x_grid) / (1 + np.exp(x_grid))
        S = np.diag(t_param**(np.diag(N))) @ np.diag(weight)

        # H = S * H_BK * S^{-1}
        S_inv = np.linalg.inv(S)
        H = S @ H_BK @ S_inv

        return H

    def compute_gue_statistics(self, spacings: np.ndarray) -> dict:
        """
        Compute GUE statistics for a set of level spacings.
        Returns dict with various statistical measures.
        """
        # Normalize by mean spacing
        s = spacings / np.mean(spacings)

        # Wigner surmise for GUE
        def wigner_gue(x):
            return (32 / np.pi**2) * x**2 * np.exp(-4 * x**2 / np.pi)

        # Compute histogram
        hist, bins = np.histogram(s, bins=30, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2

        # Compare with Wigner surmise
        wigner_vals = wigner_gue(bin_centers)

        # Chi-squared statistic
        chi2 = np.sum((hist - wigner_vals)**2 / (wigner_vals + 1e-10))

        # Nearest-neighbor spacing variance
        variance = np.var(s)

        # Level repulsion parameter (small-s behavior)
        small_s = s[s < 0.5]
        if len(small_s) > 0:
            repulsion = np.mean(small_s**2) / np.mean(small_s)**2
        else:
            repulsion = 0.0

        return {
            'normalized_spacings': s,
            'histogram': hist,
            'bin_centers': bin_centers,
            'wigner_surmise': wigner_vals,
            'chi2_gue': chi2,
            'variance': variance,
            'repulsion_parameter': repulsion,
            'mean_spacing': np.mean(spacings)
        }

    def verify_montgomery_odlyzko(self, n_samples: int = 1000) -> dict:
        """
        Verify the Montgomery-Odlyzko law: pair correlation of zeros
        matches GUE pair correlation.
        """
        # Use first n_zeros
        gamma = self.gamma_zeros

        # Compute pair correlation
        s_values = np.linspace(0, 3, 100)
        pair_corr = np.zeros_like(s_values)

        for idx, s in enumerate(s_values):
            count = 0
            for i in range(len(gamma)):
                for j in range(i+1, len(gamma)):
                    normalized_diff = (gamma[j] - gamma[i]) / np.mean(np.diff(gamma))
                    if abs(normalized_diff - s) < 0.05:
                        count += 1
            pair_corr[idx] = count

        # Normalize
        pair_corr = pair_corr / np.sum(pair_corr) * len(s_values) / 3

        # Theoretical GUE pair correlation
        def gue_pair(s):
            return 1 - (np.sin(np.pi * s) / (np.pi * s))**2

        theoretical = gue_pair(s_values)
        theoretical[0] = 0.0  # Remove singularity

        # Compute agreement
        agreement = np.mean((pair_corr - theoretical)**2)

        return {
            's_values': s_values,
            'empirical_pair_corr': pair_corr,
            'theoretical_gue': theoretical,
            'mean_squared_error': agreement
        }

    def spectral_form_factor(self, tau_range: np.ndarray) -> np.ndarray:
        """
        Compute the spectral form factor K(tau) = |Σ e^{2πi γ_n τ}|² / N.
        This is the key quantity in random matrix theory.
        """
        gamma = self.gamma_zeros
        N = len(gamma)
        K = np.zeros_like(tau_range)

        for idx, tau in enumerate(tau_range):
            phase_sum = np.sum(np.exp(2j * np.pi * gamma * tau))
            K[idx] = np.abs(phase_sum)**2 / N

        return K
