
## ideation
The problem asks for the inversion count of B where B_i = (A_i + k) mod M for every k in 0..M-1. Constraints are up to 2e5 for both N and M, so we cannot recompute inversions naively per k (O(N log N * M) is too slow).

**Core difficulty:** When we increment k by 1, the ordering of elements only changes for those A_i that lie in the interval [k, M-1] (the "large" values wrap around to become "small"). The transition formula is well known:

inv(k) = inv(k-1) - 2 * cnt_ge(k) + N

where cnt_ge(k) = number of i with A_i >= k. This is because:
- The N - cnt_ge(k) elements with A_i < k keep their relative order (no wrap).
- The cnt_ge(k) elements with A_i >= k each move from the "right side" to the "left side" of the modulo line, so for each such element, the number of elements now smaller than it decreases by (N - cnt_ge(k)) and the number larger than it increases by (cnt_ge(k) - 1). Net change for each of these cnt_ge(k) elements is (cnt_ge(k)-1) - (N-cnt_ge(k)) = 2*cnt_ge(k) - N. Multiply by cnt_ge gives 2*cnt_ge^2 - N*cnt_ge. Wait, that's not the per-step formula. Let me reconsider.

Actually the simple per-step recurrence is:
When we go from k-1 to k, every element with value A_i = k-1 changes from being at the "high end" to the "low end" (it was A_i >= k-1 and becomes A_i < k). But only the elements with value exactly k-1 change their status, and we can count the change in inversion count using the current frequencies.

The simpler known formula uses: for each k, cnt_ge(k) = number of elements in [k, M-1]. Then:

inv(k) = inv(0) + k*N - 2 * (sum of cnt_ge(j) for j=1..k)

Alternatively, the recurrence inv(k) = inv(k-1) + N - 2*cnt_ge(k) works. Let's verify with the sample.

Sample 1: A=[2,1,0], N=3, M=3.
- inv(0) = 3 (computed: (2,1),(2,0),(1,0))
- k=1: elements >= 1 are all 3. inv(1) = 3 + 3 - 2*3 = 3 + 3 - 6 = 0. But answer is 1. Hmm.

Let me recompute the formula. The classic formula is:
inv(k) = inv(k-1) - 2*cnt_ge(k) + N

For k=1: cnt_ge(1) = number of A_i >= 1 = 2 (A=2,1). inv(1) = 3 - 2*2 + 3 = 3 - 4 + 3 = 2. But answer is 1. Still wrong.

Let me reconsider. Actually the formula in the original solution I've seen is:
inv(k) = inv(k-1) + N - 2 * (number of elements >= k)

Wait, but that's what I had. Let me recompute by hand for sample 1.

A = [2,1,0].
k=0: B = [2,1,0]. Inversions: (1,2):2>1, (1,3):2>0, (2,3):1>0. Total=3. ✓
k=1: B = [0,2,1]. Inversions: (2,3):2>1. Total=1.
k=2: B = [1,0,2]. Inversions: (1,2):1>0. Total=1.

Using formula inv(k) = inv(k-1) + N - 2*cnt_ge(k):
k=1: cnt_ge(1) = #{A_i >= 1} = 2. inv(1) = 3 + 3 - 4 = 2. ✗ (should be 1)

Hmm, formula is off. Let me reconsider.

The correct recurrence is: inv(k) = inv(k-1) + N - 2 * (number of elements with value in [k, M-1]) — but wait, this assumes specific structure. Let me re-derive.

When we go from k-1 to k, the elements that change behavior are exactly those with A_i = k-1. But actually the simpler view:

For each k, define S_k = {i : A_i >= k}. |S_k| = cnt_ge(k).

The number of inversions in B(k) is:
inv(k) = sum over pairs (i,j), i<j of [B_i(k) > B_j(k)]

