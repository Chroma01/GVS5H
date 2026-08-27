The problem asks for the number of subsequences of size 5 where the middle element (3rd element) is the unique mode. For each index `i` (the middle element), we need to count the number of ways to choose 2 elements before `i` and 2 elements after `i` such that `nums[i]` is the unique mode. The conditions are: count of `nums[i]` in the subsequence is strictly greater than the count of any other value. Since the subsequence has 5 elements, the middle element can appear at most 2 times (itself plus one duplicate) to potentially be the unique mode (count = 2 vs 1 for others). However, if it appears 2 times, the other elements must be all distinct and different from it. If it appears 1 time, all other 4 elements must be distinct and different from it.

We can process each possible value `v` (as candidate for middle mode) by considering occurrences of `v` in the array. For each occurrence `i` of `v`:
- Count `left_total`: elements to the left of `i`.
- Count `right_total`: elements to the right of `i`.
- Count `left_same`: occurrences of `v` to the left of `i`.
- Count `right_same`: occurrences of `v` to the right of `i`.

Case 1: `nums[i]` appears once in the subsequence. We need to choose 2 from left (none equal to `v`) and 2 from right (none equal to `v`). Number of ways: `C(left_total - left_same, 2) * C(right_total - right_same, 2)`.

Case 2: `nums[i]` appears twice (once as middle, once as one of the other 4). The other duplicate of `v` can be in left or right, but not both (otherwise count would be 3, but the other count of other values would be at most 1, so 3 > 1, actually that's still valid! Wait, if count=3 and others are distinct, it's fine. But if count=3, the other 2 elements are distinct and not v. Actually, we need to be careful. If we have 3 v's, then 2 other elements. For v to be unique mode, the other 2 must be distinct and not v. But we are choosing a subsequence of size 5. The middle is v. We can have 2 more v's (one in left, one in right) or both in left or both in right. So actually we have cases where v appears 2, 3, 4, or 5 times? But the middle is v. If v appears 5 times, all elements are v. That works. But we need to count systematically.

Actually, let's think more generally. For a fixed middle position `i` and value `v = nums[i]`, we want to choose 2 elements from left and 2 from right. Let `a` be the number of chosen elements from left equal to `v`, and `b` from right equal to `v`. So `a ∈ {0,1,2}`, `b ∈ {0,1,2}`, and `a+b ≥ 0`. The total count of `v` in the subsequence is `1 + a + b`. The other elements (the `2-a` from left and `2-b` from right) must not be `v`. Moreover, all other elements in the subsequence must be distinct? Wait, no. The mode is the element with maximum frequency. If `v` appears `1+a+b` times, the other elements are `2-a + 2-b = 4 - (a+b)` elements. For `v` to be the unique mode, we need that no other value appears as many times as `v`. Since the other elements are at most 4 in count, the maximum frequency of any other value is at most `4 - (a+b)`. But they could repeat. However, if another value repeats, it would have frequency at least 2. If `v` appears 1 or 2 times, then another value repeating with frequency 2 would tie or exceed? If `v` appears 1, and another appears 2, v is not the mode. If `v` appears 2, and another appears 2, tie. So for v to be the unique mode, we need that the maximum frequency among the other elements is strictly less than `1+a+b`. But since we are picking 4 other elements, the maximum frequency among them is at least 1. So if `1+a+b = 1`, then other elements have max frequency at least 1, which is not strictly less. So v must appear at least 2 times? Wait, example 1: [1,1,1,1,1] has v=1 appearing 5 times, unique mode. Example 2: [1,2,2,3,3,4] subsequences [1,2,2,3,4] has v=2 appearing 2 times, others all distinct. [1,2,3,3,4] has v=3 appearing 2 times, others distinct. So indeed, the middle element must appear at least 2 times in the subsequence to be the unique mode? Not necessarily. What if v appears 1 time, but all other 4 elements are distinct and different from v? Then the frequencies are all 1, so v is a mode but not unique. The problem says "unique mode", so there must be exactly one element with the maximum frequency. If all frequencies are 1, then there are 5 modes, not unique. So v must appear strictly more times than any other element. That means the count of v must be at least 2 (since if it's 1, others are also at least 1). Actually, if v appears 1 time, and we have 4 other elements, if they are all distinct, we have 5 elements each appearing 1 time: 5 modes. If some other element appears 2 times, then that element has frequency 2, v has 1, so v is not the mode. If v appears 1 time and others are all v? That's impossible because v appears only 1 time total? Wait, v is the middle element. If v appears only once in the subsequence, that means we don't pick any other v. So the other 4 elements are not v. They could be all distinct, or some could repeat. In any case, the maximum frequency is at least 1. If the maximum frequency is 2 (some other element appears twice), then v is not the mode. If the maximum frequency is 1 (all distinct), then there are 5 modes, v is not the unique mode. Therefore, v must appear at least 2 times in the subsequence.

So the count of v in the subsequence must be at least 2. So `1+a+b >= 2` => `a+b >= 1`. Also, for v to be the unique mode, we need that no other value appears as many times as v. So we need to ensure that the other elements (the `4 - (a+b)` elements) do not have any value appearing `1+a+b` or more times. But since there are only `4 - (a+b)` other elements, the maximum frequency any other value can have is `4 - (a+b)`. We need `4 - (a+b) < 1 + a + b` => `4 < 1 + 2(a+b)` => `2(a+b) > 3` => `a+b > 1.5` => `a+b >= 2`. So the total number of v's in the subsequence must be at least 3? Wait, that seems too strict. Let's check example 2: [1,2,2,3,3,4]. Subsequence [1,2,2,3,4] has middle 2. v=2 appears 2 times. The other elements are 1,3,4 (all distinct). So frequencies: 2 appears 2, others appear 1. Maximum frequency among others is 1, which is less than 2. So v is the unique mode. Here `a+b = 1` (one extra 2). `1+a+b = 2`. The other elements count is 3. Their maximum frequency is 1, which is less than 2. So the condition is: for each other value, its count in the subsequence must be < count of v. So if count of v is k, then for any other value, its count must be <= k-1. Since we are only choosing 4 other elements, the total number of other elements is 4. The worst case is that all other elements are the same value. Then that value would have count 4. So we need 4 < k => k >= 5? That can't be right. Actually, we are not free to choose any other elements; we are constrained by the array. The condition is simply that in the chosen subsequence, v is the unique mode. So we need to count the number of ways to choose 2 from left and 2 from right such that in the resulting 5-element multiset, v appears the most times and strictly more than any other value.

