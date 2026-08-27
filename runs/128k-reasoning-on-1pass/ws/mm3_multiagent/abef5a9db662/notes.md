
## ideation
**Core difficulty**  
We have a sequence of N contests. For each contest we know an interval [L,R] and the rule *if the current rating lies inside the interval, increase it by 1*.  
For many initial ratings X (up to 3·10⁵ queries) we need the final rating after all contests.  
A naïve simulation per query would be O(N·Q) (≈ 6·10¹⁰) and is impossible.

**Key observation – monotonicity**  
Let f[i] be the rating after processing some contests when the initial rating is i.  
Initially f[i]=i, which is non‑decreasing.  
When a contest is applied, the set of indices whose rating lies in [L,R] is a single contiguous interval, because both conditions “f[i] ≥ L” and “f[i] ≤ R” are monotone. Adding 1 to this whole interval preserves the order, so the monotonicity holds for all steps.

Because of monotonicity we can answer “which indices are increased?” with only the first index a where f[a] ≥ L and the last index b where f[b] ≤ R.  
Thus a contest corresponds to a **range‑add +1** on a known interval.

**Required operations**  
We need a data structure that supports, for a dynamic array f:

* range addition (+1) on an interval,
* “first index with value > val” (to find a and b),
* point query (final value of a given index).

A lazy segment tree storing only the **maximum** in each node suffices:
* range add is handled by lazy propagation,
* “first index with value > val” is found by descending the tree (if left child’s max > val go left, else right),
* point query follows the path while pushing lazy tags.

**Size bound**  
The rating can increase at most N times, so the final value for any query never exceeds  
`max_X + N`. Hence we can limit the domain to `M = max_X + N` (≤ 7·10⁵).  
All leaves beyond M are set to –1; they never affect the searches because they are never > 0.
