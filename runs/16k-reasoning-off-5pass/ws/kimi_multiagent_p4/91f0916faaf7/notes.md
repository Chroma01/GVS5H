
## ideation
**Core structure.** For each edge i, write S_i/S_{i+1} = p_i/q_i in lowest terms; then p_i·q_i = A_i with gcd(p_i,q_i)=1. Since A_i ≤ 1000, its coprime ordered factorizations are exactly: for each prime power p^e || A_i, assign the whole p^e to either numerator or denominator. So each edge has 2^{ω(A_i)} choices (ω = number of distinct primes), at most 2^3 = 8 since A_i ≤ 1000 (2·3·5·7=210, ·11=2310>1000, so ω ≤ 3... actually 2·3·5·7=210 ≤ 1000 so ω can be 4? 2·3·5·7=210, yes ω(A_i) can be up to 4 for A_i in {210, 420, 630, 840, 330? 2·3·5·11=330, etc.} — primes 2,3,5,7 product 210 ≤ 1000, so ω up to 4, giving up to 16 factorizations).

**Chaining.** Given choices (p_i, q_i), consistency requires S_i = c · P_{<i} · Q_{>i} where P_{<i} = p_1...p_{i-1}, Q_{>i} = q_i...q_{N-1}. Wait — more precisely S_i/S_{i+1} = p_i/q_i forces S_i = c·∏_{j<i} p_j · ∏_{j≥i} q_j for a common rational c; positivity and integrality: c must be a positive rational such that all S_i integral. Actually the standard result: solutions are S_i = t · a_i where a_i = (∏_{j<i} p_j)(∏_{j≥i} q_j) and t ranges over positive rationals making everything integral — but since gcd conditions pin it down: the primitive solution is a_i / g where g = gcd(a_1,...,a_N), and all solutions are positive integer multiples of the primitive one. The gcd=1 condition then forces the sequence to be exactly the primitive one. So good sequences biject with choices of coprime ordered factorizations (p_i,q_i) of each A_i. That's why finitely many: at most ∏ 2^{ω(A_i)} sequences.

**Score.** Score = ∏_i S_i = ∏_i a_i / g^N where g = gcd of the a_i. Note a_i's prime factorization: for prime p, exponent in a_i is (sum of exponents assigned to numerators before i) + (sum assigned to denominators from i onward). Per prime p, the choices on each edge (numerator vs denominator) are independent across primes. So the total answer = sum over all per-edge sign assignments of ∏_i a_i / g^N.

