
## ideation
**Core task.** Minimize the maximum run length of equal characters using ≤ numOps flips. Classic pattern: the predicate "achievable with max-run ≤ k" is monotone in k (larger k is easier), so we can binary search or just linearly scan k = 1..n and return the smallest feasible k. n ≤ 1000, so even an O(n²) scan is trivially fast.

**Feasibility cost for a given k.**
- **k ≥ 2:** Runs are independent. For a maximal run of identical chars of length L, the minimum number of flips to break it into pieces of length ≤ k is `L // (k + 1)`: place a flipped character after every k originals; each flipped char becomes an isolated block of length 1 (its neighbors inside the run are the opposite char), and 1 ≤ k so it never violates the bound, and it can't merge with the adjacent different-character run because it's strictly interior. Hence `cost(k) = sum over runs of (L // (k+1))`, and feasible iff `cost(k) ≤ numOps`.
- **k = 1 (special case!):** The per-run formula `L // 2` is *wrong*. Counterexample: `s = "0110"`, runs (1,2,1) → formula gives 1, but flipping one '1' yields `"0010"` which has a run of length 2. The true requirement for k = 1 is that the whole string alternates, so cost = `min(#mismatches vs "0101...", #mismatches vs "1010...")` = for "0110" that's 2. So handle k = 1 separately with the alternating-pattern cost.

**Why k=1 differs:** for k ≥ 2 a flipped character (block of length 1) is always acceptable and self-contained; for k = 1 the flip's *neighbors* also become constrained, coupling adjacent runs — a global alternating constraint, not a per-run one.

**Monotonicity caution.** Mixing two different cost formulas (alternating for k=1, run-splitting for k≥2) means monotonicity of the computed cost array should be sanity-checked before binary searching. Safest: linear scan k = 1, 2, 3, … and return the first feasible k (O(n²) worst case ≈ 10⁶ ops, fine). Or binary search only over k ≥ 2 and test k = 1 separately first.

**Edge cases / pitfalls.**
- n = 1 → answer 1 always (0 flips needed).
- numOps = 0 → answer is just the existing longest run.
- All-same string, e.g. "0000" with numOps=2 → k=1 alternating cost = min(2,2)=2 ≤ 2 → answer 1 (matches Example 2).
- Example 1: "000001", numOps=1. k=1: vs "010101" mismatches = idx1,idx3 → 2; vs "101010": idx0,idx2,idx4,idx5 → 4; cost 2 > 1. k=2: runs (5,1) → 5//3 + 1//3 = 1 ≤ 1 → answer 2. ✓
- Example 3: "0101", numOps=0 → k=1 cost 0 → answer 1. ✓
- Answer is never 0; lower bound 1, upper bound n (cost(n)=0 always feasible), so the loop always terminates.
- Careful with run extraction (use itertools.groupby or a manual scan) and with off-by-one in `L // (k+1)`.

## worker: Write the complete `Solution.minLength` implementa
- Implemented `runs` via `itertools.groupby`.
- k = 1 handled specially: the entire string must alternate, so cost is `min(mismatches vs "0101...", mismatches vs "1010...")`. Per-run formula `L//2` would be wrong here (e.g. "0110").
- For k ≥ 2: each maximal run of length L needs `L // (k+1)` flips — insert a flipped char after every k originals. Each inserted char is an isolated block of length 1 ≤ k, strictly interior to the run, so runs are independent and the sum is exactly the minimum cost. This cost is non-increasing in k, so the first feasible k found by the linear scan is the answer.
- Linear scan k = 1..n with early break on exceeding numOps: worst case O(n·#runs) ≤ 10⁶ for n = 1000, plenty fast.
- Termination: k = n always gives cost 0 (every run length ≤ n < n+1), so a value is always returned; answer ≥ 1 always.
- Manual verification of all listed cases:
  - "000001",1 → k=1 cost min(2,4)=2>1; k=2: 5//3+1//3=1 ≤1 → **2** ✓
  - "0000",2 → k=1 cost min(2,2)=2 ≤2 → **1** ✓
  - "0101",0 → k=1 cost 0 → **1** ✓
  - "0110",1 → k=1 cost min(2,2)=2>1; k=2: 1//3+2//3+1//3=0 → **2** ✓
  - "0000",0 → k=1:2>0; k=2:4//3=1>0; k=3:4//4=1>0; k=4:4//5=0 → **4** ✓
  - "1",0 → k=1 cost min(1,0)=0 → **1** ✓
  - "01",1 → k=1 cost 0 → **1** ✓
