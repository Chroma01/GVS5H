We need to compute, for each k in [0, M-1], the inversion count of B_i = (A_i + k) mod M.  
Let’s denote original values A_i in [0, M-1]. For each k, the transformation is a cyclic shift of each value by k modulo M.  
We can precompute the inversion count for k=0 using a Fenwick tree (BIT) over values 0..M-1.  
When we increase k by 1, each A_i either stays the same (if A_i < M-1) or wraps from M-1 to 0. The wrap changes the relative order with other elements.  
We can maintain counts of elements in each value bucket. When k increments, all values increase by 1 mod M. The inversion count changes by:
- For each element that wraps (A_i = M-1 → 0): it moves from being the largest to the smallest, so it loses (cnt of elements smaller than it) inversions and gains (cnt of elements larger than it) inversions. Net change = (larger_count) - (smaller_count) = (N-1 - 2*smaller_count).
- For all other elements (value v → v+1): they become larger, so each such element gains inversions with elements that are smaller than its new value. Specifically, an element with original value v (v < M-1) becomes v+1. The number of elements with value ≤ v (i.e., smaller or equal to its old value) is some count. After shift, it becomes larger than those with value ≤ v. So it gains (count of elements with value ≤ v) inversions. But we must be careful: elements that were equal to v remain equal after shift? Actually if v → v+1, then elements with original value v become v+1, so among themselves they remain equal (no inversion). Elements with original value < v become < v+1, so they become smaller. So the element gains inversions over elements with original value < v. Wait, we need to count pairs (i,j) with i<j and B_i > B_j. When we shift all values by +1 mod M, the relative order between two elements changes only if one wraps and the other doesn't, or both wrap (then both become 0, still equal). So we can derive a formula for total change.

Better approach: Use the fact that the sequence of inversion counts for k=0..M-1 can be computed by simulating the shift. Let cnt[v] = number of elements with value v. For k=0, compute inv0. For each increment of k:
- The element at value M-1 moves to 0. Let x = cnt[M-1].
- All other elements move from v to v+1.
The change in inversion count Δ can be computed as:
Δ = (number of new inversions created) - (number of inversions destroyed).
When we shift, for any pair (i,j):
- If both don't wrap: their relative order remains the same (since both increase by 1, difference unchanged).
- If both wrap: both become 0, still equal, no inversion.
- If one wraps (say i wraps, j doesn't): originally B_i = M-1, B_j = v (v < M-1). After shift, B_i = 0, B_j = v+1. So if originally B_i > B_j (always true since M-1 > v), after shift B_i = 0 < v+1, so the inversion disappears. If originally B_i < B_j (impossible), after shift it might become an inversion. So each pair where exactly one element wraps loses an inversion if the wrapping element was originally larger (which it always is). So we lose x * (N - x) inversions? Wait: if i wraps and j doesn't, originally B_i = M-1 > B_j, so it's an inversion. After shift, B_i = 0 < B_j+1, so it's not an inversion. So each such pair loses one inversion. Number of such pairs: x * (N - x). But careful: if i wraps and j doesn't, we consider ordered pairs i<j. The number of unordered pairs with one wrap and one non-wrap is x*(N-x). In each such pair, the wrapping element is larger originally, so it's an inversion. After shift, it's not. So we lose x*(N-x) inversions.

Now, what about pairs where neither wraps? Their relative order doesn't change. So no change.

But wait: when we shift, the values of non-wrapping elements increase by 1. This can create new inversions among non-wrapping elements? Let's check: Suppose we have two non-wrapping elements with original values a and b, a < b. After shift, they become a+1 and b+1, still a+1 < b+1. So no inversion created. If a > b, after shift a+1 > b+1, still inversion. So relative order among non-wrapping elements is preserved. So no change.

What about pairs where both wrap? Both become 0, equal, so no inversion.

Thus the only change is the loss of inversions from pairs where exactly one element wraps. But is that all? Let's test with sample: N=3, M=3, A=(2,1,0). k=0: inv=3. k=1: shift: wrap element is the one with value 2 (x=1). N-x=2. So we lose 1*2=2 inversions. So inv1 = 3 - 2 = 1. That matches sample (inv1=1). k=2: now values are (0,2,1). Wrap element is the one with value 2? Wait, after k=1, the sequence is (0,2,1). The values are 0,2,1. The element with value 2 (original 1) is now 2. When we shift to k=2, the element with value 2 wraps to 0. x=1. N-x=2. So we lose 2 inversions. But inv2 should be 1. Let's compute: from k=1 to k=2, the sequence changes from (0,2,1) to (1,0,2). The inversion count goes from 1 to 1. So change is 0. But our formula says lose 2. So something is wrong.

Let's analyze carefully. The issue is that when we shift, the wrapping element moves to 0, but the other elements also shift. So the pair (wrap, non-wrap) originally: wrap value = M-1, non-wrap value = v. After shift: wrap=0, non-wrap=v+1. So the inversion disappears. But we also need to consider that the non-wrap element's value increased, which might affect its relation with other non-wrap elements? No, as argued, relative order among non-wraps is preserved. However, the wrapping element's new value is 0, which is smaller than all non-wrap elements (since they are at least 1). So the wrapping element becomes the smallest. So it will be smaller than all non-wrap elements, meaning no inversion from wrap to non-wrap. But what about non-wrap to wrap? Inversions are defined for i<j. If the wrapping element is at position i and non-wrap at j>i, originally B_i > B_j, after shift B_i < B_j, so inversion lost. If wrapping element is at position j and non-wrap at i<j, originally B_i < B_j (since wrap is largest), after shift B_i > B_j? Let's check: originally B_i = v (non-wrap), B_j = M-1 (wrap). Since v < M-1, it's not an inversion. After shift: B_i = v+1, B_j = 0. Now v+1 > 0, so it becomes an inversion! So we gain an inversion for each pair where the wrapping element is after a non-wrap element. So the net change is: for each pair (i,j) with i<j, exactly one wraps. If wrap is at i, we lose an inversion. If wrap is at j, we gain an inversion. So net change = (number of pairs where wrap is at j) - (number of pairs where wrap is at i). Let x = number of wrapping elements. Let pos_wrap = positions of wrapping elements. Then number of pairs where wrap is at i = sum over wrap positions of (number of non-wrap elements after it). Number of pairs where wrap is at j = sum over wrap positions of (number of non-wrap elements before it). So net change = (total non-wrap before wrap) - (total non-wrap after wrap). This depends on the positions of wrapping elements, not just counts. So my earlier simplification was incorrect.

We need a more robust method. Since M and N are up to 2e5, we can compute the inversion count for each k by simulating the shift and updating the count efficiently using a BIT or by maintaining the counts of values and using a formula that accounts for positions.

Alternative approach: For each k, B_i = (A_i + k) mod M. We can think of the sequence as a circular shift of the values. The inversion count for k can be expressed in terms of the original sequence and k. There is known solution for this problem (AtCoder ABC 107 D? Actually it's from AtCoder ABC 107? No, it's from AtCoder ABC 107? Wait, it's from AtCoder ABC 107? Actually it's from AtCoder ABC 107? Let me recall: This is AtCoder ABC 107 D? No, it's AtCoder ABC 107? Actually it's AtCoder ABC 107? I'm not sure. But I recall a problem: "Inversion Count of a Sequence with Additive Shifts" or something. The solution involves computing the inversion count for k=0, then for each k, the change is determined by the number of elements that wrap and their positions.

We can compute the inversion count for k=0 using BIT. Then for each k from 1 to M-1, we update the count. When we go from k-1 to k, the transformation is: each element's value increases by 1 mod M. This is equivalent to: for each element, if its value was M-1, it becomes 0; otherwise it becomes v+1.

We can maintain a BIT over the values to compute the number of inversions in the current sequence. But updating the BIT for each k would be O(N log M) per k, too slow.

We need a way to update the inversion count in O(1) or O(log M) per k. Since M is up to 2e5, O(M log M) is acceptable.

Observation: The inversion count of B for a given k can be computed as:
inv(k) = sum_{i=1}^{N} (number of j > i such that B_i > B_j).
We can split the sum based on the values. Let cnt[v] be the number of elements with value v in the original A. For a fixed k, the value distribution is the same: each element's value is shifted by k mod M, so the multiset of values is the same: cnt[v] for v=0..M-1. However, the order matters.

We can think of the sequence as a permutation of the multiset. The inversion count depends on the order. When we shift by k, the order of values changes because each element's value increases by k mod M. This is equivalent to taking the original sequence and applying a cyclic shift to the value axis. So we can precompute the positions of each value.

Let pos[v] be the list of positions (1-indexed) where A_i = v. For a given k, the value at position i is (A_i + k) mod M. So the sequence B is determined by the original positions and the shift.

We can compute inv(k) by iterating over positions in order of their original values? Actually, we can think of the sequence as: for each value v in the original, its new value is (v+k) mod M. So we can sort the elements by their new value. But the order of elements with the same new value is the same as their original order. So we can process values in increasing order of new value.

Alternatively, we can compute inv(k) using the formula:
inv(k) = total pairs (i,j) with i<j and (A_i + k) mod M > (A_j + k) mod M.
This is equivalent to: (A_i - A_j) mod M < (k - k) mod M? Not exactly.

We can break the condition into two cases based on whether A_i + k >= M or not. Let’s define:
B_i = A_i + k if A_i + k < M, else A_i + k - M.
So B_i = A_i + k - M * I(A_i + k >= M), where I is indicator.

Then B_i > B_j iff:
Case 1: Both A_i + k < M and A_j + k < M: then A_i > A_j.
Case 2: Both A_i + k >= M and A_j + k >= M: then A_i + k - M > A_j + k - M => A_i > A_j.
Case 3: A_i + k < M and A_j + k >= M: then A_i + k > A_j + k - M => A_i + k > A_j + k - M => A_i > A_j - M => A_i + M > A_j. Since A_i, A_j in [0, M-1], A_i + M > A_j always true. So B_i > B_j always.
Case 4: A_i + k >= M and A_j + k < M: then A_i + k - M > A_j + k => A_i - M > A_j => A_i > A_j + M. Since A_i, A_j in [0, M-1], A_i > A_j + M is impossible. So B_i > B_j never.

So the condition B_i > B_j is equivalent to:
- If A_i + k < M and A_j + k < M: A_i > A_j.
- If A_i + k >= M and A_j + k >= M: A_i > A_j.
- If A_i + k < M and A_j + k >= M: always true.
- If A_i + k >= M and A_j + k < M: always false.

Thus, the inversion count for k is:
inv(k) = (number of pairs (i,j) with i<j, A_i > A_j, and both A_i + k < M and A_j + k < M)
       + (number of pairs (i,j) with i<j, A_i > A_j, and both A_i + k >= M and A_j + k >= M)
       + (number of pairs (i,j) with i<j, A_i + k < M and A_j + k >= M).

Let’s denote:
S1(k) = number of pairs (i,j) with i<j, A_i > A_j, and A_i < M - k and A_j < M - k. (since A_i + k < M <=> A_i < M - k)
S2(k) = number of pairs (i,j) with i<j, A_i > A_j, and A_i >= M - k and A_j >= M - k.
S3(k) = number of pairs (i<j) with A_i < M - k and A_j >= M - k.

Note: S3(k) counts all pairs where the first is in the "low" group (value < M-k) and the second is in the "high" group (value >= M-k), regardless of A_i > A_j. Because in case 3, B_i > B_j always. So S3(k) is simply the number of pairs (i,j) with i<j, A_i < M-k, A_j >= M-k.

Similarly, S1(k) and S2(k) are the inversion counts within the low group and within the high group, respectively.

So inv(k) = S1(k) + S2(k) + S3(k).

Now, note that S1(k) + S2(k) is the total inversion count in the original sequence A, but only considering pairs where both elements are in the same group (low or high). Actually, the total inversion count of A is:
inv_total = S1(k) + S2(k) + S4(k), where S4(k) is the number of pairs (i,j) with i<j, A_i > A_j, and A_i >= M-k, A_j < M-k. (i.e., high group element before low group element with A_i > A_j). But note that in case 4, B_i > B_j is false, so those inversions are not counted in inv(k). So inv(k) = inv_total - S4(k) + S3(k).

But S3(k) is the number of pairs with low before high, regardless of order. And S4(k) is the number of pairs with high before low and A_i > A_j. Since A_i >= M-k and A_j < M-k, A_i > A_j is always true. So S4(k) is simply the number of pairs (i,j) with i<j, A_i >= M-k, A_j < M-k. That is exactly the number of pairs with high before low. Let's denote:
H(k) = number of pairs (i,j) with i<j, A_i >= M-k, A_j < M-k.
L(k) = number of pairs (i<j) with A_i < M-k, A_j >= M-k.
Then S3(k) = L(k), S4(k) = H(k).
So inv(k) = inv_total - H(k) + L(k).

But note that total pairs between low and high groups is L(k) + H(k). And L(k) + H(k) = (number of low elements) * (number of high elements). Because for any pair of one low and one high, either low is before high (counted in L) or high is before low (counted in H). So L(k) + H(k) = cnt_low * cnt_high, where cnt_low = number of elements with A_i < M-k, cnt_high = N - cnt_low.

Thus, inv(k) = inv_total - H(k) + L(k) = inv_total - H(k) + (cnt_low * cnt_high - H(k)) = inv_total + cnt_low * cnt_high - 2*H(k).

So we need to compute inv_total (constant), cnt_low(k) (easy to compute by prefix sums of counts), and H(k) = number of pairs (i,j) with i<j, A_i >= M-k, A_j < M-k.

H(k) can be computed as: for each element in the high group (value >= M-k), count how many low elements are before it. So H(k) = sum over positions i where A_i >= M-k of (number of j < i with A_j < M-k). This is like an inversion count but with a condition on values. We can precompute for each position the number of low elements before it, but that depends on k. However, we can compute H(k) efficiently by iterating k from 0 to M-1 and updating.

Alternatively, we can compute H(k) using a BIT over positions? But H(k) is a function of k. We can precompute an array H for all k. Since M is up to 2e5, we can compute H(k) in O(M log M) or O(M) time.

Let's think: For a fixed k, the threshold is T = M - k. So low group: values < T, high group: values >= T. As k increases from 0 to M-1, T decreases from M to 1. So the low group shrinks and the high group grows. Specifically, when k increases by 1, T decreases by 1. So the element with value T-1 moves from low to high. So we can update H(k) incrementally.

Let’s define for each value v, the positions where A_i = v. Let pos[v] be the list of positions (1-indexed). For a given T, H(T) = number of pairs (i,j) with i<j, A_i >= T, A_j < T. This is equivalent to: for each position i with A_i >= T, count the number of positions j < i with A_j < T. So if we know for each position i, the number of low elements before it, we can sum over high elements.

We can precompute an array low_prefix[i] = number of elements with value < T before position i. But T varies. However, we can compute H(T) by iterating T from M down to 1, and maintaining a BIT over positions to count low elements? Actually, we can compute H(T) for all T by processing values in decreasing order.

Consider T = M: low group is values < M, i.e., all elements. So H(M) = number of pairs (i,j) with i<j, A_i >= M, A_j < M. But A_i >= M is impossible since A_i < M. So H(M) = 0.
T = M-1: low group: values < M-1, high group: values >= M-1. So H(M-1) = number of pairs where A_i = M-1 and A_j < M-1 with i<j. That is: for each position i with A_i = M-1, count number of j < i with A_j < M-1. This is like: total pairs with A_i = M-1 and A_j < M-1 and i<j. We can compute this by iterating positions in order and maintaining a count of low elements seen so far.

In general, for a given T, H(T) = sum over values v >= T of (number of pairs (i,j) with A_i = v, A_j < T, i<j). We can compute this by processing values v from T to M-1. But we need H(T) for all T.

We can compute an array H[0..M] where H[T] corresponds to threshold T (i.e., low: < T, high: >= T). Note that for k, T = M - k. So we need H[M-k] for k=0..M-1. So we need H[T] for T=1..M. (T=M corresponds to k=0, all elements low, H=0).

We can compute H[T] by iterating T from M down to 1, and when we decrease T by 1, the element with value T-1 moves from low to high. So we need to update H accordingly. Initially, for T=M, low group is all, high group empty, H=0. When we set T=M-1, the value M-1 becomes high. So we need to add to H the number of pairs (i,j) with A_i = M-1, A_j < M-1, i<j. But note that for T=M-1, low group is values < M-1, so A_j < M-1. So we need to count for each position i with A_i = M-1, the number of low elements before it. At this point, low elements are all elements except those with value M-1. So we can compute this by iterating positions of value M-1 in order, and for each, count how many elements before it are not M-1. That is: (i-1) - (number of M-1 elements before i). So we can precompute for each value v, the positions. Then for each position i in pos[v], the number of low elements before it (when low group is all except v) is (i-1) - (number of elements with value v before i). So we can compute the contribution of value v to H when it becomes high.

In general, when we move value v from low to high (i.e., when T decreases to v+1), we need to add to H the number of pairs (i,j) with A_i = v, A_j < v+1, i<j. But note that at that moment, low group consists of values < v+1, which includes all values except those >= v+1. But since we are processing T decreasing, the values that are already high are those >= T. So when we add value v, the low group is values < v+1, which are exactly the values that are currently low (since we haven't added v yet). So the number of low elements before a position i with A_i = v is: (i-1) - (number of elements with value >= v+1 before i). But we can maintain a BIT over positions to count the number of high elements seen so far? Actually, we can process values in decreasing order of v, and maintain a data structure that tracks the positions of elements that are already high. Then for each position i of the current value v, the number of low elements before i is (i-1) - (number of high elements before i). So we can compute the contribution as sum over i in pos[v] of ((i-1) - high_count_before_i). And we add this to H. Then we mark all positions of value v as high (i.e., add them to the BIT). Then we proceed to v-1.

This way, we can compute H[T] for all T in O(N log M) or O(N) if we use a Fenwick tree over positions. Since N and M are up to 2e5, O(N log M) is fine.

Let's formalize:
We want H[T] for T=1..M. H[T] = number of pairs (i,j) with i<j, A_i >= T, A_j < T.
We can compute an array H of size M+1 (index by T). Initialize H[M] = 0.
We will process values v from M-1 down to 0. For each v, when we set T = v+1, we are adding value v to the high group. So we need to compute the increase in H when moving from T=v+2 to T=v+1. Actually, let's define H[T] for T from 1 to M. We can compute H[T] incrementally: start with T=M, H[M]=0. Then for T from M-1 down to 1, we update H[T] = H[T+1] + delta, where delta is the number of new pairs created when we move the threshold from T+1 to T. When we decrease T by 1, the value T becomes high. So delta = number of pairs (i,j) with A_i = T, A_j < T, i<j. At this point, the high group consists of values >= T+1. So the low group is values < T. So we need to count for each position i with A_i = T, the number of low elements before i. That is: (i-1) - (number of high elements before i). So we can compute delta by iterating over positions of value T, and for each, query a BIT that stores the positions of high elements (values > T). Initially, for T=M, high group is empty. So we process v from M-1 down to 0. For each v, we compute delta_v = sum_{i in pos[v]} ( (i-1) - query(i) ), where query(i) returns the number of high elements (values > v) before position i. Then we set H[v] = H[v+1] + delta_v? Wait, careful with indices.

Let's define threshold T: low: < T, high: >= T.
We want H[T] for T=1..M.
We can compute H[T] by starting from T=M (all low, H=0) and decreasing T.
When we go from T to T-1, the value T-1 becomes high. So the increase in H is the number of pairs (i,j) with A_i = T-1, A_j < T-1, i<j. At this moment, high group is values >= T, so low group is values < T-1. So the number of low elements before a position i with A_i = T-1 is (i-1) - (number of high elements before i). So we can compute this if we know the high elements (values >= T). So we process values in decreasing order: start with v = M-1, then v = M-2, ..., 0.
For each v, we want to compute the contribution when v becomes high. That contribution is exactly the number of pairs (i,j) with A_i = v, A_j < v, i<j. But note that when v becomes high, the low group is values < v. So we need to count for each position i with A_i = v, the number of low elements before i. At that time, the high elements are those with value > v. So we can maintain a BIT over positions that contains all elements with value > v. Initially, for v=M-1, high group is empty. So we process v from M-1 down to 0. For each v, we compute delta_v = sum_{i in pos[v]} ( (i-1) - BIT.query(i) ), where BIT contains positions of elements with value > v. Then we add all positions of value v to the BIT. Then we set H[v] = H[v+1] + delta_v? But careful: H[T] is defined for threshold T. When we process v, we are effectively setting T = v+1? Let's see: initially T=M, H[M]=0. After processing v=M-1, we have added value M-1 to high. So now high group is values >= M-1, so T = M-1. So H[M-1] = delta_{M-1}. After processing v=M-2, we add value M-2, so T = M-2, H[M-2] = H[M-1] + delta_{M-2}. So in general, after processing values from M-1 down to v, we have T = v+1, and H[v+1] = sum_{u=v+1}^{M-1} delta_u. So we can store H[T] for T=1..M as: H[T] = sum_{u=T}^{M-1} delta_u, where delta_u is computed when processing value u. So we can compute an array H of size M+1, where H[T] = sum_{u=T}^{M-1} delta_u. Then for k, we need T = M - k, so H[M-k] = sum_{u=M-k}^{M-1} delta_u.

Alternatively, we can compute an array ans[k] directly. Since inv(k) = inv_total + cnt_low * cnt_high - 2*H(T), where T = M-k, cnt_low = number of elements with A_i < T, cnt_high = N - cnt_low. We can precompute cnt_low for each T easily by prefix sums of counts. And we can compute H(T) as described.

So algorithm:
1. Read N, M, and array A.
2. Compute inv_total: inversion count of original A using BIT over values. O(N log M).
3. Compute cnt[v] for v=0..M-1.
4. Compute prefix sum of cnt to get cnt_low[T] = sum_{v=0}^{T-1} cnt[v] for T=1..M. (cnt_low[M] = N).
5. Compute H[T] for T=1..M:
   - Initialize BIT over positions (size N) to store high elements.
   - Initialize H[M] = 0.
   - For v from M-1 down to 0:
        delta = 0
        for each position i in pos[v]:
            delta += (i-1) - BIT.query(i)   # number of low elements before i
        H[v] = H[v+1] + delta   # but careful: H[v] corresponds to threshold v? Actually, after processing v, the threshold is v+1? Let's define H_thresh[T] for T=1..M. We want H_thresh[T] = number of pairs (i,j) with i<j, A_i >= T, A_j < T.
        We can compute H_thresh[T] by starting from T=M: H_thresh[M]=0.
        Then for T from M-1 down to 1:
            delta = number of pairs with A_i = T, A_j < T, i<j.
            H_thresh[T] = H_thresh[T+1] + delta.
        So we can compute delta for each value v = T. So we process v from M-1 down to 0, and for each v, compute delta_v, then set H_thresh[v] = H_thresh[v+1] + delta_v. (Here H_thresh[v] corresponds to T=v). So we need an array H of size M+1, with H[M]=0, and for v from M-1 down to 0: H[v] = H[v+1] + delta_v.
        Then for k, T = M-k, so we need H[M-k].
   - After computing delta_v, add all positions of value v to BIT (update BIT at position i with +1).
6. For each k from 0 to M-1:
   T = M - k
   cnt_low = prefix[T]   # number of elements with value < T
   cnt_high = N - cnt_low
   H_val = H[T]   # H[T] is number of pairs with A_i >= T, A_j < T
   ans[k] = inv_total + cnt_low * cnt_high - 2 * H_val

Check with sample 1: N=3, M=3, A=(2,1,0).
inv_total: pairs: (2,1), (2,0), (1,0) -> 3.
cnt: [1,1,1] (values 0,1,2 each count 1).
prefix: T=1: cnt_low=1 (value 0), T=2: cnt_low=2 (values 0,1), T=3: cnt_low=3.
Compute H:
pos[2]=[1], pos[1]=[2], pos[0]=[3].
Process v=2: delta = (1-1) - BIT.query(1)=0-0=0. H[2]=H[3]+0=0. Add pos[2] to BIT.
Process v=1: delta = (2-1) - BIT.query(2)=1 - (number of high elements before 2). High elements: pos[2]=1, so BIT.query(2)=1. delta=0. H[1]=H[2]+0=0. Add pos[1] to BIT.
Process v=0: delta = (3-1) - BIT.query(3)=2 - (number of high before 3). High: pos[2]=1, pos[1]=2, so BIT.query(3)=2. delta=0. H[0]=H[1]+0=0.
So H[3]=0, H[2]=0, H[1]=0, H[0]=0.
Now for k=0: T=3, cnt_low=3, cnt_high=0, H=0. ans=3+0-0=3.
k=1: T=2, cnt_low=2, cnt_high=1, H=0. ans=3+2*1-0=5? But sample says 1. So something is wrong.

Let's recalc: For k=1, T=M-k=2. cnt_low = number of elements with A_i < 2 = values 0 and 1: count=2. cnt_high=1. H[T]=H[2]=0. So ans=3+2-0=5. But sample output for k=1 is 1. So our formula is incorrect.

Let's debug the formula. We had inv(k) = inv_total - H(k) + L(k), where H(k) = number of pairs with high before low, L(k) = number of pairs with low before high. And L(k) + H(k) = cnt_low * cnt_high. So inv(k) = inv_total + cnt_low * cnt_high - 2*H(k). But in sample, inv_total=3, cnt_low=2, cnt_high=1, so cnt_low*cnt_high=2. H(k) should be the number of pairs with high before low. For k=1, T=2, high group: values >=2, i.e., value 2. Low group: values 0,1. The sequence A: positions: 1:2, 2:1, 3:0. High before low: pairs where high element is before low element. The only high element is at position 1. Low elements at positions 2 and 3. So pairs: (1,2) and (1,3). Both are high before low. So H(k)=2. Then inv(k) = 3 + 2 - 2*2 = 3+2-4=1. That matches! So our computed H[2] should be 2, but we got 0. So our computation of H[T] is wrong.

Let's recompute H[T] manually. For T=2, we want number of pairs (i,j) with i<j, A_i >=2, A_j <2. A_i >=2 means A_i=2. A_j <2 means A_j=0 or 1. So we need pairs where the first is 2 and the second is 0 or 1. In the sequence, the 2 is at position 1. The 0 and 1 are at positions 3 and 2 respectively. So pairs: (1,2) and (1,3). So H=2.

Our algorithm: We process v from M-1 down to 0. For v=2, we compute delta when v becomes high. But when v=2 becomes high, the threshold T becomes 2? Actually, when we set T=2, high group is values >=2. So we need to count pairs with A_i=2 and A_j <2. That is exactly delta for v=2. In our algorithm, we computed delta for v=2 as: for each position i in pos[2], (i-1) - BIT.query(i). At that time, BIT contains high elements with value >2, which is empty. So delta = (1-1) - 0 = 0. But we need to count pairs with A_i=2 and A_j <2. The number of low elements before position 1 is 0 because it's the first element. So indeed, there are no pairs where the 2 is before a low element? Wait, the 2 is at position 1, so there are no elements before it. So the pairs with A_i=2 and A_j <2 and i<j are pairs where the 2 is before a low element. Since the 2 is at position 1, there are no low elements after it? Actually, i<j means the 2 is at i, and the low element is at j>i. So we need to count low elements after the 2, not before. I made a mistake: H(T) counts pairs with i<j, A_i >= T, A_j < T. So for a given high element at position i, we need to count low elements at positions j > i. So it's the number of low elements after i, not before. So my delta computation was wrong: it should be (number of low elements after i) not before. So we need to compute for each position i with A_i = v, the number of low elements after i. That is: (total low elements) - (number of low elements before i) - (1 if A_i is low? but A_i=v is high). So we need to know the total number of low elements. But when we are processing v, the low group is values < v. So total low elements = sum_{u=0}^{v-1} cnt[u]. We can precompute prefix sums of cnt. So for each position i in pos[v], the number of low elements after i is: total_low - (number of low elements before i). And number of low elements before i is: (i-1) - (number of high elements before i). So we can compute it if we know the number of high elements before i. So we still need a BIT for high elements before i. But we also need total_low. So we can compute delta_v = sum_{i in pos[v]} ( total_low - ( (i-1) - BIT.query(i) ) ) = sum_{i in pos[v]} ( total_low - i + 1 + BIT.query(i) ). But careful: total_low is the number of elements with value < v. That is constant for all i in pos[v]. So we can compute it.

Let's test with sample: v=2, total_low = number of elements with value <2 = cnt[0]+cnt[1]=2. pos[2]=[1]. BIT.query(1)=0. So delta = 2 - (1-1) + 0 = 2. So H[2] = H[3] + 2 = 2. That matches.

So corrected algorithm:
For v from M-1 down to 0:
   total_low = prefix[v]   # number of elements with value < v
   delta = 0
   for i in pos[v]:
        low_before = (i-1) - BIT.query(i)   # number of low elements before i
        low_after = total_low - low_before
        delta += low_after
   H[v] = H[v+1] + delta
   then add all positions of value v to BIT.

But wait: H[v] corresponds to threshold T=v. We want H[T] for T=1..M. So we need H[1], H[2], ..., H[M]. We can compute an array H of size M+1, with H[M]=0. Then for v from M-1 down to 0: H[v] = H[v+1] + delta_v. Then for k, T = M-k, we need H[T] = H[M-k].

Let's test with sample 1:
v=2: total_low=2, pos[2]=[1], BIT empty, low_before=0, low_after=2, delta=2. H[2]=0+2=2. Add pos[2] to BIT.
v=1: total_low=1 (cnt[0]=1), pos[1]=[2], BIT has pos[2]=1, so BIT.query(2)=1. low_before = (2-1)-1=0. low_after = 1-0=1. delta=1. H[1]=2+1=3. Add pos[1] to BIT.
v=0: total_low=0, pos[0]=[3], BIT has pos[2]=1, pos[1]=2, so BIT.query(3)=2. low_before = (3-1)-2=0. low_after=0-0=0. delta=0. H[0]=3+0=3.
So H[3]=0, H[2]=2, H[1]=3, H[0]=3.
Now for k=0: T=3, cnt_low=3, cnt_high=0, H=0. ans=3+0-0=3.
k=1: T=2, cnt_low=2, cnt_high=1, H=2. ans=3+2-4=1.
k=2: T=1, cnt_low=1, cnt_high=2, H=3. ans=3+2-6=-1? But sample says 1. So still wrong.

Wait, for k=2, T=1. cnt_low = number of elements with A_i <1 = value 0: count=1. cnt_high=2. H[1]=3. ans=3+1*2 - 2*3 = 3+2-6=-1. But sample output for k=2 is 1. So something is still off.

Let's compute manually for k=2: B = (A_i+2) mod 3: (2+2)%3=1, (1+2)%3=0, (0+2)%3=2. So B=(1,0,2). Inversions: (1,0) is inversion, (1,2) not, (0,2) not. So 1 inversion. So ans=1.

Our formula gives -1. So the formula inv(k) = inv_total + cnt_low * cnt_high - 2*H(T) is not correct? Let's re-derive.

We had: inv(k) = S1(k) + S2(k) + S3(k).
S1(k): pairs with both low, A_i > A_j.
S2(k): pairs with both high, A_i > A_j.
S3(k): pairs with low before high, regardless of values.
And inv_total = S1(k) + S2(k) + S4(k), where S4(k): pairs with high before low and A_i > A_j.
So inv(k) = inv_total - S4(k) + S3(k).
Now, S3(k) = number of pairs with low before high. S4(k) = number of pairs with high before low and A_i > A_j. But note that in the high before low case, since high values are >= T and low values are < T, we have A_i >= T > A_j? Actually, if A_i >= T and A_j < T, then A_i > A_j is always true because T is an integer and A_i >= T, A_j <= T-1. So A_i > A_j always. So S4(k) is simply the number of pairs with high before low. So S4(k) = H(k). And S3(k) = L(k). So inv(k) = inv_total - H(k) + L(k). And L(k) + H(k) = cnt_low * cnt_high. So inv(k) = inv_total + cnt_low * cnt_high - 2*H(k). That seems correct.

But in sample, for k=2, T=1, cnt_low=1, cnt_high=2, H(1)=? Let's compute H(1) manually: T=1, high: values >=1, i.e., values 1 and 2. Low: value 0. Sequence: positions: 1:2, 2:1, 3:0. High before low: pairs where high element is before low element. High elements at positions 1 and 2. Low element at position 3. So pairs: (1,3) and (2,3). So H=2. But our computed H[1]=3. So our H[1] is wrong. Let's recalc H[1] using our algorithm.

We had H[1]=3 from the algorithm. But manual H(1)=2. So the algorithm overcounted.

Let's trace the algorithm for v=1: total_low = number of elements with value <1 = cnt[0]=1. pos[1]=[2]. BIT at that point contains pos[2]=[1]. So BIT.query(2)=1. low_before = (2-1)-1=0. low_after = total_low - low_before = 1-0=1. So delta=1. That seems correct: for the element at position 2 with value 1, the number of low elements after it is 1 (the element at position 3 with value 0). So that contributes 1 to H when T=1? But wait, when T=1, high group is values >=1, so value 1 is high. So the pair (2,3) is high before low, so it should be counted. So delta for v=1 should be 1. But we also have v=2: delta=2. So total H(1) = delta_2 + delta_1 = 2+1=3. But manual H(1)=2. Why the discrepancy? Because when T=1, high group includes both values 1 and 2. The pairs are: (1,3) from value 2, and (2,3) from value 1. That's 2 pairs. But our algorithm counted 3. So where is the extra pair? Let's list all pairs with high before low when T=1:
High elements: positions 1 (value 2) and 2 (value 1). Low element: position 3 (value 0).
Pairs: (1,3) and (2,3). That's 2.
But our algorithm for v=2 gave delta=2: for position 1, low_after = total_low (which is 2) - low_before (0) = 2. That means we counted 2 low elements after position 1. But at that time, total_low is number of elements with value <2, which is values 0 and 1: count=2. So low elements after position 1 are positions 2 and 3. But position 2 has value 1, which is not low when T=1? Wait, when we are processing v=2, we are computing delta for when v=2 becomes high. At that moment, the threshold is T=2? Actually, when we process v=2, we are adding value 2 to the high group. So the new threshold is T=2? Or T=1? Let's clarify the mapping.

We want H[T] for threshold T. We process values v from M-1 down to 0. For each v, we compute the increase in H when we move the threshold from T=v+1 to T=v. That is, when we add value v to the high group. So for v=2, we are moving from T=3 to T=2. So the delta for v=2 is the number of pairs with A_i=2 and A_j <2, i<j. That is correct: pairs where the 2 is before a low element (value <2). At T=2, low group is values <2, i.e., values 0 and 1. So for position 1 (value 2), the low elements after it are positions 2 and 3. So delta=2. That gives H[2]=2. Then for v=1, we move from T=2 to T=1. The delta for v=1 is the number of pairs with A_i=1 and A_j <1, i<j. At T=1, low group is values <1, i.e., value 0 only. So for position 2 (value 1), the low elements after it are only position 3. So delta=1. That gives H[1]=H[2]+1=3. But H[1] should be the number of pairs with A_i >=1 and A_j <1, i<j. That includes pairs from both value 2 and value 1. So it should be: from value 2: pairs (1,3) and (1,2)? Wait, (1,2): A_i=2, A_j=1. But when T=1, A_j=1 is not <1, so (1,2) is not counted because A_j is not low. So only (1,3) is counted from value 2. From value 1: (2,3) is counted. So total 2. But our delta for v=2 counted (1,2) and (1,3). So the issue is that when we computed delta for v=2, we used total_low = number of elements with value <2, which includes value 1. But when we later move to T=1, the element with value 1 becomes high, so the pair (1,2) should not be counted in H[1] because A_j=1 is not low. So our incremental approach double-counts or miscounts because the definition of low changes.

We need to compute H[T] directly for each T, not incrementally by adding deltas that depend on the current low group. Because when we add a value to high, the low group shrinks, so pairs that were counted as low before might become high. So the incremental approach is not straightforward.

We need a different method to compute H[T] for all T.

Let's think: H[T] = number of pairs (i,j) with i<j, A_i >= T, A_j < T.
We can compute this by iterating over all pairs? Too slow.
We can precompute for each pair (i,j) the condition A_i >= T and A_j < T. This is equivalent to T <= A_i and T > A_j. So for a given pair (i,j) with A_i > A_j, it contributes to H[T] for all T such that A_j < T <= A_i. So H[T] is the number of pairs (i,j) with i<j, A_i > A_j, and A_j < T <= A_i.
Thus, H[T] = sum over pairs (i,j) with i<j, A_i > A_j of I(A_j < T <= A_i).
So if we can compute for each T, the number of such pairs, we can do it by processing pairs in order of A_i and A_j.

We can think of it as: for each value v, consider pairs where A_i = v and A_j < v. For a fixed v, the pairs (i,j) with A_i=v, A_j<v, i<j contribute to H[T] for T in (A_j, v]. So for each such pair, it contributes to H[T] for T from A_j+1 to v. So we can add to an array H_diff: for each pair, we add 1 to H_diff[A_j+1] and subtract 1 from H_diff[v+1]? Actually, we want H[T] = sum_{pairs} I(A_j < T <= A_i). So we can do a difference array: for each pair, we increment a counter at A_j+1 and decrement at A_i+1. Then prefix sum gives H[T].

But the number of pairs is O(N^2), too many.

We need a smarter way. Since M is up to 2e5, we can compute H[T] by iterating T from 1 to M and using a BIT to count pairs dynamically.

Consider T from 1 to M. We want H[T] = number of pairs (i,j) with i<j, A_i >= T, A_j < T.
We can process T in increasing order. When T increases by 1, the condition A_i >= T becomes stricter: elements with value T-1 move from high to low? Actually, as T increases, the high group shrinks. So it's easier to process T in decreasing order, as we did. But we need to correctly account for the changing low group.

Let's process T from M down to 1. Initially T=M: high group empty, H[M]=0.
When we decrease T to T-1, the value T-1 moves from low to high. So we need to add to H the number of pairs (i,j) with i<j, A_i = T-1, A_j < T-1. But note that at this moment, the low group is values < T-1. So we need to count for each position i with A_i = T-1, the number of low elements after i. The low elements are those with value < T-1. So we need to know, for each position i, how many elements after i have value < T-1. This is similar to before, but now we need to count low elements after i, not before. And the set of low elements is fixed for this T: it's all elements with value < T-1. So we can compute this if we know the positions of low elements. But as T changes, the set of low elements changes. However, if we process T in decreasing order, when we move from T to T-1, the low group loses the value T-1. So the low elements become those with value < T-1. So we need to count, for the new high elements (value T-1), the number of low elements after them. But the low elements are exactly the elements with value < T-1. So we can precompute for each value v, the positions. Then for a given T, the low elements are values 0..T-2. So we need to count, for each position i with A_i = T-1, the number of positions j > i with A_j in [0, T-2]. This is like: for each position i, we want to know how many low elements are after it. We can compute this by iterating positions in reverse order and maintaining a BIT over values? Or we can precompute an array next_low[i] = number of low elements after i for each possible T? That seems complicated.

Alternative: We can compute H[T] by iterating over all pairs (i,j) with i<j and A_i > A_j, and for each such pair, it contributes to H[T] for T in (A_j, A_i]. So we can do a difference array on T. But we need to generate these pairs efficiently. We can use a BIT to count for each element, the number of smaller elements after it? Actually, for each position i, we want to count the number of j > i with A_j < A_i. That's exactly the number of inversions where i is the left element. Let inv_right[i] = number of j > i with A_j < A_i. Then for each such pair, it contributes to H[T] for T from A_j+1 to A_i. So we can update a difference array: for each j > i with A_j < A_i, we add 1 to diff[A_j+1] and subtract 1 from diff[A_i+1]. Then prefix sum gives H[T]. But we need to do this for all pairs, which is O(N^2). However, we can aggregate by value. For each value v, consider all positions i with A_i = v. For each such i, we want to add to diff for each j > i with A_j < v. We can do this by processing values v from M-1 down to 0, and for each v, we process positions i with A_i = v in order, and for each i, we query a BIT that stores the counts of values < v for positions > i? Actually, we can process from right to left: maintain a BIT over values that stores the counts of elements to the right. For each position i from N down to 1, we query the BIT for the number of elements with value < A_i. That gives inv_right[i]. Then for each such pair (i,j) with A_j < A_i, we need to update diff[A_j+1] += 1, diff[A_i+1] -= 1. But we don't know A_j individually; we only know the count. We need to distribute the count over the possible A_j values. So we can maintain another BIT over values to accumulate the contributions? This seems messy.

Maybe we can compute H[T] directly using a BIT over positions and values. Let's think differently.

We have inv(k) = inv_total + cnt_low * cnt_high - 2*H(T). We can compute inv(k) for all k by simulating the shift and updating the inversion count incrementally, but correctly.

We can maintain the current inversion count as we shift k from 0 to M-1. When we increase k by 1, the values change as described. We can update the inversion count by considering the effect of the shift on each element. But we need to do it efficiently.

Let's consider the effect of shifting all values by 1 mod M. This is equivalent to: for each element, if its value is M-1, it becomes 0; otherwise it becomes v+1. The relative order between two elements changes only if one wraps and the other doesn't, or both wrap. As we saw, if both don't wrap, order unchanged. If both wrap, both become 0, order unchanged (equal). If one wraps (say i wraps, j doesn't), then originally B_i = M-1, B_j = v. After shift, B_i = 0, B_j = v+1. So if originally B_i > B_j (always true), after shift B_i < B_j, so the inversion disappears. If originally B_i < B_j (impossible), after shift it might become an inversion. So for each pair where exactly one wraps, the inversion status flips. Specifically, if the wrapping element is the left element (i<j and i wraps), then originally it was an inversion, after shift it is not. So we lose an inversion. If the wrapping element is the right element (i<j and j wraps), then originally it was not an inversion (since left is non-wrap, value < M-1, so left < right), after shift it becomes an inversion (left becomes v+1, right becomes 0, so left > right). So we gain an inversion. So the net change in inversion count when shifting by 1 is: (number of pairs where the right element wraps) - (number of pairs where the left element wraps). Let x = number of wrapping elements. Let L = number of wrapping elements that are left in their pair with a non-wrap. More precisely, for each wrapping element at position i, let l_i = number of non-wrap elements before i, and r_i = number of non-wrap elements after i. Then the net change is sum_{i in wrap} (r_i - l_i). Because for each wrap element, it gains inversions with non-wrap elements after it, and loses inversions with non-wrap elements before it. So Δ = sum_{i in wrap} (r_i - l_i). Note that l_i + r_i = N - x (since there are x wrap elements total, and for a given wrap element, the non-wrap elements are all other elements). So r_i - l_i = (N - x) - 2*l_i. So Δ = x*(N-x) - 2*sum_{i in wrap} l_i.

So if we can compute for each k, the set of wrapping elements (those with value M-1 in the current shifted sequence), and for each, the number of non-wrap elements before it, we can compute Δ. But the set of wrapping elements changes as k changes. Specifically, an element wraps when its current value is M-1. So we need to know, for each k, which elements have value M-1 in the sequence B for that k. That is equivalent to: A_i + k ≡ M-1 mod M => A_i ≡ M-1-k mod M. So the wrapping elements for shift k are those with A_i = (M-1-k) mod M. So as k increases, the wrapping value cycles through M-1, M-2, ..., 0.

So we can precompute for each value v, the positions where A_i = v. Then for each k, the wrapping elements are pos[(M-1-k) mod M]. So we can iterate k from 0 to M-1, and for each k, we know the set of wrapping elements. We need to compute sum_{i in wrap} l_i, where l_i is the number of non-wrap elements before i. But non-wrap elements are all elements except those in wrap. So l_i = (i-1) - (number of wrap elements before i). So we need to know, for each position i in the wrap set, how many wrap elements are before i. That depends on the order of positions in the wrap set. Since the wrap set is just the positions of a particular value, we can precompute for each value v, the list of positions. Then for a given k, the wrap value is w = (M-1-k) mod M. So we need to compute for each position i in pos[w], the number of elements in pos[w] before i. That is easy: if pos[w] = [p1, p2, ..., px] in increasing order, then for pj, the number of wrap elements before it is j-1. So l_i = (i-1) - (j-1). So sum_{i in pos[w]} l_i = sum_{j=1}^{x} ( (p_j - 1) - (j-1) ) = sum_{j=1}^{x} (p_j - j). So we can precompute for each value v, the sum of (p_j - j) over its positions. Let's denote S_v = sum_{j=1}^{cnt[v]} (p_j - j), where p_j are the positions of value v in increasing order.

Then for shift k, wrap value w = (M-1-k) mod M. Then sum_{i in wrap} l_i = S_w. And x = cnt[w]. So Δ = x*(N-x) - 2*S_w.

Then we can compute inv(k) iteratively: inv(0) = inv_total. For k from 1 to M-1, inv(k) = inv(k-1) + Δ, where Δ is computed for the transition from k-1 to k. But careful: when we go from k-1 to k, the wrap value changes. Specifically, for shift k-1, the wrap value is (M-1-(k-1)) mod M = (M-k) mod M. For shift k, the wrap value is (M-1-k) mod M. So the set of wrapping elements changes from value (M-k) mod M to value (M-1-k) mod M. So the elements that wrap at step k are those with value (M-1-k) mod M. So we can compute Δ_k = cnt[w] * (N - cnt[w]) - 2 * S_w, where w = (M-1-k) mod M.

Then inv(k) = inv(k-1) + Δ_k.

Let's test with sample 1: N=3, M=3, A=(2,1,0).
inv_total=3.
Compute S_v:
pos[2]=[1], so S_2 = (1-1)=0.
pos[1]=[2], so S_1 = (2-1)=1.
pos[0]=[3], so S_0 = (3-1)=2.
Now for k=1: w = (M-1-1) mod 3 = (2-1)=1 mod 3 =1. cnt[1]=1, S_1=1. Δ_1 = 1*(3-1) - 2*1 = 2 - 2 = 0. So inv(1)=3+0=3? But sample says 1. So still wrong.

Wait, our Δ formula might be incorrect. Let's derive carefully.

We have sequence B for shift k. We want to compute B' for shift k+1. The transformation: B'_i = (B_i + 1) mod M.
Let wrap set W = { i | B_i = M-1 }. For i in W, B'_i = 0. For i not in W, B'_i = B_i + 1.
We want to compute the change in inversion count from B to B'.
Consider a pair (i,j) with i<j.
Case 1: Both not in W. Then B'_i = B_i+1, B'_j = B_j+1. So B'_i > B'_j iff B_i > B_j. So inversion status unchanged.
Case 2: Both in W. Then B'_i = 0, B'_j = 0. So B'_i > B'_j is false. Originally, B_i = M-1, B_j = M-1, so B_i > B_j false. So unchanged.
Case 3: i in W, j not in W. Originally: B_i = M-1, B_j = v (v < M-1). So B_i > B_j true. After: B'_i = 0, B'_j = v+1. So B'_i > B'_j false. So inversion lost.
Case 4: i not in W, j in W. Originally: B_i = v (v < M-1), B_j = M-1. So B_i > B_j false. After: B'_i = v+1, B'_j = 0. So B'_i > B'_j true. So inversion gained.

So for each pair with exactly one in W, the inversion status flips. Specifically, if the left element is in W, we lose an inversion. If the right element is in W, we gain an inversion.
So net change Δ = (number of pairs with right in W) - (number of pairs with left in W).
Let x = |W|.
For each i in W, let l_i = number of non-W elements before i, r_i = number of non-W elements after i.
Then number of pairs with left in W and right not in W = sum_{i in W} l_i.
Number of pairs with left not in W and right in W = sum_{i in W} r_i.
So Δ = sum_{i in W} r_i - sum_{i in W} l_i = sum_{i in W} (r_i - l_i).
Now, l_i + r_i = N - x (since total non-W elements = N-x).
So r_i - l_i = (N-x) - 2*l_i.
Thus Δ = x*(N-x) - 2*sum_{i in W} l_i.
Now, l_i = number of non-W elements before i = (i-1) - (number of W elements before i).
So sum_{i in W} l_i = sum_{i in W} (i-1) - sum_{i in W} (number of W elements before i).
Let the positions of W be p_1 < p_2 < ... < p_x.
Then for p_j, number of W elements before it is j-1.
So sum_{i in W} (number of W elements before i) = sum_{j=1}^{x} (j-1) = x*(x-1)/2.
And sum_{i in W} (i-1) = sum_{j=1}^{x} (p_j - 1).
So sum_{i in W} l_i = sum_{j=1}^{x} (p_j - 1) - x*(x-1)/2.
Thus Δ = x*(N-x) - 2*( sum_{j=1}^{x} (p_j - 1) - x*(x-1)/2 ) = x*(N-x) - 2*sum_{j=1}^{x} (p_j - 1) + x*(x-1).
Simplify: x*(N-x) + x*(x-1) = x*(N-1). So Δ = x*(N-1) - 2*sum_{j=1}^{x} (p_j - 1).
But note that sum_{j=1}^{x} (p_j - 1) = sum_{j=1}^{x} p_j - x.
So Δ = x*(N-1) - 2*(sum p_j - x) = x*(N-1) - 2*sum p_j + 2x = x*(N+1) - 2*sum p_j.
Alternatively, we can write Δ = x*(N-x) - 2*sum_{j=1}^{x} (p_j - j) because sum_{j=1}^{x} (p_j - 1) - x*(x-1)/2 = sum_{j=1}^{x} (p_j - j). Let's check:
sum_{j=1}^{x} (p_j - j) = sum p_j - sum j = sum p_j - x*(x+1)/2.
But we had sum_{i in W} l_i = sum (p_j - 1) - x*(x-1)/2 = sum p_j - x - x*(x-1)/2 = sum p_j - x*(x+1)/2. Yes, so sum_{i in W} l_i = sum_{j=1}^{x} (p_j - j). So Δ = x*(N-x) - 2*sum_{j=1}^{x} (p_j - j).

So Δ = x*(N-x) - 2*S_w, where S_w = sum_{j=1}^{x} (p_j - j) for the positions of the wrap value w.

Now test with sample 1: For k=0, we want to compute inv(0)=3. For k=1, we need Δ from k=0 to k=1. The wrap value for the transition from k=0 to k=1 is the value that wraps when we add 1. In B for k=0, the values are A_i. The wrap value is M-1 = 2. So w=2. pos[2]=[1], x=1, S_2 = (1-1)=0. Δ = 1*(3-1) - 2*0 = 2. So inv(1) = 3 + 2 = 5? But sample says 1. So still wrong.

Wait, maybe the direction: when we go from k to k+1, we are adding 1 to each B_i. So the wrap value is the value that becomes M-1 after adding 1? Actually, if B_i = M-1, then B_i+1 mod M = 0. So the wrap value is M-1. So for transition from k to k+1, the wrap value is M-1 in the current B (for shift k). So