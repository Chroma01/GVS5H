
## ideation
- Core difficulty: n up to 100 and k up to 10^15 means we cannot enumerate permutations; we must do a "k-th permutation" style construction where at each position we try candidate values in increasing order and count how many valid completions follow each candidate, subtracting from k as we go.
- Key structural insight: the constraint is purely about parity adjacency (no two odds or two evens adjacent). Once the parity of the first element is fixed, the entire parity pattern is forced (must strictly alternate). So a valid permutation corresponds to: (a) choosing a starting parity, (b) assigning actual odd numbers to odd slots and even numbers to even slots.
- Feasibility: alternating parities over length n requires the counts of odd/even numbers to differ by at most 1. For numbers 1..n: odds = ceil(n/2), evens = floor(n/2). This always satisfies |odds - evens| ≤ 1, so valid permutations always exist for n ≥ 1. For even n, both starting parities work; for odd n, must start with odd (since odds = evens + 1).
- Counting completions: given we have `o` odd numbers and `e` even numbers remaining, and the parity of the last placed element (or "none" at start), the number of completions is:
  - If the parity pattern of remaining slots is forced: count = o! * e! if the pattern is feasible (slot counts match remaining counts), else 0.
  - At the very first position (no previous parity), both parities may be possible; but when we fix a candidate first value, its parity fixes everything, so the count formula still applies per-candidate.
- So the per-candidate count function: after placing a candidate of parity p, remaining counts (o, e) and next required parity is opposite of p. The remaining sequence must alternate. Number of ways = o! * e! if feasible else 0. Feasibility check: the number of remaining slots of each parity is determined; must equal o and e respectively.
- Simpler formulation: with remaining counts (o, e) and "next parity must be q": if q is odd, we need o == e or o == e + 1... precisely: starting with parity q and alternating over (o+e) slots uses ceil/floor counts. If q odd: odd slots = ceil((o+e)/2), even slots = floor((o+e)/2); need o == odd slots and e == even slots. Similarly for q even. Then count = o! * e!.
- Total count for boundary check: sum over valid starting parities of (odds! * evens!). For odd n: odds! * evens!. For even n: 2 * odds! * evens!. If k > total, return [].
- Pitfalls:
  - k is 1-indexed per examples (k=6 gives the 6th). Must decrement carefully.
  - Factorials up to 100! are huge (~10^158) but Python handles big ints natively; still, capping at k (or k+something) keeps arithmetic fast and avoids any concern. Since k ≤ 10^15, capping factorials/counts at, say, 10^18 is safe and efficient.
  - Precompute factorials once (0..100) with capping.
  - At each position, iterate over remaining candidate numbers in ascending order (lexicographic order), compute completions if that candidate is placed, and skip blocks until k falls inside one.
  - Lexicographic order over permutations of integers compares element-wise numerically; since values are 1..n, ascending candidate order is correct.
  - Edge cases: n=1 → only [1], total=1. n=2 → 2 permutations. Odd n forces first element odd — the counting handles this automatically (even-start count = 0).
- Complexity: O(n^2) candidate evaluations with O(1) count lookups after factorial precomputation — trivially fast.

## worker: Implement the complete solution: capped factorial 
- **Counting model**: Once the parity of the first element is chosen, the parity pattern of the whole permutation is forced (strict alternation). Given `o` remaining odd numbers, `e` remaining even numbers, and a required next parity, feasibility holds iff the forced slot counts match `(o, e)`; then the number of completions is `o! * e!` (assign any remaining odds to odd slots, evens to even slots).
- **Capping**: All counts are capped at `10^18 > 10^15 ≥ k`, so comparisons against `k` stay exact while arithmetic stays cheap (also fine uncapped since 100! is a native Python big int, but capping is cleaner).
- **Early exit**: Total valid permutations = sum over feasible starting parities of `odds! * evens!` (capped). For odd `n` only odd starts are feasible; for even `n` both are. If `k > total`, return `[]`.
- **Main loop**: At each position, iterate remaining values in ascending numeric order (lexicographic order), skip candidates whose parity equals the previous element's parity, compute the block size of completions for each candidate, subtract blocks while `k > block`, and pick the candidate whose block contains the `k`-th permutation. `k` is treated as 1-indexed, matching the examples.
- **Verification against examples**:
  - `n=4, k=6`: totals = `2*(2!*2!)=8 ≥ 6`. Construction picks 3 (blocks: 1→4, 2→4, cumulative 8 ≥ 6 after subtracting 4... walking: val 1 block 4, k=6>4 → k=2; val 2 block 4, k=2 ≤ 4? parity of 2 is even, block = 2!*1!... recompute: after placing 2, o=2,e=1, next odd, slots=3, odd slots 2, even 1 → 2!*1!=2, k=2 ≤ 2 → pick 2? But expected answer starts with 3.) — careful re-trace: candidates in order 1,2,3,4. val=1 (odd): o=1,e=2, next even, total slots 3, even slots 2, odd 1 → feasible, count = 1!*2! = 2. k=6 > 2 → k=4. val=2 (even): o=2,e=1, count = 2!*1! = 2. k=4 > 2 → k=2. val=3 (odd): count 2, k=2 ≤ 2 → pick 3. Next: prev odd, candidates 2,4 (evens). val=2: o=1,e=1, next odd → count 1!*1!=1, k=2 > 1 → k=1. val=4: count 1, k=1 ≤ 1 → pick 4. Then prev even, candidates 1,2: val=1 (odd): o=0,e=1, next even → count 1 → pick 1. Then 2. Result `[3,4,1,2]` ✓.
  - `n=3, k=2`: total = 2!*1! = 2. val=1: o=1,e=1,next even → 1!*1!=1, k=2>1 → k=1. val=2 (even): o=2,e=0, next odd, slots 2, odd slots 1 ≠ 2 → 0, skip. val=3: count 1, k=1 ≤ 1 → pick 3; then 2, then 1 → `[3,2,1]` ✓.
  - `n=2, k=3`: total = 2*(1!*1!) = 2 < 3 → `[]` ✓.
  - `n=1, k=1` → `[1]`; `n=1, k=2` → `[]`. Large `n=100, k=10^15`: total = 2*(50!*50!) ≫ cap, loop runs O(n²)=10⁴ iterations with O(1) lookups — instant.
- Complexity: O(n) factorial precomputation, O(n²) candidate scans, O(1) count per candidate.
