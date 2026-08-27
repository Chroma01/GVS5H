
## ideation
We need to split the array A[1..N] into three non‑empty contiguous parts at positions i and j (1 ≤ i < j ≤ N‑1). For each split we compute the number of distinct values in each of the three subarrays and sum them. We want the maximum possible sum.

Observations:
- The count of distinct integers in a prefix (1..i) can be computed for all i in O(N) by scanning from left to right and using a frequency array (or set) to know when a new value appears.
- Similarly, the count of distinct integers in a suffix (j+1..N) can be computed for all j in O(N) by scanning from right to left.
- The middle subarray (i+1..j) also has its own distinct count. The problem reduces to choosing i and j to maximise:
  pref[i] + mid[i+1..j] + suff[j+1]
  where pref[i] = distinct count of A[1..i], suff[k] = distinct count of A[k..N].

A classic approach for the “harder” version (three subarrays) is to iterate over the middle split j and keep track of the best possible left split i ≤ j‑1. For a fixed j, the middle subarray is (i+1..j) for some i ≤ j‑1. However, the middle distinct count changes with i, so we cannot simply pre‑compute pref[i] + something independent of i.

We can rewrite the expression by fixing j (the right end of the middle subarray) and considering all possible i. For each i ≤ j‑1, the middle subarray distinct count is the distinct count of A[i+1..j]. This depends on both i and j, making a direct O(N²) enumeration too slow.

Alternative viewpoint: fix i (the left split) and j (the right split). The middle subarray is A[i+1..j]. Its distinct count can be computed if we pre‑compute for each pair? Not feasible.

Better approach: Use a sweeping technique similar to the “two subarrays” problem but extended. For the “two subarrays” problem (split into two non‑empty parts), we compute prefix distinct counts and then for each split point we combine with the suffix distinct count of the remaining part. That works because the second part starts at a fixed index.

For three subarrays, we can fix the middle split point j, and we need to choose i to maximise pref[i] + distinct(i+1..j). As we vary i from j‑1 down to 1, the middle subarray grows to the left. We can maintain the distinct count of the current middle subarray as we expand leftwards. This is like: for each j, start with middle = A[j] (distinct count = 1) and i = j‑1, then iteratively include A[i] into the middle, update its distinct count, and compute candidate = pref[i-1] + middle_distinct + suff[j+1]. But pref[i-1] is known. So we could loop i from j‑1 down to 1 for each j, which is O(N²).

We need a smarter way.

Observation: The total sum = distinct(1..i) + distinct(i+1..j) + distinct(j+1..N). We can think of it as:
total = distinct(1..i) + distinct(i+1..j) + suffix[j+1].

For each j, we want to maximise over i:
  f(i) = distinct(1..i) + distinct(i+1..j).

This is a function of i with j fixed. If we could compute for each i the distinct count of the segment (i+1..j) quickly, perhaps we can pre‑compute some data structure.

Note that distinct(1..i) is known from the prefix array. So we need to know for each j, the best value of distinct(1..i) + distinct(i+1..j) over i < j.

This is reminiscent of the “maximum sum of two distinct counts” problem. There is a known solution: iterate i from 1 to N, keep a data structure of prefix distinct counts, and for each j, we need the distinct count of the middle segment starting after i and ending at j. This seems like we need to support queries of distinct count in a range, which can be done with offline processing using BIT or segment tree? But we need to maximise over i for each j, not just query.

Alternate approach: iterate over the left split i, and for each i, we need to choose j > i to maximise distinct(i+1..j) + suffix[j+1]. This is similar to the previous but symmetric.

Maybe we can reduce to two‑pointer? Not obvious because distinct counts are not monotonic.

Another idea: Since N ≤ 3e5, we might be able to afford an O(N log N) solution using divide and conquer or segment tree. For each j, we need to find i that maximises pref[i] + distinct(i+1..j). This is like a DP: let dp[i] = pref[i] (distinct count of prefix up to i). For a fixed j, the middle segment distinct count is the number of distinct values in A[i+1..j]. This can be expressed as: total distinct in A[1..j] minus distinct in A[1..i] plus (number of values that appear in both A[1..i] and A[i+1..j])? Not exactly, because distinct count of union minus intersection.

Actually, distinct(1..j) = distinct(1..i) + distinct(i+1..j) - common(i, j), where common(i, j) is the number of values that appear in both prefixes (i.e., values that appear in A[1..i] and also in A[i+1..j]). So:
distinct(i+1..j) = distinct(1..j) - distinct(1..i) + common(i, j).
Therefore:
pref[i] + distinct(i+1..j) = pref[i] + (distinct(1..j) - pref[i] + common(i, j)) = distinct(1..j) + common(i, j).
So the sum for a fixed j and i < j is:
total = distinct(1..j) + common(i, j) + suffix[j+1].

Wow! That simplifies a lot. Let's verify:
pref[i] = distinct(1..i).
distinct(1..j) = number of distinct values in A[1..j].
common(i, j) = number of values that appear in A[1..i] and also in A[i+1..j]. Note that a value v is counted in common if its first occurrence? Actually, any value that appears in both parts contributes. Since the union of the two parts is exactly A[1..j], and the intersection is the set of values that appear in both the prefix and the suffix of the split i. So indeed:
distinct(1..j) = distinct(1..i) + distinct(i+1..j) - |common(i, j)|.
Thus distinct(i+1..j) = distinct(1..j) - distinct(1..i) + |common(i, j)|.
Plugging into pref[i] + distinct(i+1..j) = pref[i] + distinct(1..j) - pref[i] + common = distinct(1..j) + common(i, j).

Therefore the total sum for a split at i and j is:
total(i, j) = distinct(1..j) + common(i, j) + suffix[j+1].

Here suffix[j+1] = distinct(A[j+1..N]).

For a fixed j, distinct(1..j) and suffix[j+1] are constants. So we need to maximise common(i, j) over i < j. common(i, j) is the number of distinct values that appear in A[1..i] and also in A[i+1..j]. Equivalently, it's the number of distinct values in the set of values that have at least one occurrence in A[1..i] and at least one occurrence in A[i+1..j].

But we can also think of it as: for each value v, if v appears in A[1..i] and also appears after position i up to j, then v contributes 1 to common(i, j). So for a fixed j, as i decreases, the set of values in A[1..i] grows, and the set of values in A[i+1..j] shrinks. common(i, j) is the size of the intersection of the two sets.

We need to find i < j that maximises this intersection size. This is a classic problem: given an array, and a fixed j, we want the prefix i (1 ≤ i < j) that has the largest intersection with the suffix i+1..j.

This can be solved by scanning i from left to right while maintaining the set of values seen so far. For a fixed j, we can precompute the distinct values in the suffix? But the suffix changes with i.

Alternative viewpoint: For each j, we can compute the maximum over i of common(i, j) efficiently if we process j in increasing order. As j moves right, the set of values in the right part (i+1..j) changes. Perhaps we can maintain a data structure that for each i gives the current common(i, j) and we update it as j increases.

Let's define for each i (1 ≤ i < j) the value c_i = |values that appear in A[1..i] and also in A[i+1..j]|. When we move j to j+1, we add a new element A[j+1] to the right part. This can affect c_i for some i: specifically, if A[j+1] already appears in A[1..i] and we haven't seen it in the right part before? Actually, the right part for i is A[i+1..j+1]. Adding a new element v = A[j+1] will increase the intersection size c_i by 1 if v is present in A[1..i] but was not previously in A[i+1..j]. However, if v was already in A[i+1..j], then c_i does not change because the value is already counted. But we need to know if v was already in the right part for that i. This seems complicated.

Maybe there's another simplification. Since the total is distinct(1..j) + suffix[j+1] + common(i, j), and distinct(1..j) and suffix[j+1] are known for each j, we just need the maximum common(i, j) over i < j. This maximum is simply the number of distinct values in A[1..j-1] that also appear in A[j]? Not exactly. Let's test with a small example.

Consider A = [1,2,1]. N=3. Possible splits: only (i=1, j=2). Pref(1)=1 (value 1). Middle (2..2)=1 (value 2). Suffix(3..3)=1 (value 1). Sum=3. Our formula: j=2: distinct(1..2)=2 (1,2). suffix[3]=1. common(1,2): values in A[1..1]={1} and A[2..2]={2} → intersection empty, size 0. Total=2+1+0=3. Good.

Now for A = [1,2,1,2]. N=4. Splits: (1,2), (1,3), (2,3). Compute:
- (i=1,j=2): pref(1)=1, mid(2..2)=1 (2), suff(3..4)=2 (1,2) → sum=4.
- (i=1,j=3): pref(1)=1, mid(2..3)=2 (2,1), suff(4)=1 (2) → sum=4.
- (i=2,j=3): pref(2)=2 (1,2), mid(3..3)=1 (1), suff(4)=1 (2) → sum=4.
Max=4. Let's compute via formula for each j:
j=2: distinct(1..2)=2, suffix[3]=2 (1,2). common(1,2): A[1..1]={1}, A[2..2]={2} → 0. Total=2+2+0=4.
j=3: distinct(1..3)=2 (1,2), suffix[4]=1 (2). For i=1: A[1..1]={1}, A[2..3]={2,1} → intersection {1} size 1. For i=2: A[1..2]={1,2}, A[3..3]={1} → intersection {1} size 1. Max common=1. Total=2+1+1=4. So answer=4.

