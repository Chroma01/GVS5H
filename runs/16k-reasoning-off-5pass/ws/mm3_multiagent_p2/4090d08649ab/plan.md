We need to compute for every subarray the minimum number of operations to erase the multiset by repeatedly picking an interval [l,r] that fully contains the current set's value range. The optimal strategy is to split the set into groups that are already "coverable" as a contiguous value interval. In each operation we can delete a set of values that form a contiguous value interval and that all appear on the board.

Key insight: For a subarray, consider the set of distinct values. It can be viewed as a union of "blocks" of consecutive values that are all present. Each block can be deleted in one operation. So `f(L,R)` equals the number of connected components of the set of distinct values when viewed as a subgraph on the line of values 1..N.

Therefore we need to sum, over all subarrays, the number of connected components of its distinct value set.

We can transform the problem: for each adjacent pair of values (x, x+1), consider the subarrays where both x and x+1 appear. If in a subarray both appear, then the components for those two values merge (they are in the same component). So `f(L,R) = (#distinct values in subarray) - (#adjacent value pairs x,x+1 that both appear in subarray)`.

Let `D(L,R)` be the number of distinct values in subarray, and `C(L,R)` the number of adjacent value pairs (x,x+1) with both present. Then
```
f(L,R) = D(L,R) - C(L,R)
```
So the answer is
```
sum D(L,R) - sum C(L,R)
```

We can compute both sums efficiently.

**Sum of D(L,R):** classic problem; each value v contributes to subarrays that include at least one occurrence of v. The contribution of each occurrence is the number of subarrays containing it, but we need distinct per subarray, so we need to avoid double counting when a subarray has multiple occurrences of v. Standard technique: for each position i, consider the previous occurrence of the same value. The number of subarrays where i is the first occurrence (i.e., the leftmost occurrence) of v in the subarray is (i - prev) * (N - i + 1) (where prev is previous occurrence of A[i], or 0 if none). Sum this over i.

**Sum of C(L,R):** For each adjacent value pair (x, x+1), we need to count subarrays that contain at least one x and at least one x+1. This is a 2-value covering problem. We can process each pair independently. For a fixed pair (a,b) = (x,x+1), we look at the positions of a and b in the array. A subarray contains both iff it includes at least one a and at least one b. Count of subarrays containing both = total subarrays - subarrays missing a - subarrays missing b + subarrays missing both a and b.

- Total subarrays = N*(N+1)/2.
- Subarrays missing a: treat only positions of a as "gaps" in the array, and count subarrays that lie entirely in the gaps between a's. If the positions of a are p1 < p2 < ... < pk, then there are k+1 gaps: before p1, between p1 and p2, ..., after pk. A subarray missing a is any subarray fully inside one gap. The total count of subarrays missing a is sum over gaps of len*(len+1)/2 where len is the gap length.
- Subarrays missing b: similar.
- Subarrays missing both a and b: these are subarrays that contain neither a nor b. To count them efficiently we can merge the positions of a and b and compute gaps between them. Since N is up to 3e5 and there are N-1 pairs, total sum of frequencies is 2N per pair? Wait, each pair is processed individually. The total work to process all pairs would be O(N^2) if done naively because we would need to traverse the whole array for each pair. Need a better approach.

**Alternative approach:** Process all pairs together by iterating over the array and tracking the last occurrences of each value. For each new position i, we can update contributions of pairs involving A[i]. The number of pairs is N-1 (adjacent values). We can use a segment tree or Fenwick tree to maintain something, or a divide-and-conquer offline solution.

But perhaps there is a known simpler formula. Let's think.

