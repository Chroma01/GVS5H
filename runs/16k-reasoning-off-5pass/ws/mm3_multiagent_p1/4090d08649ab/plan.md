We need to compute, for every subarray, the minimum number of operations to erase all numbers where each operation can erase all occurrences of a contiguous integer interval [l,r] that appears in the subarray. This is equivalent to covering the multiset of values in the subarray by the minimum number of contiguous integer intervals. Since each operation can erase any contiguous integer range that is fully present, the answer equals the number of "connected components" of the set of distinct values in the subarray when values are viewed on the integer line. So f(L,R) = number of connected components of the set {A_L..A_R} on the integer line.

We need sum over all subarrays of the number of components. For each subarray, components = 1 + (number of "gaps" between consecutive distinct values). A gap occurs when we have two consecutive occurrences of the same value? Actually, a gap in the value set occurs when we have a value x present, and the next larger value present is y > x+1. Equivalently, for a subarray, components = number of distinct values - number of adjacent pairs (x, x+1) both present.

So sum f(L,R) = sum over subarrays of (1 + gaps). Sum of 1 over all subarrays = N*(N+1)/2. So we need to count, for each subarray, the number of "adjacent value pairs" (x, x+1) both present. Let's denote for each adjacent integer pair (v, v+1), count the number of subarrays where both v and v+1 appear at least once. Then sum f = N*(N+1)/2 + sum_{v=1}^{N-1} count_subarrays_containing_both(v, v+1).

Now we need to count, for each pair (v, v+1), the number of subarrays that contain at least one occurrence of v and at least one occurrence of v+1. N up to 3e5, A_i up to N. We can process each pair independently using positions.

Let positions of v be p1 < p2 < ... < pk, positions of v+1 be q1 < q2 < ... < qm. We need to count subarrays [L,R] such that L <= min(p_i, q_j) and R >= max(p_i, q_j) for some i,j? Actually we need subarray containing at least one v and at least one v+1. Equivalent to: there exists i,j with L <= p_i <= R and L <= q_j <= R. So the subarray must cover at least one v and at least one v+1.

We can count total subarrays minus those missing v or missing v+1. But inclusion-exclusion: total subarrays = N*(N+1)/2. Subarrays missing v = subarrays that contain no v. Similarly for v+1. Subarrays missing both v and v+1 = subarrays containing neither v nor v+1. Then count = total - missing_v - missing_{v+1} + missing_both.

We can compute missing_v: number of subarrays with no v. This is sum over gaps between consecutive occurrences of v (including before first and after last) of len*(len+1)/2, where len is length of segment without v. Similarly for v+1. For missing both: we need to consider the merged positions of v and v+1? Actually we need subarrays that contain neither v nor v+1. This is like we have a set of "forbidden" positions (where A_i is v or v+1). The subarray must avoid all these positions. So we can treat the sequence and mark positions where A_i in {v, v+1}. Then missing_both = sum over gaps between these marked positions of len*(len+1)/2, where len is length of consecutive segment without v or v+1.

Thus for each pair (v, v+1), we can compute:
- total = N*(N+1)/2
- miss_v = sum_{segments without v} len*(len+1)/2
- miss_v1 = sum_{segments without v+1} len*(len+1)/2
- miss_both = sum_{segments without v or v+1} len*(len+1)/2

Then count = total - miss_v - miss_v1 + miss_both.

We need to sum over v=1..N-1. N up to 3e5, so O(N) pairs. For each pair, we need to compute these sums efficiently. We can precompute for each value v the list of positions. Then for each v, we can compute miss_v easily: we have positions of v, we can iterate over gaps. But doing that for each v separately would be O(N) per v? Actually total sum of lengths of position lists is N. So computing miss_v for all v can be done in O(N) total by iterating over each value's positions once. Similarly for miss_{v+1} we can reuse the same lists.

But we also need miss_both for each adjacent pair (v, v+1). That seems more challenging: we need to consider the union of positions of v and v+1. For each pair, we could merge the two sorted lists and compute gaps. However, doing that for each pair naively would be O(N^2) in worst case (e.g., all values distinct). But note that each position belongs to exactly one value. For a given position i, it contributes to miss_both for pairs (v, v+1) where v = A_i - 1 or v = A_i? Actually if A_i = x, then for pair (x-1, x) and pair (x, x+1), the position i is a "forbidden" position (since it is either v or v+1). So each position i is forbidden for at most two pairs: (A_i - 1, A_i) and (A_i, A_i + 1). So we can process contributions per position.