Note that for j=3, common(i,j) is 1 for both i=1 and i=2. Interesting.

Now, is there a way to compute max_{i<j} common(i,j) quickly? This is the size of the largest intersection between a prefix of the array (up to i) and the subarray from i+1 to j. This is similar to the problem of finding the maximum number of "shared" values across the boundary at position i for a fixed j. Alternatively, we can think of it as: for each value v, consider the set of positions where it occurs. For a given j, the value v contributes to common(i,j) if there is at least one occurrence of v in A[1..i] and at least one occurrence in A[i+1..j]. For a fixed v, the set of i such that v contributes is: i must be at least the first occurrence of v, and also i must be at least the first occurrence of v in the prefix? Actually, let first occurrence of v be pos_v. For i < pos_v, A[1..i] does not contain v, so v does not contribute. For i >= pos_v, A[1..i] contains v. But we also need v to appear in A[i+1..j]. That means there must be an occurrence of v in the interval (i, j]. So i must be less than the last occurrence of v that is ≤ j. In other words, for a fixed j, v contributes to common(i,j) if and only if the first occurrence of v (call it L) is ≤ i and there is an occurrence of v in (i, j]. That is equivalent to: i is in the range [L, last_occurrence_of_v_up_to_j - 1]? Actually, we need an occurrence after i and ≤ j. So the maximum i for which v contributes is the position just before the last occurrence of v in [1..j]. So v contributes to common(i,j) for all i such that L ≤ i < last_occurrence_of_v_up_to_j.

Thus, for each value v, if we know the last occurrence of v up to j (call it last_v(j)), then v contributes to common(i,j) for all i in [first_v, last_v(j)-1]. So the total common(i,j) is the number of distinct values v for which first_v ≤ i < last_v(j). In other words, it's the count of values whose first occurrence is ≤ i and whose last occurrence up to j is > i.

This is a known problem: for a fixed j, we want to find i that maximises the number of values that "cross" the boundary at i (i.e., have first occurrence ≤ i and last occurrence in [1..j] > i). This is exactly the same as in the two‑subarray problem where we split into two parts and we want the maximum sum of distinct counts: there we used the same insight: total = distinct(1..N) + common(i,N) and we needed the maximum common(i,N). The solution was to iterate i from left to right, keep a set of values that have appeared, and for each i, the number of values that have their last occurrence > i? Actually, in the two‑subarray split, we fixed the split point i, and the second part is from i+1 to N. The sum is distinct(1..i) + distinct(i+1..N) = distinct(1..N) + common(i,N). The maximum over i of common(i,N) is the maximum number of values that appear on both sides of i. The solution is: for each i, common(i,N) = number of values whose first occurrence ≤ i and last occurrence > i. This is computed by precomputing first and last occurrences, and then for each i, counting how many values have first ≤ i and last > i. This can be done by sorting first occurrences and last occurrences, or using a sweepline.

But here j is not fixed at N; j varies. So for each j, we need to compute the maximum over i of common(i,j). This is like: for each j, we consider the prefix of the array up to j, and we want the maximum number of values that have first occurrence ≤ i and last occurrence in [1..j] > i. This is a classic problem that can be solved by iterating i from 1 to j-1 and maintaining a count, but we need to do it for all j efficiently.

Observing that as j increases, the last occurrence of each value updates. The condition last_v(j) > i: last occurrence of v up to j is the last position ≤ j where v appears. As j increases, last_v(j) may increase. For a fixed i, common(i,j) is the number of v such that first_v ≤ i < last_v(j). So as j increases, if a new occurrence of v appears at position j, and v's last occurrence was previously ≤ i, then after updating, last_v(j) becomes j which is > i, so v now contributes to common(i,j). Conversely, if v's last occurrence was already > i, it continues to contribute. If v's last occurrence was ≤ i and no new occurrence at j, it still doesn't contribute.

Thus, for a fixed i, common(i,j) is non‑decreasing as j increases (because last_v(j) only increases). So the function f_i(j) = common(i,j) is monotonic non‑decreasing in j. However, we are interested in max_{i<j} common(i,j). For a fixed j, we want the best i. This is like we have a set of functions f_i(j) and we want the maximum over i of f_i(j) for each j. Since each f_i is monotonic, the maximum over i is also monotonic? Not necessarily, because as j increases, the best i might change.

We can try to compute the answer by iterating j from 2 to N-1, and for each j, we want to compute the maximum of common(i,j) over i < j. This is equivalent to: for each j, consider the array of length j-1 (positions i=1..j-1), and we assign to each i the value common(i,j). We need the max of that array. If we can maintain these values as j increases, we can update the max in O(1) amortised.

Let's try to maintain for each i (1 ≤ i < j) the value common(i,j) as we increment j. When we move from j to j+1, we add the new element A[j+1] to the right part. How does this affect common(i,j+1) for each i < j+1?

We have two cases for i:
- For i ≤ j, the right part for i is A[i+1..j+1]. The new element is at position j+1. The change in common(i, *) is determined by whether the new element's value, call it v = A[j+1], is present in the left part (A[1..i]) and whether it was already present in the right part (A[i+1..j]). Since the right part expanded by one element, the intersection size increases by 1 if and only if v is in the left part and was not previously in the right part. But "was not previously in the right part" means that the last occurrence of v up to j is ≤ i (i.e., v did not appear in A[i+1..j]). Because if v appeared in A[i+1..j], then it was already in the right part, so the intersection already includes v; adding another occurrence of v does not change the distinct set. However, careful: the intersection is about distinct values, not about occurrences. So if v is already in the right part, its contribution is already counted; adding another occurrence does not change the distinct count of the right part, so the intersection size remains the same. If v is not in the right part, but is in the left part, then adding v to the right part increases the distinct count of the right part by 1, and since v is in the left part, the intersection size increases by 1.

Thus, for each i, the new common(i,j+1) = common(i,j) + 1 if v is in A[1..i] and v is not in A[i+1..j]; otherwise it stays the same. Note that "v is not in A[i+1..j]" is equivalent to last_occurrence_of_v_up_to_j ≤ i. Because if the last occurrence of v up to j is ≤ i, then v does not appear in (i, j]. If it is > i, then v appears in A[i+1..j].

So the update rule: for a fixed j and new element v = A[j+1], for each i from 1 to j, we add 1 to common(i) if (i >= first_occurrence_of_v?) Wait, the condition "v is in A[1..i]" means i must be at least the first occurrence of v, say L. Also, the condition "v is not in A[i+1..j]" means i must be at least the last occurrence of v up to j, say last_j. Actually, v is not in A[i+1..j] if and only if the last occurrence of v up to j is ≤ i. So we need i >= last_occurrence_of_v_up_to_j? No, if last_occurrence ≤ i, then v does not appear after i up to j. But we also need v to be in A[1..i], so i must be at least the first occurrence L. So the condition for incrementing common(i) is: i >= L and i >= last_occurrence_of_v_up_to_j? Wait, if i >= last_occurrence, then v's last occurrence is ≤ i, meaning v does not appear in (i, j]. That is correct. But we also need i >= L to have v in the left part. However, note that L is the first occurrence, so if i >= last_occurrence, then automatically i >= L? Not necessarily: last_occurrence could be after L, but if i is between L and last_occurrence, then v appears in the left part, but also appears in the right part because its last occurrence is > i. So in that case, v is already in the right part, so adding v at j+1 (which is after the last occurrence? Wait, the new element is at j+1, which is > last_occurrence? Actually, the last occurrence up to j is some position ≤ j. The new occurrence is at j+1, so it's after that. So if last_occurrence ≤ i, then the new occurrence is definitely > i, so it adds a new occurrence to the right part. But if last_occurrence > i, then v already appears in A[i+1..j], so the new occurrence does not add a new distinct value to the right part.

Thus, the condition for incrementing common(i) is: i < last_occurrence_of_v_up_to_j? Let's check: if i < last_occurrence, then v appears in A[i+1..j] (since there is an occurrence at last_occurrence which is > i and ≤ j). So the right part already contains v, so no increase. If i >= last_occurrence, then v does not appear in A[i+1..j], so adding v at j+1 introduces v to the right part, increasing the intersection by 1 provided v is in the left part (i.e., i >= L). So the condition is: i >= L and i >= last_occurrence? Wait, if i >= last_occurrence, then v is not in the right part. But we also need v to be in the left part. Since last_occurrence >= L, if i >= last_occurrence, then automatically i >= L. So the condition reduces to i >= last_occurrence_of_v_up_to_j. But careful: what if last_occurrence = 0 (v hasn't occurred yet)? Then for all i, v is not in the left part, so no increase. So the update is: for all i in the range [last_occurrence, j] (since i can be up to j, because i < j+1, and we consider i from 1 to j), we increment common(i) by 1, provided that last_occurrence is defined (i.e., v has appeared at least once up to j). However, we also need to ensure that i is at least the first occurrence? But as argued, if i >= last_occurrence, then i >= first_occurrence automatically. So indeed, the range of i that get incremented is from last_occurrence to j (inclusive). But wait, i can be exactly last_occurrence? If i = last_occurrence, then v is in the left part (since its occurrence is at i), and it is not in the right part because the right part starts at i+1. So yes, i = last_occurrence should get incremented. So the range is [last_occurrence, j].

