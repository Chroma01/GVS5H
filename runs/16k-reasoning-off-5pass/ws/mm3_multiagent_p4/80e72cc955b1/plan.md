We need, for each query `[l, r]`, the minimum number of pairwise `/4` operations to zero all elements `l…r`.  
Let `cost(x)` be the number of times we must apply `floor(v/4)` to a single value to reach 0; equivalently, `cost(x) = 1 + cost(floor(x/4))` with `cost(0)=0`. We can precompute `cost(x)` for `x` up to `10^9` (max depth ~ 16) by iterating powers of 4.

For a multiset, the optimal strategy is: repeatedly pair the two largest remaining costs. This greedy is optimal because each operation reduces total "remaining cost sum" by exactly 1, while using both slots per operation. The minimum operations is therefore `max(ceil(S/2), max_cost)`, where `S` is the sum of costs of all elements and `max_cost` the largest cost in the range.

So per query:
- compute `S(l, r)` = sum of `cost(x)` for x in `[l, r]`,
- compute `M(l, r)` = max of `cost(x)` for x in `[l, r]`,
- answer = `max( (S+1)//2, M )`.

Both `S` and `M` can be computed in O(log r) by counting how many numbers in `[l, r]` fall into each bucket `[4^k, 4^{k+1}-1]`. Iterate `k` while `4^k <= r`; let `lo = max(l, 4^k)`, `hi = min(r, 4^{k+1}-1)`; if `lo <= hi`, add `(hi-lo+1) * (k+1)` to sum and update max with `k+1`. Finally sum answers.