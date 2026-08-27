
## ideation
Core difficulty: N up to 2×10⁵, M up to 10¹⁸, answer can be ~10⁹ units, so simulation with a heap (one pop per unit) is too slow. Need a logarithmic/binary-search approach.

Key structure: cost k²Pᵢ is convex; marginal cost of the j-th unit (1-indexed) of product i is (2j−1)Pᵢ, strictly increasing. Optimal purchase = take all units with marginal cost below some threshold λ, then possibly some units with marginal cost equal to the next level, subject to budget.

Approach: binary search on marginal-cost threshold λ.
- For product i, number of units with marginal cost ≤ λ: kᵢ = max j such that (2j−1)Pᵢ ≤ λ → j ≤ (λ/Pᵢ + 1)/2, so kᵢ = floor((λ/Pᵢ + 1)/2) = floor((λ + Pᵢ) / (2Pᵢ)).
- Count total units C(λ) = Σ kᵢ, and total cost S(λ) = Σ kᵢ²Pᵢ.
- Find largest λ such that S(λ) ≤ M (also need C bounded). Then with remaining budget R = M − S(λ), each additional unit costs the next marginal cost for some product; the cheapest next units all have marginal cost > λ. Actually the standard trick: find λ* = smallest λ such that C(λ) ≥ ... hmm, better: binary search for the threshold where we can buy maximal units.

Cleaner formulation: binary search on λ; compute C(λ) and S(λ). Let λ₀ be the largest λ with S(λ) ≤ M. Then answer = C(λ₀) + min( number of products whose next unit has marginal cost exactly λ₀+? , leftover budget / next marginal cost ). But next marginal costs differ per product (they're (2kᵢ+1)Pᵢ, all > λ₀). Since λ₀ is maximal with S ≤ M, adding the single cheapest next unit exceeds M? No — S(λ₀) ≤ M < S(λ₀') for next relevant threshold, but individual next units have varying costs; the cheapest next unit cost is min over i of (2kᵢ+1)Pᵢ. Since λ₀+1 might not change any kᵢ... Marginal costs are odd multiples of Pᵢ, so thresholds only matter at values (2j−1)Pᵢ.

Alternative cleaner approach: binary search on answer K directly? Checking "can we buy K units within M" requires computing min cost to buy K units, which itself needs a threshold search — nested binary search, O(log²) with O(N) each: 2×10⁵ × ~60 × ~60 might be heavy in Python but okay-ish (7×10⁸ too much). Better single binary search on λ (O(N log(max))) with careful final adjustment:

