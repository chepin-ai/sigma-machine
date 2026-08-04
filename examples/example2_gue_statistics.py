#!/usr/bin/env python3
"""
Example 2: GUE Statistics from p-bits
=======================================
This example shows how the Sigma Machine's thermal noise
naturally generates GUE statistics.
"""

import numpy as np
import matplotlib.pyplot as plt
from sigma_machine.core import SigmaMachine

machine = SigmaMachine(n_modes=100)
pbits = machine.sample_pbits(n_samples=5000, n_pbits=100)

# Compute nearest-neighbor spacings
spacings = []
for row in pbits:
    ones = np.where(row == 1)[0]
    if len(ones) > 1:
        spacings.extend(np.diff(ones))

spacings = np.array(spacings)
if len(spacings) > 0:
    spacings_norm = spacings / np.mean(spacings)

    plt.figure(figsize=(10, 5))
    plt.hist(spacings_norm, bins=30, density=True, alpha=0.6, label='MNN p-bits')

    s = np.linspace(0, 4, 200)
    wigner = (32/np.pi**2) * s**2 * np.exp(-4*s**2/np.pi)
    poisson = np.exp(-s)
    plt.plot(s, wigner, 'r-', linewidth=2, label='GUE')
    plt.plot(s, poisson, 'g--', linewidth=2, label='Poisson')

    plt.xlabel('Normalized spacing')
    plt.ylabel('Probability density')
    plt.title('GUE Statistics from Sigma Machine p-bits')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('gue_statistics.png', dpi=150)
    print("Saved gue_statistics.png")
