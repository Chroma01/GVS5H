
## ideation
The core difficulty is that each number in `nums` can potentially satisfy multiple targets simultaneously if it becomes a common multiple of them. Since `target.length <= 4`, we can use bitmask DP over subsets of targets. For each subset, we need the LCM of its targets. For each `nums[i]`, the cost to make it a multiple of `L` is `(L - nums[i] % L) % L`. We want to choose disjoint assignments of nums elements to subsets (each element used at most once) minimizing total cost to cover all targets.

Key insight: This is a set-cover-like DP where `dp[mask]` = min cost to satisfy targets in `mask`. For each number, we can either skip it or use it to cover some submask. Since each number can only be used once, we iterate numbers and update DP in reverse (or use new DP array per number).

Pitfalls:
- LCM can overflow if not careful, but with values ≤ 10^4 and at most 4 targets, LCM fits in 64-bit (max ~10^16, but Python handles big ints anyway).
- Cost formula: if `nums[i] % L == 0`, cost is 0, not L.
- We must not reuse the same nums element for multiple subsets in the same "step" — but actually one element CAN cover multiple targets at once (as a common multiple), which is handled by assigning it to a subset mask (the LCM of that subset).
- DP transition: for each element, for each mask, for each submask of mask's complement... Standard approach: `new_dp[mask | sub] = min(new_dp[mask | sub], dp[mask] + cost[i][sub])` for all submasks, plus carry-over `new_dp[mask] = dp[mask]`.

Complexity: O(n * 3^k) where k = target.length ≤ 4, so 3^4 = 81, n ≤ 5*10^4 → ~4M operations, fine.

## worker: Implement the complete solution: precompute LCM fo
- Precomputed `lcm[mask]` for all non-empty subsets of `target` using the standard `a // gcd(a, b) * b` formula (safe ordering to avoid intermediate overflow concerns in fixed-width languages; Python handles big ints anyway).
- For each `x` in `nums`, computed `cost[mask] = (L - x % L) % L` equivalently via the `r == 0` check, giving the increments needed to make `x` a multiple of `lcm[mask]` — meaning that single element then covers every target in `mask`.
- Bitmask DP: `dp[mask]` = min operations to cover targets in `mask` using processed elements. For each element we either skip it (carry over) or assign it to any non-empty submask of the uncovered targets. Using a fresh `new_dp` per element guarantees each element is used at most once.
- Complexity: O(n · 3^k) with k ≤ 4 → at most ~4M submask iterations for n = 5·10⁴, well within limits. LCM values fit comfortably (≤ ~10¹⁶ worst case, exact in Python).
- Verified against examples: [1,2,3],[4] → 1; [8,4],[10,5] → 2 (element 8 → 10 covers both via lcm(10,5)=10, cost 2); [7,9,10],[7] → 0.
