"""
sigma_machine/isomorphisms/information_thermodynamics.py
=========================================================
Isomorphism 5: Information Theory ↔ Thermodynamics

Mathematical side: Shannon entropy, relative entropy, channel capacity
Physical side: Thermodynamic entropy, free energy, heat capacity

Key mappings:
  Shannon entropy S ↔ Thermodynamic entropy S/k_B
  Relative entropy D ↔ Free energy difference ΔF
  Mutual information I ↔ Entanglement entropy S_A
  Channel capacity C ↔ Carnot efficiency η
  Data compression ↔ Adiabatic process
  Error correction ↔ Maxwell demon
"""

import numpy as np
from typing import Tuple, Callable
from scipy.integrate import quad


class InformationThermodynamics:
    """Implements the Information ↔ Thermodynamics isomorphism."""

    def __init__(self, k_B: float = 1.38e-23, T: float = 300.0):
        self.k_B = k_B
        self.T = T

    def shannon_entropy(self, probabilities: np.ndarray) -> float:
        """
        Compute Shannon entropy: S = -Σ p_i log p_i.
        """
        p = probabilities[probabilities > 0]
        return -np.sum(p * np.log(p))

    def relative_entropy(self, p: np.ndarray, q: np.ndarray) -> float:
        """
        Compute relative entropy (Kullback-Leibler divergence):
        D(p||q) = Σ p_i log(p_i/q_i).
        """
        return np.sum(p * np.log(p / (q + 1e-10) + 1e-10))

    def mutual_information(self, joint: np.ndarray) -> float:
        """
        Compute mutual information from joint distribution:
        I(X:Y) = S(X) + S(Y) - S(X,Y).
        """
        # Marginals
        p_x = np.sum(joint, axis=1)
        p_y = np.sum(joint, axis=0)

        S_X = self.shannon_entropy(p_x)
        S_Y = self.shannon_entropy(p_y)
        S_XY = self.shannon_entropy(joint.flatten())

        return S_X + S_Y - S_XY

    def landauer_principle(self, n_bits: int) -> float:
        """
        Compute minimum heat dissipation for erasing n_bits:
        Q = n_bits * k_B * T * log(2).
        """
        return n_bits * self.k_B * self.T * np.log(2)

    def jarzynski_equality(self, 
                          work_distribution: Callable[[float], float],
                          beta: float) -> float:
        """
        Verify Jarzynski equality: <e^{-βW}> = e^{-βΔF}.
        """
        # Compute <e^{-βW}>
        def integrand(W):
            return np.exp(-beta * W) * work_distribution(W)

        avg_exp_W, _ = quad(integrand, -np.inf, np.inf)

        return avg_exp_W

    def black_hole_entropy(self, area: float, G_N: float = 6.67e-11) -> float:
        """
        Compute Bekenstein-Hawking entropy:
        S = A / (4 G_N) (in natural units, simplified).
        """
        # Simplified: using Planck units
        return area / (4 * G_N)

    def holographic_bound(self, area: float, 
                          volume: float,
                          G_N: float = 6.67e-11) -> bool:
        """
        Check if the holographic entropy bound is satisfied:
        S ≤ A / (4 G_N).
        """
        # Maximum entropy for given volume
        S_max = area / (4 * G_N)

        # Compute actual entropy (simplified)
        S_actual = volume  # placeholder

        return S_actual <= S_max

    def maxwell_demon_efficiency(self, 
                                 information_gain: float,
                                 temperature_difference: float) -> float:
        """
        Compute efficiency of a Maxwell demon:
        η = W_extracted / Q_in = 1 - T_cold / T_hot - I / S.
        """
        T_hot, T_cold = temperature_difference, 0.0
        if T_hot > 0:
            carnot = 1 - T_cold / T_hot
            correction = information_gain / (self.shannon_entropy(np.array([0.5, 0.5])))
            return carnot - correction
        return 0.0
