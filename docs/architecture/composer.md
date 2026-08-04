# IsomorphismComposer

## Purpose

Composes the 5 deep isomorphisms into a unified framework, resolving the v1.0 issue where isomorphisms were isolated.

## Usage

```python
from sigma_machine import SigmaMachine

machine = SigmaMachine()

# Compose isomorphisms along a path
result = machine.run("compose_isomorphisms", {
    "start_iso": "riemann_chaos",
    "end_iso": "info_thermo",
    "data": np.array([1.0])
})

print(f"Path: {result.metadata['path']}")
# Output: ['riemann_chaos', 'langlands_qft', 'ncg_sm', 
#          'twistor_amplitudes', 'info_thermo']
```

## Verification

```python
# Verify commutative diagram
composer = machine.composer
is_commutative = composer.verify_commutative_diagram(
    path1=["riemann_chaos", "langlands_qft"],
    path2=["riemann_chaos", "info_thermo", "langlands_qft"],
    test_data=np.array([1.0])
)
```
