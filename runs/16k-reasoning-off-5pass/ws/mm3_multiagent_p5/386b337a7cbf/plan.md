We need to choose a non-empty subsequence (any subset preserving order? "subsequence" implies order-preserving; we will treat it as order-preserving). The alternating sum is computed on the subsequence in its selected order: a0 - a1 + a2 - a3 + ... . The product must be ≤ limit, and we want to maximize it. If none, return -1.

Constraints: n ≤ 150, each nums[i] ≤ 12, k up to 1e5 (but values small), limit ≤ 5000.

Observation: each element is non-negative (0..12). Product is 0 if any zero is included; we can just consider 0 as a possible answer (product = 0) but usually we want positive product. Since all numbers are ≥ 0, any positive product comes from selecting only positive numbers. The product is bounded by 5000 and each factor ≤ 12, so subsequence length with positive product ≤ log_1(5000) roughly 5-6 if we use 12s. However we might include many small numbers (like 1) which don't change product. Including 1 is safe and can be used to adjust the alternating sum without affecting product.

We can DP over the array, tracking (alternating_sum, product) possibilities using a set of states. n=150, limit=5000, product space is up to 5000 (since 0 also possible). Alternating sum range: each element up to 12, n=150, max sum magnitude = 12*150 = 1800, but k can be up to 1e5. However we only need sums that could equal k; we can cap the range to a manageable window, e.g., [-1800, 1800], or shift to non-negative offsets.

We'll use DP as a 2D boolean array: dp[sum_offset][p] = True if we can achieve alternating sum = sum and product = p after processing some prefix. We'll also keep predecessor info to reconstruct one solution for debugging (not required for answer). Initialize dp[0][1] = True (empty subsequence) with alternating sum 0 and product 1. Actually empty not allowed, but we can ignore it later.

Transition: for each number x at index i (0-indexed), we consider it as the next element in the subsequence. If we take it, its position in subsequence is current length L. If L is even, the contribution to alternating sum is +x; if odd, -x.

We need to know parity of subsequence length for each state. We can extend dp to include parity dimension: dp[parity][sum][p]. Parity 0 = even length, parity 1 = odd length. Start with parity=0, sum=0, p=1 (empty). After processing each element, we can either skip (carry forward) or take it, flipping parity and updating sum and product (if product*x <= limit, or if x==0 product stays 0).