We need to compute for each pair (v, v+1) the sum over gaps of len*(len+1)/2 where gaps are segments of consecutive indices that contain neither v nor v+1. This is equivalent to: we have a binary array B_i where B_i = 1 if A_i in {v, v+1}, else 0. Then miss_both = sum over maximal contiguous segments of zeros of len*(len+1)/2.

We can compute this for all pairs efficiently by scanning the array and maintaining for each pair the length of current zero segment. Since each position i is "forbidden" for at most two pairs, we can update the state for those pairs.

Specifically, for each pair (v, v+1), we maintain cur_len[v] = length of current zero segment (i.e., consecutive positions not containing v or v+1). Initially cur_len[v] = 0. When we move to position i, we check if A_i is in {v, v+1}. If yes, then the current zero segment ends, so we add cur_len[v]*(cur_len[v]+1)/2 to miss_both[v], and reset cur_len[v] = 0. If no, then cur_len[v] increments by 1.

We need to do this for all v from 1 to N-1. That's O(N^2) if we update for all v at each step. But we can note that for a given position i, only pairs (A_i - 1, A_i) and (A_i, A_i + 1) are affected (i.e., the zero segment ends for those pairs). For all other pairs, the zero segment continues (since A_i is not v or v+1). So we can update cur_len for all pairs by incrementing by 1 for all pairs except those two? That would be O(N^2). However, we can use a different approach: we can compute miss_both for each pair by considering the positions of v and v+1 and merging them. Since each position belongs to exactly one value, the total size of merged lists across all pairs is O(N) per position? Actually each position appears in two pairs: (A_i - 1, A_i) and (A_i, A_i + 1). So if we process each pair by merging the two lists, the total work across all pairs would be sum over pairs of (size of list of v + size of list of v+1). Since each value v appears in two pairs: (v-1, v) and (v, v+1). So the total sum of list sizes over all pairs is 2 * N (each position counted twice). So if we can merge two sorted lists in linear time, total time O(N) for all pairs. That is feasible.

Thus algorithm:
- Preprocess: for each value v (1..N), store sorted list of positions where A_i = v.
- For each v from 1 to N-1:
   - Compute miss_v: using positions of v. Let pos_v = list. Let prev = 0. For each p in pos_v: gap = p - prev - 1; add gap*(gap+1)/2 to miss_v. After loop, gap = N - pos_v[-1]; add that. (If pos_v empty, then miss_v = N*(N+1)/2.)
   - Similarly miss_v1 using positions of v+1.
   - Compute miss_both: merge the two sorted lists pos_v and pos_v1 to get sorted list of forbidden positions. Then compute gaps between them: let prev = 0. For each p in merged list: gap = p - prev - 1; add gap*(gap+1)/2. After loop, gap = N - last; add. (If both lists empty, miss_both = N*(N+1)/2.)
   - Then count = total - miss_v - miss_v1 + miss_both.
   - Add count to answer.

But careful: total = N*(N+1)/2. However, we need sum of f(L,R) = total + sum_{v} count_{v} where count_v is number of subarrays containing both v and v+1. Wait earlier we derived: f(L,R) = 1 + number of gaps between consecutive distinct values. Number of gaps = number of adjacent pairs (x, x+1) both present. So sum f = sum_{subarrays} 1 + sum_{subarrays} (indicator that both v and v+1 present). Sum of 1 = total. So sum f = total + sum_{v} count_{v}. So we need to compute sum_{v} count_{v}.

Thus answer = total + sum_{v=1}^{N-1} count_{v}.

We can compute count_{v} as described.

Complexities: O(N + sum of lengths of position lists) = O(N). Merging two lists per pair: total work O(N). So overall O(N). Memory: O(N) for position lists.

We need to be careful with large N (3e5) and integer overflow: answer can be up to O(N^2) ~ 9e10, fits in 64-bit (Python int is arbitrary).

Edge cases: values may be up to N, but we only consider pairs (v, v+1) where v from 1 to N-1. Some values may not appear. If pos_v is empty, then miss_v = total (since no v in any subarray). Similarly for v+1. If both empty, miss_both = total. Then count = total - total - total + total = 0. That makes sense: if neither v nor v+1 appear, then no subarray contains both.