This is a combinatorial counting problem with constraints. Since n <= 1000, we can do O(n^2) or O(n^2 log n) per value? There are up to 1000 distinct values, so O(n^3) is too slow. We need O(n^2) or similar.

Observation: For each index i as the middle, we need to count pairs (L, R) where L is a 2-element subset from left, R from right, such that the condition holds. The condition depends on the counts of values in L and R. Since n is only 1000, we can precompute for each index i, and for each possible count of how many v's are chosen from left and right, but we also need to ensure no other value ties or exceeds.

Alternative approach: For each value v, consider its occurrences. For each occurrence i of v, we want to count the number of ways to pick 2 elements from left and 2 from right such that v is the unique mode. Let's denote the chosen elements as a multiset. Let the count of v in the chosen left be a (0,1,2), and from right be b (0,1,2). The total count of v is 1+a+b. The other elements are the 2-a from left and 2-b from right. They are all not equal to v. Let the multiset of these other elements be S. We need that for every value u != v, count_S(u) < 1+a+b.

Since the subsequence size is 5, the possible (a,b) with a+b >= 1 (so v appears at least twice) are:
- (0,1), (1,0), (0,2), (2,0), (1,1), (0,3? no b max 2), (2,1), (1,2), (2,2). But a and b are at most 2. So (a,b) can be:
(0,1), (1,0), (0,2), (2,0), (1,1), (1,2), (2,1), (2,2). But also a+b can be 3,4,5? Actually if a=2, b=2, total v=5. That's allowed. If a=2, b=1, total v=4. If a=2, b=0, total v=3. If a=1, b=1, total v=3. If a=1, b=0, total v=2. If a=0, b=1, total v=2. If a=0, b=2, total v=3. If a=1, b=2, total v=4. So v can appear 2,3,4,5 times. For each case, the other elements count is 4 - (a+b). For v to be unique mode, we need that among the other elements, no value appears as many times as v. So if v appears k times, the other elements are 5-k elements. They must not contain any value with frequency >= k. Since the other elements are 5-k in number, the maximum frequency any value can have is 5-k. So we need 5-k < k => k > 2.5 => k >= 3. Wait, if k=2, then other elements are 3. They could have a value appearing 2 times? But 2 is not less than 2, it's equal. So if k=2, we need all other elements to be distinct and not v, and also no other value appears twice. So the other 3 elements must be all distinct. So for k=2, the other elements must be 3 distinct values. For k=3, other elements are 2. They could be both the same value? If both are the same, that value has count 2, which is less than 3, so that's fine. So for k=3, the other 2 elements just need to not be v, but they can be equal to each other. For k=4, other element is 1, so no restriction. For k=5, no other elements.

So the conditions per (a,b) are:
- a+b = 1: k=2. Other elements: 3 elements, all not v, and all distinct. So we need to choose 2 from left, 1 from right (or 1 left, 2 right) such that the 3 non-v elements are all distinct.
- a+b = 2: k=3. Other elements: 2 elements, not v, but they can be same or different. So just need them to be not v.
- a+b = 3: k=4. Other element: 1 element, not v.
- a+b = 4: k=5. No other elements.

But wait, for a+b=2, if the two other elements are the same, that value appears twice, and v appears 3 times, so v is unique mode. That's fine. So the condition is simply that the other elements are not v, and for k=2, they must be all distinct.

Now, we need to count for each i (middle index of value v), the number of ways to pick left and right elements satisfying these conditions. We can precompute for each i, the number of v's to the left and right, and also the number of ways to pick left and right with certain properties regarding distinctness.

Since n is 1000, we can do O(n^2) per value? There are at most 1000 values, so O(n^3) is too slow. But we can do O(n^2) total if we are careful.

Another approach: For each i as middle, we can compute the number of valid (L,R) pairs. Let left array be indices 0..i-1, right array be i+1..n-1. We need to count pairs (L,R) where L is a 2-element subset of left, R is a 2-element subset of right, and the conditions hold.

We can compute for each i, the following:
- total left = i
- total right = n-1-i
- left_v = number of v in left
- right_v = number of v in right

We can compute the number of ways to choose L and R with given number of v's. But we also need to handle the distinctness condition for k=2.

Let's break down by a and b (number of v's chosen from left and right respectively).

For a fixed i, let L be the set of left indices. We choose a elements from L that are v, and (2-a) elements from L that are not v. Similarly for right.

Let:
- left_v = L_v
- left_nv = i - L_v  (non-v elements in left)
- right_v = R_v
- right_nv = n-1-i - R_v

Number of ways to choose a v's and 2-a non-v's from left: C(L_v, a) * C(left_nv, 2-a). Similarly for right: C(R_v, b) * C(right_nv, 2-b).

So for each (a,b) with a+b >= 1, the number of ways to pick the required counts is:
Ways(a,b) = C(L_v, a) * C(left_nv, 2-a) * C(R_v, b) * C(right_nv, 2-b).

But we have the additional condition: for k=2 (a+b=1), the 3 non-v elements must be all distinct. So we cannot just count any choice; we need to subtract the choices where among the 3 non-v elements (which are (2-a) from left and (2-b) from right, total 3 elements), there is a duplicate value. Since they are from left and right, duplicates can occur if we pick the same value from left and right, or if we pick two of the same from left (if a=0, we pick 2 non-v from left; if a=1, we pick 1 non-v from left; if a=0, b=1, we pick 2 non-v from left and 1 non-v from right, etc.). So we need to count only those choices where the 3 non-v elements are all distinct.

Similarly, for k=3 (a+b=2), the 2 non-v elements just need to be not v. They can be the same. So no additional condition.

For k=4 (a+b=3), 1 non-v element, no condition.
For k=5 (a+b=4), 0 non-v elements, no condition.

So the only tricky part is the k=2 case, where we need the 3 non-v elements to be all distinct.

Let's list the (a,b) for k=2:
- (a,b) = (0,1): left: 0 v, 2 non-v; right: 1 v, 1 non-v. Total non-v: 3 elements: 2 from left, 1 from right. They must be all distinct. So we need to choose 2 distinct non-v from left, and 1 non-v from right, such that the right one is different from both left ones.
- (1,0): symmetric: 1 non-v from left, 2 non-v from right, all distinct.
- (0,0) would be k=1, not allowed.
- (0,2) is k=3.
- (2,0) is k=3.

