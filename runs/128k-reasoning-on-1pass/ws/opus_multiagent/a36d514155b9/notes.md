
## ideation
**Core idea (symmetry / linearity of expectation over pairs).**
Fix any two distinct cells $u,v$. The number of valid arrangements in which both $u$ and $v$ hold a piece is the same for every pair: choose the remaining $k-2$ pieces among the other $mn-2$ cells, i.e. $\binom{mn-2}{k-2}$. Hence

$$\text{answer} = \binom{mn-2}{k-2}\cdot S,\qquad S=\sum_{\{u,v\}} \big(|x_u-x_v|+|y_u-y_v|\big).$$

**Computing $S$ (sum of Manhattan distance over all unordered cell pairs).**
Manhattan distance separates into row part and column part.
- Row part: for each pair of rows at distance $d$ ($1\le d\le m-1$) there are $(m-d)$ such row pairs, and each row has $n$ cells, so $n^2$ cell pairs per row pair. Contribution $= n^2\sum_{d=1}^{m-1} d(m-d)$.
- Also pairs in the *same* row contribute 0 to the row part, so nothing missed.
- Symmetrically for columns.

With $T(t)=\sum_{d=1}^{t-1} d(t-d) = \frac{t^3-t}{6} = \binom{t+1}{3}$:
$$S = n^2 T(m) + m^2 T(n).$$

**Sanity checks.**
- $m=n=2,k=2$: $T(2)=1$, $S=4+4=8$, $\binom{2}{0}=1$ → 8 ✓.
- $m=1,n=4,k=3$: $T(1)=0$, $T(4)=10$, $S=16\cdot0+1\cdot10=10$, $\binom{2}{1}=2$ → 20 ✓.

**Complexity.** $O(mn)$ for a factorial table up to $mn\le 10^5$; $O(1)$ for $S$. Trivially within limits.

**Pitfalls to watch.**
- Note that the "distance sum" here counts each unordered pair once (per the examples), not ordered pairs — do not double count.
- $k = mn$ edge case: $\binom{mn-2}{mn-2}=1$; also $k=2$ gives $\binom{mn-2}{0}=1$. Since $2\le k\le mn$, $0\le k-2\le mn-2$ always, so the binomial is never degenerate/negative. Also $mn\ge 2$ so $mn-2\ge 0$ (factorial table needs size $\ge 1$).
- $m=1$ or $n=1$: $T(1)=0$, formula still correct.
- Modular division by 6: either use `pow(6, MOD-2, MOD)` or (simpler in Python) compute $T(t)=(t^3-t)//6$ exactly as a Python int (fits easily, $t\le 10^5$) and then reduce mod. Integer division is exact since $t^3-t=(t-1)t(t+1)$ is divisible by 6.
- Reduce $n^2$, $m^2$ mod $10^9+7$ before multiplying (or just rely on Python bigints and mod at the end — $S$ is at most ~$10^{20}$, harmless).
- Avoid `math.comb` on huge values if worried about cost; modular factorials + Fermat inverse is safe and $O(mn)$.
- Don't try to enumerate arrangements or do DP over placements — the combinatorial identity is essential.

## worker: Write the complete `Solution.distanceSum` implemen
- Every unordered pair of distinct cells is simultaneously occupied in exactly `C(mn-2, k-2)` valid arrangements, so the answer factors as `C(mn-2, k-2) * S` where `S` is the total Manhattan distance over all unordered cell pairs.
- `S = n^2 * T(m) + m^2 * T(n)` with `T(t) = Σ_{d=1}^{t-1} d(t-d) = (t^3 - t)/6` (exact integer division since `(t-1)t(t+1)` is divisible by 6).
- Verified on the samples: (2,2,2) → `T(2)=1`, `S=8`, `C(2,0)=1` → 8 ✓; (1,4,3) → `T(1)=0`, `T(4)=10`, `S=10`, `C(2,1)=2` → 20 ✓.
- Factorial tables built up to `mn ≤ 1e5` (with a floor of 2 to keep indexing safe), `nCr` guards out-of-range arguments. Complexity O(mn) time, O(mn) memory.
- Edge cases: `k=2` → `C(mn-2,0)=1`; `k=mn` → `C(mn-2,mn-2)=1`; `m=1` or `n=1` handled since `T(1)=0`.
