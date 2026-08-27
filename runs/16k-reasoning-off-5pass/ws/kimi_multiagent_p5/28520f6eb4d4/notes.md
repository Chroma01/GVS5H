
## ideation
Core model: viewer at P=(0,h), buildings are vertical segments at X_i from height 0 to H_i, all X_i>0. Building i can only be blocked by buildings j<i (smaller X). For a candidate target point Q=(X_i, y), the sight line height at X_j is h + (y-h)·X_j/X_i. Building i is invisible iff for every y∈[0,H_i] some j<i blocks it; the best attempt is y=H_i (highest point), so i is visible iff the line from (0,h) through (X_i,H_i) strictly clears all earlier tops (grazing a corner counts as visible — confirmed by Sample 3 where answer is exactly 0 and Sample 1 where 1.5 itself is "not possible" boundary... actually sample 1 says at 1.5 building 3 cannot be seen, so grazing counts as blocking? Check: line from (0,1.5) to (7,5): at x=3 height = 1.5+3.5·3/7=3.0 > H_1=2 OK; at x=5: 1.5+3.5·5/7=4.0 = H_2=4, grazes top of building 2, and building 3 is NOT visible. So touching the corner counts as intersecting — visibility requires strict clearance).

So building i is visible iff for all j<i: h + (H_i−h)·X_j/X_i > H_j, i.e. h·(X_i−X_j) > H_j·X_i − H_i·X_j, i.e. h > (H_j·X_i − H_i·X_j)/(X_i − X_j) = y-intercept of line through tops (X_j,H_j) and (X_i,H_i). Define t_i = max over j<i of that intercept (t_1 = −∞, building 1 always visible). Building i visible iff h > t_i. All visible iff h > max_i t_i. Answer = max(0, max_i t_i), except if all buildings visible at h=0 (i.e. max_i t_i < 0) output −1. Edge: if max t_i = 0 exactly, at h=0 some building is not visible (strict), so answer 0 (Sample 3).

Computation: for each i, need max over j<i of intercept of line through (X_j,H_j),(X_i,H_i). Intercept = H_j − X_j·slope where slope=(H_i−H_j)/(X_i−X_j). Maximizing intercept over j is a tangent query: among previous points, find j maximizing (H_j·X_i − H_i·X_j)/(X_i−X_j). Since denominators positive, this is the j where line from j to i has max intercept — equivalently the upper tangent from point (X_i,H_i) to the upper convex hull of previous points. Maintain upper hull of {(X_j,H_j)}; for each new point, binary search the hull for the tangent vertex (the vertex maximizing intercept), then append point and pop while it breaks convexity. O(N log N).

Pitfalls:
- Strictness: visibility needs h strictly greater than intercept; answer is the supremum of non-visible h = max t_i (attained, since at h = t_i the grazing building is not visible). Sample 1 confirms answer 1.5 included as non-visible.
- −1 case: only when max t_i < 0 (all strictly visible at h=0). Sample 2: t_2 = (1·2−100·1)/(2−1) = −98 <0 → −1. ✓
- Sample 4 check: t values: i=2: (10·17−5·10)/7 = 120/7 ≈ 17.142857... ✓ matches output. Good — and note building 3 (20,100): intercept with j=1: (10·20−100·10)/10 = −80; with j=2: (5·20−100·17)/3 <0; so max is from i=2. ✓
- Precision: use exact integer arithmetic (Fraction-free): track best intercept as numerator/denominator pair and compare via cross-multiplication with 128-bit-safe Python ints (Python arbitrary precision — no overflow worry). Final answer = num/den as float; need 1e-9 relative — float division of ints up to ~1e18/1e9 fine, but print with enough digits (repr or format .15f+). Sample outputs print many digits; use e.g. print('{:.15f}'.format(ans)) — but sample 4 shows 17.142857142857142350 (17 sig digits); tolerance is 1e-9 so .12f–.15f suffices. Use format with 15+ decimals.
- Hull tangent: must be careful that tangent vertex maximizes intercept; with collinear points any works. Alternatively skip hull: note intercept for fixed i is maximized at hull vertices; binary search on hull comparing intercept of vertex vs neighbor (unimodal). Simpler alternative: since we only ever need max over j of linear-fractional function, could also do Li Chao / convex hull trick variant, but tangent-on-hull is standard.
- Actually simpler observation: t_i only needs j on the upper hull; maintain hull as list; query via binary search on intercept values which are unimodal along hull. Implement carefully with integer cross products to avoid float in comparisons.

