
## ideation
The conditions force the black region to be a "staircase" (Ferrers/Young diagram shape): each row has a black prefix, each column has a black prefix. This is equivalent to: black cells form a down-set (order ideal) in the product poset — if (r,c) is black, every (r',c') with r'<=r, c'<=c is black. Contrapositive: there must be NO pair consisting of a white cell W at (r1,c1) and a black cell B at (r2,c2) with r2>=r1 and c2>=c1 (distinct cells, but since colors differ they're automatically distinct). Proof sketch: such a pair violates either row r2's prefix property (white at c1<=c2 left of black) or column c2's prefix property. Conversely, if no such pair exists among all cells, one can define f(r)=max black column and show consistency; for the decision problem we only need the fixed cells to not already violate this.

So the task: given a set of B points and W points in an N×N grid (N up to 1e9, M up to 2e5), decide whether any W point is weakly dominated (southeast quadrant, inclusive) by some B point. If yes → "No", else "Yes".

Efficient check: sort all fixed cells by row ascending; sweep rows, maintaining the maximum column among black cells seen so far in rows <= current row. For a white cell at (r,c), if maxBlackCol among rows <= r is >= c → violation. But careful with same-row ordering: within the same row, a black cell at column >= c also violates. If we process row by row and first add all black cells of that row to the structure, then query white cells of that row, we include same-row blacks (correct, since r2>=r1 allows equality). Actually we must include same row blacks before querying whites of that row. Since condition is r2>=r1 AND c2>=c1, processing per row: update blacks of row r, then for each white in row r query max column >= c. Using a global running maximum of black columns for rows <= r suffices because we only need max column, and the condition c2>=c1 just compares with max. So: sort cells by row; iterate groups by row; for each group, first update mx = max(mx, black cols in group), then for each white in group check mx >= c → violation. Wait — but whites in earlier rows must also be checked against blacks in later rows? No: violation requires black row >= white row, so when sweeping top-down, a white at row r only conflicts with blacks at rows >= r. Sweeping from top, at row r we know blacks in rows <= r, not rows > r. So we should sweep from the BOTTOM up: maintain max black column over rows >= current row. For white at (r,c), conflict iff maxBlackCol(rows >= r) >= c. Within same row, include that row's blacks before querying. That works.

Alternative: sort by row descending, or sort ascending and process whites before blacks... simplest: sort by row descending; group by row; add blacks of the group to running max; then check whites of the group against running max. Since all rows >= r are processed before row r, and same-row blacks are added first, correct.

Edge cases: M can be 0? Constraints say M>=1, but handle anyway. N up to 1e9 irrelevant beyond input. Sample 3: single W at (1,1), no blacks → Yes. Sample 2: W(1,2), B(2,2): black row 2>=1, col 2>=2 → violation → No. Sample 1: W(3,2); blacks (4,1) col1<2 no; (1,3) row1<3 no → Yes.

Complexity O(M log M) from sorting; running max is O(1) per cell. No BIT needed since we only need max column (1D dominance after row sweep). Pitfall: same-row handling — must add blacks before querying whites within the same row group. Also multiple cells per row. Also note: could there be an issue where a white conflicts with a black in the same row but smaller column? No — needs c2>=c1.

Also double check the characterization "no W-B pair in SE relation iff extendable to staircase": Given fixed cells with no such pair, define for each row r: a(r) = max column of fixed black in row r (0 if none), b(r) = min column of fixed white in row r (N+1 if none). No-pair condition implies... we need a monotone non-increasing f with a(r) <= f(r) < b(r). The no-pair condition gives: for r1<=r2, not (black at r2 col >= white at r1 col), i.e., for r1<=r2, a(r2) < b(r1). Define f(r) = max over r'>=r of a(r'). Then f is non-increasing, f(r)>=a(r), and f(r) < b(r) since for all r'>=r, a(r')<b(r). So a valid staircase exists. Great, characterization confirmed.

## worker: Write the complete Python solution: parse stdin, g
- Characterization: row-prefix + column-prefix conditions ⇔ black region is a Ferrers/order-ideal shape ⇔ no fixed white cell (r1,c1) coexists with a fixed black cell (r2,c2) satisfying r2≥r1 and c2≥c1. Sufficiency proof: define f(r) = max black column among rows ≥ r (0 if none); the no-pair condition implies f(r) < (min white column in row r), and f is non-increasing, giving a valid completion.
- Algorithm: group fixed cells by row, sweep rows in descending order maintaining the running maximum black column over rows ≥ current row; add same-row blacks before querying whites (equality in row is allowed). A white cell with column ≤ that maximum is a violation → "No"; otherwise "Yes".
- Complexity: O(M log M) due to sorting rows (O(M) distinct-row sort), O(1) work per cell; memory O(M). N up to 1e9 is irrelevant since only fixed cells matter.
- Verified against samples mentally: sample 2 (W(1,2), B(2,2)) → violation → No; sample 3 (single W) → Yes; sample 1 → Yes.

## worker: Verify the solution against the four samples by re
Verification of the solution:

**Correctness (characterization).** Row-prefix + column-prefix conditions ⇔ black cells form an order ideal of the product poset ⇔ no fixed white cell (r1,c1) coexists with a fixed black cell (r2,c2) with r2≥r1 and c2≥c1.
- Necessity: such a pair violates row r2's prefix property (white at column c1 ≤ c2 left of black) — contradiction.
- Sufficiency: define f(r) = max black column among fixed blacks in rows ≥ r (0 if none). f is non-increasing, f(r) ≥ every black column in row r, and the no-pair condition gives f(r) < (min white column in row r) for every row with a fixed white. Coloring (r,c) black iff c ≤ f(r) is a valid staircase respecting all fixed cells.

**Algorithm.** Group cells by row; sweep rows in descending order maintaining `max_black` = max column of black cells in rows ≥ current row. Within a row, blacks are added before whites are queried, so same-row blacks (r2 = r1, allowed) are included. A white with column ≤ max_black is a violation → "No"; else "Yes".

**Sample verification by reasoning:**
- Sample 1: W(3,2); blacks (4,1),(1,3). Sweep: row 4 adds black col 1 (max=1); row 3: white col 2 > 1, OK; row 1 adds black col 3 (max=3), no whites. → Yes ✓
- Sample 2: row 2 adds black col 2 (max=2); row 1: white col 2 ≤ 2 → No ✓
- Sample 3: single W(1,1), no blacks, max_black=0 < 1 → Yes ✓
- Sample 4: contains W(1789,211) and B(1814,712): black row 1814 ≥ 1789, col 712 ≥ 211 → violation → No ✓ (sweep finds it since row 1814 processed before 1789).

**Edge cases:**
- M=0 (not possible per constraints but handled): no rows, loop skipped → Yes.
- N=1 with W: max_black=0 < 1 → Yes; with B: no whites → Yes.
- Same-row interactions: blacks added before whites within a group, so B(r,5) & W(r,3) → violation (correct); B(r,3) & W(r,5) → max_black=3 < 5, no violation (correct, since c2≥c1 fails).
- Same-column interactions: B below W in same column (r2>r1, c2=c1) → max_black ≥ c1 → violation (correct).
- Duplicate cells: guaranteed distinct by constraints; even if duplicated with same color, logic unaffected.

**Complexity:** O(M log M) time (sorting ≤ M distinct rows; O(1) work per cell), O(M) memory. N up to 1e9 is irrelevant since only fixed cells matter.
