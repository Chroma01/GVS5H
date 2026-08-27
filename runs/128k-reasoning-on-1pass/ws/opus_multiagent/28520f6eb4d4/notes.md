
## ideation
**Restating / verifying the reduction (the plan is correct):**

- P = (0,h), building i = vertical segment {X_i}×[0,H_i], all X_i ≥ 1 > 0, so every building is to the right of the observer.
- Segment from P to (X_i, y) has height at x=X_j (X_j<X_i): `h + (y−h)·X_j/X_i`, which is **increasing in y** (coefficient X_j/X_i>0). Hence aiming at the **top** (y=H_i) maximizes clearance over *all* blockers simultaneously ⇒ building i is visible ⟺ for every j<i: `h + (H_i−h)X_j/X_i > H_j`.
- Multiplying by X_i>0 and using X_i−X_j>0: `h > (H_j·X_i − H_i·X_j)/(X_i − X_j)` = y-intercept at x=0 of the line through (X_j,H_j),(X_i,H_i). Note the expression is symmetric in the pair, so answer A = max over **all unordered pairs** of that intercept.
- Strictness: touching the top of a blocker counts as intersecting ⇒ at h = A the maximizing building is invisible (lower aim points are strictly worse too), and for h > A everything is visible. So the answer is exactly A when A ≥ 0, else −1. N=1 ⇒ no pairs ⇒ −1.
- Sanity checks: S1 pairs give {−1, −0.25, **1.5**} ✓; S2 gives −98 ⇒ −1 ✓; S3 collinear through origin ⇒ 0 ✓; S4 pair (10,10),(17,5) ⇒ 120/7 = 17.142857142857142… ✓ (note here the optimal pair is **not** on the global upper hull — (17,5) is dominated by (20,100),(27,270) on its right — so the "prefix/suffix hull" structure is essential).

**Reducing O(N²) pairs to O(N):**

Two symmetric formulations; either is fine:
1. **Left-to-right, upper hull of the prefix.** intercept(j,i) = H_i − X_i·slope(j,i), X_i>0 ⇒ for fixed i maximize intercept = **minimize slope(j,i) over j<i**. That min is attained at a vertex of the upper convex hull of {1..i−1} (supporting line through i with everything below). Key implementation fact: in Andrew's monotone-chain upper hull, when inserting point i and popping while `cross(hull[-2],hull[-1],i) ≥ 0`, the surviving `hull[-1]` **is** the tangent (min-slope) point. Total O(N) amortized. (Verified on A=(0,0),B=(1,10),C=(2,0),i=(3,0): pops C, tangent = B, min slope −5 ✓.)
2. Right-to-left, lower hull of the suffix, minimize slope(j,i) over i>j, intercept = H_j − X_j·slope. Same cost.

I lean to (1) because "tangent = stack top after the standard pop loop" avoids any separate binary-search/tangent code.

**Numerics / exactness:**
- Compute num = H_j·X_i − X_j·H_i (exact Python int, |num| ≤ 2e18) and den = X_i − X_j (>0, ≤ 1e9), then value = num/den as a float (correctly rounded, rel. err ~1e-16 ≪ 1e-9).
- Sign is exact: num is an exact int, den>0, so a negative candidate never rounds to ≥0, and |num/den| ≥ 1e-9 when num≠0. So `-1` vs `A≥0` decision is safe with plain floats; no need to carry fractions, though comparing (num,den) by cross-multiplication is also cheap in Python if desired.
- Hull cross products must use integers (values up to ~1e18·1e9 = 1e27 — Python big ints fine, no overflow worry).

**Pitfalls to remember:**
- Print exactly `-1` (not `-1.000000`) in the −1 case.
- A can be as large as ~1e18 (e.g. den=1): choose a print format that keeps enough significant digits, e.g. `f"{A:.12f}"` (never `%.6g`).
- A = 0 is a legitimate answer (sample 3) — don't collapse it into the −1 branch (`A < 0` ⇒ −1, `A ≥ 0` ⇒ print A).
- Collinear points: popping with `≥ 0` (removing collinear middles) is safe since collinear pairs give identical intercepts.
- Don't forget to still evaluate the candidate for every i ≥ 2 (including when the pop loop empties the hull down to one element — then j = hull[0]).
- Fast input (`sys.stdin.buffer.read().split()`), simple loop, avoid recursion; N = 2e5 so pure Python loop with big ints is OK but keep the inner loop lean.
- X strictly increasing per constraints ⇒ no equal-x degeneracies; still, don't rely on sorting input.

## worker: *Implement the full solution (formulation 1, left-
Implemented formulation 1 exactly as planned.

- **Reduction:** building *i* is visible from (0,h) iff for all j<i the segment to its top clears building j, i.e. `h > (H_j·X_i − X_j·H_i)/(X_i − X_j)` = y‑intercept at x=0 of the line through (X_j,H_j),(X_i,H_i). Answer A = max over all pairs; A ≥ 0 ⇒ print A, else −1 (N=1 ⇒ −1).
- **O(N) pair reduction:** intercept(j,i) = H_i − X_i·slope(j,i) with X_i > 0, so for fixed i we need the **minimum slope** to a left point, which is the upper tangent from i to the upper convex hull of the prefix. In monotone-chain construction, after popping while `cross(hull[-2],hull[-1],i) ≥ 0`, the surviving top of the stack *is* that tangent point (verified on the (0,0),(1,10),(2,0),(3,0) example: tangent = (1,10), min slope −5). Amortized O(N).
- **Exactness:** hull cross products and the candidate `(num, den)` are pure Python ints; candidates are compared by cross‑multiplication (`num*bd > bn*den`, both denominators positive), so both the maximizing pair and the sign test `bn < 0` are exact — no floating point can flip the −1 vs 0 decision (sample 3's A = 0 is preserved). Only the final `bn/bd` is a correctly rounded float division (rel. error ~1e‑16 ≪ 1e‑9).
- **Formatting:** `-1` printed as bare `-1`; otherwise `%.12f`, which keeps all integer digits for values up to ~1e18 (relative accuracy is what matters and floats give ~16 significant digits).
- Uses parallel coordinate stacks (`hx`,`hy`) instead of index lookups to keep the inner loop lean; input read in one shot. N = 2·10⁵ runs comfortably.

Hand checks: S1 → 1.5; S2 → −1 (best intercept −98); S3 → 0.0; S4 → 120/7 = 17.142857142857 (pair (10,10),(17,5), correctly found because (17,5) is on the prefix hull when i is processed).
