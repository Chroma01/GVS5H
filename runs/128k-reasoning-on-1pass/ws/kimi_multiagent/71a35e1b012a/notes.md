
## ideation
Core difficulty: this is not just interval covering. Each operation offers a choice between two complementary sets: middle interval `[L,R]` (op1) or the two end segments outside it (op2). Since writes only set `0 -> 1`, order is irrelevant; we need the minimum number of chosen/oriented operations whose union is `[1,N]`, plus reconstruction.

Important correction to the stated plan: “if achievable then ≤2” is false. Counterexample: `N=10`, intervals `[4,7]`, `[1,6]`, `[5,10]`. Choose op1 for the first and op2 for the last two: chosen sets are `[4,7]`, `[7,10]`, `[1,4]`, whose union is all positions, but no pair covers everything. So 3 can be necessary.

Better model: put positions on a circle by adding the adjacency `N-1`. Then both choices become circular arcs: op1 is arc `L..R`, op2 is the complementary arc `R+1 .. L-1` wrapping through `N,1`. The “uncovered/forbidden” set of a chosen operation is also a circular arc. By the Helly property for circular arcs, if any oriented family has empty forbidden intersection, then some subfamily of at most 3 already has empty forbidden intersection. Equivalently: if the goal is achievable, it is achievable with cost at most 3. Thus the decision reduces to testing existence of cost 1, 2, or 3; if none exist, answer is -1.

Cost 1: some interval is `[1,N]` and used as op1. Op2 can never cover everything for a nonempty interval.

Cost 2 cases remain valid: two op1 intervals chain from `1` to `N`; two op2 intervals have disjoint holes; or one interval contains another, using outer as op1 and inner as op2. Need distinct indices.

Cost 3 can be attacked either by circular-arc endpoint alternation, or by enumerating orientation patterns in line terms:
- three op1 intervals chain across `[1,N]`;
- one op2 with hole `[L,R]` plus two op1 intervals whose union covers that hole;
- two op2 whose holes overlap, with the overlap contained in a third op1 interval;
- three op2 cannot help beyond cost 2 because pairwise overlapping line intervals have a common point.

Pitfalls: do not use the same operation twice or both orientations of it; handle `N=1` and full/empty complements; coverage is discrete so “touching” means `R+1 >= next_L`; avoid `O(NM)` and aim for sorting/sweep/segment-tree `O(M log M)`; reconstruction must store indices, not just boolean feasibility.

## worker: Implement the complete O(M log M) solution in Pyth
- Operations only change zeros to ones, so their order is irrelevant; only the union of the chosen sets matters.
- Cost 1 is possible exactly when some interval is `[1, N]`, using Operation 1.
- All possible cost-2 configurations are checked:
  - Operation 1 + Operation 1: intervals must chain from position `1` to `N`.
  - Operation 2 + Operation 2: their intervals must be disjoint.
  - Operation 1 + Operation 2: the Operation-2 interval must be contained in the Operation-1 interval.
- If no cost-2 solution exists and `M >= 3`, no two intervals are disjoint. Thus `[max L_i, min R_i]` is nonempty and contained in every interval. Operation 2 on the two extreme intervals leaves exactly this segment uncovered, and Operation 1 on any third interval covers it.
- Therefore the answer is always at most 3 when `M >= 3`.
- Complexity: `O(M log M)` time from sorting, `O(M)` memory.

## worker: Stress test the solution against a brute-force sol
- Finalized the interval-set solution: order is irrelevant because operations only turn `0` into `1`; only the union of chosen sets matters.
- Cost 1 is exactly an interval `[1, N]` used as Operation 1.
- Cost 2 is fully characterized by three distinct-index cases:
  - op1+op1: intervals chain from `1` to `N` with discrete touching `R >= next_L - 1`;
  - op2+op2: the two intervals/holes are disjoint, detected by `min R < max L`;
  - op1+op2: the op2 interval is contained in the op1 interval, found by a sorted sweep.
- If none of those exist and `M >= 3`, then all intervals pairwise intersect and none contains another. Thus `I = [max L, min R]` is nonempty and contained in every interval. Operation 2 on the max-`L` and min-`R` intervals leaves only `I` uncovered, and Operation 1 on any third interval covers `I`, giving cost 3.
- Stress-checking approach used for validation: brute force all `3^M` assignments for small `N <= 8`, `M <= 6`, compare minimum cost, verify every `-1`, and simulate emitted operations. Targeted checks included duplicates/equal intervals, touching chains, `N=1`, `M=1/2` infeasible cases, all samples, and a true cost-3 witness such as `N >= 7` with `[2,5], [3,6], [4,7]`. Note: the triple `[3,6], [5,8], [4,10]` is nested and is actually cost 2 via op1 on `[4,10]` plus op2 on `[5,8]`.
- Complexity: `O(M log M)` time from sorting, `O(M)` memory.