**Key difficulty: the gcd division couples primes.** g = ∏_p p^{min_i e_p(i)}. So score = ∏_p p^{Σ_i e_p(i) - N·min_i e_p(i)}. Since primes are independent in the choice space, the total sum factorizes as a product over primes of per-prime DP values! Because the choice space is a Cartesian product over primes (each edge's factorization choice = independent per-prime binary choices), and the score factorizes as a product over primes of p^{...}. So:

Answer = ∏_{p} W_p, where W_p = Σ over per-edge binary choices (for edges where p | A_i) of p^{Σ_i e(i) − N·min_i e(i)}, with e(i) = exponent of p in a_i.

Wait, but careful: edges where p ∤ A_i contribute no choice and exponent 0. For a prime p dividing some set of edges, the exponent sequence: define on each edge j where p^e_j || A_i a choice σ_j ∈ {+1 (numerator), −1 (denominator)}. Then exponent of p in a_i = Σ_{j<i, σ_j=+} e_j + Σ_{j≥i, σ_j=−} e_j. Define prefix sums. Σ_i e(i) and min_i e(i) are determined. W_p = Σ_{σ} p^{Σ_i e(i) − N min_i e(i)}.

**DP per prime.** For prime p with edges j_1 < ... < j_k where it appears, exponents e_1..e_k (e ≤ 9 since 2^9=512, 2^10=1024>1000; for p≥3, e ≤ 6; etc.). We need Σ over 2^k sign assignments of p^{F(σ)} where F = Σ_i e(i) − N·min_i e(i). k ≤ N−1 ≤ 999, so we need an efficient DP, not 2^k.

Think of it as a path: define b_0 = 0, and walk: e(i) = (total exponent assigned to denominators among edges ≥ i) + (numerators among edges < i). Alternative: let T = Σ_j e_j (total). e(i) = Σ_{j<i} [σ_j=+] e_j + Σ_{j≥i} [σ_j=−] e_j. Consider the "profile" as i goes 0..N: define h_i = exponent of p in a_i for i=1..N. Then h_{i+1} = h_i + (σ_i=+ ? +e_i : −e_i)... check: a_{i+1} vs a_i: a_i has edge i contributing e_i if denominator; a_{i+1} has edge i contributing e_i if numerator. Other edges same side. So h_{i+1} = h_i + e_i if σ_i = numerator, h_{i+1} = h_i − e_i if denominator. So h is a walk with steps ±e_i, starting at h_1 = Σ_{j≥1, σ_j=−} e_j... hmm, actually h_1 = Σ_{j≥1, σ_j=−} e_j which depends on all choices. Better: define walk w_0 = 0, w_i = w_{i-1} + e_i·(σ_i=+ ? +1 : −1)? Then h_i = w_{i-1}... let me redo: h_i = Σ_{j<i, +} e_j + Σ_{j≥i, −} e_j. Define w_i = Σ_{j≤i, +} e_j − Σ_{j≤i, −} e_j (signed prefix). Then h_i = w_{i-1} + Σ_{j≥i, −} e_j + Σ_{j<i,−} e_j − ... hmm: h_i = Σ_{j<i,+} e_j + Σ_{j≥i,−} e_j = w_{i-1} + Σ_{j<i,−} e_j + Σ_{j≥i,−} e_j = w_{i-1} + (Σ_{all −} e_j) − ... no: Σ_{j<i,−} + Σ_{j≥i,−} = Σ_{all j, −} e_j =: D (total denominator exponent). So h_i = w_{i-1} + D. Nice: h_i = D + w_{i-1}, where w_0 = 0 and w_i = w_{i-1} ± e_i.

So Σ_i h_i = N·D + Σ_{i=0}^{N-1} w_i, and min_i h_i = D + min_{0≤i≤N-1} w_i. Thus F = Σ_i h_i − N·min_i h_i = Σ_{i=0}^{N-1} w_i − N·min_{0≤i≤N-1} w_i. The D cancels! So F depends only on the walk w (starting at 0, steps ±e_i for edges where p appears; edges where p doesn't appear contribute nothing — but wait, the walk indices: w_i defined only via edges with p; positions i where p doesn't appear in any edge still count in Σ over i=0..N-1 of w_i and min. Since w_i stays constant across gaps, gaps contribute multiplicity.)

So per prime: we have a walk of N positions (i=0..N−1), starting w_0=0; at each edge j where p | A_j, step ±e_j (choice); elsewhere stay. F = (Σ_{i=0}^{N-1} w_i) − N·min_i w_i. W_p = Σ_{walks} p^F.

**DP formulation.** Process positions i=0..N−1, tracking current level w and running min m, accumulating sum s = Σ w_i. State space: w ranges over possible signed sums — could be large (Σ e_j up to ~ 9·999). Too big? Total exponent sum per prime: e.g., p=2, each A_i ≤ 1000 contributes e ≤ 9, N=1000 → range ±9000, and min tracking another dimension → O(range²) states = 8·10⁷ per prime per step — too slow.

**Better transformation.** F = Σ_i (w_i − min w). Let v_i = w_i − min ≥ 0. Alternative: use the identity Σ_{i=0}^{N-1} w_i − N·min = Σ_{i} (w_i − min). Hmm.

Alternative approach: reflect / cycle-lemma style? Or: since steps are ±e_j, think of DP tracking (current height relative to min, i.e., w − min) and the accumulated Σ(w_i − min). When min decreases, all previous partial sums shift. Standard trick: DP over d = w − min ≥ 0, with weight p^{Σ (w_i − min)}: when we take a step that lowers w below min, d would go negative; instead we "shift": new min, and the accumulated sum increases by (old min − new min)·(number of steps so far +1). So DP state: (d, position) with value = Σ over walks of p^{accumulated Σ(w_j − min)}. Transition at a step of size e:
- Up step: d' = d + e, acc' = acc + d' (add new w_i − min). Multiply by p^{d'}.
- Down step: d − e ≥ 0: d' = d − e, multiply by p^{d'}.
- Down step below 0: new min = w − e... d' = 0? No: if d − e < 0, new min drops by e − d, so all previous i positions (i count = t+1 positions so far, where t = steps taken... positions counted so far in acc) get their (w_i − min) increased by (e − d). So acc' = acc + (e − d)·(count) + 0, where count = number of terms already summed (positions processed so far including current? need care). Then d' = 0... wait no: after the step, w_new − min_new = 0 only if the step lands exactly at new min — yes if it goes below old min, the new position is the new minimum, so d' = 0. Hmm but it could land below; new min = new w, d' = 0. Yes.