Case 1: A_i, A_j both < k. Then B_i = A_i+k, B_j = A_j+k, and B_i > B_j iff A_i > A_j.
Case 2: A_i, A_j both >= k. Then B_i = A_i+k-M, B_j = A_j+k-M, and B_i > B_j iff A_i > A_j.
Case 3: A_i < k <= A_j. Then B_i = A_i+k (in [k, k+M-1] but since A_i<M, B_i in [k, M-1+k]... wait, A_i+k could be >= M). Hmm, actually A_i < k and k <= M, so A_i+k < 2k <= 2M-1. But we take mod M. B_i = A_i+k if A_i+k < M, else A_i+k-M. Since A_i < k, A_i+k < 2k. If k <= M/2 this is < M, but generally could be >= M.

OK the case analysis gets complex. Let me look up the standard result.

The standard result for "cyclic shift" inversion is:
inv(k) = inv(0) + k*N - 2 * (sum_{i : A_i < k} A_i)  — no that's not right either.

Actually the correct formula I recall is:
inv(k) = inv(k-1) + N - 2 * (number of elements with A_i >= k)

Let me recheck with sample 2.
A = [5,3,5,0,1], N=5, M=6.
inv(0): pairs (i,j) with A_i > A_j:
(1,2):5>3 ✓
(1,4):5>0 ✓
(1,5):5>1 ✓
(1,3):5=5 ✗
(2,4):3>0 ✓
(2,5):3>1 ✓
(3,4):5>0 ✓
(3,5):5>1 ✓
(2,3):3<5 ✗
(4,5):0<1 ✗
Total = 7. ✓ matches sample.

k=1: B = [0,4,0,1,2]. Inversions: (2,4):4>1, (2,5):4>2, (2,3):4>0. Also (1,3):0=0 no. (4,5):1<2 no. Total = 3. ✓

k=2: B = [1,5,1,2,3]. Inversions: (2,4):5>2, (2,5):5>3, (2,3):5>1, (2,1):5>1, (4,5):2<3 no, (1,4):1<2 no, (1,5):1<3 no, (3,4):1<2 no, (3,5):1<3 no, (1,3):1=1 no. Total = 3. ✓

k=3: B = [2,0,2,3,4]. Inversions: (1,3):2=2 no, (1,2):2>0, (3,2):2>0, (1,4):2<3 no, (1,5):2<4 no, (3,4):2<3 no, (3,5):2<4 no, (4,5):3<4 no. Total = 1. ✓

k=4: B = [3,1,3,4,5]. Inversions: (1,2):3>1, (3,2):3>1, (1,4):3<4 no, (1,5):3<5 no, (3,4):3<4 no, (3,5):3<5 no, (4,5):4<5 no. Total = 1. ✓

k=5: B = [4,2,4,5,0]. Inversions: (1,2):4>2, (3,2):4>2, (1,3):4=4 no, (1,4):4<5 no, (1,5):4>0, (3,4):4<5 no, (3,5):4>0, (4,5):5>0, (2,5):2>0, (4,2):5>2. Let me redo: (i,j), i<j:
(1,2):4>2 ✓
(1,3):4=4 ✗
(1,4):4<5 ✗
(1,5):4>0 ✓
(2,3):2<4 ✗
(2,4):2<5 ✗
(2,5):2>0 ✓
(3,4):4<5 ✗
(3,5):4>0 ✓
(4,5):5>0 ✓
Total = 5. ✓ matches sample.

Now using formula inv(k) = inv(k-1) + N - 2*cnt_ge(k):
cnt_ge(1) = #{A_i >= 1} = 4 (5,3,5,1). inv(1) = 7 + 5 - 8 = 4. ✗ (should be 3)

So formula is wrong. Let me reconsider.

Maybe: inv(k) = inv(k-1) - 2*cnt_lt(k) + N where cnt_lt(k) = #{A_i < k}?
cnt_lt(1) = 1 (just 0). inv(1) = 7 - 2 + 5 = 10. ✗

Or inv(k) = inv(k-1) + 2*cnt_lt(k) - N?
inv(1) = 7 + 2 - 5 = 4. ✗

Let me think again. The change from k-1 to k:

When we add 1 to k, elements with A_i in [k, M-1] wrap around: their values go from (A_i + k-1) mod M to (A_i + k) mod M = (A_i + k-1) mod M + 1, except when A_i + k - 1 mod M = M-1, then it wraps to 0. So elements with A_i + k - 1 >= M, i.e., A_i >= M - k + 1, wrap from M-1 to 0, decreasing by (M-1) effectively. Other elements just increase by 1.

This is getting complicated. Let me think of it differently.

For fixed pair (i,j) with i<j, define f(k) = [(A_i+k) mod M > (A_j+k) mod M].
- If A_i = A_j, f(k) = 0 for all k.
- If A_i < A_j: f(k) = 0 for k <= M - 1 - (A_j - A_i), and f(k) = 1 for k > M - 1 - (A_j - A_i)... wait let me reconsider.

A_i < A_j. When does (A_i + k) mod M > (A_j + k) mod M? This happens when adding k causes A_i+k to wrap but A_j+k doesn't, OR when A_i+k doesn't wrap and A_j+k wraps but A_i+k > A_j+k (impossible since A_i < A_j and same k added without wrap means A_i+k < A_j+k).

So (A_i+k) mod M > (A_j+k) mod M iff A_i + k >= M and A_j + k < M, i.e., k >= M - A_i and k < M - A_j. Since A_i < A_j, M - A_i > M - A_j, so this range is k in [M - A_i, M - A_j - 1], which has length A_j - A_i.

Similarly, A_i > A_j: f(k) = 1 when neither wraps (always since A_i > A_j), plus when both wrap: A_i + k >= M and A_j + k >= M, then (A_i+k-M) > (A_j+k-M) iff A_i > A_j, still true. Plus when A_i + k < M and A_j + k < M: A_i+k > A_j+k iff A_i > A_j, true. So f(k) = 1 for all k except when A_i + k < M and A_j + k >= M, i.e., k < M - A_i and k >= M - A_j. Range: k in [M - A_j, M - A_i - 1], length A_i - A_j.

So contribution to inv(k) from pair (i,j):
- If A_i = A_j: 0.
- If A_i < A_j: 1 if k in [M - A_i, M - A_j - 1], else 0. Length A_j - A_i.
- If A_i > A_j: 1 if k not in [M - A_j, M - A_i - 1], else 0. Length M - (A_i - A_j).

Hmm this is getting complex. Let me think of inv(k) as a function of k.

inv(k) = inv(0) + (number of (i,j), i<j, A_i < A_j with k in [M-A_i, M-A_j-1]) - (number of (i,j), i<j, A_i > A_j with k in [M-A_j, M-A_i-1])

For k in [M-A_j, M-A_i-1] where A_i > A_j, the pair stops being an inversion. For A_i < A_j and k in [M-A_i, M-A_j-1], the pair becomes an inversion.

This is getting too complex for a quick derivation. Let me just use the known O((N+M) log M) approach: precompute freq, then for each k, the answer is:

inv(k) = inv(0) + k*N - 2 * (sum over A_i < k of A_i) - 2 * k * (count of A_i >= k)... no.

Let me try yet another approach. Use the fact that for each k:
inv(k) = sum_{i<j} [(A_i + k) mod M > (A_j + k) mod M]

For each pair, the contribution as a function of k is:
- 0 if A_i = A_j.
- For A_i < A_j: 1 on a contiguous range of length A_j - A_i, 0 elsewhere.
- For A_i > A_j: 1 except on a contiguous range of length A_i - A_j.

Total inv(k) = (number of i<j with A_i > A_j) - (pairs that "stop" being inversions at k) + (pairs that "start" being inversions at k)
= inv(0) - (number of (i<j) with A_i > A_j and k in wrap range) + (number of (i<j) with A_i < A_j and k in wrap range)

A pair (i,j) with i<j, A_i > A_j "stops" being inversion at k if k is in [M - A_j, M - A_i - 1] (mod M, but in [0, M-1] this is the range). Length A_i - A_j.

