# Core Module

## DistinguishabilitySpace

```python
from sigma_machine import DistinguishabilitySpace, SpaceConfig

config = SpaceConfig(
    dimension=10,
    metric_type="quantum",
    tolerance=1e-10,
    quantum_weak_transitivity=True  # v2.0 fix
)

space = DistinguishabilitySpace(config)
```

## State

```python
from sigma_machine import State
import numpy as np

state = State(
    vector=np.array([1.0, 0.0]),
    label="|0⟩",
    metadata={"basis": "computational"}
)
```

## SigmaMachine

```python
from sigma_machine import SigmaMachine, MachineConfig

machine = SigmaMachine(MachineConfig(
    n_modes=20,
    parallel=True,
    cache_results=True
))
```
