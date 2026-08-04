# SigmaMachine API

## Classes

### `SigmaMachine`

| Method | Description |
|--------|-------------|
| `__init__(config)` | Create machine |
| `configure_for_riemann_zeros(zeros)` | Set resonator frequencies |
| `transmission(omega, power)` | Compute \|S₂₁\|² |
| `detect_zeros(range, n_points)` | Find nulls |
| `sample_pbits(n_samples, n_pbits)` | GUE statistics |
| `run(task, params)` | Universal interface |
| `visualize(result)` | Plot results |

### `MachineConfig`

| Field | Default | Description |
|-------|---------|-------------|
| `n_modes` | 20 | Number of modes |
| `operating_temperature` | 300.0 | Temperature (K) |
| `frequency_base` | 2.0 | Base frequency (GHz) |
| `nonlinearity` | 0.01 | Kerr coefficient |
| `parallel` | True | Parallel execution |
| `n_workers` | CPU-1 | Worker processes |
| `cache_results` | True | Result caching |

### `ComputationResult`

| Field | Description |
|-------|-------------|
| `output` | Computation output |
| `computation_time` | Time (seconds) |
| `energy_cost` | Energy (Joules) |
| `information_gain` | Information (bits) |
| `critical_parameter` | Critical value |
| `converged` | Convergence flag |

## CLI Usage

```bash
# Detect zeros
python -m sigma_machine --task zero_detection --n-modes 20

# Criticality analysis
python -m sigma_machine --task criticality --config config.json

# With visualization
python -m sigma_machine --task gue_sampling --visualize
```