A pair (i,j) with i<j, A_i < A_j "starts" being inversion at k if k is in [M - A_i, M - A_j - 1]. Length A_j - A_i.

This is hard to compute directly. Let me try the formula inv(k) = inv(k-1) - 2*cnt_ge(k) + N by checking sample 2 more carefully.

Sample 2: A=[5,3,5,0,1], N=5.
freq: 0:1, 1:1, 2:0, 3:1, 4:0, 5:2.
cnt_ge(k) for k=1..5: #{>=1} = 4, #{>=2} = 4, #{>=3} = 3, #{>=4} = 2, #{>=5} = 2.

inv(0) = 7.
inv(1) predicted = 7 + 5 - 2*4 = 4. Actual = 3. Off by 1.
inv(2) predicted = 4 + 5 - 2*4 = 1. Actual = 3. Off.

So formula doesn't work. Let me think again.

Actually I recall now: the correct formula involves the number of elements strictly less than k, but I might be confusing with another problem. Let me derive it properly.

inv(k) - inv(k-1) = change in inversions when we go from k-1 to k.

Going from k-1 to k, each B_i increases by 1 mod M. So B_i either increases by 1 (if A_i + k - 1 < M, i.e., A_i < M - k + 1) or wraps (if A_i >= M - k + 1, in which case B_i was M - (M - k + 1 - 0) = ... let me re-examine).

If A_i < M - k + 1, then A_i + k - 1 < M, so B_i(k-1) = A_i + k - 1, and B_i(k) = A_i + k (no wrap). Increase by 1.
If A_i >= M - k + 1, then A_i + k - 1 >= M, so B_i(k-1) = A_i + k - 1 - M, and B_i(k) = A_i + k - M (also no wrap, since A_i + k could be >= M still). 

Hmm wait, A_i + k = (A_i + k - 1) + 1. If A_i + k - 1 >= M, then A_i + k >= M+1 > M, so B_i(k) = A_i + k - M. B_i(k-1) = A_i + k - 1 - M. So B_i(k) = B_i(k-1) + 1.

So actually every B_i just increases by 1! No wrapping happens within the sequence B when we go from k-1 to k. The wrapping is "absorbed" because all B values shift together.

Wait but then inv(k) = inv(k-1) always? That's clearly wrong since inv(0)=7, inv(1)=3 in sample 2.

I made an error. Let me reconsider. B_i(k) = (A_i + k) mod M. B_i(k) - B_i(k-1) mod M is always 1. But the actual integer value (not mod) increases by 1 if A_i + k - 1 < M, else stays in [0, M-1] after subtracting M. Specifically:
- If A_i + k - 1 < M: B_i(k) = A_i + k - 1 + 1 = A_i + k. Integer value increased by 1.
- If A_i + k - 1 >= M: B_i(k-1) = A_i + k - 1 - M, B_i(k) = A_i + k - M = B_i(k-1) + 1. Integer value increased by 1.

So yes, each B_i as an integer increases by exactly 1. Then how can inv change?

Oh I see, because the comparison is between the values as integers in [0, M-1], and when B_i was M-1 and increases, it goes to 0. So integer-wise it increased by 1, but the cyclic order changes.

So elements with B_i(k-1) = M-1 (i.e., A_i + k - 1 mod M = M-1, i.e., A_i + k ≡ 0 mod M, i.e., A_i = (M - k) mod M = M - k if k < M, 0 if k = M) "wrap" and become 0, which is smaller than everything.

Specifically, elements with A_i = M - k (for k >= 1) have B_i(k-1) = M-1 and B_i(k) = 0. So these elements drop from the maximum to the minimum.

So at step k, elements with A_i = M - k (or A_i = 0 when k = 0... but for k=0 we don't apply) wrap. But for general step from k-1 to k, the wrapping element is A_i = M - k (for k = 1..M-1, and for k = M it's A_i = 0, but k = M is same as k = 0).

Wait, for k from 1 to M-1, the elements that wrap are A_i = M - k.

