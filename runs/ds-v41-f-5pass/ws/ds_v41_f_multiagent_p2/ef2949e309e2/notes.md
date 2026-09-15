- **Problem:** Count size-5 subsequences whose middle element is the unique mode, modulo 1e9+7.
- **Approach:** Fix middle selected index `i`, let `x = nums[i]`. Choose 2 indices left of `i` and 2 right. `x` must appear at least twice overall. Split counts by total frequency `f` of `x` in the 5 elements.
- **Frequency cases:** `f = 5, 4, 3` are always valid because the at most 2 non-`x` elements cannot tie or beat `x`. Only `f = 2` needs care: the 3 non-`x` values must be pairwise distinct.
- **Formulas:** Let `Lx, Rx` be counts of `x` on the left/right, and `lNonx, rNonx` be non-`x` counts. Let `C2[t] = t*(t-1)//2`.
  - `f=5`: `C2[Lx] * C2[Rx]`
  - `f=4`: `C2[Lx] * Rx * rNonx + C2[Rx] * Lx * lNonx`
  - `f=3`: `C2[Lx] * C2[rNonx] + C2[Rx] * C2[lNonx] + Lx * Rx * lNonx * rNonx`
  - `f=2`: `Lx * A + Rx * B`, where for `v != x` with `p_v = left[v]`, `q_v = right[v]`:
    `Sp = sum C2[p_v]`, `Sq = sum C2[q_v]`, `T1 = sum p_v*q_v`, `T2 = sum p_v*q_v^2`, `T3 = sum p_v^2*q_v`,
    `A = lNonx*(C2[rNonx]-Sq) - rNonx*T1 + T2` (extra `x` on left),
    `B = rNonx*(C2[lNonx]-Sp) - lNonx*T1 + T3` (extra `x` on right).
- **Implementation:** Coordinate-compress values. Slide `i` from left to right, maintaining `left` and `right` frequency arrays. Decrement `right[x]` before computing, increment `left[x]` after. Precompute `C2` up to `n`.
- **Complexity:** `O(n * m)` time where `m <= n` distinct values (at most ~10^6 inner steps), `O(n)` extra space.
- **Validation:** Provided examples pass: `[1,1,1,1,1,1] -> 6`; `[1,2,2,3,3,4] -> 4`; `[0,1,2,3,4,5,6,7,8] -> 0`. Randomized brute-force cross-check over small arrays (`n <= 9`) passed. `n=1000` all-equal stress test produced `291192450` (which equals `C(1000,5) mod 1e9+7`) and ran fast.
