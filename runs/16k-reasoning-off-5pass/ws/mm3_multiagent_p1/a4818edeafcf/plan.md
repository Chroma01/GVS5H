We split the array into three contiguous parts and want to maximize the sum of distinct counts. 
We can precompute the number of distinct elements in every prefix and every suffix in O(N) using sets visited left-to-right and right-to-left. 
Then for each possible middle cut `j` (the end of the middle subarray, with `j` from 2 to N-1), we can try all possible left cuts `i` (1 ≤ i < j). 
The left count is `pref[i]`, the middle count is `mid[i+1..j]`, and the right count is `suf[j+1]`. 
A naive O(N^2) would be too slow for N up to 3e5. We need a faster approach.

Let's think: for a fixed `j`, the right part's distinct count `suf[j+1]` is fixed. 
We want to maximize `pref[i] + distinct(i+1, j)` over `i < j`. 
We can precompute for each position the distinct count of suffixes of the form `distinct(i+1, j)`, but that's also too large.

Instead, observe that we can iterate `i` from left to right, maintaining a sliding window of distinct counts for the middle segment. 
Specifically, we can do a two-pointer or sweep: 
- Fix the right end of the middle segment `j`. 
- As we increase `i` from 1 to j-1, the set of elements in the middle segment `[i+1, j]` changes. 
- We can maintain the distinct count of the current middle segment while moving `i`. 
- However, moving `i` leftwards (decreasing i) makes the middle segment grow. That's not monotonic in a simple way if we fix j.

Better: iterate `i` from left to right, and for each `i`, we need to consider all `j > i`. 
The total number of pairs (i, j) is O(N^2), too many.

Alternative approach using divide and conquer or Mo's algorithm? 
The array is static. The function f(i, j) = pref[i] + distinct(i+1, j) + suf[j+1]. 
We need max over i < j.

We can try to fix the middle segment's distinct count incrementally. 
Notice that distinct(i+1, j) as j increases is non-decreasing, and as i increases it's non-increasing. 
But that doesn't directly help.

Another idea: Use the fact that A_i ≤ N. 
We can try to process the array and maintain for each possible value the latest occurrence? 
Maybe we can use a sweepline on the middle cut. 
For each j, we want max_{i < j} [pref[i] + distinct(i+1, j)]. 
If we can compute this quickly for all j, we add suf[j+1] and take max.

How to compute max_{i < j} [pref[i] + distinct(i+1, j)] efficiently? 
Consider the set of elements in (i, j]. 
As j increases by 1, the new element A_{j+1} is added to the middle segment for all i ≤ j. 
The distinct count for middle segment starting at i+1 and ending at j increases by 1 if A_{j+1} is not in (i+1..j). 
So for a fixed j, as we look at smaller i, the middle segment gets larger, and its distinct count can only increase. 
But pref[i] can vary.

Let's try to maintain an array best[i] = pref[i] + something. 
Actually, let's think backwards. 
Fix i. The middle segment is (i, j]. As j goes from i+1 to N-1, the distinct count of the middle segment increases. 
We need to find j that maximizes pref[i] + mid_distinct(i+1, j) + suf[j+1].

We can precompute suf array (distinct count in suffix). 
For each i, we could iterate j, but that's O(N^2).