So DP per prime: state d ≥ 0, value = Σ p^{acc}. d ranges 0..(max possible w − min) ≤ total positive step sum ≤ ~9000 for p=2. Steps: N−1 ≤ 999. Per step transition O(1) per d. So O(N · maxd) per prime ≈ 1000·9000 = 9·10⁶ for p=2; primes 3,5,7,... have smaller exponent budgets (e ≤ 6 for 3, etc., and fewer multiples). Total across all primes: sum over p of (N · total exponent budget) — each A_i ≤ 1000 has total exponent sum ≤ 9+6+5+4... actually Ω(A_i) ≤ 9 (2^9=512, 2^10>1000). Sum over primes of budget = Σ_i Ω(A_i) ≤ 999·9 ≈ 9000. So total work ≈ N · 9000 ≈ 9·10⁶. 

But wait — the "count" multiplier: acc' = acc + (e−d)·count where count = number of positions processed so far (i.e., i index). Since positions include gaps (edges where p absent → w unchanged, still contributes w_i to sum and counts for min shifts). So we process all N positions i=0..N−1 in order; at each position, either a choice-step (if p | A_{i+1}... index carefully) or a "stay". For a stay: acc' = acc + d (add w_i − min = d), multiply by p^d. For a step at edge i (transition from w_{i-1} to w_i... need consistent indexing).

Let me re-index: positions t = 0..N−1 (w_0..w_{N-1}), F = Σ_{t=0}^{N-1} w_t − N min. w_0 = 0. Edge j (1-indexed, j=1..N−1) determines step from w_{j-1} to w_j: ±e_j if p | A_j, else w_j = w_{j-1}.

DP over t: before processing position t we have accumulated acc = Σ_{s<t} (w_s − min_{s<t} w_s) and d = w_{t-1} − min so far... Let me define processing: at each t from 0 to N−1: first, if t ≥ 1, apply step from edge t (choice or forced stay); then add current (w_t − min) to acc. Hmm, min updates during step. Let me define state after processing position t: d_t = w_t − min_{s≤t} w_s, acc_t = Σ_{s≤t} (w_s − min_{s≤t} w_s). Note acc uses final min so far, updated retroactively.

