
## ideation
The core insight: every inversion must be resolved by adjacent swaps, and each swap at boundary i costs i. For an inversion where element at position x (smaller position) has larger value than element at position y (x < y, P_x > P_y), the two elements must cross every boundary in [x, y-1] exactly once. So the total minimum cost = sum over all inversions (x,y) of (x + (x+1) + ... + (y-1)) = sum over inversions of (prefix_sum(y-1) - prefix_sum(x-1)) where prefix_sum(k) = 1+2+...+k = k(k+1)/2.

Why this is achievable: bubble-sort style — moving each element to its correct place via adjacent swaps crosses each required boundary exactly the forced number of times; no boundary needs more swaps than the number of inversions crossing it (each swap at boundary i reduces the "crossing count" there by exactly 1, and a standard argument shows you can always find an adjacent inverted pair to swap). So the lower bound equals the achievable cost.

Computation: iterate positions y from 1..N. For each y, consider all previously seen positions x with P_x > P_y (these form inversions with y). Contribution of each such inversion = S(y-1) - S(x-1) where S(k)=k(k+1)/2. So total contribution at step y = (count of such x) * S(y-1) - sum over such x of S(x-1). Maintain two Fenwick trees over positions: one storing counts, one storing S(x-1) values, keyed by value (we query over values > P_y, i.e., positions of values greater than current). Actually we key by value: when processing element with value v at position y, we need positions of already-seen values > v. So BIT indexed by value, storing count and sum of S(pos-1). Query range (v+1..N). O(N log N).

Pitfalls:
- Answer can be large: up to ~N^3 scale (N=2e5, inversions ~2e10, each contributing up to ~2e5) → up to ~4e15, fits in 64-bit but use Python int anyway (no overflow concern in Python).
- S(k) = k*(k+1)//2 with k up to N-1.
- Fenwick query for suffix: query total minus prefix(v).
- Don't confuse position-indexed vs value-indexed BIT; we need value-indexed since "greater value seen before" is the inversion condition.

## worker: Implement the final solution: read N and permutati
- Reasoning: process values 1..N in increasing order. When value v is inserted, all smaller values 1..v-1 are already placed. If pos[v] has rank r among {pos[1..v]}, then exactly v - r smaller values sit to the right of v, so v must move left past them. The relative order of values 1..v-1 is already correct (inductively), so v moves from rank r to rank v among them, crossing boundaries r, r+1, ..., v-1 exactly once, costing sum_{i=r}^{v-1} i = S(v-1) - S(r-1). Summing over v gives the minimum total cost (each inversion's forced boundary crossings are each paid exactly once).
- Fenwick tree over positions gives r in O(log N) per value → O(N log N) total.
- Sample checks:
  - N=3, P=(3,2,1): pos=[-,3,2,1]. v=1: p=3, r=1, ans+=S(0)-S(0)=0. v=2: p=2, r=1, ans+=S(1)-S(0)=1. v=3: p=1, r=1, ans+=S(2)-S(0)=3 → total 4. ✓
  - N=5, P=(2,4,1,3,5): pos=[-,3,1,4,2,5]. v=1: p=3,r=1,+0. v=2: p=1,r=1,+S(1)=1. v=3: p=4,r=3,+S(2)-S(2)=0. v=4: p=2,r=2,+S(3)-S(1)=6-1=5. v=5: p=5,r=5,+0 → total 6. ✓
  - N=2, P=(1,2): v=1: p=1,r=1,+0. v=2: p=2,r=2,+0 → 0. ✓
- Python ints avoid overflow; answer can be ~N^3/6 ≈ 1.3e15 for N=2e5.