Let me redo. When k goes from k-1 to k:
- For k = 1: elements with A_i = M - 1 wrap (B goes from M-1 to 0).
- For k = 2: elements with A_i = M - 2 wrap.
- ...
- For k = M-1: elements with A_i = 1 wrap.
- For k = M: elements with A_i = 0 wrap, but k=M is same as k=0.

So at step k (1 <= k <= M-1), elements with A_i = M - k wrap.

When an element wraps from M-1 to 0:
- Pairs where it was larger: all pairs (i,j) with i < j where i is the wrapping element, and A_j (no, B_j(k-1)) < M-1 — these were inversions, now stop. Number of such j > i with B_j(k-1) < M-1 = (number of elements after i) - (number of elements after i with B_j(k-1) = M-1, i.e., A_j = M-k).
  Hmm, but there could be multiple wrapping elements.

Let's say at step k, there are w_k = freq[M-k] elements wrapping (positions p_1 < p_2 < ... < p_{w_k}). For each wrapping element at position p:
- It stops being larger than elements after it that aren't wrapping: decreases inversions by (N - p) - (number of wrapping elements after p) - (elements after p that don't wrap). Hmm complex.

Actually I think the simpler approach is the one I should use: for each k, the answer can be computed using a BIT over the original A values. But that would be O(M log M) per k, total O(M^2 log M), too slow.

Let me think of the O(N + M) approach. I think the formula is:

inv(k) = inv(0) + k * (number of A_i = 0) - ... no.

Let me just carefully derive using the "wrap" interpretation.

Define w(k) = freq[M - k mod M] = freq[(M-k) % M] for k = 0, 1, ..., M-1. (For k=0, w(0) = freq[0], but k=0 is the base case.)

When k increases by 1 (from k-1 to k), w(k) elements wrap (their B value goes from M-1 to 0).

For a wrapping element at position p:
- Before wrap: it's M-1, larger than all other B values (which are in [0, M-1]). So it forms inversions with all elements after it (at positions > p).
- After wrap: it's 0, smaller than all other B values. So it forms inversions with all elements before it (at positions < p).

Change in inversions from this single wrap: - (number of elements after p) + (number of elements before p) = -(N - p) + (p - 1) = 2p - N - 1.

For all w(k) wrapping elements at positions p_1, ..., p_{w_k}, the total change is:
sum_{j=1}^{w_k} (2 p_j - N - 1) = 2 * (sum of positions of wrapping elements) - w(k) * (N + 1)

So inv(k) = inv(k-1) + 2 * S(k) - w(k) * (N + 1)

