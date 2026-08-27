
## ideation
**Core structure.** Since each $P_i$ is uniform on $\{1,\dots,i-1\}$ independently, $T(P)$ is a uniform *random recursive tree*, and
$$\text{Answer} = (N-1)!\cdot \mathbb{E}[\mathrm{dist}(u,v)].$$
Use $\mathrm{dist}(u,v)=d(u)+d(v)-2d(\mathrm{lca}(u,v))$ with $d(x)$ = weighted depth, then linearity of expectation over "is vertex $i$ an ancestor(-or-self)" indicators.

**Fact 1 (single ancestor prob).** For $i<x$: $\Pr[i \text{ anc } x]=1/i$.
Proof by induction on $x$: $\Pr = \frac{1}{x-1}+\sum_{j=i+1}^{x-1}\frac{1}{x-1}\cdot\frac1i=\frac{1}{x-1}\cdot\frac{i+(x-1-i)}{i}=\frac1i$. ✓ (checked $N=3$: $\Pr[2\text{ anc }3]=1/2$).

**Fact 2 (joint ancestor prob).** For $i<u<v$: $\Pr[i \text{ anc both } u,v]=\dfrac{2}{i(i+1)}$, independent of $u,v$.
Hand-verified: $(i,u,v)=(2,3,4)\Rightarrow 1/3$; $(2,3,5)\Rightarrow 1/2\cdot 2/3=1/3$; $(3,4,5)\Rightarrow 1/6=2/12$. ✓
For $i=u$: probability is $\Pr[u\text{ anc }v]=1/u$. For $i>u$: $0$ (only smaller labels can be ancestors). Note $j$ is anc-or-self of $\mathrm{lca}(u,v)$ iff $j$ is anc-or-self of both $u$ and $v$ — that's why this sum gives $\mathbb{E}[d(\mathrm{lca})]$.

**Resulting O(1)-per-query formulas** (set $A_1=0$ so $u=1$ is automatic; assume $u<v$):
- $D(x)=A_x+\sum_{i=2}^{x-1}A_i\cdot i^{-1}$
- $L(x)=A_x\cdot x^{-1}+\sum_{i=2}^{x-1}2A_i\cdot i^{-1}(i+1)^{-1}$
- Answer $=(N-1)!\,\bigl(D(u)+D(v)-2L(u)\bigr) \bmod 998244353$.

Sanity check on Sample 1 ($N=3$, $A=(1,1)$, $(N-1)!=2$): $D(2)=1$, $D(3)=3/2$, $L(1)=0$ → queries give $2\cdot1=2$ and $2\cdot 3/2=3$. ✓ Sample 2: $N=2$, $1!\cdot D(2)=A_2=100$. ✓

**Pitfalls to watch.**
- Must multiply by $(N-1)!$ (not just output the expectation); $N\le 2\cdot10^5 < p$ so the factorial is nonzero and inverses $1..N+1$ all exist.
- Define $A_1=0$ and index arrays from 0/1 consistently; $L$ and $D$ use prefix sums up to $x-1$, plus the separate $x$-term with different coefficients ($1$ vs $x^{-1}$).
- Reduce $A_i\le 10^9$ mod $p$ before use.
- Queries guarantee $u<v$, but defensively take $u=\min,v=\max$; $u=v$ would give 0 anyway with the same formula ($D(u)+D(u)-2L(u)$ is *not* 0, so don't rely on it — but constraints forbid it).
- Python speed: use `sys.stdin.buffer.read().split()`, precompute inverses with the linear recurrence `inv[i] = -(p//i)*inv[p%i] % p`, build prefix arrays in one pass, join output.

## worker: Write the complete O(N+Q) Python solution: read al
Implemented the O(N+Q) solution exactly as planned.

Key facts (re-verified rigorously):
- Since each `P_i` is uniform on `{1,…,i-1}` independently, the number of trees is `(N-1)!` and the answer is `(N-1)! · E[dist(u,v)]`.
- `Pr[i is ancestor of x] = 1/i` for `i < x` (induction on x).
- Joint probability `c(i,u,v) = Pr[i anc of both u,v] = 2/(i(i+1))` for `i < u < v`. Proof by induction on `v`: conditioning on `P_v = j` uniform in `1..v-1`,
  `c = (1/(v-1))[ 1/i (j=i) + 1/i (j=u) + (v-2-i)·2/(i(i+1)) ] = 2/(i(i+1))`.
  Base `u=i+1, v=i+2` gives `(1/(i+1))·(2/i)` ✓.
- `j` is an ancestor-or-self of `lca(u,v)` iff it is an ancestor-or-self of both `u` and `v`, so `E[d(lca)] = A_u·(1/u) + Σ_{i=2}^{u-1} A_i·2/(i(i+1))` (with `A_1=0`, terms `i>u` vanish).
- Hence answer `= (N-1)!·(D(u)+D(v)-2L(u))` with `D(x)=A_x+Σ_{i<x}A_i/i`, `L(x)=A_x/x+Σ_{i<x}2A_i/(i(i+1))`, `D(1)=L(1)=0`.

Implementation details: linear inverse sieve up to `N+1` (needed since `x=N` uses `inv[N+1]`), running prefix sums updated *after* being used for the current vertex, `A_i` reduced mod p, defensive `u=min,v=max`, fast I/O and joined output. Verified by hand on Samples 1 and 2 (2 and 3; 100).