But is that always correct? Let's test with an example. A = [2, 1, 2]. N=3.
j=1: we don't consider.
j=2: (i must be < j, so i=1). common(1,2): left {2}, right {1} → 0.
Now j=2, we want to update to j=3 by adding A[3]=2.
Last occurrence of 2 up to j=2: positions: A[1]=2, A[2]=1, so last occurrence of 2 is 1. So we should increment common(i) for i in [1, 2]? But i can only be 1 (since i < j+1=3, but we consider i up to j=2 for the new j+1? Actually, when we move to j+1, the valid i are those < j+1, so i=1,2. For i=1: i >= last_occurrence (1 >= 1) → increment. For i=2: i >= last_occurrence (2 >= 1) → increment. But wait, for i=2, the left part is A[1..2] = {2,1}, right part for i=2 is A[3..3] = {2}. The new element is added to the right part? Actually, when we increase j to 3, the right part for i=2 is A[3..3], which includes the new element. So before the update (j=2), the right part for i=2 would be empty (since i=2, j=2, so right part is A[3..2]? That's not valid. Actually, when j=2, the right part is from i+1 to j. For i=2, j=2, the right part is A[3..2] which is empty, but we only consider i < j, so for j=2, i can only be 1. So the common(i) values for j=2 are only defined for i=1. For j=3, i can be 1 or 2. So when we transition from j=2 to j=3, we need to compute common(i,3) for i=1,2. The update rule from j=2 to j=3: the new element v=A[3]=2. For i=1: left {2}, right before update (A[2..2]) = {1}. After update, right becomes A[2..3] = {1,2}. So intersection becomes {2}? Actually, left {2}, right {1,2} → intersection {2} size 1. Before, intersection was 0. So increased by 1. For i=2: left {2,1}, right before update (A[3..2]) empty. After update, right becomes A[3..3]={2}. Intersection: left has 2, right has 2 → size 1. Before it was 0. So both increased by 1. According to our rule, last_occurrence of 2 up to j=2 is 1. So we increment for i in [1, 2]. That matches.

But wait, for i=2, the condition i >= last_occurrence holds (2>=1), but also we need i to be a valid i (< j+1=3). So i=2 is valid. So the range is [last_occurrence, j] where j is the old j (the one before update). In the update, j is the current j (before increment), and we consider i from 1 to j. So the range is [last_occurrence, j]. But is it always [last_occurrence, j]? Let's test with another example: A = [1, 2, 1]. j=2: i=1, common(1,2)=0. Now j=2 to j=3: v=A[3]=1. Last occurrence of 1 up to j=2: A[1]=1, A[2]=2, so last_occurrence=1. Range: [1,2]. For i=1: i=1 >=1, increment. For i=2: i=2 >=1, increment. Let's compute manually: j=3, i=1: left {1}, right A[2..3]={2,1} → intersection {1} size 1. Before: 0. So +1. i=2: left {1,2}, right A[3..3]={1} → intersection {1} size 1. Before: for i=2, j=2, right part A[3..2] empty, intersection 0. So +1. Works.

What if the new element v has not occurred before? Then last_occurrence is 0 (or undefined). Then no i gets incremented. That makes sense: if v is new, it's not in any left part, so intersection doesn't increase.

But is it sufficient to just check last_occurrence? Consider the case where v has occurred before, but the last occurrence is after the left part? For example, A = [1, 2, 1]. j=2, v=A[3]=1. last_occurrence=1. For i=1, left contains 1, right does not contain 1 (since right is A[2..2]={2}), so increment. For i=2, left contains 1 (since A[1..2] contains 1), but right is empty, so increment. That matches.

But what about a case where v has occurred before, and its last occurrence is before the left part? That's impossible because if last occurrence is before i, then v is not in the left part, so no increment. So our condition i >= last_occurrence ensures that v is in the left part? Not exactly: if i >= last_occurrence, it could be that i is between the first occurrence and the last occurrence? Actually, if i >= last_occurrence, then the last occurrence is ≤ i, so all occurrences are ≤ i, so v is in the left part. So yes.

Thus, the update rule seems correct: when we add a new element v at position j+1, we need to increment common(i) for all i in the range [last_occurrence_of_v_up_to_j, j] (where j is the old j). But wait, we also need to consider that i must be at least 1. And what if last_occurrence is 0? Then no increment.

But is it exactly that range? Let's test a more complex case. A = [1, 2, 3, 1, 2]. Consider j=4 (so we are at position 4, and we will add A[5]=2). For j=4, the valid i are 1,2,3. Let's compute common(i,4) for each i manually:
- i=1: left {1}, right A[2..4]={2,3,1} → intersection {1} size 1.
- i=2: left {1,2}, right A[3..4]={3,1} → intersection {1} size 1.
- i=3: left {1,2,3}, right A[4..4]={1} → intersection {1} size 1.
Now add v=2 at j=5. last_occurrence of 2 up to j=4 is at position 2 (A[2]=2). So range: [2,4]. We increment common(2), common(3), common(4)? But i=4 is not valid for j=4? Actually, when we move to j=5, the valid i are 1..4. So for the new j=5, we need common(i,5) for i=1..4. The update from j=4 to j=5 affects i=1..4. For i=1: left {1}, right A[2..5]={2,3,1,2} → intersection {1} size 1. So no change. For i=2: left {1,2}, right A[3..5]={3,1,2} → intersection {1,2} size 2. Previously size 1, so +1. For i=3: left {1,2,3}, right A[4..5]={1,2} → intersection {1,2} size 2. Previously size 1, so +1. For i=4: left {1,2,3,1} = {1,2,3}, right A[5..5]={2} → intersection {2} size 1. Previously for i=4, j=4, common(4,4) was? Actually, for j=4, i=4 is not valid because i < j, so i=4 is not considered. But when we move to j=5, i=4 becomes valid. So we need to initialise common(4,5). According to our update rule, we increment common(i) for i in [2,4] because last_occurrence=2 and j=4. So for i=4, we increment. But what was the previous value for i=4? It was 0 (since it didn't exist). After increment, it becomes 1. That matches the manual calculation: intersection size 1. So the rule works if we consider that common(i) for i=j is initialised to 0, and then we add the increment.

But wait, in the range [last_occurrence, j], we are including i=j. But i=j is the split where the middle subarray is empty? Actually, for a fixed j, we consider i < j. So i=j is not a valid split. However, when we update to j+1, the new j becomes j+1, and the new valid i are up to j. So i=j is now valid for the new j. So we need to include i=j in the update because it becomes a valid split for the next step. In the example, i=4 was not valid for j=4, but becomes valid for j=5. So the range should be [last_occurrence, j] where j is the old j. That includes i=j, which will be used in the next iteration.

Thus, the update is: for each new element v at position j+1, let last = last occurrence of v up to j. Then for all i from last to j (inclusive), we do common[i] += 1. This is a range increment.

But wait, is that sufficient? Let's test with a case where the new element v is already present in the right part for some i, but not for others. Consider A = [1, 2, 1, 2]. j=2: valid i=1, common(1,2)=0. Now add A[3]=1. last occurrence of 1 up to j=2 is 1. Range [1,2]: increment common(1) and common(2). For i=1: becomes 1. For i=2: becomes 1? But common(2,3) for i=2: left {1,2}, right A[3..3]={1} → intersection {1} size 1. So yes. Now j=3 to j=4: add A[4]=2. last occurrence of 2 up to j=3: A[2]=2, A[3]=1, so last=2. Range [2,3]: increment common(2) and common(3). For i=2: previous common(2,3)=1, becomes 2. For i=3: previous common(3,3) didn't exist, becomes 1. Let's compute manually for j=4:
- i=1: left {1}, right A[2..4]={2,1,2} → intersection {1} size 1. So common(1,4)=1.
- i=2: left {1,2}, right A[3..4]={1,2} → intersection {1,2} size 2.
- i=3: left {1,2,1}={1,2}, right A[4..4]={2} → intersection {2} size 1.
So our updates gave: common(1) was 1 (from previous step), no update for i=1 because last=2 > 1, so stays 1. common(2) was 1, incremented to 2. common(3) was 0, incremented to 1. Matches.

What about i=1 in the last step? Did we need to increment? For i=1, last=2, so i=1 < 2, so no increment. Correct.

So the update rule seems correct: when we process position j from 2 to N-1, we have an array common[1..j] (where common[i] = common(i,j) for i=1..j, with the understanding that for i=j, it corresponds to the split where the middle subarray is just A[j]? Actually, for a fixed j, i can be j? No, i < j. But in our array we include i=j as a placeholder that will be used when j increases. So we can maintain an array common[1..N] of size N, where for the current j, the valid values are common[1..j-1], and common[j] is a temporary value that will become valid for the next j. But it's easier to think of common[i] as the value for the current j, and we will compute the answer for the current j as max_{i=1..j-1} common[i] + distinct(1..j) + suffix[j+1]. But careful: the formula for total is distinct(1..j) + suffix[j+1] + common(i,j). So for each j, we need max over i < j of common(i,j). So we can maintain the maximum of common[1..j-1] as we update.

So algorithm:
1. Compute prefix distinct counts: pref[i] = number of distinct values in A[1..i]. Also we can compute distinct(1..j) for any j (which is just pref[j]).
2. Compute suffix distinct counts: suff[k] = number of distinct values in A[k..N] for k=1..N+1. suff[N+1]=0.
3. We will iterate j from 2 to N-1. For each j, we need max_{i < j} common(i,j). We can maintain an array cur_common[i] for i=1..j (with cur_common[j] being a dummy that will be used in the next step). Initially, for j=2, we have only i=1. We can compute cur_common[1] directly: common(1,2) = number of values in A[1..1] and A[2..2] that are the same. That's 1 if A[1]==A[2] else 0. So we can initialise.
But for general j, we can update from j-1 to j using the range increment idea. However, note that the update depends on the new element A[j] (since we are moving from j-1 to j). Actually, when we increment j to j+1, the new element is A[j+1]. So for iteration j, we need to have the cur_common array corresponding to j. We can start with j=2, compute cur_common[1] manually, then for j from 3 to N-1, we update from j-1 to j using the new element A[j].

But careful: The update rule we derived is: when adding the new element v = A[j] (at position j), we need to know the last occurrence of v up to j-1. Then we increment cur_common[i] for i in [last, j-1]. And we also need to initialise cur_common[j] for the new i = j-1? Actually, when we move to j, the valid i are 1..j-1. So we need cur_common[i] for i=1..j-1. The update from j-1 to j will give us new values for i=1..j-1. Also, we need a value for i=j-1? Wait, when we move to j, the largest i is j-1. In the previous step (j-1), the largest valid i was j-2. So we need to have a value for i=j-1. In the update, we are incrementing a range that includes i = j-1? Because the range is [last, j-1] (since old j is j-1). So if last <= j-1, then i=j-1 gets incremented. But what is the base value of cur_common[j-1] before the update? It was not defined (or 0) because it wasn't a valid i in the previous step. So we need to ensure that before applying the increment, cur_common[j-1] is 0. So we can initialise the array with zeros, and then for each j, after updating, we have cur_common[1..j-1] correct.

Let's test this with the earlier example: A = [2, 1, 2]. N=3.
j=2: we need cur_common[1]. Compute manually: common(1,2)=0. So cur_common = [0, 0, ...] (index 1 is 0). Then j=2 to j=3? But we only iterate j up to N-1=2? Actually, N=3, so j=2 is the only j. But we need to update to compute for j=2? The iteration is for j from 2 to N-1. For j=2, we need the maximum over i<2 of common(i,2). That's just cur_common[1]. So we can compute that without any update. So for N=3, it's simple. But for larger N, we need to update.

Let's test with A = [1,2,1,2,3]. N=5. We want to compute for j=2,3,4.
j=2: cur_common[1] = common(1,2). A[1]=1, A[2]=2, different → 0.
Now we want to move to j=3. The new element is A[3]=1. last occurrence of 1 up to j=2 is 1. So we increment cur_common[i] for i in [1, 2] (since j-1=2). So cur_common[1] += 1 → becomes 1. cur_common[2] is new (was 0) becomes 1. Now for j=3, the valid i are 1,2. cur_common[1]=1, cur_common[2]=1. So max common = 1. Total = distinct(1..3) + suffix[4] + max_common. distinct(1..3) = 2 (1,2). suffix[4] = distinct(A[4..5]) = {2,3} = 2. So total = 2+2+1=5. Let's check manually: splits: (i=1,j=2): pref(1)=1, mid(2..2)=1, suff(3..5)=3 (1,2,3) → sum=5. (i=1,j=3): pref(1)=1, mid(2..3)=2, suff(4..5)=2 → sum=5. (i=2,j=3): pref(2)=2, mid(3..3)=1, suff(4..5)=2 → sum=5. So max=5. Good.

Now j=3 to j=4: new element A[4]=2. last occurrence of 2 up to j=3: A[2]=2, A[3]=1, so last=2. Increment cur_common[i] for i in [2, 3] (j-1=3). So cur_common[2] += 1 → becomes 2. cur_common[3] is new (0) becomes 1. cur_common[1] unchanged (1). Now for j=4, valid i=1,2,3. cur_common = [1,2,1]. max common = 2. Total = distinct(1..4) + suffix[5] + 2. distinct(1..4) = 3 (1,2). suffix[5] = distinct(A[5..5]) = 1 (3). So total = 3+1+2=6. Check manually: splits: (1,2): pref1=1, mid2=1, suff3..5=3 → 5. (1,3): pref1=1, mid2..3=2, suff4..5=2 → 5. (1,4): pref1=1, mid2..4=3 (2,1,2? actually distinct {2,1}=2), suff5=1 → 1+2+1=4. (2,3): pref2=2, mid3=1, suff4..5=2 → 5. (2,4): pref2=2, mid3..4=2, suff5=1 → 5. (3,4): pref3=2, mid4=1, suff5=1 → 4. Max=5? Wait, we got 6 from formula. Something is off. Let's recompute common for j=4 manually:
- i=1: left {1}, right A[2..4]={2,1,2} → intersection {1} size 1.
- i=2: left {1,2}, right A[3..4]={1,2} → intersection {1,2} size 2.
- i=3: left {1,2,1}={1,2}, right A[4..4]={2} → intersection {2} size 1.
So max common = 2. distinct(1..4) = 3. suffix[5] = 1. Total = 3+1+2=6. But manual splits for j=4 give: (1,4): 1+2+1=4, (2,4): 2+2+1=5, (3,4): 2+1+1=4. None gives 6. Where is the discrepancy? The formula is total = distinct(1..j) + common(i,j) + suffix[j+1]. For j=4, distinct(1..4)=3, suffix[5]=1. For i=2, common(2,4)=2, so total=3+1+2=6. But manual calculation for (i=2,j=4): pref(2)=2, mid(3..4)=2, suffix(5)=1, sum=5. So why the formula gives 6? Let's check the derivation: total = pref(i) + distinct(i+1..j) + suffix(j+1). We expressed distinct(i+1..j) = distinct(1..j) - pref(i) + common(i,j). So total = pref(i) + distinct(1..j) - pref(i) + common(i,j) + suffix(j+1) = distinct(1..j) + common(i,j) + suffix(j+1). For i=2, j=4: distinct(1..4)=3, common(2,4)=2, suffix[5]=1, sum=6. But pref(2)=2, distinct(3..4)=2, suffix(5)=1, sum=5. So 2+2+1=5, not 6. So the formula seems to overestimate by 1. Where is the error? Let's compute common(2,4) carefully. common(2,4) is the number of distinct values that appear in both A[1..2] and A[3..4]. A[1..2] = {1,2}. A[3..4] = {1,2}. So common = 2. Then distinct(1..4) = 3 (1,2). So distinct(1..4) = pref(2) + distinct(3..4) - common = 2+2-2=2? That's not 3. Actually, the formula distinct(1..j) = pref(i) + distinct(i+1..j) - |intersection| holds only if the intersection is counted correctly. But here, pref(i) counts distinct in A[1..i], distinct(i+1..j) counts distinct in A[i+1..j]. The union is A[1..j], and the intersection is the set of values that appear in both. So |A[1..j]| = |A[1..i]| + |A[i+1..j]| - |intersection|. For i=2, j=4: |A[1..4]| = 3, |A[1..2]| = 2, |A[3..4]| = 2, intersection = {1,2} size 2. So 2+2-2=2, not 3. So the formula is wrong. Why? Because the sets A[1..i] and A[i+1..j] are not necessarily disjoint. Their union is A[1..j], but the intersection is the set of values that appear in both. However, the formula for union size is |A| + |B| - |A ∩ B|. That is correct. So |A[1..j]| = 2+2-2=2, but actually |A[1..4]|=3. So there is a contradiction. That means that for i=2, j=4, the sets A[1..2] and A[3..4] are not covering A[1..4] completely? They do: A[1..2] = {1,2}, A[3..4] = {1,2}. Their union is {1,2}, not {1,2,3}? But A[1..4] contains 1,2, and also 1,2, but wait, A[1..4] = [1,2,1,2]? No, the array is [1,2,1,2,3]. So A[1..4] = [1,2,1,2]. The distinct values in A[1..4] are {1,2}, not 3! I made a mistake: A = [1,2,1,2,3], so A[1..4] = [1,2,1,2], distinct = {1,2} = 2, not 3. I earlier said distinct(1..4)=3, but it's 2. Let's recalc: A[1]=1, A[2]=2, A[3]=1, A[4]=2, A[5]=3. So distinct(1..4) = 2. Then total for i=2,j=4: distinct(1..4)=2, common(2,4)=2, suffix[5]=1, total=5. That matches manual. So the formula is correct.

So the algorithm is:
- Compute pref[i] = distinct count of A[1..i].
- Compute suff[i] = distinct count of A[i..N] for i=1..N+1, with suff[N+1]=0.
- We will iterate j from 2 to N-1. For each j, we need to compute the maximum over i < j of common(i,j). We can maintain an array cur_common of size N+1, initialised to 0. We'll also keep track of the last occurrence of each value. Since A_i ≤ N, we can use an array last_occurrence of size N+1, initialised to 0.
- For j=2, we compute cur_common[1] directly: if A[1]==A[2] then 1 else 0. Actually, common(1,2) = 1 if A[1]==A[2], else 0. But we can also compute it using the update rule if we start from j=1? But j starts at 2. Alternatively, we can start with j=1 as a base, but j=1 is not a valid split because we need i < j, so j must be at least 2. So we can initialise for j=2 by computing cur_common[1] manually.
But to make it uniform, we can start with j=1 having cur_common[1] = 0 (since for j=1, there is no i < 1). Then when we move to j=2, we update using the new element A[2]. But careful: the update rule we derived assumes we are moving from j-1 to j, and the new element is A[j]. For j=2, the new element is A[2]. The last occurrence of A[2] up to j-1=1 is last_occurrence[A[2]] (which is 0 if A[2] hasn't appeared). So we would increment cur_common[i] for i in [last, 1] (since j-1=1). If last=0, no increment. So cur_common[1] remains 0. But we need it to be 1 if A[1]==A[2]. So that doesn't work. So we need to handle the base case separately, or adjust the update rule for the first step.

Maybe the update rule is slightly different for the first element? Let's derive the update from j=1 to j=2. For j=1, we have only i=1? But i < j, so no i. We are defining cur_common[i] for i=1..j-1. For j=1, there are no i. When we go to j=2, we need cur_common[1] = common(1,2). How to compute it using the update idea? We can think of the array cur_common as representing the common counts for the current j, and we update it when we add a new element at the end. The update rule we derived was: for each i, cur_common[i] increases by 1 if the new element v is in A[1..i] and not in A[i+1..j-1]. But for j=2, the right part for i=1 is A[2..2] (the new element itself). Before adding, the right part was empty. So the condition is: v is in A[1..1] and not in empty (always true). So if v == A[1], then cur_common[1] increases by 1. But initially cur_common[1] is 0, so it becomes 1. If v != A[1], it stays 0. So the rule works if we consider that the right part before adding is A[i+1..j-1], which for j=2 and i=1 is A[2..1] = empty. So the condition "v is not in A[i+1..j-1]" is vacuously true. And "v is in A[1..i]" is true if A[1]==v. So we need to increment if A[1]==v. That matches.

In our earlier general update, we used last occurrence of v up to j-1. For j=2, j-1=1. last occurrence of v up to 1 is 1 if v == A[1], else 0. So the range is [last, 1]. If last=1, we increment i=1. If last=0, no increment. So it works! So we can start with j=1, with cur_common array of size N+1 initialised to 0, and then for j from 2 to N-1, we do the update with new element A[j], using last occurrence of A[j] up to j-1. But we need to have last_occurrence updated as we go.

But wait: for j=1, we don't have any valid i, so we don't compute an answer. We start with j=2 after updating. So the algorithm:
- Initialise last_occurrence array of size N+1 to 0.
- Initialise cur_common array of size N+1 to 0.
- For j from 2 to N-1:
    - v = A[j]
    - last = last_occurrence[v]
    - If last > 0:
        - For i from last to j-1: cur_common[i] += 1
      But we cannot do this naively for each j because j can be up to 3e5, and doing a loop over the range for each j would be O(N^2) in the worst case. We need a more efficient way to perform the range increment.

We need to support: for each j, add 1 to cur_common[i] for i in [last, j-1]. This is a range add on an array. We can use a difference array technique: maintain an array diff such that cur_common[i] is the prefix sum of diff up to i. When we add 1 to a range [L, R], we can do diff[L] += 1, diff[R+1] -= 1. Then after processing all updates, we can compute cur_common by taking prefix sums. But here, the updates are happening sequentially, and we need the current values of cur_common for each j to compute the maximum. We could use a Fenwick tree (BIT) to support range add and point query, or range add and range max? Actually, we need the maximum over i < j of cur_common[i] for each j. So we need to maintain a data structure that supports:
- Range add on [L, R] (where R = j-1, L = last)
- Query maximum over all i (or over i < j? Actually, for a fixed j, we need max over i=1..j-1. So we need the maximum over the first j-1 elements.

We can use a segment tree that supports range add and range max query. Alternatively, we can use two Fenwick trees: one for the values and one for the maximum? Actually, we can maintain the maximum easily if we use a segment tree with lazy propagation for range add and range max. Since N is up to 3e5, a segment tree is fine.

But maybe we can avoid the segment tree by using an array and a prefix sum to get the values, and then compute the maximum in O(j) for each j? That would be O(N^2). We need O(N log N) or O(N).

Observing that the range we update is always a suffix: from last to j-1. That is, we are adding 1 to all elements from some index last to the end (j-1). This is like we have an array, and we perform operations: add 1 to all elements from last to current_end. We also need to know the maximum of the array. This can be done using a data structure that maintains a set of indices with their values, and we can update ranges. Alternatively, we can think of it as: each time we add 1 to a suffix, the values of indices from last to j-1 increase by 1. This is similar to the "array manipulation" problem where we have operations of adding to suffixes, and we need the maximum. We can use a binary indexed tree to store the differences, and then we can compute the actual values by taking prefix sums. But to get the maximum, we might need to maintain additional information.

Maybe we can reformulate: we are maintaining an array cur_common[1..N] (though we only care up to j-1). Initially all zeros. For each j from 2 to N-1, we add 1 to indices from last to j-1. After adding, we need the maximum of cur_common[1..j-1]. We can maintain a multiset of the values? But when we add to a range, the values of many elements change, so updating a multiset would require updating each element, which is slow.

We need a data structure that supports range addition and range maximum query. A segment tree with lazy propagation is standard.

But maybe we can find a way to avoid the segment tree by using the fact that the updates are only to suffixes. Consider the array cur_common. Let diff[i] = cur_common[i] - cur_common[i-1] (with cur_common[0]=0). Then range add on [L, R] corresponds to: diff[L] += 1, diff[R+1] -= 1. So we can maintain an array diff. To get the maximum of cur_common, we need to know the maximum prefix sum of diff. This is like maintaining the maximum prefix sum of an array that we update by adding 1 to a suffix? Actually, the updates are: for each j, we add 1 to cur_common[L..R] where R = j-1. In terms of diff, that means: diff[L] += 1, diff[R+1] -= 1. Since R = j-1, and L = last. So we are adding 1 to diff[last], and subtracting 1 from diff[j] (since R+1 = j). So each operation is: diff[last] += 1, diff[j] -= 1. This is a point update on diff. Then the values cur_common[i] = sum_{k=1..i} diff[k]. We need the maximum of cur_common[i] for i=1..j-1. This is the maximum prefix sum of diff up to j-1. So we need to maintain the maximum prefix sum of a dynamic array where we do point updates: add 1 to diff[last], and add -1 to diff[j]. This is a classic problem: we have an array diff of size N (or N+1), initially all zeros. We perform operations: diff[last] += 1, diff[j] -= 1. After each pair of updates (for each j), we need to know the maximum prefix sum of diff up to index j-1. Note that the updates are paired: one positive at last, one negative at j. And last ≤ j-1? Actually, last is the last occurrence of v up to j-1, so last ≤ j-1. So the positive update is at an index ≤ j-1, and the negative update is at index j. So the net effect on prefix sums up to j-1 is: the positive update increases the prefix sum from index last onward, and the negative update at j does not affect prefix sums up to j-1. So after the update, the maximum prefix sum up to j-1 can increase. We can maintain a Fenwick tree for diff to compute prefix sums, but we need the maximum prefix sum. We can maintain a segment tree over diff that supports point updates and range maximum query of the prefix sums. Alternatively, we can maintain a separate array that holds the current prefix sums, and we update them when diff changes. But when we update diff at an index, it affects all subsequent prefix sums. That would require updating a suffix, which is again a range update.

Maybe we can use a segment tree where each node stores the maximum prefix sum in its segment. We can build a segment tree over the array cur_common directly, with lazy propagation for range adds. That seems straightforward.

But note that the range we add to is [last, j-1]. Since j increases, the right endpoint is always j-1, which is the current maximum index. So we are always adding to a suffix that ends at the current j-1. This means we can maintain a variable that represents the current maximum index, and we extend the array as j increases. Actually, we can maintain a segment tree over the entire array of size N, but we only care about the first j-1 elements. We can update the segment tree with range adds on [last, j-1]. We need to query the maximum on [1, j-1]. Since j-1 increases, we can just query the maximum on [1, current_end]. So we can use a segment tree that supports range add and range max. The range add is on an interval, and the range max is on a prefix. That's fine.

Let's design the segment tree:
- Size: N (since indices go from 1 to N)
- Initially all zeros.
- For each j from 2 to N-1:
    - v = A[j]
    - last = last_occurrence[v]
    - if last > 0:
        - range_add(last, j-1, 1)
    - Then we need to compute candidate = distinct(1..j) + suffix[j+1] + query_max(1, j-1)
    - But careful: query_max(1, j-1) gives the maximum cur_common[i] for i < j. That's exactly max_{i<j} common(i,j).
    - So we update answer = max(answer, candidate)
    - Then we update last_occurrence[v] = j (since now j is the last occurrence of v up to j).

We also need to compute distinct(1..j) and suffix[j+1]. We can precompute pref and suff arrays in O(N).

Let's test this algorithm on the earlier example: A = [1,2,1,2,3], N=5.
Precompute:
pref: [1,1,2,2,2,2]? Actually:
i=1: {1} ->1
i=2: {1,2} ->2
i=3: {1,2} ->2
i=4: {1,2} ->2
i=5: {1,2,3} ->3
So pref = [0,1,2,2,2,3] (1-indexed)
suff: from right:
i=5: {3} ->1
i=4: {2,3} ->2
i=3: {1,2,3} ->3
i=2: {1,2,3} ->3
i=1: {1,2,3} ->3
suff[6]=0
So suff = [0,3,3,3,2,1,0]

Now segment tree initially all zeros.
last_occurrence array size 6 (since A_i ≤5, but we can use N+1) all 0.
We iterate j=2,3,4 (N-1=4).
j=2:
v=A[2]=2, last=last_occurrence[2]=0. So no range add.
Query max on [1,1]: cur_common[1] is 0. So max_common=0.
candidate = distinct(1..2) + suffix[3] + max_common = pref[2]=2 + suff[3]=3 + 0 =5.
Update answer=5.
Update last_occurrence[2]=2.

j=3:
v=A[3]=1, last=last_occurrence[1]=0? Actually, last_occurrence[1] is still 0 because A[1]=1 but we haven't updated it? Wait, we need to update last_occurrence as we go. After processing j=2, we updated last_occurrence[2]=2. But we haven't updated last_occurrence[1] yet. We should update last_occurrence[A[j]] = j after processing j. So for j=2, we did update last_occurrence[2]=2. For j=3, before processing, last_occurrence[1] is still 0 because we haven't seen 1? But we have seen 1 at position 1. So we need to initialise last_occurrence with the first occurrence? Actually, we can update last_occurrence as we go: when we are at position j, the last occurrence of A[j] up to j-1 should be already stored. So we need to update last_occurrence for all positions as we iterate. So before the loop, we can set last_occurrence[A[1]] = 1. Then for j=2, we use last_occurrence[A[2]] which was 0, then after, we set last_occurrence[A[2]]=2. For j=3, last_occurrence[A[3]] should be 1 (from position 1). So we need to initialise last_occurrence with the first element. So let's do that: before the loop, set last_occurrence[A[1]] = 1. Then for j=2, last = last_occurrence[A[2]] (0). Then update last_occurrence[A[2]]=2. For j=3, last = last_occurrence[A[3]] (1). Then update last_occurrence[A[3]]=3. So that works.

So j=3:
v=1, last=1. range_add(1, 2, 1) because j-1=2. So add 1 to indices 1 and 2.
Now cur_common[1] becomes 1, cur_common[2] becomes 1.
Query max on [1,2]: max=1.
candidate = distinct(1..3)=pref[3]=2 + suffix[4]=2 + max_common=1 =5.
Update answer=5.
Update last_occurrence[1]=3.

j=4:
v=2, last=last_occurrence[2]=2. range_add(2, 3, 1) because j-1=3. So add 1 to indices 2 and 3.
Now cur_common[1]=1, cur_common[2]=2, cur_common[3]=1.
Query max on [1,3]: max=2.
candidate = distinct(1..4)=pref[4]=2 + suffix[5]=1 + max_common=2 =5.
Update answer=5.
Update last_occurrence[2]=4.

So answer=5, which matches.

Let's test with the sample 1: A = [3,1,4,1,5], N=5.
Compute pref: 
i=1: {3} ->1
i=2: {3,1} ->2
i=3: {3,1,4} ->3
i=4: {3,1,4} ->3
i=5: {3,1,4,5} ->4
suff:
i=5: {5} ->1
i=4: {1,5} ->2
i=3: {4,1,5} ->3
i=2: {1,4,1,5} -> {1,4,5} ->3
i=1: {3,1,4,1,5} -> {3,1,4,5} ->4
Now run algorithm:
last_occurrence initially: last[3]=1.
j=2: v=1, last=0, no add. max=0. candidate = pref[2]=2 + suff[3]=3 + 0 =5. update last[1]=2.
j=3: v=4, last=0, no add. max=0. candidate = pref[3]=3 + suff[4]=2 + 0 =5. update last[4]=3.
j=4: v=1, last=2 (from j=2), range_add(2,3,1). cur_common[2]=1, cur_common[3]=1. max on [1,3] = max(0,1,1)=1. candidate = pref[4]=3 + suff[5]=1 + 1 =5. update last[1]=4.
Answer=5. Matches.

Sample 2: A = [2,5,6,4,4,1,1,3,1,4], N=10.
We can trust the algorithm.

Complexity: O(N log N) due to segment tree operations. Each j does a range add and a range max, both O(log N). Also updating last_occurrence is O(1). So total O(N log N).

We need to be careful with the range add: when last=0, we skip. Also, the range is [last, j-1]. But note that when last = j-1, we are adding to a single element. When last = j, that can't happen because last ≤ j-1. When last=0, we skip.

Edge case: j=2, the range is from last to 1. If last=0, skip. If last=1, we add to index 1. That matches the initial condition.

We also need to consider that the segment tree should be built for indices 1 to N. We only query on [1, j-1]. Since j-1 increases, we can just query the maximum on [1, j-1]. Alternatively, we can query the maximum on [1, j-1] each time.

We should also consider that the array cur_common for indices >= j are not used, but we might have added to them in previous steps? Actually, we only add to indices up to j-1, so cur_common[j] and beyond are never updated until they become the new j-1 in a later step. So it's fine.

Now, we need to implement the segment tree with lazy propagation for range add and range max.

Alternatively, we can use a Fenwick tree for range add and point query, but we need the maximum over a prefix, so we would need to compute all prefix sums, which is O(N) per query. Not good.

Another idea: since the updates are always adding to a suffix, we can maintain an array of differences and a prefix maximum array. But updates are point updates to diff, and we need the maximum prefix sum. We can use a segment tree over diff where each node stores the maximum prefix sum of its segment. That is a standard segment tree variant. But implementing range add with lazy propagation is also fine.

Given N up to 3e5, O(N log N) is fine.

We should also precompute pref and suff.

Let's write the plan in detail:

1. Read N and array A (1-indexed).
2. Compute pref[1..N]: 
   seen = set()
   for i in 1..N:
     seen.add(A[i])
     pref[i] = len(seen)
   Since A_i ≤ N, we can use a boolean array visited of size N+1 to compute in O(N) without overhead of set.
3. Compute suff[1..N+1]:
   seen = set()
   for i in N down to 1:
     seen.add(A[i])
     suff[i] = len(seen)
   suff[N+1] = 0
4. Initialise segment tree for range add and max over array of size N (indices 1..N). Initially all zeros.
5. Initialise last occurrence array of size N+1 with 0. Set last[A[1]] = 1.
6. For j from 2 to N-1:
     v = A[j]
     last = last_occurrence[v]
     if last > 0:
         segment_tree.range_add(last, j-1, 1)
     max_common = segment_tree.range_max(1, j-1)
     candidate = pref[j] + suff[j+1] + max_common
     answer = max(answer, candidate)
     last_occurrence[v] = j
7. Print answer.

We need to handle the case when j-1 < 1? For j=2, j-1=1, so it's fine. For j=2, if last > 0, we range_add(last, 1, 1). That's valid.

Now, we must ensure that the segment tree query for range max on [1, j-1] works when j-1 is 0? That only happens for j=1, but we start from j=2. So j-1 >=1.

What about the initial state? We haven't added anything for j=2 before computing candidate. But we do the range add for the new element A[j] before querying. That corresponds to updating common(i,j) for the new j. So it's correct.

Let's test with a simple case: N=3, A=[1,2,3]. 
pref: [1,1,2,3]? Actually:
i=1:1, i=2:2, i=3:3.
suff: i=3:1, i=2:2, i=1:3, suff[4]=0.
last[A[1]]=1.
j=2: v=2, last=0, no add. max_common=0. candidate = pref[2]=2 + suff[3]=1 + 0 =3. last[2]=2.
j=3 is not processed because N-1=2. So answer=3. Manual: splits: (1,2): pref1=1, mid2=1, suff3=1 ->3. So correct.

Another test: N=3, A=[1,1,1]. pref: [1,1,1], suff: [1,1,1,0].
last[1]=1.
j=2: v=1, last=1, range_add(1,1,1). max_common=1. candidate = pref[2]=1 + suff[3]=1 +1=3. last[1]=2.
Answer=3. Manual: (1,2): pref1=1, mid2=1, suff3=1 ->3. Correct.

Now, we need to implement the segment tree. We can write a class with arrays for tree and lazy. Since we only need range add and range max, we can use a standard lazy propagation segment tree.

Alternatively, we can use a binary indexed tree to store the differences, and then maintain a multiset of the current prefix sums? But updating a range via diff updates requires updating two points, and then the prefix sums change for all subsequent indices. We would need to recompute the maximum prefix sum from scratch, which is O(N). So segment tree is better.

We can also use a Fenwick tree for range add and point query, and then maintain a separate structure for the maximum. But since we need the maximum over a prefix, we can use a segment tree that supports point updates (since range add can be broken into point updates if we store the diff array) and range maximum query on the prefix sums. Let's think: if we maintain an array cur_common directly, and we want to add 1 to a range [L, R], we can do that with a segment tree. That's straightforward.

Given the time, we'll implement a segment tree with lazy propagation.

Complexities: O(N log N) time, O(N) memory.

Let's write the code in Python.

We'll need to be careful with recursion depth? N=3e5, segment tree recursion depth is log N, so fine.

We'll use iterative segment tree? Possibly simpler to use a recursive one with sys.setrecursionlimit.

Implementation steps:

- Read input.
- Compute pref array of length N+1 (1-indexed).
- Compute suff array of length N+2 (1-indexed, with suff[N+1]=0).
- Initialise last array of size N+1 (since A_i ≤ N) with 0. Set last[A[1]] = 1.
- Build segment tree with N elements, all 0. (We can use size = 1 << (N-1).bit_length())
- ans = 0
- For j in range(2, N):
    v = A[j-1] if we use 0-indexed? Let's use 0-indexed for Python: A[0..N-1]. But pref and suff are 1-indexed. We'll adjust.
Better: keep 1-indexed for arrays. So A is list of length N+1, with A[1..N].
Read N, then read the list, and assign A[1]=..., etc.
Then for j from 2 to N-1 inclusive:
    v = A[j]
    last = last_occurrence[v]
    if last > 0:
        seg.add(last, j-1, 1)   # range add on [last, j-1]
    max_common = seg.query_max(1, j-1)   # max on [1, j-1]
    candidate = pref[j] + suff[j+1] + max_common
    ans = max(ans, candidate)
    last_occurrence[v] = j

- Print ans.

We need to make sure that for j=2, j-1=1, so query on [1,1] is valid.

Now, implement segment tree.

We'll write a class SegTree:
- __init__(self, n): build tree of size n, all zeros.
- range_add(l, r, val): add val to all elements in [l, r]
- range_max(l, r): return max in [l, r]

We can use arrays: tree and lazy, both size 4*n.

Let's code it.

We also need to handle the case when l > r? That could happen if last > j-1? But last ≤ j-1, so l <= r. If last=0, we skip.

Now, test on samples.

Sample 1: N=5, A=[3,1,4,1,5]
Compute pref: as before.
Compute suff: as before.
last[3]=1.
j=2: v=1, last=0, no add. max=0. cand=2+3+0=5. ans=5. last[1]=2.
j=3: v=4, last=0, no add. max=0. cand=3+2+0=5. ans=5. last[4]=3.
j=4: v=1, last=2, add(2,3,1). max=1. cand=3+1+1=5. ans=5. last[1]=4.
Output 5.

Sample 2: N=10, A=[2,5,6,4,4,1,1,3,1,4]
Compute pref:
i=1: {2} ->1
i=2: {2,5} ->2
i=3: {2,5,6} ->3
i=4: {2,5,6,4} ->4
i=5: {2,5,6,4} ->4
i=6: {2,5,6,4,1} ->5
i=7: {2,5,6,4,1} ->5
i=8: {2,5,6,4,1,3} ->6
i=9: {2,5,6,4,1,3} ->6
i=10: {2,5,6,4,1,3} ->6? Actually, A[10]=4, so still 6.
suff:
from right:
i=10: {4} ->1
i=9: {1,4} ->2
i=8: {3,1,4} ->3
i=7: {1,3,4} ->3
i=6: {1,3,4} ->3
i=5: {4,1,3} ->3
i=4: {4,1,3} ->3
i=3: {6,4,1,3} ->4
i=2: {5,6,4,1,3} ->5
i=1: {2,5,6,4,1,3} ->6
suff[11]=0.
Now run algorithm:
last[2]=1.
j=2: v=5, last=0, no add. max=0. cand=pref[2]=2 + suff[3]=4 + 0 =6. ans=6. last[5]=2.
j=3: v=6, last=0, no add. max=0. cand=3 + suff[4]=3 + 0 =6. ans=6. last[6]=3.
j=4: v=4, last=0, no add. max=0. cand=4 + suff[5]=3 + 0 =7. ans=7. last[4]=4.
j=5: v=4, last=4, add(4,4,1). max on [1,4]: cur_common[4]=1, others 0, so max=1. cand=4 + suff[6]=3 + 1 =8. ans=8. last[4]=5.
j=6: v=1, last=0, no add. max on [1,5]: still max=1. cand=5 + suff[7]=3 + 1 =9. ans=9. last[1]=6.
j=7: v=1, last=6, add(6,6,1). max on [1,6]: now cur_common[6]=1, max=1. cand=5 + suff[8]=3 + 1 =9. ans=9. last[1]=7.
j=8: v=3, last=0, no add. max=1. cand=6 + suff[9]=2 + 1 =9. ans=9. last[3]=8.
j=9: v=1, last=7, add(7,8,1). max on [1,8]: now cur_common[7]=1, cur_common[8]=1, max=1. cand=6 + suff[10]=1 + 1 =8. ans=9. last[1]=9.
So answer=9. Matches sample.

Great.

Now, we need to implement the segment tree efficiently. Since we are doing range add and range max, we can use a segment tree with lazy propagation.

Let's write the code.

We'll need to handle the case when the range is empty? We skip if last=0.

Also, we need to ensure that for j=2, we have last_occurrence for A[1] set. So we initialise last_occurrence[A[1]] = 1 before the loop.

What about the segment tree size? We need to support indices 1 to N. So n = N.

We'll write:

class SegTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

    def _push(self, node):
        if self.lazy[node]:
            self.tree[node*2] += self.lazy[node]
            self.lazy[node*2] += self.lazy[node]
            self.tree[node*2+1] += self.lazy[node]
            self.lazy[node*2+1] += self.lazy[node]
            self.lazy[node] = 0

    def range_add(self, l, r, val, node, node_l, node_r):
        if r < node_l or node_r < l:
            return
        if l <= node_l and node_r <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self._push(node)
        mid = (node_l + node_r) // 2
        self.range_add(l, r, val, node*2, node_l, mid)
        self.range_add(l, r, val, node*2+1, mid+1, node_r)
        self.tree[node] = max(self.tree[node*2], self.tree[node*2+1])

    def range_max(self, l, r, node, node_l, node_r):
        if r < node_l or node_r < l:
            return -10**9   # or a very small number
        if l <= node_l and node_r <= r:
            return self.tree[node]
        self._push(node)
        mid = (node_l + node_r) // 2
        return max(self.range_max(l, r, node*2, node_l, mid), self.range_max(l, r, node*2+1, mid+1, node_r))

We can simplify by using iterative segment tree, but recursive is fine.

We need to call range_add(l, r, val) and range_max(l, r). We'll wrap them.

Now, the main code:

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))
    # Compute pref
    pref = [0] * (N+1)
    seen = [False] * (N+1)   # since A_i ≤ N
    for i in range(1, N+1):
        if not seen[A[i]]:
            seen[A[i]] = True
            pref[i] = pref[i-1] + 1
        else:
            pref[i] = pref[i-1]
    # Compute suff
    suff = [0] * (N+2)
    seen = [False] * (N+1)
    for i in range(N, 0, -1):
        if not seen[A[i]]:
            seen[A[i]] = True
            suff[i] = suff[i+1] + 1
        else:
            suff[i] = suff[i+1]
    suff[N+1] = 0
    # Segment tree
    seg = SegTree(N)
    # last occurrence
    last = [0] * (N+1)
    last[A[1]] = 1
    ans = 0
    for j in range(2, N):
        v = A[j]
        last_v = last[v]
        if last_v > 0:
            seg.range_add(last_v, j-1, 1, 1, 1, seg.n)
        max_common = seg.range_max(1, j-1, 1, 1, seg.n)
        candidate = pref[j] + suff[j+1] + max_common
        if candidate > ans:
            ans = candidate
        last[v] = j
    print(ans)

But note: in the segment tree, the range we query is [1, j-1]. For j=2, that's [1,1]. For j=2, we have not added anything yet, so max_common is 0. That's correct.

We need to handle the case when j-1 might be 0? For j=2, j-1=1, so fine. For j=1, we don't enter the loop.

Also, we need to ensure that the segment tree methods are defined with the correct node range. In the class, we need to store n and use it in the wrapper.

Let's write the segment tree class with wrapper methods.

We'll also need to handle the case when the range is empty? We skip if last_v=0.

Now, test with the samples.

We'll run through the code in our head.

Potential issues: The segment tree's range_max returns -inf for out-of-range, but we are always querying within [1, j-1] which is within the tree. However, if j-1 is 0? That doesn't happen. So it's fine.

We should also consider that for j=2, the range_add might be called with last_v=0? We skip that. So no issue.

One more thing: In the segment tree, the node range is [1, seg.n]. We need to make sure seg.n is the size we built. In __init__, we set self.n = n. So we can use self.n.

But in the wrapper, we need to pass the correct parameters. We'll write:

def range_add(self, l, r, val):
    self._range_add(l, r, val, 1, 1, self.n)

def range_max(self, l, r):
    return self._range_max(l, r, 1, 1, self.n)

And then the recursive functions take node, node_l, node_r.

Let's code it properly.

Now, time complexity: O(N log N). Memory: O(N).

We should also consider that N can be 3e5, and recursion depth in segment tree is log2(3e5) ~ 19, so safe.

We can also use an iterative segment tree to avoid recursion, but it's fine.

Let's write the final code.

We'll also need to handle the case when N=3, the loop for j in range(2, N) is range(2,3) so j=2 only. That works.

Now, we should test with a random small case to ensure correctness. We can do mental test: N=4, A=[1,2,3,4]. All distinct.
pref: [1,2,3,4]
suff: i=4:1, i=3:2, i=2:3, i=1:4.
last[1]=1.
j=2: v=2, last=0, no add. max=0. cand=pref[2]=2 + suff[3]=2 + 0=4. last[2]=2.
j=3: v=3, last=0, no add. max=0. cand=3 + suff[4]=1 + 0=4. last[3]=3.
Answer=4. Manual: splits: (1,2):1+1+2=4, (1,3):1+2+1=4, (2,3):2+1+1=4. So max=4. Correct.

Another: A=[1,1,1,1]. pref: [1,1,1,1], suff: [1,1,1,1,0].
last[1]=1.
j=2: v=1, last=1, add(1,1,1). max=1. cand=1 + suff[3]=1 +1=3. last[1]=2.
j=3: v=1, last=2, add(2,2,1). max on [1,2]: now cur_common[1]=1, cur_common[2]=1, max=1. cand=1 + suff[4]=1 +1=3. last[1]=3.
Answer=3. Manual: (1,2):1+1+1=3, (1,3):1+1+1=3, (2,3):1+1+1=3. So max=3. Correct.

Now, we should ensure that the segment tree query returns the correct max. In the update, we add to a range, and we query the max. Since we are only adding, the max is non-decreasing over time for each index, but different indices have different values.

One potential pitfall: The segment tree range_add is called with parameters (last_v, j-1, 1). But if last_v > j-1? That cannot happen because last_v is the last occurrence of v up to j-1, so last_v ≤ j-1. So it's fine.

Now, we need to be careful with the segment tree implementation: when we do range_add, we need to make sure that the node range covers exactly [1, n]. In the recursive function, we pass node_l=1, node_r=n. That's fine.

Now, let's write the complete code.

We'll also add a fast I/O.

Edge case: N=3, A=[1,1,1]. Already tested.

Now, we can produce the final answer.

But wait: the problem statement says "This problem is a harder version of Problem C." It might be from an AtCoder contest. The constraints are up to 3e5. Our solution is O(N log N) which should pass.

We should also consider that the values A_i are up to N, so we can use the last array of size N+1.

Now, let's write the code in the final response.

We'll structure it as:

import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))
    # prefix distinct
    pref = [0]*(N+1)
    seen = [False]*(N+1)
    for i in range(1, N+1):
        if not seen[A[i]]:
            seen[A[i]] = True
            pref[i] = pref[i-1] + 1
        else:
            pref[i] = pref[i-1]
    # suffix distinct
    suff = [0]*(N+2)
    seen = [False]*(N+1)
    for i in range(N, 0, -1):
        if not seen[A[i]]:
            seen[A[i]] = True
            suff[i] = suff[i+1] + 1
        else:
            suff[i] = suff[i+1]
    # segment tree
    class SegTree:
        __slots__ = ('n', 'size', 'tree', 'lazy')
        def __init__(self, n):
            self.n = n
            self.size = 1
            while self.size < n:
                self.size <<= 1
            self.tree = [0]*(2*self.size)
            self.lazy = [0]*(2*self.size)
        def _push(self, node):
            if self.lazy[node]:
                self.tree[node*2] += self.lazy[node]
                self.lazy[node*2] += self.lazy[node]
                self.tree[node*2+1] += self.lazy[node]
                self.lazy[node*2+1] += self.lazy[node]
                self.lazy[node] = 0
        def _range_add(self, l, r, val, node, node_l, node_r):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                self.tree[node] += val
                self.lazy[node] += val
                return
            self._push(node)
            mid = (node_l + node_r) // 2
            self._range_add(l, r, val, node*2, node_l, mid)
            self._range_add(l, r, val, node*2+1, mid+1, node_r)
            self.tree[node] = max(self.tree[node*2], self.tree[node*2+1])
        def range_add(self, l, r, val):
            if l > r:
                return
            self._range_add(l, r, val, 1, 1, self.n)
        def _range_max(self, l, r, node, node_l, node_r):
            if r < node_l or node_r < l:
                return -10**9
            if l <= node_l and node_r <= r:
                return self.tree[node]
            self._push(node)
            mid = (node_l + node_r) // 2
            return max(self._range_max(l, r, node*2, node_l, mid), self._range_max(l, r, node*2+1, mid+1, node_r))
        def range_max(self, l, r):
            return self._range_max(l, r, 1, 1, self.n)
    seg = SegTree(N)
    last = [0]*(N+1)
    last[A[1]] = 1
    ans = 0
    for j in range(2, N):
        v = A[j]
        last_v = last[v]
        if last_v > 0:
            seg.range_add(last_v, j-1, 1)
        max_common = seg.range_max(1, j-1)
        candidate = pref[j] + suff[j+1] + max_common
        if candidate > ans:
            ans = candidate
        last[v] = j
    print(ans)

if __name__ == "__main__":
    solve()

We should test with the samples.

Sample 1: N=5, A=[3,1,4,1,5] -> output 5.
Sample 2: N=10, A=[2,5,6,4,4,1,1,3,1,4] -> output 9.

We can also test with a random small case by brute force.

But since we are confident, we'll go with this.

One more thing: The problem statement says "This problem is a harder version of Problem C." It might be from an AtCoder contest, and there is also a two-subarray version. Our solution is for the three-subarray version.

We should ensure that the code reads from stdin and writes to stdout.

Now, we need to output the code within the delimiters as per the instruction.

The instruction says: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT."

It doesn't specify the delimiters, but typically we use ```python or just the code. Since it says "Enclose your code within delimiters", maybe we should use triple backticks. But in the response, we can just provide the code.

I'll output the code in a code block.

Now, let's write the final response.</mm:think>```python
import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))
    
    # prefix distinct counts
    pref = [0] * (N + 1)
    seen = [False] * (N + 1)
    for i in range(1, N + 1):
        if not seen[A[i]]:
            seen[A[i]] = True
            pref[i] = pref[i - 1] + 1
        else:
            pref[i] = pref[i - 1]
    
    # suffix distinct counts
    suff = [0] * (N + 2)
    seen = [False] * (N + 1)
    for i in range(N, 0, -1):
        if not seen[A[i]]:
            seen[A[i]] = True
            suff[i] = suff[i + 1] + 1
        else:
            suff[i] = suff[i + 1]
    suff[N + 1] = 0
    
    # segment tree for range add and range max
    class SegTree:
        __slots__ = ('n', 'size', 'tree', 'lazy')
        def __init__(self, n):
            self.n = n
            self.size = 1
            while self.size < n:
                self.size <<= 1
            self.tree = [0] * (2 * self.size)
            self.lazy = [0] * (2 * self.size)
        
        def _push(self, node):
            if self.lazy[node]:
                self.tree[node * 2] += self.lazy[node]
                self.lazy[node * 2] += self.lazy[node]
                self.tree[node * 2 + 1] += self.lazy[node]
                self.lazy[node * 2 + 1] += self.lazy[node]
                self.lazy[node] = 0
        
        def _range_add(self, l, r, val, node, node_l, node_r):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                self.tree[node] += val
                self.lazy[node] += val
                return
            self._push(node)
            mid = (node_l + node_r) // 2
            self._range_add(l, r, val, node * 2, node_l, mid)
            self._range_add(l, r, val, node * 2 + 1, mid + 1, node_r)
            self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])
        
        def range_add(self, l, r, val):
            if l > r:
                return
            self._range_add(l, r, val, 1, 1, self.n)
        
        def _range_max(self, l, r, node, node_l, node_r):
            if r < node_l or node_r < l:
                return -10**9
            if l <= node_l and node_r <= r:
                return self.tree[node]
            self._push(node)
            mid = (node_l + node_r) // 2
            return max(self._range_max(l, r, node * 2, node_l, mid),
                       self._range_max(l, r, node * 2 + 1, mid + 1, node_r))
        
        def range_max(self, l, r):
            return self._range_max(l, r, 1, 1, self.n)
    
    seg = SegTree(N)
    last = [0] * (N + 1)
    last[A[1]] = 1
    ans = 0
    
    for j in range(2, N):
        v = A[j]
        last_v = last[v]
        if last_v > 0:
            seg.range_add(last_v, j - 1, 1)
        max_common = seg.range_max(1, j - 1)
        candidate = pref[j] + suff[j + 1] + max_common
        if candidate > ans:
            ans = candidate
        last[v] = j
    
    print(ans)

if __name__ == "__main__":
    solve()
```

## worker: Implement the segment tree based algorithm in Pyth
The solution uses the algebraic identity `pref[i] + distinct(i+1..j) = distinct(1..j) + common(i,j)`, reducing the three-variable problem to maximizing `common(i,j)` for each j. The segment tree efficiently maintains the running `common` values with range additions in O(log N) per update, giving overall O(N log N) time complexity.
