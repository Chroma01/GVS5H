
## ideation
The core insight is already identified in the plan: for index i, we need the max divisor d of A_i such that at least K elements are divisible by d. Key considerations:

1. **Core difficulty**: N up to 1.2×10⁶ and A_i up to 10⁶. A per-element divisor enumeration is O(N·√M) ≈ 1.2×10⁹ — too slow. Need the sieve-based approach.

2. **Algorithm**:
   - Build freq array `f[v]` = count of elements equal to v (size M+1, M = max(A)).
   - `cnt[d] = sum of f[m]` over multiples m of d. Cost: Σ M/d = O(M log M) ≈ 10⁶ · ~14 ≈ 1.4×10⁷ operations. Fine in Python if written with tight loops (slicing can help: `sum(f[d::d])` is C-speed and very fast).
   - `best[d]` propagation: for each d with cnt[d] >= K, mark all multiples m of d: `best[m] = max(best[m], d)`. That's another O(M log M). Alternatively, compute `ans[x]` for each distinct value x: largest d | x with cnt[d] >= K. Doing it by iterating d and assigning to multiples: `for d in range(M,0,-1): if cnt[d]>=K: for m in range(d, M+1, d): if best[m] < d: best[m] = d` — but since we iterate d descending, the first time we set best[m] it's already the max, so we can skip if set. Actually simpler: iterate d ascending and always overwrite — then best[m] ends up being the largest qualifying d. That's O(M log M) writes ≈ 1.4×10⁷ — okay but Python loop-heavy. Better: iterate d descending, only fill unset entries; worst case still O(M log M).
   - Then answer for each i is `best[A_i]`.

3. **Pitfalls**:
   - Python speed: 1.4×10⁷ inner-loop iterations for cnt plus ~1.4×10⁷ for best propagation. Using `sum(f[d::d])` with list slicing is much faster than explicit loops for cnt. For best, explicit loop needed, but we can restrict to d where cnt[d] >= K, which may prune heavily; worst case (all elements equal, K=1) still ~M log M ≈ 1.4×10⁷ assignments — acceptable (~2-4 s). Could also use array slicing tricks: `best[d::d] = [d]*len(best[d::d])` only valid when ascending overwrite is fine — yes! Iterating d ascending and overwriting via slice assignment gives each multiple the largest d last. Slice assignment is C-speed. Total work O(M log M) but fast.
   - Wait: ascending overwrite — for a fixed m, divisors d of m that qualify are visited in increasing order, so final value is the largest qualifying divisor. Correct.
   - Memory: lists of size 10⁶+1 ints — fine (~8 MB each with array module or ~36 MB as list of ints; use `array('i')` or plain lists carefully). Plain Python lists of ints: small ints cached, but values up to 10⁶ create distinct objects... Actually list stores references; ints > 256 are separate objects. freq list with counts — each entry an int object. 3 lists × 10⁶ × ~36 bytes ≈ 100 MB — risky. Use `array('i', ...)` or `list` of int but values are reused? No. Better: use `array` module or numpy if allowed. Safest: `array('i', [0]) * (M+1)` — 4 bytes per entry, 4 MB per array. But slice assignment on array works too. However `sum(f[d::d])` on array creates a new array — sum works. Speed of array slicing is decent. Alternatively use lists but be mindful; typical AtCoder (this looks like AtCoder ABC/ARC style) memory limit is 256 MB, three Python lists of 10⁶ ints ≈ 3 × (8 MB list + int objects). Int objects: freq values up to N (distinct objects per entry) — ~28 bytes each → 28 MB per list plus 8 MB list overhead ≈ 36 MB; three lists ≈ 108 MB. Probably OK but array is safer.
   - Edge cases: K=1 → answer is A_i itself (cnt[A_i] >= 1 always). K=N → answer is GCD of whole array if it divides A_i... actually largest d | A_i with all elements divisible by d = gcd of all elements. Handled naturally.
   - Note d must divide A_i; best[m] as defined gives exactly that.

4. **Implementation sketch**:
   - Read input, M = max(A).
   - `f = [0]*(M+1)`; count.
   - cnt: `cnt = [0]*(M+1)`; `for d in range(1, M+1): cnt[d] = sum(f[d::d])` — slicing a list of ints: f[d::d] creates sublist; total elements summed = M log M ≈ 1.4×10⁷, C-speed. Should run ~1-2 s.
   - Optimization: only compute cnt[d] for d that divide at least one element? Not needed.
   - best: `best = [0]*(M+1)`; `for d in range(1, M+1): if cnt[d] >= K: best[d::d] = [d]*len(best[d::d])`. Ascending overwrite ensures max. Creating `[d]*len(...)` each time allocates M/d ints — total 1.4×10⁷ int references, C-speed. Fine.
   - Output: `'\n'.join(str(best[a]) for a in A)`.
   - Micro-opt: skip d where cnt[d] < K (the check is cheap).

5. **Verification with sample 1**: A=[3,4,6,7,12], K=2. cnt[3]=2 (3,6,12→ actually 3 elements: 3,6,12 → cnt[3]=3), cnt[4]=2 (4,12), cnt[6]=2 (6,12), cnt[12]=1. best[3]: divisors of 3 with cnt>=2: 1,3 → 3 ✓. best[4]: 1,2,4 → cnt[2]=3 (4,6,12)>=2, cnt[4]=2 → 4 ✓. best[6]: 1,2,3,6 → 6 ✓. best[7]: 1 → 1 ✓. best[12]: divisors 1,2,3,4,6,12; cnt[12]=1 <2; largest with cnt>=2 is 6 ✓.

## worker: Implement the complete solution: write solve() wit
- **Correctness**: For index i, any chosen set of K elements including A_i has gcd g, which must divide A_i, and all K chosen elements are multiples of g, so cnt[g] >= K. Conversely, if d | A_i and cnt[d] >= K, we can pick A_i plus any K-1 other multiples of d, giving a gcd that is a multiple of d — so the maximum achievable gcd equals the largest divisor d of A_i with cnt[d] >= K, which is exactly `best[A_i]`.
- **cnt computation**: `sum(f[d::d])` sums frequencies over multiples of d at C speed; total work Σ M/d = O(M log M) ≈ 1.4×10⁷ for M=10⁶.
- **best computation**: iterating d ascending and slice-assigning `d` to all multiples of d means each position x gets overwritten by every qualifying divisor of x in increasing order, so the final value is the largest qualifying divisor. Slice assignment is C-speed. Only d with cnt[d] >= K do work, which prunes heavily in practice.
- **Edge cases**: K=1 → cnt[A_i] >= 1 always, and A_i itself qualifies, so best[A_i] = A_i. K=N → only divisors of the global gcd qualify, answer = gcd of all elements (which divides every A_i). N=1=K → answer = A_1. All handled naturally.
- **Sample 1 check**: cnt[2]=3, cnt[3]=3, cnt[4]=2, cnt[6]=2, cnt[12]=1. best[3]=3, best[4]=4, best[6]=6, best[7]=1, best[12]=6 — matches expected output.
- **Memory**: three lists of size ~10⁶+1. Values stored are Python ints; worst case ~100 MB total which fits typical 256 MB limits. Runtime is dominated by the two O(M log M) C-speed slice loops (~1-3 s).
