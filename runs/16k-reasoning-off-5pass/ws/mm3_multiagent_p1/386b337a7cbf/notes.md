
## ideation
**Core difficulty:**  
- We need to pick a subsequence (order preserved) whose alternating sum equals k and whose product ≤ limit, maximizing the product.  
- `n ≤ 150`, but `2^150` is impossible. However, `nums[i] ≤ 12` and `limit ≤ 5000` suggest a DP over achievable (alternating sum, product) states.

**Key observations:**  
1. Alternating sum = `sum(even indices) - sum(odd indices)`. This is equivalent to a running difference: start at 0, for each added element `v`:
   - If added at even index (0-based in the subsequence), the new diff = `old_diff + v`.
   - If added at odd index, the new diff = `old_diff - v`.
   So we can maintain parity (even/odd length) and the current difference.
2. Product is at most `limit` (or we can cap at `limit` to prune). `limit ≤ 5000` is small.
3. For each parity and each possible alternating sum, we only need to keep the **maximum product** achievable (if two states have same sum and parity, the larger product dominates the smaller one for future extensions and final answer).
4. DP transitions: iterate over `nums`. For each `v`, we decide to take it (flipping parity, updating sum and product) or skip it. We must process in order to maintain subsequence property.

**Candidate approaches:**  
- **DP over index, parity, sum, product** using sets/dictionaries.
  - For each parity, maintain a dictionary `sum -> max_product`.
  - Transition by taking `v`: new_parity = 1 - parity, new_sum = sum ± v, new_product = product * v (capped at `limit` if we only care about ≤ limit, but we need to keep exact product up to `limit`).
  - Skip: keep previous states.
- Since `sum` can range from `-150*12 = -1800` to `+1800`, and product from 0 to `limit` (5000), this is feasible.
- Use a dictionary or two dictionaries for even/odd parity.

**Pitfalls:**  
- Product can be zero (since `nums[i]` can be 0). If we multiply by 0, product becomes 0 and stays 0. We must handle 0 correctly: once a 0 is included, product is 0 and cannot increase.
- Subsequence must be non-empty.
- Need to handle negative alternating sums (`k` can be negative).
- Capping product at `limit` to keep state small, but be careful: if we only keep products ≤ limit, we might miss that a larger product is later divided? No division; only multiplication. So if product exceeds `limit`, it can never become ≤ limit again. So we can safely discard states with product > limit.
- Subsequence order matters only for the alternating sum sign, which we handle via parity.
- Complexity: For each element, we iterate over current states. Number of states is bounded by number of possible sums * 2. Sums are bounded by ±1800, so ~3600 possible sums per parity. That's about 7200 states max. Transitions are O(states) per element, so ~150 * 7200 ≈ 1M operations, easily fast.

