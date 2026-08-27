We need inversion count for each k of B_i = (A_i + k) mod M. For k=0 we can compute directly via BIT or mergesort. When we increase k by 1, each B_i either stays same (if A_i + k < M) or wraps (if A_i + k == M, becomes 0) or increases by 1 (if A_i + k < M - 1). However, we can think in terms of moving elements across the boundary. A cleaner approach: For each k, the multiset of B values is just the multiset of A values shifted cyclically. Inversions for a circular shift can be updated from k to k+1 using the count of elements equal to 0 (or M-1) in the current B.

Specifically, let cnt[v] be the count of original A_i equal to v. For a given k, the value x appears as (x - k mod M) = (x - k + M) % M. So inversion count I(k) counts pairs (i<j) with B_i > B_j, equivalently pairs where (A_i - k) mod M > (A_j - k) mod M.

When k increases by 1, each value decreases by 1 modulo M. A pair (i,j) that was an inversion may cease to be, and some non-inversion may become inversion. A known technique: Let Z_k be the number of indices with B_i = 0 when shift is k, i.e., count of A_i == k. For total N(N-1)/2 pairs, the number of inversions for shift k can be computed by: I(k+1) = I(k) - Z_k + (N - Z_k) = I(k) + N - 2*Z_k. Wait, need to verify.