So only (0,1) and (1,0) are k=2 cases that need the distinctness condition. What about (0,0) and a=0,b=0? That's k=1, not allowed.

What about (a,b) = (0,1) and (1,0) are the only ones with a+b=1. So for these two cases, we need to count the number of ways to choose the non-v elements with all distinct.

Now, for each i, we need to compute:
1. For (a,b) = (0,1): C(L_v, 0)*C(left_nv, 2) * C(R_v, 1)*C(right_nv, 1) but with the condition that the two non-v from left and the one non-v from right are all distinct.
2. Similarly for (1,0).
3. For other (a,b) with a+b >= 2, we can just use the product of combinations.

But we need to compute for each i. Since n=1000, we can precompute for each i and for each value, but we need to know the counts of non-v elements. However, the distinctness condition depends on the specific values chosen, not just counts. So we need to know for each pair of positions, the value.

This suggests a different approach: Since n is only 1000, we can for each value v, process its occurrences. For each occurrence i, we can look at the left and right sides. The number of ways to choose 2 from left and 2 from right is O(n^2) per i, leading to O(n^3) total. That's 10^9, too slow.

We need an O(n^2) algorithm. Perhaps we can fix the middle i, and compute the number of valid pairs (l1, l2, r1, r2) with l1 < l2 < i < r1 < r2. We can do this by iterating over the left pair and right pair? Still O(n^3).

Alternative: For each i, we can compute the number of ways to choose left elements with certain properties. For example, we can compute for each i, the number of ways to choose a pair from left that are both not v and distinct, etc. But the distinctness condition involves cross-side distinctness for the k=2 case.

Let's think about the k=2 case more carefully. For (a,b)=(0,1), we choose 2 from left (both not v) and 1 from right (not v), and these 3 must be all distinct. So we need to count the number of triples (l1, l2, r1) with l1<l2<i<r1, such that nums[l1] != v, nums[l2] != v, nums[r1] != v, and all three values are distinct. Similarly for (1,0): choose 1 from left, 2 from right, all distinct.

We can compute this for each i by knowing the frequency of each value in the prefix and suffix. Since n=1000, we can precompute for each i, the frequency map of the left part and right part. But the values can be up to 10^9, so we need to compress them.

For each i, we can compute:
- For the left side, we have the counts of each value.
- For the right side, similarly.

We want to count the number of ways to pick 2 from left (not v) and 1 from right (not v) with all distinct. Let A be the set of values in left excluding v, B be the set in right excluding v. We want to count the number of pairs (x,y) from left with x!=y, and z from right, such that x,y,z are all distinct.

Number of ways = sum over x != y in left: count_left(x) * count_left(y) * sum_{z != x, z != y} count_right(z).

This is equal to:
Let S = total ways to pick 2 from left not v: C(left_nv, 2).
Let T = total ways to pick 1 from right not v: right_nv.
We want to subtract the cases where the right element equals one of the left elements.
So Ways = S * T - sum_{x} (number of left pairs that contain x) * count_right(x).

Number of left pairs that contain x: count_left(x) * (left_nv - count_left(x)). But careful: we are picking 2 from left, both not v. So the number of pairs where one of them is x is count_left(x) * (left_nv - count_left(x)) because we pick x and another element that is not v and not x? Actually, if we pick two elements from left that are not v, the number of pairs that include a specific element with value x is: we choose one occurrence of x, and the other element can be any of the left_nv - count_left(x) elements that are not v and not x? But wait, the other element could also be x? That would be a pair of two x's. That is allowed in the pair? Yes, a pair of two x's is a valid pair from left. So the number of pairs that contain at least one x is: pairs with exactly one x: count_left(x) * (left_nv - count_left(x)) + pairs with two x's: C(count_left(x), 2). So total pairs containing x: count_left(x) * left_nv - C(count_left(x), 2). Alternatively, we can think: total left pairs = C(left_nv, 2). Pairs not containing x = C(left_nv - count_left(x), 2). So pairs containing x = C(left_nv, 2) - C(left_nv - count_left(x), 2). But that's more complicated.

Simpler: For each value u, let L_u = count of u in left (excluding v if u=v, but we already excluded v). Let R_u = count of u in right (excluding v). Then the number of ways to choose 2 from left and 1 from right with all distinct is:
Sum_{u != w} L_u * L_w * (right_nv - R_u - R_w)   (for left pair u,w and right z not u or w)
+ Sum_{u} C(L_u, 2) * (right_nv - R_u)            (for left pair both u, right not u)

But this is O(n^2) per i if we sum over all u,w. Too slow.

