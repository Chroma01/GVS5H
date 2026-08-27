
## ideation
**Reformulation.** If the whole procedure uses $m$ operations, the total cost is $\sum_{j=1}^m W_j$ where $W_j$ = weight of the "on" set after op $j$. Equivalently, each index $k$ contributes $C_k\cdot(\#\text{ops after which }k\text{ is on})$.

**Which indices get flipped.**
- $A_k=B_k=0$: never touch (turning it on costs $\ge C_k>0$ and adds 2 ops, which can only raise other coefficients).
- $A_k=1,B_k=0$ (set $P$): flipped once (off-event).
- $A_k=0,B_k=1$ (set $Q$): flipped once (on-event).
- $A_k=B_k=1$ (set $R$): either untouched (on all the time, contributes $m\,C_k$) or flipped twice (off then on) — set $T\subseteq R$. More flips than this never helps (extra ops only add cost / shift coefficients upward).

**Cost for a fixed flip multiset.** With $m=|P|+|Q|+2|T|$:
$$\text{cost}=m\,(\mathrm{Sum}R-\mathrm{Sum}T)+\sum_{\text{off-events}}c\,(pos-1)+\sum_{\text{on-events}}c\,(m-pos+1).$$
Off-events want early positions, on-events want late positions, so an exchange argument shows the optimal order is **all off-events first, then all on-events** (this also automatically satisfies "off before on" for each $T$ element). Then by rearrangement: off-costs sorted **descending** get coefficients $0,1,\dots,K-1$; on-costs sorted **ascending** get coefficients $L,\dots,1$. Using $\sum_i (i-1)d_i=\sum_{\text{unordered pairs}}\min$:
$$\boxed{\text{cost}(T)=m(\mathrm{Sum}R-\mathrm{Sum}T)+\mathrm{mp}(P\cup T)+\big(\mathrm{Sum}Q+\mathrm{Sum}T\big)+\mathrm{mp}(Q\cup T)}$$
where $\mathrm{mp}(X)=\sum_{\{x,y\}\subseteq X}\min(x,y)$, $K=|P|+|T|$, $L=|Q|+|T|$, $K+L=m$.

**Choice of $T$.** For fixed $t=|T|$, take the $t$ **largest** elements of $R$: replacing $c\in T$ by $c'\in R\setminus T$ with $\delta=c'-c>0$ raises $\mathrm{mp}(P\cup T)$ by $\le (K-1)\delta$, $\mathrm{mp}(Q\cup T)$ by $\le (L-1)\delta$, $\mathrm{Sum}$ by $\delta$, total $\le (m-1)\delta$, while the first term drops by exactly $m\delta$ — strict improvement. So just sweep $t=0..|R|$ over $R$ sorted descending.

**Incremental update.** Adding a new value $c=r_t$ (smaller than all previously added $r$'s):
$\mathrm{mp}$ increases by $(\text{sum of existing elements} < c) + c\cdot(\text{count of existing elements}\ge c)$. For the static part $P$ (or $Q$) use sorted array + prefix sums + `bisect_left`; for the already-added $t-1$ elements of $R$ (all $\ge c$) it's simply $c\,(t-1)$. Ties are harmless because $\min(c,c)=c$ either way. Total $O(N\log N)$.

**Check on sample 1:** $P=\{6,9\},Q=\{4\},R=\{2\}$; $\mathrm{mp}(P)=6$. $t=0$: $m=3$, cost $=3\cdot2+6+4+0=16$ ✓. $t=1$: $m=5$, cost $=0+10+6+2=18$. Answer 16 ✓. Sample 2: all in $R$, $t=0\Rightarrow m=0\Rightarrow 0$ ✓.

**Pitfalls.**
- Don't forget the plain $\mathrm{Sum}(Q\cup T)$ term (from coefficient $L+1-i$, not $L-i$).
- $t=0$ must be included; empty sets ⇒ answer 0.
- Numbers are big (~$10^{16}$–$10^{17}$) but Python ints are fine; avoid floats.
- Fast input parsing (`sys.stdin.buffer.read().split()`); avoid per-element Python loops with heavy work (2·10^5 is fine).
- Careful: $R$ sorted **descending** for the sweep; prefix sums of $P,Q$ sorted **ascending** for bisect.

## worker: *Core implementation + sweep task:** Write the com
Implemented exactly the planned formula.

- Partition indices: `P = {A=1,B=0}` (off-events), `Q = {A=0,B=1}` (on-events), `R = {A=B=1}` (candidates for a temporary off→on toggle pair), and `A=B=0` ignored.
- `mp(X) = Σ_{unordered pairs} min(x,y)` computed for an ascending sorted list as `Σ_i x_i·(n−i)` (1‑indexed), which is the closed form of the optimal-ordering cost (off-events descending get coefficients 0..K−1; on-events ascending get K..1 → an extra plain `Sum` term).
- Cost for a chosen `T ⊆ R` (with `m = |P|+|Q|+2|T|`):
  `cost = m·(SumR − sumT) + mp(P∪T) + mp(Q∪T) + (SumQ + sumT)`.
- For fixed `t = |T|` the optimum is the `t` largest of `R` (exchange argument in the plan: swapping up by δ costs ≤ (m−1)δ in the pair/sum terms but saves exactly mδ), so we sweep `t = 0..|R|` over `R` sorted descending.
- Incremental update when adding `c` (smaller than all previously added R-values): `mp` grows by (sum of existing elements < c) + c·(count of existing elements ≥ c) = `prefP[i] + c·(nP−i) + c·(t−1)` with `i = bisect_left(P, c)`; ties are fine since min(c,c)=c either way.
- Complexity O(N log N), all integer arithmetic. Verified by hand on sample 1 (t=0 → 16, t=1 → 18, answer 16) and sample 2 (all in R, t=0 → m=0 → 0). Sample 3 relies on the same formula.
- Input parsing uses raw bytes comparison (`b'1'`) to avoid int conversion of A/B.

## worker: *Testing task:** Write a brute-force checker (Dijk
**What I did**

1. **Refactored** the solution into `solve(n,A,B,C)` + thin I/O wrapper, and **embedded the brute-force checker** (`_brute`: Dijkstra over all `2^N` states, edge = flip one bit, edge cost = weight of the *resulting* state) plus a randomized comparison harness `_selftest()` (400 random cases, `N ≤ 8`, `C ∈ [1,5]`, covering `N=1`, `A=B`, `B=¬A`, `A` all-zero (P,R empty), `A` all-one (Q empty), and all-equal `C`), together with the three provided samples. It runs only via `python prog.py selftest`, so normal judging (plain stdin run) is unaffected.

2. **Hand-verified all three samples** against the formula:
   - Sample 1: `P={6,9}, Q={4}, R={2}`; t=0 → `3·2+6+4=16`, t=1 → `0+10+6+2=18` ⇒ **16** ✓
   - Sample 2: everything in `R`, t=0 ⇒ `m=0` ⇒ **0** ✓
   - Sample 3: `P={1,22,27,52,73,79,90,97}` (mp=949), `Q={2,13,15,54}` (mp=47, SumQ=84), `R={72,67,46}` (SumR=185).
     t=0: `12·185+949+47+84 = 3300`; t=1 (c=72): mpP=1339, mpQ=131, `14·113+1339+131+84+72 = 3208`; t=2 (c=67): mpP=1776, mpQ=282, `16·46+1776+282+84+139 = 3017`; t=3 (c=46): mpP=2148, mpQ=450, `0+2148+450+84+185 = ` **2867** ✓ (matches the expected output exactly — a strong end-to-end check of the incremental `bisect`/prefix-sum update, including the tie/`c·(t−1)` term).

3. **Closed the remaining proof gap** (that no index is flipped more than the minimum number of times), which is what the brute force was mainly meant to probe:
   Take an optimal schedule with the fewest operations. If some index has two *consecutive* flips of it that are "on then off" (i.e. it is **on** during the ops strictly between them), delete both flips: every remaining op keeps or lowers its weight (weights of the ops in between drop by `C_k`), and two nonnegative op-costs disappear ⇒ strictly better/equal with fewer ops, contradiction. Hence:
   - `A=B=0` with 2 flips ⇒ that pair is on-then-off ⇒ impossible ⇒ 0 flips;
   - `A=B=1` with ≥4 flips ⇒ flips 2,3 form an on-then-off pair ⇒ at most 2 flips (necessarily off then on);
   - `A=1,B=0` with 3 flips ⇒ flips 2,3 are on-then-off ⇒ exactly 1; `A=0,B=1` with 3 ⇒ flips 1,2 are on-then-off ⇒ exactly 1.
   Together with the already-proved facts (adjacent-transposition argument ⇒ all off-events precede all on-events, feasible for `T`; rearrangement ⇒ off-events descending, on-events ascending; exchange argument ⇒ for fixed `t` take the `t` largest of `R` since the pair terms grow by ≤ `(m−1)δ` while `m·SumT` saves `mδ`), the formula
   `cost(T) = m(SumR−SumT) + mp(P∪T) + mp(Q∪T) + SumQ + SumT`, minimized over `t = 0..|R|`, is **provably optimal**.

4. Also sanity-checked small cases by hand against the direct optimum: `N=1 (0→1,C=5) → 5`; `N=1 (1→0,C=5) → 0`; `A=(1,1),B=(0,1),C=(3,10) → 10` (toggling R gives 13); `A=(1,1,1),B=(0,0,1),C=(10,10,100) → 130` via the temporary toggle (brute path: 20+10+0+100), confirming the `t>0` branch is exercised and correct.

No mismatches found; arithmetic is pure integer, complexity `O(N log N)`, parsing via `sys.stdin.buffer.read()`.
