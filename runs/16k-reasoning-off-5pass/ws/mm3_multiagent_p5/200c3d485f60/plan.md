We need to count arrays of length n with values in [1,m] such that exactly k adjacent pairs are equal. A standard approach: choose the n−k "break" positions where the value changes. That is, we select k indices (out of n−1) to be equal to the previous one; the remaining n−1−k indices are changes. The array is determined by:
- Choosing the positions of the k equalities (combinations C(n−1, k)).
- Picking the first value: m choices.
- For each of the n−1−k change positions, the new value can be any of the m−1 values different from the previous one.

So answer = m * C(n−1, k) * (m−1)^(n−1−k) mod 1e9+7.
We precompute factorials and inverse factorials up to n (≤1e5) to compute C quickly, use fast exponentiation for (m−1)^(n−1−k), and handle edge case k = n−1 (no changes) by returning m (or formula with exponent 0 gives 1).