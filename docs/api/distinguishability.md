# Distinguishability API

## Classes

### `State`

| Method | Description |
|--------|-------------|
| `__init__(vector, label, metadata)` | Create state |
| `norm()` | L2 norm |
| `normalize()` | Return normalized copy |
| `to_dict()` | Serialize to dict |
| `from_dict(d)` | Deserialize from dict |

### `DistinguishabilitySpace`

| Method | Description |
|--------|-------------|
| `__init__(config)` | Create space |
| `metric(x, y)` | Compute δ(x,y) |
| `add_state(state)` | Add state |
| `verify_axioms()` | Check all axioms |
| `compute_distance_matrix()` | Full distance matrix |
| `find_critical_points()` | Find critical states |
| `to_json()` | Serialize |
| `from_json(s)` | Deserialize |

### `SpaceConfig`

| Field | Default | Description |
|-------|---------|-------------|
| `dimension` | 2 | State dimension |
| `metric_type` | "euclidean" | Metric type |
| `tolerance` | 1e-10 | Numerical tolerance |
| `max_states` | 10000 | Max states |
| `enable_caching` | True | LRU cache |
| `quantum_weak_transitivity` | True | v2.0 fix |