Init t=0: w_0 = 0, d=0, acc=0, weight 1.
Transition to t (≥1) with step size e (e=0 for stay, no choice):
- choice up (+e): d' = d + e; acc' = acc + d'; factor p^{d'}.
- choice down (−e): if d ≥ e: d' = d − e, acc' = acc + d', factor p^{d'}. If d < e: new min drops by (e − d); all t previous terms (s = 0..t−1, that's t terms) increase by (e−d); new term d' = 0. acc' = acc + (e−d)·t + 0; factor p^{(e−d)·t}. d' = 0.
- stay (e=0): d' = d, acc' = acc + d, factor p^d.

At end (t = N−1 processed), W_p = Σ over states of value (value already includes p^{acc}). 

Check factor for down-below-min: acc' − acc = (e−d)·t, so multiply DP value by p^{(e−d)·t}. Yes.

Number of terms: at time t (0-indexed), before adding position t, we have t terms (s=0..t−1). Correct.

**Combining.** Answer = ∏_{p prime} W_p mod 998244353. Primes involved: those dividing some A_i. For primes dividing no A_i, W_p = 1 (only trivial walk, F=0). 

Wait — is the factorization Answer = ∏ W_p exactly right? Total sum = Σ over global assignments (per edge, per prime, sign) of ∏_p p^{F_p(σ_p)}. Since assignment space = product over p of (sign assignments for edges with p), and summand factorizes, yes: total = ∏_p (Σ_{σ_p} p^{F_p}) = ∏_p W_p. 

But hold on: each edge's factorization choice must be consistent — choosing per-prime signs independently gives a unique coprime ordered factorization (p_i, q_i): p_i = ∏_{p: σ=+} p^{e}, q_i = ∏_{σ=−} p^e. Yes, bijection. And distinct sign assignments give distinct sequences? The sequence is determined by (p_i, q_i) via the primitive scaling — yes, good sequences biject with factorization choices (need to double check the claim that the primitive sequence has gcd 1 and every choice yields a valid good sequence — the constructed a_i satisfy S_i/S_{i+1} = p_i/q_i in lowest terms? S_i/S_{i+1} = a_i/a_{i+1} = p_i/q_i · (common factors cancel). Since gcd(p_i, q_i)=1 and a_i = c·(∏_{j<i} p_j)(∏_{j≥i} q_j), a_i/a_{i+1} = p_i/q_i exactly (telescoping), and after dividing by g the ratio is unchanged, and p_i/q_i is already reduced, so f = p_i q_i = A_i. ✓. And gcd of primitive sequence is 1 by construction. ✓.)

**Sanity check with sample 2.** N=2, A_1=9=3². Prime 3, one edge, e=2, positions t=0,1. Walks: up: w=(0,2), F = (0+2) − 2·0 = 2 → 3²=9. Down: w=(0,−2), F = −2 − 2·(−2) = 2 → 9. W_3 = 18. ✓ matches (sequences (9,1) score 9 and (1,9) score 9; sum 18 ✓).

**Check sample 1 partially?** Trust later via code test mentally is hard; rely on implementation.

**Complexity.** For each prime p: budget B_p = Σ_{i: p|A_i} e_p(A_i). d ranges 0..B_p. DP O(N·B_p). Σ B_p = Σ_i Ω(A_i) ≤ 999·9 ≈ 9000. Total O(N·9000) ≈ 9·10⁶ operations with modular exponentiation-by-precomputed powers. p^{d'} and p^{(e−d)·t}: exponents can be large (acc up to N·B ≈ 9·10⁶), so precompute powers of p up to needed exponent: max single factor exponent = max(d', (e−d)·t) ≤ max(B, B·N) — (e−d)·t can be up to B·N ≈ 9·10⁶. Precomputing p^k for k up to 9·10⁶ per prime is too much memory across primes but fine per prime if we only need p=2 worst case (9·10⁶ entries ~ 72 MB as Python ints — too much). Better: compute factor via pow(p, exponent, MOD) — Python's pow is fast (log exponent ~ 24 multiplications). 9·10⁶ pow calls × ~24 ops ≈ 2·10⁸ — too slow in Python.

Optimization: precompute pw[k] = p^k for k up to B_p (for the d' factors), and for the (e−d)·t factor note (e−d) ≤ e ≤ 9 and t ≤ N: precompute p^{k·t}? Alternatively precompute p^c for c ≤ 9 and use pow(p, (e−d)*t, MOD) only when the down-below-min transition occurs — but that's every d < e at each step, i.e., up to e·N ≈ 9000 pow calls per prime — fine! Because d < e ≤ 9 only for small d. The bulk transition (d ≥ e, up/stay) uses pw[d'] with d' ≤ B_p. Down-below-min only happens for d ∈ [0, e−1], at most e values per step → ≤ 9·1000 = 9000 pow calls per prime, each ~24 muls → trivial.

Actually also precompute pw up to B_p: B_p ≤ ~9000 for p=2, less for others; total Σ B_p ≈ 9000 — tiny.

Number of distinct primes: up to primes ≤ 1000 = 168, but only those dividing some A_i. DP per prime O(N·B_p). Total ≈ 9·10⁶ modular multiply-adds in pure Python — might be ~10–20 seconds. Hmm, borderline. Optimizations:
- Use list-based DP, local variables, avoid mod where possible (values < MOD² overflow? Python ints arbitrary precision but slow when big; must mod each op).
- For "stay" positions (p ∤ A_t): transition d→d with factor pw[d] — still O(B) per position. Can't skip easily since acc accumulates. Total stays = Σ_p (N − count_p) which is large: 168 primes × 1000 positions... but B_p = 0 for primes not dividing any A_i (skip entirely, W=1). For primes dividing few A_i, B_p small so O(N·B_p) small. Σ_p N·B_p = N·Σ B_p ≈ 1000·9000 = 9·10⁶. OK that's the same bound. Good.

But constant factor in Python: 9·10⁶ iterations each with a couple of modular multiplications and list indexing — roughly 5–15 s. Risky but likely OK with PyPy-style optimizations (this will run in CPython presumably). We can micro-optimize: for each prime, dp as list of ints length B+1; new dp zeros; loops. Use `mod = 998244353`; do `val = dp[d]`; accumulate.

Alternative micro-opt: note transitions:
- stay: ndp[d] += dp[d]·pw[d]
- up: ndp[d+e] += dp[d]·pw[d+e]
- down (d≥e): ndp[d−e] += dp[d]·pw[d−e]
- down (d<e): ndp[0] += dp[d]·pow(p,(e−d)·t,MOD)

We can vectorize with numpy? Modular arithmetic with int64: products of two mod-values < 2³⁰ each → product < 2⁶⁰ fits int64; sums of a few → OK with mod reduction. numpy could speed up 10–100×. But numpy may not be available; safer to write pure Python optimized. Let me estimate more carefully: Σ_p B_p ≤ Σ_i Ω(A_i) ≤ (N−1)·max Ω. A_i ≤ 1000: max Ω = 9 (512=2⁹). So Σ B_p ≤ 8991. Positions per prime: N. So total inner iterations ≈ Σ_p N·(B_p+1) ≈ 1000·9000 + (#primes)·1000 ≈ 9·10⁶ + small. Each iteration: up/stay/down updates. For choice steps, ~3 updates per d; for stays 1 update per d. Number of choice positions total = Σ_p count_p ≤ Σ_i ω(A_i) ≤ 999·4 ≈ 4000. So choice-step iterations ≈ Σ_p count_p·B_p ≤ ... bounded by B_p·count_p summed — worst case p=2: count ≈ up to 999 (all even A_i), B=8991 → 9·10⁶ iterations × 3 updates = 2.7·10⁷ updates. Hmm, that's more. Each update ~ a few ops → maybe 10⁸ ops in Python → too slow (≈100 s).

Need to reduce. Observation: for prime 2 with count c and budget B, DP is O(N·B) with B ≤ 9c. So O(9c·N). For c ≈ 999, that's 9·10⁶ states × ~2–3 transitions ≈ 2·10⁷ modular ops. In Python ~20–40 s. Too slow. Need numpy or smarter.

**Numpy approach.** Represent dp as int64 array length B+1. Each transition is index-shift + multiply by pw array + mod. Stay: ndp = dp·pw % mod (elementwise). Up: ndp[e:] += dp[:B+1−e]·pw[e:]... but careful: multiple contributions to same ndp — compute each contribution array and sum, then mod. All vectorized. Per step O(B) in C. Total: Σ_p (number of steps for p)·B_p ≈ same 9·10⁶ but in C → fast (<1 s). Memory fine.

But is numpy guaranteed? AtCoder (this looks like AtCoder) allows numpy in Python. The problem style (mod 998244353, constraints) is AtCoder. AtCoder's Python includes numpy. I'll write with numpy and a pure-Python fallback? To be safe, maybe implement pure Python but optimized enough... Let me reconsider complexity: actually can we shrink B? d = w − min ranges up to total up-steps minus... max d = max over walks of (w − min) ≤ B (total sum of e's). Tight. 

Alternatively pure Python with `array` of Python ints and list comprehensions? List comprehension with zip: `ndp = [(a*b) % mod for a,b in zip(dp, pw)]` — C-level loop but per-element Python ops; ~10⁷ such ops across all → maybe 5–10 s. Hmm.

Let me reconsider: total element-operations = Σ_p Σ_{steps} (B_p+1). For p=2: steps ≈ N = 1000, B ≈ 9·(count of even A_i). If all A_i even, B ≈ 9000 → 9·10⁶ element-ops per transition type. With numpy each is vectorized: 1000 steps × (few vector ops on 9000-array) = 1000 × ~5 × 9000 = 4.5·10⁷ C-ops → ~0.1–0.2 s. 

I'll go with numpy, using int64 and mod after each step (values: dp < mod, pw < mod, product < mod² < 2⁶⁰, sum of up to 3 such < 2⁶² — safe in int64). 

**Edge cases.** A_i = 1: no primes, no choice — edge contributes nothing. Fine. Primes with B_p = 0 skipped. N up to 1000.

**Double-check the "count t" in down-below-min with numpy:** for d in 0..e−1: contribution to ndp[0] += dp[d]·p^{(e−d)·t}. Small loop (e ≤ 9) per step — fine with pow().

Wait, also need to double check the up-step factor: acc' = acc + d' where d' = d+e, factor p^{d+e} = pw[d+e]. And down d≥e: factor pw[d−e]. Stay: pw[d]. Yes.

Also initial: t=0, dp[0]=1 (d=0, acc=0). Then process t=1..N−1 (edges 1..N−1). At the end sum(dp) % mod = W_p. Note position t=0 contributes acc 0. Total positions N: t=0..N−1. ✓. In the down-below-min case at step to position t, previous terms count = t (positions 0..t−1). ✓.

Hmm wait, one subtlety: at a choice edge, both up and down transitions from each d. At stay, only stay. At an edge where p appears with exponent e: up = numerator choice, down = denominator choice. ✓.

**Verify F formula once more.** h_i = exponent of p in a_i (unscaled). g's p-exponent = min_i h_i. Score p-exponent = Σ_i h_i − N·min_i h_i. h_i = D + w_{i−1} where w_{i−1} = signed prefix sum over edges 1..i−1 (+e if numerator, −e if denominator), D = Σ_{denominator edges} e. Σ_i h_i = N·D + Σ_{i=1}^{N} w_{i−1} = N·D + Σ_{t=0}^{N−1} w_t. min_i h_i = D + min_{t} w_t. F = Σ w_t − N min w_t. ✓ independent of D. 

**Now the answer = ∏_p W_p mod p_mod.** 

Let me sanity check sample 1 by hand partially? N=6, A = 1,9,2,2,9. Primes: 2 (edges 3,4 with e=1,1), 3 (edges 2,5 with e=2,2). Answer = W_2·W_3.

Compute W_2: positions t=0..5. Steps at t=3 (e=1) and t=4 (e=1); stays at t=1,2,5.
- t=0: dp={0:1}.
- t=1 stay: ndp[d]=dp[d]·2^d → {0:1}.
- t=2 stay: {0:1}.
- t=3 step e=1: from d=0: up → d'=1, factor 2^1=2; down (d<e): ndp[0] += 1·2^{(1−0)·3}=2³=8. So dp={0:8, 1:2}.
- t=4 step e=1: from d=0 (val 8): up → d'=1 factor 2: 16; down below: ndp[0] += 8·2^{1·4}=8·16=128. From d=1 (val 2): up → d'=2 factor 2²=4: 8; down d≥e → d'=0 factor 2⁰=1: 2. ndp: {0:128+2=130, 1:16, 2:8}.
- t=5 stay: ndp[d] = dp[d]·2^d: {0:130, 1:32, 2:8·4=32}. Sum = 130+32+32 = 194. W_2 = 194.

Compute W_3: steps at t=2 (e=2) and t=5 (e=2); stays t=1,3,4.
- t=0: {0:1}. t=1 stay: {0:1}.
- t=2 step e=2: from d=0: up → d'=2 factor 3²=9. down below: ndp[0] += 3^{2·2}=3⁴=81. dp={0:81, 2:9}.
- t=3 stay: {0:81, 2:9·9=81}.
- t=4 stay: {0:81, 2:81·9=729}.
- t=5 step e=2: from d=0 (81): up → d'=2, factor 9 → 729; down below: ndp[0] += 81·3^{2·5}=81·3^{10}=81·59049=4782969. From d=2 (729): up → d'=4 factor 3⁴=81 → 729·81=59049; down d≥e → d'=0 factor 3⁰=1 → 729. ndp: {0: 4782969+729=4783698, 2:729, 4:59049}. Sum = 4783698+729+59049 = 4843476. W_3 = 4843476.

Answer = 194 · 4843476 = 939634344? Compute: 4843476·194 = 4843476·200 − 4843476·6 = 968695200 − 29060856 = 939634344. ✓✓ Matches sample output exactly! Great, the approach is verified.

**Implementation plan.**
1. Read N, A.
2. Factor each A_i (primes ≤ 1000; precompute spf up to 1000).
3. For each prime p, collect list of (position t, exponent e) for edges t=1..N−1 where p | A_t.
4. For each prime with nonempty list, run DP:
   - B = sum of e's.
   - dp = numpy zeros int64 length B+1; dp[0]=1.
   - pw = p^k mod M for k=0..B (numpy array, computed via repeated multiply mod).
   - For t=1..N−1: if t in p's edges with exponent e: vectorized up/down transitions; else stay transition.
   - W_p = dp.sum() % M.
5. Answer = ∏ W_p % M.

For efficiency, per prime precompute edge dict; loop t from 1..N−1. Total inner vector ops fine.

Numpy details: use dtype=np.int64. Products < M² ≈ 10¹⁸ < 2⁶³ ≈ 9.2·10¹⁸. M = 998244353 ≈ 10⁹. M² ≈ 9.96·10¹⁷ < 9.2·10¹⁸ ✓. Sum of two such products could exceed 2⁶³? Up transition + down transition into same index: ndp[d'] gets at most one up and one down contribution (from different sources) plus... ndp[d'] = up_contrib (from d'−e) + down_contrib (from d'+e) + maybe stay? No, choice steps have no stay. So ndp = up_arr + down_arr, each < M² ≈ 10¹⁸, sum < 2·10¹⁸ < 9.2·10¹⁸ ✓. Then mod. For stay steps: single product. Safe.

But careful: dp values < M, pw < M, product < M² ≈ 9.965·10¹⁷. Two such summed: 1.99·10¹⁸ < 2⁶³−1 ≈ 9.22·10¹⁸ ✓.

Down-below-min: python loop d in range(min(e, current_max_d+1)): ndp[0] = (ndp[0] + int(dp[d])·pow(p, (e−d)*t, M)) % M.

Also track current max possible d to slice arrays (minor opt; can just use full arrays length B+1).

Potential issue: pw needs exponents up to B (for d' up to B). Compute via np: pw = pow(p, arange(B+1), M)? Vectorized: iterative multiply. Fine.

Pure Python fallback if numpy unavailable? I'll include a fallback pure-Python DP (same logic with lists) to be safe, choosing based on import success. Actually to keep code simple and robust, maybe write pure Python only but optimize: total ops estimate 2·10⁷ — too slow. I'll do numpy primary with fallback.

Let me also double-check sample 3 can't be verified by hand — trust.

**Complexity final:** fine.

**Indexing care:** edges t = 1..N−1 correspond to A_t (1-indexed) = A[t−1] (0-indexed array). Steps at position t use A_{t}. ✓.

Now write the code.

```python
import sys
def main():
    import numpy as np
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    A = list(map(int, data[1:1+N-1]))
    # spf up to 1000
    MAXA = 1000
    spf = list(range(MAXA+1))
    for i in range(2, int(MAXA**0.5)+1):
        if spf[i]==i:
            for j in range(i*i, MAXA+1, i):
                if spf[j]==j: spf[j]=i
    from collections import defaultdict
    prime_edges = defaultdict(list)  # p -> list of (t, e), t=1..N-1
    for t in range(1, N):
        x = A[t-1]
        while x > 1:
            p = spf[x]; e=0
            while x % p == 0:
                x//=p; e+=1
            prime_edges[p].append((t,e))
    ans = 1
    for p, edges in prime_edges.items():
        B = sum(e for _,e in edges)
        ed = dict(edges)
        pw = [1]*(B+1)
        for k in range(1, B+1): pw[k] = pw[k-1]*p % MOD
        pwa = np.array(pw, dtype=np.int64)
        dp = np.zeros(B+1, dtype=np.int64); dp[0]=1
        for t in range(1, N):
            e = ed.get(t)
            if e is None:
                dp = dp * pwa % MOD
            else:
                ndp = np.zeros(B+1, dtype=np.int64)
                # up: from d to d+e
                ndp[e:] = dp[:B+1-e] * pwa[e:] % MOD
                # down d>=e: from d to d-e
                ndp[:B+1-e] = (ndp[:B+1-e] + dp[e:] * pwa[:B+1-e]) % MOD
                # down d<e: to 0 with pow factor
                base = int(ndp[0])
                for d in range(0, e):
                    v = int(dp[d])
                    if v:
                        base = (base + v * pow(p, (e-d)*t, MOD)) % MOD
                ndp[0] = base
                dp = ndp
        ans = ans * (int(dp.sum()) % MOD) % MOD
    print(ans)
main()
```

Wait, in the up transition: ndp[e:] = dp[:B+1−e]·pwa[e:] — pwa index should be d' = d+e, and d ranges 0..B−e, so pwa[e..B] ✓. Down: ndp[d−e] += dp[d]·pwa[d−e], d from e..B → ndp[0..B−e] += dp[e..B]·pwa[0..B−e] ✓.

Overflow check in up: dp·pwa < M² ✓, assigned directly. Down sum: ndp existing (up contribution < M²... wait ndp[e:] was set to products < M² but not modded? I did `% MOD` on the up assignment. Then down: ndp[:B+1−e] + dp[e:]·pwa[:B+1−e]: first < M, product < M², sum < M + M² < 2⁶³ ✓ then mod. ✓.

But note up assignment `ndp[e:] = dp[:B+1-e] * pwa[e:] % MOD` — operator precedence: `*` and `%` same precedence, left-to-right: (dp·pwa) % MOD ✓.

One more check: dp entries always < MOD after each step ✓.

t in pow(p,(e−d)*t,MOD): t is the position index (1..N−1) — matches our DP where step to position t has t previous terms ✓ (verified against sample 1 computation which matched).

Also need to double check the stay step also applies at positions where edge has no p — yes loop over all t=1..N−1.

Edge case: prime edges dict per prime; primes dividing A_i only. ✓.

The result for sample 1 computed by hand matches; confident.

Fallback without numpy: I'll add a pure-Python path if import fails. Given AtCoder provides numpy, primary is fine, but include fallback for robustness. Pure Python version: same loops with lists; stay: `dp = [d*w % MOD for d,w in zip(dp,pw)]`; up/down with slices and zip. It'd be slower but correct.

Actually, let me just include both, selecting via try/except import.

Also small thing: `ndp[0]` base — after up/down assignments, ndp[0] may already have down contribution (from d=e). Then add d<e contributions. ✓ handled.

Memory/time: fine.

Write final solution with solve() and __main__ guard.

## worker: Implement the verified solution in Python: read N 
- **Reduction (verified against samples 1 and 2 by hand):** Each edge i needs S_i/S_{i+1} = p_i/q_i in lowest terms with p_i·q_i = A_i, i.e., for each prime power p^e ∥ A_i, independently assign it to numerator or denominator. Given all choices, the primitive (gcd-1) sequence is forced, so good sequences biject with per-edge, per-prime sign choices.
- For a fixed prime p, writing h_i = exponent of p in S_i, we get h_i = D + w_{i-1} where w is a walk starting at 0 with step +e (numerator) or −e (denominator) at each edge containing p, and D cancels in the score exponent: F = Σ_{t=0}^{N-1} w_t − N·min w_t. The total answer factorizes as ∏_p W_p with W_p = Σ_walks p^F.
- **DP per prime:** state d = w − min ≥ 0, value = Σ p^{Σ(w_s − min)}. Transitions at an edge with exponent e: up (d→d+e, ×p^{d+e}), down in-range (d→d−e, ×p^{d−e}), down below min (d<e: →0, ×p^{(e−d)·t} where t previous terms get shifted); stay (×p^d) at positions without p. Hand-computed W_2=194, W_3=4843476 for sample 1, product = 939634344 ✓; sample 2 gives 9+9=18 ✓.
- **Complexity:** Σ_p B_p = Σ_i Ω(A_i) ≤ 999·9 ≈ 9000, so total work ≈ N·9000 ≈ 9·10⁶ element-ops, vectorized with numpy int64 (products < MOD² < 2⁶⁰, sums of two < 2⁶³, safe). The below-min case only touches d < e ≤ 9 entries per step, using fast pow().
- Pure-Python fallback included in case numpy is unavailable (same logic, list-based).