We can compute it as:
Total = C(left_nv, 2) * right_nv - Sum_{u} (number of left pairs containing u) * R_u.
And number of left pairs containing u = L_u * (left_nv - 1) - C(L_u, 2)? Let's derive:
Number of left pairs containing at least one u: choose one u and one other from left not v: L_u * (left_nv - L_u) (for one u and one not u) + C(L_u, 2) (for two u's). So total = L_u * (left_nv - L_u) + L_u*(L_u-1)/2 = L_u * left_nv - L_u^2 + (L_u^2 - L_u)/2 = L_u * left_nv - L_u^2/2 - L_u/2 = L_u * left_nv - L_u*(L_u+1)/2.
Alternatively, we can use: number of pairs containing u = total pairs - pairs not containing u = C(left_nv, 2) - C(left_nv - L_u, 2).
But maybe we can precompute for each i, the sum over u of R_u * something. Since n=1000, we can for each i, iterate over all possible values u in the union of left and right, and compute L_u and R_u. The number of distinct values is at most n, so per i we can do O(n) work. Then over all i, O(n^2) = 10^6, which is fine.

So algorithm for each i:
1. Compute left_nv, right_nv, and for each value u, L_u, R_u.
2. For the (0,1) case: compute S_left = C(left_nv, 2), T_right = right_nv. Then compute Sum_{u} (pairs_containing_u) * R_u. Then valid_ways_01 = S_left * T_right - Sum.
3. Similarly for (1,0): valid_ways_10 = left_nv * C(right_nv, 2) - Sum_{u} (pairs_containing_u_in_right) * L_u, where pairs_containing_u_in_right = R_u * right_nv - R_u*(R_u+1)/2.
4. For other (a,b) with a+b >= 2, we can compute using combinations of L_v, left_nv, R_v, right_nv. Specifically:
   For each a in {0,1,2}, b in {0,1,2} with a+b >= 2:
   ways = C(L_v, a) * C(left_nv, 2-a) * C(R_v, b) * C(right_nv, 2-b)
   but we must ensure that for a+b=2, we don't need the distinctness condition (since k=3, the two non-v can be same). So we just multiply.
5. Sum over all a,b, and over all i.

But wait: for a+b=2, we have cases (0,2), (2,0), (1,1). For (0,2): left picks 0 v, 2 non-v; right picks 2 v, 0 non-v. The two non-v from left can be any (including same). So no condition. Similarly (2,0). For (1,1): left picks 1 v, 1 non-v; right picks 1 v, 1 non-v. The two non-v can be same, no condition.
For a+b=3: (2,1), (1,2), (3,0?) no, max 2 each. So (2,1) and (1,2). Also (0,3) not possible. So (2,1): left 2 v, 0 non-v; right 1 v, 1 non-v. The one non-v from right is free. (1,2): symmetric.
For a+b=4: (2,2): all v, no non-v. Ways = C(L_v, 2) * C(R_v, 2).

So for each i, we can compute:
- L_v = count of v in left
- left_nv = i - L_v
- R_v = count of v in right
- right_nv = n-1-i - R_v

Precompute factorials up to 1000 for combinations.

Now, the (0,1) and (1,0) cases need the distinctness calculation. For (0,1):
We need to choose 2 from left (not v) and 1 from right (not v), all distinct.
As derived: total_left_pairs = C(left_nv, 2)
total_right_single = right_nv
Subtract the cases where the right element equals one of the left elements.
For each value u, the number of left pairs that contain u is:
L_u * (left_nv - 1) - C(L_u, 2)? Let's recalc carefully.
Left pairs are unordered pairs of two indices from left, both not v. Let the values of these two indices be x and y. We want the number of pairs where x = u (or y = u). This is the number of ways to choose one index with value u from left, and another index from left with value != v (and could be u again? If we choose two indices both with value u, then that pair contains u twice. But in that case, the right element being u would be equal to both, but we just need that the right element equals u, which is already true. So we need to count all pairs that have at least one u. So for a fixed value u, the number of pairs (i,j) from left not v such that at least one of them has value u:
= (number of ways to choose one index with value u and one index with any value not v) - (overcount when both are u? Actually, if we choose one index with value u and one index with any value not v, we are counting pairs where one is u and the other is not u. If both are u, that is also a valid pair containing u. So the total number of pairs containing u is:
= C(L_u, 2) (both u) + L_u * (left_nv - L_u) (one u, one not u) = L_u * left_nv - C(L_u, 2).
Yes, because L_u * left_nv counts each pair with one u and one other (not v) L_u times for the first u, but if the other is also u, it gets counted multiple times? Actually, L_u * (left_nv - L_u) counts ordered pairs? No, L_u * (left_nv - L_u) counts: pick one of the L_u indices as the first, and one of the (left_nv - L_u) indices as the second. This gives an ordered pair? No, if we pick one u and one not u, the order doesn't matter for the set. But L_u * (left_nv - L_u) gives the number of unordered pairs? Actually, if we pick one u and one not u, the number of such unordered pairs is L_u * (left_nv - L_u) because we choose the u from L_u choices, and the not u from left_nv - L_u choices, and the set is {u, not u}. So that's correct. And C(L_u, 2) is the number of pairs with both u. So total pairs containing u = L_u * (left_nv - L_u) + C(L_u, 2) = L_u * left_nv - L_u^2 + (L_u^2 - L_u)/2 = L_u * left_nv - (L_u^2 + L_u)/2 = L_u * left_nv - L_u*(L_u+1)/2. So that matches.

Then the number of invalid (left pair, right single) where the right single has value u and the left pair contains u is: (pairs containing u) * R_u.
So total valid for (0,1) = total_left_pairs * right_nv - sum_u (pairs_containing_u * R_u).

Similarly for (1,0): total_left_single = left_nv, total_right_pairs = C(right_nv, 2). Invalid when the left single has value u and the right pair contains u. Pairs in right containing u = R_u * right_nv - R_u*(R_u+1)/2. So valid = left_nv * C(right_nv, 2) - sum_u (L_u * pairs_in_right_containing_u).

So for each i, we can compute these values by iterating over all values u present in left or right. But we need to know L_u and R_u for each u. We can precompute for each i, the frequency maps. Since n=1000, we can for each i, build a frequency map of the left side and right side. But doing this naively per i would be O(n^2) to build the maps, and then O(n) to iterate over the union, total O(n^2) which is fine.

Specifically, for each i from 0 to n-1:
- left_indices = 0..i-1
- right_indices = i+1..n-1
We can maintain running totals? Since we iterate i from left to right, we can update the left and right counts incrementally. But we need to do this for each i anyway. Let's think: we can precompute prefix and suffix frequency maps. For each i, we need L_u for u in prefix, and R_u for u in suffix. The number of distinct values in prefix can be up to i. So for each i, we can iterate over all possible values (say, compress the array to indices 0..m-1). Then for each i, we can look at the frequency of each value in prefix and suffix. But iterating over all m values for each i gives O(n*m) = O(n^2) since m <= n. That's 10^6, which is fine.

So we can compress the values. Let val_to_idx be a mapping. Let arr = [val_to_idx[x] for x in nums]. Then n distinct values at most.

Precompute:
- prefix_counts[i+1][c] = number of times value c appears in arr[0..i]. This is 2D array of size n x m. That's O(n^2) memory, which is 10^6, fine.
- suffix_counts[i][c] = number of times value c appears in arr[i..n-1]. Or we can use prefix and compute suffix on the fly.

Actually, we can for each i, compute L_v and left_nv using prefix counts, and R_v and right_nv using suffix counts. And for the distinctness sum, we need sum over u of (L_u * left_nv - L_u*(L_u+1)/2) * R_u, etc. We can compute this by iterating over all values c from 0 to m-1, and for each i, we have L_c and R_c. So we can compute the sum in O(m) per i. Total O(n*m) = O(n^2).

So algorithm outline:
1. Compress values: let m <= n be the number of distinct values.
2. Precompute prefix sums: pref[i][c] = count of c in arr[0..i-1] (size n+1 x m). Also, we can precompute for each i, the total count of each value in the left, but we can just use pref[i] as the left counts.
3. Precompute factorials up to n for combinations modulo MOD = 10^9+7.
4. For each i from 0 to n-1:
   v = arr[i]
   L_v = pref[i][v]
   left_nv = i - L_v
   R_v = (pref[n][v] - pref[i+1][v])
   right_nv = (n-1-i) - R_v
   Compute contributions for all (a,b):
   ans_i = 0
   For a in 0..2:
     For b in 0..2:
       if a+b == 0: continue
       if a+b == 1: # k=2
          if a==0 and b==1:
             # compute distinctness
             total_left_pairs = C(left_nv, 2)
             total_right_single = right_nv
             sum_invalid = 0
             for c in 0..m-1:
                L_c = pref[i][c]
                if c == v: L_c = 0? Wait, pref[i][v] is the count of v in left. But for the distinctness, we need L_u for u != v. Actually, in the sum, for u=v, L_v is the count of v in left. But we are choosing elements not v from left. So we should not include v in the left_nv. We already defined left_nv as i - L_v, which excludes v. So when we iterate over c, we should only consider c != v, or we can include v but with L_v = 0? Actually, in the left side, the non-v elements are only those with c != v. So we can set L_c = 0 for c == v. Similarly for right.
             So for c from 0 to m-1, c != v:
                L_c = pref[i][c]
                R_c = pref[n][c] - pref[i+1][c]
                pairs_containing_c_in_left = L_c * left_nv - L_c*(L_c+1)/2   # this is valid since L_c is count of non-v in left
                sum_invalid += pairs_containing_c_in_left * R_c
             valid_01 = total_left_pairs * right_nv - sum_invalid
             ans_i += C(L_v, 0) * C(left_nv, 2) * C(R_v, 1) * C(right_nv, 1) ??? Wait, we already multiplied by C(L_v,0) and C(R_v,1) in the total? Actually, the total ways to pick 2 from left (not v) and 1 from right (v) and 1 from right (not v) is C(L_v, 0) * C(left_nv, 2) * C(R_v, 1) * C(right_nv, 1). But C(L_v,0)=1, C(R_v,1)=R_v. So we need to multiply the valid_01 (which is the number of ways to pick the non-v elements with distinctness) by C(R_v,1) = R_v. But wait, in the distinctness calculation, we assumed we are picking the non-v elements. The v element from right is fixed: we pick one v from right. There are R_v ways to pick which v from right. So the total ways for (0,1) is: R_v * (number of ways to pick 2 non-v from left and 1 non-v from right with distinctness). So we can compute valid_nonv = total_left_pairs * right_nv - sum_invalid, and then multiply by C(R_v, 1) = R_v. Similarly for (1,0): multiply by L_v.
          elif a==1 and b==0:
             similar.
       elif a+b >= 2:
          # no distinctness condition
          ways = C(L_v, a) * C(left_nv, 2-a) * C(R_v, b) * C(right_nv, 2-b)
          ans_i += ways
   Add ans_i to total answer.

But wait: for a+b=2, we have cases (0,2), (2,0), (1,1). In these cases, the non-v elements are either 2 from left, 2 from right, or 1 from left and 1 from right. For (0,2): left picks 2 non-v, right picks 2 v. The two non-v from left can be anything (including same). So no condition. Similarly (2,0): right picks 2 non-v, left picks 2 v. (1,1): left picks 1 non-v, right picks 1 non-v. They can be same. So no condition. So we can just use the product.

For a+b=3: (2,1) and (1,2). (2,1): left 2 v, right 1 v and 1 non-v. The non-v from right is free. So product: C(L_v,2) * C(left_nv,0) * C(R_v,1) * C(right_nv,1). (1,2): symmetric.

For a+b=4: (2,2): C(L_v,2) * C(R_v,2).

So we can compute these using combinations.

But we must be careful: for (0,1) and (1,0), we need to compute the distinctness sum efficiently. We can precompute for each i, the sum over c of (L_c * left_nv - L_c*(L_c+1)/2) * R_c. Since left_nv depends on i, we can compute it.

Let's define for each i, we have arrays L_c and R_c for c=0..m-1. We can compute:
sum1 = sum_{c} (L_c * left_nv - L_c*(L_c+1)/2) * R_c
= left_nv * sum_c (L_c * R_c) - sum_c (L_c*(L_c+1)/2 * R_c)

We can precompute for each i, the sum over c of L_c * R_c, and sum over c of (L_c*(L_c+1)/2) * R_c. But L_c and R_c depend on i. We can compute these in O(m) per i. Since m <= n=1000, n*m = 10^6, which is fine.

So for each i, we can:
- Get L_c = pref[i][c]
- Get R_c = pref[n][c] - pref[i+1][c]
- But we need to exclude c == v. So we can set L_v = 0, R_v = 0 for the sum? Actually, for c == v, L_c is the count of v in left, but in the non-v selection, we are not choosing v. So we should not include c==v in the sum. We can just skip c==v.
- Also, left_nv = sum_{c != v} L_c = i - L_v.
- right_nv = sum_{c != v} R_c = (n-1-i) - R_v.

So we can compute:
sum_LR = sum_{c != v} L_c * R_c
sum_L2R = sum_{c != v} L_c * (L_c+1) / 2 * R_c  (need modular inverse of 2)

Then sum_invalid = left_nv * sum_LR - sum_L2R.

Then valid_01_nonv = C(left_nv, 2) * right_nv - sum_invalid.

Then total for (0,1) = R_v * valid_01_nonv.

Similarly for (1,0):
sum_RL = sum_{c != v} R_c * L_c = same as sum_LR.
sum_R2L = sum_{c != v} R_c * (R_c+1) / 2 * L_c.
Then sum_invalid = right_nv * sum_RL - sum_R2L.
valid_10_nonv = left_nv * C(right_nv, 2) - sum_invalid.
Total for (1,0) = L_v * valid_10_nonv.

We need to compute C(x,2) = x*(x-1)/2. We'll precompute modular inverses.

Now, for a+b >= 2, we just use the combination formula.

Let's list all (a,b) pairs to sum:
a in [0,2], b in [0,2], a+b >= 1.
But for a+b=1, we handle separately.
For a+b >= 2:
(0,2): C(L_v,0)*C(left_nv,2) * C(R_v,2)*C(right_nv,0) = C(left_nv,2) * C(R_v,2)
(2,0): C(L_v,2) * C(right_nv,2)
(1,1): C(L_v,1)*C(left_nv,1) * C(R_v,1)*C(right_nv,1) = L_v * left_nv * R_v * right_nv
(2,1): C(L_v,2) * C(R_v,1) * C(right_nv,1)  (since left_nv choose 0)
(1,2): C(L_v,1) * C(left_nv,1) * C(R_v,2)  (since right_nv choose 0)
(2,2): C(L_v,2) * C(R_v,2)
(0,3) not possible, (3,0) not possible.
Also (0,2) and (2,0) are already included.
What about (0,0)? a+b=0, skip.
(0,1) and (1,0) handled separately.

So total for i:
ans_i = R_v * valid_01_nonv + L_v * valid_10_nonv
      + C(left_nv,2) * C(R_v,2)
      + C(L_v,2) * C(right_nv,2)
      + L_v * left_nv * R_v * right_nv
      + C(L_v,2) * R_v * right_nv
      + L_v * left_nv * C(R_v,2)
      + C(L_v,2) * C(R_v,2)

Wait, check: (2,1): C(L_v,2) * C(R_v,1) * C(right_nv,1) = C(L_v,2) * R_v * right_nv. Yes.
(1,2): C(L_v,1) * C(left_nv,1) * C(R_v,2) = L_v * left_nv * C(R_v,2). Yes.
(0,2): C(left_nv,2) * C(R_v,2). Yes.
(2,0): C(L_v,2) * C(right_nv,2). Yes.
(1,1): L_v * left_nv * R_v * right_nv. Yes.
(2,2): C(L_v,2) * C(R_v,2). Yes.

So we have 2 special terms for k=2, and 6 terms for k>=3.

But wait: are we overcounting? For (0,1) and (1,0), we used R_v and L_v respectively. In the product for (0,1), the number of ways to pick the v from right is C(R_v,1) = R_v. And the non-v part is valid_01_nonv. So that's correct.

Now, we need to compute valid_01_nonv and valid_10_nonv. As derived:
valid_01_nonv = C(left_nv, 2) * right_nv - (left_nv * sum_{c!=v} L_c * R_c - sum_{c!=v} L_c*(L_c+1)/2 * R_c)
= C(left_nv, 2) * right_nv - left_nv * S1 + S2
where S1 = sum_{c!=v} L_c * R_c
S2 = sum_{c!=v} L_c*(L_c+1)/2 * R_c

Similarly,
valid_10_nonv = left_nv * C(right_nv, 2) - right_nv * S1 + S3
where S3 = sum_{c!=v} R_c*(R_c+1)/2 * L_c

Note that S1 is symmetric. We can compute S1, S2, S3 in O(m) per i.

We need to be careful with modular arithmetic: division by 2 can be done by multiplying by inverse of 2.

Now, for each i, we need to compute L_c and R_c for c=0..m-1. We can precompute prefix counts: pref[i][c] for i=0..n, c=0..m-1. pref[0][c] = 0. pref[i+1][c] = pref[i][c] + (1 if arr[i]==c else 0). This is O(n*m) memory and time. n=1000, m<=1000, so 10^6 integers, fine.

Then for each i:
- L_c = pref[i][c]
- R_c = pref[n][c] - pref[i+1][c]
- v = arr[i]
- L_v = pref[i][v]
- R_v = pref[n][v] - pref[i+1][v]
- left_nv = i - L_v
- right_nv = (n-1-i) - R_v

Then compute S1, S2, S3 by looping c=0..m-1, skipping c==v.
S1 = sum L_c * R_c
S2 = sum L_c * (L_c+1) / 2 * R_c
S3 = sum R_c * (R_c+1) / 2 * L_c

All modulo MOD.

Then compute the terms.

We also need to handle the case where left_nv < 2, etc. The combination functions should return 0 if k < 0 or k > n. We can define a function nCk(x, k) that returns 0 if x < k or k < 0.

Let's test with example 1: nums = [1,1,1,1,1,1]. n=6, m=1, v=0.
For i=0: L_v=0, left_nv=0, R_v=5, right_nv=0. left_nv<2 so C(left_nv,2)=0. So most terms 0. ans_0=0.
i=1: L_v=1, left_nv=0, R_v=4, right_nv=0. ans_1=0.
i=2: L_v=2, left_nv=0, R_v=3, right_nv=0. C(L_v,2)=1. C(R_v,2)=3. C(L_v,2)*C(R_v,2)=3. Other terms 0. So ans_2=3.
i=3: L_v=3, left_nv=0, R_v=2, right_nv=0. C(L_v,2)=3, C(R_v,2)=1. ans_3=3.
i=4: L_v=4, left_nv=0, R_v=1, right_nv=0. C(L_v,2)=6, C(R_v,2)=0. ans_4=0.
i=5: L_v=5, left_nv=0, R_v=0, right_nv=0. ans_5=0.
Total = 6. Correct.

Example 2: nums = [1,2,2,3,3,4]. n=6. Let's list: 1,2,2,3,3,4.
Compressed: 1->0, 2->1, 3->2, 4->3.
i=0 (v=0): L_v=0, left_nv=0. R_v=0, right_nv=5. Most terms 0. ans_0=0.
i=1 (v=1): L_v=0 (no 2 before), left_nv=1. R_v=1 (one 2 after at i=2), right_nv=3. left_nv<2, so C(left_nv,2)=0. Check a+b>=2: (0,2): C(left_nv,2)=0. (2,0): C(L_v,2)=0. (1,1): L_v*left_nv*R_v*right_nv = 0*...=0. (2,1): 0. (1,2): 0. (2,2):0. (0,1) and (1,0): left_nv=1 so C(left_nv,2)=0, valid_01_nonv=0. So ans_1=0.
i=2 (v=1): L_v=1 (arr[1]=1), left_nv=1 (arr[0]=0). R_v=0 (no 2 after i=2? wait, arr[2]=1 is middle, so after: arr[3]=2, arr[4]=2? Actually arr[3]=2 is 3, arr[4]=3 is 2? Let's list: idx0:1(0), idx1:2(1), idx2:2(1), idx3:3(2), idx4:3(2), idx5:4(3). So for i=2 (v=1), left: idx0, idx1. L_v = count of 1 in left = idx1 is 1, so L_v=1. left_nv = 2-1=1 (idx0). Right: idx3,4,5. R_v = count of 1 in right = 0 (no 1 after). right_nv = 3-0=3.
Compute terms: left_nv=1, so C(left_nv,2)=0. So (0,2)=0, (0,1)=0. (1,0): valid_10_nonv? left_nv=1, C(right_nv,2)=C(3,2)=3. S1: sum over c!=1 of L_c * R_c. L_c: c=0:1, others 0. R_c: c=2:1 (idx3), c=2 again? idx4 is 2? Wait, arr[3]=2 (value 2), arr[4]=2 (value 2)? No, arr[3]=3 (compressed 2), arr[4]=3 (compressed 2). So R_2 = 2, R_3=1. c=1 is v, skip. So c=0: L_0=1, R_0=0. c=2: L_2=0, R_2=2. c=3: L_3=0, R_3=1. So S1 = 0.
S2: L_c*(L_c+1)/2 * R_c. L_0=1, R_0=0 -> 1*2/2*0=0. L_2=0. So S2=0.
S3: R_c*(R_c+1)/2 * L_c. R_2=2, L_2=0 ->0. R_3=1, L_3=0 ->0. So S3=0.
Then valid_10_nonv = left_nv * C(right_nv,2) - right_nv * S1 + S3 = 1*3 - 3*0 + 0 = 3.
Then L_v * valid_10_nonv = 1 * 3 = 3.
Now other terms: (2,0): C(L_v,2)=0. (1,1): L_v*left_nv*R_v*right_nv = 1*1*0*3=0. (2,1):0. (1,2):0. (2,2):0.
So ans_2 = 3.
Wait, example says output 4. So there should be 1 more from somewhere.
i=3 (v=2): v=arr[3]=2 (compressed 2). Left: idx0,1,2. L_v: count of 2 in left: idx1,2 are 2, so L_v=2. left_nv = 3-2=1 (idx0=1). Right: idx4,5. R_v: count of 2 in right: idx4 is 2, so R_v=1. right_nv = 2-1=1 (idx5=4).
Compute: left_nv=1, right_nv=1.
(0,1): R_v=1, valid_01_nonv? C(left_nv,2)=0, so 0.
(1,0): L_v=2, valid_10_nonv? left_nv=1, C(right_nv,2)=0, so 0.
Other terms:
(0,2): C(left_nv,2)=0.
(2,0): C(L_v,2)=1, C(right_nv,2)=0.
(1,1): L_v*left_nv*R_v*right_nv = 2*1*1*1=2.
(2,1): C(L_v,2)=1, R_v*right_nv=1*1=1 -> product=1.
(1,2): L_v*left_nv=2*1=2, C(R_v,2)=0.
(2,2): C(L_v,2)=1, C(R_v,2)=0.
Total = 0+0+0+0+2+1+0+0 = 3.
i=4 (v=2): v=arr[4]=2. Left: idx0,1,2,3. L_v: idx1,2 are 2, so L_v=2. left_nv = 4-2=2 (idx0,3). Right: idx5. R_v=0. right_nv=1.
Compute: left_nv=2, right_nv=1.
(0,1): R_v=0 -> 0.
(1,0): L_v=2, valid_10_nonv? left_nv=2, C(right_nv,2)=0 ->0.
(0,2): C(left_nv,2)=1, C(R_v,2)=0.
(2,0): C(L_v,2)=1, C(right_nv,2)=0.
(1,1): L_v*left_nv*R_v*right_nv = 2*2*0*1=0.
(2,1): C(L_v,2)=1, R_v*right_nv=0*1=0.
(1,2): L_v*left_nv=4, C(R_v,2)=0.
(2,2): 0.
Total = 0.
i=5: v=3, left_nv=... probably 0.
So total ans = ans_2 + ans_3 = 3+3=6? But example says 4. So we are overcounting. Let's check what subsequences are counted.

Example 2 says: [1,2,2,3,4] and [1,2,3,3,4] are valid. Each is counted once? Actually, the problem says "each have a unique middle mode... This subsequence can be formed in 6 different ways" for the first example, but for example 2, it just says output 4. So there are 4 subsequences? Let's list all valid subsequences of size 5 with unique middle mode.

Array: [1,2,2,3,3,4]
Indices: 0:1, 1:2, 2:2, 3:3, 4:3, 5:4.
We need to choose 5 indices, middle is index 2 (the 3rd element). The middle element value is the middle of the subsequence. So the middle index in the subsequence is 2 (0-indexed). So we choose i1 < i2 < i3 < i4 < i5, and the middle is i3.

We need to count combinations (i1,i2,i3,i4,i5) such that arr[i3] is unique mode.

Let's enumerate possible i3 (the middle index in the original array). Since we need i3 to be the middle, we need at least 2 elements before and 2 after. So i3 can be 2,3. (Indices 0,1 have less than 2 before; 4,5 have less than 2 after). So i3 = 2 or 3.

Case i3=2 (value 2). We need to choose i1<i2 from {0,1}, i4<i5 from {3,4,5}.
Possible left pairs: (0,1) only.
Right pairs: choose 2 from {3,4,5}: (3,4), (3,5), (4,5).
So total 3 combinations.
For each, the subsequence is:
(0,1,2,3,4): [1,2,2,3,3] -> values: 1,2,2,3,3. Frequencies: 2:2, 3:2, 1:1. Not unique mode (2 and 3 tie).
(0,1,2,3,5): [1,2,2,3,4] -> 2:2, others 1. Unique mode 2. Valid.
(0,1,2,4,5): [1,2,2,3,4]? Wait, i4=4 (value 3), i5=5 (value 4). So [1,2,2,3,4]. Same as above? Actually, [1,2,2,3,4] appears twice? Let's check: (0,1,2,3,5) gives 1,2,2,3,4. (0,1,2,4,5) gives 1,2,2,3,4? i4=4 is 3, i5=5 is 4, so 1,2,2,3,4. Yes, both are [1,2,2,3,4]. So that subsequence is formed in 2 ways. So for i3=2, we have 1 valid subsequence [1,2,2,3,4] formed in 2 ways, and 1 invalid [1,2,2,3,3]. So contributions: 2.

Case i3=3 (value 3). Left pairs from {0,1,2}: (0,1), (0,2), (1,2).
Right pairs from {4,5}: (4,5) only.
Combinations:
(0,1,3,4,5): [1,2,3,3,4] -> 3:2, others 1. Valid. Formed once? left pair (0,1), right (4,5).
(0,2,3,4,5): [1,2,3,3,4] -> same subsequence? i1=0 (1), i2=2 (2), i3=3 (3), i4=4 (3), i5=5 (4). So [1,2,3,3,4]. Yes, another way. So formed 2 ways.
(1,2,3,4,5): [2,2,3,3,4] -> 2:2, 3:2, 4:1. Not unique.
So for i3=3, we have [1,2,3,3,4] formed in 2 ways. So contributions: 2.
Total = 4. Correct.

Now, our algorithm gave for i=2 (original index 2? Wait, our i is the middle index in the array, which is the third element of the subsequence. In the example, i3=2 and i3=3. Our algorithm iterates over i as the middle position. So for i=2 (value 2), we got ans_2=3. But we expected 2 (the two ways for [1,2,2,3,4]). And for i=3 (value 3), we got ans_3=3, but expected 2. So we are overcounting by 1 in each.

Let's examine why. For i=2, we had:
L_v=1, left_nv=1, R_v=0, right_nv=3.
Our terms:
(0,1): R_v=0, so 0.
(1,0): L_v=1, valid_10_nonv=3. So 3.
This counts choosing 1 v from left, 2 non-v from right, with the 1 non-v from left and 2 non-v from right all distinct. Let's see what this counts.
We have left: idx0 (1), idx1 (2). v=2. So L_v=1 (idx1). left_nv=1 (idx0).
Right: idx3,4,5: values 3,3,4. R_v=0. right_nv=3.
We need to pick 1 v from left (must be idx1), and 2 non-v from right, and the 1 non-v from left (must be idx0) and the 2 non-v from right must be all distinct. So we need to pick 2 from right such that they are distinct from each other and from idx0 (value 1). Right values: 3,3,4. We need to pick 2 that are all distinct and not 1. The possible pairs from right: (3,3) - not distinct. (3,4) - distinct, and not 1. There are two 3's, so we can pick (idx3, idx5) or (idx4, idx5). That's 2 ways. Also (3,3) is invalid because they are not distinct (they are the same value). So valid_10_nonv should be 2, not 3. Our formula gave 3. Let's recalc: left_nv=1, C(right_nv,2)=C(3,2)=3. S1: sum L_c * R_c. L_c for c!=v: c=0 (1): L_0=1, R_0=0. c=2 (3): L_2=0, R_2=2. c=3 (4): L_3=0, R_3=1. So S1=0. S2=0. So valid_10_nonv = 1*3 - 3*0 + 0 = 3. But we missed the condition that the two non-v from right must be distinct from each other! In the (1,0) case, we are choosing 2 non-v from right. We need all 3 non-v elements (1 from left, 2 from right) to be distinct. So the two from right must be distinct from each other and from the left one. In our formula, we subtracted the cases where the left one equals one of the right ones. But we did not subtract the cases where the two right ones are equal to each other! In the (0,1) case, we choose 2 from left and 1 from right. The 2 from left can be equal? No, we required all 3 distinct, so the 2 from left must be distinct. But in our formula for (0,1), we used C(left_nv,2) which counts unordered pairs from left, including pairs of the same value. And we subtracted cases where the right element equals one of the left elements. But we did not subtract cases where the two left elements are equal! So we need to also ensure that the two left elements are distinct. In the (0,1) case, we have 2 from left and 1 from right. All three must be distinct. So the two from left must be distinct values. So we need to count only pairs of distinct values from left. Similarly, in the (1,0) case, the two from right must be distinct values.

So our valid_01_nonv and valid_10_nonv are wrong because they allow the two elements from the same side to be equal.

Let's correct:
For (0,1): choose 2 from left (distinct values, not v) and 1 from right (not v, distinct from both left values).
So the number of ways to choose 2 from left with distinct values: let's call it D_left. Then choose 1 from right not equal to either left value.
So total = sum_{u != w} L_u * L_w * (right_nv - R_u - R_w)  + sum_u C(L_u,2) * (right_nv - R_u). Wait, if the two left are distinct u and w, then the right must be not u and not w. If the two left are both u, then right must be not u. So we can compute:
Total = [Sum_{u} L_u * (right_nv - R_u) * (L_u - 1) ? No.

We can compute as: total pairs from left with distinct values = sum_{u} C(L_u, 2) * 2? No, that's ordered. Unordered distinct pairs = sum_{u} C(L_u, 2) (pairs of same value) + sum_{u<w} L_u * L_w (pairs of different values). But we need the right element to be distinct from both. So for a pair (u,w) with u != w, the number of right choices is right_nv - R_u - R_w. For a pair (u,u), the number of right choices is right_nv - R_u.
So total = sum_{u} C(L_u, 2) * (right_nv - R_u) + sum_{u<w} L_u * L_w * (right_nv - R_u - R_w).
This is equal to:
= sum_{u,w} L_u * L_w * (right_nv - R_u - R_w) / 2? No, careful: the first sum is over u, the second over u<w. We can write:
= sum_{u} L_u^2 * (right_nv - R_u) / 2? Not exactly because C(L_u,2) = L_u*(L_u-1)/2.
And sum_{u<w} L_u L_w = ( (sum_u L_u)^2 - sum_u L_u^2 ) / 2.
But we also have the R_w term.
Alternatively, we can compute:
Total distinct left pairs = (total left pairs) - (pairs with same value) = C(left_nv, 2) - sum_u C(L_u, 2).
For each distinct left pair, the number of right choices is right_nv minus the counts of the two values in the right.
So we can write:
Total = sum_{distinct left pairs} (right_nv - R_u - R_w)
= (right_nv) * (number of distinct left pairs) - sum_{distinct left pairs} (R_u + R_w)
= right_nv * (C(left_nv,2) - sum_u C(L_u,2)) - sum_{u<w} L_u L_w (R_u + R_w) - sum_u C(L_u,2) * 2 R_u? Wait, for pairs (u,u), the sum of R is 2 R_u. For pairs (u,w) with u<w, the sum is R_u + R_w.
So we can compute:
A = C(left_nv,2) - sum_u C(L_u,2)  (number of distinct-value pairs from left)
B = sum_{u<w} L_u L_w (R_u + R_w) + sum_u C(L_u,2) * 2 R_u
= sum_{u<w} L_u L_w R_u + sum_{u<w} L_u L_w R_w + sum_u L_u(L_u-1) R_u
= sum_{u} R_u L_u ( sum_{w != u} L_w ) + sum_u L_u(L_u-1) R_u? Let's do carefully:
sum_{u<w} L_u L_w R_u = sum_u R_u L_u (sum_{w>u} L_w)
sum_{u<w} L_u L_w R_w = sum_w R_w L_w (sum_{u<w} L_u)
So