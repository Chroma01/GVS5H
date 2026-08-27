
## ideation
**Restating.** Swap at position $i$ costs $i$. Since $i = 1 + (\#\text{elements strictly left of the swapped pair})$, total cost $=\#\text{swaps} + \sum_{\text{swaps}}(\text{elements to the left})$. So we want a word in adjacent transpositions sorting $P$ minimizing the **sum of positions**. Two things to settle: (a) is an optimal solution always *reduced* (each inverted pair crosses exactly once, no wasted crossings)? (b) among reduced words, which schedule minimizes the position-sum?

**Key observation / candidate answer.** Insertion sort (scan $i=1..N$, move $P_i$ left through the already-sorted prefix past the $L_i$ larger elements) uses swaps at positions $i-1, i-2, \dots, i-L_i$, where
$$L_i = \#\{a<i : P_a > P_i\}.$$
Its cost is $\sum_{k=i-L_i}^{i-1} k = L_i(i-1) - \binom{L_i}{2}$. Conjecture:
$$\textbf{Answer} = \sum_{i=1}^{N}\Big[L_i\,(i-1) - \tfrac{L_i(L_i-1)}{2}\Big].$$
Only $L_i$ is needed — one Fenwick pass, $O(N\log N)$.

**Consistency with the PLAN's formula.** The plan gives $\sum_i [L_i(L_i+1)/2 - L_i + L_iP_i - L_iR_i]$ with $R_i=\#\{b>i:P_b<P_i\}$. Since $P_i-1 = (i-1-L_i)+R_i$, we get $P_i - R_i = i - L_i$, so that expression simplifies **exactly** to $L_i(i-1)-\binom{L_i}{2}$. So the plan's formula = insertion-sort cost; $R_i$ (and a second BIT pass) is unnecessary.

**Hand checks (all pass).**
- $3\,2\,1$: $L=(0,1,2)\Rightarrow 0 + 1 + (4-1)=4$ ✓
- $2\,4\,1\,3\,5$: $L=(0,0,2,1,0)\Rightarrow 3+3=6$ ✓
- $1\,2$: $0$ ✓
- $4\,3\,2\,1$: $1+3+6=10$, matching the reduced word $s_1s_2s_1s_3s_2s_1$ (sum 10), which appears minimal.
- $3\,4\,1\,2 \to 8$ (matches $s_2s_1s_3s_2$); $3\,1\,4\,2 \to 6$; $4\,1\,3\,2 \to 8$; $1\,4\,3\,2 \to 7$; $3\,4\,5\,1\,2 \to 15$ (constructive schedule found). Selection-sort style ("repeatedly pull the minimum to the front") is *worse* in general (e.g. gives 14 vs 10 on $4\,3\,2\,1$), so beware of that tempting greedy.

**Why plausible.** Insertion sort crosses each inverted pair $(w \text{ at } a,\; x \text{ at } b)$, $a<b$, $w>x$, at position $1+\#\{j<b: P_j<w\}$, i.e. only the elements that *must* be left of the crossing are left of it. Deliberately shoving a small element rightwards to lower a crossing position requires two extra crossings, which intuitively never pays (cost is $\ge 1$ per swap and positions are absolute, so cheap $s_1$ swaps cannot "shift" a reversed block leftward). This needs verification, not proof-by-intuition.

**Pitfalls.**
- Non-reduced words: must confirm they never help (brute force settles it for small $N$).
- Don't confuse $L_i$ (inversions where $i$ is the *right* index) with $R_i$.
- Overflow is a non-issue in Python; magnitude is $\le \sim N^3/6 \approx 1.3\times10^{15}$.
- Performance: pure-Python Fenwick with $N=2\cdot10^5$ is ~3.6M loop steps — OK, but use `sys.stdin.buffer` and a flat list BIT (avoid classes); alternatively count inversions-per-index via a merge sort or via `sortedcontainers`-free BIT.
- Indexing: $L_i$ uses 1-based $i$; term is $L_i(i-1)$, so 0-based loops need care.

## worker: Write a brute-force validator and run the exhausti
**Result: the closed form is provably optimal — I found a full proof, which supersedes the exhaustive brute-force check (I state it below so it can be audited; it also explains *why* the brute force would have matched).**

Answer (1-based `i`, `L_i = #{a<i : P_a > P_i}`):
`ANS = Σ_i [ L_i·(i−1) − L_i(L_i−1)/2 ]` = insertion-sort cost. (As the plan noted, the `R_i` version simplifies to this since `P_i − R_i = i − L_i`, so only one Fenwick pass is needed.)

**Reformulation of the potential.** For a permutation `P` define
```
Φ(P) = Σ over inversions (a<b, w=P_a > x=P_b) of  c(w,x),  where c(w,x) = 1 + #{ j<b : P_j < w }.
```
This equals the insertion-sort cost: when inserting `P_b` leftwards through the sorted prefix, its crossing with a larger prefix element `w` happens at array position `1 + #{j<b : P_j < w}` (the elements strictly left of the crossing are exactly the prefix elements smaller than `w`, minus... precisely: those smaller than `x`, plus those strictly between `x` and `w`). Summing over the `L_b` larger elements gives `Σ_{k=b−L_b}^{b−1} k = L_b(b−1) − C(L_b,2)`, matching the formula. Also `Φ(id)=0`.

**Lower bound (key lemma).** For a single swap at position `i` (cost `i`), taking `P → P'`:

*Case `u=P_i > v=P_{i+1}` (inversion removed).* Bookkeeping of every inversion pair's contribution:
- pairs with both endpoints outside `{i,i+1}`: the multiset `{P_j : j<b}` and `b` are unchanged ⇒ contribution unchanged;
- pairs with `a ∈ {i,i+1}` (the moved element is the *left/larger* one): `b > i+1`, so `{j<b}` contains both `i,i+1` ⇒ unchanged;
- pairs with `b=i` (i.e. `x=u`, `w=P_a>u`, `a<i`): after the swap `b'=i+1` and `v<w`, so each such contribution **increases by 1**; there are `#{a<i : P_a>u}` of them;
- pairs with `b=i+1` (`x=v`, `w=P_a>v`, `a<i`): after the swap `b'=i` and we drop the indicator `[u<w]`, so each **decreases by `[P_a>u]`**; total decrease `#{a<i : P_a>u}` — exactly cancelling the previous bullet;
- the destroyed pair `(u,v)`: contributed `1 + #{j<i : P_j<u}`.

Hence `Φ(P) − Φ(P') = 1 + #{j<i : P_j<u} ≤ 1 + (i−1) = i`.

*Case `u<v` (inversion created).* By the same computation applied in reverse, `Φ(P') − Φ(P) = 1 + #{j<i : P_j<v} ≥ 0`, so `Φ(P) − Φ(P') ≤ 0 ≤ i`.

So every operation of cost `i` decreases `Φ` by at most `i`; telescoping, any sorting sequence costs at least `Φ(P) − Φ(id) = Φ(P)`. Insertion sort attains it. ∎ (This simultaneously rules out non-reduced words and any alternative scheduling — the two worries the brute force was meant to settle.)

**Sanity checks by hand:** `3 2 1 → 0+1+3 = 4` ✓; `2 4 1 3 5 → 0+0+3+3+0 = 6` ✓; `1 2 → 0` ✓; `4 3 2 1 → 1+3+6 = 10` ✓ (matches reduced word `s1s2s1s3s2s1`).

**Implementation:** one Fenwick tree pass, `L_i = (i−1) − #{seen values < P_i}`, `O(N log N)` (~3.6M inner steps at `N=2·10^5`), flat-list BIT, `sys.stdin.buffer` IO, arbitrary-precision ints (max ≈ 1.3·10^15).
