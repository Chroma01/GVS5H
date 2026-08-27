We need to compute, for each shift `k` (0..M-1), the inversion count of `B_i = (A_i + k) mod M`. A naive recomputation per k is O(NM). Since N, M ≤ 2e5, we need an O((N+M) log M) solution.

The key observation: for any pair (i, j) with i < j, the order of `B_i` and `B_j` depends only on the relative values of `A_i` and `A_j` and on the shift `k`. Specifically, for shift `k`, we add `k` to both then take `mod M`. The relative cyclic order is preserved but possibly with a "wrap-around" at 0.

We can compute the inversion count for `k = 0` using a Fenwick tree over the value range [0, M-1]. Then, for each increment of k by 1, we can update the answer in O(log M) by considering the effect of elements wrapping from `M-1` to `0`.

**Transition from k to k+1:**
- Elements that were `M-1` become `0`: they move from being "largest" to "smallest".
- For each value `v`, its new value is `(v+1) mod M`.

Effect on inversions:
- The count of "ordered pairs" where the value difference changes sign due to wrap.

We can maintain a data structure tracking the distribution of A values. Using a Fenwick tree (BIT) that stores frequencies, we can compute:
- `L` = number of elements that will wrap (value `M-1`).
- `W` = number of elements that become the new smallest (after wrap).
- For each wrap-around, pair inversions change.

Actually, the standard approach for this "shifts" problem is:
- For k=0, compute inversion count using BIT.
- For each step k -> k+1:
  - Let `cnt = frequency of M-1` (elements that are about to wrap).
  - The number of inversions increases by `(N - cnt)` (since these elements become smallest, they will now be smaller than all other N-cnt elements that remain larger).
  - Then decreases by `cnt - 1`? No, let's think carefully.

Actually, we can derive: when we add 1 modulo M, for an element with value v, new value is v+1 if v < M-1, else 0.
- Pairs where both have v < M-1: order preserved, no change.
- Pairs where both have v = M-1: order preserved (both become 0), no change.
- Pairs where one is M-1 and other is not: order flips (since M-1 > anything, but after shift 0 < anything). This contributes +1 inversion per such pair (since it was 0, becomes 1).

So if `cnt` = number of M-1 elements, `N - cnt` = other elements, then:
- Number of pairs that flip: `cnt * (N - cnt)`.
- Inversion count changes by `+cnt * (N - cnt)`.

Wait, but we also need to consider elements that were 0 becoming 1, etc. Their relative order with each other is preserved. Only pairs with one M-1 and one not-M-1 change.

So `inv(k+1) = inv(k) + cnt * (N - cnt)`.

But we also need to update the frequencies for the next step: elements with value v become value (v+1) mod M. So we need a way to shift frequencies.