Maybe we can use a segment tree or a data structure. 
For each j, we need to query over i < j. 
The expression is pref[i] + distinct(i+1, j) + suf[j+1]. 
Let's denote for a fixed j, we want to maximize over i: pref[i] + distinct(i+1, j). 
The term distinct(i+1, j) depends on j. 
As we move from j to j+1, the middle segment gains A_{j+1}. 
For a given i, distinct(i+1, j+1) = distinct(i+1, j) + (1 if A_{j+1} not in (i+1, j) else 0). 
So it's like we need to add 1 to some prefix of i's. Specifically, to those i such that A_{j+1} does not appear in (i+1, j). 
That means i < last occurrence of A_{j+1} in the range (i+1, j). 
Actually, for i such that the last occurrence of A_{j+1} in (i, j] is at position j+1 (i.e., it hasn't appeared in (i+1, j)), then distinct increases by 1. 
Otherwise, it doesn't change.

This is getting complicated.

Alternative perspective: The problem is similar to splitting into two parts (Problem C), where we compute distinct counts of prefixes and suffixes, and for each i, the sum is pref[i] + suf[i+1]. Then answer is max. 
For three parts, we need to choose two cut points. 
We can iterate the middle cut j (the end of the middle part). For each j, we want to maximize over i < j: pref[i] + distinct(i+1, j) + suf[j+1]. 
If we can compute the maximum of pref[i] + distinct(i+1, j) efficiently for all j, we can then add suf[j+1] and take max.

How to compute max_{i < j} (pref[i] + distinct(i+1, j))? 
Let's define for each position p, a value val[p] that we can maintain. 
We can think of the middle segment's distinct count as we expand from left to right. 
Actually, consider fixing i and looking at the middle segment as j increases. 
We can precompute for each i, an array of when each value appears. 
Maybe we can do a two-pointer: For each j, we want to find the best i. 
The distinct(i+1, j) is the number of distinct elements in the window (i, j]. 
As i decreases, the window grows, so distinct count is non-decreasing. 
pref[i] is arbitrary. 
So for a fixed j, as we go i from j-1 down to 1, distinct(i+1, j) is non-decreasing, but pref[i] is just the prefix distinct count. 
The sum might not be unimodal.

But maybe we can use a segment tree where we maintain for each i the current value of pref[i] + distinct(i+1, current_j). 
As we increase j, we update the values for i: for each i < j, if A_{j} is not in (i, j-1], then distinct(i+1, j) = distinct(i+1, j-1) + 1, else same. 
So we need to add 1 to all i such that the last occurrence of A_j before position j is ≤ i. 
That is, i < last_occurrence[A_j] where last_occurrence is the previous index of A_j before j. 
Wait: if A_j has last occurrence at position p, then for any i < p, the element A_j is not in (i, j-1] because the last occurrence is at p > i? Actually, if i < p, then A_j is in (i, j-1] if p > i. So A_j is in (i+1, j-1] if p ≥ i+1. So for i < p, A_j is already present in the middle segment. For i ≥ p, A_j is not present. 
So as we move j to j+1, we add 1 to distinct(i+1, j+1) for those i ≥ p, where p is the previous occurrence of A_{j+1} (or 0 if none). 
More precisely: let prev = last index < j+1 where A[prev] = A[j+1], or 0 if none. 
Then for i = 1..prev, the element A[j+1] is already in (i+1, j] (since prev ≥ i+1 for i ≤ prev-1, and for i=prev, prev is in (i+1, j]? Wait, i+1 = prev+1 if i=prev, so the element at prev is not in (i+1, j] if i=prev. So for i ≤ prev, the element A[j+1] is in (i+1, j]? Let's check: 
We want to know if A[j+1] is in the interval (i, j] (since middle is from i+1 to j). 
If i < prev, then the interval (i, j] includes prev, so yes. 
If i = prev, then (prev, j] starts after prev, so does not include prev, so A[j+1] is not in the interval. 
If i > prev, then definitely not in the interval. 
So the condition for A[j+1] NOT being in (i, j] is i ≥ prev. 
Thus, when we go from j to j+1, the distinct count for middle segment starting at i+1 increases by 1 if i ≥ prev. 
So we can maintain an array add[i] for i=1..N. Initially, for j=1, middle segment is from i+1 to 1? But j must be at least 2 for the first cut. Let's set up properly.

We want to iterate j from 2 to N-1 (the end of the middle segment). 
For each j, we need the value for all i < j. 
We can maintain an array mid_val[i] representing pref[i] + distinct(i+1, j). 
Initially, for j=1? Not valid. Let's start with j=1? But j must be ≥2. 
Alternatively, we can initialize for j=1: the middle segment is empty? But we need j > i, so i < j. For j=1, i can only be 0, invalid. 
So we start with j=2. For j=2, i can be 1. 
The middle segment is from 2 to 2, which is just A_2. 
So for i=1: pref[1] + distinct(2,2) = pref[1] + 1. 
And for i=0 (invalid). 
We can maintain a data structure (like a segment tree) over i=1..N. 
When we move j to j+1, we need to update the values for i=1..j (since i < j+1). 
The update is: for all i in [prev, j] (where prev is last occurrence of A[j+1] before j+1, or 0 if none), we add 1 to the distinct count part. Actually, for i ≥ prev, we add 1. But careful: i ranges from 1 to j. For i > j, we don't care yet. 
So we need to add 1 to the range i = max(prev, 1) to j. 
But note: for i < prev, the value doesn't change. 
Also, we need to ensure that the pref[i] part is constant. So we can store for each i a base value pref[i], and an additional offset that we update. 
We can maintain a segment tree that stores for each i the total value (pref[i] + offset[i]), and we need to query the maximum over i=1..j-1. 
When we move j to j+1, we do: range add 1 to i in [prev, j] (since for i in this range, the new element A[j+1] is not in the previous middle segment). 
Wait, check: For i in [prev, j], the previous middle segment was (i, j] before adding A_{j+1}? Actually, before adding, the middle segment was (i, j]. When we add A_{j+1} to the array, the new middle segment is (i, j+1] (since j increases). 
The new element A_{j+1} is not in (i, j] if i ≥ prev. 
So yes, we add 1 to the distinct count for i in [prev, j]. 
But we must be careful: when i = j, the middle segment is (j, j+1] which is just A_{j+1}. The previous middle segment for i=j was (j, j] which is empty, so distinct count goes from 0 to 1, so +1. And prev is the last occurrence of A_{j+1} before j+1. If prev ≤ j, then i=j is in [prev, j], so we add 1. Correct. 
If prev = 0, then range is [1, j], all i from 1 to j get +1, which is correct because A_{j+1} is new to all middle segments. 
So the algorithm:
- Compute pref[i] for i=1..N: distinct elements in A[1..i].
- Compute suf[i] for i=1..N: distinct elements in A[i..N]. (We need suf[j+1])
- Initialize a segment tree (or Fenwick tree? But we need range add and range max query) over i=1..N. 
  We can use a segment tree with lazy propagation for range add and query max. 
  Initially, for i=1..N, the value is pref[i] (since for j=1, the middle segment is empty, distinct=0, but j starts at 2, so we need to set initial values for the first j=2? Let's think: 
  When j=2, the middle segment is from i+1 to 2. For i=1, it's A_2. So the offset for i=1 should be 1 (distinct of A_2). For i=0 invalid. For i>2, not valid yet. 
  We can start with j=1 as a base: middle segment empty, offset=0. Then for j=2, we do the update: prev = last occurrence of A_2 before index 2. Since A_2 is at index 2, the last occurrence before 2 is 0. So we add 1 to range [0, 1]? Actually, range is [prev, j-1]? Let's be precise.
  
Let's set j as the current end of the middle segment. Initially, j=1 (meaning the middle segment is up to index 1, but since we need j ≥ 2 for the first valid cut, we can start with j=1 and then update to j=2). 
For a given j, the middle segment is (i, j] for i < j. 
The number of distinct elements in (i, j] is what we want. 
We can maintain an array D[i] = distinct(i+1, j) for the current j. 
Initially, j=1: for i=1, the interval (1,1] is empty, so D[1]=0. But i must be < j, so for j=1, no valid i. So we can just set D[i]=0 for all i, and j=1. 
Then, to move to j+1, we need to update D[i] for all i < j+1. 
The new element is A_{j+1}. It will be included in the middle segment for all i < j+1. 
It increases the distinct count by 1 if it was not already in (i, j]. 
As derived, it is not in (i, j] if i ≥ prev, where prev is the last index < j+1 with A[prev] = A[j+1] (or 0). 
So for i in [prev, j] (since i < j+1, so i ≤ j), we add 1 to D[i]. 
Note: for i > j, we don't care because i must be < j+1, so i ≤ j. 
So the update range is i from prev to j. 
But careful: if prev = 0, we start from 1. 
So we do range add [max(prev,1), j] of +1. 
But wait: what if prev > j? Then the range is empty, no update. 
Also, we need to ensure that for i > j, we don't query them. So we can query max over i=1..j (since i < j+1, the valid i for the next j+1 are 1..j). 
But when we are at j, the valid i are 1..j-1. So we should query over i=1..j-1. 
So after updating to j+1, we query the max over i=1..j (which are the valid i for j+1), add suf[j+2]? Wait: the right part is from j+2 to N. The distinct count of the right part is suf[j+2]. 
So for each j from 2 to N-1 (since we need at least one element in the right part, so j+1 < N, i.e., j ≤ N-2? Actually, the right part is A_{j+1}..A_N, so it must be non-empty, so j+1 ≤ N, i.e., j ≤ N-1. And the middle part must be non-empty, so i < j and j > i, so j ≥ 2. And left part non-empty, so i ≥ 1. So j ranges from 2 to N-1. 
For each such j, we consider all i from 1 to j-1. 
Our query after updating to j (i.e., middle segment up to j) should be over i=1..j-1. 
So the steps:
- Initialize data structure for j=1: all D[i]=0, query over i=1..0 (empty, ignore). 
- For j from 1 to N-1 (or up to N-2 for final answer? Let's do j from 1 to N-2 for the answer, but we need to update up to N-1 for the right part? Actually, for the answer, we consider j from 2 to N-1. So we need to have the state for j=2,3,...,N-1. 
So we can start with j=1, then for j=1,2,...,N-2, we update to j+1, then query for that j+1. 
At j=1, after update we have state for j=2. Then query max over i=1..1 (since j=2, i<2 means i=1). Then answer candidate = that max + suf[3]? Wait: for j=2, the right part starts at j+1=3. So we add suf[3]. 
For j=3, we update from j=2 to j=3, then query over i=1..2, add suf[4]. 
So in general, after updating to j (where j goes from 2 to N-1), we query max over i=1..j-1, and add suf[j+1] (since right part is A_{j+1}..A_N). 
But suf array: let's define suf[k] = number of distinct elements in A[k..N]. Then for right part starting at j+1, we need suf[j+1]. 
So we need suf[3] for j=2, suf[4] for j=3, ..., suf[N] for j=N-1. 
We can precompute suf array of size N+2 for safety. 
Also, we need to handle the update: when moving from j to j+1, we add 1 to D[i] for i in [prev, j] where prev is last occurrence of A[j+1] before j+1. 
But careful: the update should be done before the query for the new j. 
So loop:
prev_occurrence = array of size N+1 initialized to 0.
Initialize segment tree with values: for i=1..N, value = pref[i]. (This is base value, since D[i] is initially 0, so total value = pref[i] + 0)
But note: for j=1, the valid i are none. For j=2, after update, we query i=1..1. 
But for i=1, the value should be pref[1] + D[1]. D[1] after update from j=1 to j=2: 
j=1, update with j+1=2: prev = last occurrence of A[2] before 2. If A[2] hasn't appeared, prev=0. So we add 1 to D[i] for i in [prev, j] = [0,1] = [1,1] (since i starts at 1). So D[1] becomes 1. So total value for i=1 is pref[1] + 1. That matches: distinct(2,2) = 1. 
So it's correct.
We need to maintain the D[i] separately? Actually, we can just store the total value in the segment tree: initially total = pref[i] + 0. Then we do range adds. 
But we must be careful: the range add for j+1 should be applied to i from max(prev, 1) to j. But what if j=1? Then range is from prev to 1. If prev=0, then [1,1] is valid. If prev=1, then range is [1,1] as well? Actually, if prev=1, that means A[2] appeared at position 1. Then for i=1, the middle segment is (1,2] which includes both positions? Wait, i=1, middle is from 2 to 2. The element A[2] is at position 2. The previous occurrence is at 1. So for i=1, the element A[2] is not in the previous middle segment (which was empty) because previous middle segment was (1,1] empty. So actually, even if prev=1, we should add 1? Let's check: 
We have i=1. The previous middle segment is (1,1] = empty. A[2] is not in empty set. So distinct count becomes 1. So we add 1. 
But our condition was i ≥ prev. For i=1, prev=1, so i ≥ prev is true. So we add 1. So the range should be [prev, j]? But for i=1, prev=1, j=1, so range is [1,1]. That works. 
But wait, what about i=0? Not valid. 
So the range is i from prev to j. But we need to ensure that if prev=0, we start from 1. So range is [max(prev,1), j]. 
But is it correct for prev > j? Then range is empty, no add. That happens if the previous occurrence is after the current i? Actually, if prev > j, that means the last occurrence of A[j+1] is at a position > j, which is impossible because we are looking at occurrences before j+1. The last occurrence before j+1 is at some index ≤ j. So prev ≤ j. So the range is never empty in that sense. But if prev = j+1? No, prev < j+1, so prev ≤ j. So range is always non-empty? Not necessarily: if the element hasn't occurred, prev=0, then range is [1, j], non-empty. If it occurred, prev ≥ 1 ≤ j, so range is [prev, j], non-empty. So always non-empty. 
But we must cap the range to valid i: i < j+1, so i ≤ j. So range is [max(prev,1), j]. 
But what if prev = 0? Then range is [1, j]. That's fine. 
So the update is: let prev = last_occurrence[A[j+1]]; then add 1 to interval [max(prev, 1), j]. 
After the update, we query the segment tree for the maximum over i in [1, j]. Because the valid i for this j (as the end of middle) are 1..j-1. Wait: for j (the new j), the middle segment ends at j, and i must be < j, so i ≤ j-1. So we should query over i=1..j-1. 
In our loop, after updating to j+1, we set j = j+1, then we query i=1..j-1. 
So in the loop variable: let's use cur_j as the current end of the middle segment. 
Initialize: for all i, value = pref[i]. (This corresponds to cur_j = 0? Actually, for cur_j=0, the middle segment is empty, so D[i]=0. But we need to have a base. We can start with cur_j=1: then the middle segment is (i,1] which is empty. So D[i]=0. So we can set initial values = pref[i] + 0. But we need to be able to update to cur_j=2. So initially, we set cur_j=1. Then in the loop, for cur_j from 1 to N-2, we do: update to cur_j+1, then query max over i=1..cur_j (since for new cur_j = cur_j+1, the valid i are 1..cur_j). Then compute answer candidate = that max + suf[cur_j+2] (because right part starts at cur_j+2). 
Wait: if we update to cur_j+1, then the new cur_j is cur_j+1. The right part starts at cur_j+2. So we add suf[cur_j+2]. 
Let's test with small example. 
N=5, A=[3,1,4,1,5]
pref: [1,2,3,3,4] (distinct counts for prefixes 1,2,3,4,5)
suf: 
suf[6]=0
suf[5]=1 (5)
suf[4]=2 (1,5)
suf[3]=2 (4,1,5)
suf[2]=3 (1,4,1,5) -> distinct: 1,4,5 = 3
suf[1]=4 (3,1,4,1,5) -> 3,1,4,5 = 4
Actually, we need suf array where suf[k] = distinct in A[k..N]. 
So:
k=1: [3,1,4,1,5] -> {3,1,4,5} = 4
k=2: [1,4,1,5] -> {1,4,5} = 3
k=3: [4,1,5] -> {4,1,5} = 3? Wait, 1 and 4 and 5, yes 3.
k=4: [1,5] -> {1,5} = 2
k=5: [5] -> 1
k=6: [] -> 0
So suf[1]=4, suf[2]=3, suf[3]=3, suf[4]=2, suf[5]=1, suf[6]=0.

Now algorithm:
Initialize values: for i=1..5: val = pref[i] = [1,2,3,3,4]
cur_j = 1
last_occ array for values 1..5 initialized to 0.
Loop:
Iteration 1: cur_j=1, we update to cur_j+1=2. 
  Element A[2] = 1. prev = last_occ[1] = 0. 
  Add 1 to range [max(0,1), cur_j=1] = [1,1]. 
  So val[1] becomes 1+1=2. val[2..5] unchanged.
  Then cur_j becomes 2. 
  Query max over i=1..cur_j-1 = i=1..1. val[1]=2. 
  Candidate = 2 + suf[cur_j+1] = suf[3] = 3. So 2+3=5. 
  Update last_occ[1] = 2.

Iteration 2: cur_j=2, update to cur_j+1=3.
  Element A[3] = 4. prev = last_occ[4] = 0.
  Add 1 to range [1, cur_j=2] = [1,2]. 
  val[1] becomes 3, val[2] becomes 3. 
  cur_j=3. Query max over i=1..2: max(3,3)=3.
  Candidate = 3 + suf[4] = 2. So 3+2=5.
  Update last_occ[4] = 3.

Iteration 3: cur_j=3, update to cur_j+1=4.
  Element A[4] = 1. prev = last_occ[1] = 2.
  Add 1 to range [max(2,1)=2, cur_j=3] = [2,3].
  val[2] becomes 4, val[3] becomes 4? Wait, val[3] was 3 (from pref[3]=3) + updates? Actually, val[3] initially 3. In iteration 2, we added 1 to range [1,2], so val[3] not updated. So val[3]=3. Now add 1 to [2,3]: val[2] becomes 3+1=4, val[3] becomes 3+1=4.
  cur_j=4. Query max over i=1..3: max(val[1]=3, val[2]=4, val[3]=4) = 4.
  Candidate = 4 + suf[5] = 1. So 4+1=5.
  Update last_occ[1] = 4.

Iteration 4: cur_j=4, update to cur_j+1=5.
  Element A[5] = 5. prev = last_occ[5] = 0.
  Add 1 to range [1, 4] = [1,4].
  val[1] becomes 4, val[2] becomes 5, val[3] becomes 5, val[4] becomes 4 (since pref[4]=3 + 1 from iteration 3? Wait, val[4] initially pref[4]=3. In iteration 3, we added to [2,3] only, so val[4]=3. Now add 1 to [1,4]: val[4] becomes 4.
  cur_j=5. Query max over i=1..4: max(4,5,5,4)=5.
  Candidate = 5 + suf[6] = 0. So 5+0=5.
  But note: for cur_j=5, the right part starts at 6, which is empty. But we need the right part to be non-empty. So we should only consider cur_j up to N-1? In this loop, we went up to cur_j=5, but the right part is empty. So we should stop the loop at cur_j = N-1. That is, we should only consider j from 2 to N-1. So the last valid j is N-1. In the loop, we update to cur_j+1, and then query. So we need to do the update and query for cur_j from 2 to N-1. That means we start with cur_j=1, and then for cur_j=1, we update to 2, query for j=2. Then cur_j=2, update to 3, query for j=3. ... cur_j=N-2, update to N-1, query for j=N-1. So the loop should run for cur_j = 1, 2, ..., N-2. Then we don't do the update to N. So in the above, for N=5, we should have iterations for cur_j=1,2,3. That gives j=2,3,4. For j=5, we don't consider because right part would be empty. So we stop at cur_j=3 (N-2=3). 
So the maximum candidate was 5 from j=2,3,4. That matches sample output 5. 
But we also got a candidate 5 from j=4, which is valid? For j=4, the right part is A[5..5] which is non-empty. So yes, j=4 is valid. So the answer is 5. 
Our loop would give candidates for j=2,3,4. The candidate for j=4 is 5, which is correct. 
So the loop should be: 
cur_j = 1
for step in range(N-1):  # actually we need N-2 steps
    # update to cur_j+1
    next_j = cur_j + 1
    prev = last_occ[A[next_j]]
    add 1 to range [max(prev,1), cur_j]
    cur_j = next_j
    if cur_j >= 2 and cur_j <= N-1:  # always true since we start at 1 and go to N-1? Actually, if we run N-2 steps, cur_j goes from 2 to N-1.
        query max over i=1..cur_j-1
        candidate = max_val + suf[cur_j+1]
        ans = max(ans, candidate)
But careful: when cur_j = N-1, the query is over i=1..N-2, and we add suf[N]. That is valid because right part is A[N..N] non-empty. 
So we can just run for cur_j from 2 to N-1, and for each, we have the state after update. 
Implementation: 
- Precompute pref[1..N] and suf[1..N+1].
- Initialize an array val[1..N] with val[i] = pref[i].
- Initialize last_occ[1..N] = 0 (since A_i ≤ N).
- Initialize a segment tree over i=1..N with values val[i]. We need to support range add and range max query.
- ans = 0.
- For j from 2 to N-1:
    - prev = last_occ[A[j]]
    - add 1 to range [prev, j-1] but cap lower bound to 1. Actually, the range is [max(prev,1), j-1]? Wait, in the update, we said range is [max(prev,1), j] where j is the old j? Let's re-index.
In the loop, we are at j (the new j). Before the update, we were at j-1. The update for the new element A[j] (since we are moving to j) should add 1 to D[i] for i in [prev, j-1] because the valid i for the new middle segment (ending at j) are i < j, so i ≤ j-1. And the condition is i ≥ prev. So range is [max(prev,1), j-1].
But in our earlier step-by-step, we updated to cur_j+1, and the range was [max(prev,1), cur_j] where cur_j was the old j. So if we are iterating j from 2 to N-1, and we want the state for j, we need to have applied the update for A[j]. That update should be based on the previous j-1. So we can do:
- Start with j=1, but we don't query.
- For j from 2 to N-1:
    - Apply update for A[j]: let prev = last_occ[A[j]]; then add 1 to range [max(prev,1), j-1].
    - Query max over i=1..j-1.
    - candidate = that max + suf[j+1].
    - ans = max(ans, candidate).
    - Update last_occ[A[j]] = j.
This is cleaner. 
But we need to ensure that the initial state (before any updates) corresponds to j=1. For j=1, the middle segment is empty, so D[i]=0. Our val[i] = pref[i] + 0. So that's correct. 
Now, when we apply the update for j=2: prev = last_occ[A[2]] (which is 0 initially). We add 1 to range [max(0,1)=1, j-1=1]. So we add 1 to val[1]. That gives val[1] = pref[1] + 1, which is correct for middle segment (2,2). 
Then query max over i=1..1: val[1]. 
So this works. 
We need to be careful: the range update for j should be applied to i in [max(prev,1), j-1]. But what if prev = 0? Then we start at 1. If prev > j-1, then the range is empty? Actually, prev is the last occurrence before j, so prev ≤ j-1. So the range is always non-empty if prev ≥ 1. If prev = 0, then range is [1, j-1], which is non-empty. So it's fine. 
But we must ensure that we don't update i > j-1. So the upper bound is j-1. 
Now, the segment tree: we need to support range add and range max query. 
N up to 3e5, so O(N log N) is fine. 
We also need to store the values. 
Let's test with the second sample: 
N=10, A=[2,5,6,4,4,1,1,3,1,4]
We can compute manually later, but the algorithm should give 9. 
Now, we need to implement the segment tree. 
We'll build a segment tree with size N. The values are initially pref[i]. 
We need to do range add: add v to all elements in [l, r]. 
And range max query: max over [l, r]. 
We'll use lazy propagation. 
Let's code.

We need to be careful with 1-indexing. 
pref[i] for i=1..N: number of distinct in A[1..i]. 
suf[i] for i=1..N+1: number of distinct in A[i..N]. suf[N+1]=0. 
We can compute pref by iterating left to right, using a set or boolean array. Since A_i ≤ N, we can use a boolean array of size N+1. 
Similarly for suf, iterate right to left. 
Now, segment tree: 
We can implement as a class with n, tree (max), lazy (add). 
Operations: 
- build: initialize tree[i] = pref[i] for leaves. 
- range_add(l, r, val)
- range_max(l, r)

Now, main loop:
last_occ = [0] * (N+1)  # since A_i ≤ N
ans = 0
for j in range(2, N):  # j from 2 to N-1 inclusive
    prev = last_occ[A[j]]
    l = max(prev, 1)
    r = j - 1
    if l <= r:
        seg.range_add(l, r, 1)
    # query max over i=1..j-1
    max_val = seg.range_max(1, j-1)
    candidate = max_val + suf[j+1]
    if candidate > ans:
        ans = candidate
    last_occ[A[j]] = j

Print ans.

But we need to handle the case when N=3. Then loop runs for j=2 only. 
For j=2, we update with A[2], then query over i=1..1, add suf[3]. That works. 
Now, we need to ensure that suf array is computed correctly. 
suf[i] for i=N+1 is 0. 
We'll compute suf by iterating from N down to 1, maintaining a set or boolean array. 
Since we need suf[j+1] for j up to N-1, we need suf[N] to be computed. 
For j=N-1, we need suf[N]. 
So we compute suf of size N+2, with suf[N+1]=0. 
We'll iterate i from N down to 1, update boolean array, and set suf[i] = current distinct count. 
Also, we need to ensure that the segment tree is built with pref. 
pref: iterate i from 1 to N, update boolean array, set pref[i] = current distinct count. 
Now, the values A_i are up to N, so we can use boolean arrays of size N+1. 
But N can be 3e5, so boolean array of size 3e5+1 is fine. 
We need to be careful with the segment tree implementation for speed. 
We'll write a segment tree with 1-indexed nodes. 
Let's code in Python. 
We need to ensure that the segment tree is efficient. We'll use iterative segment tree? Or recursive? 
Recursive with lazy might be fine for 3e5 if optimized. 
We can use a segment tree with size as a power of 2, or just use an array of size 4*N. 
We'll implement recursive with functions. 
But we need to be careful about recursion depth? N=3e5, recursion depth might be up to 4*3e5 calls? Actually, the recursion depth is log2(N) ~ 19, so it's fine. 
We'll define:
class SegTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        # build leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
    
    def _push(self, v):
        if self.lazy[v] != 0:
            self.tree[2*v] += self.lazy[v]
            self.lazy[2*v] += self.lazy[v]
            self.tree[2*v+1] += self.lazy[v]
            self.lazy[2*v+1] += self.lazy[v]
            self.lazy[v] = 0
    
    def _add(self, v, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.tree[v] += val
            self.lazy[v] += val
            return
        self._push(v)
        mid = (l + r) // 2
        self._add(2*v, l, mid, ql, qr, val)
        self._add(2*v+1, mid+1, r, ql, qr, val)
        self.tree[v] = max(self.tree[2*v], self.tree[2*v+1])
    
    def add(self, l, r, val):
        if l > r:
            return
        self._add(1, 0, self.size-1, l, r, val)
    
    def _query(self, v, l, r, ql, qr):
        if ql > r or qr < l:
            return -10**9  # negative infinity
        if ql <= l and r <= qr:
            return self.tree[v]
        self._push(v)
        mid = (l + r) // 2
        left = self._query(2*v, l, mid, ql, qr)
        right = self._query(2*v+1, mid+1, r, ql, qr)
        return max(left, right)
    
    def query(self, l, r):
        if l > r:
            return -10**9
        return self._query(1, 0, self.size-1, l, r)

But note: our data is 1-indexed, but in the segment tree we can use 0-indexed internally. 
We'll pass pref[1..N] as a list, but we need to be careful: we want to query over i=1..j-1, which in 1-indexed is 1..j-1. In 0-indexed, that is 0..j-2. So we can either keep 1-indexed throughout. 
Let's keep 1-indexed for simplicity: we can build the segment tree with indices 1..N. So we'll create an array data of length N+1 (1-indexed), and build the tree accordingly. 
In the segment tree implementation above, it uses 0-indexed leaves. We can adjust. 
Alternatively, we can use 0-indexed for the array A, and adjust. 
Let's use 0-indexed for Python lists: A[0..N-1]. 
Then pref[i] for i=0..N-1: distinct in A[0..i]. 
But then our cuts: we split at i and j (1-indexed). Let's convert to 0-indexed: 
Original: i from 1 to N-2, j from i+1 to N-1. 
In 0-indexed: let left cut at l (0-indexed) meaning the first subarray is A[0..l], second is A[l+1..m], third is A[m+1..N-1], with 0 ≤ l < m < N-1. 
We want to maximize distinct(A[0..l]) + distinct(A[l+1..m]) + distinct(A[m+1..N-1]). 
We can iterate m from 1 to N-2 (since m is the index of the last element of the middle subarray, so m ≥ 1 and m ≤ N-2). 
For each m, we want to maximize over l from 0 to m-1: pref[l] + distinct(l+1, m) + suf[m+1]. 
Here, pref[l] is distinct in A[0..l], and suf[m+1] is distinct in A[m+1..N-1]. 
distinct(l+1, m) is the number of distinct in A[l+1..m]. 
We can maintain a segment tree over l = 0..N-1. 
Initial values: val[l] = pref[l] + 0 (since middle segment empty). 
When we move m from 1 to N-2, we update for the new element A[m]. 
For each m, we need to update the distinct count for middle segment ending at m. 
The new element is A[m]. We need to add 1 to distinct(l+1, m) for those l such that A[m] is not in A[l+1..m-1]. 
As before, let prev = last occurrence of A[m] before index m. 
Then for l ≥ prev, the element A[m] is not in A[l+1..m-1] because the last occurrence is at index prev, and if l ≥ prev, then l+1 > prev, so the previous occurrence is not included. 
So we add 1 to val[l] for l in [prev, m-1] (since l < m). 
But careful: l ranges from 0 to m-1. So the range is [max(prev, 0), m-1]. 
Since prev can be -1 if no previous occurrence, we use max(prev, 0). 
So update: add 1 to range [max(prev, 0), m-1]. 
Then query max over l in [0, m-1]. 
Then candidate = max_val + suf[m+1]. 
This is exactly the same as before, just with 0-indexing. 
We'll use 0-indexed for implementation to avoid off-by-one. 
So:
N = int(input())
A = list(map(int, input().split()))
# compute pref
pref = [0]*N
seen = [False]*(N+1)  # since A_i ≤ N
cnt = 0
for i in range(N):
    if not seen[A[i]]:
        seen[A[i]] = True
        cnt += 1
    pref[i] = cnt
# compute suf
suf = [0]*(N+1)  # suf[i] for i=0..N, where suf[i] = distinct in A[i..N-1], and suf[N]=0
seen = [False]*(N+1)
cnt = 0
for i in range(N-1, -1, -1):
    if not seen[A[i]]:
        seen[A[i]] = True
        cnt += 1
    suf[i] = cnt
suf[N] = 0  # already 0

Now, initialize segment tree with val[l] = pref[l] for l=0..N-1.
We'll build a segment tree with size N.
We'll use an iterative segment tree with lazy propagation? Or recursive. 
Let's use a class with methods. 
We need to support range add and range max. 
We'll implement a segment tree with 1-indexed tree array, but our data is 0-indexed. 
We'll write a segment tree that uses an array of size 4*N. 
We'll define:
class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0]*(4*n)
        self.lazy = [0]*(4*n)
    
    def build(self, node, l, r, data):
        if l == r:
            self.tree[node] = data[l]
        else:
            mid = (l+r)//2
            self.build(2*node, l, mid, data)
            self.build(2*node+1, mid+1, r, data)
            self.tree[node] = max(self.tree[2*node], self.tree[2*node+1])
    
    def push(self, node):
        if self.lazy[node] != 0:
            self.tree[2*node] += self.lazy[node]
            self.lazy[2*node] += self.lazy[node]
            self.tree[2*node+1] += self.lazy[node]
            self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
    
    def add(self, node, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self.push(node)
        mid = (l+r)//2
        self.add(2*node, l, mid, ql, qr, val)
        self.add(2*node+1, mid+1, r, ql, qr, val)
        self.tree[node] = max(self.tree[2*node], self.tree[2*node+1])
    
    def query(self, node, l, r, ql, qr):
        if ql > r or qr < l:
            return -10**9
        if ql <= l and r <= qr:
            return self.tree[node]
        self.push(node)
        mid = (l+r)//2
        left = self.query(2*node, l, mid, ql, qr)
        right = self.query(2*node+1, mid+1, r, ql, qr)
        return max(left, right)

Then:
seg = SegTree(N)
seg.build(1, 0, N-1, pref)

last_occ = [ -1 ] * (N+1)  # initialize to -1, since 0-indexed, and A_i ≥ 1
ans = 0
for m in range(1, N-1):  # m from 1 to N-2 inclusive
    # update for A[m]
    val = A[m]
    prev = last_occ[val]
    l = max(prev, 0)
    r = m-1
    if l <= r:
        seg.add(1, 0, N-1, l, r, 1)
    # query max over l=0..m-1
    max_val = seg.query(1, 0, N-1, 0, m-1)
    candidate = max_val + suf[m+1]
    if candidate > ans:
        ans = candidate
    last_occ[val] = m

Print ans.

We need to test with the samples. 
Let's test manually with the first sample: 
N=5, A=[3,1,4,1,5]
pref: [1,2,3,3,4]
suf: 
i=4: A[4]=5, seen[5]=True, cnt=1, suf[4]=1
i=3: A[3]=1, seen[1]=True, cnt=2, suf[3]=2
i=2: A[2]=4, seen[4]=True, cnt=3, suf[2]=3
i=1: A[1]=1, seen[1] already, cnt=3, suf[1]=3
i=0: A[0]=3, seen[3]=True, cnt=4, suf[0]=4
suf[5]=0
So suf = [4,3,3,2,1,0] (indices 0..5)

Now loop:
m=1: 
  val = A[1]=1, prev = -1, l = max(-1,0)=0, r=0. Add 1 to [0,0].
  seg initially: [1,2,3,3,4]. After add: [2,2,3,3,4]
  query max over 0..0: 2
  candidate = 2 + suf[2] = 2+3=5. ans=5.
  last_occ[1]=1

m=2:
  val = A[2]=4, prev = -1, l=0, r=1. Add 1 to [0,1].
  seg: [3,3,3,3,4]
  query max over 0..1: 3
  candidate = 3 + suf[3] = 3+3=6? Wait, suf[3] is 2? Actually, suf array: suf[0]=4, suf[1]=3, suf[2]=3, suf[3]=2, suf[4]=1, suf[5]=0.
  So for m=2, we use suf[m+1] = suf[3] = 2. So candidate = 3+2=5. ans remains 5.
  last_occ[4]=2

m=3:
  val = A[3]=1, prev = 1, l = max(1,0)=1, r=2. Add 1 to [1,2].
  seg: [3,4,4,3,4]? Let's compute: 
  Before: [3,3,3,3,4]
  Add 1 to indices 1 and 2: becomes [3,4,4,3,4]
  query max over 0..2: max(3,4,4)=4
  candidate = 4 + suf[4] = 4+1=5. ans=5.
  last_occ[1]=3

m=4 is not included because m goes up to N-2=3.
So ans=5. Correct.

Now test with second sample: 
N=10, A=[2,5,6,4,4,1,1,3,1,4]
We can trust the algorithm.

We need to ensure that the segment tree handles the case when m-1 < 0? For m=1, r=0, so it's fine. For m=1, query over 0..0, ok.

Now, we need to be careful about the initial state: for m=1, we update with A[1]. But what about the left part? For l=0, the middle segment is from l+1=1 to m=1, which is A[1]. That's correct. For l=0, pref[0] is distinct in A[0..0], which is 1. After update, val[0] = pref[0] + 1 = 2, which is distinct(A[0..0]) + distinct(A[1..1]) = 1+1=2. That matches. But wait, for m=1, the middle segment is A[1..1], and the left part is A[0..0]. The sum of distinct counts is distinct(A[0..0]) + distinct(A[1..1]) = 1+1=2. But we also have the right part starting at m+1=2, which is A[2..9]. The distinct count of that is suf[2]. So candidate = 2 + suf[2]. In our calculation, we got candidate = 2 + suf[2] = 2+3=5. But is that correct? For m=1, the split is: left: A[0..0], middle: A[1..1], right: A[2..9]. The distinct counts: left: {2} ->1, middle: {5} ->1, right: {6,4,4,1,1,3,1,4} -> distinct: 6,4,1,3 = 4? Wait, let's compute: A[2..9] = [6,4,4,1,1,3,1,4]. Distinct: 6,4,1,3 = 4. So total = 1+1+4=6. But our candidate was 5. So there is a discrepancy. 
Let's check: In our algorithm, for m=1, we updated val[0] to pref[0] + 1 = 1+1=2. Then candidate = 2 + suf[2]. suf[2] is distinct in A[2..9] which is 4. So 2+4=6. But earlier I said suf[2]=3? That was a mistake. Let's recompute suf correctly for the second sample. 
A: 2 5 6 4 4 1 1 3 1 4
Indices: 0:2, 1:5, 2:6, 3:4, 4:4, 5:1, 6:1, 7:3, 8:1, 9:4
Compute suf from right:
i=9: A[9]=4, seen[4]=True, cnt=1, suf[9]=1
i=8: A[8]=1, seen[1]=True, cnt=2, suf[8]=2
i=7: A[7]=3, seen[3]=True, cnt=3, suf[7]=3
i=6: A[6]=1, seen[1] already, cnt=3, suf[6]=3
i=5: A[5]=1, seen[1] already, cnt=3, suf[5]=3
i=4: A[4]=4, seen[4] already, cnt=3, suf[4]=3
i=3: A[3]=4, seen[4] already, cnt=3, suf[3]=3
i=2: A[2]=6, seen[6]=True, cnt=4, suf[2]=4
i=1: A[1]=5, seen[5]=True, cnt=5, suf[1]=5
i=0: A[0]=2, seen[2]=True, cnt=6, suf[0]=6
suf[10]=0
So suf[2]=4, not 3. My earlier miscalculation. So candidate for m=1 is 2+4=6. 
Now, the sample output is 9. So the maximum is 9. Let's continue the algorithm to see if we get 9. 
We need to compute pref:
i=0: A[0]=2, seen[2]=True, cnt=1, pref[0]=1
i=1: A[1]=5, seen[5]=True, cnt=2, pref[1]=2
i=2: A[2]=6, seen[6]=True, cnt=3, pref[2]=3
i=3: A[3]=4, seen[4]=True, cnt=4, pref[3]=4
i=4: A[4]=4, seen[4] already, cnt=4, pref[4]=4
i=5: A[5]=1, seen[1]=True, cnt=5, pref[5]=5
i=6: A[6]=1, seen[1] already, cnt=5, pref[6]=5
i=7: A[7]=3, seen[3]=True, cnt=6, pref[7]=6
i=8: A[8]=1, seen[1] already, cnt=6, pref[8]=6
i=9: A[9]=4, seen[4] already, cnt=6, pref[9]=6
So pref = [1,2,3,4,4,5,5,6,6,6]

Now, initial seg values = pref.
last_occ = [-1]*11 (since values up to 10? Actually A_i ≤ N=10, so size 11, but values can be up to 10, so last_occ[1..10] = -1, last_occ[0] unused).

Loop:
m=1:
  val=A[1]=5, prev=-1, l=0, r=0. Add 1 to [0,0].
  seg: [2,2,3,4,4,5,5,6,6,6]
  query max over 0..0: 2
  candidate = 2 + suf[2] = 2+4=6. ans=6.
  last_occ[5]=1

m=2:
  val=A[2]=6, prev=-1, l=0, r=1. Add 1 to [0,1].
  seg: [3,3,3,4,4,5,5,6,6,6]
  query max over 0..1: 3
  candidate = 3 + suf[3] = 3+3=6. ans=6.
  last_occ[6]=2

m=3:
  val=A[3]=4, prev=-1, l=0, r=2. Add 1 to [0,2].
  seg: [4,4,4,4,4,5,5,6,6,6]
  query max over 0..2: 4
  candidate = 4 + suf[4] = 4+3=7. ans=7.
  last_occ[4]=3

m=4:
  val=A[4]=4, prev=3, l=max(3,0)=3, r=3. Add 1 to [3,3].
  seg: [4,4,4,5,4,5,5,6,6,6] (index 3 becomes 4+1=5)
  query max over 0..3: max(4,4,4,5)=5
  candidate = 5 + suf[5] = 5+3=8. ans=8.
  last_occ[4]=4

m=5:
  val=A[5]=1, prev=-1, l=0, r=4. Add 1 to [0,4].
  seg: [5,5,5,6,5,5,5,6,6,6] (indices 0..4 +1)
  query max over 0..4: max(5,5,5,6,5)=6
  candidate = 6 + suf[6] = 6+3=9. ans=9.
  last_occ[1]=5

m=6:
  val=A[6]=1, prev=5, l=5, r=5. Add 1 to [5,5].
  seg: [5,5,5,6,5,6,5,6,6,6]
  query max over 0..5: max(5,5,5,6,5,6)=6
  candidate = 6 + suf[7] = 6+3=9. ans=9.
  last_occ[1]=6

m=7:
  val=A[7]=3, prev=-1, l=0, r=6. Add 1 to [0,6].
  seg: [6,6,6,7,6,7,6,6,6,6]
  query max over 0..6: 7
  candidate = 7 + suf[8] = 7+2=9. ans=9.
  last_occ[3]=7

m=8:
  val=A[8]=1, prev=6, l=6, r=7. Add 1 to [6,7].
  seg: [6,6,6,7,6,7,7,7,6,6]
  query max over 0..7: 7
  candidate = 7 + suf[9] = 7+1=8. ans=9.
  last_occ[1]=8

m=9 is not included (m goes to N-2=8).
So max ans=9. Correct.

So the algorithm works.

Now, we need to implement it efficiently. 
We need to be careful about the segment tree implementation in Python. With N=3e5, the operations are O(N log N). Each operation (add and query) is O(log N). So total O(N log N) ~ 3e5 * 19 = 5.7e6, which should be fine in Python if optimized. 
We need to avoid recursion overhead? We can use an iterative segment tree? But lazy propagation is easier with recursion. However, recursion depth is log N ~ 19, so it's fine. But the number of recursive calls per operation is O(log N), and we have N operations, so total recursive calls ~ N log N, which might be a bit slow in Python due to function call overhead. We can try to optimize by using a faster segment tree, perhaps an iterative one with lazy propagation using loops. 
Alternatively, we can use a Fenwick tree? But we need range add and range max, which is not directly supported by Fenwick. 
We can also use a segment tree with a loop-based approach for max and another for lazy? 
Maybe we can use a segment tree with arrays and implement add and max in a non-recursive way using a tree structure. 
I think the recursive segment tree will pass with PyPy if optimized. 
We can also use a class with methods that are defined as local functions to reduce attribute access overhead. 
Let's write the segment tree in a fast way. 
We can use a list-based segment tree with size as a power of 2, and store max values in a tree array, and lazy values in another array. 
We can implement range add and range max using a recursive function but with inline code. 
Alternatively, we can use an iterative segment tree for range add and point query? But we need range max query. 
There is a known approach: use two Fenwick trees to support range add and prefix sum, but not max. 
So we need segment tree. 
Let's write a segment tree class with methods add and query. 
We'll use 0-indexed tree array. 
We'll build the tree such that the leaves are at indices offset to n-1. 
We'll use an iterative approach for max query, and for range add, we can use a lazy propagation with a segment tree where each node covers a range. 
I think the recursive one is simpler. 
Let's code it carefully.

We'll define:
class SegTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
    
    def build(self, data):
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
    
    def _apply(self, idx, val):
        self.tree[idx] += val
        self.lazy[idx] += val
    
    def _push(self, idx):
        if self.lazy[idx] != 0:
            self._apply(2*idx, self.lazy[idx])
            self._apply(2*idx+1, self.lazy[idx])
            self.lazy[idx] = 0
    
    def _add(self, idx, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self._apply(idx, val)
            return
        self._push(idx)
        mid = (l + r) // 2
        self._add(2*idx, l, mid, ql, qr, val)
        self._add(2*idx+1, mid+1, r, ql, qr, val)
        self.tree[idx] = max(self.tree[2*idx], self.tree[2*idx+1])
    
    def add(self, l, r, val):
        if l > r:
            return
        self._add(1, 0, self.size-1, l, r, val)
    
    def _query(self, idx, l, r, ql, qr):
        if ql > r or qr < l:
            return -10**9
        if ql <= l and r <= qr:
            return self.tree[idx]
        self._push(idx)
        mid = (l + r) // 2
        left = self._query(2*idx, l, mid, ql, qr)
        right = self._query(2*idx+1, mid+1, r, ql, qr)
        return max(left, right)
    
    def query(self, l, r):
        if l > r:
            return -10**9
        return self._query(1, 0, self.size-1, l, r)

This is similar to before but with size as power of 2. 
We need to pass data as a list of length n. 
We'll build with seg.build(pref) where pref is a list of length N. 
Then, in the loop, we call seg.add(l, r, 1) and seg.query(0, m-1). 
Note: in the query, we use l and r inclusive. 
We need to ensure that m-1 is within [0, N-1]. For m=1, m-1=0, ok. 
Now, we need to handle the case when m=0? The loop starts at m=1. So it's fine. 
Now, let's test with the first sample in code. 
We can write the code and run on the samples. 
But since we are not to test on sample inputs, we trust the logic. 
Now, we need to write the full code. 
We'll read input, compute pref and suf, build segment tree, then loop. 
We need to be careful with the suf array: we need suf[m+1] for m up to N-2, so we need suf up to index N-1. We'll compute suf of size N+1, with suf[N]=0. 
Now, let's write the code.

One more check: the value of A_i can be up to N, so we need last_occ of size N+1. We'll use 0-indexed for A, so A[i] is in [1, N]. We'll create last_occ = [ -1