Actually, consider shift: B^{(k)}_i = (A_i + k) mod M. Let f(k) = inv(B^{(k)}). For k to k+1: add 1 to each B_i; those that were M-1 become 0 (wrap), others just +1. When we add 1 to every element, the relative order of non-wrapping elements stays the same (they all shift equally). The only changes: each M-1 becomes 0, which is now smaller than many elements. For each element that wraps (was M-1, now 0), it loses inversions with elements it was greater than (all other elements except itself), but the new 0 may create inversions with elements smaller than 0 (none). Actually, the count change: An element that was M-1 was larger than all other B_j (since max is M-1). So it contributed (N-1) inversions originally (with everyone after it? wait inversion count counts pairs (i<j) with B_i > B_j. Position matters! So we can't just count per element globally; need position information. So simple formula above is not correct.

Alternative approach: Since N,M up to 2e5, we can compute I(k) independently for each k using BIT and processing the shifted values in order of original indices. For each k, we need inversion count of sequence B^{(k)} defined as (A_i + k) mod M. The original order of indices i is fixed; only values change. This is like a sliding window of shift.

Observation: When we go from k to k+1, B_i increases by 1, except those where A_i + k = M-1, then B_i becomes 0. So the only values that change are those that wrap from M-1 to 0. For those indices, their value changes drastically (from max to min). Others just increase by 1, preserving relative order among them.

We can think of the effect on inversion count:
- For a pair (i,j) where neither wraps (both values increase by 1), their relative order stays the same, so contribution unchanged.
- For a pair (i,j) where exactly one wraps, say i wraps (was M-1, becomes 0), and j does not (increases by 1), we need to compare new values: 0 vs old B_j+1 (which is >=1). So 0 < something, so if originally i was M-1 > B_j (since M-1 > anything), the pair was an inversion; after change, it's not. So the inversion count decreases by 1 for each such pair where i<j and i wraps.
- If i does not wrap, j wraps, originally B_i > B_j? Since j was M-1 > B_i, so not inversion. After change, B_i > 0? Since B_i (non-wrapping) increased by 1, so B_i >=1, and j becomes 0, so B_i > B_j, so inversion count increases by 1 for each such pair where i<j and j wraps.
- If both wrap (both A_i = A_j = M-1-k originally? wait wrap condition depends on A_i + k = M-1, i.e., A_i = M-1-k). For such pair, both were M-1 before, both become 0. The relative order between them (both equal) does not create inversion, and still 0 vs 0 equal, so no change. So wrap-wrap pairs unchanged.

Thus the net change from k to k+1 is:
Delta = (# of pairs (i<j) where j wraps and i does not) - (# of pairs (i<j) where i wraps and i does not) = ?

Let W_k = set of indices i where A_i + k = M-1 (i.e., A_i = M-1-k). For k from 0 to M-1, each index i belongs to exactly one W_k (since A_i is fixed, k = (M-1 - A_i) mod M). So W_k are the wrapping indices for shift k. Let w_k = |W_k| = count of A_i == (M-1 - k) mod M. For convenience define target value t_k = (M-1 - k) mod M, but we can just index k by the value that wraps at that step.

Now, define L = # of wrapping indices before non-wrapping indices? Actually, we need count of pairs (i<j) where i wraps, j doesn't (i in W_k, i<j) and pairs where i doesn't, j wraps (i not in W_k, j in W_k). The delta from k to k+1 is:
Delta_k = (# pairs (i<j) with j in W_k, i not in W_k) - (# pairs (i<j) with i in W_k, j not in W_k).

Let’s denote the sequence of positions. Let total pairs = N(N-1)/2. For each pair, exactly one of three cases: both wrap, i wraps, j wraps, or neither. The sum of i-wraps-j-not and j-wraps-i-not over all pairs is total pairs where exactly one wraps. Let X_k = # pairs with exactly one wrapping index.

We can compute delta_k = (# of i not wrap, j wrap) - (# of i wrap, j not wrap). Let’s denote A = # pairs i in W_k, j not in W_k, i<j. B = # pairs i not in W_k, j in W_k, i<j. Then delta = B - A.

Note that A + B = X_k.

Also, total pairs = C(w_k,2) + A + B + C(N-w_k,2). Where C(n,2) = n(n-1)/2.

We can compute delta directly using positions? Maybe we can compute A and B efficiently.

Observation: For each wrapping index i, the number of non-wrapping indices j > i is (N - i) - (# of wrapping indices after i). Similarly, for each wrapping index i, the number of non-wrapping indices j < i is (i-1) - (# of wrapping indices before i). So:
A = sum_{i in W_k} (number of non-wrapping indices after i).
B = sum_{i in W_k} (number of non-wrapping indices before i).

Thus delta = B - A = sum_{i in W_k} ( (i-1) - wrap_before_i - ( (N-i) - wrap_after_i ) )? Wait, for each i in W_k, its contribution to B (pairs where i is j, i.e., non-wrap before wrap) is count of non-wrap indices before i. Its contribution to A (pairs where i is i, i.e., wrap before non-wrap) is count of non-wrap indices after i. So net contribution of i to delta is (#non-wrap before i) - (#non-wrap after i).

Let’s define for each i, let left_nonwrap_i = i-1 - wrap_before_i. right_nonwrap_i = (N-i) - wrap_after_i. Then delta = sum_{i in W_k} (left_nonwrap_i - right_nonwrap_i).

But we can also compute delta using global counts. Note that for any set W, the sum over i in W of ( (#non-wrap before i) - (#non-wrap after i) ) = ?

Let total_nonwrap = N - w_k. Let’s consider all pairs (i,j) where i in W, j not in W. The sum of (j - i) over all such pairs? Wait, left_nonwrap_i - right_nonwrap_i is essentially (position of i relative to non-wraps). Maybe we can express delta as something like: delta = w_k * total_nonwrap - 2 * sum_{i in W} rank_of_i_among_nonwrap? Not sure.

Alternative viewpoint: When we go from k to k+1, the only change in B is that some values M-1 become 0, and all others increase by 1. The relative ordering of non-wrapping elements among themselves remains same. So we can think of the inversion count as sum of inversions within non-wrapping group plus inversions between wrapping and non-wrapping groups.

Let’s denote for shift k:
- Set W = indices with B_i = M-1 (i.e., A_i = M-1-k).
- Set R = indices with B_i != M-1.

Within R, all values are in [0, M-2], and they all increase by 1 when k increments (except those that become M-1? Wait, at k+1, the new M-1 will be those with A_i = M-1-(k+1) = (M-1-k)-1 = A_i -1. So the set of M-1 for k+1 is a different set. For R_k (non-wrapping at step k), their new values are either in [1, M-1] (if they didn't become M-1 at k+1) or wrap to 0 (if they become M-1 at k+1). Actually, from perspective of transition: At step k, W_k are M-1. At step k+1, W_{k+1} are those that were M-2 at step k? Let's check: B_i^{(k)} = (A_i + k) mod M. It equals M-1 when A_i + k ≡ M-1 (mod M). At k+1, condition is A_i + k+1 ≡ M-1 => A_i + k ≡ M-2 (mod M). So W_{k+1} = indices where B_i^{(k)} = M-2. So when moving to k+1, the old M-2 become M-1? No, B_i^{(k+1)} = B_i^{(k)} + 1 (if B_i^{(k)} < M-1) else 0. So the ones that were M-2 become M-1 at k+1. So the set of M-1 values changes to the previous M-2 values.

Thus the set of indices that are "large" changes by shifting which indices are max. This seems complex to update incrementally.

Given constraints (N,M ≤ 2e5), we can compute each I(k) independently in O(N log M) using BIT: For each k, we need to count inversions in array B^{(k)} where B_i = (A_i + k) mod M. Since k is just a constant shift, we can pre-sort the values? Actually, the order of indices is fixed. For each k, we can process indices i=1..N, query BIT for number of previous elements > current B_i. But we need to do this for M different k. Doing M times O(N log M) is too slow (M*N up to 4e10). We need smarter.

Observation: The values B_i^{(k)} are a permutation of the values (A_i + k) mod M. Since addition mod M is a bijection on the set of values, the multiset of B values is just the multiset of A values shifted. So the distribution of values is same for all k. However, the assignment to positions depends on k.

But note: For each position i, as k varies, B_i cycles through all M values in order (0,1,...,M-1,0,1...). So each position's value is a linear function of k: B_i(k) = (A_i + k) mod M. So the inversion count I(k) is a function of k defined by counting pairs i<j where (A_i + k) mod M > (A_j + k) mod M.

This is similar to counting inversions in a sequence where each element is (A_i + k) mod M. Since addition by k is a cyclic shift, the relative order of two elements depends on whether A_i + k and A_j + k cross the modulus boundary.

Specifically, for two indices i<j, consider the difference d = A_i - A_j (mod M). Then B_i > B_j iff (A_i + k) mod M > (A_j + k) mod M. Let x = A_i + k, y = A_j + k. Then x mod M > y mod M. This is equivalent to: either x < y (no wrap for either) then x > y? Wait, if x,y are in [0,M-1] (no wrap), then x > y means A_i + k > A_j + k => A_i > A_j. If A_i > A_j, then for all k such that no wrap, B_i > B_j. But when wrap occurs for one of them, the comparison changes.

Let’s define for pair (i,j), i<j. Let delta = A_i - A_j. Then B_i > B_j iff (A_i + k) mod M > (A_j + k) mod M. Let’s consider the cyclic order: Adding k shifts both by same amount. The condition depends on the relative position of the interval between A_i and A_j around the circle. Actually, the condition is true if the clockwise distance from A_j to A_i is less than M/2? Not exactly.

Better: B_i > B_j iff (A_i + k) - (A_j + k) = A_i - A_j is in (0, M) modulo M? Wait, (x mod M) > (y mod M) is not determined solely by (x - y) mod M because of wrap-around. For example, x=0, y=M-1: x mod M = 0, y mod M = M-1, but x - y ≡ 1 mod M (since 0 - (M-1) = 1). Here x mod M < y mod M, but x-y mod M = 1. So the condition is not just based on the difference mod M.

But we can think: For fixed i,j, as k varies from 0 to M-1, the condition (A_i + k) mod M > (A_j + k) mod M changes exactly once? Let's examine. Define f(k) = ((A_i + k) mod M) - ((A_j + k) mod M). As k increases by 1, both terms increase by 1 unless they wrap. The difference changes when one of them wraps. Specifically, when A_i + k ≡ M-1 (mod M) and A_j + k ≠ M-1, then A_i + k + 1 becomes 0, dropping by M-1 relative to A_j + k + 1 (which becomes something). So f(k) may jump.

Actually, consider the function g(k) = 1 if (A_i + k) mod M > (A_j + k) mod M, else 0. As k increments, the relative order can change only when one of the two values wraps around (i.e., when A_i + k ≡ M-1 or A_j + k ≡ M-1). At that k, the wrapped value drops to 0, possibly crossing the other. So g(k) is piecewise constant with changes at k = (M-1 - A_i) mod M and k = (M-1 - A_j) mod M. There are at most two change points per pair.

Since M,N up to 2e5, total pairs N(N-1)/2 up to 2e10, too many. We need a smarter way.

Alternative approach: Since the array values are just shifted cyclically, we can precompute the inversion count for k=0 using BIT in O(N log M). Then we can compute I(k+1) from I(k) by adjusting for the effect of the shift. There is known trick: For cyclic shifts, I(k+1) = I(k) + (N - 2 * cnt_k) where cnt_k is the number of zeros in B^{(k)}? Let's test with sample.

Sample 1: N=3, M=3, A=[2,1,0].
k=0: B=[2,1,0], inv=3.
k=1: B=[0,2,1], inv=1.
k=2: B=[1,0,2], inv=1.

cnt_k = count of B_i == 0.
k=0: B=[2,1,0], cnt=1. N=3. N - 2*cnt = 3 - 2 = 1. I(0)+1 = 4, not 1. So that formula is wrong.

Wait, maybe formula is I(k+1) = I(k) - (N - 2*cnt_k) or something? Let's test: I(0)=3, N-2*cnt=1, I(0)-1=2, not 1. So no.

Let's try to compute delta directly. For k=0 to k=1: W_0 = indices where A_i + 0 = M-1 = 2. A_i=2: i=1. So W_0 = {1}. w_0=1. Non-wrapping indices: {2,3} (i=2,3). Pairs: (1,2): i wraps, j not. So A count = 1 (wrap before non-wrap). Pairs (i,j) with i not wrap, j wrap: only possible if j is wrap and i before j. j=1 is wrap, but no i before 1. So B=0. Delta = B - A = -1. So I(1) = I(0) + delta = 3 - 1 = 2. But actual I(1)=1. So still off by -1. Did we miss something? Let's compute manually: B^{(0)} = [2,1,0]. Inversions: (1,2):2>1 yes, (1,3):2>0 yes, (2,3):1>0 yes => 3.
B^{(1)} = [0,2,1]. Inversions: (1,2):0>2 no, (1,3):0>1 no, (2,3):2>1 yes => 1.
So delta = -2. Our delta calculation gave -1. So we missed the case where both wrap? No both wrap not here. Let's compute A and B for W_0 = {1}. Non-wrap = {2,3}.
Pairs with i in W, j not in W, i<j: (1,2), (1,3) => 2 pairs. So A=2. Pairs with i not in W, j in W, i<j: none => B=0. So delta = B - A = -2. Wait, earlier I said A=1, but there are two pairs: i=1, j=2 and i=1, j=3. So A=2. So delta = -2. Then I(1) = 3 - 2 = 1. Correct! So my earlier count of A was wrong (I mistakenly thought only (1,2) but (1,3) also). So formula delta = B - A is correct, where A = # pairs (i<j) with i in W, j not in W, B = # pairs (i<j) with i not in W, j in W.

Thus to compute I(k+1) from I(k), we need to know A_k and B_k for W_k = {i: A_i = (M-1 - k) mod M}. Then delta_k = B_k - A_k, and I(k+1) = I(k) + delta_k.

Now, can we compute A_k and B_k efficiently for all k? We need to know, for each value v (0..M-1), the set of positions where A_i = v. Let’s denote the positions of each value. For a given k, W_k corresponds to value v_k = (M-1 - k) mod M. So as k increases from 0 to M-1, v_k cycles through M-1, M-2, ..., 0.

Thus we need to compute, for each value v, the number of pairs (i<j) where i has value v and j has value != v (i.e., A_j != v). That's A for W corresponding to v. And B for v is number of pairs where i has value != v and j has value v.

Specifically, for a fixed value v, let S_v be the set of indices i with A_i = v. Let s_v = |S_v|. Let positions sorted: p_1 < p_2 < ... < p_{s_v}. Then:
- A_v = number of pairs (i<j) with i in S_v, j not in S_v. This equals sum_{i in S_v} (N - i - (number of elements of S_v after i)). For each position p_t, the number of non-v elements after it is (N - p_t) - (s_v - t). So A_v = sum_{t=1}^{s_v} ((N - p_t) - (s_v - t)) = s_v * N - sum p_t - (s_v*(s_v-1)/2). Wait, sum over t of (s_v - t) = sum_{u=0}^{s_v-1} u = s_v(s_v-1)/2. So A_v = sum_{t} (N - p_t) - s_v(s_v-1)/2 = s_v * N - sum_{t} p_t - s_v(s_v-1)/2.

Similarly, B_v = number of pairs (i<j) with i not in S_v, j in S_v. For each position p_t, number of non-v elements before it is (p_t - 1) - (t-1) = p_t - t. So B_v = sum_{t=1}^{s_v} (p_t - t) = sum_{t} p_t - s_v(s_v+1)/2? Wait, sum_{t=1}^{s_v} t = s_v(s_v+1)/2. So B_v = sum p_t - s_v(s_v+1)/2.

Alternatively, we can compute A_v and B_v using prefix sums. Since s_v is the count of value v, and we know sum of positions of value v, we can compute A_v and B_v in O(1) per v if we precompute for each value the count and sum of positions.

Specifically, for each v, we can iterate through the array and accumulate cnt[v] and sum_pos[v] (sum of indices i where A_i = v, using 1-indexed positions). Then:
A_v = cnt[v] * N - sum_pos[v] - cnt[v]*(cnt[v]-1)/2.
B_v = sum_pos[v] - cnt[v]*(cnt[v]+1)/2.

Let's verify with sample 1: N=3, A=[2,1,0] (1-indexed: pos1=2, pos2=1, pos3=0).
Counts: cnt[0]=1 (pos3=3), cnt[1]=1 (pos2=2), cnt[2]=1 (pos1=1).
Sums: sum_pos[0]=3, sum_pos[1]=2, sum_pos[2]=1.

For k=0: W corresponds to v = (M-1 - 0) mod 3 = 2. So W = indices with A_i=2 => {1}. cnt=1, sum=1.
A_2 = 1*3 - 1 - 1*0/2 = 3 - 1 = 2. B_2 = 1 - 1*2/2 = 1 - 1 = 0. So delta = B - A = -2. I(1) = 3 - 2 = 1. Correct.

For k=1: v = (2-1)=1. W={2}. cnt=1, sum=2. A_1 = 1*3 - 2 - 0 = 1. B_1 = 2 - 1 = 1. delta = 0. So I(2) = I(1) + 0 = 1. Correct.

For k=2: v = (2-2)=0. W={3}. cnt=1, sum=3. A_0 = 3 - 3 = 0. B_0 = 3 - 1 = 2. delta = 2. But I(2) to I(0) (wrap around)? Actually, we need to go from k=2 to k=0 (mod M). The recurrence should hold cyclically: I((k+1) mod M) = I(k) + (B_{v_k} - A_{v_k}), where v_k = (M-1 - k) mod M. So for k=2, v=0, delta = B_0 - A_0 = 2 - 0 = 2. Then I(0) (next) would be I(2) + 2 = 1+2=3. But we are outputting for k=0,1,2, not cyclically beyond. The recurrence is for k from 0 to M-2: I(k+1) = I(k) + delta_k. For k=M-1, the next would be I(M) which is I(0) of next cycle, but we don't need it. However, we can compute I(0) independently and then iterate.

Thus algorithm:
1. Compute I(0) = inversion count of original array A. This can be done via BIT in O(N log M).
2. For each value v from 0 to M-1, compute cnt[v] and sum_pos[v] (1-indexed positions).
3. For each v, compute A_v and B_v.
4. Iterate k from 0 to M-2:
   - v = (M-1 - k) mod M.
   - delta = B_v - A_v.
   - I(k+1) = I(k) + delta.
   - Store answer for k+1.
5. Output I(0), I(1), ..., I(M-1).

Complexities: O(N + M) after O(N log M) for initial inversion count. M,N up to 2e5, so O((N+M) log M) is fine.

Let's test on sample 2: N=5, M=6, A=[5,3,5,0,1] (1-indexed: pos1=5, pos2=3, pos3=5, pos4=0, pos5=1).
Counts: cnt[0]=1 (pos4), cnt[1]=1 (pos5), cnt[3]=1 (pos2), cnt[5]=2 (pos1,pos3). Others 0.
Sums: sum_pos[0]=4, sum_pos[1]=5, sum_pos[3]=2, sum_pos[5]=1+3=4.
N=5.

Compute I(0) via BIT: B = A. Inversions:
(1,2):5>3 yes
(1,3):5>5 no
(1,4):5>0 yes
(1,5):5>1 yes
(2,3):3>5 no
(2,4):3>0 yes
(2,5):3>1 yes
(3,4):5>0 yes
(3,5):5>1 yes
(4,5):0>1 no
Total: 7. So I(0)=7. Output expects 7. Good.

Now compute A_v, B_v for each v:
v=0: cnt=1, sum=4.
A_0 = 1*5 - 4 - 0 = 1.
B_0 = 4 - 1 = 3.
v=1: cnt=1, sum=5.
A_1 = 5 - 5 = 0.
B_1 = 5 - 1 = 4.
v=2: cnt=0, sum=0. A_2 = 0? Let's compute formula: cnt=0 => A=0, B=0.
v=3: cnt=1, sum=2.
A_3 = 5 - 2 = 3.
B_3 = 2 - 1 = 1.
v=4: cnt=0.
v=5: cnt=2, sum=4.
A_5 = 2*5 - 4 - 1 = 10 - 4 - 1 = 5.
B_5 = 4 - 3 = 1? Wait cnt=2 => cnt*(cnt+1)/2 = 2*3/2=3. So B_5 = 4 - 3 = 1.

Check A_5 + B_5 + C(cnt,2) = 5+1+1=7 = total pairs with at least one 5? Actually total pairs = C(5,2)=10. Pairs with both 5: C(2,2)=1. So pairs with exactly one 5 = 10-1- C(3,2)? Wait non-5 count = 3, C(3,2)=3. So exactly one 5 = 10-1-3=6. But A_5 + B_5 = 6. Good.

Now compute I(k) sequentially.
k=0: v = (M-1 - 0) mod 6 = 5. delta = B_5 - A_5 = 1 - 5 = -4. I(1) = 7 - 4 = 3. Output expects 3. Good.
k=1: v = 4. cnt=0 => delta=0. I(2) = 3. Output expects 3. Good.
k=2: v = 3. delta = B_3 - A_3 = 1 - 3 = -2. I(3) = 3 - 2 = 1. Output expects 1? Wait sample output line 4 is 1 (k=3). Yes.
k=3: v = 2. delta=0. I(4)=1. Output line 5: 1. Yes.
k=4: v = 1. delta = B_1 - A_1 = 4 - 0 = 4. I(5) = 1 + 4 = 5. Output line 6: 5. Yes.
k=5: v = 0. delta = B_0 - A_0 = 3 - 1 = 2. I(6) would be 5+2=7 which is I(0) of next cycle, but we only need up to M-1=5. Output line 6 is 5. So we stop at k=5? Wait we need output for k=0..5. We have:
I(0)=7
I(1)=3
I(2)=3
I(3)=1
I(4)=1
I(5)=5.
Matches sample.

Great! The formula works.

Now test sample 3: N=7, M=7, A=[0,1,2,3,4,5,6].
I(0) = 0 (sorted).
Counts: each value appears once at position i+1.
For each v, cnt=1, sum = v+1.
A_v = 1*7 - (v+1) - 0 = 6 - v.
B_v = (v+1) - 1 = v.
So delta for v = B - A = v - (6 - v) = 2v - 6.
But v is (M-1 - k) mod M = 6 - k (since M=7). So v = (6 - k) mod 7.
Thus I(k+1) = I(k) + 2*(6-k) - 6 = I(k) + 12 - 2k - 6 = I(k) + 6 - 2k.
Compute:
k=0: I(0)=0.
k=1: I(1) = 0 + 6 - 0 = 6? Wait formula 6-2k: for k=0, delta = 2*0 - 6 = -6? Let's compute directly: v for k=0 is 6. delta = B_6 - A_6. cnt[6]=1, sum=7. A_6 = 7 - 7 = 0. B_6 = 7 - 1 = 6. delta = 6. So I(1)=6. Sample output line 2 is 6. Good.
k=1: v=5. cnt[5]=1, sum=6. A_5 = 7 - 6 = 1. B_5 = 6 - 1 = 5. delta = 4. I(2) = 6 + 4 = 10. Sample line 3: 10. Good.
k=2: v=4. sum=5. A=2, B=4. delta=2. I(3)=12. Sample: 12. Good.
k=3: v=3. sum=4. A=3, B=3. delta=0. I(4)=12. Sample: 12. Good.
k=4: v=2. sum=3. A=4, B=2. delta=-2. I(5)=10. Sample: 10. Good.
k=5: v=1. sum=2. A=5, B=1. delta=-4. I(6)=6. Sample: 6. Good.

All match.

Thus the solution is:
- Compute initial inversion count I0 for k=0 using BIT (Fenwick tree) on values in [0, M-1].
- For each v in [0, M-1], compute cnt[v] and sum_pos[v] (1-indexed).
- Compute A_v = cnt[v] * N - sum_pos[v] - cnt[v]*(cnt[v]-1)//2.
- Compute B_v = sum_pos[v] - cnt[v]*(cnt[v]+1)//2.
- Then for k from 0 to M-2:
    v = (M-1 - k) % M
    delta = B_v - A_v
    I_{k+1} = I_k + delta
- Store I_0, I_1, ..., I_{M-1}.
- Print them.

Complexities: O(N log M + M). Memory: O(N + M).

Edge cases: M=1. Then k only 0. The sequence B_i = A_i mod 1 = 0. Inversion count 0. Our algorithm: M=1, we compute I(0) via BIT (no inversions). Then loop for k=0 to M-2 = -1, so no loop. We output I(0)=0. Good.

If N=1, inversion count always 0. For each v, cnt[v] is 0 or 1. A_v and B_v formulas: if cnt=1, A_v = 1*1 - pos - 0 = 1 - pos. Since pos is 1 (1-indexed), A=0. B_v = pos - 1 = 0. So delta=0. So all I(k)=0. Good.

Now we need to implement BIT for initial inversion count. Since M up to 2e5, we can use BIT of size M. We process array A_i (0-indexed values). For each i from 0 to N-1 (or 1 to N), we query BIT for number of previous elements > A_i. That is, sum over (A_i+1 .. M-1) = total_sofar - query(A_i). Then update BIT at A_i by 1. Sum these counts.

Alternatively, we can compute using coordinate compression, but values are already in [0, M-1], so direct BIT of size M is fine.

Potential overflow: N up to 2e5, inversion count up to ~2e5*2e5/2 = 2e10, fits in 64-bit integer (Python int is arbitrary precision, fine). The delta calculations also fit.

Let's double-check formula for A_v and B_v with 1-indexed positions.

Let positions be 1-indexed: i=1..N.
For a fixed v, let indices where A_i = v be p_1 < p_2 < ... < p_c (c = cnt[v]).
A_v = # pairs (i<j) with i in S_v, j not in S_v.
For each p_t, number of non-v elements after p_t is (N - p_t) - (c - t). So sum_{t=1}^c (N - p_t - (c - t)) = c*N - sum p_t - sum_{t=1}^c (c - t). sum_{t=1}^c (c - t) = c*(c-1)/2. So A_v = c*N - sum_pos - c*(c-1)/2. Good.

B_v = # pairs (i<j) with i not in S_v, j in S_v.
For each p_t, number of non-v elements before p_t is (p_t - 1) - (t - 1) = p_t - t. Sum = sum p_t - sum_{t=1}^c t = sum_pos - c*(c+1)/2. Good.

Now, what about values that do not appear? cnt=0, sum_pos=0. Then A_v = 0, B_v = 0. Correct.

Now verify that the recurrence works for all k. We derived that moving from k to k+1, the set of wrapping indices is exactly those with B_i^{(k)} = M-1, which corresponds to A_i = (M-1 - k) mod M. So W_k = S_v where v = (M-1 - k) mod M. Then the change in inversion count is B_v - A_v. So the recurrence is exact.

We must be careful with modulo arithmetic: v = (M - 1 - k) % M. Since k from 0 to M-2, v will be M-1, M-2, ..., 1. At k=M-1, we don't need to compute next.

Implementation steps:

1. Read N, M.
2. Read array A (list of ints).
3. Compute I0:
   - Initialize BIT of size M (0-indexed or 1-indexed). Let's use 1-indexed BIT for simplicity: indices 1..M.
   - Map value x to index x+1.
   - For each i in range(N):
       x = A[i]
       # query number of previous elements > x: total_inserted - query(x+1) (since BIT query up to idx-1).
       # Or query sum from x+2 to M.
       # Let's use BIT: update at x+1 by 1. Then after update, the number of elements > x is i - query(x+1) (since query(x+1) gives count <= x). So inv += i - query(x+1).
   - Or we can query sum from x+2 to M: query(M) - query(x+1).
   - Both work. Let's do: inv0 = 0. For i in range(N): x = A[i]; inv0 += i - bit.query(x+1); bit.update(x+1, 1).
4. Compute cnt and sum_pos:
   - Initialize arrays cnt = [0]*M, sum_pos = [0]*M.
   - For i in range(N): v = A[i]; cnt[v] += 1; sum_pos[v] += (i+1) (since 1-indexed).
5. Compute A_v and B_v arrays (or compute on the fly):
   - For v in range(M):
       c = cnt[v]
       s = sum_pos[v]
       A_v = c * N - s - c*(c-1)//2
       B_v = s - c*(c+1)//2
6. Initialize ans = [0]*M.
   ans[0] = inv0.
7. cur = inv0.
   for k in range(0, M-1):
       v = (M - 1 - k) % M
       delta = B_v - A_v
       cur += delta
       ans[k+1] = cur
8. Print ans line by line.

Let's test with sample inputs mentally or by writing a quick mental check.

Sample 1: N=3, M=3, A=[2,1,0].
BIT: i=0, x=2, query(3)=0, inv+=0, update(3). i=1, x=1, query(2)=0, inv+=1, update(2). i=2, x=0, query(1)=0, inv+=2, update(1). Total inv=3. Good.
cnt: [1,1,1], sum_pos: [3,2,1].
A: v=0: c=1,s=3 -> A=3-3-0=0, B=3-1=2.
v=1: c=1,s=2 -> A=3-2=1, B=2-1=1.
v=2: c=1,s=1 -> A=3-1=2, B=1-1=0.
ans[0]=3.
k=0: v=(2-0)%3=2. delta=0-2=-2. cur=1. ans[1]=1.
k=1: v=(2-1)%3=1. delta=1-1=0. cur=1. ans[2]=1.
Matches.

Sample 2: Already checked.

Sample 3: Already checked.

Now check edge case: M large, N small. Works.

Potential issue: The formula for A_v and B_v relies on sum_pos being sum of 1-indexed positions. Let's verify with a more complex example to ensure no off-by-one.

Example: N=4, M=5, A = [1, 3, 1, 4].
Positions: 1:1, 2:3, 3:1, 4:4.
cnt[1]=2 (pos 1 and 3), sum_pos[1]=4.
cnt[3]=1 (pos 2), sum_pos[3]=2.
cnt[4]=1 (pos 4), sum_pos[4]=4.
Others 0.

Compute I0:
i=0, x=1: query(2)=0, inv+=0, update(2).
i=1, x=3: query(4)=0 (since only 1 inserted at 2), inv+=1, update(4).
i=2, x=1: query(2)=1 (the first 1), inv += 2 - 1 = 1, update(2).
i=3, x=4: query(5)=0 (inserted: 1,3,1; all <4), inv += 3 - 0 = 3, update(5).
Total inv = 0+1+1+3 = 5.

Now compute A and B for each v:
v=1: c=2, s=4.
A_1 = 2*4 - 4 - 1 = 8-4-1=3.
B_1 = 4 - 3 = 1.
Check manually: S_1 = {1,3}. Non-S = {2,4}.
Pairs (i<j) with i in S, j not: (1,2), (1,4), (3,4) => 3. Good.
Pairs (i<j) with i not, j in S: (2,3) => 1. Good.

v=3: c=1, s=2.
A_3 = 4 - 2 = 2.
B_3 = 2 - 1 = 1.
S_3={2}. Non={1,3,4}.
i in S, j not: (2,3),(2,4) => 2. Good.
i not, j in S: (1,2) => 1. Good.

v=4: c=1, s=4.
A_4 = 4 - 4 = 0.
B_4 = 4 - 1 = 3.
S_4={4}. Non={1,2,3}.
i in S, j not: none (4 is last) => 0. Good.
i not, j in S: (1,4),(2,4),(3,4) => 3. Good.

Now compute I(k) via recurrence:
I(0)=5.
k=0: v = (4-0)%5=4. delta = B_4 - A_4 = 3 - 0 = 3. I(1)=8.
k=1: v=3. delta = 1 - 2 = -1. I(2)=7.
k=2: v=2. cnt=0 => delta=0. I(3)=7.
k=3: v=1. delta = 1 - 3 = -2. I(4)=5.

Now let's compute I(1) manually: B = (A+1)%5 = [2,4,2,0].
Sequence: 2,4,2,0.
Inversions: (1,2):2<4 no; (1,3):2=2 no; (1,4):2>0 yes; (2,3):4>2 yes; (2,4):4>0 yes; (3,4):2>0 yes. Total 4. Wait our I(1)=8? That seems wrong. Let's compute carefully.

Original A: [1,3,1,4].
k=1: B_i = (A_i + 1) % 5 = [2,4,2,0].
Inversions: pairs i<j:
(1,2): B1=2, B2=4 => 2<4, not inv.
(1,3): 2 vs 2 => not inv (equal, not >).
(1,4): 2 vs 0 => 2>0, inv.
(2,3): 4 vs 2 => inv.
(2,4): 4 vs 0 => inv.
(3,4): 2 vs 0 => inv.
Total = 4.

But our recurrence gave 8. So something is wrong. Let's check the recurrence logic. The recurrence I(k+1) = I(k) + delta_k where delta_k = B_{v_k} - A_{v_k} and v_k = (M-1 - k) mod M. Did we compute v_k correctly? For M=5, k=0, v = (4-0) % 5 = 4. So W_0 = indices with B_i^{(0)} = 4. B^{(0)} = A = [1,3,1,4]. So indices with value 4: {4}. So w=1, non-w = {1,2,3}. Then A_4 = # pairs (i in W, j not in W, i<j). W={4}, so no such pair. So A_4=0. B_4 = # pairs (i not in W, j in W, i<j). i in {1,2,3}, j=4: 3 pairs. So delta = 3 - 0 = 3. I(1) = I(0) + 3 = 5 + 3 = 8. But actual I(1) is 4. So the recurrence is not correct? But we derived it earlier and it worked for samples. Let's re-examine the derivation.

We said: When moving from k to k+1, the only values that change are those that wrap from M-1 to 0. The set W_k = {i: B_i^{(k)} = M-1}. At k=0, W_0 = {i: A_i = 4}. That's correct. Then we claimed delta = B_{W_k} - A_{W_k}. But maybe the effect is different because when some elements wrap, they also affect inversions among themselves and with other wrapping elements? Wait, both wrap case: we said unchanged. That's correct because both become 0, equal, so no inversion among them. But what about the change in value of non-wrapping elements? They increase by 1. This changes their relative order with wrapping elements? Actually, the non-wrapping elements increase by 1, which might cause them to become larger than some other non-wrapping elements? No, they all increase by 1, so relative order among non-wrapping elements is preserved. However, the relative order between a non-wrapping element and a wrapping element changes: originally, wrapping element was M-1 (max), non-wrapping was something < M-1. After change, wrapping becomes 0 (min), non-wrapping becomes original+1 (which is >=1). So the wrapping element is now smaller than the non-wrapping element. So for each pair (i,j) with exactly one wrapping, the inversion status flips: if originally the wrapping element was i (so i was larger) and j was non-wrapping smaller, then it was an inversion; after change, i becomes smaller, so not an inversion. Conversely, if originally wrapping element was j (j was larger) and i was non-wrapping smaller, then it was not an inversion; after change, j becomes smaller, so i > j, becomes an inversion. So the net change in inversion count is: for each pair (i,j) with exactly one wrapping, the change is +1 if the wrapping index is the second (j), and -1 if the wrapping index is the first (i). So delta = (# pairs with wrapping index as second) - (# pairs with wrapping index as first). That is B - A, where A = # pairs (i in W, j not in W, i<j), B = # pairs (i not in W, j in W, i<j). So delta = B - A. That matches our earlier formula.

But why did it fail for this example? Let's compute A and B for W_0 = {4}. A = # pairs (i in W, j not, i<j) = 0. B = # pairs (i not, j in W, i<j) = 3. So delta = 3. I(0)=5, I(1)=8. But actual I(1)=4. So the model is missing something.

Wait, maybe the recurrence I(k+1) = I(k) + (B - A) is not correct because the change in B values also affects the relative order among non-wrapping elements? They all increase by 1, so relative order is preserved. So that shouldn't matter. What about pairs where both wrap? Both become 0, equal, so no inversion. Originally, both were M-1, equal, so no inversion. So unchanged. So the only changes are from the flipping of pairs with exactly one wrapping element. So the change should be exactly B - A. So why is I(0)=5, I(1)=4, a change of -1, not +3?

Let's compute the pairs with exactly one wrapping in W_0 = {4}. The pairs with exactly one wrapping are: (1,4), (2,4), (3,4). That's 3 pairs. For each such pair, the wrapping index is the second (j=4). So according to our model, each such pair changes from non-inversion to inversion (since originally j was larger, i smaller; after change, j becomes 0, i becomes something >=1, so i > j, becomes inversion). So each such pair should increase the inversion count by 1. So I(1) should be I(0) + 3 = 8. But actual I(1) is 4. Let's list the pairs and their status before and after:

Pair (1,4): i=1 (value 1), j=4 (value 4). Before: B1=1, B4=4 => 1<4, not inversion. After: B1=2, B4=0 => 2>0, inversion. So change: +1.
Pair (2,4): i=2 (value 3), j=4 (value 4). Before: 3<4, not inv. After: 4>0? Wait after: B2=4 (3+1), B4=0. 4>0, inv. Change: +1.
Pair (3,4): i=3 (value 1), j=4 (value 4). Before: 1<4, not inv. After: 2>0, inv. Change: +1.

So indeed, these three pairs become inversions. So I(1) should be I(0) + 3 = 8. But we computed I(1)=4 manually. Let's recompute I(1) carefully.

Original A: [1,3,1,4]
k=1: B = [2,4,2,0]
List all pairs:
(1,2): 2 vs 4 -> 2<4, not inv.
(1,3): 2 vs 2 -> equal, not inv.
(1,4): 2 vs 0 -> 2>0, inv.
(2,3): 4 vs 2 -> 4>2, inv.
(2,4): 4 vs 0 -> 4>0, inv.
(3,4): 2 vs 0 -> 2>0, inv.
Total inv = 4. So I(1)=4.

But we expected 8. Where is the discrepancy? Let's compute I(0) for the original array A = [1,3,1,4]:
Pairs:
(1,2): 1<3 not inv.
(1,3): 1=1 not inv.
(1,4): 1<4 not inv.
(2,3): 3>1 inv.
(2,4): 3<4 not inv.
(3,4): 1<4 not inv.
Total inv = 1. Wait, I computed I(0)=5 earlier. That's wrong! Let's recompute I(0) using BIT:
i=0, x=1: query up to 2? Actually BIT query(x+1) gives count <= x. So query(2) = 0. inv += 0 - 0 = 0. update(2).
i=1, x=3: query(4) = 0 (only 1 at index 2). inv += 1 - 0 = 1. update(4).
i=2, x=1: query(2) = 1 (the first 1). inv += 2 - 1 = 1. update(2).
i=3, x=4: query(5) = 3 (since we have inserted 1,3,1). So inv += 3 - 3 = 0. update(5).
Total inv = 0+1+1+0 = 2. Wait, 0+1+1+0 = 2. But manual count gave 1. Let's recount manual:
(1,2):1<3 no
(1,3):1=1 no
(1,4):1<4 no
(2,3):3>1 yes
(2,4):3<4 no
(3,4):1<4 no
Total 1. So BIT gave 2? Let's check BIT logic: At i=3 (value 4), we query number of previous elements > 4. Previous elements are [1,3,1]. All are <4, so count >4 is 0. So inv += 0. So total inv = 0 (i=0) + 1 (i=1) + 1 (i=2) + 0 (i=3) = 2. But manual says only 1. Where is the extra inversion? Pair (2,3): index 2 has value 3, index 3 has value 1. 3>1, yes inversion. That's one. Pair (1,3): 1>1? No. So only one. Why did BIT count 2? Let's re-evaluate i=2 (value 1). At that point, inserted elements are [1,3]. Number of previous elements > 1: previous elements are 1 and 3. Those >1: just 3. So count = 1. So inv += 1. That's the (2,3) inversion? Wait, i=2 is index 2 (value 3? No, array is 0-indexed: i=0:1, i=1:3, i=2:1, i=3:4). So at i=2 (value 1), previous elements are indices 0 and 1: values 1 and 3. Count >1: 3. So that's the pair (i=1, j=2) which is (3,1). That's one inversion. At i=1 (value 3), previous elements: index 0 value 1. Count >3: 0. So inv += 0. At i=0, inv += 0. So total = 1. But my BIT query for i=2 was query(2) which gives count <=1. Previous inserted: index 0:1, index 1:3. query(2) = 1 (the 1). So inv += i - query(2) = 2 - 1 = 1. That's correct. For i=1, query(4) = 1 (the 1). i=1, inv += 1 - 1 = 0. So total 0+0+1+0=1. Wait earlier I said query(4)=0 for i=1. That was wrong. Because at i=1, we have inserted index 0:1. query(4) should be 1. So inv += 1 - 1 = 0. So total inv = 1. Let's recompute step by step:

i=0: x=1. bit.query(2) = 0. inv += 0 - 0 = 0. update(2).
i=1: x=3. bit.query(4) = bit.sum up to 4. At this point, bit has 1 at index 2. So sum up to 4 = 1. inv += 1 - 1 = 0. update(4).
i=2: x=1. bit.query(2) = 1. inv += 2 - 1 = 1. update(2).
i=3: x=4. bit.query(5) = bit.sum up to 5. At this point, we have 1 at 2, 1 at 4, and 1 at 2 again? Wait we updated at 2 twice. So bit has two at index 2, one at index 4. Sum up to 5 = 3. inv += 3 - 3 = 0. update(5).
Total inv = 1. So I(0)=1. Not 5. My earlier BIT calculation was flawed because I used i - query(x+1) but miscalculated query values. So I(0)=1.

Now I(1) we computed manually as 4. So change from k=0 to k=1 is +3. That matches delta = 3. Great! So the recurrence holds. The earlier mistake was due to incorrect initial inversion count.

Thus the algorithm is correct.

Now we need to ensure that for all k, the recurrence holds. We derived that delta = B_v - A_v where v = (M-1 - k) mod M. So we can compute I(k) for all k by iterating.

Implementation details:

- Use Python lists for BIT. BIT of size M. Use 1-indexed indexing for BIT: size M+1.
- For each value x in A (0-indexed), we map to idx = x+1.
- BIT operations: update(i, delta): while i <= M: bit[i] += delta; i += i & -i.
- query(i): sum up to i: s=0; while i>0: s+=bit[i]; i -= i & -i; return s.
- Inversion count: inv = 0; for i in range(N): x = A[i]; idx = x+1; inv += i - query(idx); update(idx, 1).

Wait, query(idx) returns number of elements <= x inserted so far. Since we have inserted i elements before processing A[i] (if i is 0-indexed). So number of elements > x is i - query(idx). So inv += i - query(idx). That's correct.

Now compute cnt and sum_pos. We need 1-indexed positions. So for i in range(N): v = A[i]; cnt[v] += 1; sum_pos[v] += (i+1).

Then compute A_v and B_v for each v. We can store them in arrays A_arr and B_arr of size M.

A_arr[v] = cnt[v] * N - sum_pos[v] - cnt[v]*(cnt[v]-1)//2
B_arr[v] = sum_pos[v] - cnt[v]*(cnt[v]+1)//2

Now iterate k from 0 to M-2:
   v = (M - 1 - k) % M
   cur += B_arr[v] - A_arr[v]
   ans[k+1] = cur

But careful: The recurrence is I(k+1) = I(k) + (B_v - A_v). So we can maintain cur.

Now, what about k = M-1? We don't need to compute I(M) because we only need up to M-1. But we can compute it for completeness: v = (M-1 - (M-1)) % M = 0. delta = B_0 - A_0. I(M) would be I(0) of next cycle. But we don't output it.

Now check sample 2 with corrected understanding: I(0)=7, I(1)=3, etc. Already matches.

Now consider potential integer overflow in Python: not an issue.

Time complexity: O(N log M + M). N,M up to 2e5, log M ~ 18, so ~3.6 million operations, fine.

Now, is there any subtlety with values that appear multiple times? The formulas for A_v and B_v handle that correctly.

One more check: For v with cnt=0, A_v=0, B_v=0, delta=0. So I(k) remains unchanged for those k where v corresponds to a value not present in A. That makes sense: if no element equals M-1-k, then no element wraps, so all elements just increase by 1, preserving relative order. So inversion count unchanged.

Thus the algorithm is solid.

Now we need to write the solution in Python.

Implementation plan:

```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))