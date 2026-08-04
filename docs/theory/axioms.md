# The Five Axioms of Distinguishability

## Axiom I: Primal Distinguishability

There exists a fundamental operation $\delta(x,y)$ that determines whether two entities $x$ and $y$ are distinguishable.

**Properties:**
- Reflexive: $\delta(x,x) = 0$
- Symmetric: $\delta(x,y) = \delta(y,x)$
- Non-negative: $\delta(x,y) \geq 0$

**Physical interpretation:** Measurement.
**Computational interpretation:** Bit comparison.

## Axiom II: Structure Preservation

Any valid transformation $T$ must preserve distinguishability:

$$\delta(Tx, Ty) = \delta(x,y)$$

**Mathematical:** Isometry.
**Physical:** Symmetry (conservation law).
**Computational:** Reversible computation.

## Axiom III: Weak Transitivity (v2.0 Fix)

For quantum-compatible systems:

$$\delta(x,y) < \varepsilon \land \delta(y,z) < \varepsilon \implies \delta(x,z) < 2\varepsilon + O(\varepsilon^2)$$

This replaces the classical strict transitivity which fails for quantum superposition states.

## Axiom IV: Self-Reference with Bounded Recursion (v2.0 Fix)

The system can model itself, but with bounded recursion depth $d_{\max}$:

$$x^* = f^{(d_{\max})}(x^*)$$

This prevents Russell-type infinite regress.

## Axiom V: Criticality

The system operates at the critical point where information, energy, and complexity are balanced:

$$\mathcal{C}[\text{state}] = E - T \cdot S_{\text{info}} + \lambda \cdot \text{Complexity}$$