where S(k) = sum of positions of elements with A_i = M - k (or A_i = 0 if k = 0... but for k >= 1, it's A_i = M - k).

Wait, for k = 1, elements with A_i = M - 1 wrap. For k = 2, A_i = M - 2. For k = M-1, A_i = 1.

Let me verify with sample 2: A = [5,3,5,0,1] (1-indexed).
freq: 0:1 (pos 4), 1:1 (pos 5), 2:0, 3:1 (pos 2), 4:0, 5:2 (pos 1, 3).

k=1: wrap A_i = M-1 = 5. Elements at pos 1, 3. S(1) = 1+3 = 4. w(1) = 2. Change = 2*4 - 2*6 = 8 - 12 = -4. inv(1) = 7 - 4 = 3. ✓

k=2: wrap A_i = 4. No elements. w(2) = 0. Change = 0. inv(2) = 3. ✓

k=3: wrap A_i = 3. Element at pos 2. w(3) = 1, S(3) = 2. Change = 4 - 6 = -2. inv(3) = 3 - 2 = 1. ✓

k=4: wrap A_i = 2. No elements. inv(4) = 1. ✓

k=5: wrap A_i = 1. Element at pos 5. w(5) = 1, S(5) = 5. Change = 10 - 6 = 4. inv(5) = 1 + 4 = 5. ✓

So the formula is:
inv(k) = inv(k-1) + 2 * S(M-k) - w(M-k) * (N + 1)

where w(v) = freq[v] and S(v) = sum of positions of elements with A_i = v.

To compute S(v) for each v, we iterate through A once and accumulate:
pos_sum[v] = sum of 1-indexed positions where A_i = v.

Then for k = 1 to M-1:
  v = M - k
  inv[k] = inv[k-1] + 2 * pos_sum[v] - freq[v] * (N + 1)

This is O(N + M)! 

Let me double check sample 1: A = [2,1,0], N=3, M=3. 1-indexed: A_1=2, A_2=1, A_3=0.
freq: 0:1, 1:1, 2:1.
pos_sum: 0:3, 1:2, 2:1.
inv(0) = 3 (computed).

k=1: v = M-1 = 2. freq[2]=1, pos_sum[2]=1. Change = 2*1 - 1*4 = -2. inv(1) = 3 - 2 = 1. ✓
k=2: v = M-2 = 1. freq[1]=1, pos_sum[1]=2. Change = 4 - 4 = 0. inv(2) = 1. ✓

Sample 3: A = [0,1,2,3,4,5,6], N=7, M=7.
inv(0) = 0.
freq[v] = 1 for all v. pos_sum[v] = v+1.
k=1: v=6. Change = 2*7 - 1*8 = 14-8 = 6. inv(1) = 6. ✓
k=2: v=5. Change = 2*6 - 8 = 4. inv(2) = 10. ✓
k=3: v=4. Change = 2*5 - 8 = 2. inv(3) = 12. ✓
k=4: v=3. Change = 2*4 - 8 = 0. inv(4) = 12. ✓
k=5: v=2. Change = 2*3 - 8 = -2. inv(5) = 10. ✓
k=6: v=1. Change = 2*2 - 8 = -4. inv(6) = 6. ✓

All match.

So the algorithm is:
1. Read N, M, A.
2. Compute inv(0) using BIT (Fenwick tree) on values 0..M-1.
3. Compute freq[v] and pos_sum[v] for v in 0..M-1.
4. Print inv(0).
5. For k = 1 to M-1:
   v = M - k
   inv += 2 * pos_sum[v] - freq[v] * (N + 1)
   Print inv.

This is O((N+M) log M) for step 2 (BIT) and O(N+M) for the rest, total O((N+M) log M).

**Pitfalls:**
- The formula is derived assuming 1-indexed positions. Make sure to use 1-indexed pos_sum.
- inv(0) must be computed correctly (can be large, up to N*(N-1)/2 ~ 2e10, need 64-bit).
- For k from 1 to M-1, the wrapping value is M-k. Note that for k = M, we'd have v = 0, and inv would return to inv(0) (cyclic), but we only need k = 0..M-1.

**Edge cases:**
- M = 1: all A_i = 0, B_i = 0, inv = 0 for all k. Only k=0 is output.
- N = 1: inv = 0 for all k.
- All A_i equal: inv = 0 for all k.

## worker: Implementation complete; the solution is ready as 
I implemented the O((N+M) log M) algorithm derived in the ideation:

1. **Inversion count for k=0**: Computed using a Fenwick tree (BIT) by processing the array in reverse and counting how many elements seen so far are smaller than `A[j]`. Each inversion is counted exactly once, giving `inv(0)`.

2. **Frequencies and position sums**: I compute `freq[v]` (count of values equal to `v`) and `pos_sum[v]` (sum of 1-indexed positions where `A_i = v`) in a single pass.

3. **Transition formula**: When `k` increments by 1, the elements that "wrap" from `M-1` to `0` are exactly those with `A_i = M - k`. For each such wrapping element at position `p`, the change in inversion count is `2p - N - 1` (it loses inversions with elements after it and gains inversions with elements before it). Summing over all wrapping elements gives:
   - `inv(k) = inv(k-1) + 2 * pos_sum[M-k] - freq[M-k] * (N + 1)`

4. **Verification**: This formula was verified against all three samples and produced correct results.

The algorithm uses 64-bit integers implicitly (Python's default), handles the edge case `M=1` correctly (only outputs `inv(0)`), and runs in `O((N+M) log M)` time which is well within the constraints.
