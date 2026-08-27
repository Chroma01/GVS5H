
## ideation
**Core difficulty**

We have a deterministic process: we know the N intervals in order. For any starting rating X, we can simulate step‑by‑step: for each contest i, if current rating ∈ [L_i, R_i] we add 1. The rating never decreases, so it is a monotonic walk.

We need to answer up to 3·10⁵ queries of the form “starting at X, what is the final rating after all N contests?”.

Naively simulating each query would be O(N) per query → O(N·Q) ≈ 6·10¹⁰ which is impossible.
