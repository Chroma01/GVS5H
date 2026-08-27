
## ideation
The plan is essentially correct, but let me stress-test the key claim and edge cases.

**Core difficulty:** The decision problem "can we make all runs ≤ L with ≤ numOps flips?" needs a correct, provably minimal flip count per candidate L.

**Verifying the per-run formula for L ≥ 2:** For a maximal run of length `len`, flipping k positions splits the run into at most k+1 pieces. We need every piece ≤ L, so we need k ≥ ceil(len/(L+1))... wait, let me recompute. With k flipped positions inside the run, the run is divided into k+1 segments of identical characters (assuming flips are spaced apart and not adjacent). To have all segments ≤ L, we need len ≤ k·(stuff)... Actually: k flipped positions create k+1 gaps; total length len = sum of gap sizes + k (the flipped chars themselves). If flips are isolated (no two adjacent), each gap ≤ L requires len - k ≤ (k+1)·L, i.e., len ≤ k(L+1) + L, i.e., k ≥ (len - L)/(L+1), so k = ceil((len-L)/(L+1)) = floor(len/(L+1)). Yes — floor(len/(L+1)) is correct. E.g., len=5, L=2: floor(5/3)=1 flip → "00 1 00", pieces 2,2. ✓. len=6, L=2: floor(6/3)=2 → "00 1 00 1 0"? pieces 2,2,1 ✓ (can't do with 1 flip since max covered = 1·3+2=5 < 6 ✓).

**Pitfall 1 — flipped characters merging with neighbors:** When we flip a character inside a run of '0's, it becomes '1'. If adjacent to a neighboring run of '1's (length up to L), could the flipped '1' merge with it and create a run of L+1? For L ≥ 2, we have freedom in *which* positions to flip within the run, so we can always choose positions avoiding boundary-adjacent conflicts... but need care: if len is small (e.g., len = L+1, exactly one flip needed), the flip must be interior (not at the run's edge) to avoid merging — flipping position at distance ≥1 from both boundaries works when len ≥ 3, i.e., L+1 ≥ 3, i.e., L ≥ 2. That's exactly why L ≥ 2 is safe and L = 1 needs separate handling. Good — the plan's case split is justified.

**Pitfall 2 — L = 1:** String must be perfectly alternating. Only two target patterns (starting with '0' or '1'); answer is min mismatches. Flips here can't be analyzed per-run because flipping a boundary char affects both sides. Handled separately. ✓

**Pitfall 3 — monotonicity:** Feasibility is monotone in L (if achievable with longest run ≤ L, also achievable for L+1 with same or fewer flips). Binary search valid. ✓

**Pitfall 4 — edge cases:** numOps = 0 → answer is the existing longest run (binary search handles naturally). n = 1 → answer 1. numOps ≥ n could make L=1 always feasible. Search range lo=1, hi=n.

**Complexity:** O(n log n) — trivially fine for n ≤ 1000. Could also do O(n) via direct reasoning but unnecessary.

## worker: Implement the full solution: `flipsNeeded(L)` help
- **Decision problem:** For candidate max run length `L`, compute the minimum flips required; feasible iff `<= numOps`. Feasibility is monotone in `L`, so binary search works.
- **L >= 2:** For a maximal run of length `run`, flipping `k` isolated positions splits it into `k+1` pieces; all pieces `<= L` requires `run <= k*(L+1) + L`, i.e. `k >= (run - L)/(L+1)`, so minimal `k = floor(run/(L+1))`. Since `L >= 2`, any run needing flips has length `>= L+1 >= 3`, so flips can always be placed at interior positions (distance >= 1 from both run edges), meaning flipped characters never merge with adjacent runs — runs are independent and the sum is globally optimal.
- **L == 1:** The string must be perfectly alternating; only two target patterns exist. Mismatches to the two patterns sum to `n`, so compute one and take `min(mism_a, n - mism_a)`.
- **Verification:**
  - `s="000001", numOps=1`: L=2 needs `6//3=2` flips for the run of six 0s... wait, run lengths are 5 zeros + 1 one: `5//3=1`, `1//3=0` → 1 flip <= 1, feasible. L=1 needs min mismatches to alternating = 3 > 1. Answer 2. ✓
  - `s="0000", numOps=2`: L=1 → min mismatches = 2 <= 2 feasible. Answer 1. ✓
  - `s="0101", numOps=0`: L=1 → 0 mismatches <= 0. Answer 1. ✓
  - `n=1` (e.g. `"0"`, any numOps): L=1 needs 0 flips → answer 1. ✓
  - `numOps=0`: binary search returns the existing longest run. ✓
  - `numOps=n`: L=1 always feasible (worst case needs `floor(n/2)` flips <= n). ✓
  - `s="010", numOps=1`: already alternating, L=1 needs 0 flips → answer 1. ✓
- **Complexity:** O(n log n) time, O(1) extra space; n <= 1000, trivially fast.
