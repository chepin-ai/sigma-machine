#!/usr/bin/env python3
"""
Example 1: Detect Riemann Zeros with Sigma Machine
====================================================
This example demonstrates how to configure the Sigma Machine
to detect transmission nulls corresponding to Riemann zeros.
"""

import numpy as np
import matplotlib.pyplot as plt
from sigma_machine.core import SigmaMachine

# Initialize Sigma Machine with 20 modes
machine = SigmaMachine(n_modes=20, frequency_base=2.0)

# Configure for first 20 Riemann zeros
zeros = np.array([
    14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
    37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
    52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
    67.0798, 69.5464, 72.0672, 75.7047, 77.1448
])
machine.configure_for_riemann_zeros(zeros)

# Scan frequency range
freqs = np.linspace(3.0, 7.0, 1000)
T_vals = [machine.transmission(f, pump_power=1.0) for f in freqs]

# Plot transmission spectrum
plt.figure(figsize=(12, 5))
plt.plot(freqs, T_vals, 'b-', linewidth=1)
for z in zeros[:5]:
    f_z = 2.0 + z * 0.1
    plt.axvline(f_z, color='r', linestyle='--', alpha=0.5)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Transmission |S_21|^2')
plt.title('Sigma Machine: Riemann Zero Detection')
plt.grid(True, alpha=0.3)
plt.savefig('zero_detection.png', dpi=150)
print("Saved zero_detection.png")