We can maintain a circular array. The key insight: the formula `inv(k+1) = inv(k) + cnt * (N - cnt)` where `cnt` is the count of elements currently equal to the value that is about to wrap (i.e., the maximum value among current A_i + k mod M? No, it's the count of value M-1 in the current shifted array, which is the count of original A_i such that (A_i + k) mod M = M-1, i.e., A_i = (M-1 - k) mod M).

So we can iterate k = 0 to M-1:
- cnt = number of A_i equal to (M-1 - k) mod M.
- Update inv.
- Decrement the count for that value (since after shift, those elements are no longer M-1; they become 0).

We can precompute the frequency array `freq[0..M-1]` of original A. Then we process k from 0 to M-1:
- `v = (M-1 - k) mod M` (but careful: k from 0..M-1, we want the value that is M-1 at shift k).
- For shift k, the elements that are M-1 are those with original A_i = (M-1 - k) mod M.
- Wait: B_i = (A_i + k) mod M = M-1 implies A_i = (M-1 - k) mod M.
- So `cnt = freq[(M-1 - k) mod M]`.
- Then `inv[k+1] = inv[k] + cnt * (N - cnt)`.
- Then decrement `freq[(M-1 - k) mod M]` by `cnt` (i.e., set to 0) because after shift, they become 0, not M-1.

But we also need to consider that the distribution of values changes. Actually, the frequency array represents the multiset of A_i. At step k, the multiset of B_i is just a shifted version of A_i. So if we know the frequency of each value in the current B, we can compute cnt = freq_B[M-1] = freq_A[(M-1 - k) mod M].

So we can precompute `base_freq` of A. Then for each k, we look up `cnt = base_freq[(M-1 - k) mod M]`, update inv, and conceptually "use up" those cnt elements (since after shift they are 0, and in the next step, the element that wraps is different).

But wait: for the next step (k+1), the value that wraps to 0 is M-1, which corresponds to original A_i = (M-1 - (k+1)) mod M. That's a different set of elements. So yes, the frequency of M-1 at step k+1 is `base_freq[(M-1 - (k+1)) mod M]`.

So we can compute:
```
inv = 0
for i in range(N):
    inv += i - query(A[i] + 1)  # number of previous elements > A[i]
    update(A[i], 1)
```
But that's for k=0. For general k, we want inversion count of (A_i + k) mod M.

We can use the property: (A_i + k) mod M = A_i + k if A_i + k < M, else A_i + k - M.

This is similar to the "shifts" problem (e.g., AtCoder ABC 274 F? No, this is like ABC 268 F? Actually, this is exactly the problem "Shift" or "Inversions after shift").

I recall a known solution: 
- Sort the array A.
- For k=0, compute inv0 using BIT on original A.
- Then for k from 1 to M-1:
  - Let x = number of A_i such that A_i + k >= M, i.e., A_i >= M - k.
  - Then inv_k = inv_{k-1} + (N - x) - x? Or something.

Wait, I need to derive carefully.

Consider the sequence B^(k) where B_i^(k) = (A_i + k) mod M.
For a fixed pair i < j, when does the order of B_i and B_j flip as k increases by 1?
- It flips exactly when one of them wraps (i.e., A_i + k >= M or A_j + k >= M) and the other doesn't.
- More precisely: For a given k, B_i = A_i + k if A_i + k < M, else A_i + k - M.
- The condition B_i > B_j depends on whether they wrap.

Alternatively, we can think: For k=0, we have sequence A. For k=1, we add 1 to each, but if it reaches M, it becomes 0. So relative order changes only for pairs where exactly one wraps.

As k increases from 0 to M-1, each element wraps exactly once (when k + A_i >= M). So over the whole process, each pair's order flips exactly once if they have different wrap times? No.

Actually, for a fixed pair (i, j), as k goes 0..M-1, B_i and B_j are both shifted. The difference B_i - B_j (mod M) is (A_i - A_j) mod M? No, B_i - B_j = (A_i - A_j) mod M, but that's the cyclic distance. Wait: (A_i + k) - (A_j + k) = A_i - A_j, but if we consider them as integers in [0, M-1], then B_i = A_i + k - M * [A_i + k >= M]. So B_i - B_j = (A_i - A_j) - M * ([A_i + k >= M] - [A_j + k >= M]).
So the integer difference changes by multiples of M.

The inversion condition B_i > B_j (as integers) is true unless B_i = B_j (which can only happen if A_i = A_j and same wrap, but since A_i, A_j are fixed, if A_i != A_j, they never become equal because difference is at most M-1 in absolute value, and the shift by M is either 0 or ±M, so the integer order can flip).

Specifically, if A_i < A_j, then initially B_i < B_j. As k increases, at some point B_i might wrap (become 0) while B_j hasn't, then B_i > B_j (inversion). Then later B_j also wraps and they both become small, but the order may restore? Let's check: if A_i < A_j, and both wrap at different times. Suppose A_i wraps first (at k = M - A_i), then B_i becomes 0, B_j = A_j + k (which is >0). So B_i < B_j still? 0 < something. So no inversion. Wait, that suggests that wrapping doesn't create inversion from smaller to larger, but rather from larger to smaller.

Actually, if A_i > A_j, then initially B_i > B_j. When B_i wraps (becomes 0) while B_j hasn't, then B_i < B_j, so the inversion is lost. When B_j wraps later, B_j becomes 0, B_i is still 0? No, B_i is 0 too (since it wrapped earlier and then increased). So they are both small. So the order is restored? Not exactly: after both wrap, B_i and B_j are both 0 + (k - wrap_time). Since A_i > A_j, A_i wraps earlier (at larger k? Wait: A_i wraps when A_i + k >= M, i.e., k >= M - A_i. Since A_i > A_j, M - A_i < M - A_j, so A_i wraps at smaller k. So at k = M - A_i, A_i becomes 0, A_j is A_j + k = A_j + M - A_i = M - (A_i - A_j) > 0. So B_i = 0, B_j = M - (A_i - A_j). Since A_i > A_j, A_i - A_j > 0, so B_j > 0, so B_i < B_j. Initially B_i > B_j. So at the moment A_i wraps, the inversion is lost. At k = M - A_j, A_j wraps, becomes 0. At that point, B_i = A_i + k - M = A_i + (M - A_j) - M = A_i - A_j > 0. B_j = 0. So B_i > B_j again! So the inversion is restored. So actually, for a pair with A_i > A_j, the inversion count for that pair is 1 except in the interval between M - A_i and M - A_j - 1? Let's see: from k = M - A_i to k = M - A_j - 1, B_i < B_j. At k = M - A_j, B_i > B_j again. So the inversion is lost only for a contiguous range of k values of length (M - A_j) - (M - A_i) = A_i - A_j. So the number of k for which the pair is inverted is M - (A_i - A_j).

This is the key insight! For a pair (i, j) with i < j (but actually position doesn't matter for the value difference, only the values matter), if we let d = (A_i - A_j) mod M, but actually the difference in the "phase" matters.

Wait, the above analysis assumed A_i > A_j. If A_i < A_j, then initially no inversion. When A_i wraps (at k = M - A_i, which is larger than M - A_j since A_i < A_j), at that point B_i = 0, B_j = A_j + (M - A_i) - M = A_j - A_i > 0. So B_i < B_j still. When A_j wraps earlier? No, A_j wraps at M - A_j which is smaller. At that time, B_j = 0, B_i = A_i + (M - A_j) = M - (A_j - A_i) > 0. So B_i > B_j, so inversion appears! So for A_i < A_j, inversion appears at k = M - A_j and remains until A_i wraps? At k = M - A_i, both are 0 + something? Actually at k = M - A_i, B_i becomes 0, B_j is 0 + (A_j - A_i) = A_j - A_i > 0. So B_i < B_j again. So inversion exists for k in [M - A_j, M - A_i - 1]. Length is (M - A_i) - (M - A_j) = A_j - A_i. So number of k with inversion is A_j - A_i.

So in summary, for a pair (i, j), the number of shifts k (0 <= k < M) for which they form an inversion is:
- If we consider the cyclic order, the number of k such that (A_i + k) mod M > (A_j + k) mod M.
This is exactly the number of k where the "wrapped" value of i is greater than j.
This is known: the number of k is min((A_i - A_j) mod M, (A_j - A_i) mod M)? No, from above:
- If A_i > A_j: inversion count = M - (A_i - A_j).
- If A_i < A_j: inversion count = A_j - A_i.

Wait, for A_i > A_j: inversion count = M - (A_i - A_j). For A_i < A_j: inversion count = A_j - A_i. These are symmetric? Not exactly: M - (A_i - A_j) vs A_j - A_i. If A_i < A_j, then A_j - A_i is positive, and M - (A_i - A_j) would be M + (A_j - A_i) > M, which is not in range. So the formula is: inversion count for pair = (A_j - A_i) mod M? Let's test:
- If A_i > A_j: (A_j - A_i) mod M = M - (A_i - A_j). Yes.
- If A_i < A_j: (A_j - A_i) mod M = A_j - A_i. Yes.
So for any pair (i, j), the number of k in [0, M-1] such that B_i^(k) > B_j^(k) is exactly (A_j - A_i) mod M.

That's beautiful! So the total inversion count for shift k is:
inv_k = sum_{i < j} [ (A_i + k) mod M > (A_j + k) mod M ]
We can also write it as:
inv_k = sum_{i < j} [ ((A_j - A_i) mod M) > something? No.

Alternatively, we can think of it as: For a fixed k, the condition is (A_i + k) mod M > (A_j + k) mod M.
This is equivalent to: (A_i - A_j) mod M is in some set? Actually, (A_i + k) mod M > (A_j + k) mod M iff (A_i - A_j) mod M is such that adding k to both doesn't cross the boundary in a way that flips order.

We can compute inv_k efficiently using a BIT on the values, but we need to do it for all k. The known approach is:
- Sort the array.
- For k=0, compute inv0 using BIT (or merge sort) on the original values.
- Then for k=1 to M-1, we can update using the counts of values.

Specifically, consider going from k to k+1.
- The new sequence is (A_i + k + 1) mod M = ( (A_i + k) mod M + 1 ) mod M.
- So we are adding 1 modulo M to each element of the sequence at step k.
- How does the inversion count change when we add 1 mod M to every element of a sequence?
- Let S be a multiset of values. The new multiset S' is S shifted by 1 mod M.
- The number of inversions of S' can be computed from S and the shift.

Actually, if we have a sequence, not just a multiset, the order matters. But the values are attached to positions. The relative order of two elements i < j depends on their values.

We can use the fact that the inversion count of a sequence depends only on the multiset of values and the order. But when we shift all values by 1 mod M, the relative order of any two elements changes only if the boundary is crossed between them. That is, if one value is M-1 and the other is not, then their order flips. If both are M-1 or both are not M-1, order is preserved.

Wait, is that true? If we have a sequence, and we add 1 mod M to each element, then for a pair (i, j), the new values are (v_i + 1) mod M and (v_j + 1) mod M. The condition (v_i + 1) mod M > (v_j + 1) mod M is equivalent to v_i > v_j unless the addition of 1 causes one to wrap and the other not. Specifically:
- If v_i = M-1 and v_j != M-1, then (v_i+1) mod M = 0, (v_j+1) mod M = v_j+1 > 0, so new value of i is less than new value of j. So if originally v_i > v_j (which is true since v_i = M-1 >= v_j), then after shift, v_i < v_j. So the inversion is lost.
- If v_i != M-1 and v_j = M-1, then originally v_i < v_j. After shift, v_i+1 > 0 = (v_j+1) mod M, so v_i > v_j. So inversion is gained.

So indeed, for each pair (i, j), the inversion status flips if and only if exactly one of them equals M-1.

Thus, if we let `cnt = number of occurrences of M-1 in the current sequence`, then the number of pairs that flip is `cnt * (N - cnt)`. And the change in inversion count is: for pairs (i, j) with i < j, we need to count those where exactly one is M-1. But the formula `cnt * (N - cnt)` counts all unordered pairs, but we need ordered pairs with i < j. However, since the number of M-1 elements is `cnt`, and there are `N - cnt` others, the number of ordered pairs (i, j) with i < j where exactly one is M-1 is `cnt * (N - cnt)`? Not exactly: it's the number of pairs where one is M-1 and one is not, regardless of order. Since for each M-1 element, it pairs with each non-M-1 element. So yes, it's `cnt * (N - cnt)` unordered pairs. But in the sequence, each unordered pair corresponds to exactly one ordered pair (i, j) with i < j. So yes, the change is `cnt * (N - cnt)`.

But wait: we also need to know the sign of the change. If a pair had v_i > v_j and i < j, it was an inversion. After shift, if v_i = M-1 and v_j != M-1, then new v_i < new v_j, so it is no longer an inversion. So we lose an inversion. If v_i != M-1 and v_j = M-1, then originally v_i < v_j (not inversion), after shift v_i > v_j (inversion). So we gain an inversion. So in both cases, the change in inversion count is: for pairs where the M-1 element is the larger index j, we gain; where it's the smaller index i, we lose. The net change depends on the positions of M-1 elements relative to non-M-1 elements.

So it's not just `cnt * (N - cnt)`, we need to know how many M-1 elements are before non-M-1 elements, etc.

Specifically, for each non-M-1 element, count how many M-1 elements are before it (these become non-inversions) and how many are after it (these become inversions). The net change is (number of M-1 after non-M-1) - (number of M-1 before non-M-1) = (total M-1 * (N - cnt)) - 2 * (number of M-1 before non-M-1)? No.

Let `pos_M` be the set of indices of M-1 elements. For each non-M-1 element at index j, the number of M-1 elements before j is `|{i in pos_M: i < j}|`. The number of M-1 after is `cnt - that`. The net change from all such j is sum over non-M-1 j of ( (cnt - before) - before ) = sum (cnt - 2*before). This is (N - cnt)*cnt - 2 * (number of pairs (i, j) with i < j, i is M-1, j is not M-1). But note that "before" for non-M-1 j is the count of M-1 i < j. So sum over j (non-M-1) of before = number of pairs (i, j) with i < j, i in pos_M, j not in pos_M. Let's call this `pairs_before`. Then net change = (N - cnt)*cnt - 2 * pairs_before.

But we also have to consider the case where both are M-1: no change. And both non-M-1: no change.

So the change is:
inv_{k+1} = inv_k + (number of new inversions created) - (number of inversions lost)
= inv_k + (number of pairs (i, j) with i < j, i not M-1, j is M-1) - (number of pairs (i, j) with i < j, i is M-1, j not M-1)
= inv_k + (cnt * (N - cnt) - pairs_before) - pairs_before
= inv_k + cnt * (N - cnt) - 2 * pairs_before

So we need to know `pairs_before` at each step: the number of pairs where the M-1 element is before the non-M-1 element.

Alternatively, we can maintain the sequence and update efficiently? But updating the positions of M-1 elements each step is expensive.

Another approach: The total inversion count for shift k is:
inv_k = sum_{i < j} I( (A_i + k) mod M > (A_j + k) mod M )

We can use a different representation. Since the values are in [0, M-1], we can think of the sequence as a string of characters. The operation is adding k modulo M to each character.

We can use the fact that inv_k can be computed from inv_0 and the shifts. Specifically, we can compute the number of inversions for k=0 using BIT. Then for each k, we can update using the count of elements that wrap.

But we need to track the positions of the elements that will wrap. That is, at step k, the elements that equal M-1 are those with original A_i = (M-1 - k) mod M. We can precompute the positions for each value.

Let `pos[v]` be the list of indices where A_i = v.
At step k, the M-1 elements are those with A_i = (M-1 - k) mod M. Let `v_k = (M-1 - k) mod M`.
We need to compute, for the sequence at step k (which is the original sequence shifted by k), the number of M-1 elements that appear before non-M-1 elements. This is equivalent to: for each index j where A_j != v_k, count how many indices i < j have A_i = v_k. So it's the number of pairs (i, j) with i < j, A_i = v_k, A_j != v_k.

We can precompute for each value v, and for each k, the number of such pairs. But that's O(M^2).

We need a smarter way.

Alternative approach: Since N, M <= 2e5, we can use offline queries? Actually, we can process k from 0 to M-1 and maintain a BIT that tracks the current sequence's values? But updating all values each step is O(NM).

Wait, the known solution for this type of problem (e.g., AtCoder ABC 274 F? No, this is like "Shift" problem) is to use the fact that we can sort the values and use a Fenwick tree to compute the initial inversions, then use a formula involving the number of elements that are "large" and "small".

I recall a solution: 
- Sort A.
- For k=0, compute inv0.
- For k from 1 to M-1:
  - Let x = number of A_i such that A_i + k >= M, i.e., A_i >= M - k.
  - Then inv_k = inv_{k-1} + (N - 2*x)? Or something.

Let's derive the change from k to k+1 using the sorted array.
At step k, the sequence is (A_i + k) mod M. The values are in [0, M-1].
The number of elements with value >= M - k? No, that depends on k.

Actually, note that (A_i + k) mod M >= M - k iff A_i + k >= M - k, i.e., A_i >= M - 2k. That's not constant.

Wait, maybe we should use the complement: think of the number of elements that are "small" after shift.

Another idea: For each k, we can compute inv_k by:
inv_k = total pairs - (number of non-inversions)
But non-inversions include equal values and smaller ones.

We can use the fact that (A_i + k) mod M > (A_j + k) mod M is equivalent to: the cyclic order is such that A_i is "ahead" of A_j in the circle? Not exactly.

I think the most straightforward efficient solution is:
1. Compute inv_0 using a BIT (or merge sort) on the original A.
2. For k from 1 to M-1, update using:
   - Count the number of elements that wrap around (i.e., become smaller than they were).
   - Use a second BIT or some data structure to track the number of elements before each position.

But maintaining positions is hard because the "value" changes, not the position.

Wait, the positions are fixed! The sequence is always (A_1 + k) mod M, (A_2 + k) mod M, ..., (A_N + k) mod M. So the i-th element is always based on A_i. The relative order of the values changes with k, but the underlying A_i is fixed.

So we can think of each A_i as having a "phase" or something.

We can compute the inversion count for each k by:
inv_k = sum_{i=1}^N (number of j > i such that (A_j + k) mod M < (A_i + k) mod M)

For a fixed i, as k increases, the condition (A_j + k) mod M < (A_i + k) mod M changes at certain k. Specifically, it changes when either A_i + k or A_j + k crosses M.

This is similar to the "number of inversions after adding a constant modulo" problem.

I recall a solution that uses the following:
- Preprocess the array A.
- For k=0, compute inv0.
- For k=1 to M-1:
  - The number of elements that are "large" (>= M - k) is some value.
  - Use a data structure to update.

But let's look for a pattern. Consider the sample 3:
N=7, M=7, A=0,1,2,3,4,5,6.
inv0 = 0.
inv1: A+1 = 1,2,3,4,5,6,0. Inversions: pairs where i<j and B_i > B_j. The 0 is at the end, so it creates 6 inversions (with 1,2,3,4,5,6). So inv1 = 6.
inv2: A+2 = 2,3,4,5,6,0,1. The 0 is at position 6, 1 at position 7. Inversions: 0 is less than nothing after it? Actually, 0 is at index 6: pairs (6,7) with 0<1, no. 1 is at index 7: no. But the 0 and 1 are at the end, so they are smaller than the first 5? Wait, the sequence is 2,3,4,5,6,0,1. The inversions are pairs (i,j) with i<j and B_i > B_j. For i=1..5, B_i > 0 and >1, so each of the first 5 elements forms an inversion with both 0 and 1? That would be 5*2 = 10. But the sample says 10. So inv2=10.
inv3: 3,4,5,6,0,1,2. First 4 elements > 0,1,2. So 4*3 = 12. Sample 12.
inv4: 4,5,6,0,1,2,3. First 3 > last 4. So 3*4 = 12.
inv5: 5,6,0,1,2,3,4. First 2 > last 5: 2*5=10.
inv6: 6,0,1,2,3,4,5. First 1 > last 6: 1*6=6.

Pattern: inv_k = k * (M - k) for k=0..M? For M=7:
k=0: 0
k=1: 1*6=6
k=2: 2*5=10
k=3: 3*4=12
k=4: 4*3=12
k=5: 5*2=10
k=6: 6*1=6
Yes! So for this particular sorted array, inv_k = k*(M-k) mod? Actually, it's exactly that.

In general, for any A, we can compute inv_k by:
inv_k = sum_{i=1}^N (number of j such that j > i and (A_j + k) mod M < (A_i + k) mod M)

We can rewrite the condition:
(A_j + k) mod M < (A_i + k) mod M
iff (A_j - A_i + k) mod M < k? No.
Let's set x = A_i, y = A_j.
We want to know for given x, y (with x, y in [0,M-1]) and k in [0,M-1], when is (y+k) mod M < (x+k) mod M.
Let d = (y - x) mod M. Then (y+k) mod M = (x + d + k) mod M.
So condition: (x + d + k) mod M < (x + k) mod M.
This is equivalent to: when you add d to (x+k) mod M, you get a smaller value mod M. This happens iff (x+k) mod M is in [0, M-1-d]. So the condition depends on (x+k) mod M.

Alternatively, the condition (y+k) mod M < (x+k) mod M is equivalent to: the interval [ (x+k) mod M, (y+k) mod M ) wraps around? Not helpful.

We can use the fact that for fixed x and y, the set of k for which (x+k) mod M > (y+k) mod M is exactly an interval of length (x - y) mod M? As derived earlier: number of k is (x - y) mod M. So for a given pair (i, j) with values x = A_i, y = A_j, the pair contributes 1 to inv_k for exactly (A_i - A_j) mod M values of k.

Thus, the total inv_k = sum_{i < j} I( (A_i + k) mod M > (A_j + k) mod M ) = sum_{i < j} c_{ij}(k), where c_{ij}(k) is 1 for k in some interval.

We can compute inv_k by iterating over all pairs? No, N up to 2e5.

We need a way to compute the sum over all pairs efficiently for each k.

Since each pair contributes a contiguous block of k values (of length (A_i - A_j) mod M) where they are inverted, we can think of inv_k as a function that is a sum of many step functions. We can use a difference array approach: for each pair, add +1 to inv_k for k in a certain range. But there are O(N^2) pairs.

We need to use the structure of the pairs. The length of the interval depends only on the difference of values, not on the positions? But the positions determine which pairs are considered (i < j). So the sum is over all ordered pairs (i, j) with i < j.

We can separate the pairs by their value difference. Let’s count for each possible value difference d (where d = (A_i - A_j) mod M, with A_i > A_j possibly), the number of pairs (i, j) with i < j and A_i - A_j = d (mod M). But A_i and A_j are in [0, M-1], so the difference mod M is just an integer in [0, M-1]. However, the actual difference A_i - A_j (as integers) is not necessarily d; d is the "cyclic distance".

But from earlier, the number of k for which (A_i + k) mod M > (A_j + k) mod M is exactly d = (A_i - A_j) mod M. Note that if A_i > A_j, then d = A_i - A_j. If A_i < A_j, then d = M - (A_j - A_i). So d can be thought of as the "forward distance" from A_j to A_i in the cyclic order.

So for a pair (i, j) with i < j, let d = (A_i - A_j) mod M. Then the pair is inverted for k in the set {0, 1, ..., d-1}? Or some other range? Let's check with the earlier interval analysis.

For A_i > A_j: d = A_i - A_j. The inversion exists for k in [0, M - d - 1]? Wait, earlier we said for A_i > A_j, the inversion is lost for k in [M - A_i, M - A_j - 1], which has length A_i - A_j = d. So the inversion exists for k in [0, M - A_i - 1] union [M - A_j, M-1]. That's two intervals? Actually, the complement of [M - A_i, M - A_j - 1] in [0, M-1] is [0, M - A_i - 1] and [M - A_j, M-1]. Total length M - (A_i - A_j) = M - d. So the pair is inverted for M - d values of k, and not inverted for d values of k. Which is it? Earlier we said: for A_i > A_j, the inversion count is M - (A_i - A_j) = M - d. So the number of k with inversion is M - d. So the pair is inverted for k in a set of size M - d. But is it a single interval? From the analysis: at k=0, inversion exists. It is lost when A_i wraps (k >= M - A_i). It is regained when A_j wraps (k >= M - A_j). So the inversion exists for k in [0, M - A_i - 1] and [M - A_j, M-1]. That's two intervals! Their total length is (M - A_i) + (M - (M - A_j)) = M - A_i + A_j = M - d. So indeed, it's not a single interval; it's two intervals.

But wait, the problem asks for inv_k for k=0,1,...,M-1. So we need to compute the sum over pairs of the indicator for each k.

We can use a BIT or segment tree to add contributions? The number of pairs is O(N^2), but we can group them by the values.

Let’s define for each value v, the list of positions where A_i = v.
For a pair (i, j) with A_i = x, A_j = y, the condition for k is as above.
We can compute inv_k by iterating over k and using a BIT on the positions? Since the sequence is fixed positions, we can compute for each k the number of inversions by scanning the sequence? That's O(MN) if we do it naively.

But we can use the fact that the sequence at step k is just the original sequence with values shifted. The inversion count of a sequence can be computed by a BIT over values, but we need to do it for each k. However, we can update the BIT efficiently if we can track how the frequencies change.

At step k, the value at position i is (A_i + k) mod M. So the frequency of value v in the sequence is the number of i such that (A_i + k) mod M = v, i.e., A_i = (v - k) mod M. So the frequency of v at step k is the original frequency of (v - k) mod M.

Thus, if we let `freq[v]` be the frequency of value v in the original array, then at step k, the frequency of value v is `freq[(v - k) mod M]`.

Now, the inversion count of a sequence depends not only on the frequencies of values, but also on the order of values. However, the order of values in the sequence is determined by the original order of A_i, but mapped to new values.

We can think of the sequence as: for each position i, the value is f_i(k) = (A_i + k) mod M. As k increases, each f_i increases by 1 modulo M.

We can maintain the inversion count as k increases. When k increases by 1, each f_i increases by 1. For two positions i < j, the order of f_i and f_j changes if and only if the addition of 1 causes one to wrap and the other not. That is, if exactly one of f_i, f_j equals M-1. So at step k, the elements that are M-1 are those with (A_i + k) mod M = M-1, i.e., A_i = (M-1 - k) mod M. Let `cnt = number of i with A_i = (M-1 - k) mod M`. As derived, the change in inversion count is:
inv_{k+1} = inv_k + (number of new inversions) - (number of lost inversions)
= inv_k + (number of pairs (i, j) with i < j, f_i != M-1, f_j = M-1) - (number of pairs (i, j) with i < j, f_i = M-1, f_j != M-1)

Let `L` be the number of M-1 elements that appear before non-M-1 elements (i.e., pairs where M-1 is the first element). Let `R` be the number of M-1 elements that appear after non-M-1 elements (i.e., pairs where M-1 is the second element). Note that L + R = cnt * (N - cnt). And the change is R - L.

So we need to compute L and R efficiently for each k. That is, given the set of positions where A_i = v_k (where v_k = (M-1 - k) mod M), we need to know how many of these positions are before the other elements, and how many are after.

This is equivalent to: for the set S = {i : A_i = v_k}, we need to count sum_{i in S} (number of j > i with A_j != v_k) - sum_{i in S} (number of j < i with A_j != v_k). Actually, R = number of pairs (i, j) with i not in S, j in S, i < j. L = number of pairs (i, j) with i in S, j not in S, i < j. So R - L = (number of non-S elements before S elements) - (number of S elements before non-S elements). This is like the "imbalance" of S relative to the rest.

We can precompute for each position i, the number of elements before it and after it that are of a certain value? But v_k changes each step.

We can use a BIT over positions to maintain the current "state"? But the state changes: at step k, we need to know L and R for the set S_k = {i : A_i = v_k}. But note that S_k for different k are disjoint? Because v_k = (M-1 - k) mod M, and as k runs from 0 to M-1, v_k takes all values 0..M-1 exactly once. So the sets S_k partition the positions! Indeed, each position i belongs to exactly one S_k, corresponding to k = (M-1 - A_i) mod M.

So at step k, the M-1 elements are exactly the set S_k. And after step k, we move to step k+1, and the M-1 elements become S_{k+1}.

So we can precompute for each value v, the set of positions where A_i = v. Then at step k, v_k = (M-1 - k) mod M. We need to compute, for the set S_{v_k}, the number of elements of S_{v_k} that are before elements not in S_{v_k}, and the number after. This is equivalent to: for each i in S_{v_k}, let left = number of j < i with j not in S_{v_k}, and right = number of j > i with j not in S_{v_k}. Then L = sum_{i in S} left, R = sum_{i in S} right. And R - L = sum_{i in S} (right - left) = sum_{i in S} ( (N - |S| - i + 1) - (i - 1 - (|S| - rank))? Not simple.

Alternatively, we can compute the net contribution of set S to the inversion count change as:
For each i in S, the contribution to the change is: (number of j > i, j not in S) - (number of j < i, j not in S). So if we let `pos` be the sorted list of positions in S, and for each i in S, let `before = i - 1 - (number of elements in S before i)`, and `after = N - i - (number of elements in S after i)`. Then the contribution of i is `after - before`. Summing over i in S gives the total change.

But we can precompute for each position i, some values? However, the set S changes, and we need to do this for all k. We can do it by maintaining a data structure as we process the values v in some order.

Since the sets partition the positions, we can process the values v in the order of the steps k. That is, we process v from (M-1) down to 0 (since k from 0 to M-1, v_k = (M-1 - k) mod M, so v goes M-1, M-2, ..., 0). For each v, we need to compute the effect of having these elements wrap.

We can maintain two BITs or segment trees over the positions to track the number of elements that are "active" (i.e., have been processed or not)? But the effect depends on the current set S relative to all positions.

Let's think of it as: initially, no elements are "wrapped" yet. At step k, the wrapped elements are those with v_k. We want to compute the change in inversion count due to these elements wrapping (i.e., becoming the smallest). But actually, the change from k to k+1 is due to the elements that are M-1 at step k. So we can iterate k from 0 to M-1, and for each k, we look at the set S_k, and update the answer.

We need to compute, for the set S_k, the number of pairs (i, j) with i < j, i in S_k, j not in S_k (which is L) and i not in S_k, j in S_k (which is R). Note that R = |S_k| * (N - |S_k|) - L? Actually, total pairs between S_k and complement is |S_k| * (N - |S_k|). And L + R = that. So R = |S_k| * (N - |S_k|) - L. So we only need L.

L = number of pairs (i, j) with i < j, i in S_k, j not in S_k.
This is equal to: for each i in S_k, count the number of j > i with j not in S_k.
If we know the positions in S_k, we can compute L by iterating over i in S_k and using a BIT to count how many j > i are not in S_k. But if we process all k, we can maintain a BIT that tracks the positions of all elements, and as we process each S_k, we "remove" them or something? Wait, S_k are disjoint, and we process them one by one. For a given S_k, we need to know for each i in S_k, the number of j > i in the complement. If we have a BIT that initially has 1 for all positions, and we remove the elements of S_k? But the complement of S_k is the union of all other S values. If we process values in some order, we can maintain a BIT that tracks which positions are "available" (not yet processed). But the complement of S_k is everything except S_k, which includes both already processed and not yet processed. So we need to distinguish.

Alternatively, we can compute L for all v efficiently by precomputing prefix sums of counts per value.

For each value v, we have a list of positions pos_v. We want to compute L_v = sum_{i in pos_v} (number of j > i with A_j != v).
This is equal to: for each i in pos_v, (N - i) - (number of j > i with A_j = v). So if we know, for each position i, the number of occurrences of the same value after i, we can compute L_v.
We can precompute for each position i, the number of same-valued elements after it. But that depends on the value. We can group by value.

For a fixed v, let the positions be p1 < p2 < ... < p_m. Then for p_t, the number of same value after it is m - t. So L_v = sum_{t=1}^m ( (N - p_t) - (m - t) ) = sum_{t=1}^m (N - p_t) - sum_{t=1}^m (m - t).
The first sum: m*N - sum p_t.
The second sum: sum_{t=1}^m (m - t) = 0+1+...+(m-1) = m*(m-1)/2.
So L_v = m*N - sum_{p in pos_v} p - m*(m-1)/2.

Then the change in inversion count from k to k+1 is:
delta = R - L = (m * (N - m) - L) - L = m*(N-m) - 2L.
Where m = |S_k| = frequency of v_k.
So we can compute L using the formula above! We need for each value v, the sum of positions of that value. And we know m from the frequency.

This is brilliant! We don't need any complex data structure. We just need:
- The frequency `m_v` for each v.
- The sum of positions `sum_pos_v` for each v.

Then at step k, v = (M-1 - k) mod M. We have m = m_v, and L = m * N - sum_pos_v - m*(m-1)/2.
Then delta = m * (N - m) - 2 * L.
And inv_{k+1} = inv_k + delta.

We also need to compute inv_0. We can compute inv_0 using a BIT (Fenwick tree) on the values A_i. Since M <= 2e5, we can do it in O(N log M).

Let's verify with sample 3: A = [0,1,2,3,4,5,6], M=7, N=7.
Frequencies: each m_v = 1.
Sum positions: for v, position is v+1 (1-indexed) or v (0-indexed). Let's use 0-indexed positions: positions 0..6.
sum_pos_v = v.
For k=0, v = (7-1-0) mod 7 = 6. m=1, sum_pos=6.
L = 1*7 - 6 - 0 = 1. (Indeed, the 6 is at position 6, and there is 1 element after it? Actually, L is number of pairs (i in S, j not in S) with i<j. For v=6, S={6}, i=6, j>6: none. Wait, my L formula might be off by index. Let's recalculate carefully.

Positions: let's use 1-indexed for easier arithmetic. N=7, positions 1..7.
A = [1,2,3,4,5,6,7]? Actually sample 3: 0 1 2 3 4 5 6. So A_1=0, A_2=1, ..., A_7=6.
Positions: 1,2,3,4,5,6,7.
For v=6: pos = {7}. m=1.
N - p_t = 7-7=0.
m - t = 0.
So L = sum (0 - 0) = 0. My formula gave L = m*N - sum p - m(m-1)/2 = 1*7 - 7 - 0 = 0. Good.
Then delta = m*(N-m) - 2L = 1*6 - 0 = 6.
inv1 = inv0 + 6. inv0=0, so inv1=6. Correct.

For k=1, v = (6-1) mod 7 = 5. m=1, sum_pos=6.
L = 1*7 - 6 - 0 = 1? Wait, pos for v=5 is 6. m=1, sum_pos=6. L = 7-6-0=1. But is that correct? For v=5, S={6}. Pairs (i in S, j not in S, i<j): i=6, j>6: none. So L should be 0. Why did formula give 1? Let's check the formula: L_v = sum_{i in S} (number of j > i with A_j != v). For i=6, j>6: none. So L=0. But formula: m*N - sum p_t - m(m-1)/2 = 1*7 - 6 - 0 = 1. So there's an off-by-one error. Because positions are 1-indexed, and N is 7, but p_t=6, so N - p_t = 1. But the number of j > 6 is 0. So the formula should be (N - p_t) not (N - p_t) + something? Actually, number of indices j with j > p_t is N - p_t. For p_t=6, N=7, N - p_t = 1. But there is no index 7? Wait, indices are 1..7, so p_t=6, indices >6 are {7}, so there is 1 index. But in the sample, A_7=6, which is the same value! So j=7 has A_j=6, so it is not in the complement. So the number of j > i with A_j != v is (N - p_t) - (number of same values after p_t). That is what I had: (N - p_t) - (m - t). For p_t=6, m=1, t=1, so (7-6) - (0) = 1. But that counts j=7, which has value 6, so it should be excluded. Wait, the number of same values after p_t is m - t. For m=1, t=1, m-t=0. So it doesn't exclude j=7. But j=7 is not after p_t? p_t=6, j=7 is after, so it should be counted if it's same value. But m=1, so there are no same values after. So j=7 is not same value? But A_7=6, same as v. So there is a same value after. Contradiction: for v=5, pos={6}. But A_7=6, not 5. So A_7 != 5. So for v=5, the element at position 7 is not same value. So j=7 is in complement. So L should count j=7? But j=7 is after i=6, and A_7 != 5, so yes, it should be counted. So L = 1. But is that correct? For k=1, the M-1 elements are those with value 5. In the sequence at k=1, B_i = (A_i + 1) mod 7. So the values are: A_1+1=1, A_2+1=2, ..., A_6+1=6, A_7+1=0. So the M-1 elements are those with value 6, which correspond to A_i=5. So S = {i: A_i=5} = {6}. So the M-1 element is at position 6 in the sequence. The complement elements are at positions 1,2,3,4,5,7. Pairs (i in S, j not in S) with i<j: i=6, j=7. Since 7 is in complement, this is a pair. So L=1. R would be pairs (i not in S, j in S) with i<j: i=1..5, j=6. That's 5 pairs. So R=5. Then delta = R - L = 4. But from k=1 to k=2, inv should change from 6 to 10, so delta=4. And m*(N-m) - 2L = 1*6 - 2 = 4. Correct! So the formula works.

So we can compute inv_0 using BIT, then for k=1 to M-1, compute delta using the precomputed m_v and sum_pos_v, and accumulate.

We need to precompute m_v and sum_pos_v for all v in [0, M-1]. We can do that in O(N + M).

Algorithm:
1. Read N, M, and array A (1-indexed).
2. Initialize arrays freq[0..M-1] and sum_pos[0..M-1] to 0.
3. For i from 1 to N:
   v = A[i]
   freq[v] += 1
   sum_pos[v] += i
4. Compute inv0:
   Use a Fenwick tree of size M. For i from 1 to N:
     v = A[i]
     // number of previous elements > v
     inv0 += (i-1) - query(v+1, M-1)  // query sum from v+1 to M-1
     update(v, 1)
   This is O(N log M).
5. Initialize ans[0] = inv0.
6. For k from 1 to M-1:
   v = (M-1 - (k-1)) mod M? Wait, careful: for step k, the M-1 elements are those with value (M-1 - (k-1)) mod M? Let's define:
   At step k (0-indexed), the value that is M-1 is v_k = (M-1 - k) mod M.
   For k=0, v_0 = M-1.
   For k=1, v_1 = M-2.
   ...
   For k=M-1, v_{M-1} = 0.
   The change from k to k+1 is based on v_k.
   So for k from 0 to M-2:
     v = (M-1 - k) mod M
     m = freq[v]
     L = m * N - sum_pos[v] - m*(m-1)/2
     delta = m * (N - m) - 2 * L
     inv_next = inv_current + delta
     ans[k+1] = inv_next
7. Output ans[0..M-1].

We need to ensure we use 64-bit integers (N up to 2e5, M up to 2e5, inversions up to N^2 ~ 4e10, fits in 64-bit).

Let's test with sample 1:
N=3, M=3, A=[2,1,0] (positions 1,2,3).
freq: 0:1 at pos3; 1:1 at pos2; 2:1 at pos1.
sum_pos: 0:3, 1:2, 2:1.
inv0: compute:
i=1, v=2: query(3,2) = 0, inv0=0. update(2).
i=2, v=1: query(2,2) = 1 (since 2>1), inv0=1. update(1).
i=3, v=0: query(1,2) = 2, inv0=3. update(0).
So inv0=3. Correct.
k=0: v= (3-1-0) mod 3? M=3, M-1=2. v = (2 - 0) mod 3 = 2.
m = freq[2] = 1.
sum_pos[2] = 1.
L = 1*3 - 1 - 0 = 2.
delta = 1*(3-1) - 2*2 = 2 - 4 = -2.
inv1 = 3 - 2 = 1. Correct.
k=1: v = (2 - 1) mod 3 = 1.
m = freq[1] = 1, sum_pos[1] = 2.
L = 1*3 - 2 - 0 = 1.
delta = 1*2 - 2*1 = 0.
inv2 = 1 + 0 = 1. Correct.
k=2: v = (2-2) mod 3 = 0.
m=1, sum_pos=3.
L = 3 - 3 - 0 = 0.
delta = 2 - 0 = 2.
inv3 = 1+2=3? But we only need up to M-1=2. So ans[2]=1, then if we did k=2, inv3=3 which is for k=3=0 mod 3, but we don't need it. Actually, we run for k=0 to M-2. So we get ans[1] and ans[2]. ans[0]=3, ans[1]=1, ans[2]=1. Matches sample.

Test sample 2:
N=5, M=6, A=[5,3,5,0,1]
Positions 1..5.
freq: 0:1 (pos4), 1:1 (pos5), 2:0, 3:1 (pos2), 4:0, 5:2 (pos1,3).
sum_pos: 0:4, 1:5, 2:0, 3:2, 4:0, 5:4.
inv0:
i=1, v=5: query(6,5)=0, inv0=0. update5.
i=2, v=3: query(4,5)=1 (5>3), inv0=1. update3.
i=3, v=5: query(6,5)=1, inv0=2. update5.
i=4, v=0: query(1,5)=4, inv0=6. update0.
i=5, v=1: query(2,5)=3 (5,3,5? actually frequencies: 5:2, 3:1, 0:1, so >1: 5,3,0? wait, 0 is not >1. So values >1: 5 (2), 3 (1) =3. So query(2,5)=3. inv0=9.
So inv0=9? But sample says 7. Let's recalculate manually:
A = [5,3,5,0,1]
Pairs: (1,2):5>3 inv
(1,3):5=5 not inv
(1,4):5>0 inv
(1,5):5>1 inv
(2,3):3<5 not
(2,4):3>0 inv
(2,5):3>1 inv
(3,4):5>0 inv
(3,5):5>1 inv
(4,5):0<1 not
Total inversions: (1,2),(1,4),(1,5),(2,4),(2,5),(3,4),(3,5) = 7. My computation gave 9, so error in query.
i=2, v=3: number of previous >3 is only 5? Previous elements: 5. So 1. Correct.
i=3, v=5: previous: 5,3. >5: none? Actually, 5 is not >5. So 0. But I said query(6,5)=1. That's wrong: query(6,5) should be 0 because value 6 doesn't exist. M=6, so values 0..5. v=5, so query(6,5) is empty. I should query from v+1 to M-1. For v=5, v+1=6 > M-1=5, so query(6,5)=0. I mistakenly said 1.
i=4, v=0: previous: 5,3,5. >0: 5,3,5 -> 3. So inv0=1+0+3=4. I said 4, then i=5: v=1, previous: 5,3,5,0. >1: 5,3,5 -> 3. So inv0=4+3=7. Correct. So inv0=7.
Now, k=0: v = (6-1-0) mod 6 = 5.
m = freq[5] = 2, sum_pos[5] = 1+3=4.
L = 2*5 - 4 - 2*1/2 = 10 - 4 - 1 = 5.
delta = 2*(5-2) - 2*5 = 6 - 10 = -4.
inv1 = 7 - 4 = 3. Sample says 3. Correct.
k=1: v = (5 - 1) mod 6 = 4.
freq[4]=0, sum_pos=0.
L = 0*5 - 0 - 0 = 0.
delta = 0*5 - 0 = 0.
inv2 = 3 + 0 = 3. Sample says 3. Correct.
k=2: v = (5-2) mod 6 = 3.
m = freq[3] = 1, sum_pos[3] = 2.
L = 1*5 - 2 - 0 = 3.
delta = 1*4 - 6 = -2.
inv3 = 3 - 2 = 1. Sample says 1. Correct.
k=3: v = (5-3) mod 6 = 2.
m=0, delta=0.
inv4 = 1. Sample says 1. Correct.
k=4: v = (5-4) mod 6 = 1.
m = freq[1] = 1, sum_pos[1] = 5.
L = 1*5 - 5 - 0 = 0.
delta = 1*4 - 0 = 4.
inv5 = 1 + 4 = 5. Sample says 5. Correct.
k=5: v = (5-5) mod 6 = 0.
m = freq[0] = 1, sum_pos[0] = 4.
L = 1*5 - 4 - 0 = 1.
delta = 1*4 - 2 = 2.
inv6 = 5 + 2 = 7 (which is inv0). Correct.

So the algorithm works!

Complexity: O(N log M + M). N, M <= 2e5, so fine.

We need to be careful with modulo for v: (M-1 - k) mod M. In Python, (M-1-k) % M works.

Implementation details:
- Use 0-indexed positions? The formula used 1-indexed. Let's check if we can use 0-indexed to simplify.
If positions are 0-indexed (0 to N-1), then:
For i in S, number of j > i is N-1-i. So L_v = sum_{i in S} ( (N-1-i) - (number of same values after i) ).
Let positions be p_t (0-indexed). Then number of same after = m - t.
So L_v = sum_{t=1}^m (N-1 - p_t) - sum_{t=1}^m (m-t) = m*(N-1) - sum p_t - m(m-1)/2.
Then delta = m*(N-m) - 2L_v.
Let's test with sample 3 using 0-indexed:
N=7, A=[0,1,2,3,4,5,6], pos: 0,1,2,3,4,5,6.
freq[v]=1, sum_pos[v]=v.
k=0: v=6, m=1, sum_pos=6.
L = 1*(7-1) - 6 - 0 = 6-6=0.
delta = 1*6 - 0 = 6. inv1=6. Correct.
k=1: v=5, m=1, sum_pos=5.
L = 1*6 - 5 - 0 = 1.
delta = 6 - 2 = 4. inv2=10. Correct.
k=2: v=4, m=1, sum_pos=4.
L = 6-4=2.
delta = 6-4=2. inv3=12. Correct.
Works.

So we can use 0-indexed positions to avoid +1.

Now, for the BIT: we need to compute inv0. We can do it with a Fenwick tree on the values. Since M up to 2e5, we can use a list of size M+2.

Code outline:
```python
import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    freq = [0] * M
    sum_pos = [0] * M
    for i, v in enumerate(A):
        freq[v] += 1
        sum_pos[v] += i  # 0-indexed position
    # Compute inv0
    bit = [0] * (M + 1)
    def update(i):
        i += 1
        while i <= M:
            bit[i] += 1
            i += i & -i
    def query(i):
        # sum from 0 to i
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    inv0 = 0
    for i, v in enumerate(A):
        # number of previous elements > v
        # total previous = i, number <= v = query(v)
        inv0 += i - query(v)
        update(v)
    ans = [0] * M
    ans[0] = inv0
    cur = inv0
    for k in range(1, M):
        v = (M - 1 - (k - 1)) % M  # this is v_{k-1}
        m = freq[v]
        L = m * (N - 1) - sum_pos[v] - m * (m - 1) // 2
        delta = m * (N - m) - 2 * L
        cur += delta
        ans[k] = cur
    print('\n'.join(map(str, ans)))

solve()
```

Wait, in the loop, for k from 1 to M-1, we need v_{k-1} = (M-1 - (k-1)) mod M.
So for k=1, v0 = M-1. For k=M-1, v_{M-2} = (M-1 - (M-2)) mod M = 1.
Then we don't compute for v_{M-1} because that would give the change to k=M, which is same as k=0. So we only need M-1 steps.

Let's verify the loop bounds:
k=0: ans[0] = inv0
k=1: use v = (M-1 - 0) = M-1
k=2: use v = (M-1 - 1) = M-2
...
k=M-1: use v = (M-1 - (M-2)) = 1
We never use v=0. That's correct because the change from k=M-1 to k=M (which is 0) is based on v=0, but we don't need to compute ans[M] since we wrap around. Actually, we only need ans[0..M-1]. The last computed is k=M-1 using v=1. But what about the change from k=M-1 to k=0? That would be based on v=0. But we don't need ans[M] = ans[0]. So we don't need to compute it. However, is it true that ans[0] is exactly the result of applying the delta from v=0 to the previous? That would require that the sum of all deltas over a full cycle is 0. Let's check: sum_{v=0}^{M-1} delta_v should be 0. We can check: for each pair, the inversion count over k=0..M-1 sums to something? Actually, the total number of inversions over all k is not zero, but the change over a full cycle should bring us back to the same state, so sum delta = 0. Indeed, since after M steps we return to the original sequence, the total change must be 0. So if we computed all M deltas (for v=M-1 down to 0), we would get back to inv0. But we only computed M-1 deltas (for v=M-1 down to 1). The remaining delta for v=0 should be such that inv after M-1 steps + delta_0 = inv0. So our computed cur after M-1 steps is not necessarily inv0. But we don't need it to be; we just need ans[M-1]. So it's fine.

But wait, in the sample 1, M=3. We computed:
k=0: inv0=3
k=1: v=2, delta=-2, inv1=1
k=2: v=1, delta=0, inv2=1
We didn't compute v=0. That's correct.

In sample 2, M=6:
k=0: 7
k=1: v=5, delta=-4, inv1=3
k=2: v=4, delta=0, inv2=3
k=3: v=3, delta=-2, inv3=1
k=4: v=2, delta=0, inv4=1
k=5: v=1, delta=4, inv5=5
We didn't use v=0. Correct.

So the loop `for k in range(1, M): v = (M - 1 - (k - 1)) % M` works.

But note: in Python, `(M-1 - (k-1)) % M` is fine. For k=1: (M-1 - 0) % M = M-1. For k=M-1: (M-1 - (M-2)) % M = 1.

We must ensure that when M=1, the loop doesn't run. For M=1, range(1,1) is empty, so ans[0]=inv0. Correct, since there is only k=0, and B_i = A_i mod 1 = 0 for all, so inversion count is 0. Our inv0 computation should give 0. Let's check: if M=1, A_i are all 0. The BIT will have size 1. For each i, v=0, query(0) returns number of previous elements <=0, which is i. So inv0 += i - i = 0. Good.

Edge cases: N=1. Then for any k, the sequence has 1 element, inversion count is 0. Our algorithm: inv0: i=0, v=A[0], query(v) = 0 if v>0? Actually, for i=0, previous is 0, so inv0 = 0. Then for each k, m = freq[v] = 1 (since N=1, A[0]=0, but M could be larger). Then L = 1*(0) - pos - 0 = -pos? Wait, N=1, so N-1=0. L = m*(N-1) - sum_pos - m(m-1)/2 = 0 - pos - 0 = -pos. delta = m*(N-m) - 2L = 1*0 - 2(-pos) = 2*pos. But pos=0, so delta=0. So cur remains 0. Good.

What if some freq[v] = 0? Then m=0, L=0, delta=0. So it works.

So the solution is correct and efficient.

One more check: the BIT query for inv0: we used `i - query(v)`. This gives the number of previous elements with value > v. Because query(v) gives number of previous elements with value <= v. So that's correct.

Complexity: O(N log M + M). With N, M up to 2e5, it's about 2e5 * log(2e5) ~ 3e6 operations, which is fast.

Now, we need to write the code in Python. Ensure we use sys.stdin for speed.

Let's write the final code.

Note: The problem statement says "Print M lines. The i-th line (1 <= i <= M) should contain the answer for the case k = i-1." So we output ans[0] to ans[M-1] each on a new line.

We should also consider that the values A_i are given as non-negative integers less than M. The sample input has them space-separated.

Code:
```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    freq = [0] * M
    sum_pos = [0] * M
    for i, v in enumerate(A):
        freq[v] += 1
        sum_pos[v] += i  # 0-indexed
    
    # Fenwick tree
    bit = [0] * (M + 1)
    def update(idx):
        idx += 1
        while idx <= M:
            bit[idx] += 1
            idx += idx & -idx
    def query(idx):
        # sum of [0, idx]
        idx += 1
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s
    
    inv0 = 0
    for i, v in enumerate(A):
        inv0 += i - query(v)
        update(v)
    
    ans = [0] * M
    ans[0] = inv0
    cur = inv0
    for k in range(1, M):
        v = (M - 1 - (k - 1)) % M
        m = freq[v]
        L = m * (N - 1) - sum_pos[v] - m * (m - 1) // 2
        delta = m * (N - m) - 2 * L
        cur += delta
        ans[k] = cur
    
    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

solve()
```

We should double-check the formula for L with 0-indexed positions.
For 0-indexed: positions 0..N-1.
For each i in S, number of j > i is (N-1 - i).
Number of same values after i: if positions are sorted, for the t-th element (0-indexed t), there are m - t - 1 same values after? Wait, careful.
If m elements, sorted p_0 < p_1 < ... < p_{m-1}.
For p_t, number of same values after is m - t - 1? Actually, indices of same values after are t+1, t+2, ..., m-1, so count = (m-1) - t.
So L_v = sum_{t=0}^{m-1} [ (N-1 - p_t) - (m-1 - t) ].
= sum (N-1 - p_t) - sum (m-1 - t)
= m*(N-1) - sum p_t - [ m*(m-1) - sum_{t=0}^{m-1} t ]
= m*(N-1) - sum p_t - [ m*(m-1) - m*(m-1)/2 ]
= m*(N-1) - sum p_t - m*(m-1)/2.
Yes, that matches what I had. In the code I used: `m * (N - 1) - sum_pos[v] - m * (m - 1) // 2`. Note: `sum_pos[v]` is sum of positions (0-indexed). `m*(m-1)//2` is integer. So correct.

Test with a small case: N=2, M=5, A=[0,1].
Positions 0,1.
freq[0]=1, sum_pos=0; freq[1]=1, sum_pos=1.
inv0: i=0, v=0: query(0)=0, inv0=0. update0.
i=1, v=1: query(1)=1 (since 0<=1), inv0 += 1 - 1 = 0. So inv0=0.
k=0: ans[0]=0.
k=1: v = (5-1-0) % 5 = 4. freq[4]=0, m=0, L=0, delta=0, cur=0, ans[1]=0.
k=2: v=3, m=0, ans[2]=0.
k=3: v=2, m=0, ans[3]=0.
k=4: v=1, m=1, sum_pos=1, L = 1*(1) - 1 - 0 = 0. delta = 1*(2-1) - 0 = 1. cur=1, ans[4]=1.
So outputs:
k=0: B=(0,1) inv=0
k=1: B=(1,2) inv=0
k=2: B=(2,3) inv=0
k=3: B=(3,4) inv=0
k=4: B=(4,0) inv: 4>0, so 1 inversion. Correct.

Another test: N=2, M=3, A=[1,2] (so positions 0,1).
freq[1]=1 sum=0; freq[2]=1 sum=1.
inv0: i=0, v=1: query(1)=0, inv0=0. update1.
i=1, v=2: query(2)=1 (since 1<=2), inv0 += 1 - 1 = 0. So inv0=0.
k=0: ans[0]=0.
k=1: v=2, m=1, sum=1. L = 1*(1) - 1 - 0 = 0. delta = 1*(1) - 0 = 1. cur=1, ans[1]=1.
k=2: v=1, m=1, sum=0. L = 1*1 - 0 - 0 = 1. delta = 1*1 - 2 = -1. cur=0, ans[2]=0.
So:
k=0: B=(1,2) inv=0
k=1: B=(2,0) inv: 2>0, so 1.
k=2: B=(0,1) inv=0.
Correct.

So the algorithm is solid.

One final check: The BIT query function returns the number of elements <= v. We used `i - query(v)`. This gives number of previous elements with index > v, i.e., value > v. Since the array is processed in order, "previous" means indices < i. So it's correct.

Memory: O(N + M). Fine.

Now, produce the final answer.</mm:think>### PLAN
We need to compute the inversion count for each shift `k` of the sequence `B_i = (A_i + k) mod M`. A naive recomputation per `k` is O(NM), which is too slow. Instead, we compute `inv_0` using a Fenwick tree in O(N log M), then update the answer for each subsequent `k` in O(1) using a formula derived from the change in inversion count when all values are incremented modulo M.

When increasing `k` by 1, only pairs where exactly one element equals `M-1` change their order. For a value `v` with frequency `m` and sum of positions `S`, the number of such pairs where the `M-1` element appears first (i.e., smaller index) is `L = m*(N-1) - S - m*(m-1)/2` (using 0-indexed positions). The net change in inversion count is `delta = m*(N-m) - 2L`. Precomputing `m` and `S` for each value allows O(1) updates per `k`.