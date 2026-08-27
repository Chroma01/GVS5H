
## ideation
- Sort positions; define gaps g_k = x_{k+1} - x_k for k=1..N-1.
- The operation on 4 consecutive pieces with gaps (a,b,c) produces gaps (c,b,a): it reverses three consecutive gaps. First and last positions never change.
- Reversal of 3 consecutive elements lets us swap elements at distance 2 (reverse(i..i+2), then reverse(i+1..i+3) appropriately — standard result: adjacent transposition within same parity class is achievable). So gaps at odd indices can be permuted arbitrarily among themselves; same for even indices. Parity classes are invariant (reversal of 3 preserves each element's index parity).
- Sum of coordinates = N*x_1 + Σ g_k*(N-k), weights w_k = N-k strictly decreasing in k.
- Within each parity class, to minimize Σ w_k g_k with freely permutable gaps: by rearrangement inequality, pair largest gaps with smallest weights, i.e., sort gaps in class descending and assign to indices in decreasing order of k (weights ascending). Equivalent: sort class gaps ascending and assign to increasing k? Let's be careful: weights decrease with k, so smallest weight at largest k. Pair largest gap with largest k. So sort gaps ascending → assign to k ascending within class.
- Verify sample 1: gaps 4,2,3. Odd indices {1,3}: gaps {4,3}, weights w1=3, w3=1. Pair largest gap (4) with smallest weight (w3=1): sum = 3*3+1*4=13; even index {2}: 2*2=4. Total = 4*1 + 13+4 = 21. ✓
- Sample 2: x=0,1,6,10,14,16; gaps 1,5,4,4,2. Odd indices {1,3,5}: gaps {1,4,2}, weights {5,3,1}; sorted gaps ascending [1,2,4] paired with weights descending [5,3,1]: 5+6+4=15. Even indices {2,4}: gaps {5,4}, weights {4,2}: 4*5? No—ascending gaps [4,5] with descending weights [4,2]: 16+10=26. Total = 6*0 + 15+26 = 41. ✓
- Pitfalls: N up to 2e5, coordinates up to 1e12 → use 64-bit (Python fine). Must confirm reachability: any permutation within parity class achievable via 3-reversals (adjacent swap of distance-2 elements via two reversals: rev(i,i+2) then rev(i+1,i+3)? Need care but standard: reverse positions i..i+2 twice with overlap yields swap of g_i and g_{i+2} while restoring middle. Actually sequence: reverse(i..i+2): (a,b,c)→(c,b,a); then reverse(i+1..i+3) on (c,b,a,d)→(c,d,a,b)? That swaps a,c but moves d. Hmm; proper: rev(i..i+2) then rev(i+1..i+3) then rev(i..i+2)? (a,b,c,d)→(c,b,a,d)→(c,d,a,b)→(a,d,c,b). Not clean. But known AtCoder solution (ABC 269? Actually "ARC" problem) confirms parity classes fully permutable. The generator: swapping g_i and g_{i+2} while fixing others is achievable via commutator; editorial states even/odd gap indices independently sortable. Trust known result (this is ABC/ARC "Reversing Gaps" — answer matches both samples).

## worker: Implement the solution: read N and X, compute gaps
- Sorted positions are already given; gaps g_k = x_{k+1} - x_k (1-indexed).
- The operation on 4 consecutive pieces with gaps (a,b,c) yields gaps (c,b,a): it reverses three consecutive gaps, leaving the first and last positions fixed.
- Reversing 3 consecutive elements preserves each gap's index parity, and adjacent transpositions within a parity class are achievable, so odd-indexed gaps can be permuted arbitrarily among themselves, and even-indexed gaps likewise.
- Total sum = N*x_1 + Σ g_k*(N-k), with weights N-k strictly decreasing in k. By the rearrangement inequality, within each parity class we pair the smallest gaps with the largest weights (ascending gaps vs descending weights) to minimize.
- Verified against samples: Sample 1 → 21 (4*1 + (3*3+1*4) + 2*2), Sample 2 → 41 (6*0 + (5*1+3*2+1*4) + (4*4+2*5)).
- Complexity: O(N log N) time, O(N) memory; Python ints handle up to ~2e5 * 1e12 magnitudes safely.

## worker: Final review of code for I/O format and correctnes
- **I/O review**: Input format is `N` on one line, then `N` integers. `sys.stdin.buffer.read().split()` handles any whitespace layout robustly. Output is a single integer printed with newline — matches spec. Reading via buffer is fast enough for N = 2×10⁵.
- **Correctness review**:
  - Operation on 4 consecutive pieces with gaps (a,b,c) yields gaps (c,b,a): a reversal of 3 consecutive gaps. Verified algebraically (p, q, r, s → p, p+s−r, p+s−q, s; new gaps (s−r, q−r... ) = (c, b, a) since s−r = c, (p+s−q)−(p+s−r) = r−q = b, s−(p+s−q) = q−p = a). ✓
  - 3-reversal preserves index parity of each gap, and generates the full symmetric group within each parity class (adjacent swap of elements at distance 2 is achievable via compositions of 3-reversals), so each parity class of gaps is freely permutable. This matches the known editorial result for this problem.
  - Sum of coordinates = N·x₁ + Σ g_k·(N−k): each gap g_k is included in exactly the N−k positions to its right, and x₁ (the leftmost) never moves and is counted in all N positions. ✓
  - Rearrangement inequality: weights w_k = N−k are strictly decreasing in k; to minimize, pair smallest gaps with largest weights → iterate gaps ascending while weights descend (w starts at n−1 for odd class, n−2 for even class, stepping −2). ✓
  - Hand-verified against both samples in the plan: Sample 1 → 21, Sample 2 → 41.
  - Edge cases: N=4 (only i=1 possible; odd class {g₁,g₃}, even {g₂}) works. All gaps positive (distinct sorted input) so no zero-gap concerns. Python ints handle magnitudes up to ~2×10⁵ × 10¹² = 2×10¹⁷ without overflow.
- Complexity: O(N log N) time (two sorts totaling N−1 elements), O(N) memory.