**State representation:**  
- `even`: dict mapping `sum` to max product for subsequences of even length (including empty subsequence: sum=0, product=1? Wait, empty subsequence has product 1 by convention? Actually for product, empty is 1. But we can just initialize `even` with {0: 1} representing empty subsequence. When we take first element, we go to odd parity. For product 1 is neutral. But we must be careful: if we include 0, product becomes 0. Starting product 1 is fine.
- `odd`: dict for subsequences of odd length, initially empty.
- For each `v` in `nums`:
  - Take it from `even` -> update `odd`: `new_sum = sum + v` (since it's added at even index in the new subsequence? Wait: If current subsequence has even length, its last added element was at odd index (0-based in subseq). Adding a new element makes it odd length, and the new element is at even index? Let's re-derive:  
    - Subsequence indices: 0,1,2,...  
    - If we have an even-length subsequence (length L even), its last index is L-1 (odd). Adding a new element at index L (even in the new subsequence). So the new element contributes `+v` to the alternating sum.  
    - If we have an odd-length subsequence (length L odd), its last index is L-1 (even). Adding new element at index L (odd), contributes `-v`.  
  - So from `even` (even length), adding v: new parity = odd, new_sum = old_sum + v.  
  - From `odd` (odd length), adding v: new parity = even, new_sum = old_sum - v.  
  - Update product: `new_product = old_product * v` (capped at `limit` if we want to prune, but we need to store exact product if ≤ limit; if > limit, we can ignore).
  - Skip: keep `even` and `odd` unchanged.
  - After processing both, we need to merge: for each sum in new states, keep max product.

**Implementation details:**  
- Use `defaultdict(lambda: -inf)` or just dict with max comparison.
- During transition, iterate over items of current dict, compute new sum, new product = old_product * v. If new_product > limit, skip (or set to limit+1 and later ignore). But wait: if we cap, we lose information. Better: if new_product > limit, don't add the state. Because any further multiplications will only increase product, so it will never become ≤ limit.
- However, what if we multiply by 0? Product becomes 0. That's fine.
- For each transition, we create a new dict for the target parity, then merge by taking max.
- At the end, check `odd` dict (since non-empty subsequence has odd length? No, length can be even or odd. The alternating sum definition works for any length. For even length, the last index is odd; for odd length, last is even. Both are valid subsequences. So we need to check both `even` and `odd` for `sum == k`. But wait: if we start with empty subsequence in `even`, then any subsequence is reachable. At the end, we should look at all states in `even` and `odd` (except the empty one in `even` if we only want non-empty, but empty has sum 0, product 1. If k=0, we might erroneously return 1 if we include empty. We must exclude empty subsequence explicitly. Since we only transition by taking elements, and we start with only empty in `even`, we can just ignore the entry with product=1? Actually, we can just check after DP: if k != 0, empty doesn't match. If k == 0, we must not return the empty subsequence product (which is 1). So we should either not include the empty state in the final check, or ensure that we only consider states that resulted from taking at least one element. Since we start with empty in `even`, and we add to `even` from `odd` transitions, and `odd` is empty initially, the empty state remains in `even` but we can simply not consider product=1 unless it came from a real subsequence. Actually, we can just remove the initial empty state before checking, or better, initialize `even` as empty and handle the first element specially? But it's easier to keep `even` = {0: 1} as base, and at the end filter out product=1 only if we know it's the empty one. But if there is a real subsequence with product 1 (all 1's), we should keep it. So we can't just filter by product. Instead, we can simply not include the empty state in the initial set, but then how to transition? We need a base for taking the first element. Actually, we can treat the first element as starting from "no previous state" and just add it to `odd` with sum=v, product=v. That avoids the empty state entirely. But the generic transition from `even` to `odd` works if we have the empty state. The empty state has sum=0, product=1. It's a valid state in DP but not a valid final answer unless k=0 and we consider empty. Since problem says "non-empty subsequence", we must exclude empty. So we can just keep the DP with empty base, and at the end when looking for k, we ignore the state (0,1) in even. But if there is a non-empty subsequence with sum=0 and product=1, it would be in `even` with product=1, same as empty. That's fine because they are distinct states but same value. We just need to not return 1 if no other state gives k=0. Actually, if we return the max product among all states with sum=k, and the empty state is the only one with sum=k=0, we would return 1, which is wrong. So we must explicitly exclude the empty state. Since the empty state is uniquely identified by product=1 and sum=0 and parity even, but there could be other even-length subsequences with product=1 (all ones). So we can't just exclude by value. Better: just don't add the empty state to the final candidate set. Since we only need the max product, we can just start DP without the empty state and handle the first element by directly initializing `odd` with (v, v) for each v? But that doesn't allow combining multiple elements properly because we need to track parity. Actually, we can start with `even` = {} and `odd` = {}. For each v, we can take v as the first element: it goes to `odd` with sum=v, product=v. Then we can also skip. So we need to handle "start new subsequence" separately. The generic transition from `even` (empty) to `odd` works if we include the empty state. So it's simpler to include it and at the end, we can just check all states in `even` and `odd` but if the only state for k is (0,1) in `even`, we return -1. But we can do: if k == 0 and the max product is 1, we need to know if there is any non-empty subsequence. So we can just track a boolean or count. Simpler: we can just not add the empty state to the initial `even` dict, but instead for each v, we can add a transition from "nothing" to `odd` with (v, v). This is equivalent to initializing `odd` with {v: v} for each v. But then we lose the ability to extend? No, we can just do: for each v, we have a "virtual" state that we can extend. But it's easier to include the empty state and at the end, if the answer is 1 and k=0, we return -1 (unless there is a real subsequence with product 1). Wait, if there is a real subsequence with product 1 (e.g., [1]), its product is 1. That is a valid answer. The empty subsequence is not valid. But both have product 1. So returning 1 is correct if there is a real subsequence with product 1. The only problem is if the ONLY subsequence with alternating sum k is the empty one. So we need to know if the state (0,1) corresponds to a real subsequence or just the base. Since we start with (0,1) in `even`, and we never remove it (we only add to it), the state (0,1) in `even` always exists regardless of whether we build a real subsequence. So at the end, if we look at `even` and see sum=0, product=1, it might be the base or a real one. We can't distinguish. So we must avoid including the base in the final check.  
**Solution:** Start with `even` = {0: 1} but at the end, we ignore the state (0,1) in `even`. But if there is another real subsequence with sum=0, product=1, its state will also be (0,1). We only have one entry per sum-product pair? Actually we store max product per sum. So if there is a real subsequence with product 1, it will be stored as product 1, same as base. So we can't distinguish. But that's fine: the base is always there with product 1. If there is no other way to get sum=0 with product ≤ limit, then the only state is the base, and we should return -1. But if we just return the max product, we get 1. So we need to know if there is at least one non-empty subsequence.  
**Better approach:** Do not include the empty base. Instead, for the first element, we manually add it to `odd`. But then we have to handle the fact that we can also skip it. Actually, we can just initialize `even` = {0: 1} and then after processing all elements, we remove the entry for sum=0 if product=1 and it's the only one? But there could be multiple real subsequences with sum=0, product=1. They would all merge into the same (0,1) entry. So we can't tell.  
**Alternative:** Track a set of states including a flag "is_nonempty". Or simpler: we can just not include the empty state in the initial `even`. Instead, for each `v`, we consider taking it as the first element: new state in `odd` with sum=v, product=v. And we can also skip. But we need to ensure that we can take multiple elements. The recurrence:  
- `new_even` = `even` (skip all) + take from `odd`  
- `new_odd` = `odd` (skip all) + take from `even`  
If we start with `even` = {} and `odd` = {}, then `new_odd` from taking from `even` is empty. So we need to seed `odd` with singletons. For each v, we can add (v, v) to `odd` before processing? But that would treat each v as a separate base, and then we can extend them. But we have to be careful: we process v's sequentially. We can just do: for each v, we first add a transition from "empty" to `odd` with (v, v). But since we are iterating in order, we can just do: for each v, we compute new_odd = (odd with skip) union (even with take v) union {(v, v)}. But wait, that would allow using v as a subsequence by itself, which is correct. But we also need to allow combinations like v1 then v2. If we do this for each v sequentially, the first v will be added to odd, and then when we process the second v, we can take it from odd (which now has the first v) to go to even. So it works. So we can just initialize `even` = {} and `odd` = {}. Then for each v in nums:  
- new_even = even copy  
- new_odd = odd copy  
- For each (s, p) in even: new_odd[s+v] = max(new_odd.get(s+v, 0), min(p*v, limit)) but we only keep if p*v <= limit.  
- For each (s, p) in odd: new_even[s-v] = max(...)  
- Also, add (v, v) to new_odd if v <= limit.  
- Assign even = new_even, odd = new_odd.  
But wait: we also need to skip elements. The copy handles that. This avoids the empty base entirely. At the end, we check both even and odd for sum == k, take max product. This correctly handles non-empty because we never add the empty state.  
However, we must be careful: when we add (v, v) to new_odd, we are treating v as a subsequence of length 1. That's fine. But what about the empty subsequence? It's never added. So this is clean.  
But we also need to consider that we can take elements out of order? No, subsequence preserves order. Our DP processes in order, so it's correct.  
One more thing: we need to cap product at limit. If product > limit, we discard the state. So we only store products ≤ limit. This keeps the state space small.  
We should also consider that product can be 0. If v=0, then p*v = 0. That's fine.  
Complexity: For each element, we iterate over current states. The number of states is bounded by the number of possible sums (which is at most n*12*2 = 3600) per parity, so 7200 states. Each transition is O(states). So total O(n * states) = 150 * 7200 = 1,080,000. With some overhead for dict operations, it's fine.  
We need to handle negative sums. Python dicts support negative keys.  
We should use `defaultdict(int)` or just regular dict and `.get()`.  
We can also prune by keeping only the max product per sum. So we can use a dict for each parity: `sum -> max_product`.  
**Algorithm steps:**  
1. Initialize `even = {}`, `odd = {}`.  
2. For each `v` in `nums`:  
   a. If `v > limit`, we can still include it? No, if v > limit, then any subsequence containing v has product at least v > limit (since all nums >= 0). So we can skip such v entirely (they can never be in a valid subsequence). Actually, wait: if v=0, product is 0. If v>limit, then even a single element exceeds limit, so we cannot take it. But we could still skip it. So we can just process v normally: when we try to take it, we check if old_product * v <= limit. If v > limit, then old_product * v > limit for any old_product >= 1. So it will be discarded. So we don't need a special case. But if v=0, old_product * 0 = 0 <= limit (if limit >= 0). So it's fine.  
   b. Create new dicts `new_even = even.copy()`, `new_odd = odd.copy()`.  
   c. Add singleton: if v <= limit: new_odd[v] = max(new_odd.get(v, 0), v)   [Note: product is v, sum is v]  
   d. Transitions from even to odd: for (s, p) in even.items(): new_p = p * v; if new_p <= limit: new_odd[s+v] = max(new_odd.get(s+v, 0), new_p)  
   e. Transitions from odd to even: for (s, p) in odd.items(): new_p = p * v; if new_p <= limit: new_even[s-v] = max(new_even.get(s-v, 0), new_p)  
   f. even = new_even, odd = new_odd  
3. After loop, check both even and odd for sum == k, find max product ≤ limit. If none, return -1.  
**Potential issues:**  
- We are using `max(new_odd.get(s+v, 0), new_p)`. But what if new_p is 0? That's fine. But we should initialize missing keys to -1 or something to indicate absence. Since product is non-negative, we can use -1 to mean no state. But we also have to be careful: if we have multiple ways to reach the same sum, we keep the max product. If product is 0, it's valid. So we can use -1 as sentinel for "no product". But when we do `max(new_odd.get(s+v, -1), new_p)`, if new_p is 0, it works.  
- However, we also have to consider that product can be 0. If we have a state with product 0, any further multiplications stay 0. So it's fine.  
- We must ensure that we don't accidentally drop states with product 0 if there is a better product? But we keep max, so if we have a product 0 and a product 5 for the same sum, we keep 5. If we only have 0, we keep 0. That's correct.  
- What about the limit being 0? The problem says 1 <= limit <= 5000. So limit >= 1. So product 0 is always ≤ limit. So states with product 0 are valid.  
- Edge case: k can be negative. Our sums are signed. The transitions use s+v and s-v. That's correct.  
- Edge case: nums can contain 0. If we take 0, product becomes 0. The alternating sum changes by +v or -v. So we need to handle that. Our transitions handle it.  
- Memory: we store at most ~3600 entries per dict. That's fine.  
- Speed: 150 iterations, each iterating over up to 3600 entries. That's ~540k iterations. Very fast.  

**Possible improvement:**  
- We can use `defaultdict(lambda: -1)` for new_even and new_odd, but we need to copy the old ones. Using dict and .copy() is fine.  
- We should be careful: when we do `even.copy()`, we get a shallow copy. That's fine since values are numbers.  

**Testing with examples:**  
Example 1: nums=[1,2,3], k=2, limit=10.  
- Start: even={}, odd={}  
- v=1: new_even={}, new_odd={1:1} (singleton)  
- v=2: from odd {1:1} -> new_even: s=1-2=-1, p=2 -> {-1:2}. from even {} nothing. singleton: new_odd[2]=2. also keep old odd {1:1}. So odd={1:1, 2:2}, even={-1:2}  
- v=3: from even {-1:2} -> new_odd: s=-1+3=2, p=6 -> odd[2]=max(2,6)=6. from odd {1:1, 2:2} -> new_even: s=1-3=-2, p=3; s=2-3=-1, p=6. So even gets {-2:3, -1:6}. singleton: new_odd[3]=3. Keep old odd. So odd={1:1, 2:6, 3:3}, even={-1:2, -2:3, -1:6? wait we need to merge. Let's do carefully:  
  even was {-1:2}.  
  odd was {1:1, 2:2}.  
  Process v=3:  
  new_even = even.copy() = {-1:2}  
  new_odd = odd.copy() = {1:1, 2:2}  
  Singleton: v=3 <=10, so new_odd[3] = max(new_odd.get(3, -1), 3) = 3.  
  From even: s=-1, p=2 -> new_p=6 <=10 -> s+v = 2 -> new_odd[2] = max(new_odd.get(2, -1), 6) = 6.  
  From odd:  
    s=1, p=1 -> new_p=3 -> s-v = -2 -> new_even[-2] = max(new_even.get(-2, -1), 3) = 3.  
    s=2, p=2 -> new_p=6 -> s-v = -1 -> new_even[-1] = max(new_even.get(-1, -1), 6) = 6 (was 2, now 6).  
  So final: even = {-2:3, -1:6}, odd = {1:1, 2:6, 3:3}.  
  Check k=2: odd has 2:6. That's product 6. limit=10, so 6 <=10. Answer 6. Correct.  

Example 2: nums=[0,2,3], k=-5, limit=12.  
- v=0: new_odd from singleton: 0 <=12, new_odd[0]=0. even stays {}. odd={0:0}.  
- v=2: from odd {0:0} -> new_even: s=0-2=-2, p=0*2=0 -> new_even[-2]=0. from even {} nothing. singleton: new_odd[2]=2. Keep old odd. So even={-2:0}, odd={0:0, 2:2}.  
- v=3: from even {-2:0} -> new_odd: s=-2+3=1, p=0 -> new_odd[1]=0. from odd: s=0 -> new_even: s=0-3=-3, p=0 -> new_even[-3]=0; s=2 -> new_even: s=2-3=-1, p=6 -> new_even[-1]=6. singleton: new_odd[3]=3.  
  So even={-2:0, -3:0, -1:6}, odd={0:0, 2:2, 1:0, 3:3}.  
  Check k=-5: not found. Return -1. Correct.  

Example 3: nums=[2,2,3,3], k=0, limit=9.  
Let's simulate quickly:  
- v=2: odd={2:2}  
- v=2: from odd {2:2} -> even: s=2-2=0, p=4 -> even={0:4}. singleton: odd[2]=max(2,2)=2. So even={0:4}, odd={2:2}.  
- v=3: from even {0:4} -> odd: s=0+3=3, p=12 >9? 4*3=12 >9, so skip. singleton: odd[3]=3. from odd {2:2} -> even: s=2-3=-1, p=6 -> even[-1]=6. So even={0:4, -1:6}, odd={2:2, 3:3}.  
- v=3: from even {0:4} -> odd: s=0+3=3, p=12>9 skip. from even {-1:6} -> odd: s=-1+3=2, p=18>9 skip. singleton: odd[3]=max(3,3)=3. from odd {2:2} -> even: s=2-3=-1, p=6 -> even[-1]=max(6,6)=6. from odd {3:3} -> even: s=3-3=0, p=9 -> even[0]=max(4,9)=9. So even={-1:6, 0:9}, odd={2:2, 3:3}.  
Check k=0: even has 0:9. limit=9, so 9 <=9. Answer 9. Correct.  

**Conclusion:** The DP approach works and is efficient.  

**One more pitfall:** The problem says "subsequence" not "subset". Our DP processes in order and considers taking or skipping each element in the given order. That's exactly subsequence.  

**Another pitfall:** We must ensure that we don't miss the case where we take elements and the product becomes 0 early, then later multiply by something. But product 0 stays 0. So it's fine.  

**Final check:** The DP keeps only max product per sum. Could there be a case where a smaller product is better because it allows a future multiplication that stays under limit, while the larger product would exceed limit? No, because products only increase when multiplied by positive numbers (nums[i] >= 0). So if you have a larger product now, any future multiplications will yield an even larger product. So if a larger product is ≤ limit now, it will always be at least as good as a smaller product for future extensions (the resulting product will be larger, but could exceed limit sooner). Wait, that's a problem! If we have two states with the same sum: one with product 5, one with product 3. Both are ≤ limit. If we multiply both by 2, the first gives 10, the second gives 6. If limit is 8, then the first becomes invalid, but the second is still valid. So the smaller product might be better! This is a crucial pitfall. We cannot prune by keeping only the max product per sum, because a larger product might be "too large" to allow future multiplications, while a smaller product could still grow.  
**Correction:** We need to keep multiple products per sum, or we need to rethink. Since nums[i] ≤ 12, and limit ≤ 5000, the number of possible products is not too large. For each sum, we might need to keep several products. But the number of possible products up to 5000 is at most 5000. But with sums, the state space could blow up. However, we can observe that for a fixed sum, the products that matter are those that are "Pareto optimal": you can't have two products where one is a multiple of the other and the larger one doesn't exceed the limit? Actually, if we have products p1 < p2, and p2 is valid (≤ limit), then p2 is always at least as good as p1 for final answer (since we want max product). But for extending, p2 might exceed limit sooner. So we need to keep all products that are "minimal" in some sense? Actually, we want to keep all products that are not "dominated". A product p1 dominates p2 if p1 ≤ p2 and p1 is "more flexible"? No, if p1 < p2, p1 is smaller. For extension, multiplying by v gives p1*v and p2*v. p1*v < p2*v. So if p2*v ≤ limit, then p1*v is also ≤ limit. So p1 can always reach any state that p2 can, with a smaller product. So for the purpose of existence of some product, p1 is "better" (more flexible) because it can be multiplied further without exceeding limit. However, we want to maximize the final product. So if p2*v is valid and larger than p1*v, we want p2. But if p2*v exceeds limit, p1*v might still be valid. So we need to keep p1. In fact, for each sum, we should keep all products that are not "dominated" in the sense that no other product is a divisor? Actually, the set of useful products for a given sum is the set of products that are "maximal" under the relation: p1 is better than p2 if p1 <= p2 and p1 divides p2? Not exactly.  
Consider two products p1 and p2 with p1 < p2. If p1 * v <= limit but p2 * v > limit, then p1 is better for extension with v. So we cannot discard p1. In general, we need to keep all products that are "Pareto optimal" with respect to future extensions. Since the future extensions are multiplications by numbers from the set (which are bounded by 12), we can keep all products that are not "redundant". A product p is redundant if there exists another product q < p such that for all v in the remaining numbers, q*v <= limit implies p*v <= limit? But we don't know the remaining numbers. So we might need to keep all products up to limit. That would be up to 5000 per sum, which times 3600 sums is ~18 million, still maybe okay? 150 * 18000000 = too big.  
But we can do better: since nums[i] <= 12, the product grows by factors up to 12. The number of distinct products reachable for a given sum is at most the number of subsets, but we can bound it. Actually, we can keep a set of products for each sum, but we can prune by removing any product p if there is another product q < p such that q divides p? Not exactly. If q < p, and we multiply both by the same sequence, the final product from q will be smaller. But if p * v > limit while q * v <= limit, we need q. So we need to keep q. In fact, for a fixed sum, the set of useful products are those that are not "dominated" by a smaller product that can be multiplied by the same factors to stay within limit. Since the factors are all <= 12, if p1 and p2 are such that p1 < p2 and p1 * 12^k <= limit < p2 * 12^k for some k? This is getting complicated.  
**Alternative approach:** Since n is only 150, maybe we can use a different DP: treat the product as a dimension, but with limit 5000, we can do DP over (index, parity, sum, product) but only keep reachable states. The number of states is at most n * 2 * (range of sum) * (limit+1) = 150 * 2 * 3600 * 5001 ≈ 5.4e9, too large. But we don't need to keep all products; we can use a set of reachable (sum, product) pairs. The total number of reachable (sum, product) pairs across all parities is bounded by the number of subsequences, which is 2^150, but in practice much less because product is capped at 5000. For each sum, the number of distinct products is at most 5001. But sums range over ~3600, so worst-case 18 million states. That might be too much memory and time.  
**Observation:** We only care about the maximum product for each (sum, parity) at the end, but during DP we need to consider all because a smaller product might allow a longer sequence. However, note that the product is monotonic: if we have a product p, any future multiplications will increase it. If p > limit, it's invalid. So we only care about products ≤ limit. For a given sum, the set of products that can be achieved is a subset of [0, limit]. But we can prune: for a given sum, if we have two products p1 < p2, and both are ≤ limit, is p1 ever strictly better than p2 for the final answer? Only if p2 is invalid for the final answer (i.e., p2 > limit) but p1 is not. But if p2 ≤ limit, then p2 gives a larger or equal product for any extension (since multiplying by v >= 0 gives p2*v >= p1*v). So if p2 ≤ limit, p2 dominates p1 for the purpose of final product. However, for intermediate steps, p2 might exceed limit later, while p1 doesn't. But wait: if p2 ≤ limit now, and we multiply by v, we get p2*v. If p2*v > limit, then that path is invalid. But the path with p1 might still be valid if p1*v ≤ limit. So p1 could lead to a valid final product while p2 cannot. Therefore, we cannot discard p1.  
But note: if p2 ≤ limit, then p1 < p2. If we multiply by v, p1*v < p2*v. So if p2*v > limit, p1*v could still be ≤ limit. So p1 is "more flexible". So we need to keep both. However, we can keep a set of products that are "minimal" in the sense that no product divides another? Not exactly. For a fixed sum, the set of products we can achieve is closed under taking divisors? Not necessarily. But we can keep all products that are not "dominated" in the following sense: a product p is dominated if there exists another product q < p such that for all v in {0..12} (or all possible future v), q*v <= limit whenever p*v <= limit? That's not true in general because the future v's are specific to the remaining array. But we don't know them. So we might need to keep all products that are "reachable" and not "obsolete".  
**Better approach:** Since the array length is 150, we can use a meet-in-the-middle? 2^75 is too large.  
**Another idea:** Use DP where state is (parity, sum, product) but we use a dictionary of dictionaries, and we prune by only keeping products that are not "multiples" of smaller products? Let's think: For a fixed sum, if we have products p1 and p2 with p1 < p2, and p1 divides p2, then for any v, p1*v divides p2*v. If p2*v <= limit, then p1*v <= limit, and p1*v is smaller. So p2 is always better in terms of final product? Not exactly: if p2*v <= limit, p1*v is also <= limit but smaller. So p2 gives a larger product. So if we care about maximizing the final product, we should keep p2. But if p2*v > limit, p1*v might still be <= limit. So p1 might allow a valid sequence that p2 does not. So we need to keep p1 if it can lead to a valid sequence that p2 cannot. But note: if p1 divides p2, then p1 = p2 / d for some d. The only way p1*v <= limit while p2*v > limit is if p2*v > limit >= p1*v. That means p1*v <= limit < p2*v. Since p1 = p2/d, this is possible if d is large enough. So p1 is not dominated by p2.  
But we can keep the set of products that are "Pareto optimal" with respect to the partial order: p1 <= p2 in both value and divisibility? Actually, if p1 and p2 are such that p1 < p2 and p1 does not divide p2, they are not comparable. So we might need to keep all products that are not "dominated" by another product in the sense that for all future multiplications, the larger product is always better. But since future multiplications are multiplicative, if p1 and p2 are such that p1 <= p2, then for any sequence of multiplications by v_i, the product from p2 is always >= product from p1. So if p2 is valid (≤ limit) at the end, it gives a larger product. If p2 is invalid, p1 might be valid. So we need to keep p1 if p2 could become invalid while p1 remains valid. But p2 becomes invalid if multiplied by a v that makes it > limit. p1 might still be <= limit after that multiplication. So we need to keep p1 if there exists some v such that p2*v > limit and p1*v <= limit. That is equivalent to: limit/p2 < v <= limit/p1. Since v <= 12, if this interval contains an integer, then p1 is not dominated.  
**Pruning rule:** For a fixed sum, we can keep a set of products. We can remove a product p if there exists another product q in the set such that q <= p and for all v in {0,1,...,12} (or all possible remaining v), if q*v <= limit then p*v <= limit? Actually, we want to keep p if there is any v such that p*v > limit but q*v <= limit. That is: p is dominated by q if for all v, p*v <= limit implies q*v <= limit. But since p >= q, p*v >= q*v. So if p*v <= limit, then q*v <= limit automatically. So the condition is: for all v, if p*v <= limit then q*v <= limit. This is always true if q <= p because q*v <= p*v. So p is always dominated by any q <= p in the sense that if p is valid, q is valid. But that doesn't help because we want to know if p can lead to a valid final product that q cannot. Actually, if p is valid at the end, q is also valid but gives a smaller product. So we prefer p. The only reason to keep q is if p might become invalid later while q remains valid. But if p is currently valid, and we multiply by v, p might become invalid. q might remain valid. So we need q if there is some v such that p*v > limit and q*v <= limit. So p is not dominated by q if there exists v such that p*v > limit and q*v <= limit.  
So we can prune: remove q if for all v in the "future" set (which is all possible v from the array, i.e., 0..12), q*v <= limit implies p*v <= limit? That's always true. So we cannot prune based on current value alone without knowing future v. But we can keep all products that are "minimal" in the sense that no product in the set is a divisor of another? Not exactly.  
Given the constraints (n=150, limit=5000), the number of reachable (sum, product) pairs is actually not that large because for each sum, the products are the products of some subset of numbers. The number of distinct products of subsets of numbers with sum S is at most the number of subsets, but since numbers are small and limit is small, it's bounded. In the worst case, if all numbers are 1, then products are just 1 (since 1*1=1). So it's small. If numbers are 2, products are powers of 2 up to 2^150, but limited by 5000, so at most log_2(5000) ≈ 12 distinct products. So the number of products per sum is small. In fact, since all numbers are integers <= 12, the number of distinct products up to 5000 is at most 5000, but typically much smaller. We can just store a set of products for each sum. The total number of states across all sums is at most the number of subsequences with product ≤ 5000. That could be large but probably manageable. Let's estimate: each subsequence product ≤ 5000. The number of such subsequences is at most the number of subsets with product ≤ 5000. For numbers up to 12, the product grows quickly. The maximum length of a subsequence with product ≤ 5000 is when all numbers are 1: then length can be up to 150. So there are 2^150 subsets, but most have product > 5000. The number of subsets with product ≤ 5000 is at most the number of ways to choose a multiset of numbers from {1..12} with product ≤ 5000, times the number of ways to arrange them? Actually, since order matters in subsequence, the number of distinct (sum, product) pairs is the number of distinct multisets? No, because the sum depends on the order (parity). But if we consider all subsequences, the number of distinct (sum, product) pairs is at most the number of subsequences with product ≤ 5000. How many subsequences have product ≤ 5000? We can think of it as: each element is either taken or not, and the product of taken elements ≤ 5000. This is like a knapsack with product constraint. The number of such subsets is not trivial but for n=150 and small numbers, it might be large. For example, if all numbers are 1, then any subset has product 1, so there are 2^150 subsets, all with product 1. But the sum varies. So for sum=0, there are C(150,0)+C(150,2)+... subsets with alternating sum 0. The number of subsets with product 1 is 2^150. But in our DP, we only keep one product per sum? No, if we keep all products, we have 2^150 states for sum=0? That's impossible. So we must prune.  
The key is that for a fixed sum, the product is not unique. If all numbers are 1, then product is always 1 regardless of the subset. So we only need to keep product=1 for that sum. The issue is when numbers are not all 1. But if there are multiple ways to get the same sum with different products, we need to keep them. In the all-1 case, all products are 1, so we only need one. In general, the number of distinct products for a given sum is at most the number of distinct values of product of subsets that yield that sum. Since the numbers are small, the number of distinct products is small. For example, if we have numbers that are 2 and 3, the product can be 2^a * 3^b. Up to 5000, there are not many combinations. So the state space is manageable.  
**Revised approach:** Use DP with states as sets of (sum, product) pairs, without pruning by keeping only max product per sum. Instead, we keep all reachable (sum, product) pairs for each parity. We can represent each parity's state as a dictionary mapping sum to a set of products. But we need to be careful with memory. Since n=150, limit=5000, the number of possible products is at most 5001. The number of possible sums is about 3600. So worst-case 5001*3600 ≈ 18 million pairs. That's a lot but maybe okay in Python if we use sets of integers for products per sum. But we can do better: we can use a dictionary mapping (sum, product) to True, but we only need to store reachable pairs. The number of reachable pairs is at most the number of subsequences with product ≤ 5000. In the worst case, if all numbers are 1, the number of subsequences is 2^150, but the product is always 1, so for each sum, there is only one product (1). So the number of distinct (sum, product) pairs is at most the number of possible sums, which is ~3600. In the worst case, if numbers are such that many subsets yield different products, how many can there be? The product is a multiplicative function. For each sum, the set of products is a subset of divisors of numbers up to 5000. The number of divisors of numbers up to 5000 is not huge. For each product, the sum of elements is fixed. So the number of pairs is at most the number of ways to choose a subset with product ≤ 5000. That is bounded by the number of integer partitions with product constraint. I think it's safe to say it's manageable.  
We can implement it as:  
`even = set of (sum, product)`  
`odd = set of (sum, product)`  
Then for each v, we create new sets by taking each (s,p) in even, adding (s+v, p*v) if p*v <= limit, and similarly for odd. Also we add the singleton (v, v) for odd. This will store all reachable pairs. The size of the set will be at most the number of reachable pairs. In the worst case, it's bounded by the number of subsequences with product ≤ 5000. For n=150, is that number too large? Let's test a worst-case scenario: all numbers are 2. Then the product is 2^k. The limit is 5000, so 2^k ≤ 5000 => k ≤ 12. So any subsequence of length > 12 has product > 5000. So the number of subsequences with product ≤ 5000 is sum_{k=0}^{12} C(150, k). This is huge (C(150,12) is enormous). But many of these subsequences have the same product (2^k) and different sums. The sum is the sum of k twos, which is 2k. So for a fixed product 2^k, the sum is always 2k. So the (sum, product) pair is (2k, 2^k). So there are only 13 distinct pairs. So the set size is small.  
In general, the number of distinct (sum, product) pairs is bounded by the number of possible products (up to 5000) times the number of possible sums? No, each product corresponds to a specific sum in a given subsequence? Actually, the sum and product are not independent: for a given subset, the sum is the sum of its elements, product is the product. If all elements are 2, sum is 2k, product is 2^k. So for a fixed product, the sum is determined (if all elements are equal). But if elements are varied, a given product can correspond to many sums. For example, with elements {1,2,3}, product 6 can be from {2,3} sum=5 or {1,2,3} sum=6. So the number of pairs could be larger. But the number of distinct products is at most 5000. For each product, the number of possible sums is at most the number of ways to factor the product into numbers from the array, which is limited. So the total number of pairs is at most 5000 * (some small number). I think it's fine.  
**Implementation with sets of tuples:**  
- `even = set()` initially empty.  
- `odd = set()` initially empty.  
- For each v:  
  - `new_even = even.copy()`  
  - `new_odd = odd.copy()`  
  - If v <= limit: `new_odd.add((v, v))`  
  - For (s, p) in even: new_p = p * v; if new_p <= limit: new_odd.add((s+v, new_p))  
  - For (s, p) in odd: new_p = p * v; if new_p <= limit: new_even.add((s-v, new_p))  
  - even = new_even, odd = new_odd  
- At the end, iterate over even and odd, find max p where s == k.  
This will keep all reachable pairs. The memory usage is the number of reachable pairs. In the worst case, how many pairs can there be? Let's think of an array with many 1's and some other numbers. The product is mainly determined by the non-1 numbers. The 1's can be added to any subsequence without changing the product, but they change the sum. So for a fixed set of non-1 numbers, adding a subset of 1's will produce many different sums but the same product. So the number of pairs can be large: if we have 100 ones, and we have a fixed product P, we can have sums from S to S+100. So that gives 100 pairs for the same product. If we have many such products, the total could be large. But with n=150, the number of ones can be up to 150. The number of products is at most 5000. So worst-case pairs = 5000 * 150 = 750,000. That's okay. Actually, it's even less because the number of products is much smaller. So storing all pairs is feasible.  
**But wait:** If we have many ones, the number of subsequences is 2^150, but they all have product 1 if there are no other numbers. So the set of pairs is just (sum, 1) for each possible sum. The number of possible sums is 150 (from 0 to 150). So the set size is 151. So it's fine.  
Therefore, we can use the set-of-tuples approach. It is simpler and avoids the pruning pitfall. The only downside is that we might generate many states if there are many combinations of numbers that yield the same sum and product? But the set automatically handles duplicates. So it's safe.  
**Time complexity:** For each of the 150 elements, we iterate over the current sets. The size of the sets is at most the number of reachable pairs. In the worst case, if the set size is M, then time is O(n * M). M is bounded by the number of (sum, product) pairs, which as argued is at most a few hundred thousand. So n*M is at most 150 * 300,000 = 45 million, which might be a bit slow in Python but probably okay. We can optimize by using a dictionary for each parity: `sum -> set of products` or `sum -> list of products`. But the set of tuples is fine.  
We can also use a dictionary of sets to avoid iterating over all pairs for each v? No, we need to iterate anyway.  
**Optimization:** Use `defaultdict(set)` for each parity: `even[s] = set of products`. Then when we add a new state, we add to the set. This might be faster than storing tuples because we can iterate over sums and products. But the number of sums is smaller than the number of pairs? Actually, number of sums is ~3600. For each sum, the number of products is at most the number of ways to get that sum. So total pairs is sum of sizes of these sets. We can store as `dict[sum] -> set(product)`. This might be more efficient for iteration: for each v, we iterate over all (s, products_set) in even, and for each p in products_set, we compute new_p and add to new_odd. This is similar.  
Let's do that.  

**Final algorithm:**  
- Use two dictionaries: `even` and `odd`, each mapping `sum` to a set of valid products.  
- Initialize both as empty dicts.  
- For each v in nums:  
  - new_even = copy of even  
  - new_odd = copy of odd  
  - If v <= limit: add v to new_odd[v] (create set if needed)  
  - For each (s, prod_set) in even.items():  
    - For each p in prod_set:  
      - new_p = p * v  
      - If new_p <= limit: add new_p to new_odd[s+v]  
  - For each (s, prod_set) in odd.items():  
    - For each p in prod_set:  
      - new_p = p * v  
      - If new_p <= limit: add new_p to new_even[s-v]  
  - even = new_even, odd = new_odd  
- At the end, for each parity, look for sum == k, find max product in its set. Take max over both parities. If none, return -1.  

This should work.  

**Test with the examples:** Already did with the pruned version, but with sets we will keep all, so it should give the same results.  

**Edge case:** If k is not achievable, return -1.  

**Another edge case:** If limit is very small, e.g., limit=1, and nums contain 0. Then product 0 is allowed. Our DP will handle 0.  

**One more pitfall:** When we do `new_odd.add((v, v))`, we are adding the singleton. But note that this is added to `new_odd` after copying. This is correct. However, we also need to consider that we can take v as the first element, and then later take more. That's handled because we add (v, v) to odd, and then when we process the next elements, we can take from odd.  

**What about the empty subsequence?** We never add it, so we are safe.  

**Complexity analysis:**  
- Number of sums: from -1800 to 1800, so ~3600.  
- For each sum, number of products: at most the number of distinct products of subsets yielding that sum. In worst case, if we have many 1's, for a fixed product P, we can have many sums. So the total number of pairs is bounded by the number of subsets with product ≤ limit. As argued, it's manageable.  
- The inner loop: for each v, we iterate over all pairs in even and odd. The total number of pair updates is O(n * M). M is the average size of the sets. With M up to 100,000, n=150, that's 15 million iterations. Each iteration does a multiplication and a set insert. Should be okay in Python.  

**Alternative optimization:** Since product can be 0, we can treat 0 as a special case: once product is 0, it stays 0. So we can store product 0 separately. But not necessary.  

**Let's code it up.**  

We need to write the solution in the given format.  

One more thing: The problem says "subsequence" not "subset". Our DP processes in order, so it correctly considers subsequences.  

**Final check on the alternating sum definition:** "The alternating sum of a 0-indexed array is defined as the sum of the elements at even indices minus the sum of the elements at odd indices." So for a subsequence, we consider its own indices. Our DP uses parity to track whether the next element added will be at an even or odd index in the subsequence. Starting with no elements, the first element we add is at index 0 (even), so it adds +v. The second is at index 1 (odd), adds -v. So from even parity (length even), adding an element makes it odd, and the new element is at an even index? Wait: if we have a subsequence of even length L, its indices are 0..L-1. The last index is L-1 (odd). Adding a new element makes it length L+1, index L (even). So the new element is at an even index, so it adds +v. So from even parity, we add +v. From odd parity (length odd), last index is even, adding new element at index L (odd) adds -v. So our transitions: even -> odd with +v, odd -> even with -v. That's what we have. Correct.  

**One more check:** When we add a singleton, it has length 1 (odd), so it goes to odd. The sum is +v. Correct.  

**Implementation details:**  
- Use `defaultdict(set)` for `even` and `odd`.  
- When copying, we can do `new_even = {k: v.copy() for k, v in even.items()}` or use `copy.deepcopy`? No, we can just create a new defaultdict and then add to it. But we need to start with the old states (skip). So we can do: `new_even = defaultdict(set, {k: set(v) for k, v in even.items()})` but that's slow. Better: we can iterate over even and odd and add to new dicts as we go. Actually, we can avoid copying the sets if we build new dicts from scratch and include the old states. So:  
  - Initialize `new_even = defaultdict(set)` and `new_odd = defaultdict(set)`.  
  - First, add all existing states (skip): for each (s, p_set) in even.items(): for p in p_set: new_even[s].add(p)  
  - Similarly for odd.  
  - Then add transitions and singleton.  
This is O(M) to copy, plus O(M) to add transitions. So total O(M) per element. That's fine.  

We can write it as:  
```python
from collections import defaultdict

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        even = defaultdict(set)  # sum -> set of products
        odd = defaultdict(set)
        
        for v in nums:
            new_even = defaultdict(set)
            new_odd = defaultdict(set)
            
            # Copy existing states (skip)
            for s, p_set in even.items():
                for p in p_set:
                    new_even[s].add(p)
            for s, p_set in odd.items():
                for p in p_set:
                    new_odd[s].add(p)
            
            # Add singleton (start new subsequence with v)
            if v <= limit:
                new_odd[v].add(v)
            
            # Transitions from even to odd (take v)
            for s, p_set in even.items():
                for p in p_set:
                    new_p = p * v
                    if new_p <= limit:
                        new_odd[s + v].add(new_p)
            
            # Transitions from odd to even (take v)
            for s, p_set in odd.items():
                for p in p_set:
                    new_p = p * v
                    if new_p <= limit:
                        new_even[s - v].add(new_p)
            
            even = new_even
            odd = new_odd
        
        ans = -1
        if k in odd:
            ans = max(ans, max(odd[k]))
        if k in even:
            ans = max(ans, max(even[k]))
        return ans
```
This should work.  

**Potential optimization:** We can combine the copy and transition loops to avoid double iteration. For example, we can start with new_even and new_odd as copies, then add transitions. But we need to be careful: if we iterate over even and add to new_even, then also iterate over even to add to new_odd, we are doing two passes. We can do one pass: for each (s, p) in even, add (s, p) to new_even, and also add (s+v, p*v) to new_odd. That saves one pass. Let's do that.  

Revised:  
```python
for v in nums:
    new_even = defaultdict(set)
    new_odd = defaultdict(set)
    
    # Add singleton
    if v <= limit:
        new_odd[v].add(v)
    
    # Process even states
    for s, p_set in even.items():
        for p in p_set:
            # Keep (skip)
            new_even[s].add(p)

## worker: Implement the solution in Python using the set-of-
The solution uses dynamic programming over the array, tracking reachable (alternating sum, product) pairs for subsequences of even and odd length separately. For each number `v`, we consider two options: skip it (keep existing states) or take it (flip parity and update sum/product). We also handle starting a new subsequence with just `v`. Products exceeding `limit` are discarded since they can never become valid again (all numbers are non‑negative). The state space is bounded because `limit ≤ 5000` and the alternating sum range is roughly `[-1800, 1800]`, keeping the total number of reachable pairs manageable (worst case around a few hundred thousand). This approach correctly handles the non‑empty requirement by never seeding the empty subsequence.

## worker: Implement the solution in Python using the set-of-
The solution uses dynamic programming over the array, tracking reachable (alternating sum, product) pairs for subsequences of even and odd length separately. For each number `v`, we consider two options: skip it (keep existing states) or take it (flip parity and update sum/product). We also handle starting a new subsequence with just `v`. Products exceeding `limit` are discarded since they can never become valid again (all numbers are non‑negative). The state space is bounded because `limit ≤ 5000` and the alternating sum range is roughly `[-1800, 1800]`, keeping the total number of reachable pairs manageable (worst case around a few hundred thousand). This approach correctly handles the non‑empty requirement by never seeding the empty subsequence.
