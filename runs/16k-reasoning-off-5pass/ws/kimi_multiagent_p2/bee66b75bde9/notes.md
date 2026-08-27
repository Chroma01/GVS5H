
## ideation
The core difficulty is recognizing that the row/column prefix conditions are equivalent to the black cells forming a Young diagram (Ferrers shape) anchored at the top-left. This shape is fully described by a monotone boundary path. Each pre-colored cell imposes a constraint that the path must lie on a specific side of that cell. With N up to 1e9, we cannot simulate the grid; we must work only with the M constraint points. The main pitfall is handling the strictness of inequalities correctly (a white cell at (x,y) forbids black at (x,y), but the boundary can pass adjacent to it) and managing large coordinate compression.

## worker: Formalize the boundary representation: define f(y)
- Modeled the black region as a Ferrers/Young diagram anchored at the top-left: row condition says each row's black cells form a left prefix; column condition says each column's black cells form a top prefix. Together these are equivalent to: there exists a nonincreasing integer function f(y) = number of black cells in column y, with 0 <= f(y) <= N.
- Constraint derivation:
  - Black cell (x, y): cell is black ⟺ x <= f(y), so f(y) >= x.
  - White cell (x, y): cell is white ⟺ x > f(y), so f(y) <= x - 1.
- Per column, take the max of lower bounds and min of upper bounds; immediate contradiction if lo > hi.
- Feasibility of a nonincreasing sequence with bounds at sparse columns: greedy left-to-right, keeping the largest feasible value `cur = min(cur, hi[y])`; fail if `cur < lo[y]`. Choosing the largest value is always safe since we can decrease freely later (columns between constrained ones are unconstrained, and N is huge but irrelevant — we only process M points, O(M log M) total).
- Verified against samples: sample 2 gives column 2 with lo=2 (from B at (2,2)) and hi=0 (from W at (1,2)) → contradiction → No. Sample 3: W at (1,1) → f(1) <= 0, feasible → Yes.