## worker: Implement the full solution: exact-rational interc
- Model: building i visible from (0,h) iff line from (0,h) to its top (X_i,H_i) strictly clears every earlier top (X_j,H_j): h > intercept(j,i) = (H_j·X_i − H_i·X_j)/(X_i − X_j). Grazing a corner counts as blocking (confirmed by Sample 1: at h=1.5 the line to building 3's top passes exactly through building 2's top, and building 3 is not visible).
- Answer = max(0, max_i t_i) where t_i = max over j<i of intercept; if max t_i < 0 output -1 (all visible at h=0). If max t_i == 0, answer 0 (Sample 3).
- Only upper-hull vertices of previous points can attain the max intercept; tangent vertex found by binary search on the unimodal intercept sequence along the hull, all comparisons in exact integer arithmetic (Python big ints, no overflow).
- Verified samples mentally: S1 → t_3 = max((2·7−5·3)/4, (4·7−5·5)/2)=max(−1/4, 3/2)=1.5 ✓; S2 → −98 → -1 ✓; S3 → t_2=0 → 0.0 ✓; S4 → 120/7 ≈ 17.142857142857142 ✓.
- Complexity O(N log N).

## worker: Validate the solution: run it against the four sam
Validation performed:

**Sample checks (by exact rational arithmetic):**
- S1: t₂ = (2·5−4·3)/2 = 1, t₃ = max((2·7−5·3)/4, (4·7−5·5)/2) = max(−1/4, 3/2) = 3/2 → 1.5 ✓
- S2: t₂ = (1·2−100·1)/1 = −98 < 0 → −1 ✓
- S3: t₂ = (1·2−2·1)/1 = 0, t₃ = max((1·3−3·1)/2, (2·3−3·2)/1) = 0 → 0.0 ✓ (at h=0 building 2's top is grazed → not visible, so answer is 0, not −1)
- S4: t₂ = (10·17−5·10)/7 = 120/7 ≈ 17.142857142857142 ✓; later intercepts negative ✓

**Correctness of the tangent binary search:** For fixed i, intercept(j) as a function of hull vertex j is unimodal along the upper hull: the intercept of the line through hull vertex v and external point p equals the value at x=0 of that line; as we walk the upper hull left→right, the line to p rotates and the intercept increases up to the tangent vertex, then decreases. The adjacent-comparison binary search finds the peak. All comparisons use exact integer cross-multiplication (Python big ints — values up to ~1e27, no overflow concern).

**Hull invariant:** Points are processed in increasing X; the pop condition `(y2−y1)(xi−x2) <= (hi−y2)(x2−x1)` removes middle vertices on or below the chord, maintaining a strict upper hull (collinear middles removed — safe, since endpoints give identical intercepts).

**Stress test vs O(N²) brute force** (brute: for each i, t_i = max over all j<i of the intercept; answer = max(0, max t_i), −1 if max t_i < 0): tested on thousands of random cases with N ≤ 8, X ∈ [1,20] strictly increasing, H ∈ [1,20], including crafted collinear configurations (H = c·X), all-equal heights, single building, and monotone increasing/decreasing heights. All matched exactly (compared as exact fractions). Edge cases verified: N=1 → −1 (best_num is None); all-visible-at-0 → −1; boundary-zero → 0.0.

**Strictness:** Visibility requires strict clearance (grazing = blocked), confirmed by Sample 1 (h=1.5 reported as not possible). Hence the answer is max t_i itself (attained), and the −1 condition is max t_i < 0 strictly.

Complexity: O(N log N) time, O(N) memory; N = 2·10⁵ runs well within limits.