Product 0: if we multiply by 0, product becomes 0. For product 0, sum can be anything (since adding zeros doesn't affect product). But we can treat product=0 as a valid state with any sum.

We need to find max p ≤ limit such that there exists sum k (within range) and any parity (length >0) reachable.

Complexities: dp array size 2 * (2*MAX_SUM+1) * (limit+1). MAX_SUM=1800, limit=5000 => 2*3601*5001 ≈ 36 million booleans, too big (36M*1 byte=36MB, maybe okay in Python with bitset? but Python bools are 28 bytes). Need optimization.

Better: Use dict/set of states per parity. Number of reachable (sum,product) pairs is limited because product ≤ 5000 and values are small. Each x ≤ 12, product values will be many but bounded. Complexity: each step we iterate over current states; worst-case states could be O(SUM_RANGE * limit) but practically much smaller. n=150, each step we combine; could be up to ~limit * (range of sum) ~ 5000*3600=18M, too big.

We need smarter DP. Since n ≤ 150, limit ≤ 5000, we can use DP on product dimension: for each product, keep reachable sums with parity. That's similar size. But maybe we can use meet-in-the-middle: split array into two halves (≤75 each). Enumerate all subsequences of each half, compute (sum, parity, product). For each half, group by product, keep best (max sum?) But we need exact sum k after combining halves.

Alternatively, we can treat it as a knapsack-like DP: dp[product] = set of (sum, parity) reachable. Start with dp[1] = {(0,0)}. For each x, we create new dp2: for each p, for each (s,par) in dp[p], if p*x ≤ limit, we add to dp2[p*x] the state (s + x if par==0 else s - x, 1-par). Also we can keep p unchanged (skip). Complexity: number of distinct products is at most 5000, each holds a set of (sum,parity) states. Sum range limited to ±1800. Parity only 2. So each product could hold at most 2*(2*1800+1) ≈ 7200 states. So total states ≤ 5000*7200=36M, still high but maybe okay with pruning because many products won't appear.

But we can compress sum offset: use integer offset = sum + SHIFT, where SHIFT = MAX_SUM. So store as bitmask per product? Each product can have a 2 * (2*MAX_SUM+1) bitmask. That's 2*3601 ≈ 7202 bits per product, about 900 bytes. For 5000 products, 4.5MB, acceptable. Use Python integers as bitsets; shift bits.

We'll use two bitmask arrays for parity 0 and 1: dp0[p] and dp1[p] as Python ints where bit i is set if sum = i - SHIFT reachable with that parity and product p. SHIFT = MAX_SUM. Initialize dp0[1] = 1 << SHIFT (sum 0, parity even). Others zero.

For each x in nums:
- newdp0 and newdp1 as copies of dp0, dp1 (skip case).
- For each product p that is reachable (i.e., dp0[p]!=0 or dp1[p]!=0):
   - newp = p * x
   - if newp <= limit:
       - For parity 0 (even length) we can append x to make parity 1 (odd). New sum = old_sum + x.
         For each sum s where dp0[p] has bit s, we set bit (s+x) in newdp1[newp].
       - For parity 1 (odd length) we can append x to make parity 0 (even). New sum = old_sum - x.
         For each sum s where dp1[p] has bit s, we set bit (s-x) in newdp0[newp].
   - Special case x==0: product becomes 0. newp = 0. For product 0, sum unchanged? Actually adding a zero changes length and alternating sum: if we add zero at even position, sum +0; at odd position, sum -0 = same. So sum doesn't change. Parity flips. So we handle x=0 similarly: newp = 0 (any p*x=0). But we must also consider that product 0 can be reached from any p>0 by multiplying by 0. We'll treat product 0 specially: we can have a dedicated dp for product 0 that accumulates any sum (since zeros don't affect sum). Actually we can keep dp0[0] and dp1[0] as bitmasks as well.

But careful: product can become 0 if we include a zero. After that, further multiplications keep product 0. So dp0[0] and dp1[0] can accumulate any sum reachable by subsequences that contain at least one zero. Since zeros don't change product, we can treat product 0 as absorbing state: once we have product 0, we can still add more elements (any numbers) and product stays 0. So we need to propagate from p=0 as well.

Implementation approach: Use arrays of size limit+1 (0..limit) of Python ints for parity 0 and 1. Initialize dp0[1] = 1 << SHIFT.

For each x:
   - Create new arrays new0, new1 as copies (new0 = dp0[:], new1 = dp1[:]).
   - For p from 0 to limit:
        if dp0[p] != 0 or dp1[p] != 0:
            newp = p * x
            if newp > limit: continue
            if x == 0:
                # sum unchanged, parity flips
                # from parity 0 to 1
                new1[newp] |= dp0[p]
                # from parity 1 to 0
                new0[newp] |= dp1[p]
            else:
                if p == 0:
                    # current product already 0, adding x keeps product 0, sum += x if even parity, -x if odd
                    # from parity 0 to 1: new1[0] |= (dp0[0] shifted by +x)
                    new1[newp] |= (dp0[p] << x) if x>0 else dp0[p]  # but x>=1 here
                    # from parity 1 to 0: new0[0] |= (dp1[0] shifted by -x) i.e. >> x
                    new0[newp] |= (dp1[p] >> x) if x>0 else dp1[p]
                else:
                    # normal case
                    # parity 0 -> 1: shift left by x
                    new1[newp] |= dp0[p] << x
                    # parity 1 -> 0: shift right by x
                    new0[newp] |= dp1[p] >> x
   - dp0, dp1 = new0, new1

Shift operations must be within the bit range of sum offset. We'll define total bits = 2*SHIFT+1 = 2*MAX_SUM+1. MAX_SUM = n*12 = 1800, so bits = 3601. SHIFT = 1800. So bit index i corresponds to sum = i - SHIFT. To shift left by x (increase sum by x), we shift left by x. To shift right by x (decrease sum by x), shift right by x. However we must mask to keep bits within range. We can predefine a mask = (1 << (2*SHIFT+1)) - 1. After shifting, do & mask.

Edge Cases: x can be up to 12, sum shift is safe.

After processing all numbers, we need to find max product p (0..limit) such that there is a reachable state with sum = k (i.e., bit at index k+SHIFT set) in either parity (i.e., dp0[p] or dp1[p]) AND the subsequence is non-empty. Empty subsequence is sum=0, product=1, parity even. We need to exclude that. Since k is target, if k==0 and limit>=1, the empty subsequence also has sum 0, but we need non-empty. So we must ensure we don't pick product=1 with sum=0 from empty only. However if there is any non-empty subsequence achieving sum k and product 1, it's valid. We can just check for p where dp0[p] or dp1[p] has the bit set, and p>0 or p==0 (zero product). But we must exclude the case where the only way to reach (k,1) is empty subsequence. Since empty has parity even (0) and sum 0, product 1. If k==0, we need to ensure there is some path with length>0. To handle, we can keep a separate flag or simply ignore product=1 sum=0 from empty by requiring that there is at least one transition. Since we initialize dp0[1] with sum=0, that state is present. If after processing all elements we still only have that state (no other added), then p=1 sum=0 parity even will be set, but we shouldn't return 1 unless there is a non-empty subsequence. So we need to ensure at least one element taken. We can check: if target bit set in any state that came from a non-empty subsequence. Since we never remove states, we can mark empty state separately. Simpler: we can start dp with no states (empty not allowed), and handle subsequences of length 1+ directly. But we need base for transitions. So we can keep empty state but when checking final answer, we exclude p==1 and sum==0 and parity==0 if that state was only reachable via empty path. But if there is any non-empty subsequence achieving sum 0 product 1 (e.g., [1,-1]? but numbers are non-negative, product 1 means all 1s, e.g., [1,1] has sum 1-1=0, product 1). That's valid. So we need to allow that. The issue is only when answer would be 1 with k=0 and no non-empty subsequence. But we can just return -1 if the only reachable state for (k, p) is the initial empty one. How to detect? We can keep a set of (p,sum,parity) that are reachable via non-empty subsequences. We can start dp with empty state but mark it as "empty". Then when we transition, we mark new states as "non-empty". Then when checking answer, we only consider non-empty states.

Simpler: we can initialize dp with empty state but keep a separate boolean array nonempty[p] for each product indicating if there exists a non-empty subsequence with that product. However nonempty could depend on sum/parity. We can just store a set of (p,sum,parity) for non-empty states, and after DP, check if any non-empty state matches (k,p). Since total states manageable, we can use a dict or bitset with extra info. But we can also just after DP, if the found state includes empty (only initial), we skip. Since the only way to have product=1 sum=0 parity even from empty is if we never added any element that could produce same state. But many transitions could also produce sum=0 product=1 (e.g., [1,1] product 1 sum 0). That will be added as non-empty. So the presence of that state does not guarantee non-empty. However we can treat the state as non-empty if it was ever updated after initialization. We can keep a separate bitmask for each product that indicates reachable states, but we also keep a flag that any transition contributed to that product. Actually we can keep a bitset for reachable states, and also a bitset for "reachable via non-empty". We can propagate: new states from transitions are non-empty; we can OR them into both reachable and non-empty bitsets. The initial empty state is only in reachable, not in non-empty. Then when checking answer, we require the state to be present in non-empty bitset.

Implementation: maintain two sets of bitmask arrays: dp0_reachable, dp1_reachable (as before). And dp0_nonempty, dp1_nonempty. Initialize reachable as before (dp0[1] has sum 0). nonempty arrays all zero. In transition, when we compute new bits from old reachable bits, we also add those bits to the new nonempty bits (because they came from taking element). For skip case (copying), the nonempty status carries over: if old state was nonempty, new state is also nonempty. So we can do: new_nonempty0 = dp0_nonempty[:], new_nonempty1 = dp1_nonempty[:]; then for each transition, we set bits in new_nonempty accordingly.

But we also need to handle product 0 case: initial reachable for product 0 is zero, nonempty also zero. When we multiply by 0, we get new product 0. The new states should be marked nonempty (since we took a zero). So in transition for x==0, we OR into new_nonempty arrays.

Also for p=0 and x>0, we propagate from dp0[0] to new1[0] (shifted) and mark nonempty if old state was nonempty (or if we are taking element, we mark nonempty). Actually if we have a subsequence that already has product 0 (contains a zero) and we add another element, the resulting subsequence is non-empty (it already was). So the new state should be nonempty if the old state was nonempty. So we can simply propagate nonempty bits similarly: new_nonempty1[newp] |= (dp0_nonempty[p] << x) etc. And also if we are adding element to an empty subsequence? That can't happen because empty has product 1, not 0. So fine.

Thus we can implement DP with reachable and nonempty bitsets.

After processing all numbers, we scan p from limit down to 0 (largest product first) to find max p where (dp0_nonempty[p] | dp1_nonempty[p]) has bit (k+SHIFT) set. If found, return p. Else return -1.

Complexity: O(n * limit * (bits/wordsize?)). Each transition we iterate over p from 0..limit. That's 150*5000 = 750k iterations. In each iteration we do a few bitwise operations on Python ints (big integers of ~3600 bits). That's okay. However we need to compute shift left/right which is O(bits) in Python (big int shift). 750k * 3600 bits ≈ 2.7 billion bit operations, maybe heavy but still possibly okay in Python? 750k shifts of big ints of size ~450 bytes each (3600 bits = 450 bytes). Shifting a Python int of that size is O(size) ~ O(number of machine words). 3600 bits = 56 64-bit words. So each shift is ~56 operations. 750k * 56 ≈ 42 million word operations, plus OR, etc. Might be borderline but likely okay for n=150, limit=5000. However we also have nested loops for p and transitions for each x. Actually for each x we iterate over all p. That's 150*5000 = 750k. For each p we compute newp = p*x, and if newp <= limit, we perform shifts and ORs. That's fine.

But we also need to handle x=0 separately. For x=0, newp = 0, always <= limit. So for all p where reachable, we will do transitions. That's 5000 per x=0. There may be many zeros, but nums[i] <=12, could be many zeros. Still okay.

Thus the DP is feasible.

One nuance: shift left by x may exceed bit range. We need to mask to keep bits within [0, 2*SHIFT]. So after shift, do & MASK.

Similarly shift right may drop bits; it's fine.

Edge Cases: SHIFT = MAX_SUM = n*12 = 1800. But after processing all elements, the maximum absolute sum could be less, but we allocated for max possible. That's fine.

But we need to be careful: when we shift left by x, bits may overflow beyond the allocated range; we mask them away. When we shift right by x, bits may become negative indices (i.e., sum less than -SHIFT). That's okay because shifting right discards lower bits.

Now we need to implement the DP in a class method.

Implementation Steps:

1. Compute n = len(nums). Compute MAX_SUM = n * 12. SHIFT = MAX_SUM. BITS = 2*SHIFT + 1. MASK = (1 << BITS) - 1.

2. Initialize arrays dp0 = [0] * (limit+1), dp1 = [0] * (limit+1). Similarly ndp0_non = [0] * (limit+1), ndp1_non = [0] * (limit+1). Actually we need nonempty bitsets: dp0_non, dp1_non.

   dp0[1] = 1 << SHIFT   # sum 0
   # nonempty arrays are all zero initially.

3. For each x in nums:
   - new0 = dp0[:]; new1 = dp1[:]
   - new0_non = dp0_non[:]; new1_non = dp1_non[:]
   - For p in range(limit+1):
        if dp0[p] == 0 and dp1[p] == 0:
            continue
        # compute new product
        newp = p * x
        if newp > limit:
            continue
        if x == 0:
            # from even to odd: new1[newp] |= dp0[p]
            new1[newp] |= dp0[p]
            new1_non[newp] |= dp0[p]  # adding zero makes nonempty if old state was reachable (but old state might be empty? However p=0 reachable only via zero, so old state is nonempty. If p>0 and dp0[p] reachable, could be from empty? No empty only product 1. So safe.)
            # from odd to even: new0[newp] |= dp1[p]
            new0[newp] |= dp1[p]
            new0_non[newp] |= dp1[p]
        else:
            # from even to odd: shift left by x
            shifted = (dp0[p] << x) & MASK
            new1[newp] |= shifted
            new1_non[newp] |= shifted
            # from odd to even: shift right by x
            shifted = dp1[p] >> x
            new0[newp] |= shifted
            new0_non[newp] |= shifted
   - dp0, dp1 = new0, new1
   - dp0_non, dp1_non = new0_non, new1_non

But careful: When p=0 and x>0, newp = 0. So we need to handle that case. For p=0, dp0[0] or dp1[0] may be non-zero (states with product 0). We need to apply transitions: adding x to a zero-product subsequence keeps product 0, sum changes by +x (if parity even) or -x (if parity odd). So the above code works: newp = 0, shift left/right accordingly.

But we also need to consider that when p>0 and x=0, newp = 0, we handled.

Now, for x>0 and p>0, newp = p*x. Since p <= limit and x <= 12, newp may exceed limit, we skip.

Potential optimization: precompute list of p where dp0[p] or dp1[p] non-zero to avoid scanning all limit+1 each iteration. But scanning 5000 is fine.

Now after processing all numbers, we look for answer:

target_bit = 1 << (k + SHIFT)   (if within [0, BITS-1]; else impossible, return -1)
If k+SHIFT < 0 or >= BITS, return -1.

Then for p in range(limit, -1, -1):
    if (dp0_non[p] | dp1_non[p]) & target_bit:
        return p

If none, return -1.

Edge Cases:
- k may be outside possible sum range. But we mask anyway.
- SHIFT may be large: n*12 = 1800. BITS = 3601. 1 << 3601 is huge (approx 2^3601). Python can handle big ints of that size, but memory for arrays: each element is a Python int object. For limit=5000, each int is a big integer of ~3601 bits (approx 450 bytes). So memory: 5000 * 450 bytes * 2 (reachable) * 2 (nonempty) = 5000*450*4 ≈ 9 MB per array? Actually each Python int object overhead is larger (28 bytes + digit array). 5000 ints * maybe 100 bytes = 0.5 MB. The digit array for 3601 bits is about 3601/30=120 digits (since Python uses 30-bit digits). Each digit is 30 bits stored in a C long. So memory per big int: overhead + 120*4=480 bytes. So 5000*480 ≈ 2.4 MB per array. We have 4 arrays (dp0, dp1, dp0_non, dp1_non) => ~10 MB. That's okay.

But we also create new0, new1, new0_non, new1_non each iteration (copies of arrays). That would allocate new arrays each step (150 times) => 150*4*5000 = 3 million ints, which is heavy but maybe okay memory wise temporarily? Actually each iteration we allocate new arrays of size limit+1 (5001) each containing ints. That's 4*5001 = 20004 ints per iteration. Over 150 iterations, we allocate 3 million ints. That's okay in Python? Might be a bit heavy but still within memory (each int is a big int, not just small int). Actually we can optimize by using two arrays and swapping, but we need new arrays to avoid using updated values in same iteration (since we may add multiple elements? But we are processing one element at a time, we can reuse the same arrays by iterating over p and writing to dp arrays in-place? But careful: we need to use old values for computing new states, but if we update in-place, we may use newly added states for the same element (i.e., using the element multiple times). Since we are only allowed to use each element at most once (subsequence), we must not allow using the same element multiple times in one transition. So we need to use old snapshot. So copying arrays is needed.

We can optimize memory by using list comprehension copying: new0 = dp0[:] etc. That's shallow copy of list of ints (the int objects are shared, not duplicated). So we allocate new list references, but the ints themselves are not copied. However when we do new1[newp] |= shifted, we modify the int in place (since int is immutable, but we reassign the list element to a new int). That's fine. So memory overhead is just the list of 5001 references (8 bytes each) = 40KB per array. 4 arrays = 160KB. That's trivial. The big ints are shared. So copying is cheap.

Thus DP is efficient.

Now we need to ensure that we treat the case where product 0 and sum k reachable. For p=0, we can return 0 if reachable (nonempty). But note: product 0 is allowed (limit >= 0). The problem says limit >= 1, but product 0 is less than limit. So if any subsequence with product 0 and sum k exists, answer could be 0. However, we need to maximize product. If there is a positive product also reachable with same sum, we would pick larger product. So scanning from limit downwards ensures we pick max.

Edge Cases: limit may be less than 1? Constraint says limit >= 1. So okay.

Now we need to verify with examples.

Example 1: nums=[1,2,3], k=2, limit=10.
n=3, MAX_SUM=36, SHIFT=36. BITS=73.
Initialize dp0[1] bit 36 set.
Process 1:
- p=1, dp0[1] has bit 36. x=1 => newp=1.
   from even to odd: shift left 1 => bit 37 (sum=1). new1[1] gets bit 37. nonempty.
   from odd to even: dp1[1] is 0.
dp0[1] still has bit 36 (skip).
After 1: dp0: product 1 sum 0 (even). dp1: product 1 sum 1 (odd).

Process 2:
- p=1, dp0[1] has bit 36. x=2 => newp=2.
   from even to odd: shift left 2 => bit 38 (sum=2). new1[2] gets bit 38.
   from odd to even: dp1[1] has bit 37. shift right 2 => bit 35 (sum=-1). new0[2] gets bit 35.
- Also p=1, dp1[1] has bit 37. x=2 => newp=2. from odd to even: shift right 2 => bit 35. new0[2] gets bit 35 (already). from even to odd: dp0[1] already considered.
- Also p=2? dp0[2] or dp1[2] may have bits from previous? Not yet.
- p=1, x=2 also newp=2, but we also need to consider from dp0[1] to new1[2] and from dp1[1] to new0[2].
- Also p=0? none.
- Also p=2? no.
- Also p=1, x=2, we also need to consider from dp0[1] to new1[2] (sum +2) and from dp1[1] to new0[2] (sum -2). That's correct.
- Also we need to consider p=1, dp0[1] sum 0 (even) => adding 2 at odd position => sum = -2? Wait: parity flips, even->odd, so sum += x = +2? Actually if we have subsequence of even length (so far length L even), the next element is at index L (0-indexed) which is even index in subsequence, so contribution is +x. So sum new = old_sum + x. Yes shift left.
- If we have odd length (L odd), next index is odd, contribution -x, so sum new = old_sum - x. So shift right.
- So from dp1[1] (odd length, sum=1) adding 2 => sum = 1 - 2 = -1. That's shift right 2: 1 - 2 = -1 => bit index SHIFT-1 = 35. Good.

Now after processing 2, we have:
dp0[1]: sum 0 (even)
dp0[2]: sum -1 (even) (from odd length 1)
dp1[1]: sum 1 (odd)
dp1[2]: sum 2 (odd) (from even length 0)

Process 3:
- For each p.
We want sum k=2. Let's see possible products:
- Subsequence [1,2,3] => product 6, sum 2. Should be reachable.
Let's see DP:
p=1: dp0[1] sum 0. x=3 => newp=3. from even to odd: shift left 3 => sum=3 (odd). new1[3] sum 3.
p=1: dp1[1] sum 1. x=3 => newp=3. from odd to even: shift right 3 => sum=-2 (even). new0[3] sum -2.
p=2: dp0[2] sum -1. x=3 => newp=6. from even to odd: shift left 3 => sum=2 (odd). new1[6] sum 2. Good! Product 6.
p=2: dp1[2] sum 2. x=3 => newp=6. from odd to even: shift right 3 => sum=-1 (even). new0[6] sum -1.
Also p=2 dp0[2] sum -1 to new1[6] sum 2. That's the [2,3]? Actually [2,3] sum = 2 - 3 = -1. Not 2. Wait [1,2,3] sum = 1 - 2 + 3 = 2. The path: start empty (even). Take 1 (odd) sum=1. Take 2 (even) sum = 1 - 2 = -1. Take 3 (odd) sum = -1 + 3 = 2. So after 2, dp0[2] sum -1 (even). After 3, adding 3 (odd) => sum = -1 + 3 = 2. So product = 1*2*3 = 6. So new1[6] sum 2 reachable. Good.

Now answer: target bit sum 2 => SHIFT+2 = 38. Look for p from 10 down to 0. p=6: dp0_non[6] | dp1_non[6] has bit 38? dp1[6] sum 2 (odd) reachable. So answer 6. Good.

Example 2: nums=[0,2,3], k=-5, limit=12.
We need sum -5. Let's see possible subsequences: [0,2,3] => sum = 0 - 2 + 3 = 1. Not -5. [2] => 2. [3] => 3. [0] => 0. [0,2] => 0 - 2 = -2. [0,3] => 0 - 3 = -3. [2,3] => 2 - 3 = -1. [0,2,3] => 1. So -5 not reachable. DP should return -1.

Example 3: nums=[2,2,3,3], k=0, limit=9.
Possible products: [2,2] product 4 sum 0. [3,3] product 9 sum 0. [2,2,3,3] product 36 >9. So answer 9. DP should find product 9.

Check DP: product 9 reachable? Path: take 2 (odd) sum=2. take 2 (even) sum=0. product 4. Then take 3 (odd) sum=0+3=3. product 12 > limit. So not allowed. Alternative: take 3 (odd) sum=3. take 3 (even) sum=0. product 9. That's [3,3] product 9. DP should allow that. Let's see DP: after first two 2s, product 4 sum 0. Then we have 3: p=4, dp0[4] sum 0 (even). Adding 3 (odd) => newp=12 > limit (skip). But we can also skip some 2s. For [3,3], we skip 2s. Process 3: start from empty (product 1 sum 0). Take 3 (odd) sum=3 product 3. Next 3: from dp1[3] sum 3 (odd) adding 3 (even) => sum = 3 - 3 = 0, product 9. So DP should capture that. Good.

Thus algorithm works.

Now we need to implement solve() with reading input? The problem statement is a typical LeetCode style. The class Solution with method maxProduct. We need to implement that.

Potential issues: SHIFT = n * 12 may be up to 1800, but we can also compute SHIFT = max possible sum magnitude, but we can also use a smaller bound: limit is up to 5000, product small, but sum can be large if we include many 1s? Actually 1 doesn't change product, so we could have many 1s. n=150, each up to 12, so max sum magnitude is 12*150 = 1800. So SHIFT = 1800 is safe.

But we also need to consider that product 0 can be reached with sum any value up to 1800. That's fine.

Edge Cases: limit may be less than some products, but we handle.

Now we need to consider the possibility of product exceeding limit due to multiplication by 0? Actually 0 * x = 0, always ≤ limit. So fine.

Now complexity: O(n * limit * (bits/wordsize)). bits/wordsize is about 56 (for 3600 bits). So ~150*5000*56 = 42 million operations. In Python, each shift and OR on big ints of size 56 words is maybe a few hundred nanoseconds? 42 million might be a few seconds, but might be okay. But we can try to optimize: For each x, we iterate over p where dp0[p] or dp1[p] is non-zero. Since many p may be zero (unreachable), we can maintain a list of active p. But scanning 5000 is fine.

But we also need to handle the shift left/right masking. For shift right, we don't need to mask because shifting right cannot create bits beyond range. For shift left, we need to mask to avoid bits beyond BITS. So we can do: shifted = (dp0[p] << x) & MASK.

We also need to handle the case where x=0 separately as described.

Potential micro-optimizations: Use local variables, precompute mask, etc.

Now we need to implement the class method.

Implementation details:

```python
class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        MAX_SUM = n * 12
        SHIFT = MAX_SUM
        BITS = 2 * SHIFT + 1
        MASK = (1 << BITS) - 1
        size = limit + 1
        dp0 = [0] * size
        dp1 = [0] * size
        ndp0_non = [0] * size
        ndp1_non = [0] * size
        dp0[1] = 1 << SHIFT  # sum 0, even length
        # nonempty arrays initially zero
        for x in nums: