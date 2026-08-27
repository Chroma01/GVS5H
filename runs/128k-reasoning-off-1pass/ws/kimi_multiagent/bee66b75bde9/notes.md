
## ideation
The black region must be a top-left-anchored Ferrers (Young diagram) shape: row x has a[x] black cells (0..N), with a[1] >= a[2] >= ... >= a[N]. Cell (x,y) is black iff y <= a[x].

Key observations:
- A given black cell (x,y) forces a[x] >= y.
- A given white cell (x,y) forces a[x] <= y-1.
- So per row: L[x] = max y over black cells in row x (0 if none), U[x] = min(y-1) over white cells in row x (N if none). Need L[x] <= U[x] per row, plus existence of a non-increasing sequence a with L[x] <= a[x] <= U[x].

Existence of non-increasing sequence with per-position bounds: scan rows top to bottom, maintaining the feasible interval for a[x]. Since a[x] <= a[x-1], the feasible set for a[x] is [L[x], min(U[x], prev_max)] where prev_max is the max feasible value so far. Actually the standard greedy: keep `hi` = min(U[1..x]) so far (since a[x] <= a[x-1] <= ... <= a[1], we need a[x] <= min of all U up to x... wait, a[x] <= a[x-1], and a[x-1] <= U[x-1], so a[x] <= min(U[1..x])). Also a[x] >= L[x]. But also we need future rows to be satisfiable — since future rows only need a[x+1] <= a[x] and a[x+1] >= L[x+1], choosing a[x] as large as possible is never worse... but a[x] is also bounded below by L[x] only. However, there's a subtlety: a[x] must be >= a[x+1] >= L[x+1], so a[x] >= max(L[x..N])? No — a[x] >= a[x+1] >= L[x+1], and inductively a[x] >= max(L[x], L[x+1], ..., L[N]). So the condition is: for every x, max(L[x..N]) <= min(U[1..x]). That's a clean suffix-max vs prefix-min check.

Alternative equivalent view: conflict iff exists black (x1,y1) and white (x2,y2) with x2 <= x1 and y2 <= y1. This can be checked by sorting, but the row-bound formulation is simpler and directly constructive.

Pitfalls:
- N up to 1e9, so cannot allocate arrays of size N; only rows with given cells matter. Rows without constraints are flexible (L=0, U=N), and they never create infeasibility on their own — but they sit between constrained rows, so the suffix-max/prefix-min condition must be evaluated only at constrained rows? Careful: the condition max(L[x..N]) <= min(U[1..x]) must hold for ALL x, but L of unconstrained rows is 0 and U is N, so they don't affect suffix max or prefix min. However the check at an unconstrained position x uses suffix max over rows >= x which includes constrained rows below — but that same check is also performed at the position of the constrained row itself. Actually the tightest constraints occur exactly at constrained rows: for a white cell at row x2 and black cell at row x1 with x1 >= x2, the check at x2 catches it (suffix max from x2 includes row x1's L, prefix min up to x2 includes row x2's U). So checking only at rows that have white cells (prefix min changes) suffices; equivalently, just check: for every white cell (x2,y2) and black cell (x1,y1) with x1 >= x2: y1 <= y2 - 1, i.e., y1 < y2. So: no black cell weakly below a white cell in the same column-or-left... precisely: no pair with x1 >= x2 and y1 >= y2. 

Simplest robust implementation: collect per-row L and U only for constrained rows, sort rows, and verify the condition max suffix L <= min prefix U at each constrained row boundary. Or even simpler: compute for each row its L (black max) and U (white min-1); then check that for every pair of constrained rows r1 >= r2: L[r1] <= U[r2]. This is: max L over rows >= r2 must be <= U[r2] for all r2. Compute suffix max of L over sorted constrained rows, then check suffix_max_L[r] <= U[r] for each constrained row r (only rows with white cells matter, but checking all is fine). Also need L[r] <= U[r] within a row, which is included since suffix max at r includes L[r].

Edge cases: M can be 0? Constraints say M >= 1, but handle anyway (answer Yes). N=1 cases. Duplicate cells are guaranteed absent.

Algorithm:
1. Parse input, build dict row -> [maxBlackY (init 0), minWhiteY (init N+1)].
2. For each constrained row, L = maxBlackY, U = minWhiteY - 1.
3. Sort constrained row indices descending, compute suffix max of L.
4. For each constrained row r (in any order with suffix max available): if suffixMaxL(r) > U[r], output No.
5. Else Yes.

Complexity O(M log M).

## worker: Write the final Python solution: read N, M and the
- The black region must be a top-left Ferrers shape: row x has a[x] black cells with a[1] >= a[2] >= ... >= a[N]; cell (x,y) black iff y <= a[x].
- Black cell (x,y) forces a[x] >= y; white cell (x,y) forces a[x] <= y-1. Per row: L[x] = max black y (0 default), U[x] = min white y - 1 (N default).
- A non-increasing sequence a with L[x] <= a[x] <= U[x] exists iff for every x, max(L[x..N]) <= min(U[1..x]). Unconstrained rows (L=0, U=N) never tighten either side, so it suffices to check at constrained rows: scanning bottom-to-top, maintain suffixMaxL = max L over rows >= current; require suffixMaxL <= U[r] for each constrained row r (this also covers the within-row case L[r] <= U[r] since suffixMaxL includes L[r]).
- Equivalent to: no black cell (x1,y1) and white cell (x2,y2) with x1 >= x2 and y1 >= y2.
- Sample checks:
  - Sample 1: rows {4:[1,N+1], 3:[0,2], 1:[3,N+1]}. Bottom-up: r=4 suffix=1, U=4 ok; r=3 suffix=1, U=1 ok; r=1 suffix=3, U=4 ok → Yes.
  - Sample 2: rows {1:[0,2], 2:[2,N+1]}. r=2 suffix=2, U=2 ok; r=1 suffix=2, U=1 → No.
  - Sample 3: row 1: L=0, U=0, suffix=0 ≤ 0 → Yes.
  - Sample 4: e.g., white at (1700,1083) gives U=1082, while black at (1814,712) and (1789,211) are below; also white (1789,211) U=210 with black (1814,712) below → suffix max at row 1789 includes L=712 > 210 → No. Correct.
- Complexity O(M log M), memory O(M); N up to 1e9 handled since only constrained rows are stored.
