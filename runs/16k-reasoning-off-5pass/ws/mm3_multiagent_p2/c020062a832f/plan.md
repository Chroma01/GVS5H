We need to compute inversion counts of B(k) where B_i(k) = (A_i + k) mod M for each k in [0, M-1]. N, M up to 2e5, so O(N log N + M log M) is acceptable.

Key observation: For each pair (i, j) with i < j, the contribution to inversion count depends on whether (A_i + k) mod M > (A_j + k) mod M. This is equivalent to checking if the cyclic order of A_i and A_j on a circle of length M is "forward" (A_i < A_j) or "backward" (A_i > A_j) when shifted by k.

For a fixed pair (i, j) with A_i != A_j:
- If A_i < A_j: the pair is an inversion when k is in range [M - A_j, M - A_i - 1] (mod M), i.e., k such that (A_i + k) mod M > (A_j + k) mod M.
- If A_i > A_j: the pair is an inversion when k is in range [M - A_i, M - A_j - 1].

If A_i == A_j: never an inversion.

So each pair contributes +1 to exactly one contiguous range of k values (mod M). We can use difference array / imos on a circular array of size M.

Approach:
1. For each pair (i, j) with i < j:
   - If A_i < A_j: range is [M - A_j, M - A_i - 1] (inclusive). Length = A_j - A_i.
   - If A_i > A_j: range is [M - A_i, M - A_j - 1]. Length = A_i - A_j.
2. Use a difference array `diff` of size M+1 (for handling wrap-around):
   - For range [l, r] (inclusive, non-wrapping): diff[l] += 1, diff[r+1] -= 1.
   - For wrapping range [l, M-1] ∪ [0, r]: diff[0] += 1, diff[r+1] -= 1, diff[l] += 1, diff[M] -= 1.
3. Prefix sum to get count[k] for each k.
4. Output count[0], count[1], ..., count[M-1].

Time complexity: O(N^2) for pairs is too slow. We need O(N log N) or O(N + M log M).

Better approach using counting:
For each k, B_i(k) = (A_i + k) mod M. We can think of sorting A and tracking how the cyclic shift affects inversions.

Alternative O(N log N + M log M) approach:
- Sort A. Let sorted_A be the sorted version.
- For k = 0: compute inversion count of A directly using BIT in O(N log N).
- When we increase k by 1, each element increases by 1 mod M. Elements that were M-1 become 0 (they "wrap around" and become smallest).

Let cnt[x] = number of occurrences of value x in A.
When k increases by 1:
- Elements with value M-1 become 0: they move from largest to smallest.
- All other elements increase by 1.

