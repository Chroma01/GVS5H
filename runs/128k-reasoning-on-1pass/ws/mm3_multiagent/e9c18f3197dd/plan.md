The problem can be reframed as covering the set of target values with “upgraded” numbers from `nums`.  
Since each target needs a multiple, and any element can be increased to any larger value, for a subset `S` of targets the cheapest way to make a number `x` a multiple of all values in `S` is to raise it to the smallest multiple of `LCM(S)` that is at least `x`.  
Thus each `nums[i]` can be assigned a (possibly empty) subset `S_i` with cost `ceil(x/LCM(S_i))*LCM(S_i) – x`.  
We must choose subsets for all elements so that every target appears in at least one chosen subset, minimizing total cost.  
Because `|target| ≤ 4`, there are at most `2^4‑1 = 15` non‑empty subsets. We can pre‑compute their LCMs and, for every `nums[i]`, the cost for each subset.  
A dynamic programming over masks (`mask` = set of already covered targets) processes the array once: `dp[mask]` = minimal cost after handling some prefix of `nums`. For each new element we try assigning it any subset `S` and update `dp[mask|S]` with the added cost.  
Complexity is `O(n·4^{|target|}) ≤ 5·10⁴·256 ≈ 1.3·10⁷` operations and `O(2^{|target|})` memory, well within limits.