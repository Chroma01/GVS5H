
## ideation
- Core problem: maximum matching where a smaller mochi `a` can sit on `b` iff `2*a <= b`. Each mochi used at most once, so K ≤ N//2.
- Key structural fact (standard exchange argument): if K pairs are achievable, then it's achievable using the K smallest mochi as tops and the K largest as bottoms, paired in order (smallest top with smallest of those bottoms). So the feasibility check for a given K reduces to: `A[i] * 2 <= A[N-K+i]` for all `0 <= i < K`.
- Candidate approaches:
  1. Binary search on K in [0, N//2] with the O(K) check above → O(N log N), simple and safe.
  2. Single greedy two-pointer pass: iterate tops over the first half (indices 0..N/2-1), bottoms pointer starting at N//2 (or more precisely at the position that maximizes matches), advancing the bottom pointer whenever a match fails. This yields O(N). Care needed: starting the bottom pointer at N//2 is correct because tops can only come from the smaller half in an optimal solution; any top beyond index N//2-1 can't be matched since there wouldn't be enough larger mochi remaining. Actually the cleanest O(N): tops i from 0..N//2-1, bottoms j from N//2..N-1, greedily match — this is the well-known correct greedy for this AtCoder problem (ABC 088 D-like / typical "Kagamimochi" max-pairing).
- Pitfalls:
  - Overflow isn't an issue in Python, but in other languages `2*a` needs care.
  - Off-by-one: K can be at most N//2; check loop bounds.
  - Don't confuse with the "count distinct sizes" version (ABC 085 B); this is the pairing version.
  - Input size up to 5×10^5 — use fast input reading (sys.stdin.buffer).
  - For the two-pointer version, ensure the bottom pointer starts at N//2 (not at some binary-searched position) — correctness relies on the fact that in an optimal matching, tops are among the smallest half and bottoms among the largest half; greedy matching smallest available top to smallest feasible bottom is optimal.

## worker: Write the complete Python solution: fast stdin rea
- Greedy two-pointer: tops are taken from the first half (indices `0..half-1`), bottoms pointer `j` starts at `half`.
- For each top `a[i]`, advance `j` until `2*a[i] <= a[j]`; if found, match them (count++, j++), else stop since no bottom remains.
- Correctness: in any optimal solution with K pairs, the tops can be taken as the K smallest mochi and bottoms as K mochi from the larger half (exchange argument). Matching the smallest available top to the smallest feasible bottom is optimal (standard greedy exchange). Tops beyond index `half-1` can never be used since there wouldn't be enough larger mochi.
- Complexity: O(N) time, O(N) memory for the array. Fast input via `sys.stdin.buffer.read`.
- Verified against samples mentally: sample1 `2 3 4 4 7 10`: tops 2,3,4; j starts at index 3 (value 4): 2→4, 3→7, 4→10 ⇒ 3. Sample2: half=1, top 387, bottoms 388,389: 774>389 ⇒ 0. Sample3 gives 6.

## worker: Validate the solution on samples (expected 3, 0, 6
Validation of the greedy two-pointer solution (tops from indices `0..half-1`, bottom pointer `j` starting at `half`, advancing until `2*a[i] <= a[j]`):

**Sample verification (traced by hand):**
- Sample 1: `N=6, A=[2,3,4,4,7,10]`, half=3, j starts at index 3 (value 4).
  - i=0 (2): 2*2=4 ≤ 4 → match, count=1, j=4
  - i=1 (3): 3*2=6 > 4 → j=5 (7); 6 ≤ 7 → match, count=2, j=6... wait, j=5 is value 7, match → count=2, j=6? No: j=5 → match → j=6? j was 4, value 7 at index 4. Let me redo: indices 3,4,5 = values 4,7,10.
  - i=0 (2): 4 ≤ a[3]=4 → match, count=1, j=4
  - i=1 (3): 6 > a[4]=7? No, 6 ≤ 7 → match, count=2, j=5
  - i=2 (4): 8 > a[5]=10? No, 8 ≤ 10 → match, count=3, j=6
  - Output: **3** ✓
- Sample 2: `N=3, A=[387,388,389]`, half=1, j=1.
  - i=0 (387): 774 > 388 → j=2; 774 > 389 → j=3 = n → break.
  - Output: **0** ✓
- Sample 3: `N=24`, half=12, tops = first 12 values `[307,321,330,339,349,392,422,430,477,481,488,537]`, bottoms from index 12: `[541,571,575,602,614,660,669,678,712,723,785,792]`.
  - 307→614 (541 too small: 614≥614 ✓; 541<614 skip, 571<614 skip, 575<614 skip, 602<614 skip → 614) count=1
  - 321→660 (642 needed; 660≥642) count=2
  - 330→669 (660 needed; 669≥660) count=3
  - 339→678 (678≥678) count=4
  - 349→712 (698 needed; 712≥698) count=5
  - 392→785 (784 needed; 785≥784) count=6
  - 422→ needs 844; 792 < 844 → j reaches n → break.
  - Output: **6** ✓

**Edge cases:**
- N=2, match: `A=[1,2]` → half=1, i=0: 2 ≤ a[1]=2 → count=1 ✓
- N=2, no match: `A=[1,1]` → 2 > 1 → j=2=n → break → 0 ✓
- All equal: `A=[5,5,5,5]` → 10 > 5 always → 0 ✓
- Doubling sequence: `A=[1,2,4,8]` → half=2, j=2: 1→4 (2*1=2 ≤ a[2]=4; note a[2]=4 is first checked... j starts at 2: 2 ≤ 4 → match), 2→8 (4 ≤ 8) → count=2 = N//2 ✓
- Odd N: `A=[1,2,4,8,16]` → half=2, j=2: 1→4, 2→8 → count=2 = N//2 ✓ (middle element a[2]=4 correctly used as a bottom)
- Odd N where middle should be unused: `A=[1,3,4,7,10]` → half=2, j=2: 1→4 (2≤4), 3→7 (6≤7) → 2 ✓

**Correctness argument:** If K pairs are achievable, an exchange argument shows the K smallest mochi can serve as tops and K mochi from the upper half as bottoms, paired in sorted order. Greedy matching of the smallest remaining top to the smallest feasible bottom never does worse (standard exchange: if top t matches bottom b' while a smaller feasible bottom b < b' exists, swapping preserves feasibility). Since tops beyond index half-1 can never be matched (fewer larger mochi remain than tops used), restricting tops to the first half is without loss. The pointer j only moves forward, so the scan is linear.

**Performance:** O(N) time, O(N) memory. N = 5×10^5 integers parse instantly via `sys.stdin.buffer.read().split()`; the loop is a single pass with at most N pointer advances — runs in well under 0.5s in CPython. No recursion, no overflow concerns (Python ints).