The change in inversion count when k -> k+1:
- For each element that wraps (value M-1 -> 0): it was larger than all other elements, now smaller than all. So it loses (N - 1) inversions and gains 0 inversions. Net change: -(N - 1) * cnt[M-1].
- For each element that increases by 1 (value v -> v+1, where v < M-1): it was larger than elements with value <= v, now larger than elements with value <= v+1. So it gains cnt[v+1] inversions (new pairs where it's larger) and loses cnt[v] inversions (pairs where it was larger but now equal? No, it was larger than elements with value v, now equal, so those pairs are no longer inversions).

Wait, let me think more carefully. Let f(k) = inversion count of B(k).

When k increases by 1:
- Each element with value v (v < M-1) becomes v+1.
- Each element with value M-1 becomes 0.

For an element with original value v (v < M-1):
- Before: it was greater than elements with value < v.
- After: it is greater than elements with value < v+1, i.e., value < v or value = v (but original value v elements are now v+1, so they're greater than original v elements? No, original v elements become v+1, so two original v elements both become v+1, still equal).

Actually, let's track pairs. For a pair (i, j) with i < j, original values a, b.
- If a < b: inversion when k in [M-b, M-a-1].
- If a > b: inversion when k in [M-a, M-b-1].
- If a == b: never inversion.

The contribution of pair (a, b) with a < b is a range of length b - a.
The contribution of pair (a, b) with a > b is a range of length a - b.

So total inversions for k is sum over pairs of indicator that k is in the pair's range.

We can compute this efficiently using the difference array approach, but we need to sum over all pairs efficiently.

For each pair of distinct values (x, y) with x < y:
- Number of pairs (i, j) with i < j, A_i = x, A_j = y: let's call this P(x, y).
- Number of pairs (i, j) with i < j, A_i = y, A_j = x: let's call this Q(x, y).

For value pair (x, y) with x < y:
- P(x, y) pairs contribute range [M-y, M-x-1] (length y - x).
- Q(x, y) pairs contribute range [M-x, M-y-1] (length x - y? No, length is y - x as well? Wait.

If A_i = y, A_j = x (y > x), then range is [M-y, M-x-1], length = (M-x-1) - (M-y) + 1 = y - x.

Hmm, both have the same length y - x. But they occupy different ranges:
- P(x, y): range [M-y, M-x-1]
- Q(x, y): range [M-x, M-y-1]

These two ranges are adjacent and together cover [M-y, M-x-1] ∪ [M-x, M-y-1] = [M-y, M-y-1] which is length y - x + (y - x) = 2(y-x)? No.

[M-y, M-x-1] has length (M-x-1) - (M-y) + 1 = y - x.
[M-x, M-y-1] has length (M-y-1) - (M-x) + 1 = y - x.

So total contribution from value pair (x, y) is:
- P(x, y) * 1 in range [M-y, M-x-1]
- Q(x, y) * 1 in range [M-x, M-y-1]

We can compute P(x, y) and Q(x, y) efficiently.

Let pos[x] = list of positions where A_i = x.
P(x, y) = number of pairs (i, j) with i < j, A_i = x, A_j = y.
Q(x, y) = number of pairs (i, j) with i < j, A_i = y, A_j = x.

We can compute these using prefix sums.

For each value x, let count_x = number of occurrences.
For each pair (x, y) with x < y:
- P(x, y) = sum over positions i where A_i = x of (number of y's after position i).
- Q(x, y) = sum over positions i where A_i = y of (number of x's after position i).

We can compute P(x, y) by iterating through the array and maintaining counts.

Actually, we can compute the total contribution to the diff array directly.

For each position i with value v = A_i:
- For each j > i with value w = A_j:
  - If v < w: contributes +1 to range [M-w, M-v-1].
  - If v > w: contributes +1 to range [M-v, M-w-1].

This is O(N^2) if done naively.

Better: process by value pairs.

For each value v, let S_v = set of positions where A_i = v.
For each pair of values (v, w) with v < w:
- P(v, w) = number of (i, j) with i < j, A_i = v, A_j = w.
- Q(v, w) = number of (i, j) with i < j, A_i = w, A_j = v.

We can compute P(v, w) for all v < w in O(N + M^2) or better.

Actually, we can compute the diff array contributions as follows:

For each value v, let c_v = count of v in A.
For each pair (v, w) with v < w:
- Contribution to diff: 
  - P(v, w) added to range [M-w, M-v-1]
  - Q(v, w) added to range [M-v, M-w-1]

We can compute P(v, w) and Q(v, w) using the positions.

Let total[v] = total count of v in A.
Let suffix_y[i] = number of y's in positions > i.

For each i with A_i = v:
- P contribution from this i: for each w > v, (number of w's after i).
- Q contribution from this i: for each w < v, (number of w's after i).

We can precompute for each position i, the count of each value after i? That's O(N*M).

Alternative: use the fact that we only need the sum over all pairs.

Let's think differently. The inversion count for k is:
inv(k) = sum_{i < j} [ (A_i + k) mod M > (A_j + k) mod M ]

This equals:
inv(k) = sum_{i < j} [ A_i > A_j and k in [M - A_i, M - A_j - 1] ] + sum_{i < j} [ A_i < A_j and k in [M - A_j, M - A_i - 1] ]

For each k, we can compute this if we know, for each value v, how many elements with value > v come before elements with value v, etc.

Actually, let's use the following approach:
For each k, inv(k) = total_pairs - non_inversions.
non_inversions = pairs where (A_i + k) mod M <= (A_j + k) mod M.

Or: inv(k) = sum over pairs of indicator.

Let's define for each value v, let L_v(k) = number of elements with value <= v in the sequence after applying shift k.
Actually, (A_i + k) mod M <= v means A_i is in [(M - k) mod M, (M - k + v) mod M] (with wrap).

This is getting complex. Let me think of a cleaner approach.

Approach using BIT and incremental update:

Compute inv(0) using BIT on A.
Then for k = 1 to M-1, update from inv(k-1) to inv(k).

When k increases by 1:
- Elements with value M-1 become 0.
- Elements with value v (0 <= v < M-1) become v+1.

Change in inversion count:
- For each element that was M-1 and becomes 0: it was greater than all N-1 other elements, now it's smaller than all. So it loses N-1 inversions, gains 0. Net: -(N-1).
- For each element with value v (v < M-1) that becomes v+1:
  - It was greater than elements with value < v.
  - It becomes greater than elements with value < v+1.
  - New inversions gained: elements with value v+1 that come after this element? No, wait.

Let's track for a specific element e at position i with value v (v < M-1).
Before shift (k): e has value v.
After shift (k+1): e has value v+1.

Pairs (e, other) where other is at position j > i:
- Before: e > other iff v > A_j.
- After: e > other iff v+1 > A_j, i.e., A_j <= v.

So the change for pairs where e is the left element:
- If A_j = v: before e > A_j (true), after e > A_j (false). Loses 1 inversion.
- If A_j < v: before true, after true. No change.
- If A_j > v: before false, after false. No change.

Wait, that's not right. If A_j = v, before e > A_j (v > v is false). So no inversion before. After: v+1 > v is true. So gains 1 inversion.

Let me redo:
Before: e > other iff v > A_j.
After: e > other iff v+1 > A_j.

Case A_j < v: before true, after true. No change.
Case A_j = v: before false, after true. Gains 1.
Case A_j > v: before false, after false. No change.
Case A_j = v+1: before false, after false. No change.

So for left element e with value v (v < M-1), it gains inversions with elements to its right that have value v.

Similarly, for pairs where e is the right element (other at position j < i, value w):
Before: other > e iff w > v.
After: other > e iff w > v+1.

Case w < v: before false, after false. No change.
Case w = v: before false, after false. No change.
Case w = v+1: before true, after false. Loses 1.
Case w > v+1: before true, after true. No change.

So for right element e with value v (v < M-1), it loses inversions with elements to its left that have value v+1.

Now for elements with value M-1 becoming 0:
Before: e > other iff M-1 > A_j, i.e., always true (since A_j < M).
After: e > other iff 0 > A_j, i.e., never true.

So loses N-1 inversions as left element.
As right element: before other > e iff A_j > M-1, never. After other > e iff A_j > 0.
So gains (number of elements to left with value > 0) inversions.

Wait, this is getting messy. Let me think again.

Actually, the cleanest way is:
inv(k) = number of pairs (i, j) with i < j and (A_i + k) mod M > (A_j + k) mod M.

This is equivalent to: in the circular order, A_i comes after A_j when shifted by k.

For fixed k, sort the shifted values. The inversion count is the number of pairs out of order.

We can compute inv(k) for all k using the following observation:

For each pair (i, j) with i < j, define f(i, j) = the set of k where (A_i + k) mod M > (A_j + k) mod M.
This is a contiguous range on the circle of length M.

We can accumulate these ranges using a difference array.

To do this efficiently, we need to process all pairs (i, j) with i < j.

Number of pairs is O(N^2), too many.

But we can group by values. Let cnt[v] = count of value v.
For each pair of values (a, b) with a != b:
- Let P(a, b) = number of pairs (i, j) with i < j, A_i = a, A_j = b.
- Let Q(a, b) = number of pairs (i, j) with i < j, A_i = b, A_j = a.

Note P(a, b) + Q(a, b) = cnt[a] * cnt[b].

For a < b:
- P(a, b) contributes to range [M-b, M-a-1] (length b-a).
- Q(a, b) contributes to range [M-a, M-b-1] (length b-a).

So for each unordered pair {a, b} with a < b, we add:
- P(a, b) to diff[M-b .. M-a-1]
- Q(a, b) to diff[M-a .. M-b-1]

We need to compute P(a, b) for all a < b.

P(a, b) = sum over positions i with A_i = a of (number of b's after position i).

We can compute this by iterating through the array once:
Maintain count_so_far[v] = number of v's seen so far.
For each position i with value v = A_i:
- For each b > v: P(v, b) += count_so_far[b]? No, we need b's after, not before.

Wait, P(a, b) is pairs (i, j) with i < j, A_i = a, A_j = b.
So for fixed i with A_i = a, we need number of b's at positions > i.

We can precompute suffix counts: for each position i, suffix_b[i] = number of b's in positions > i.
Then P(a, b) = sum over i with A_i = a of suffix_b[i].

This is O(N * M) if we store all suffix counts.

Alternative: process by value.
For each value a, let positions_a = list of positions where A_i = a.
For each value b > a, P(a, b) = sum over i in positions_a of (number of b's after i).

We can compute this by iterating through positions_a and using a BIT or just counting.

Actually, we can compute P(a, b) for all a, b using the following:
For each position i, value v = A_i.
For each b > v, we want to add to P(v, b) the number of b's after i.

We can precompute for each value b, the positions of b. Then for each i, we can binary search to find how many b's are after i.

But we need to do this for all pairs (v, b) with v < b, which is O(M^2).

However, we can use the fact that we only need the sum, and we can use a sweep.

Let's think of it as: for each value b, we process positions of b. For each position j of b, it contributes to P(a, b) for all a < b, specifically to the count of a's before j.

So P(a, b) = sum over positions j of b of (number of a's before j).

This is symmetric.

We can compute all P(a, b) by:
For each value b from 0 to M-1:
  count_a = 0
  Iterate through array positions 1 to N:
    If A_i = b: for each a < b, P(a, b) += count_a.
    If A_i < b: count_a += 1.

This is O(N * M) in the inner loop.

But we can optimize: we don't need to iterate over all a < b. We can maintain a BIT or just an array count[0..M-1].

For each b:
  count[0..b-1] = number of elements < b seen so far.
  When we see a b, we add count[0..b-1] to P(0, b), P(1, b), ..., P(b-1, b).

This is still O(M) per b, total O(M^2).

But M is up to 2e5, so O(M^2) is too slow.

We need O((N + M) log M) or similar.

Alternative approach: use the formula
inv(k) = sum_{i=1}^{N} (number of j > i with (A_j + k) mod M < (A_i + k) mod M)

For fixed k, this is like counting inversions in a transformed array.

We can compute inv(k) for all k by noting that as k increases, the array undergoes a cyclic shift of values.

Actually, there's a known technique for this type of problem.

Let's define the array C where C_i = A_i.
For k, B_i(k) = (C_i + k) mod M.

inv(k) = number of pairs (i, j) with i < j and B_i(k) > B_j(k).

Consider the permutation that sorts B(k). The inversion count is the number of inversions in this permutation.

As k varies, the relative order of elements changes only when two elements "cross" in the cyclic order.

Specifically, for two elements with values a and b (a != b), they swap relative order when k passes through M - max(a, b) or something.

Actually, (a + k) mod M > (b + k) mod M iff k is in a specific range.

For a < b: (a + k) mod M > (b + k) mod M iff k in [M-b, M-a-1].
For a > b: (a + k) mod M > (b + k) mod M iff k in [M-a, M-b-1].

So each pair (i, j) with A_i = a, A_j = b contributes +1 to inv(k) for k in a specific range of length |a - b|.

The total inv(k) is the sum of these indicators.

We can compute this by iterating over all pairs (i, j) and updating a difference array. But there are O(N^2) pairs.

However, we can group by values. For each pair of values (a, b) with a < b:
- Let n_ab = number of pairs (i, j) with i < j, A_i = a, A_j = b.
- Let n_ba = number of pairs (i, j) with i < j, A_i = b, A_j = a.

Then:
- n_ab pairs contribute to range [M-b, M-a-1] (length b-a).
- n_ba pairs contribute to range [M-a, M-b-1] (length b-a).

We need to compute n_ab for all a < b.

n_ab = (number of a's before each b) summed over all b's.
= sum over positions j with A_j = b of (number of a's at positions < j).

We can compute this for all a, b using a 2D prefix sum or by processing.

Since M is up to 2e5, and we have N up to 2e5, we can do O((N + M) log M) or O(N sqrt M) etc.

Let's try to compute n_ab efficiently.

For each position i with value v = A_i:
- It contributes to n_{v, w} for all w > v as: for each w > v, n_{v, w} increases by (number of w's after i).
- It contributes to n_{w, v} for all w < v as: for each w < v, n_{w, v} increases by (number of w's before i).

Actually, let's define:
For each i, let v = A_i.
For each w > v: n_{v, w} += (count of w in positions > i).
For each w < v: n_{w, v} += (count of w in positions < i).

We can precompute for each position i, the count of each value after i. But that's O(NM).

Alternative: process by value.
For each value w, let positions_w = sorted list of positions.
For each value v < w:
  n_{v, w} = sum over j in positions_w of (number of v's at positions < j).

We can compute this by iterating through positions_w and using a BIT on positions, or by using the fact that positions are sorted.

For fixed w, we iterate through positions_w in order. For each position j in positions_w, we want to count how many v's are before j, for all v < w.

We can maintain an array count_v = number of v's seen so far (before current position in the array).
When we are at position j with A_j = w, for each v < w, n_{v, w} += count_v.

This is O(M) per w, total O(M^2).

But we can optimize: we only need to update n_{v, w} for v < w. We can maintain a Fenwick tree or segment tree over values.

Actually, we can do this:
For each position i from 1 to N:
  v = A_i
  For all values u < v: n_{u, v} += count_u (where count_u is number of u's seen so far)
  count_v += 1

This is O(N * M) if we iterate over all u < v.

But we can use a BIT to query sum of counts for range [0, v-1], and we need to add this to n_{u, v} for each u < v individually? No, we need to add to each n_{u, v} separately.

Wait, n_{u, v} is a 2D array. We need to add count_u to n_{u, v} for each u < v.

This is like: for each v, we add the vector (count_0, count_1, ..., count_{v-1}) to the row n_{*, v}.

We can do this by maintaining an array of size M for the current counts, and for each v, we need to add the prefix sums to n_{0, v}, n_{1, v}, ..., n_{v-1, v}.

This is still O(M^2) in total.

Alternative: since we only need the final diff array, and the diff array is 1D of size M, maybe we can compute the contribution to diff directly.

For each pair of values (a, b) with a < b:
- n_ab contributes to diff[M-b .. M-a-1]
- n_ba contributes to diff[M-a .. M-b-1]

The total contribution to diff[l] for each l is:
diff[l] = sum over pairs (a, b) with a < b and l in [M-b, M-a-1] of n_ab + sum over pairs (a, b) with a < b and l in [M-a, M-b-1] of n_ba.

This is complex.

Let's try a different approach: compute inv(k) for all k using the fact that inv(k) can be computed from inv(k-1) with O(N) or O(N log N) update.

When k increases by 1:
- Elements with value M-1 become 0.
- Elements with value v (v < M-1) become v+1.

Change in inversion count:
Let me define the change more carefully.

Let S be the set of positions. For each position i, let old_val = A_i, new_val = (old_val + 1) mod M.

For each pair (i, j) with i < j:
- Before: old_i > old_j ?
- After: new_i > new_j ?

Case 1: old_i < M-1 and old_j < M-1.
  new_i = old_i + 1, new_j = old_j + 1.
  new_i > new_j iff old_i > old_j.
  So no change.

Case 2: old_i = M-1, old_j < M-1.
  new_i = 0, new_j = old_j + 1.
  Before: old_i > old_j (true).
  After: new_i > new_j iff 0 > old_j + 1 (false, since old_j >= 0).
  So loses 1 inversion.

Case 3: old_i < M-1, old_j = M-1.
  new_i = old_i + 1, new_j = 0.
  Before: old_i > old_j (false).
  After: new_i > new_j iff old_i + 1 > 0 (true).
  So gains 1 inversion.

Case 4: old_i = M-1, old_j = M-1.
  new_i = 0, new_j = 0.
  Before: old_i > old_j (false).
  After: new_i > new_j (false).
  No change.

So the change in inversion count when k -> k+1 is:
- For each pair (i, j) with i < j, old_i = M-1, old_j < M-1: -1
- For each pair (i, j) with i < j, old_i < M-1, old_j = M-1: +1

Number of pairs (i, j) with i < j, old_i = M-1, old_j < M-1:
= (number of M-1's at positions i) * (number of non-M-1's at positions j > i)
= sum over i with A_i = M-1 of (number of non-M-1's after i)

Number of pairs (i, j) with i < j, old_i < M-1, old_j = M-1:
= (number of non-M-1's at positions i) * (number of M-1's at positions j > i)
= sum over i with A_i != M-1 of (number of M-1's after i)

Let c = count of M-1 in A.
Let total_non_m1 = N - c.

For each position i with A_i = M-1:
  non_m1_after_i = (total_non_m1) - (number of non-M-1's before i)
  But we can compute: non_m1_after_i = (N - i) - (number of M-1's after i) - (number of non-M-1's at positions > i that are... wait.

Actually:
non_m1_after_i = total_non_m1 - non_m1_before_i.
non_m1_before_i = (i-1) - m1_before_i.

So non_m1_after_i = total_non_m1 - (i-1) + m1_before_i.

Similarly, for positions i with A_i != M-1:
  m1_after_i = c - m1_before_i.

So:
loss = sum over i with A_i = M-1 of (total_non_m1 - (i-1) + m1_before_i)
gain = sum over i with A_i != M-1 of (c - m1_before_i)

This can be computed in O(N) if we know m1_before_i for each i.

We can precompute m1_before_i by iterating through the array.

Let m1_prefix[i] = number of M-1's in positions 1..i.

Then:
loss = sum over i with A_i = M-1 of (total_non_m1 - (i-1) + m1_prefix[i-1])
     = c * total_non_m1 - sum_{i: A_i=M-1} (i-1) + sum_{i: A_i=M-1} m1_prefix[i-1]

gain = sum over i with A_i != M-1 of (c - m1_prefix[i-1])
     = (N - c) * c - sum_{i: A_i != M-1} m1_prefix[i-1]

Note: sum_{i: A_i=M-1} m1_prefix[i-1] + sum_{i: A_i != M-1} m1_prefix[i-1] = sum_{i=1}^{N} m1_prefix[i-1] = sum_{j=0}^{N-1} m1_prefix[j].

So:
change = gain - loss
= [(N-c)c - sum_{i: A_i != M-1} m1_prefix[i-1]] - [c*(N-c) - sum_{i: A_i=M-1} (i-1) + sum_{i: A_i=M-1} m1_prefix[i-1]]
= - sum_{i: A_i != M-1} m1_prefix[i-1] + sum_{i: A_i=M-1} (i-1) - sum_{i: A_i=M-1} m1_prefix[i-1]
= sum_{i: A_i=M-1} (i-1) - sum_{i=1}^{N} m1_prefix[i-1]
= sum_{i: A_i=M-1} (i-1) - sum_{j=0}^{N-1} m1_prefix[j]

Let S = sum_{i: A_i=M-1} (i-1).
Let T = sum_{j=0}^{N-1} m1_prefix[j].

Then change = S - T.

We can compute S and T in O(N).

Then inv(k+1) = inv(k) + change.

But wait, this is only for one step. We need to do this M times, but the array changes each time (elements with M-1 become 0, etc.).

Actually, the above calculation assumes we know which elements are M-1 in the current array. After the shift, the values change.

After shift k -> k+1:
- Elements that were M-1 become 0.
- Elements that were v become v+1.

So for the next step (k+1 -> k+2), the "M-1" elements are those that were M-2 before the first shift, i.e., those with original value M-2.

So we need to track for each k, which original values act as "M-1" in the current configuration.

This suggests we can precompute for each original value v, the contribution to the change when v becomes the "wrap" value.

Specifically, when we shift from k to k+1, the elements that wrap are those with current value M-1, which are those with original value (M-1 - k) mod M.

So for each k, the wrapping value is w_k = (M-1-k) mod M.

The change from inv(k) to inv(k+1) depends on w_k.

We can precompute for each value w (0 <= w < M), the change that occurs when w is the wrapping value.

Let change[w] = the change in inversion count when we shift and the wrapping value is w.

From the formula above:
change[w] = sum_{i: A_i=w} (i-1) - sum_{j=0}^{N-1} prefix_w[j]
where prefix_w[j] = number of w's in positions 1..j.

Wait, in the formula, we used m1_prefix which is count of M-1's. Here, w is the wrapping value.

So:
change[w] = sum_{i: A_i=w} (i-1) - sum_{j=0}^{N-1} (number of w's in positions 1..j)

Let pos_w = list of positions where A_i = w (1-indexed).
sum_{i: A_i=w} (i-1) = sum_{p in pos_w} (p-1).

sum_{j=0}^{N-1} prefix_w[j] = sum_{j=0}^{N-1} (number of w's in positions 1..j)
= sum_{p in pos_w} (N - p + 1)? Let's compute:
For each position p in pos_w, it contributes to prefix_w[j] for j >= p.
So sum_{j=0}^{N-1} prefix_w[j] = sum_{p in pos_w} (N - p + 1).

Wait: prefix_w[j] for j=0 is 0. For j from 1 to N, prefix_w[j] = number of w's in 1..j.
Sum_{j=0}^{N} prefix_w[j] = sum_{p in pos_w} (N - p + 1).
Because position p contributes to prefix_w[p], prefix_w[p+1], ..., prefix_w[N], that's N - p + 1 terms.

So:
change[w] = sum_{p in pos_w} (p-1) - sum_{p in pos_w} (N - p + 1)
= sum_{p in pos_w} [(p-1) - (N - p + 1)]
= sum_{p in pos_w} [2p - N - 2]

We can compute this for each w in O(|pos_w|), total O(N).

Then:
inv(0) = inversion count of A.
For k = 1 to M-1:
  w = (M-1 - (k-1)) mod M = (M-k) mod M.
  inv(k) = inv(k-1) + change[w].

Wait, when going from k-1 to k, the wrapping value is the value that becomes M-1 after shift k-1, i.e., original value (M-1 - (k-1)) mod M = (M-k) mod M.

So:
inv(k) = inv(k-1) + change[(M-k) mod M].

We need to compute inv(0) and then apply M-1 updates.

Time complexity: O(N log N + M) for inv(0) using BIT, plus O(N) to precompute change[w], plus O(M) to apply updates.

Total: O(N log N + M).

Let's verify with sample.

Sample 1: N=3, M=3, A=[2,1,0]
inv(0): pairs: (2,1), (2,0), (1,0) all inversions. inv(0)=3.

Compute change[w]:
w=0: pos_0 = [3]. sum (2p - N - 2) = 2*3 - 3 - 2 = 6-5=1.
w=1: pos_1 = [2]. 2*2 - 3 - 2 = 4-5=-1.
w=2: pos_2 = [1]. 2*1 - 3 - 2 = 2-5=-3.

Now:
k=1: w = (3-1) mod 3 = 2. change[2] = -3. inv(1) = 3 + (-3) = 0? But sample says 1.

Hmm, discrepancy. Let me recheck.

Sample 1:
k=0: B=[2,1,0], inv=3.
k=1: B=[0,2,1], inv=1.
k=2: B=[1,0,2], inv=1.

My formula gives inv(1)=0, which is wrong.

Let me re-derive the change formula.

When k increases by 1:
- old_i = A_i + k (mod M)? No, B_i(k) = (A_i + k) mod M.
- B_i(k+1) = (A_i + k + 1) mod M = (B_i(k) + 1) mod M.

So the shift is applied to B(k), not to A.

In my derivation, I used "old" as the current values and "new" as after shift.

Let me redefine:
At step k, we have array B(k) where B_i = (A_i + k) mod M.
We want to compute inv(B(k)).

When moving from k to k+1:
B_i(k+1) = (B_i(k) + 1) mod M.

Elements with B_i(k) = M-1 become 0.
Elements with B_i(k) = v (v < M-1) become v+1.

Change in inversion count:
For pair (i, j) with i < j:
- If B_i(k) = M-1 and B_j(k) < M-1: before B_i > B_j (true), after B_i=0, B_j+1, so 0 > B_j+1 is false. Loses 1.
- If B_i(k) < M-1 and B_j(k) = M-1: before B_i > B_j (false), after B_i+1 > 0 (true). Gains 1.
- Otherwise: no change.

So change = (number of pairs with i < j, B_i < M-1, B_j = M-1) - (number of pairs with i < j, B_i = M-1, B_j < M-1).

Let c = number of M-1 in B(k).
Let S = set of positions with B_i = M-1.

gain = number of pairs (i, j) with i < j, i not in S, j in S.
loss = number of pairs (i, j) with i < j, i in S, j not in S.

gain = sum_{j in S} (number of non-S elements before j).
loss = sum_{i in S} (number of non-S elements after i).

Note: gain + loss = c * (N - c).

Specifically:
gain = sum_{j in S} [(j-1) - (number of S elements before j)]
loss = sum_{i in S} [(N-i) - (number of S elements after i)]

Let prefix_S[j] = number of S elements in 1..j.
Then:
gain = sum_{j in S} (j-1 - prefix_S[j-1])
loss = sum_{i in S} (N-i - (c - prefix_S[i]))

So:
change = gain - loss
= sum_{j in S} (j-1 - prefix_S[j-1]) - sum_{i in S} (N-i - c + prefix_S[i])
= sum_{i in S} [(i-1 - prefix_S[i-1]) - (N-i - c + prefix_S[i])]
= sum_{i in S} [i-1 - prefix_S[i-1] - N + i + c - prefix_S[i]]
= sum_{i in S} [2i - N - 1 + c - prefix_S[i-1] - prefix_S[i]]

Note prefix_S[i] = prefix_S[i-1] + (1 if i in S else 0).
So for i in S: prefix_S[i] = prefix_S[i-1] + 1.
Thus prefix_S[i-1] + prefix_S[i] = 2*prefix_S[i-1] + 1.

So:
change = sum_{i in S} [2i - N - 1 + c - 2*prefix_S[i-1] - 1]
= sum_{i in S} [2i - N - 2 + c - 2*prefix_S[i-1]]

For sample 1, k=0, B=[2,1,0], S = positions where B_i=2, i.e., position 1.
c=1.
prefix_S[0]=0.
change = 2*1 - 3 - 2 + 1 - 2*0 = 2 - 3 - 2 + 1 = -2.
inv(1) = 3 + (-2) = 1. Correct!

k=1, B=[0,2,1], S = position 2.
c=1.
prefix_S[1] = 0 (since position 1 is not in S).
prefix_S[2-1] = prefix_S[1] = 0.
change = 2*2 - 3 - 2 + 1 - 2*0 = 4 - 3 - 2 + 1 = 0.
inv(2) = 1 + 0 = 1. Correct!

Great, the formula works.

Now, the key is: at step k, the set S is the positions where B_i(k) = M-1.
B_i(k) = (A_i + k) mod M = M-1 iff A_i = (M-1-k) mod M.

So S_k = positions where A_i = (M-1-k) mod M.

For each original value v, let pos_v = list of positions where A_i = v.
Then S_k = pos_{(M-1-k) mod M}.

We need to compute change for each possible S, i.e., for each value v.

change[v] = sum_{i in pos_v} [2i - N - 2 + c_v - 2*prefix_v[i-1]]
where c_v = |pos_v|, and prefix_v[i] = number of elements in pos_v with position <= i.

We can precompute change[v] for all v in O(N) total.

Then:
inv(0) = inversion count of A.
For k = 1 to M-1:
  v = (M-1 - (k-1)) mod M = (M-k) mod M.
  inv(k) = inv(k-1) + change[v].

Wait, for k=1, v = (M-1) mod M = M-1.
In sample 1, M=3, v=2. change[2] should be -2.
pos_2 = [1]. c=1. prefix[0]=0.
change = 2*1 - 3 - 2 + 1 - 0 = -2. Correct.

For k=2, v = (M-2) mod M = 1.
pos_1 = [2]. c=1. prefix[1]=0.
change = 2*2 - 3 - 2 + 1 - 0 = 0. Correct.

So the algorithm is:
1. Read N, M, A.
2. Compute inv(0) using BIT (Fenwick tree) on A.
3. For each value v in 0..M-1:
   - Let pos_v = sorted list of positions (1-indexed) where A_i = v.
   - c = len(pos_v).
   - prefix = 0
   - change_v = 0
   - For each p in pos_v:
     change_v += 2*p - N - 2 + c - 2*prefix
     prefix += 1
4. Initialize ans[0] = inv(0).
5. For k = 1 to M-1:
   v = (M - k) % M
   ans[k] = ans[k-1] + change[v]
6. Output ans[0], ans[1], ..., ans[M-1].

Time complexity: O(N log N + M + N) = O(N log N + M).
Space: O(N + M).

This should work for N, M up to 2e5.

Let's verify with sample 2.
N=5, M=6, A=[5,3,5,0,1]
inv(0): 
Pairs:
(5,3): 5>3, inv
(5,5): equal, no
(5,0): 5>0, inv
(5,1): 5>1, inv
(3,5): no
(3,5): no
(3,0): 3>0, inv
(3,1): 3>1, inv
(5,0): inv
(5,1): inv
(0,1): no
Total: 7. Matches sample.

Compute change[v]:
v=0: pos=[4]. c=1. prefix=0.
change = 2*4 - 5 - 2 + 1 - 0 = 8-7+1=2.
v=1: pos=[5]. c=1. prefix=0.
change = 2*5 - 5 - 2 + 1 = 10-7+1=4.
v=2: pos=[]. c=0. change=0.
v=3: pos=[2]. c=1. prefix=0.
change = 2*2 - 5 - 2 + 1 = 4-7+1=-2.
v=4: pos=[]. change=0.
v=5: pos=[1,3]. c=2.
  p=1: prefix=0, change += 2*1 - 5 - 2 + 2 - 0 = 2-7+2=-3.
  p=3: prefix=1, change += 2*3 - 5 - 2 + 2 - 2 = 6-7+2-2=-1.
  Total change[5] = -4.

Now:
k=0: ans=7
k=1: v=(6-1)%6=5. ans = 7 + (-4) = 3. Matches sample (3).
k=2: v=(6-2)%6=4. ans = 3 + 0 = 3. Matches.
k=3: v=3. ans = 3 + (-2) = 1. Matches.
k=4: v=2. ans = 1 + 0 = 1. Matches.
k=5: v=1. ans = 1 + 4 = 5. Matches.

Perfect.

Sample 3:
N=7, M=7, A=[0,1,2,3,4,5,6]
inv(0) = 0 (sorted).

change[v]:
v=0: pos=[1]. c=1. change = 2*1 - 7 - 2 + 1 = 2-9+1=-6.
v=1: pos=[2]. change = 4-9+1=-4.
v=2: pos=[3]. change = 6-9+1=-2.
v=3: pos=[4]. change = 8-9+1=0.
v=4: pos=[5]. change = 10-9+1=2.
v=5: pos=[6]. change = 12-9+1=4.
v=6: pos=[7]. change = 14-9+1=6.

k=0: 0
k=1: v=6, ans=0+6=6. Matches.
k=2: v=5, ans=6+4=10. Matches.
k=3: v=4, ans=10+2=12. Matches.
k=4: v=3, ans=12+0=12. Matches.
k=5: v=2, ans=12-2=10. Matches.
k=6: v=1, ans=10-4=6. Matches.

All samples match.

Implementation details:
- Use 1-indexed positions for A.
- Compute inv(0) using BIT: iterate i=1..N, query BIT for sum of values > A_i, then update BIT at A_i.
- Precompute change[v] for v=0..M-1.
- Compute ans array.

Edge cases:
- M=1: only k=0. B_i = A_i mod 1 = 0. inv=0.
- N=1: inv=0 always.

The algorithm handles these.

Time complexity: O(N log M + M).
Space: O(N + M).

This is efficient enough for N, M <= 2e5.