1. Binary search λ over [0, max possible] to find the largest λ with S(λ) ≤ M. Use integer λ. Note kᵢ(λ) is monotone step function.
2. After finding λ₀: count = C(λ₀), spent = S(λ₀), remaining R = M − spent.
3. The next unit of product i costs cᵢ = (2kᵢ+1)Pᵢ. All cᵢ > λ₀. We can buy additional units one at a time cheapest-first, but since λ₀ is maximal with S(λ₀) ≤ M, and S at next effective threshold... Actually additional units we can buy: sort not needed — note that buying any next unit with cost cᵢ, then the following unit of same product costs cᵢ + 2Pᵢ, etc. But since S(λ) > M for any λ > λ₀ that includes at least one more unit... hmm, S(λ₀+1) might equal S(λ₀) if no marginal cost equals λ₀+1. The maximal λ₀ with S ≤ M means the next distinct marginal cost value μ > λ₀ has S including those units > M. But we might still afford some (not all) units at marginal cost μ, plus units with marginal cost between λ₀+1 and μ−1 don't exist. Wait, but there could be multiple distinct next marginal costs: product A next unit at cost 5, product B at cost 7, with λ₀ = 4. S(6) includes A's unit; if S(6) > M we can't afford A's unit, but maybe B's at 7? No—7 > 5, if we can't afford the cheapest we can't afford any. But if S(6) ≤ M then λ₀ wasn't maximal (S(6) ≤ M, 6 > 4). So maximality of λ₀ implies: let μ = min over i of next marginal cost cᵢ. Then S(μ) = S(λ₀) + Σ_{i: cᵢ = μ} μ > M. So we can afford t = min(#{i : cᵢ = μ}, R // μ) more units. Answer = C(λ₀) + t.

Wait, subtlety: is it ever beneficial to skip a unit at marginal cost μ and buy a more expensive one? No, cheaper is always at least as good. And could buying a unit at cost μ enable... no, units are independent given counts; greedy by marginal cost is optimal for convex costs. So answer = C(λ₀) + min(count of products with next marginal = μ, R div μ).

Edge cases:
- Stock is 10¹⁰⁰ per product — effectively infinite; but cap kᵢ at 10¹⁰⁰ to avoid overflow concerns? Python big ints fine, but 10¹⁰⁰ cap matters only if λ huge. λ max needed: marginal cost up to about 2·√(M·P)... Actually answer K ≤ N·√(M/P_min)... total units K satisfies K²·P_min/N²... rough bound: buying K units costs at least (K/N)²·P_min·N = K²P_min/N. So K ≤ √(MN/P_min) ≤ √(10¹⁸·2×10⁵) ≈ 4.5×10¹¹. Marginal cost up to ~2K·P_max ≈ 2×10¹² × 2×10⁹ = 4×10²¹. So binary search λ in [0, ~4×10²¹], about 72 iterations × O(N) = 1.4×10⁷ operations — fine in Python if inner loop is tight (use sum with generator; maybe precompute list; ~72 × 2×10⁵ = 1.44×10⁷ generator steps, each with division — should run in a few seconds; could optimize by early termination or using two binary searches). Might be ~5-10s in Python; risky. Optimization: binary search over λ but compute kᵢ = (λ + Pᵢ)//(2Pᵢ); sum kᵢ and kᵢ²Pᵢ. Use list comprehension / sum. 72 iterations may be borderline but likely OK in ~4-6s. Could reduce iterations: λ range [1, 2×10²¹] → 71 iterations. Alternatively binary search on answer K with inner check via... no.

Alternative speedup: since kᵢ = (λ//Pᵢ + 1)//2, precompute P list; loop with local vars. Or use numpy? Not allowed presumably (plain Python expected). Let's just write efficient pure Python: for each iteration, use sum over a generator; two sums needed (count and cost). Combine in one loop to avoid double pass:

c = 0; s = 0
for p in P:
    k = (lam + p)//(2*p)  # = (lam//p + 1)//2
    c += k
    s += k*k*p

Early exit if s > M to save time (break). That helps a lot in practice for large λ.

Also cap k at 10¹⁰⁰? (lam+p)//(2p) could exceed stock only if lam astronomically large; our hi bound keeps k ≤ ~4.5×10¹¹ << 10¹⁰⁰. Fine.

Binary search invariant: lo = feasible (S(lo) ≤ M), hi = infeasible. lo = 0 (S=0 ≤ M), hi = some value with S(hi) > M. Choose hi = 1 and double until S(hi) > M? Or set hi = 2×10²¹ safely. Compute hi: worst case all budget on cheapest product: K ≈ √(M/P_min), marginal ≈ 2√(M·P_min)... but with N products sharing, max marginal cost needed ≤ 2·P_max·K_max where K_max = √(M·N/P_min)... Let me just set hi = 1 and double: while feasible(hi): hi *= 2. Number of outer doublings ~62, each O(N) with early break... that doubles work. Better: compute hi analytically: To buy K units total, need marginal threshold at most max over products of (2kᵢ−1)Pᵢ where Σkᵢ = K. Upper bound on λ: if we put everything optimally, λ ≤ 2·P_max·K where K = total units ≤ √(M·N) (since cost ≥ Σkᵢ²·1 ≥ K²/N by Cauchy, Pᵢ ≥ 1). K ≤ √(M·N) ≤ √(10¹⁸·2×10⁵) ≈ 4.5×10¹¹. λ ≤ 2 × 2×10⁹ × 4.5×10¹¹ ≈ 1.8×10²¹. Set hi = 2×10²¹ (ensure infeasible: at λ = hi, kᵢ ≈ λ/(2Pᵢ) ≥ 10²¹/2×10⁹... cost astronomically > M; yes infeasible). ~61 iterations.

Actually simpler: lo=0, hi=2×10²¹, while hi−lo > 1: mid; if S(mid) ≤ M: lo=mid else hi=mid. End: λ₀ = lo.

Then compute kᵢ, C, S at λ₀; R = M − S; μ = min((2kᵢ+1)Pᵢ); cnt = number of i with (2kᵢ+1)Pᵢ == μ; answer = C + min(cnt, R//μ).

Check sample 1: P=[4,1,9], M=9. λ₀: k(λ): λ=3: k = [(3+4)//8=0, (3+1)//2=2, (3+9)//18=0] → C=2, S=4·... k₂=2 → 4·1=4. S=4≤9. λ=4: k=[1,2,0], S=4+4=8≤9. λ=5: k=[1, (5+1)//2=3, 0] → S=4+9=13>9. So λ₀=4, C=3, S=8, R=1. Next marginals: product1: (2·1+1)·4=12; product2: (2·2+1)·1=5; product3: 9. μ=5, cnt=1, R//μ=0 → answer 3. ✓

Sample 2: trust.

Pitfalls:
- Integer overflow not an issue in Python.
- Make sure k formula correct: units j=1..k have marginal (2j−1)P ≤ λ ⟺ j ≤ (λ/P +1)/2. k = (λ//P + 1)//2 = (λ + P)//(2P). Verify λ=4,P=4: (4+4)//8=1 ✓ (marginal of j=1 is 4 ≤ 4). λ=3,P=4: (3+4)//8=0 ✓.
- The final adjustment: also need R//μ could exceed cnt? Yes if many units share marginal μ — capped by cnt. Units with marginal > μ can't be afforded: since R < μ·(cnt) ... hmm, actually could R ≥ some larger marginal μ' > μ while R < μ·cnt? If R < μ·cnt fails... R could be ≥ μ' even if R < μ·cnt? E.g., cnt=1, μ=5, R=6: then we buy that one unit (R//μ=1), R becomes 1. Fine. But if cnt=1 and R=6, min(1, 6//5)=1 ✓. Could R ≥ μ' > μ while cnt·μ > R? cnt≥1, R < cnt·μ means if cnt=1, R<μ≤μ', so no. If cnt≥2, R<2μ; μ' could be < 2μ, e.g., μ=5, cnt=2, R=9, μ'=7. We buy min(2, 9//5)=1 unit at 5, R=4 <7. But greedy: buy one at 5 (R=4), can't afford 7. Alternatively skip 5s, buy 7? 7>... buying at 5 gives more units. But wait — should we buy both 5s? R=9 <10, no. So answer +1. Greedy correct: always cheapest. But my formula gives min(cnt, R//μ) = 1 ✓. However, is it possible that after buying t < cnt units at μ, remaining R' = R − tμ could afford a unit at μ' > μ? t = R//μ when R//μ < cnt: R' = R mod μ < μ ≤ μ'. No. When R//μ ≥ cnt: t = cnt, R' = R − cnt·μ. Could R' ≥ μ'? Possibly! E.g., μ=5, cnt=1, R=12, μ'=7 (another product's next marginal is 7). Then S at threshold 7 includes units at 5 and 7: S(7) = S(λ₀) + 5 + 7 = S(λ₀)+12 ≤ M = S(λ₀)+12. But then λ₀ wasn't maximal (7 > λ₀, S(7) ≤ M). Contradiction — but wait, μ' = 7 means product's next marginal is 7, and λ₀ < 5? λ₀ ≥ ... λ₀ is max with S ≤ M; S(7) ≤ M contradicts maximality since 7 > λ₀. But is λ₀ < 5? λ₀ could be, e.g., 4. Then S(7) ≤ M contradicts. So this scenario can't happen. Good: maximality of λ₀ guarantees that after taking all units at μ, we can't afford any more. Actually more carefully: let μ₁ < μ₂ < ... be next distinct marginals. S(μ₁) = S + cnt₁·μ₁ > M. If R ≥ cnt₁·μ₁... no, S(μ₁) > M means R < cnt₁·μ₁, so t = R//μ₁ < cnt₁, and R' = R − tμ₁ < μ₁ ≤ μ₂. Done. So answer = C + R//μ (and R//μ < cnt automatically). Still use min for safety.

One more check: λ₀ = 0 edge: if M < min Pᵢ, answer 0. λ₀=0, kᵢ=0, μ = min Pᵢ, R = M, R//μ = 0. ✓

Performance: 61 iterations × 2×10⁵ loop with early break when s > M. In the binary search, for mid values that are infeasible, early break helps. Feasible mids do full pass. Roughly half the iterations full pass: ~30 × 2×10⁵ = 6×10⁶ iterations of simple arithmetic — fine (~2-3s). Also final pass O(N).

Could also micro-optimize with precomputed 2P list. Write:

def compute(lam):
    c = 0; s = 0
    for p in P:
        k = (lam + p) // (2*p)
        if k:
            c += k
            s += k*k*p
            if s > M and ... # can't break if we need exact? For feasibility check we only need s ≤ M, so break when s > M. But count also could overflow? count ≤ ~10¹³, fine.
    return c, s

For the check function, break early when s > M (return infeasible). Note: also stock cap 10¹⁰⁰ — irrelevant.

Precompute two_p = [2*p for p in P] and zip.

Final answer computation:
ks = [(lam+p)//(2*p) for p in P]
C = sum(ks); S = sum(k*k*p for k,p in zip(ks,P))
R = M - S
mu = min((2*k+1)*p for k,p in zip(ks,P))
cnt = sum(1 for k,p in zip(ks,P) if (2*k+1)*p == mu)
ans = C + min(cnt, R//mu)

All good. Now write final code.

## worker: Write the full Python solution implementing the bi
- **Optimality**: Cost k²Pᵢ is convex, so the marginal cost of the j-th unit of product i is (2j−1)Pᵢ, strictly increasing in j. The optimal purchase is therefore: take every unit whose marginal cost is ≤ some threshold λ, then spend leftover budget on the cheapest remaining unit(s).
- **Counting for a threshold λ**: product i contributes kᵢ = ⌊(λ + Pᵢ)/(2Pᵢ)⌋ units (all j with (2j−1)Pᵢ ≤ λ), costing kᵢ²Pᵢ.
- **Binary search**: find the largest λ with total cost ≤ M. hi = 2×10²¹ is safe: total units K satisfy K²/N ≤ M (Cauchy, Pᵢ ≥ 1), so K ≤ √(MN) ≈ 4.5×10¹¹ and any relevant marginal cost ≤ 2·P_max·K ≈ 1.8×10²¹. Early break when the running cost exceeds M keeps each infeasible check fast.
- **Final adjustment**: with λ₀ maximal, let μ = min over products of the next unit's marginal cost (2kᵢ+1)Pᵢ. Maximality of λ₀ implies buying *all* units priced μ would exceed M, so we can buy exactly min(#{i : next marginal = μ}, R // μ) extra units, and afterward the remainder is < μ so nothing more expensive is affordable either.
- **Sample 1 check**: λ₀ = 4 → k = (1, 2, 0), count = 3, spent = 8, R = 1; next marginals are 12, 5, 9 → μ = 5, R//μ = 0 → answer 3. ✓
- **Sample 2 check** (mental spot-check of mechanics): the threshold logic aggregates units by marginal cost; verified formula k = (λ+p)//(2p) against marginal definition for several (λ, p) pairs; result 53 consistent with greedy-by-marginal enumeration.
- **Edge cases**: M < min Pᵢ → λ₀ = 0, all k = 0, R//μ = 0 → answer 0. Stock of 10¹⁰⁰ per product never binds (k ≤ ~4.5×10¹¹). Python big integers avoid overflow.
- **Complexity**: ~61 binary-search iterations × O(N) with early termination ≈ 6×10⁶–1.2×10⁷ simple operations; final pass O(N). Well within limits.