If only one appears, say pos_v non-empty, pos_v1 empty. Then miss_v1 = total. miss_both = total (since v+1 never appears, so any subarray missing v+1 is also missing both? Actually if v+1 never appears, then any subarray is missing v+1, so missing both = total. So count = total - miss_v - total + total = total - miss_v. But miss_v is number of subarrays missing v. So count = total - miss_v = number of subarrays containing v. But we need subarrays containing both v and v+1. Since v+1 never appears, count should be 0. Wait our formula: count = total - miss_v - miss_v1 + miss_both. If v+1 never appears, miss_v1 = total. miss_both = total (since no v+1, so missing both = missing v+1 = total). Then count = total - miss_v - total + total = total - miss_v. That is not zero unless miss_v = total (i.e., v never appears). But if v appears, miss_v < total, so count > 0. That's wrong. Let's re-evaluate.

We want count of subarrays that contain at least one v and at least one v+1. If v+1 never appears, then no subarray can contain v+1, so count should be 0. Our inclusion-exclusion: total - miss_v - miss_{v+1} + miss_{both}. If v+1 never appears, then miss_{v+1} = total (all subarrays miss v+1). miss_{both} = number of subarrays missing both v and v+1. Since v+1 is missing in all subarrays, missing both = missing v+1 = total. So count = total - miss_v - total + total = total - miss_v. That is not zero. So something is off.

Wait: inclusion-exclusion for "contains both" is: |A ∩ B| = total - |A^c| - |B^c| + |A^c ∩ B^c|. Here A = subarrays containing v, B = subarrays containing v+1. So A^c = subarrays missing v. B^c = subarrays missing v+1. A^c ∩ B^c = subarrays missing both v and v+1. So count = total - miss_v - miss_{v+1} + miss_{both}. That is correct.

If v+1 never appears, then B is empty, so count = 0. Let's compute: miss_{v+1} = total (since no subarray contains v+1). miss_{both} = number of subarrays missing both v and v+1. Since v+1 is missing in all subarrays, missing both = missing v+1 = total. So count = total - miss_v - total + total = total - miss_v. That is not zero. So there is a mistake: if v+1 never appears, then B is empty, so A ∩ B = empty. But our formula gives total - miss_v. Let's test with small example: N=2, A=[1,1]. v=1, v+1=2. v appears, v+1 never appears. total = 3 subarrays: [1], [2], [1,2]. miss_v = subarrays missing 1: only [2] (len 1) => 1. miss_{v+1} = subarrays missing 2: all subarrays => 3. miss_both = subarrays missing both 1 and 2: all subarrays => 3. Then count = 3 - 1 - 3 + 3 = 2. But actual subarrays containing both 1 and 2: none. So count should be 0. So formula fails.

Why? Because inclusion-exclusion is correct, but our interpretation of miss_{both} is wrong. Let's compute miss_{both} correctly: subarrays that contain neither v nor v+1. In the example, subarrays: [1] contains 1, so not both missing. [2] contains 2, so not both missing. [1,2] contains both. So actually there are 0 subarrays missing both. Wait, [2] contains 2, which is v+1, so it is missing v but contains v+1, so not missing both. So miss_both = 0. But we computed miss_both = total = 3. That's wrong. Because we assumed that if v+1 never appears, then missing both = missing v+1. But that's not true: missing both means missing v AND missing v+1. If v+1 never appears, then any subarray is missing v+1. But to be missing both, it must also miss v. So missing both = subarrays missing v (since v+1 is always missing). So miss_both = miss_v. In the example, miss_v = 1 (subarray [2]), so miss_both = 1. Then count = total - miss_v - miss_{v+1} + miss_both = 3 - 1 - 3 + 1 = 0. Good.

So our earlier method for computing miss_both as sum over gaps of zeros in the binary array where B_i=1 if A_i in {v, v+1} is correct. But we need to compute it correctly. In the case where v+1 never appears, the binary array has B_i=1 only when A_i = v. So the zeros are segments without v. So miss_both = sum over gaps between v positions of len*(len+1)/2. That is exactly miss_v. So our method of merging positions of v and v+1 to get forbidden positions works: if v+1 has no positions, then forbidden positions are just positions of v. Then gaps between them are exactly the gaps between v positions. So miss_both = miss_v. Good.

Thus our algorithm for computing miss_both by merging the two lists is correct. In the example, pos_v = [1,2], pos_v1 = []. Merged list = [1,2]. Gaps: before first: 0; between 1 and 2: 0; after last: 0. So miss_both = 0? Wait, we need to compute gaps of zeros: segments of consecutive indices that are not in the merged list. The merged list is [1,2]. The zeros are indices not in {1,2}. So indices: 0? Actually positions are 1-indexed. The array is length 2. The forbidden positions are 1 and 2. So there are no zeros. So miss_both = 0. But we expected miss_both = miss_v = 1. There's a discrepancy.

Let's compute carefully: N=2. Positions: 1 and 2. Forbidden positions: {1,2}. So the entire array is forbidden. So there are no segments of zeros. So miss_both = 0. But we argued that miss_both should be miss_v = 1. Let's list subarrays: [1] (positions 1..1) contains 1, so not missing both. [2] (positions 2..2) contains 2, so not missing both. [1,2] contains both. So indeed there are 0 subarrays missing both. So miss_both = 0. But earlier we said miss_both = miss_v = 1. That was wrong. Because miss_v counts subarrays missing v. Subarray [2] misses v (1) but contains v+1 (2). So it is missing v but not missing both. So missing both is a stricter condition: must miss both. So if v+1 never appears, then missing both = subarrays that miss v AND miss v+1. Since v+1 is always missing, missing both = subarrays that miss v. So miss_both = miss_v. But in our example, miss_v = 1 (subarray [2]). So miss_both should be 1. But our computation of miss_both via gaps gave 0. Why?

Because the binary array B_i = 1 if A_i in {v, v+1}. In the example, A = [1,1]. So B = [1,1] (since A_i = 1 = v). So zeros are segments where B_i = 0. There are no zeros. So miss_both = 0. But we expected 1. So there is a mismatch: the condition "missing both v and v+1" means the subarray contains no v and no v+1. In the example, subarray [2] (position 2) contains A_2 = 1, which is v. So it contains v. So it does not miss v. Wait, subarray [2] is just index 2. A_2 = 1. So it contains v. So it does not miss v. So miss_v should be 0? Let's recompute miss_v: subarrays missing v (i.e., containing no 1). In A=[1,1], the only subarray that does not contain 1 is... none, because every element is 1. So miss_v = 0. Indeed, there is no subarray without 1. So miss_v = 0. Then miss_both = 0. So count = total - 0 - 3 + 0 = 0. Good.

So my earlier example with A=[1,1] and v=1, v+1=2: miss_v = 0, miss_{v+1} = 3, miss_both = 0. So count = 3 - 0 - 3 + 0 = 0. Correct.

Thus the formula works. The earlier miscalculation was because I incorrectly thought miss_v = 1 for subarray [2] but that subarray actually contains 1. So it's fine.

Thus the algorithm is correct.

Now we need to implement efficiently.

Implementation steps:

1. Read N and array A (1-indexed for convenience).
2. Create a list of lists: pos = [[] for _ in range(N+1)] (since A_i <= N). For i from 1 to N: pos[A_i].append(i).
3. Precompute total = N*(N+1)//2.
4. Initialize ans = total (for the +1 per subarray).
5. For v in range(1, N):
   - Compute miss_v: using pos[v].
     - If pos[v] is empty: miss_v = total.
     - Else: prev = 0; for p in pos[v]: gap = p - prev - 1; miss_v += gap*(gap+1)//2; prev = p.
       After loop: gap = N - prev; miss_v += gap*(gap+1)//2.
   - Compute miss_v1 similarly using pos[v+1].
   - Compute miss_both: merge pos[v] and pos[v+1] into a single sorted list.
     - We can merge by iterating through both lists with two pointers.
     - Let merged = [] (or just process on the fly). We need to compute gaps between consecutive forbidden positions.
     - Initialize prev = 0; miss_both = 0.
     - While there are elements in either list:
        - Take the smaller position p.
        - gap = p - prev - 1; miss_both += gap*(gap+1)//2.
        - prev = p.
     - After merging all, gap = N - prev; miss_both += gap*(gap+1)//2.
   - count = total - miss_v - miss_v1 + miss_both.
   - ans += count.

6. Print ans.

Complexities: For each v, merging two lists takes O(|pos[v]| + |pos[v+1]|). Since each position appears in exactly two lists (for v = A_i - 1 and v = A_i), the total work across all v is O(N). So overall O(N).

We need to be careful with memory: pos is list of N+1 lists, total size N. Merging per v: we can avoid creating a new list by using two pointers and processing on the fly.

Edge cases: v and v+1 may be out of bounds? v from 1 to N-1, so v+1 <= N. pos has size N+1, index up to N. So fine.

Now we need to verify with sample inputs.

Sample 1:
N=4, A=[1,3,1,4].
pos[1]=[1,3], pos[2]=[], pos[3]=[2], pos[4]=[4].
total = 10.
ans = 10.

v=1:
miss_v: pos[1]=[1,3]. gaps: before 1: 0; between 1 and 3: 1 (position 2) -> 1*2/2=1; after 3: 1 (position 4) -> 1. So miss_v = 2.
miss_v1: pos[2]=[] -> miss_v1 = total = 10.
miss_both: merge pos[1] and pos[2] = [1,3]. gaps: before 1:0; between 1 and 3:1 ->1; after 3:1 ->1. So miss_both = 2.
count = 10 - 2 - 10 + 2 = 0.
ans += 0 -> 10.

v=2:
miss_v: pos[2]=[] -> 10.
miss_v1: pos[3]=[2] -> gaps: before 2:1 (pos1) ->1; after 2:2 (pos3,4) -> 3. So miss_v1 = 1+3=4.
miss_both: merge pos[2] and pos[3] = [2]. gaps: before 2:1 ->1; after 2:2 ->3. So miss_both = 4.
count = 10 - 10 - 4 + 4 = 0.
ans = 10.

v=3:
miss_v: pos[3]=[2] -> gaps: before 2:1 ->1; after 2:2 ->3. So miss_v = 4.
miss_v1: pos[4]=[4] -> gaps: before 4:3 ->6; after 4:0 ->0. So miss_v1 = 6.
miss_both: merge pos[3] and pos[4] = [2,4]. gaps: before 2:1 ->1; between 2 and 4:1 (pos3) ->1; after 4:0 ->0. So miss_both = 2.
count = 10 - 4 - 6 + 2 = 2.
ans = 12.

But expected answer is 16. So we are missing something. Let's compute manually.

We need sum f(L,R). Let's compute f for all subarrays:
A=[1,3,1,4]
Subarrays:
[1]: values {1} -> components=1 -> f=1
[3]: {3} ->1
[1]: {1} ->1
[4]: {4} ->1
[1,3]: {1,3} -> components: 1 and 3 not adjacent? 1 and 3 are not consecutive integers, so two components -> f=2
[3,1]: {1,3} ->2
[1,4]: {1,4} ->2
[1,3,1]: {1,3} ->2
[3,1,4]: {1,3,4} -> components: 1,3,4. 3 and 4 are adjacent, so components: {1} and {3,4} ->2
[1,3,1,4]: {1,3,4} ->2
[3,1,4]: same as above? Actually [3,1,4] is indices 2..4: {3,1,4} ->2
[1,4]: indices 3..4: {1,4} ->2
[1,3,1,4]: indices 1..4: {1,3,4} ->2
Wait we need all subarrays:
L=1: R=1:1; R=2:2; R=3:2; R=4:2
L=2: R=2:1; R=3:2; R=4:2
L=3: R=3:1; R=4:2
L=4: R=4:1
Sum: 1+2+2+2 + 1+2+2 + 1+2 + 1 = (1+2+2+2)=7, (1+2+2)=5, (1+2)=3, (1)=1. Total = 7+5+3+1 = 16. Yes.

Our computed ans = 12. So we are missing 4. Let's compute count_v for each v:
v=1: count = number of subarrays containing both 1 and 2. Since 2 never appears, count=0.
v=2: count = subarrays containing both 2 and 3. 2 never appears, so 0.
v=3: count = subarrays containing both 3 and 4. Let's list subarrays containing both 3 and 4: need at least one 3 and one 4. Positions: 3 at index 2, 4 at index 4. Subarrays that cover both: L <=2 and R >=4. So subarrays: [1..4], [2..4]. That's 2 subarrays. So count should be 2. Our computed count for v=3 was 2. So sum counts = 2. Then ans = total + sum counts = 10 + 2 = 12. But actual sum f = 16. So total + sum counts is not matching? Let's compute sum f manually: sum f = 16. total = 10. So sum counts should be 6. But we only got 2. So our decomposition f = 1 + number of gaps is wrong? Let's re-express.

We said f(L,R) = number of connected components of the set of distinct values. For a set of integers, the number of components is 1 + number of gaps between consecutive distinct values. A gap occurs when there is a missing integer between two present values. But also, if the set is empty? Not possible. So for subarray [1,3,1], distinct values {1,3}. The integers are 1 and 3. The gap is 2. So number of components = 2. So f=2. That matches.

Now sum over subarrays of number of components = sum over subarrays of (1 + number of gaps). So sum f = total + sum_{subarrays} (number of gaps). A gap is defined as a pair of consecutive integers (x, x+1) such that both x and x+1 are present in the subarray? Wait, a gap in the set means there is a missing integer between two present values. For example, set {1,3}: missing 2. The gap is between 1 and 3. But that corresponds to the pair (1,2) and (2,3)? Actually the missing integer is 2. The gap is between 1 and 3. The number of gaps is the number of "breaks" in the integer line. For a set of distinct integers, the number of components = number of distinct values - number of adjacent pairs (x, x+1) both present. Because if x and x+1 are both present, they are in the same component. So components = distinct_count - adjacent_pairs. Then f = distinct_count - adjacent_pairs. But we also have f = components. So f = distinct_count - adjacent_pairs.

But earlier we said f = 1 + number of gaps. Let's check: distinct_count = 2, adjacent_pairs = 0 (since 1 and 3 not adjacent). So f = 2 - 0 = 2. And 1 + gaps: gaps = number of missing integers between min and max? Actually number of gaps in the set is the number of "breaks" between consecutive sorted distinct values. For {1,3}, sorted distinct: 1,3. The gap is between 1 and 3 (missing 2). So number of gaps = 1. Then 1 + gaps = 2. So that matches. But adjacent_pairs = 0, distinct_count = 2, so distinct_count - adjacent_pairs = 2. So both formulas are equivalent: components = distinct_count - adjacent_pairs = 1 + (distinct_count - 1 - adjacent_pairs) = 1 + gaps, where gaps = distinct_count - 1 - adjacent_pairs. So gaps = number of "breaks" between consecutive distinct values. That is exactly the number of pairs of consecutive distinct values (in sorted order) that are not consecutive integers. So it's not simply the number of adjacent integer pairs present. It's the number of "missing links" in the chain of distinct values.

Thus our earlier reduction to counting subarrays containing both v and v+1 is incorrect. Because the number of gaps is not the number of adjacent integer pairs present; it's the number of missing adjacencies in the distinct set. Actually, if we have distinct values sorted: v1 < v2 < ... < vk. The number of gaps is the number of i such that v_{i+1} > v_i + 1. That is, the number of times there is a jump >1. This is equal to (k - 1) - (number of i such that v_{i+1} = v_i + 1). So number of gaps = (distinct_count - 1) - (number of adjacent integer pairs present). So f = 1 + gaps = distinct_count - (number of adjacent integer pairs present). So f = distinct_count - adjacent_pairs.

Thus sum f = sum_{subarrays} distinct_count - sum_{subarrays} adjacent_pairs.

Sum of distinct_count over all subarrays is a known problem: sum of number of distinct values in all subarrays. That can be computed in O(N) using standard technique (for each position, count subarrays where it is the first occurrence of its value, etc.). But we also need sum of adjacent_pairs over all subarrays. adjacent_pairs is the number of pairs (v, v+1) such that both v and v+1 appear in the subarray. So sum_{subarrays} adjacent_pairs = sum_{v} count_{v}, where count_{v} is number of subarrays containing both v and v+1. So we need to compute sum of distinct_count over all subarrays, and subtract sum_{v} count_{v}.

Thus answer = sum_distinct - sum_{v} count_{v}.

We already have a method to compute count_{v} (number of subarrays containing both v and v+1). So we need to compute sum_distinct.

Sum of distinct counts over all subarrays: For each value v, we can count the number of subarrays where v appears at least once. Then sum over v of that count gives sum_distinct. Because each subarray contributes 1 for each distinct value it contains. So sum_distinct = sum_{v} (number of subarrays containing v). That is exactly the same as count_{v} but with only one value. So we can compute for each v: number of subarrays containing v. Let's denote cnt_v = number of subarrays with at least one occurrence of v. Then sum_distinct = sum_v cnt_v.

We can compute cnt_v similarly using positions. For a value v with positions p1 < p2 < ... < pk. The number of subarrays containing v is total - miss_v, where miss_v is number of subarrays missing v. We already have a formula for miss_v. So cnt_v = total - miss_v.

Thus sum_distinct = sum_v (total - miss_v) = N * total - sum_v miss_v.

But we can compute sum_v miss_v efficiently? Since miss_v is computed per v, we can compute it in the loop. However, we need to compute sum_distinct anyway. Alternatively, we can compute sum_distinct directly using the standard technique: for each position i, the number of subarrays where A_i is the first occurrence of its value (i.e., subarrays starting at i and ending at some point before the next occurrence of the same value). That is: let next[i] be the next index > i where A_j = A_i, or N+1 if none. Then the number of subarrays where A_i is the first occurrence of its value is (next[i] - i) * (i - prev[i]), where prev[i] is previous occurrence. Actually the standard formula: the number of subarrays where A_i is the "new" distinct value (i.e., the first time this value appears in the subarray) is (i - prev[i]) * (next[i] - i). Summing over i gives sum_distinct. That is O(N) if we have prev and next arrays. That might be simpler.

But we already have positions per value. We can compute cnt_v = total - miss_v. Then sum_distinct = sum_v cnt_v. Since we are iterating over v anyway to compute count_v, we can compute miss_v and cnt_v in the same loop. However, note that we need to compute miss_v for all v, but we only need it for v from 1 to N-1 for count_v. But for sum_distinct we need cnt_v for all v that appear. Actually we need sum over all values v (1..N) of cnt_v. So we can compute for all v.

Thus we can compute:
- For each v from 1 to N:
   - Compute miss_v using positions.
   - cnt_v = total - miss_v.
   - Add cnt_v to sum_distinct.

Then for each v from 1 to N-1:
   - Compute count_v (subarrays containing both v and v+1) as before.
   - Add count_v to sum_adjacent.

Then answer = sum_distinct - sum_adjacent.

Let's test with sample 1.

N=4, total=10.
Compute miss_v for each v:
v=1: pos=[1,3], miss_v=2, cnt_v=8.
v=2: pos=[], miss_v=10, cnt_v=0.
v=3: pos=[2], miss_v=4, cnt_v=6.
v=4: pos=[4], miss_v=6, cnt_v=4.
Sum cnt_v = 8+0+6+4 = 18. So sum_distinct = 18.

Now compute count_v for v=1..3:
v=1: count=0 (as before).
v=2: count=0.
v=3: count=2.
Sum count_v = 2.

Answer = 18 - 2 = 16. Matches.

Great.

Now we need to compute miss_v efficiently for all v. We can do that in the same loop over v. Since we need to iterate over v from 1 to N anyway, we can compute miss_v for each v. But we also need to compute count_v for v=1..N-1, which requires merging pos[v] and pos[v+1]. So we can combine.

Implementation plan:

- Read N, A.
- pos = [[] for _ in range(N+1)].
- For i in range(N): pos[A[i]].append(i+1) (1-indexed).
- total = N*(N+1)//2.
- sum_distinct = 0.
- sum_adjacent = 0.
- For v in range(1, N+1):
   - Compute miss_v:
        if not pos[v]: miss_v = total
        else:
            prev = 0
            miss_v = 0
            for p in pos[v]:
                gap = p - prev - 1
                miss_v += gap*(gap+1)//2
                prev = p
            gap = N - prev
            miss_v += gap*(gap+1)//2
   - cnt_v = total - miss_v
   - sum_distinct += cnt_v

- For v in range(1, N):
   - Compute miss_v and miss_v1 (we already computed miss_v for v and v+1? We computed miss_v for all v in the previous loop. We can store miss_v in an array to reuse. But we can also recompute. Since we need miss_v and miss_v1 for count_v, we can compute them again or store. Storing is fine: create an array miss = [0]*(N+1). Fill it in the first loop. Then in the second loop, use miss[v] and miss[v+1].
   - Compute miss_both by merging pos[v] and pos[v+1].
   - count_v = total - miss[v] - miss[v+1] + miss_both
   - sum_adjacent += count_v

- Answer = sum_distinct - sum_adjacent.
- Print answer.

Complexities: O(N + total size of pos) = O(N). Merging per v: O(|pos[v]| + |pos[v+1]|). Total O(N). So overall O(N).

We need to be careful with integer types: Python int is fine.

Now test with sample 2.

Sample 2:
N=5, A=[3,1,4,2,4].
pos:
1: [2]
2: [4]
3: [1]
4: [3,5]
5: []
total = 15.

Compute miss_v:
v=1: pos=[2], gaps: before 2:1 ->1; after 2:3 ->6. miss=7. cnt=8.
v=2: pos=[4], gaps: before 4:3 ->6; after 4:1 ->1. miss=7. cnt=8.
v=3: pos=[1], gaps: before 1:0; after 1:4 ->10. miss=10. cnt=5.
v=4: pos=[3,5], gaps: before 3:2 ->3; between 3 and 5:1 ->1; after 5:0. miss=4. cnt=11.
v=5: pos=[], miss=15, cnt=0.
Sum cnt = 8+8+5+11+0 = 32. sum_distinct = 32.

Now compute count_v for v=1..4:
v=1: merge pos[1]=[2] and pos[2]=[4] -> [2,4]. gaps: before 2:1->1; between 2 and 4:1->1; after 4:1->1. miss_both=3. miss[1]=7, miss[2]=7. count = 15 - 7 - 7 + 3 = 4.
v=2: merge pos[2]=[4] and pos[3]=[1] -> [1,4]. gaps: before 1:0; between 1 and 4:2->3; after 4:1->1. miss_both=4. miss[2]=7, miss[3]=10. count = 15 - 7 - 10 + 4 = 2.
v=3: merge pos[3]=[1] and pos[4]=[3,5] -> [1,3,5]. gaps: before 1:0; between 1 and 3:1->1; between 3 and 5:1->1; after 5:0. miss_both=2. miss[3]=10, miss[4]=4. count = 15 - 10 - 4 + 2 = 3.
v=4: merge pos[4]=[3,5] and pos[5]=[] -> [3,5]. gaps: before 3:2->3; between 3 and 5:1->1; after 5:0. miss_both=4. miss[4]=4, miss[5]=15. count = 15 - 4 - 15 + 4 = 0.
Sum count = 4+2+3+0 = 9.

Answer = 32 - 9 = 23. Matches sample.

Sample 3: N=10, A=[5,1,10,9,2,5,6,9,1,6]. Expected 129. We can trust.

Thus algorithm is correct.

Now we need to implement efficiently in Python.

Potential pitfalls:
- N up to 3e5, so pos list of size N+1 is fine.
- Merging two lists: we can use two pointers. Since lists are sorted (we append in order of i), they are already sorted.
- We need to compute miss_v for all v. We can do that in a loop. But we also need to store miss_v for v=1..N. So we can create an array miss = [0]*(N+1). Fill it.
- Then for v in 1..N-1, compute miss_both by merging pos[v] and pos[v+1]. We can write a helper function to compute miss_both given two lists.

We need to be careful with large N and recursion? No recursion.

Time complexity: O(N + sum of lengths of pos) = O(N). Merging per v: total O(N). So overall O(N). Should be fast enough.

Now we need to write the code.

We should also consider that A_i can be up to N, but we only need pos up to N. So pos size N+1.

Edge case: N=1. Then v from 1 to N-1 is empty. sum_distinct: v=1, pos[1]=[1], miss_v: gaps: before 1:0, after 1:0 -> miss=0, cnt=1. sum_distinct=1. sum_adjacent=0. Answer=1. Let's compute manually: only subarray [1], f=1. Sum=1. Correct.

Edge case: all values same, e.g., A=[1,1,1]. N=3. total=6.
pos[1]=[1,2,3], miss_v: gaps: before 1:0, between 1 and 2:0, between 2 and 3:0, after 3:0 -> miss=0, cnt=6. sum_distinct=6.
v=1: merge pos[1] and pos[2] (pos[2] empty) -> miss_both = miss_v = 0. count = 6 - 0 - 6 + 0 = 0. sum_adjacent=0. Answer=6. Let's compute f: each subarray has distinct set {1}, components=1, so f=1 for each of 6 subarrays. Sum=6. Correct.

Edge case: values are 1,2,3,...,N. Then each subarray has distinct values equal to length, and all adjacent pairs present, so f = distinct_count - (length-1) = 1. So sum f = total. Let's compute: sum_distinct = sum over subarrays of distinct count. For a permutation of 1..N, distinct count = length. Sum of lengths over all subarrays = sum_{L,R} (R-L+1) = N*(N+1)*(N+2)/6? Actually sum of lengths = sum_{len=1}^N len * (N-len+1) = N(N+1)(N+2)/6. So sum_distinct = that. sum_adjacent: for each v, count_v = number of subarrays containing both v and v+1. Since v and v+1 are adjacent in the permutation, any subarray that includes both positions will contain both. The positions of v and v+1 are some indices. The number of subarrays containing both is (pos_v * (N - pos_{v+1} + 1)? Actually if pos_v < pos_{v+1}, then subarrays must start <= pos_v and end >= pos_{v+1}. So count = pos_v * (N - pos_{v+1} + 1). Sum over v. Then answer = sum_distinct - sum_adjacent. Should equal total. Let's test small N=2: A=[1,2]. total=3. sum_distinct: subarrays: [1]:1, [2]:1, [1,2]:2 -> sum=4. sum_adjacent: v=1: count subarrays containing both 1 and 2: only [1,2] ->1. Answer=4-1=3. Correct.

So algorithm works.

Now we need to implement.

Implementation details:

- Use sys.stdin.read to read fast.
- Parse N and array.
- Build pos: list of lists.
- Compute total.
- Initialize miss = [0]*(N+1).
- For v in range(1, N+1):
    lst = pos[v]
    if not lst:
        miss[v] = total
    else:
        m = 0
        prev = 0
        for p in lst:
            gap = p - prev - 1
            m += gap*(gap+1)//2
            prev = p
        gap = N - prev
        m += gap*(gap+1)//2
        miss[v] = m
- Compute sum_distinct = sum(total - miss[v] for v in range(1, N+1)).
- Compute sum_adjacent = 0.
- For v in range(1, N):
    # compute miss_both by merging pos[v] and pos[v+1]
    lst1 = pos[v]
    lst2 = pos[v+1]