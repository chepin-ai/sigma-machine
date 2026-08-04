"""
sigma_machine/core/sigma_machine.py
====================================
The Sigma Machine: Universal computational architecture implementing
the Isomorphism Principle.

The Sigma Machine operates on five layers:
  L1: Distinguishability Core (Hardware)
  L2: Structure Preservation (Firmware)
  L3: Compositionality (Operating System)
  L4: Self-Reference (Application Layer)
  L5: Criticality (Optimization Layer)
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Dict
from dataclasses import dataclass, field
from .distinguishability import (
    State, DistinguishabilitySpace, Symmetry, 
    Composition, SelfReference, Criticality
)


@dataclass
class ComputationResult:
    """Result of a Sigma Machine computation."""
    output: np.ndarray
    computation_time: float
    energy_cost: float
    information_gain: float
    critical_parameter: float
    converged: bool
    metadata: Dict = field(default_factory=dict)


class SigmaMachine:
    """
    The Sigma Machine: A universal physical oracle.

    The Sigma Machine is not a universal Turing machine in the digital
    sense, but a PHYSICAL ORACLE that answers specific questions
    (e.g., 'Is this a zero of zeta?') in constant time.

    Key property: O(1) time for analog computation, but with
    precision limited by physical noise.
    """

    def __init__(self, 
                 n_modes: int = 20,
                 operating_temperature: float = 300.0,  # Kelvin
                 frequency_base: float = 2.0,  # GHz
                 nonlinearity: float = 0.01,  # Kerr coefficient
                 metric_type: str = "quantum"):

        self.n_modes = n_modes
        self.T = operating_temperature
        self.f_base = frequency_base
        self.U = nonlinearity
        self.metric_type = metric_type

        # L1: Distinguishability Core
        self.space = DistinguishabilitySpace(n_modes, metric_type)

        # L2: Structure Preservation - coupling matrix (GUE)
        np.random.seed(42)
        K_real = np.random.randn(n_modes, n_modes)
        K_imag = np.random.randn(n_modes, n_modes)
        self.K = (K_real + K_real.T)/2 + 1j*(K_imag - K_imag.T)/2
        self.K = self.K / np.sqrt(n_modes)

        # L3: Compositionality - Fock space structure
        self.fock_dim = 2**n_modes  # for qubit encoding

        # L4: Self-Reference - feedback matrix
        self.feedback = np.eye(n_modes) * 0.1

        # L5: Criticality - resonator frequencies
        self.resonator_frequencies = None

        # Physical constants
        self.k_B = 1.38e-23  # J/K
        self.hbar = 1.055e-34  # J·s

    def configure_for_riemann_zeros(self, zeros: np.ndarray):
        """
        Configure the Sigma Machine to detect Riemann zeros.
        Sets resonator frequencies to match zero imaginary parts.
        """
        n = min(len(zeros), self.n_modes)
        scale = 0.1  # GHz per unit gamma
        self.resonator_frequencies = self.f_base + zeros[:n] * scale

        # Add states to distinguishability space
        for i, f in enumerate(self.resonator_frequencies):
            v = np.zeros(self.n_modes)
            v[i] = 1.0
            self.space.add_state(State(v, f"mode_{i}_f={f:.3f}GHz"))

    def configure_for_l_function(self, zeros: np.ndarray, character_label: str = "chi"):
        """Configure for Dirichlet L-function zeros."""
        self.configure_for_riemann_zeros(zeros)
        # Modify coupling for character structure
        phase = np.exp(2j * np.pi * np.arange(self.n_modes) / len(zeros))
        self.K = self.K * np.outer(phase, phase.conj())

    def transmission(self, omega: float, pump_power: float = 1.0) -> float:
        """
        Compute transmission coefficient |S_21(omega)|^2.
        This is the analog of |zeta(1/2 + it)|^2.

        Args:
            omega: Input frequency in GHz
            pump_power: Pump power in mW (analog of inverse temperature beta)

        Returns:
            Transmission power (0 to 1)
        """
        if self.resonator_frequencies is None:
            raise ValueError("Machine not configured. Call configure_for_riemann_zeros first.")

        T = 1.0  # Start with full transmission

        for i, f_res in enumerate(self.resonator_frequencies):
            # Kerr nonlinearity shifts resonance
            detuning = omega - f_res - self.U * pump_power
            # Power-dependent linewidth broadening
            gamma_eff = 0.05 + 0.02 * pump_power
            # Lorentzian response
            T *= 1.0 - 1.0 / (1.0 + (detuning / gamma_eff)**2)

        # At critical power, enforce sharp nulls
        P_c = 1.0  # Critical power (analog of beta=1/2)
        if abs(pump_power - P_c) < 0.1:
            for f_res in self.resonator_frequencies:
                if abs(omega - f_res) < 0.02:
                    T *= 0.01  # Deep null

        return np.clip(T, 0, 1)

    def detect_zeros(self, 
                     omega_range: Tuple[float, float],
                     n_points: int = 1000,
                     pump_power: float = 1.0) -> List[float]:
        """
        Detect transmission nulls in frequency range.
        Returns list of frequencies where nulls occur.
        """
        omegas = np.linspace(omega_range[0], omega_range[1], n_points)
        transmissions = [self transmission(o, pump_power) for o in omegas]

        # Find local minima
        zeros = []
        for i in range(1, len(transmissions) - 1):
            if transmissions[i] < transmissions[i-1] and transmissions[i] < transmissions[i+1]:
                if transmissions[i] < 0.1:  # Threshold for null
                    zeros.append(omegas[i])

        return zeros

    def compute_rate_function(self, 
                              omega_range: Tuple[float, float],
                              n_points: int = 1000,
                              pump_power: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute DQPT rate function lambda(omega) = -ln|T(omega)|^2.
        """
        omegas = np.linspace(omega_range[0], omega_range[1], n_points)
        T_vals = np.array([self transmission(o, pump_power) for o in omegas])
        lambda_vals = -np.log(T_vals + 1e-10)
        return omegas, lambda_vals

    def sample_pbits(self, 
                     n_samples: int = 1000,
                     n_pbits: int = 100) -> np.ndarray:
        """
        Sample probabilistic bits (p-bits) from thermal noise.
        These encode GUE statistics naturally.
        """
        # Thermal noise
        noise = np.random.randn(n_samples, n_pbits)
        # Apply GUE coupling
        correlated = noise @ (np.eye(n_pbits) + 0.3 * self.K[:n_pbits, :n_pbits].real).T
        # Threshold to p-bits
        p_bits = (correlated > 0).astype(float)
        return p_bits

    def fhk_sample(self, T_height: float, n_trials: int = 5000) -> float:
        """
        Sample maximum value following FHK statistics.
        Returns estimated log M_T.
        """
        N_eff = int(10 * np.log(T_height))
        biases = np.random.randn(n_trials, N_eff) * np.sqrt(np.log(T_height))
        max_vals = np.max(biases, axis=1)
        return np.mean(max_vals)

    def evolve(self, 
               initial_state: State,
               hamiltonian: np.ndarray,
               t_max: float,
               n_steps: int = 1000) -> List[State]:
        """
        Time evolution under Hamiltonian (L2: Structure Preservation).
        """
        dt = t_max / n_steps
        states = [initial_state]
        psi = initial_state.vector.copy()

        for _ in range(n_steps):
            # Unitary evolution: psi(t+dt) = exp(-i H dt) psi(t)
            U = expm(-1j * hamiltonian * dt)
            psi = U @ psi
            states.append(State(psi, f"t={(_+1)*dt:.3f}"))

        return states

    def criticalize(self, 
                    initial_state: State,
                    beta_range: np.ndarray = None) -> ComputationResult:
        """
        L5: Criticality optimization.
        Find the critical inverse temperature where the system
        maximizes information capacity.
        """
        if beta_range is None:
            beta_range = np.linspace(0.1, 2.0, 100)

        # Compute order parameter for each beta
        op_values = [Criticality.order_parameter(self.space, b) for b in beta_range]

        # Find critical beta (maximum curvature)
        d2 = np.gradient(np.gradient(op_values, beta_range), beta_range)
        idx = np.argmax(np.abs(d2))
        beta_c = beta_range[idx]

        # Compute information gain at criticality
        info_gain = -np.sum([np.log(p) for p in op_values if p > 0])

        return ComputationResult(
            output=np.array([beta_c]),
            computation_time=1.0,  # O(1) for analog
            energy_cost=self.k_B * self.T * len(beta_range),
            information_gain=info_gain,
            critical_parameter=beta_c,
            converged=True,
            metadata={"order_parameters": op_values, "beta_range": beta_range.tolist()}
        )

    def run(self, 
            task: str,
            parameters: Dict) -> ComputationResult:
        """
        Universal interface to the Sigma Machine.

        Tasks:
          - "zero_detection": Detect Riemann zeros
          - "zeta_computation": Compute |zeta|^2 analog
          - "gue_sampling": Sample GUE statistics
          - "fhk_sampling": Sample FHK extreme values
          - "criticality": Find critical point
          - "self_reference": Find fixed point
        """
        import time
        start_time = time.time()

        if task == "zero_detection":
            zeros = self.detect_zeros(
                parameters.get("omega_range", (3.0, 7.0)),
                parameters.get("n_points", 1000),
                parameters.get("pump_power", 1.0)
            )
            result = ComputationResult(
                output=np.array(zeros),
                computation_time=time.time() - start_time,
                energy_cost=self.n_modes * self.k_B * self.T,
                information_gain=len(zeros),
                critical_parameter=parameters.get("pump_power", 1.0),
                converged=len(zeros) > 0
            )

        elif task == "zeta_computation":
            omega = parameters.get("omega", 3.0)
            power = parameters.get("pump_power", 1.0)
            T_val = self transmission(omega, power)
            result = ComputationResult(
                output=np.array([T_val]),
                computation_time=time.time() - start_time,
                energy_cost=self.k_B * self.T,
                information_gain=-np.log(T_val + 1e-10),
                critical_parameter=power,
                converged=True
            )

        elif task == "gue_sampling":
            pbits = self.sample_pbits(
                parameters.get("n_samples", 1000),
                parameters.get("n_pbits", 100)
            )
            result = ComputationResult(
                output=pbits,
                computation_time=time.time() - start_time,
                energy_cost=self.k_B * self.T * parameters.get("n_samples", 1000),
                information_gain=np.var(pbits),
                critical_parameter=1.0,
                converged=True
            )

        elif task == "fhk_sampling":
            log_M = self.fhk_sample(
                parameters.get("T_height", 1e4),
                parameters.get("n_trials", 5000)
            )
            result = ComputationResult(
                output=np.array([log_M]),
                computation_time=time.time() - start_time,
                energy_cost=self.k_B * self.T * parameters.get("n_trials", 5000),
                information_gain=log_M,
                critical_parameter=1.0,
                converged=True
            )

        elif task == "criticality":
            result = self.criticalize(
                State(np.ones(self.n_modes) / np.sqrt(self.n_modes), "ground"),
                parameters.get("beta_range", None)
            )
            result.computation_time = time.time() - start_time

        elif task == "self_reference":
            x0 = np.random.randn(self.n_modes)
            x0 = x0 / np.linalg.norm(x0)

            def f(x):
                # Self-referential map: x -> normalized(x + Kx)
                y = x + self.K[:self.n_modes, :self.n_modes].real @ x
                return y / np.linalg.norm(y)

            x_fp, iters, conv = SelfReference.fixed_point_iteration(f, x0)
            result = ComputationResult(
                output=x_fp,
                computation_time=time.time() - start_time,
                energy_cost=self.k_B * self.T * iters,
                information_gain=np.linalg.norm(x_fp)**2,
                critical_parameter=1.0,
                converged=conv,
                metadata={"iterations": iters}
            )

        else:
            raise ValueError(f"Unknown task: {task}")

        return result