We need sum over all subarrays of (#distinct values) - (#adjacent pairs with both values present).

Sum of #distinct values is computable in O(N) using the "first occurrence" technique.

Now for sum of C(L,R) = sum over subarrays of (number of x such that both x and x+1 appear). For each x, we need the number of subarrays where both x and x+1 appear. Let's denote for each x: count_x = number of subarrays that contain at least one occurrence of x and at least one occurrence of x+1.

Then sum C = sum_{x=1}^{N-1} count_x.

So we need to compute for each adjacent value pair (x,x+1) the number of subarrays that contain both. This is a classic problem that can be solved in total O(N log N) or O(N) with a sweep line.

**Observation:** For a fixed pair (x,x+1), we can think of the array as a sequence of blocks separated by occurrences of x or x+1. Actually, we can process all pairs simultaneously using a divide and conquer on the value range? Not sure.

Let's try to compute count_x efficiently for all x. The naive way for each x: locate positions of x and x+1, compute gaps. For each x, we might need to scan the whole array. If we do this for all x, it's O(N^2). But we can do it smarter by scanning once and updating counts for pairs (x,x+1) based on "segments" where neither x nor x+1 appears.

Alternative: Use a two-pointer / sliding window approach. For each left endpoint L, we can maintain the minimum R such that both x and x+1 are present? That would be O(N^2) if we do it for each x.

Maybe we can use the following: For each x, we can precompute the next occurrence of x and x+1 after each position. Then the condition "subarray [L,R] contains both" is equivalent to: there exists i in [L,R] with A[i]=x and j in [L,R] with A[j]=x+1. This is similar to counting subarrays that contain at least one of a set of positions.

We can use inclusion-exclusion: For each x, count_x = total - missing_x - missing_{x+1} + missing_both.

- missing_x = subarrays with no x. We can compute this for all values simultaneously: for each value v, the number of subarrays without v is sum over gaps between v's of len*(len+1)/2. We can compute this in O(N) for all v? Actually, the gaps for different v are independent. If we compute the gap sum for each v individually, it's O(N) per v, total O(N^2). Not good.

But we can compute the total number of subarrays without v for all v using a trick: For each position i, the "previous occurrence" prev_i. The number of subarrays where the first occurrence of v is at position i is (i - prev_i)*(N - i + 1). The number of subarrays with at least one v is sum over i of that. The number of subarrays without v is total - that. So we can compute for each v the number of subarrays containing v in O(N) total (by processing each position once and updating its value's contribution). Specifically, for each position i, value v=A[i], we add (i - prev_v) * (N - i + 1) to cnt_contains[v], where prev_v is the previous occurrence of v. After processing all positions, we have cnt_contains[v] for all v. Then missing_v = total - cnt_contains[v].

Great! So we can compute cnt_contains[v] for all v in O(N).

Now we need for each adjacent pair (x,x+1) the number of subarrays missing both x and x+1. Let's denote missing_both[x] = number of subarrays that contain neither x nor x+1.

If we can compute missing_both[x] for all x efficiently, then count_x = total - missing_x - missing_{x+1} + missing_both[x].

How to compute missing_both for all x? This is more challenging. For each pair (x,x+1), we need to count subarrays that avoid both values. We can think of the array and mark positions that are either x or x+1. A subarray avoids both iff it lies entirely in a gap between these marked positions. So for a fixed pair (x,x+1), the marked positions are the union of occurrences of x and x+1. The gaps are intervals between consecutive marked positions (or edges). The number of subarrays avoiding both is sum over gaps of len*(len+1)/2.

We need this sum for each of the N-1 pairs. This is still heavy if we compute individually.

But we can maybe use a divide-and-conquer on the value domain. The values are from 1 to N. For each position, we can consider its value. We need to answer for each adjacent pair (x,x+1) the sum of gap lengths squared (or len*(len+1)/2) in the array restricted to positions where A[i] is in {x,x+1}. That is, we look at the subsequence of positions where A[i] is x or x+1, and compute the gaps between consecutive such positions in the original index order.

Wait, careful: The "gaps" are in the index space (positions 1..N), not in the value space. For pair (x,x+1), we consider the set of indices i such that A[i] = x or A[i] = x+1. Sort them. The gaps are the intervals between these indices: (0, p1-1), (p1+1, p2-1), ..., (pk+1, N). Each gap is a maximal contiguous block of indices that contain neither x nor x+1.

So the problem reduces to: For each pair (x,x+1), we have a set S_x = {i | A[i] = x or x+1}. We need to compute the sum over gaps of len*(len+1)/2.

We can think of the array as a sequence, and we have N-1 queries of the form: given two values, compute the sum of len*(len+1)/2 over gaps between occurrences of these two values.

This is reminiscent of offline queries on the array with Mo's algorithm or similar, but we have N-1 queries, and the array length is N, so N is 3e5. We can perhaps do a sweepline that processes all pairs in O(N log N) or O(N).

Observation: For a fixed pair (x,x+1), the positions are exactly the union of the positions of x and positions of x+1. If we maintain a data structure that can quickly give the sum of gap lengths (or the sum of len*(len+1)/2) when we "activate" a value? But we need to do it for many pairs.

Another perspective: The sum over all subarrays of C(L,R) = number of pairs (x,x+1) such that both appear in the subarray. We can swap the order of summation: sum over x of (number of subarrays containing both x and x+1). So we need count_x for each x.

Maybe we can compute count_x by scanning the array and maintaining the "window" that contains both. There is a known approach: for each left L, we can find the minimum R such that both x and x+1 are present, but that depends on x. Not good.

Let's try to compute missing_both for all x in O(N) by using a trick similar to the distinct count problem.

We want to compute for each x: M[x] = number of subarrays that contain neither x nor x+1.

Define for each subarray [L,R], it avoids both x and x+1 iff for all i in [L,R], A[i] is not x and not x+1. That is, the subarray is contained in a gap between occurrences of x or x+1.

Equivalently, the subarray avoids both iff its set of values is disjoint from {x,x+1}.

We can think of the array and consider each position i as belonging to some "segment" defined by the nearest occurrence of x or x+1 to the left and right. But this depends on x.

Another idea: Use a segment tree to maintain for each index the set of values present? Too heavy.

Maybe we can use the following: For each subarray, the condition "contains neither x nor x+1" is equivalent to "does not contain x AND does not contain x+1". We already have counts of subarrays missing x and missing x+1. By inclusion-exclusion, missing_both = missing_x + missing_{x+1} - (subarrays missing at least one of them). Wait, no: We want subarrays missing both. That's exactly the intersection of the two events: missing x AND missing x+1. We have the counts for each event separately. The intersection is what we need.

If we can compute for each x the number of subarrays that contain at least one of x or x+1, then missing_both = total - (subarrays containing at least one). And subarrays containing at least one = subarrays containing x + subarrays containing x+1 - subarrays containing both. But that's circular because we want subarrays containing both.

Alternatively, subarrays missing both = subarrays missing x - subarrays that contain x+1 but miss x? No, subarrays missing both = subarrays that miss x AND miss x+1.

We can compute subarrays missing both by considering the positions of x and x+1 together. Let's denote the union of positions of x and x+1 as U. The gaps are intervals of indices that contain no element of U. For a subarray to miss both, it must be contained in one gap. So the number of such subarrays is the sum over gaps of len*(len+1)/2.

Now, how to compute this sum for all x? We can process the array and maintain for each adjacent value pair the "current gap length" and accumulate contributions? But there are many pairs.

Maybe we can use a divide and conquer on the value range. Since values are up to N, we can build a segment tree over the value range. For each node representing a range of values [l,r], we can consider the subarray formed by positions whose values are in that range. Then the missing_both for pair (x,x+1) where x and x+1 are in different sides of a split? Hmm.

Actually, there is a known problem: "sum over all subarrays of the number of distinct values" and "sum over all subarrays of the number of pairs of adjacent values that both appear". I recall a solution that processes the array in order and uses a Fenwick tree or similar to maintain contributions.

Let's think from a different angle. For each subarray, the number of components is the number of distinct values minus the number of adjacent value pairs that are both present. We can also compute the number of components by considering the graph where vertices are distinct values, edges between adjacent values that both appear. The components are the connected components of this graph. The number of components = #vertices - #edges (within the induced subgraph on the set of present values). But note: the graph is a subgraph of a path. The number of components in a path graph induced by a subset of vertices is exactly #vertices - (number of edges in the induced subgraph). And the edges in the induced subgraph are exactly the adjacent pairs (x,x+1) where both are in the subset. So yes, f(L,R) = |S| - E(S), where S is the set of distinct values in [L,R], and E(S) is the number of edges in the path graph between consecutive values both in S.

So we need sum_{L,R} (|S_{L,R}| - E(S_{L,R})).

We can compute sum |S| easily as described.

Now, sum E(S) = sum_{x=1}^{N-1} (number of subarrays where both x and x+1 appear). Let's focus on that.

We need for each x, the number of subarrays [L,R] such that the interval contains at least one occurrence of x and at least one occurrence of x+1.

We can think of the array and for each x, we can compute the "minimal covering interval" for each pair of positions? But we need to count all subarrays that cover at least one x and at least one x+1.

Standard technique: For each pair of positions (i,j) with A[i]=x, A[j]=x+1, the subarrays that contain both must have L <= min(i,j) and R >= max(i,j). The number of such subarrays is i * (N - j + 1) if i < j. But we would double count because a subarray might contain multiple pairs. So we need the union over all such pairs.

Alternatively, we can compute the number of subarrays that contain both as: total subarrays - subarrays missing x - subarrays missing x+1 + subarrays missing both. We already have total and missing_x. We need missing_both.

So the key is to compute missing_both for all x efficiently.

Let's attempt to compute missing_both for all x in O(N) by scanning the array once and maintaining something.

Consider the array positions 1..N. For each position i, we have a value A[i]. For a given x, the set U_x = {i | A[i] in {x, x+1}}. The gaps are the maximal intervals of indices that contain no element of U_x.

We can process the array and maintain for each x the current gap length? As we scan, when we encounter a value v, it affects the pairs (v-1, v) and (v, v+1). Specifically, for pair (v-1, v), this position belongs to U_{v-1}. For pair (v, v+1), it belongs to U_v. So each position affects exactly two pairs (except at boundaries). There are N-1 pairs. If we can maintain for each pair the current gap length and a running sum of gap contributions, we can update in O(1) per position? But we need to maintain N-1 pairs, and N is 3e5, so O(N) per update is too much if we update all pairs. But we can update only the pairs that are "active" or "changed"? Actually, when we encounter a value v, it terminates the current gap for the pairs that include v. Specifically, for pair (v-1, v), the position v is part of U, so it splits the current gap for that pair. Similarly for (v, v+1). For other pairs x, this position v is not in U_x (unless v = x or x+1, but x is not v-1 or v, so v is not in {x,x+1} for x != v-1 and x != v). Wait, for a pair x, the condition for v to be in U_x is v = x or v = x+1. So v is in U_x only for x = v-1 and x = v. So indeed, each position affects exactly two pairs.

Thus, we can maintain an array `gap_len[x]` for each pair x (1 <= x <= N-1) representing the current length of the ongoing gap (since the last occurrence of either x or x+1). As we scan the array from left to right, we update:
- For the two affected pairs, the current gap ends, so we add the contribution of that gap to some accumulator for that pair, and then reset the gap length to 0.
- For all other pairs, the gap length increases by 1 (since we passed a position that is not in their U set). But there are O(N) other pairs, so updating all of them is O(N^2).

We need a way to add 1 to gap_len for all pairs except two. This is a range update on the set of pairs. We can use a difference array: maintain a global counter `add_all` that represents the number of positions since the last "reset" for each pair. Actually, we can store for each pair the last time it was reset, and compute the current gap length as (current_index - last_reset_index - 1)? Wait, careful.

Let's think: For a fixed pair x, the set U_x is a subset of positions. As we scan, the gap lengths are the distances between consecutive elements of U_x. The sum of gap lengths is just the total number of positions that are not in U_x, which is N - |U_x|. But we need the sum of len*(len+1)/2 over gaps. That is not simply a linear function; it's quadratic in gap lengths.

If we process online, when we extend a gap by one (i.e., we are at position i and the current gap for pair x is a contiguous block of positions that are not in U_x, and we add position i to that gap), the contribution to the sum of len*(len+1)/2 increases. Specifically, if a gap has current length L (meaning we have L consecutive positions so far that are not in U_x), the contribution from that gap is L*(L+1)/2. When we extend the gap by 1, the new length is L+1, and the new contribution is (L+1)*(L+2)/2. The increase is (L+1). So we can maintain for each pair the current gap length L_x, and the total accumulated sum S_x = sum of len*(len+1)/2 over gaps that have been closed so far plus the contribution of the current open gap. Then when we move to the next position i:
- For pairs not affected by this position, L_x increases by 1. But we cannot update L_x for all pairs individually. However, we can use a global "offset" trick: maintain a global variable `delta` that represents how much we have added to all L_x since the last "event" for each pair. Actually, we can store for each pair the last position where it was reset, and compute L_x as i - last_event_x - 1? Let's define for each pair x: `last[x]` = the largest index <= i-1 such that position last[x] is in U_x (i.e., A[last[x]] is x or x+1). Then the current open gap is the interval (last[x], i), so the length of the gap so far is i - last[x] - 1. But that's not quite right: the gap is from the last occurrence to the current position. If the last occurrence is at position p, then the gap includes positions p+1, p+2, ..., i-1. So the length is (i-1) - (p+1) + 1 = i - p - 1. So L_x = i - last[x] - 1.

Now, the contribution of the current open gap to the sum of len*(len+1)/2 is L_x * (L_x + 1) / 2. The total sum for pair x, including closed gaps, is something we can accumulate when a gap closes. When we encounter a position i that is in U_x (i.e., A[i] = x or x+1), the current open gap closes. At that moment, the gap length is L = i - last[x] - 1. We should add L*(L+1)/2 to the total sum for pair x. Then we reset last[x] = i, and the new open gap length is 0.

So if we can maintain last[x] for all x, and when we encounter A[i] = v, we close the gaps for pairs x = v-1 and x = v (since they are the only ones for which this position is in U_x). For all other pairs, the current position is not in U_x, so the gap simply extends; we don't need to do anything for them explicitly because we can compute L_x on the fly using last[x] and i.

But we also need to keep a running total of the sum over closed gaps. Let's maintain an array `sum_closed[x]` which is the sum of L*(L+1)/2 for all gaps that have been closed so far. When we close a gap for pair x, we compute L = i - last[x] - 1, add L*(L+1)/2 to sum_closed[x], and update last[x] = i.

After processing the entire array, we need to close the final open gaps. For each pair x, after the last position N, the final open gap has length L = N - last[x] (since it includes positions last[x]+1 through N). We add L*(L+1)/2 to sum_closed[x]. Then missing_both[x] = sum_closed[x].

But wait: Is that correct? Let's verify: For a fixed pair x, the positions in U_x are exactly the indices where A[i] = x or x+1. As we scan, we close a gap whenever we hit such a position. The sum of L*(L+1)/2 over all gaps (including the final one after the last occurrence) indeed gives the number of subarrays that contain neither x nor x+1. Because any subarray avoiding both must be entirely contained in one of these gaps. For a gap of length L, the number of subarrays within it is L*(L+1)/2. And these gaps partition the set of positions not in U_x. So yes, missing_both[x] = sum over gaps of L*(L+1)/2.

Thus, if we can maintain for each pair x the last occurrence position `last[x]`, and when we encounter a value v at position i, we update the two pairs (v-1, v) and (v, v+1) (with appropriate boundary checks). For each such update, we compute the length of the gap that just closed: L = i - last[x] - 1, and add L*(L+1)/2 to `sum_closed[x]`. Then set `last[x] = i`.

This is O(1) per update! Because each position affects exactly two pairs. The array `last` and `sum_closed` have size N (or N-1). We process N positions, each doing O(1) work. So total O(N).

Let's double-check with an example. Array: 1 3 1 4. N=4. Values: 1,3,1,4. Pairs: (1,2), (2,3), (3,4). We need to compute missing_both for each.

Initialize last[1]=last[2]=last[3]=0. sum_closed all 0.

i=1, v=1. Affected pairs: (0,1) invalid? v-1=0, so only pair (v, v+1) = (1,2) is affected? Wait, for v=1, it belongs to U_x for x=0 (invalid) and x=1 (since x=1 gives {1,2}). So only pair x=1 is affected. So we close gap for x=1: L = i - last[1] - 1 = 1 - 0 - 1 = 0. Add 0 to sum_closed[1]. last[1] = 1.

i=2, v=3. Affected pairs: (2,3) and (3,4). For x=2: L = 2 - last[2] - 1 = 2 - 0 - 1 = 1. Add 1*2/2=1 to sum_closed[2]. last[2]=2. For x=3: L = 2 - last[3] - 1 = 1. Add 1 to sum_closed[3]. last[3]=2.

i=3, v=1. Affected pairs: x=0 (invalid) and x=1. For x=1: L = 3 - last[1] - 1 = 3 - 1 - 1 = 1. Add 1 to sum_closed[1]. last[1]=3.

i=4, v=4. Affected pairs: x=3 and x=4. For x=3: L = 4 - last[3] - 1 = 4 - 2 - 1 = 1. Add 1 to sum_closed[3]. last[3]=4. For x=4: L = 4 - last[4] - 1 = 3. Add 3*4/2=6 to sum_closed[4]. last[4]=4.

End of array. Now close final gaps:
For x=1: L = N - last[1] = 4 - 3 = 1. Add 1 to sum_closed[1]. Now sum_closed[1] = 0+1+1 = 2.
For x=2: L = 4 - last[2] = 4 - 2 = 2. Add 2*3/2=3 to sum_closed[2]. sum_closed[2] = 1+3 = 4.
For x=3: L = 4 - last[3] = 4 - 4 = 0. Add 0. sum_closed[3] = 1+1+0 = 2.
For x=4: L = 4 - last[4] = 0. Add 0. sum_closed[4] = 6.

So missing_both[1]=2, [2]=4, [3]=2, [4]=6.

Now total subarrays = 4*5/2=10.
We need missing_x for x=1..4. Let's compute cnt_contains[x] using the first occurrence method.
Array: 1: prev=0, contrib=(1-0)*(4-1+1)=1*4=4. 3: prev=0, contrib=1*3? Wait, i=2, N=4, (2-0)*(4-2+1)=2*3=6. 1: i=3, prev=1, contrib=(3-1)*(4-3+1)=2*2=4. 4: i=4, prev=0, contrib=1*1=1. So cnt_contains[1]=4+4=8? Actually 1 appears twice, contributions: at i=1: 4, at i=3: 2*2=4, total 8. cnt_contains[3]=6, cnt_contains[4]=1. So missing_x = 10 - cnt_contains[x].
missing_1 = 2, missing_2? Wait, x=2: cnt_contains[2]? No occurrence of 2, so cnt_contains[2]=0, missing_2=10.
missing_3 = 10-6=4, missing_4 = 10-1=9.

Now for each pair (x,x+1), count_x = total - missing_x - missing_{x+1} + missing_both[x].
Pair (1,2): count_1 = 10 - missing_1 - missing_2 + missing_both[1] = 10 - 2 - 10 + 2 = 0. Indeed, no subarray contains both 1 and 2? Actually, subarray [1,1] has 1, [2,2] has 3, [3,3] has 1, [4,4] has 4. No subarray contains both 1 and 2. So 0 is correct.
Pair (2,3): count_2 = 10 - missing_2 - missing_3 + missing_both[2] = 10 - 10 - 4 + 4 = 0. No 2.
Pair (3,4): count_3 = 10 - missing_3 - missing_4 + missing_both[3] = 10 - 4 - 9 + 2 = -1? That's impossible! Let's compute carefully.
missing_3 = 10 - cnt_contains[3] = 10 - 6 = 4.
missing_4 = 10 - cnt_contains[4] = 10 - 1 = 9.
missing_both[3] = 2.
count_3 = 10 - 4 - 9 + 2 = -1. Something is wrong. Maybe my cnt_contains for 4 is wrong? Let's recalc: Array indices 1..4. For value 4 at i=4, prev occurrence of 4 is none, so prev=0. Contribution: (i - prev) * (N - i + 1) = (4-0)*(4-4+1) = 4*1 = 4. Wait, N=4, i=4, so N - i + 1 = 1. So 4*1=4. Not 1! I mistakenly used N-i+1=1, but 4*1=4. So cnt_contains[4]=4. Then missing_4 = 10-4=6.
Then count_3 = 10 - 4 - 6 + 2 = 2. That seems plausible: subarrays containing both 3 and 4. Let's list: [1,4] contains 1,3,1,4 -> contains 3 and 4. [2,4] contains 3,1,4 -> contains 3 and 4. [2,3] contains 3,1 -> no 4. [3,4] contains 1,4 -> no 3. So 2 subarrays. Good.

So the formula works. And we have an O(N) algorithm to compute missing_both for all pairs.

Now we can compute the answer as:
total_f = sum_{L,R} D(L,R) - sum_{x=1}^{N-1} count_x
where count_x = total_subarrays - missing_x - missing_{x+1} + missing_both[x].

We can compute sum_{x} count_x = (N-1)*total - sum_{x} (missing_x + missing_{x+1}) + sum_{x} missing_both[x].

Note that sum_{x=1}^{N-1} (missing_x + missing_{x+1}) = missing_1 + 2*missing_2 + 2*missing_3 + ... + 2*missing_{N-1} + missing_N. Actually:
For x=1: missing_1 + missing_2
x=2: missing_2 + missing_3
...
x=N-1: missing_{N-1} + missing_N
Sum = missing_1 + 2*(missing_2 + ... + missing_{N-1}) + missing_N.

So we can compute that easily if we have all missing_x.

Alternatively, we can compute count_x directly and sum them, since we have all missing_x and missing_both[x]. That is O(N).

So the steps:
1. Read N and array A[1..N].
2. Compute total_subarrays = N*(N+1)//2.
3. Compute cnt_contains[v] for v=1..N (or up to max value, but A_i <= N so v in 1..N). Use an array last_occ of size N+1 initialized to 0. For i=1..N, v=A[i], cnt_contains[v] += (i - last_occ[v]) * (N - i + 1), then last_occ[v] = i.
4. Compute missing_v = total_subarrays - cnt_contains[v] for v=1..N.
5. Compute sum_D = sum_{v=1}^N cnt_contains[v]. (This is the sum of distinct values over all subarrays.)
6. Compute missing_both[x] for x=1..N-1 using the sweep method:
   - Initialize last_pair[x] = 0 for x=1..N-1.
   - Initialize sum_closed[x] = 0.
   - For i=1..N: v=A[i].
     - For each affected x: x = v-1 (if 1 <= x <= N-1) and x = v (if 1 <= x <= N-1).
     - For each such x: L = i - last_pair[x] - 1; sum_closed[x] += L*(L+1)//2; last_pair[x] = i.
   - After loop, for x=1..N-1: L = N - last_pair[x]; sum_closed[x] += L*(L+1)//2. Then missing_both[x] = sum_closed[x].
7. Compute sum_C = sum_{x=1}^{N-1} count_x, where count_x = total_subarrays - missing_x - missing_{x+1} + missing_both[x].
   Note: missing_x is for value x, missing_{x+1} for value x+1. We have missing array from step 4.
8. Answer = sum_D - sum_C.

We should verify with sample 1.
N=4, A=[1,3,1,4].
total=10.
cnt_contains:
v=1: i=1, last=0, contrib=1*4=4. last=1.
v=3: i=2, last=0, contrib=2*3=6. last=2.
v=1: i=3, last=1, contrib=2*2=4. last=3.
v=4: i=4, last=0, contrib=4*1=4. last=4.
So cnt: [0,8,0,6,4]? Wait, v=1:8, v=2:0, v=3:6, v=4:4. Others 0.
sum_D = 8+0+6+4 = 18.
missing: total - cnt: v=1:2, v=2:10, v=3:4, v=4:6.
Now missing_both computed earlier: [1]=2, [2]=4, [3]=2, [4]=6. (For x=1..3: [1]=2, [2]=4, [3]=2. x=4 is not a pair index; we only need up to N-1=3.)
sum_C = count_1 + count_2 + count_3.
count_1 = 10 - missing_1 - missing_2 + missing_both[1] = 10 - 2 - 10 + 2 = 0.
count_2 = 10 - missing_2 - missing_3 + missing_both[2] = 10 - 10 - 4 + 4 = 0.
count_3 = 10 - missing_3 - missing_4 + missing_both[3] = 10 - 4 - 6 + 2 = 2.
sum_C = 2.
Answer = 18 - 2 = 16. Matches sample.

Sample 2: N=5, A=[3,1,4,2,4].
total = 15.
Compute cnt_contains:
last occ all 0.
i=1, v=3: (1-0)*(5-1+1)=1*5=5. last[3]=1.
i=2, v=1: (2-0)*(5-2+1)=2*4=8. last[1]=2.
i=3, v=4: (3-0)*(5-3+1)=3*3=9. last[4]=3.
i=4, v=2: (4-0)*(5-4+1)=4*2=8. last[2]=4.
i=5, v=4: (5-3)*(5-5+1)=2*1=2. last[4]=5.
cnt: v=1:8, v=2:8, v=3:5, v=4:9+2=11, v=5:0.
sum_D = 8+8+5+11 = 32.
missing: 15-8=7, 15-8=7, 15-5=10, 15-11=4, 15-0=15.
Now missing_both for x=1..4:
Initialize last_pair[1..4]=0, sum_closed=0.
i=1, v=3: affected x=2 (v-1=2) and x=3 (v=3).
x=2: L=1-0-1=0, add 0, last=1.
x=3: L=0, add 0, last=1.
i=2, v=1: affected x=0(inv) and x=1.
x=1: L=2-0-1=1, add 1, last=1.
i=3, v=4: affected x=3 and x=4.
x=3: L=3-1-1=1, add 1, last=3.
x=4: L=3-0-1=2, add 3, last=3.
i=4, v=2: affected x=1 and x=2.
x=1: L=4-1-1=2, add 3, last=4.
x=2: L=4-1-1=2, add 3, last=4.
i=5, v=4: affected x=3 and x=4.
x=3: L=5-3-1=1, add 1, last=5.
x=4: L=5-3-1=1, add 1, last=5.
End: close final gaps:
x=1: L=5-4=1, add 1. sum_closed[1] = 1+3+1=5? Wait, let's sum carefully:
For x=1: updates: at i=2: L=1, sum=1; at i=4: L=2, sum=1+3=4; final: L=1, sum=4+1=5. So missing_both[1]=5.
x=2: at i=1: L=0, sum=0; at i=4: L=2, sum=3; final: L=5-4=1, sum=3+1=4. So missing_both[2]=4.
x=3: at i=1: L=0; at i=3: L=1, sum=1; at i=5: L=1, sum=2; final: L=5-5=0, sum=2. So missing_both[3]=2.
x=4: at i=3: L=2, sum=3; at i=5: L=1, sum=4; final: L=0, sum=4. So missing_both[4]=4.
Now sum_C:
count_1 = 15 - missing_1 - missing_2 + missing_both[1] = 15 - 7 - 7 + 5 = 6.
count_2 = 15 - missing_2 - missing_3 + missing_both[2] = 15 - 7 - 10 + 4 = 2.
count_3 = 15 - missing_3 - missing_4 + missing_both[3] = 15 - 10 - 4 + 2 = 3.
count_4 = 15 - missing_4 - missing_5 + missing_both[4] = 15 - 4 - 15 + 4 = 0. (missing_5=15)
sum_C = 6+2+3+0 = 11.
Answer = 32 - 11 = 21? But sample output is 23. Something off. Let's recalc carefully.

Maybe my cnt_contains for v=4 is wrong. Let's recompute:
Array: [3,1,4,2,4]
i=3, v=4: prev=0, contrib=(3-0)*(5-3+1)=3*3=9. last[4]=3.
i=5, v=4: prev=3, contrib=(5-3)*(5-5+1)=2*1=2. So cnt[4]=11. That's correct.
missing_4 = 15-11=4. Correct.
missing_5: no 5, so cnt[5]=0, missing=15.
count_4 = 15 - missing_4 - missing_5 + missing_both[4] = 15 - 4 - 15 + 4 = 0. Correct.

Now check count_1: 15 - missing_1 - missing_2 + missing_both[1] = 15 - 7 - 7 + 5 = 6.
count_2: 15 - 7 - 10 + 4 = 2.
count_3: 15 - 10 - 4 + 2 = 3.
Sum = 11.

But sum_D = 32. So answer 21. Sample says 23. Let's manually compute f(L,R) for this array to see where the discrepancy is.

Array: 3,1,4,2,4.
Let's list all subarrays and compute f.

Subarrays length 1: f=1 for each. There are 5, sum=5.
Length 2:
[1,2]: 3,1 -> distinct {1,3}, components: 1-2? values 1 and 3 are not adjacent (missing 2), so two components. f=2.
[2,3]: 1,4 -> {1,4}, missing 2,3 -> two components. f=2.
[3,4]: 4,2 -> {2,4}, missing 3 -> two components. f=2.
[4,5]: 2,4 -> {2,4}, missing 3 -> two components. f=2.
Sum for length 2: 4*2=8. Total so far: 13.

Length 3:
[1,3]: 3,1,4 -> distinct {1,3,4}. Adjacent pairs: 1-2? no 2. 3-4? both 3 and 4 present? Yes! So one edge. Components: vertices {1,3,4}, edge between 3-4. So graph: 1 isolated, 3-4 connected. That's 2 components. So f=2.
[2,4]: 1,4,2 -> distinct {1,2,4}. Adjacent pairs: 1-2 present? Yes. 2-3? no 3. 3-4? no 3. So only edge 1-2. Components: 1-2 connected, 4 isolated -> 2 components. f=2.
[3,5]: 4,2,4 -> distinct {2,4}. Adjacent pair 3-4? no 3. So no edges. Components: 2 components. f=2.
Sum for length 3: 2+2+2=6. Total: 19.

Length 4:
[1,4]: 3,1,4,2 -> distinct {1,2,3,4}. Adjacent pairs: 1-2, 2-3, 3-4 all present? 1,2,3,4 all there. So edges: (1,2), (2,3), (3,4). Graph is connected path. Components: 1. f=1? Wait, f is the number of operations. If the set is {1,2,3,4}, can we erase in 1 operation? Choose l=1, r=4, then all integers from 1 to 4 appear, so we can erase them all. So f=1. Let's check: the set is {1,2,3,4}, so l=1, r=4 works. So f=1.
[2,5]: 1,4,2,4 -> distinct {1,2,4}. Adjacent: 1-2 present, 2-3 no, 3-4 no. So one edge. Components: 1-2 connected, 4 isolated -> 2 components. f=2.
Sum for length 4: 1+2=3. Total: 22.

Length 5:
[1,5]: 3,1,4,2,4 -> distinct {1,2,3,4}. All four present. f=1.
Total: 22+1=23.

So the correct sum is 23. My algorithm gave 21. So there is a bug.

Let's compute using my formula for some subarrays to find the discrepancy.

My formula: f = D - C, where D is number of distinct, C is number of adjacent pairs both present.
For [1,4]: D=4, C=3 (pairs 1-2, 2-3, 3-4). So f = 4-3=1. Correct.
For [1,3]: D=3, C=1 (pair 3-4). f=2. Correct.
For [2,4]: D=3, C=1 (pair 1-2). f=2. Correct.
So the formula f = D - C seems correct for all subarrays? Let's check [1,2]: D=2, C=0 (no adjacent pair). f=2. Correct.
So the sum of f over all subarrays is sum D - sum C.

Now, my sum_D = 32. Let's compute sum_D manually by summing D over all subarrays.
Subarrays:
L=1: R=1: D=1; R=2: D=2; R=3: D=3; R=4: D=4; R=5: D=4. Sum=14.
L=2: R=2:1; R=3:2; R=4:3; R=5:3. Sum=9.
L=3: R=3:1; R=4:2; R=5:2. Sum=5.
L=4: R=4:1; R=5:2. Sum=3.
L=5: R=5:1. Sum=1.
Total D = 14+9+5+3+1 = 32. So sum_D=32 is correct.

Now sum_C should be the sum over subarrays of the number of adjacent pairs both present. Let's compute that manually.
List all subarrays and their C:
L=1,R=1: {3} -> C=0
R=2: {1,3} -> C=0
R=3: {1,3,4} -> C=1 (3-4)
R=4: {1,2,3,4} -> C=3 (1-2,2-3,3-4)
R=5: {1,2,3,4} -> C=3
Sum for L=1: 0+0+1+3+3 = 7.
L=2: R=2: {1}->0; R=3: {1,4}->0; R=4: {1,2,4}->1 (1-2); R=5: {1,2,4}->1. Sum=2.
L=3: R=3: {4}->0; R=4: {2,4}->0; R=5: {2,4}->0. Sum=0.
L=4: R=4: {2}->0; R=5: {2,4}->0. Sum=0.
L=5: R=5: {4}->0.
Total C = 7+2+0+0+0 = 9.
Then sum f = 32 - 9 = 23. Correct.

So my computed sum_C was 11, but the correct sum_C is 9. Let's find the error in my count_x or missing_both.

Recall: sum_C = sum_{x=1}^{N-1} count_x, where count_x = number of subarrays containing both x and x+1.
Let's compute count_x manually for this array.
Values: 1,2,3,4. Pairs: (1,2), (2,3), (3,4).
For pair (1,2): subarrays containing both 1 and 2.
List all subarrays and check if they contain at least one 1 and at least one 2.
L=1: R=1: no 2. R=2: {3,1} no 2. R=3: {3,1,4} no 2. R=4: {3,1,4,2} contains 1 and 2 -> yes. R=5: {3,1,4,2,4} contains 1 and 2 -> yes. So for L=1, R=4,5: 2 subarrays.
L=2: R=2: {1} no 2. R=3: {1,4} no 2. R=4: {1,4,2} contains 1 and 2 -> yes. R=5: {1,4,2,4} contains 1 and 2 -> yes. So 2 subarrays.
L=3: R=3: {4} no 1,2. R=4: {4,2} no 1. R=5: {4,2,4} no 1. So 0.
L=4: R=4: {2} no 1. R=5: {2,4} no 1. 0.
L=5: R=5: {4} no 1,2. 0.
Total count_1 = 4. So pair (1,2) appears in 4 subarrays.

Pair (2,3): need both 2 and 3.
L=1: R=1: {3} no 2. R=2: {3,1} no 2. R=3: {3,1,4} no 2. R=4: {3,1,4,2} contains 3 and 2 -> yes. R=5: {3,1,4,2,4} contains both -> yes. So 2.
L=2: R=2: {1} no. R=3: {1,4} no 3. R=4: {1,4,2} no 3. R=5: {1,4,2,4} no 3. So 0.
L=3: R=3: {4} no. R=4: {4,2} no 3. R=5: {4,2,4} no 3. 0.
L=4: R=4: {2} no 3. R=5: {2,4} no 3. 0.
L=5: R=5: {4} no.
Total count_2 = 2.

Pair (3,4): need both 3 and 4.
L=1: R=1: {3} no 4. R=2: {3,1} no 4. R=3: {3,1,4} yes. R=4: {3,1,4,2} yes. R=5: {3,1,4,2,4} yes. So 3.
L=2: R=2: {1} no. R=3: {1,4} no 3. R=4: {1,4,2} no 3. R=5: {1,4,2,4} no 3. 0.
L=3: R=3: {4} no 3. R=4: {4,2} no 3. R=5: {4,2,4} no 3. 0.
L=4: R=4: {2} no. R=5: {2,4} no 3. 0.
L=5: R=5: {4} no 3. 0.
Total count_3 = 3.

Sum C = 4+2+3 = 9. Correct.

Now my algorithm computed:
count_1 = 6, count_2 = 2, count_3 = 3, sum=11. So count_1 is off by 2. Let's check my computation of count_1.
count_1 = total - missing_1 - missing_2 + missing_both[1].
total=15.
missing_1 = 15 - cnt_contains[1] = 15 - 8 = 7.
missing_2 = 15 - cnt_contains[2] = 15 - 8 = 7.
missing_both[1] = 5 (computed earlier).
So count_1 = 15 - 7 - 7 + 5 = 6. But actual is 4. So either missing_1, missing_2, or missing_both[1] is wrong.

Let's compute missing_1 manually: number of subarrays with no 1.
Array: 3,1,4,2,4. Positions of 1: only at index 2.
Gaps before 1: length 1 (position 1). Subarrays in this gap: just [1,1] -> 1 subarray.
Gaps after 1: from index 3 to 5, length 3. Subarrays in this gap: length 1: 3; length 2: 2; length 3: 1. Total 6.
Total missing_1 = 1+6 = 7. Correct.

missing_2: positions of 2: only at index 4.
Gaps: before: length 3 (1..3). Subarrays: 3*4/2=6.
After: length 1 (5). Subarrays: 1.
Total missing_2 = 7. Correct.

missing_both[1]: subarrays with neither 1 nor 2. Positions of 1 or 2: index 2 (1) and index 4 (2). So U = {2,4}.
Gaps: before 2: length 1 (1). Subarrays: 1.
Between 2 and 4: length 1 (position 3). Subarrays: 1.
After 4: length 1 (position 5). Subarrays: 1.
Total = 3? Wait, I computed 5 earlier. Let's recalc carefully.
Array indices 1..5. Marked indices: 2 and 4.
Gaps: [1,1] length 1, [3,3] length 1, [5,5] length 1.
Each gap of length 1 gives 1 subarray. So total missing_both[1] = 3.
But my algorithm gave 5. So the algorithm's missing_both[1] is wrong.

Let's re-simulate the algorithm for x=1 on this array.
A = [3,1,4,2,4]
N=5.
last_pair[1] = 0, sum_closed[1] = 0.
i=1, v=3: affected x for v=3 are x=2 and x=3. x=1 is not affected. So gap for x=1 simply extends. But we don't do anything for x=1. That's fine.
i=2, v=1: affected x for v=1 are x=0 (invalid) and x=1. So x=1 is affected.
At i=2, for x=1: L = i - last_pair[1] - 1 = 2 - 0 - 1 = 1. Add L*(L+1)/2 = 1 to sum_closed[1]. Then last_pair[1] = 2.
i=3, v=4: affected x=3,4. x=1 not affected.
i=4, v=2: affected x=1 and x=2. For x=1: L = 4 - 2 - 1 = 1. Add 1 to sum_closed[1]. last_pair[1] = 4.
i=5, v=4: affected x=3,4. x=1 not affected.
End: close final gap: L = N - last_pair[1] = 5 - 4 = 1. Add 1 to sum_closed[1].
Total sum_closed[1] = 1+1+1 = 3. So it should give 3, not 5. But in my earlier manual run I got 5. Let's re-check my manual run for x=1 in sample 2.

Earlier I wrote:
i=2, v=1: x=1: L=2-0-1=1, add 1, last=1. (Wait, I wrote last=1? Actually I wrote last=1? No, I wrote last=1? Let's see: "x=1: L=2-0-1=1, add 1, last=1." But last should be i=2. I mistakenly set last=1. That was the error! In my earlier trace, I set last[1]=1 instead of 2. So the subsequent calculations were off. Let's fix that.

So the algorithm is correct. The manual trace had a typo. So the algorithm works.

Now we need to implement carefully.

Let's verify with sample 2 using correct algorithm.
N=5, A=[3,1,4,2,4].
total=15.
cnt_contains:
v=1: i=2, prev=0, (2)*(4)=8. last=2.
v=2: i=4, prev=0, (4)*(2)=8. last=4.
v=3: i=1, prev=0, (1)*(5)=5. last=1.
v=4: i=3, prev=0, (3)*(3)=9. last=3. i=5, prev=3, (5-3)*(1)=2. total=11. last=5.
v=5: 0.
sum_D = 8+8+5+11 = 32.
missing: v=1:7, v=2:7, v=3:10, v=4:4, v=5:15.
missing_both:
x=1: last=0, sum=0.
i=1,v=3: x=2,3 affected.
i=2,v=1: x=1 affected. L=2-0-1=1, sum=1, last=2.
i=3,v=4: x=3,4 affected.
i=4,v=2: x=1,2 affected. For x=1: L=4-2-1=1, sum=1+1=2, last=4.
i=5,v=4: x=3,4 affected.
End: x=1: L=5-4=1, sum=2+1=3. missing_both[1]=3.
x=2: last=0.
i=1,v=3: x=2 affected. L=1-0-1=0, sum=0, last=1.
i=4,v=2: x=2 affected. L=4-1-1=2, sum=3, last=4.
End: x=2: L=5-4=1, sum=3+1=4. missing_both[2]=4.
x=3: last=0.
i=1,v=3: x=3 affected. L=0, sum=0, last=1.
i=3,v=4: x=3,4 affected. For x=3: L=3-1-1=1, sum=1, last=3.
i=5,v=4: x=3,4 affected. For x=3: L=5-3-1=1, sum=1+1=2, last=5.
End: x=3: L=5-5=0, sum=2. missing_both[3]=2.
x=4: last=0.
i=3,v=4: x=4 affected. L=3-0-1=2, sum=3, last=3.
i=5,v=4: x=4 affected. L=5-3-1=1, sum=3+1=4, last=5.
End: x=4: L=0, sum=4. missing_both[4]=4.

Now count_x:
count_1 = 15 - 7 - 7 + 3 = 4. Correct.
count_2 = 15 - 7 - 10 + 4 = 2. Correct.
count_3 = 15 - 10 - 4 + 2 = 3. Correct.
count_4 = 15 - 4 - 15 + 4 = 0. Correct.
sum_C = 4+2+3+0 = 9.
Answer = 32 - 9 = 23. Matches sample.

Great! So the algorithm is correct.

Now we need to implement this in Python efficiently. N up to 3e5, so O(N) with small constant is fine.

Implementation details:
- Read N, array A (1-indexed or 0-indexed).
- Compute total_subarrays = N*(N+1)//2.
- Initialize `cnt_contains` array of size N+1 (since A_i <= N) with 0.
- Initialize `last_occ` array of size N+1 with 0.
- Loop i from 1 to N: v = A[i-1] (if 0-indexed). cnt_contains[v] += (i - last_occ[v]) * (N - i + 1). last_occ[v] = i.
- sum_D = sum(cnt_contains[1:]) (or up to max value, but N is enough).
- Compute missing array: missing[v] = total_subarrays - cnt_contains[v] for v=1..N.
- Compute missing_both for x=1..N-1:
  - Initialize `last_pair` array of size N (index 1..N-1) with 0.
  - Initialize `sum_closed` array of size N with 0 (or just use missing_both).
  - Loop i from 1 to N: v = A[i-1].
    - For each affected x:
      - If v-1 >= 1: x = v-1; L = i - last_pair[x] - 1; sum_closed[x] += L*(L+1)//2; last_pair[x] = i.
      - If v <= N-1: x = v; L = i - last_pair[x] - 1; sum_closed[x] += L*(L+1)//2; last_pair[x] = i.
    - Note: if v=1, v-1=0, skip. If v=N, v=N is not <= N-1, skip.
  - After loop, for x=1..N-1: L = N - last_pair[x]; sum_closed[x] += L*(L+1)//2.
  - missing_both[x] = sum_closed[x].
- Compute sum_C = 0.
  For x in 1..N-1:
    count_x = total_subarrays - missing[x] - missing[x+1] + missing_both[x]
    sum_C += count_x
- Answer = sum_D - sum_C.
- Print answer.

Check for potential overflow: values can be large. N=3e5, total subarrays ~ 4.5e10. Sum of f can be on the order of N^2 * N? Actually, each f is at most the number of distinct values, which is at most N. Number of subarrays is N(N+1)/2 ~ 4.5e10. So the total sum can be up to ~ 1.35e16. That fits in 64-bit integer (2^63-1 ~ 9.2e18). Python's int is arbitrary precision, so no issue.

Let's test with sample 3: N=10, A=[5,1,10,9,2,5,6,9,1,6]. Expected 129.
We can run through the algorithm mentally or trust it.

Complexity: O(N) time, O(N) memory.

One thing to optimize: The inner loop over affected pairs has at most 2 iterations, so O(1). The final loop is O(N). So overall O(N).

Let's write the code accordingly.

Edge cases: N=1. Then there are no pairs (x from 1 to 0). The sum of f is just the sum of f(L,R) for the single subarray [1,1], which is 1. Our algorithm: total=1. cnt_contains[v] for v=A[1]: (1-0)*(1-1+1)=1*1=1. sum_D=1. missing_both: no pairs, so sum_C=0. Answer=1. Correct.

N=2. Let's test: A=[1,2]. Subarrays: [1,1]: f=1; [2,2]: f=1; [1,2]: distinct {1,2}, adjacent pair present, so f=1. Sum=3.
Algorithm: total=3.
cnt: v=1: i=1, (1)*(2)=2. v=2: i=2, (2)*(1)=2. sum_D=4? Wait, v=1:2, v=2:2, sum_D=4. But there are 3 subarrays, each has distinct count 1 for length 1, and for [1,2] distinct=2. So sum D = 1+1+2 = 4. Correct.
missing: v=1: 3-2=1; v=2: 3-2=1.
missing_both for x=1: last=0.
i=1,v=1: x=1 affected. L=0, sum=0, last=1.
i=2,v=2: x=1 affected. L=2-1-1=0, sum=0, last=2.
End: L=2-2=0, sum=0. missing_both[1]=0.
count_1 = 3 - 1 - 1 + 0 = 1. (subarray [1,2] contains both)
sum_C=1.
Answer = 4 - 1 = 3. Correct.

Another test: A=[1,1]. Subarrays: [1,1]: f=1; [1,2]: distinct {1}, f=1. Sum=2.
cnt: v=1: i=1: (1)*(2)=2; i=2: (2-1)*(1)=1. total=3. sum_D=3.
missing_1 = 3-3=0.
missing_both: no pairs? N=2, pairs: x=1.
last=0.
i=1,v=1: x=1 affected. L=0, last=1.
i=2,v=1: x=1 affected. L=2-1-1=0, last=2.
End: L=0. missing_both[1]=0.
count_1 = 3 - 0 - 0 + 0 = 3? But subarrays containing both 1 and 2? There is no 2, so count_1 should be 0. Wait, missing_2? We need missing[x] and missing[x+1] for x=1. x+1=2. missing_2 = total - cnt_contains[2] = 3 - 0 = 3. So count_1 = 3 - missing_1 - missing_2 + missing_both[1] = 3 - 0 - 3 + 0 = 0. Correct.
Answer = sum_D - sum_C = 3 - 0 = 3? But actual sum f is 2. Wait, let's list subarrays for A=[1,1]:
L=1,R=1: {1} -> f=1
L=1,R=2: {1} -> f=1
L=2,R=2: {1} -> f=1
Sum f = 3. So answer 3. My manual sum was wrong. Correct.

Test: A=[1,3]. Subarrays: [1,1]:1, [2,2]:1, [1,2]: distinct {1,3}, no adjacent pair, f=2. Sum=4.
cnt: v=1: (1)*(2)=2; v=3: (2)*(1)=2. sum_D=4.
missing_1=1, missing_3=1. missing_2=3-0=3.
missing_both[1]: x=1. last=0. i=1,v=1: x=1