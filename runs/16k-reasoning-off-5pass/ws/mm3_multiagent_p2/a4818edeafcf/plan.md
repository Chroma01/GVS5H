We need to split the array A[1..N] into three non-empty contiguous subarrays at indices i < j, maximizing
S(i,j) = distinct(A[1..i]) + distinct(A[i+1..j]) + distinct(A[j+1..N]).
We can precompute the number of distinct values in any prefix efficiently using a right-to-left sweep that maintains, for each value, its last occurrence position. For each position k, let pref[k] = number of distinct values in A[1..k] and last_occ[v] = smallest index where v appears in A[1..k] (i.e., the latest position ≤ k where v is seen). We want to maximize pref[i] + (distinct in A[i+1..j]) + (pref[N] - pref[j]).
We iterate i from N-2 down to 1 (or N-1 down to 2). While expanding the middle segment to the left, we maintain its distinct count and a structure for the suffix. For each fixed left boundary i+1, we will consider all possible j ≥ i+1, but we need an O(N) overall solution.
Standard trick: we iterate i from 1 to N-2. For each i, we know the prefix distinct count pref[i]. Then we sweep j from i+1 to N-1, but we need to be efficient. Better approach: iterate i from N-1 down to 1 and simultaneously maintain a data structure for the middle segment. Actually, we can fix the middle segment boundaries and use the fact that values are bounded by N (1 ≤ A_i ≤ N). Use an array of last occurrence for values in the middle segment.
A known solution for this problem (AtCoder ABC 330 F? No, ABC 365 F? Actually it's similar to "Distinct Trio" or ABC 363 F? It's "Three Subarrays" from ABC 395 F? No, it's from a recent contest. The problem is "Distinct Subarrays" or "Three Subarrays" - likely from AtCoder). The solution: iterate the middle segment's left endpoint l from N-1 down to 2, maintaining a set of values in the middle segment and the count of distinct values in the middle. For each l, we also need to consider the right endpoint r. We can precompute for each r (or for each position, the best suffix distinct count). Wait, we can precompute suf[k] = number of distinct in A[k..N]. Then the answer for a split (i,j) is pref[i] + distinct in A[i+1..j] + suf[j+1]. So we need to maximize pref[i] + mid_distinct(i+1, j) + suf[j+1]. We can iterate the middle segment's left boundary l = i+1 from 1 to N-2, and maintain the middle segment as we expand r. But we also need to update the best for each l.
Actually, a standard O(N) solution: We process from right to left. We maintain an array best_suffix[k] which stores the maximum value of suf[r] - (something)? Not exactly.
Alternative: For each position p, we can precompute the number of distinct in suffix starting at p: suf[p]. But we need to consider all pairs (l, r) with l < r. This is a 2D problem but can be done in O(N) using the "last occurrence" technique similar to "max subarray sum with distinct elements" but here it's about distinct counts.
Wait, distinct count of a segment [l, r] can be computed if we know for each value its last occurrence. For a fixed l, as r increases, the distinct count increases by 1 only when A[r] has not been seen in the current middle segment. So if we fix l and sweep r, the middle distinct count is monotonic non-decreasing, and we can update it by checking if A[r] is already in the set. This is O(N) per l if we clear the set, but we can reuse by processing l from right to left. When we decrease l by 1, we need to add A[l] to the set, and we need to know the distinct count for all r ≥ l. We can maintain an array cur_distinct_for_each_r? No, that's too big.
Better: Iterate l from N-1 down to 2. For each l, we maintain an array mid[r] = number of distinct values in A[l..r] for r ≥ l. As we decrease l, we add A[l] to the set, and for all r ≥ l, the distinct count either stays the same or increases by 1 if A[l] was not already in A[l+1..r]. This is similar to the classic problem of maximizing prefix distinct + something.
But we need to combine with pref[l-1] and suf[r+1]. So we want max over l ≤ r of pref[l-1] + mid_distinct(l, r) + suf[r+1].
This looks like we can iterate r from 1 to N-1 (the end of middle segment) and maintain something over l.
Let's think of the classic O(N) solution for two subarrays (Problem C). For two subarrays, we split into left and right, maximizing distinct(left) + distinct(right). We can precompute pref_distinct[i] and suf_distinct[i], and for each i, answer is max_i pref_distinct[i] + suf_distinct[i+1]. Actually for two subarrays, it's exactly that: left = [1..i], right = [i+1..N]. So answer is max_i pref[i] + suf[i+1]. That's trivial.
For three subarrays, it's more complex because the middle segment can vary. But the trick is: for a fixed right boundary j of the middle segment, we want to choose the best left boundary i (i < j) to maximize pref[i] + distinct(A[i+1..j]). So for each j, we need to compute max_{i < j} pref[i] + distinct(A[i+1..j]). Then the total answer is max_j (that max) + suf[j+1].
So the problem reduces to: For each j from 2 to N-1, compute M[j] = max_{i < j} pref[i] + distinct(A[i+1..j]). Then answer = max_{j=2}^{N-1} (M[j] + suf[j+1]).
Now, how to compute M[j] efficiently? We process j from 1 to N (or 2 to N-1). We need to maintain a data structure over i (i < j) that can answer queries of the form: given j, find max over i < j of pref[i] + distinct(A[i+1..j]).
Note that distinct(A[i+1..j]) is the number of distinct values in the subarray from i+1 to j. As j increases, this count for a fixed i changes: it increases by 1 if A[j] is not in A[i+1..j-1]. So for a fixed i, the function f_i(j) = pref[i] + distinct(A[i+1..j]) is piecewise constant, increasing only when a new distinct value appears in the suffix of the middle segment.
We can process j from 1 to N. We maintain for each i a "value" which is pref[i] + distinct(A[i+1..j]). As j increases, we need to update all i such that A[j] is not in A[i+1..j-1]. But we don't want to update all i. Instead, we can think in reverse: for each value v, we can determine for which i the addition of v to the segment [i+1..j] is new.
Actually, there's a known solution: We iterate j from 1 to N. For each j, we want to compute the maximum over i < j of pref[i] + distinct(A[i+1..j]). Let's define an array best[i] initially pref[i]. But distinct(A[i+1..j]) is not simply dependent on j alone; it depends on the history.
Another approach: We can fix the left boundary i and sweep j. But we already considered that.
Let's recall the solution for AtCoder ABC 395 F? No, it's "Three Subarrays" from ABC 395? Actually, the problem is "Distinct Subarrays" or similar. I think the problem is from a recent contest. The solution is O(N) using the "last occurrence" technique but in a clever way.
Wait, the problem is exactly: Given array A of length N up to 3e5, split into three contiguous non-empty parts. Maximize sum of distinct counts.
This is known as "Three Distinct Subarrays" or "Distinct Trio" from AtCoder? Actually, it's from AtCoder Beginner Contest 395 F? No, ABC 395 F is something else. It's from ABC 365 F? No, it's "Distinct Subarrays III"? The problem statement mentions "harder version of Problem C". So it's likely from AtCoder. Problem C was "Two Subarrays" (distinct count sum for two subarrays). This is "Three Subarrays". The solution for three subarrays is to use a sweep and a "max suffix" array.
Let me think: We can compute for each position k, the distinct count in the suffix starting at k: suf[k]. But we need to split into three. Actually, we can precompute for each position p, the distinct count of the prefix: pref[p]. And for each position p, the distinct count of the suffix: suf[p].
Now, for the middle segment, we can think of it as: we choose left boundary L and right boundary R. Then total = pref[L] + distinct(A[L+1..R]) + suf[R+1]. (Note: pref[L] is distinct in A[1..L], and suf[R+1] is distinct in A[R+1..N]).
We want to maximize this over 1 ≤ L < R ≤ N-1.
We can iterate L from 1 to N-2. For each L, we need to find the best R > L to maximize pref[L] + distinct(A[L+1..R]) + suf[R+1]. This is equivalent to: for each L, we need to find max_{R > L} (distinct(A[L+1..R]) + suf[R+1]). Then add pref[L].
So for each L, we can compute B[L] = max_{R > L} (distinct(A[L+1..R]) + suf[R+1]). Then answer = max_{L=1}^{N-2} (pref[L] + B[L]).
Now, how to compute B[L] efficiently? We process L from N-1 down to 1. As we decrease L, the middle segment's left boundary moves left. We need to maintain for each possible R (R > L) the value of distinct(A[L+1..R]) + suf[R+1]. As L decreases, the distinct count for a fixed R may increase by 1 if A[L+1] was not already in A[L+2..R]. So we can maintain an array val[R] = distinct(A[L+1..R]) + suf[R+1] for all R > L. Initially, when L = N-1, the middle segment is just A[N-1..N-1]? Wait, L can go up to N-2 because we need at least one element in the suffix. Let's set L from N-1 down to 1, but we only care about L ≤ N-2. Actually, let's set L from N-1 down to 1, and maintain val[R] for R > L. When L decreases by 1, the new middle segment is A[L+1..R] for R > L. The old middle segment was A[L+2..R] for R > L+1. So for R = L+1, the new distinct count is 1 (just A[L+1]). For R > L+1, the new distinct count is old distinct count + (1 if A[L+1] not in A[L+2..R] else 0). So we need to efficiently update val[R] for all R > L where A[L+1] is not already present in the current middle segment.
This is exactly the same as the classic problem of maintaining an array of values and updating a suffix when a new element is added to the left. We can do this by keeping track of the last occurrence of each value in the middle segment. But we are iterating R as an index, and the middle segment changes.
Actually, we can think of it this way: For each value v, we want to know the range of R for which adding A[L+1] = v to the left of the current segment increases the distinct count. Specifically, if v is currently in the segment A[L+2..R] for some R, then for those R, adding v to the left does not increase the distinct count. If v is not in the segment, it does. So the condition is: v is in A[L+2..R] iff there exists some occurrence of v in A[L+2..R]. The rightmost occurrence of v in A[1..L+1] is at some position pos. If pos ≤ L, then v is not in A[L+1..R]? Wait, the new element is A[L+1]. We need to check if v = A[L+1] is already present in A[L+2..R]. That is, we need to know the last occurrence of v in A[1..R] before L+1? Actually, as we process L from right to left, we are adding A[L+1] to the left. We need to know, for a given v, what is the rightmost occurrence of v in the current middle segment. The current middle segment is A[L+1..R]. When we add A[L+1] (which is v), the distinct count for a given R increases by 1 if and only if v does not appear in A[L+2..R]. That is, the next occurrence of v after L+1 is > R, or there is no occurrence. More precisely, if we look at the original array, the next occurrence of v after index L+1 is at index nxt[L+1] (the smallest index > L+1 where A[index] = v). If nxt[L+1] > R, then v is not in A[L+2..R], so adding v increases the distinct count. If nxt[L+1] ≤ R, then v is already there, so no increase.
Therefore, for a fixed L, the increase happens for all R such that L+1 < R < nxt[L+1]. For R ≥ nxt[L+1], there is no increase because v is already in the segment (at nxt[L+1]).
So when we decrease L (i.e., we set new L = old L - 1, so the new added element is at index new_L+1 = old_L), the new element is v = A[old_L]. We need to add 1 to val[R] for all R in [old_L+1, nxt[old_L]-1]. For R ≥ nxt[old_L], no addition.
But val[R] is defined for R > L. Initially, when L = N-1, the middle segment is just A[N-1..N-1]? Actually, if L = N-2, the middle segment is A[N-1..R] for R ≥ N-1. The minimal middle segment is length 1. So we can initialize when L = N-2: the middle segment is A[N-1..R] for R ≥ N-1. The distinct count for A[N-1..R] is 1 if R = N-1, and for R > N-1, we need to consider. But N can be up to 3e5, we can't update all R naively. However, the range of R that gets an increment is a contiguous interval [L+2, nxt[L+1]-1]. This is a range update! We can use a difference array or a segment tree to support range add and range max query. Specifically, we need to maintain an array val[R] for R from L+1 to N-1 (since R is the right boundary, max R is N-1). As we decrease L, we add a value to a range of R. We also need to query the maximum of val[R] over all valid R (R > L). But wait, we need B[L] = max_{R > L} (distinct(A[L+1..R]) + suf[R+1]). We can precompute suf[R+1] as a constant. So initially, for L = N-2, we can compute val[R] = distinct(A[N-1..R]) + suf[R+1] for R = N-1. But we need to consider all R. Actually, as we decrease L, we are adding the new element to the left. We can maintain an array add[R] which is the additional distinct count from the left expansions. Initially, when L = N-2, the middle segment starts at L+1 = N-1. The distinct count of A[N-1..R] is 1 for R = N-1, and for R > N-1, we need to compute it. But if we process L from N-2 down to 1, we can maintain a difference array diff[R] such that the actual distinct count for segment [L+1..R] is base[R] + diff[R], where base[R] is something? Not exactly.
Let's think differently. We can precompute for each R, the distinct count of A[1..R], but that's prefix. We need the distinct count of the middle segment.
There is a known solution for the "Three Subarrays" problem that uses the following:
1. Compute pref[i] = distinct count in A[1..i].
2. Compute suf[i] = distinct count in A[i..N].
3. For the middle segment, we can compute for each i, the maximum of distinct(A[i..j]) + suf[j+1] over j ≥ i. Let's define F[i] = max_{j ≥ i} (distinct(A[i..j]) + suf[j+1]). Then the answer is max_{i=1}^{N-2} (pref[i] + F[i+1])? Wait, careful: if middle segment is from L+1 to R, then left is 1..L, middle is L+1..R, right is R+1..N. So total = pref[L] + distinct(A[L+1..R]) + suf[R+1]. We want max over L < R. So for each L, we want max_{R > L} (distinct(A[L+1..R]) + suf[R+1]). This is exactly: for each starting index s = L+1, we want max_{R ≥ s} (distinct(A[s..R]) + suf[R+1]). Let's call G[s] = max_{R ≥ s} (distinct(A[s..R]) + suf[R+1]). Then answer = max_{s=2}^{N-1} (pref[s-1] + G[s]).
So we need to compute G[s] for all s. Then we can compute the answer by taking max over s.
Now, how to compute G[s] efficiently? We can process s from N down to 1. For a fixed s, we need the maximum over R ≥ s of (distinct(A[s..R]) + suf[R+1]). We can maintain an array val[R] = distinct(A[s..R]) + suf[R+1] for R ≥ s. As s decreases, the segment A[s..R] gains a new element on the left. The distinct count for a fixed R either stays the same or increases by 1, depending on whether A[s] is already in A[s+1..R]. This is exactly the same situation as before. So we can process s from N down to 1, maintaining a segment tree or a difference array with range max.
Specifically, we can precompute suf[R+1] for all R. Let's define an array base[R] = suf[R+1] for R = 1..N-1. For s = N, the middle segment is just A[N..N], so R must be N. distinct = 1, so G[N] = 1 + suf[N+1] (but suf[N+1] is 0). Actually, we need to handle boundaries carefully. For s = N, the middle segment can only be A[N..N] (since R ≥ s and R ≤ N-1 for the right to be non-empty? Wait, if s = N, then the right segment would be A[N+1..N] which is empty. So s must be at most N-1. So we only care about s from 1 to N-1. But also the left segment must be non-empty, so s ≥ 2. So we compute G[s] for s=2..N-1.
Let's set s from N-1 down to 2. For s = N-1, the middle segment is A[N-1..R] for R = N-1 only. So G[N-1] = distinct(A[N-1..N-1]) + suf[N] = 1 + suf[N]. suf[N] is distinct count in A[N..N] = 1. So G[N-1] = 2.
Now, for s = N-2, the middle segment is A[N-2..R] for R = N-2 or N-1. We need to compute distinct(A[N-2..N-2]) + suf[N-1] and distinct(A[N-2..N-1]) + suf[N]. We can get these by updating the previous values. In general, we can maintain an array cur[R] for R ≥ s representing distinct(A[s..R]) + suf[R+1]. Initially, for s = N-1, cur[N-1] = 1 + suf[N]. For R > N-1, they don't exist. When we decrease s to s-1, we need to compute cur[R] for R ≥ s-1. The new element is A[s-1]. The distinct count for segment A[s-1..R] is:
- If R = s-1, it's 1.
- If R ≥ s, it's old distinct count for A[s..R] plus 1 if A[s-1] is not in A[s..R], else same.
So for R ≥ s, the new value is (old distinct count + (1 if A[s-1] not in A[s..R])) + suf[R+1].
We can maintain a difference array to apply these increments. We need to know for which R the increment happens. The increment happens if A[s-1] is not in A[s..R]. This is equivalent to: the next occurrence of value v = A[s-1] after index s-1 is at position p = nxt[s-1] (the first index > s-1 where A[index] = v). Then for R < p, v is not in A[s..R] (since the segment A[s..R] is within s..p-1), so increment. For R ≥ p, v is in A[s..R] (at p), so no increment.
Therefore, when we move from s to s-1, we need to add 1 to cur[R] for all R in [s-1, nxt[s-1]-1] (note: R can be s-1, which gets the base value 1 + suf[s]? Wait, for R = s-1, the distinct count is 1, and we add suf[s]. So cur[s-1] = 1 + suf[s]. For R ≥ s, we update based on the old cur[R]. But careful: when we decrease s, the array indices for R shift: old R corresponds to new R-1? Actually, we can keep the array indexed by the original R. Let's define an array add[R] that accumulates the increments. Initially, when s = N, we might not have any. Let's set s = N-1 down to 1. For each s, we want to compute the maximum over R ≥ s of (distinct(A[s..R]) + suf[R+1]). We can maintain a segment tree or a Fenwick tree that stores the value for each R. But we need to support range add and point query? Actually, we need to query the maximum over R ≥ s. So we can use a segment tree that supports range add and range max query.
Alternatively, we can use a difference array and a prefix maximum? Because the updates are "add 1 to a prefix of R's", we can maintain an array val[R] that is the sum of all increments for that R. Then the total value for a given s and R is: if R = s, it's 1 + suf[s+1]? Wait, for R = s, the segment is A[s..s], distinct = 1, plus suf[s+1]. For R > s, the distinct count is the number of distinct values in A[s..R]. We can precompute an array distinct_from_s_to_R? Not directly.
But we can precompute for each R, the number of distinct values in A[1..R], but that's not what we need.
Let's think of another angle: We can compute G[s] by iterating R from s to N-1 and maintaining a set of values in the middle segment. But that's O(N^2) in the worst case.
Wait, the standard solution for this problem is O(N) and uses the following trick:
We compute pref[i] and suf[i] as distinct counts.
Then we compute an array left_best[i] = pref[i] + max_{j > i} (distinct(A[i+1..j]) - something)? Not exactly.
Actually, the known solution for the "Three Subarrays" problem (from AtCoder ABC 395 F? No, I recall a problem "Three Subarrays" where we split into three parts and maximize sum of distinct counts. The solution is:
1. Compute pref[i] for i=1..N.
2. Compute suf[i] for i=1..N.
3. For the middle segment, we can compute an array mid[i] = distinct count in A[i..j] for some j? No.
Let me search my memory: There is a problem called "Three Subarrays" from AtCoder Regular Contest 109? No, it's from AtCoder Beginner Contest 297? Not sure.
Actually, the problem is "Distinct Trio" or "Three Subarrays" from Codeforces? No, the constraints and style are AtCoder. The problem is "Three Subarrays" from AtCoder Beginner Contest 365? Let me think: ABC 365 F is "Lamp and Color"? No.
Wait, the problem statement says "This problem is a harder version of Problem C." So it's likely from a contest where Problem C was the two-subarray version. For example, in AtCoder Beginner Contest 395, Problem C was "Sick? No." Actually, ABC 395 had a problem "Three Subarrays" as F? No.
Let's derive the solution ourselves.
We need to compute for each s from 2 to N-1: G[s] = max_{R=s}^{N-1} (distinct(A[s..R]) + suf[R+1]).
Notice that suf[R+1] is a known value. Let's denote C[R] = suf[R+1] for R=1..N-1. C[N] = suf[N+1] = 0.
So G[s] = max_{R=s}^{N-1} (distinct(A[s..R]) + C[R]).
Now, distinct(A[s..R]) is the number of distinct values in the subarray. This is equivalent to: if we know for each value its first occurrence in the subarray, etc. But we can also think of it as: distinct(A[s..R]) = number of values v such that the first occurrence of v in A[s..N] is ≤ R. This is not directly helpful.
Alternatively, we can process s from N-1 down to 1 and maintain a data structure of the suffix. As we decrease s, we are adding A[s] to the left of the segment. The distinct count for a fixed R increases by 1 if A[s] is not already in A[s+1..R]. This is exactly the condition that the next occurrence of A[s] after s is > R. So for a given s, the increment happens for R in [s, nxt[s]-1]. Here nxt[s] is the next index after s where the value A[s] appears. If there is no next occurrence, nxt[s] = N+1, so the range is [s, N].
So we can maintain an array add[R] which is the number of times we have added 1 to R's distinct count. Initially, for s = N, the distinct count for R = N is 1. But we only care about s up to N-1. Let's set up the array for R = 1..N-1. We want to compute for each s, the maximum over R ≥ s of (base_distinct[s..R] + C[R]), where base_distinct[s..R] is the distinct count. We can build this by starting with s = N-1, where base_distinct[N-1..R] is 1 for R = N-1, and 0 for R < N-1? Actually, for s = N-1, the segment is only R = N-1, distinct = 1. For R > N-1, we don't consider because the right segment would be empty. So for s = N-1, the only R is N-1. So G[N-1] = 1 + C[N-1] = 1 + suf[N].
Now, to get G[N-2], we need to consider R = N-2 and R = N-1. We can compute these by taking the values for s = N-1 and updating. When we move from s = N-1 to s = N-2, the new element is A[N-2]. The distinct count for R = N-2 becomes 1. For R = N-1, it was 1 (from s=N-1), and now it becomes 1 + (1 if A[N-2] is not in A[N-1..N-1] else 0). The condition is whether A[N-2] equals A[N-1]. So the update is: for R = N-1, if A[N-2] != A[N-1], add 1; else add 0. In general, for a new s, the update is: for R in [s, nxt[s]-1], add 1. Here nxt[s] is the first index > s where A[index] = A[s].
So we can maintain an array diff[R] for R = 1..N-1, initialized to 0. We also need the base value for R = s when we first introduce it. For R = s, the distinct count is 1, so we can think of it as: we have a base array base[R] = 0, but we need to add 1 when R = s. Actually, we can maintain an array val[R] = distinct(A[s..R]) + C[R]. Initially, for s = N-1, val[N-1] = 1 + C[N-1]. For other R, they are not yet defined. As we decrease s, we need to compute val[s] = 1 + C[s]. And for R > s, we update val[R] by adding 1 if A[s] is not in A[s+1..R], i.e., if R < nxt[s]. So we can do: for each s from N-1 down to 2:
   - Set val[s] = 1 + C[s] + (any previous updates that apply to R=s). But we can just initialize val[s] = 1 + C[s] and then apply the range add for the current s? Wait, the range add for a given s is: for R in [s, nxt[s]-1], we add 1. This should be applied to all future s' < s. So if we process s from N-1 down to 2, we can maintain an array val[R] that represents the current value for the current s. But the range add for a given s should affect val[R] for R ≥ s. However, when we move to the next s (s-1), the range for the new s is [s-1, nxt[s-1]-1]. So we need to add 1 to val[R] for R in that range. We can do this by maintaining a difference array add[R] that stores how many times we have added 1 to val[R] due to all processed s' > current s. But careful: when we are at s, the val[R] for R ≥ s should already include the contributions from s+1, s+2, ..., N-1. So we can maintain an array inc[R] that is the total increment from all s' > current s. Then val[R] = base[R] + inc[R], where base[R] is the distinct count from the initial segment? Actually, the distinct count for A[s..R] is exactly the number of s' in [s, R] such that A[s'] is not in A[s'+1..R]? No.
Let's define it properly: For a fixed s, the distinct count of A[s..R] is equal to 1 (for the element at s) plus the number of indices t in [s+1, R] such that A[t] is not in A[s..t-1]. This is not easy to compute incrementally.
But we have the condition: for a fixed s, the distinct count for A[s..R] is 1 for R = s. For R > s, it is the same as the distinct count for A[s+1..R] plus 1 if A[s] is not in A[s+1..R]. So if we know the distinct count for A[s+1..R] (which we do from the previous step), we can compute it for A[s..R] by adding 1 if A[s] not in A[s+1..R]. This is exactly the range update: for R in [s, nxt[s]-1], we add 1 to the distinct count. And note that the distinct count for A[s+1..R] was already computed. So if we maintain an array d[R] = distinct(A[s..R]) for the current s, we can update it to s-1 by:
   - For R = s-1: d[s-1] = 1.
   - For R ≥ s: d_new[R] = d_old[R] + 1 if R < nxt[s-1] else d_old[R].
This is a range add to d[R] for R in [s-1, nxt[s-1]-1]. But we also need to add C[R] to get the total value. So we can maintain an array total[R] = d[R] + C[R]. Initially, for s = N-1, total[N-1] = 1 + C[N-1]. For s = N-2, we need to set total[N-2] = 1 + C[N-2], and for R = N-1, total[N-1] = (1 + C[N-1]) + (1 if N-1 < nxt[N-2] else 0). This matches the range add.
So we can process s from N-1 down to 1. We maintain an array total[R] for R ≥ s. We need to support:
   - When we decrease s to s-1, we need to:
        a) Initialize total[s-1] = 1 + C[s-1].
        b) Add 1 to total[R] for R in [s-1, nxt[s-1]-1] (for R ≥ s, this is the range [s-1, min(nxt[s-1]-1, N-1)]; note that R max is N-1).
   - Then G[s-1] = max_{R ≥ s-1} total[R].
We can implement this with a segment tree that supports range add and range max query. The array indices are 1..N-1. We start with s = N-1. total[N-1] = 1 + C[N-1]. We set this in the segment tree. Then G[N-1] = that value.
Then for s from N-2 down to 1:
   - We add a new element at index s: we need to set total[s] = 1 + C[s]. But we also need to add 1 to the range [s, nxt[s]-1]? Wait, careful: when we move from s+1 to s, the new element is A[s]. The range of R that gets an increment is [s, nxt[s]-1]. But we also need to set the value for R = s. For R = s, the distinct count is 1, so total[s] should be 1 + C[s]. The range add for R in [s, nxt[s]-1] would also add 1 to R = s, but the distinct count for R = s is 1, not 1 + something. So the range add should be for R in [s+1, nxt[s]-1]? Let's check: For R = s, the segment is A[s..s], distinct = 1. For R = s+1, the segment is A[s..s+1], distinct = 1 if A[s+1] = A[s], else 2. So the increment for R = s+1 is 1 if A[s+1] != A[s], i.e., if s+1 < nxt[s]. So the range that gets an increment is [s+1, nxt[s]-1]. For R = s, we just set it to 1 + C[s]. So the update for decreasing s to s-1 is:
   - For R = s-1: set total[s-1] = 1 + C[s-1].
   - For R in [s, nxt[s-1]-1] (i.e., from s to nxt[s-1]-1), add 1 to total[R].
But note: when we are at s (having processed s+1..N-1), the array total[R] for R ≥ s already includes the contributions from the previous elements. The new element A[s] adds 1 to distinct count for R such that R < nxt[s]. So for R in [s, nxt[s]-1], we add 1. However, for R = s, the distinct count is 1, and the old total[s] (if it existed) would be from the segment starting at s+1? Actually, when s decreases, the segment now starts at s. The old total[s] corresponded to segment starting at s+1 with R = s? But R must be ≥ the start index. So old total[s] (when start was s+1) was defined for R ≥ s+1. So total[s] was not defined before. So we don't have an old value at index s. We just set it to 1 + C[s]. Then for R > s, we add 1 if R < nxt[s]. So the range add is [s+1, nxt[s]-1] (if nxt[s] > s+1). Also, we need to set the value at s. So the operations for a new s are:
   - Set the value at index s to 1 + C[s].
   - Add 1 to the range [s+1, nxt[s]-1] (if s+1 ≤ nxt[s]-1).
Then G[s] = maximum over indices ≥ s.
This can be done with a segment tree that supports point assignment (or we can just initialize the array and then do range add). But we are processing s from N-1 down to 1, and we need to query the maximum over a suffix [s, N-1] at each step. This is exactly a segment tree with range add and range max query. We can build the segment tree initially with all zeros, and then for s = N-1, we set leaf N-1 to 1 + C[N-1] (or we can just add it). Actually, we can process s = N down to 1, but we need to handle the initial state.
Let's outline the algorithm:
1. Read N and array A[1..N].
2. Compute pref[i] = distinct count in A[1..i] for i=1..N.
3. Compute suf[i] = distinct count in A[i..N] for i=1..N.
4. Compute C[i] = suf[i+1] for i=1..N-1. (C[N] = 0, but we don't need it).
5. Compute nxt[i] for i=1..N: the smallest index > i such that A[nxt[i]] = A[i], or N+1 if no such index.
6. Initialize a segment tree over indices 1..N-1. Each leaf stores a value. We will support range add and range max.
7. Process s from N-1 down to 1:
   - We need to set the value at index s to 1 + C[s]. But we also need to consider that this value might have been affected by previous range adds. However, when we are at s, the segment tree currently represents the state after processing s+1..N-1. The indices in the tree correspond to R. For R < s, they are not yet valid (since the middle segment must start at most at s, but R must be ≥ s). So we can just set the value at index s to 1 + C[s] (this overwrites any previous value, but since we are processing from right to left, the previous value at s was for a different starting index, but actually the array total[R] for a given R depends on the starting index. We are recomputing total[R] for each new s. So we need to reset the tree for each s? No, we are updating it incrementally. But the value at index R for a new s is not simply a function of the old value at R plus something. Let's check:
     For s = N-1: total[N-1] = 1 + C[N-1].
     For s = N-2: total[N-2] = 1 + C[N-2]. total[N-1] = (1 + C[N-1]) + (1 if N-1 < nxt[N-2] else 0).
     So the new total[N-1] is the old total[N-1] + 1 (if condition). So it is an update. But total[N-2] is a new value. So we can:
        - Set leaf s to 1 + C[s].
        - Add 1 to range [s+1, nxt[s]-1] (if s+1 ≤ min(nxt[s]-1, N-1)).
   - Then G[s] = max_{R ≥ s} total[R]. This is the maximum value in the segment tree over the range [s, N-1].
8. After we have G[s] for all s, we compute the answer as max_{s=2}^{N-1} (pref[s-1] + G[s]). (Note: s is the start of the middle segment, so left segment is 1..s-1, right segment is R+1..N. We take max over s from 2 to N-1 because left must be non-empty and right must be non-empty, so s ≤ N-1. Also s ≥ 2 because left must be non-empty, so s-1 ≥ 1, i.e., s ≥ 2.)
9. Print the answer.

Let's verify with a small example.
Example 1: N=5, A = [3,1,4,1,5]
Compute pref: 
i=1: {3} -> 1
i=2: {3,1} -> 2
i=3: {3,1,4} -> 3
i=4: {3,1,4} -> 3
i=5: {3,1,4,5} -> 4
Compute suf:
i=5: {5} -> 1
i=4: {1,5} -> 2
i=3: {4,1,5} -> 3
i=2: {1,4,5} -> 3 (since A2=1, A3=4, A4=1, A5=5 -> distinct 1,4,5 = 3)
i=1: {3,1,4,5} -> 4
C[i] = suf[i+1]:
C[1] = suf[2] = 3
C[2] = suf[3] = 3
C[3] = suf[4] = 2
C[4] = suf[5] = 1
nxt[i]:
A[1]=3, next 3: none -> N+1=6
A[2]=1, next 1: at 4 -> 4
A[3]=4, next 4: none -> 6
A[4]=1, next 1: none -> 6
A[5]=5, next 5: none -> 6
Now process s from 4 down to 1.
Segment tree indices 1..4.
Initially, empty (all 0). But we will set values as we go.
s=4: (N-1=4)
   Set index 4 to 1 + C[4] = 1+1=2.
   Add 1 to range [5, nxt[4]-1] = [5, 5] (but index 5 is out of range, so no add).
   G[4] = max over [4,4] = 2.
s=3:
   Set index 3 to 1 + C[3] = 1+2=3.
   Add 1 to range [4, nxt[3]-1] = [4, 5] -> only index 4 gets add. So index 4 becomes 2+1=3.
   G[3] = max over [3,4] = max(3,3)=3.
s=2:
   Set index 2 to 1 + C[2] = 1+3=4.
   Add 1 to range [3, nxt[2]-1] = [3, 3] -> index 3 becomes 3+1=4.
   G[2] = max over [2,4] = max(4,4,3)=4.
s=1:
   Set index 1 to 1 + C[1] = 1+3=4.
   Add 1 to range [2, nxt[1]-1] = [2, 5] -> indices 2,3,4 get add. So:
        index 1: 4
        index 2: 4+1=5
        index 3: 4+1=5
        index 4: 3+1=4
   G[1] = max over [1,4] = 5.
Now answer = max_{s=2}^{4} (pref[s-1] + G[s]).
s=2: pref[1] + G[2] = 1 + 4 = 5.
s=3: pref[2] + G[3] = 2 + 3 = 5.
s=4: pref[3] + G[4] = 3 + 2 = 5.
Max = 5. Correct.

Example 2: N=10, A = [2,5,6,4,4,1,1,3,1,4]
Let's compute quickly to verify.
We can trust the logic.

Time complexity: O(N log N) due to segment tree. N=3e5, log N ~ 19, so it's fine.
Space: O(N).

We need to implement the segment tree. Since we only need range add and range max, we can use a lazy propagation segment tree.
Alternatively, we can use a Fenwick tree (BIT) for range add and a segment tree for range max? But range add and range max is not directly supported by BIT. We can use a segment tree.
Since N=3e5, a segment tree with size 4N is fine.

Let's code the segment tree.
We need:
- build with size N-1.
- support range_add(l, r, val) for l <= r.
- support range_max(l, r) for l <= r.
We will also need to set a point to a specific value. But we can do point assignment by updating a range of length 1? Or we can have a set operation. Since we are processing from right to left, we can just initialize the tree with all zeros, and when we set index s, we can do a point update to set it to the value. But we need to be careful: the point update should override any previous value. However, since we are processing s in decreasing order, the index s has not been touched before (because we only update indices ≥ current s+1? Actually, when we set index s, it was not set in previous iterations because we only set indices s, s-1, etc. So it's fresh. But we also do range adds that might cover index s? In the current step, we set index s first, then we do range add starting from s+1. So index s is not affected by the range add. So we can just do a point set. But to be safe, we can do: point_set(s, 1 + C[s]) and then range_add(s+1, nxt[s]-1, 1). However, if the segment tree initially has zeros, and we do point_set, it overwrites the zero. That's fine.
But wait: what if nxt[s]-1 >= s? The range add starts at s+1, so index s is not included. So point_set(s) is correct.
But we also need to ensure that we don't accidentally carry over values from previous s? No, because we are maintaining the state for the current s. The state for s is built from the state for s+1 by: setting index s, and adding 1 to a range. So the segment tree always reflects the total values for the current s. We then query the max over [s, N-1]. This works.

Let's code it.

Implementation steps:
1. Read N, array A (1-indexed).
2. Compute pref[1..N]:
   last = dict or array of size N+1 (since A_i ≤ N). Initialize with 0.
   distinct = 0
   for i in 1..N:
       if last[A[i]] == 0: distinct += 1
       last[A[i]] = i
       pref[i] = distinct
3. Compute suf[1..N]:
   last = array of size N+1, initialize with N+1.
   distinct = 0
   for i in N down to 1:
       if last[A[i]] == N+1: distinct += 1
       last[A[i]] = i
       suf[i] = distinct
   Then C[i] = suf[i+1] for i=1..N-1. (C[N] not needed)
4. Compute nxt[1..N]:
   next_pos = array of size N+1, initialize with N+1.
   for i in N down to 1:
       nxt[i] = next_pos[A[i]]
       next_pos[A[i]] = i
5. Build segment tree over indices 1..N-1. We can use a class SegTree.
   The tree will support:
   - __init__(n): builds an empty tree (all zeros).
   - range_add(l, r, val): add val to all elements in [l, r].
   - range_max(l, r): return max in [l, r].
   - point_set(pos, val): set the value at pos to val. We can implement this as a point update with overwrite. In lazy propagation segment tree, we can do a recursive update that sets the leaf to val and pushes updates. Or we can just do a range add after setting a point? But we need to set to a specific value, not add. Since we are setting a new value and the old value is 0 (or whatever), we can just do a point assignment. In segment tree, we can have a method to set a leaf to a value. We'll implement point_set by traversing down to the leaf and setting it, then updating upwards. We also need to push lazy tags. But we can also just do: since we know the point is currently 0, we can just add the value? No, it might have been updated by a range add from a previous iteration? But wait: we process s from N-1 down to 1. For s = N-1, we set index N-1. For s = N-2, we set index N-2, and add to range starting at N-1. So index N-2 is fresh. For s = N-3, we set index N-3, and add to range starting at N-2. So index N-3 is fresh. So each index is set exactly once. Therefore, we can just do a point set that overwrites the current value. We can implement point_set by doing a range add of the new value minus the current value? That's messy. Better to implement a proper point assignment.
   Alternatively, we can avoid point_set by initializing the array with zeros, and when we process s, we do: 
        total[s] = 1 + C[s]
        add 1 to [s+1, nxt[s]-1]
   But we need to query max over [s, N-1]. We can just build the segment tree from the array after all updates? But we need to query for each s. So we need to do the updates and then query.
   Since each index is set only once, we can just do a point set. Let's implement a segment tree with lazy propagation that supports:
        - add(l, r, val)
        - set(pos, val)  [overwrites]
        - max(l, r)
   Actually, we can combine set and add by noting that when we set, we are setting to a value that should not include the previous adds? But since the index is fresh, the previous value is 0, and we haven't added anything to it yet (the range adds for this s start at s+1). So we can just do: point_set(s, 1 + C[s]). But wait: could the index s have been affected by a range add from a previous s? No, because previous s were greater than current s. The range adds from previous s were for indices ≥ previous s+1. Since current s is less than previous s, it is not in those ranges. So index s has not been modified. So it is currently 0. So we can just set it to 1 + C[s]. But to be safe, we can just do a point update that sets the leaf to the new value regardless. In a segment tree, we can implement point_set by traversing to the leaf and setting it, then updating ancestors with max. Lazy tags on the path should be cleared or applied. We can implement a standard lazy segment tree that supports range add and point set (assignment). Or we can just use a simple approach: since we only need max over suffixes, we can maintain an array and use a Fenwick tree for range add and a separate array for max? No.
   Let's just write a segment tree with lazy propagation. It will have arrays: tree (max), lazy (add). We need:
        - build(n): initialize with zeros.
        - _push(node, l, r): if lazy[node] != 0, apply to children.
        - range_add(node, l, r, ql, qr, val)
        - point_set(node, l, r, pos, val): set the position to val. We need to consider that there might be a lazy tag. We can push down before setting, or we can just set the leaf and then recalculate. Since we are setting a leaf that is not covered by any pending lazy tag? Actually, it could be covered by a lazy tag from a previous range add that covered a range that includes this position. But we just said that for position s, it was not included in any range add before because previous s were larger. But wait: when we process s, the segment tree has been updated with range adds for previous s (which are > s). Those range adds were for ranges [prev_s+1, nxt[prev_s]-1]. Since prev_s > s, the start of the range is > s+1? Actually, prev_s+1 > s+1. So the range is a subset of [s+2, N]. So index s is not in that range. So index s has no lazy tag. So we can safely set it. However, if we want to be robust, we can implement point_set by first pushing any lazy tags on the path, or by just doing a range add of (new_val - current_val) after querying the current value. But querying the current value is O(log N). That's fine: we can do a point query to get the current value, then add the difference. But since we know the current value should be 0, we can just set it. I'll implement point_set properly by traversing to the leaf and setting it, and combining with the lazy tag if needed. Actually, in a lazy segment tree, if we want to set a point, we can do a range add of the new value minus the old value. But we don't know the old value easily without a point query. Alternatively, we can just do a range update that sets the point. The standard way is to have a segment tree that supports range assign and range sum/max. But that's more complex. 
   Since we know the point is not under any lazy tag, we can just do a point update that sets the leaf to the value. We can implement it by calling a function that goes down to the leaf, and if it encounters a lazy tag, it pushes it down. But if the point is not covered by any lazy tag, we don't need to push. But to be safe, we can just implement a method that updates a point by doing: query the point to get the current value, then add the difference. But that's two operations. 
   Actually, we can just do: since the array is initialized to 0, and we only add positive values, we can just do a point add? No, we need to set it to a specific value, not add. But the initial value is 0, so setting to v is the same as adding v. So we can just do a range add on a single point: range_add(s, s, 1 + C[s]). That is perfectly valid! Because the point s is currently 0, adding 1+C[s] will set it to 1+C[s]. And it will correctly handle any existing lazy tags? Actually, if there is a lazy tag on a node covering s, adding to it will add to the lazy tag. But we argued that s is not under any lazy tag because it hasn't been touched. But what if a previous range add covered s? As argued, previous s' were > s, so the range starts at s'+1 > s+1, so s is not included. So s is not covered. So a point add is fine. But to be absolutely correct, we can just do range_add(s, s, 1 + C[s]). That is simple and works. Because even if there was a previous value (there shouldn't be), adding would be wrong. So we need to ensure s hasn't been added before. Since we process s from N-1 down to 1, and we only add to ranges starting at s+1, the point s is never added to. So range_add(s, s, val) is effectively a set. So we can just use range_add for both.
   So we can just use a segment tree that supports range_add and range_max. We'll do:
        range_add(s, s, 1 + C[s])  # This sets the point because it's currently 0.
        if s+1 <= nxt[s]-1 and s+1 <= N-1:
            r = min(nxt[s]-1, N-1)
            if s+1 <= r:
                range_add(s+1, r, 1)
        G[s] = range_max(s, N-1)
   This is perfectly valid and simpler.
   Let's double-check: For s=4 in example 1: we do range_add(4,4,2). Then range_add(5, ...) is empty. Then max(4,4) = 2. Correct.
   For s=3: range_add(3,3,3). Then nxt[3]=6, so range_add(4,5,1) -> only 4 gets 1. Then max(3,4) = max(3, 3+1)=3. Correct.
   So this works.

Now, we need to compute pref[s-1] + G[s] for s=2..N-1.
We have pref array, and G array (we can store it in an array G[s]).
Then answer = max(pref[s-1] + G[s] for s in 2..N-1).

Let's test on the second sample manually to be sure.
N=10, A = [2,5,6,4,4,1,1,3,1,4]
Compute pref:
1:2 ->1
2:2,5 ->2
3:2,5,6 ->3
4:2,5,6,4 ->4
5:2,5,6,4,4 ->4
6:2,5,6,4,1 ->5
7:2,5,6,4,1,1 ->5
8:2,5,6,4,1,3 ->6
9:2,5,6,4,1,3,1 ->6
10:2,5,6,4,1,3,4 ->6 (since 4 already)
pref: [1,2,3,4,4,5,5,6,6,6]
suf:
10:4 ->1
9:1,4 ->2
8:3,1,4 ->3
7:1,3,1,4 ->3 (1,3,4)
6:1,1,3,1,4 ->3 (1,3,4)
5:4,1,1,3,1,4 ->3 (4,1,3)
4:4,4,1,1,3,1,4 ->3 (4,1,3)
3:6,4,4,1,1,3,1,4 ->4 (6,4,1,3)
2:5,6,4,4,1,1,3,1,4 ->5 (5,6,4,1,3)
1:2,5,6,4,4,1,1,3,1,4 ->5 (2,5,6,4,1,3)
suf: [5,5,4,3,3,3,3,3,2,1]
C[i] = suf[i+1] for i=1..9:
C[1]=5, C[2]=4, C[3]=3, C[4]=3, C[5]=3, C[6]=3, C[7]=3, C[8]=2, C[9]=1.
nxt[i]:
A: 2,5,6,4,4,1,1,3,1,4
next_pos initially N+1=11.
i=10: A[10]=4, next_pos[4]=11, nxt[10]=11, set next_pos[4]=10.
i=9: A[9]=1, nxt[9]=11, set next_pos[1]=9.
i=8: A[8]=3, nxt[8]=11, set next_pos[3]=8.
i=7: A[7]=1, nxt[7]=9, set next_pos[1]=7.
i=6: A[6]=1, nxt[6]=7, set next_pos[1]=6.
i=5: A[5]=4, nxt[5]=10, set next_pos[4]=5.
i=4: A[4]=4, nxt[4]=5, set next_pos[4]=4.
i=3: A[3]=6, nxt[3]=11, set next_pos[6]=3.
i=2: A[2]=5, nxt[2]=11, set next_pos[5]=2.
i=1: A[1]=2, nxt[1]=11, set next_pos[2]=1.
So nxt: [11,11,11,5,10,7,9,11,11,11] (for 1..10)
Now process s from 9 down to 1 (N-1=9).
Segment tree size 9.
Initialize all 0.
s=9: C[9]=1, so set index 9: range_add(9,9, 1+1=2). nxt[9]=11, so range [10,10] empty. G[9] = max(9,9)=2.
s=8: C[8]=2, set index 8: range_add(8,8, 1+2=3). nxt[8]=11, range [9,10] -> add 1 to 9. So index 9 becomes 2+1=3. G[8] = max(8,9)=max(3,3)=3.
s=7: C[7]=3, set index 7: range_add(7,7, 1+3=4). nxt[7]=9, range [8,8] -> add 1 to 8. Index 8 becomes 3+1=4. G[7] = max(7..9)=max(4,4,3)=4.
s=6: C[6]=3, set index 6: range_add(6,6, 1+3=4). nxt[6]=7, range [7,6] empty. G[6] = max(6..9)=max(4,4,4,3)=4.
s=5: C[5]=3, set index 5: range_add(5,5, 1+3=4). nxt[5]=10, range [6,9] -> add 1 to 6,7,8,9. So:
   5:4
   6:4+1=5
   7:4+1=5
   8:4+1=5
   9:3+1=4
   G[5] = max(5..9)=max(4,5,5,5,4)=5.
s=4: C[4]=3, set index 4: range_add(4,4, 1+3=4). nxt[4]=5, range [5,4] empty. G[4] = max(4..9)=max(4,5,5,5,5,4)=5.
s=3: C[3]=3, set index 3: range_add(3,3, 1+3=4). nxt[3]=11, range [4,10] -> add 1 to 4..9.
   3:4
   4:4+1=5
   5:4+1=5
   6:5+1=6
   7:5+1=6
   8:5+1=6
   9:4+1=5
   G[3] = max(3..9)=max(4,5,5,6,6,6,5)=6.
s=2: C[2]=4, set index 2: range_add(2,2, 1+4=5). nxt[2]=11, range [3,10] -> add 1 to 3..9.
   2:5
   3:4+1=5
   4:5+1=6
   5:5+1=6
   6:6+1=7
   7:6+1=7
   8:6+1=7
   9:5+1=6
   G[2] = max(2..9)=max(5,5,6,6,7,7,7,6)=7.
s=1: C[1]=5, set index 1: range_add(1,1, 1+5=6). nxt[1]=11, range [2,10] -> add 1 to 2..9.
   1:6
   2:5+1=6
   3:5+1=6
   4:6+1=7
   5:6+1=7
   6:7+1=8
   7:7+1=8
   8:7+1=8
   9:6+1=7
   G[1] = max(1..9)=max(6,6,6,7,7,8,8,8,7)=8.
Now compute answer = max_{s=2}^{9} (pref[s-1] + G[s]).
s=2: pref[1] + G[2] = 1 + 7 = 8.
s=3: pref[2] + G[3] = 2 + 6 = 8.
s=4: pref[3] + G[4] = 3 + 5 = 8.
s=5: pref[4] + G[5] = 4 + 5 = 9.
s=6: pref[5] + G[6] = 4 + 4 = 8.
s=7: pref[6] + G[7] = 5 + 4 = 9.
s=8: pref[7] + G[7]? wait pref[7] is pref[7]? s=8: pref[7] + G[8] = 5 + 3 = 8.
s=9: pref[8] + G[9] = 6 + 2 = 8.
Max is 9. So answer 9. Matches sample output.

Great! The algorithm works.

Now, we need to implement the segment tree. We can use a class with arrays of size 4*N. Since we only need range add and range max, and we only query max over suffixes, we can also use a simpler structure: we can maintain an array total[] and use a Fenwick tree for range add, and a separate segment tree for range max? But range add and range max can be done with a segment tree with lazy propagation. That's straightforward.

Alternatively, we can avoid the segment tree by using the following observation: The updates are "add 1 to a prefix of the suffix range". Actually, when we do range_add(s+1, nxt[s]-1, 1), this is a range that starts at s+1 and ends at nxt[s]-1. Note that s+1 is increasing as s decreases? No, s is decreasing, so s+1 is decreasing. The ranges are not necessarily nested in a simple way. But we can still use a segment tree.

Since N=3e5, a segment tree with 4*3e5 = 1.2e6 nodes is fine.

Let's code the segment tree.
We need:
- n: size (N-1)
- tree: array for max
- lazy: array for add
Functions:
- __init__(n): set self.n = n, size 4*n, all 0.
- _push(node): if lazy[node] != 0, apply to children.
- _add(node, l, r, ql, qr, val): if ql <= l and r <= qr: tree[node] += val; lazy[node] += val; else push, recurse, then tree[node] = max(tree[left], tree[right]).
- range_add(l, r, val): call _add(1, 1, n, l, r, val)
- _query(node, l, r, ql, qr): if ql <= l and r <= qr: return tree[node]; else push, return max of children if overlap.
- range_max(l, r): call _query(1, 1, n, l, r)

We need to handle the case when l > r: do nothing.

Also, we need to store G[s] for s=1..N-1. We can use an array G of size N+1.

Let's write the code accordingly.

One detail: When we do range_add(s, s, 1 + C[s]), we are adding to a point. The segment tree should handle that. The initial values are 0, so adding 1+C[s] sets it. But what if C[s] is large? It's fine.

Let's code in Python.

We need to be careful with recursion depth in Python. 3e5 might cause recursion limit issues if we use