- **Cut condition:** Strong connectivity is equivalent to requiring an added white-to-black edge crossing from right to left across every cut between consecutive vertices.
- **Relevant cuts:** For each \(r<n\), it is sufficient to inspect the cut immediately before the \((r+1)\)-st black vertex. For \(r=n\), inspect the cut immediately after the last black vertex. Let `t[r]` be the number of whites to the left of that cut.
- **Bad event:** `E_r` is the event that all first `r` black vertices are paired with whites among the first `t[r]` whites. It is impossible when `t[r] < r`.
- **Important endpoint correction:** The final event must be included. If the string ends in `B`, then `t[n]=n`, so `E_n` is universal and the answer is zero. If it ends in `W`, the final cut uses the whites before the last black, and may be impossible rather than universally bad. Therefore no direct `s[-1] == "W"` rejection is valid.
- **Inclusion-exclusion recurrence:** With `dp[0]=1`, for valid `r`,
  `dp[r] = -invfact(t[r]-r) * sum(dp[i] * fact(t[r]-i))` over `i<r`.
- **Final count:** After the last selected bad event `E_r`, the remaining `n-r` black vertices can be paired arbitrarily, contributing `fact[n-r]`. Thus the answer is `sum(dp[r] * fact[n-r])` for `0 <= r <= n`.
- **Acceleration:** CDQ divide-and-conquer applies the transitions from the left half to the right half. Each transition batch is a convolution with the factorial sequence, computed by NTT.
- **Validation:** The corrected endpoint handling gives `BW -> 1` and `WB -> 0` for `N=1`, matches the three provided samples, and agrees with exhaustive permutation enumeration for balanced strings at small `N`.
