We need to compute for every subarray the minimum number of “interval” deletions that cover its distinct values, where each operation can erase any contiguous integer range that is fully present. This is equivalent to: for the set of values in the subarray, the minimum number of integer intervals covering them equals the number of connected components of the “value adjacency graph” where values x and y are adjacent if |x-y|=1 and both appear. So f(L,R) = number of connected components of the set S(L,R) of distinct values in A[L..R] under adjacency of consecutive integers.

Thus total answer = Σ_{subarray} (# components of S(subarray)). We can rewrite as: the subarray contributes 1 for each component it contains. Equivalently, count pairs (subarray, component) where the component is a maximal interval of integers fully contained in S(subarray). We can think of each integer position i (1..N) as a "value occurrence". Distinct values can be thought of as intervals. A standard trick: for each value v, process its occurrences and mark "break points" where the consecutive-integer chain would be split. More directly, we can use a divide-and-conquer or offline stack: we can sweep and count contributions of each maximal integer segment.

Observation: For a subarray, its distinct set S is a union of integer intervals. f(L,R) equals the number of such intervals. So answer = Σ over subarray of (# of integer intervals whose all values appear in subarray). For a fixed integer interval I = [l,r] (contiguous integers), let g(I) = number of subarrays whose distinct set S contains all integers in I (i.e., every v in [l,r] appears at least once in the subarray). Then answer = Σ_I g(I). For N up to 3e5, number of possible intervals is O(N^2), too many. But we can count efficiently using a stack / next greater element method: each subarray's f is the number of "chains" when merging values by adjacency. A classic result: Σ f(L,R) = Σ_{i=1}^{N} (number of subarrays where A_i is the maximum of its value and...). Hmm.

Alternative: Use offline counting of connected components via inclusion–exclusion of "breaks". For each pair of consecutive values (v, v+1), we can define a break indicator: a subarray does NOT have a "join" between v and v+1 if at least one of v or v+1 is missing. So component count = #distinct values - #joins inside distinct values. That is, f(L,R) = |S(L,R)| - |{(v,v+1) : v and v+1 both ∈ S(L,R)}|. Summing over subarrays: Σ|S| - Σ#joins.

Now Σ|S(L,R)| = Σ_{v} (#subarrays containing at least one occurrence of v). For each value v, if its occurrence positions are p1 < p2 < ... < pk, then a subarray [L,R] contains v iff L ≤ pi ≤ R for some i. The number of subarrays containing at least one pi is total subarrays minus those that lie completely between consecutive occurrences (or before first / after last). Total subarrays = N(N+1)/2. For each v, number of subarrays missing v = Σ_{j=0}^{k} (gap_j choose 2), where gap_0 = p1-1, gap_j = p_{j+1}-p_j-1 for 1≤j<k, gap_k = N-p_k. So Σ|S| = Σ_v ( total - missing_v ).

Similarly, Σ#joins counts, for each subarray, how many adjacent integer pairs (v, v+1) both appear. By linearity, Σ_{(v,v+1)} (#subarrays containing both v and v+1). For a pair (v,v+1), we need subarrays whose range covers at least one occurrence of v and at least one occurrence of v+1. This is classic: let positions of v be P, positions of w=v+1 be Q. We need L ≤ min(some element of P∪Q covering both?) Actually need subarray [L,R] that contains at least one v and at least one v+1. Compute: sort combined list of occurrences with labels. Then number of subarrays covering at least one of each = total subarrays - subarrays missing v - subarrays missing v+1 + subarrays missing both. Missing both means subarray lies entirely in a gap where neither v nor v+1 appears. The gaps are segments between consecutive occurrences when we merge the two sorted position lists. So for each adjacent pair (v,v+1), we can compute in O(occ_v + occ_{v+1}) time, summing over all v up to N-1, total O(N) because each position appears in exactly two pairs? Actually each value appears in at most two adjacent pairs (v-1,v) and (v,v+1). So total work is O(N) if we process each pair by merging their occurrence lists efficiently using pointers from previous pair, but that might still be O(N^2) in worst case if a value appears many times.

We need a more efficient method. Since N is up to 3e5, O(N log N) is fine, O(N sqrt N) maybe, but O(N^2) impossible. We can compute #subarrays containing both v and v+1 using the two-pointer technique on the merged sorted list: we can pre-store for each value the list of its positions (sorted). For each v from 1 to N-1, we need to count subarrays covering at least one pos in list_v and at least one pos in list_{v+1}. This can be computed as: number of subarrays that intersect both lists. Equivalent to: total subarrays - subarrays completely outside list_v - subarrays completely outside list_{v+1} + subarrays completely outside both. The "outside both" are subarrays that lie in a region where neither v nor v+1 appears, i.e., a maximal interval of indices where neither value appears. Those intervals are gaps between sorted union of positions. The union of positions sorted is easy to merge two sorted lists of total length occ_v + occ_{v+1} (which can be O(N) per v leading to O(N^2)). But each position belongs to two adjacent value pairs (value-1 and value+1), so total sum of lengths over all v is Σ_v (occ_v + occ_{v+1}) = 2 Σ_v occ_v = 2N. So total merging cost is O(N) if we process each pair sequentially, reusing the merge? Let's analyze.

If we iterate v from 1 to N-1, and for each v we merge list_v and list_{v+1}, total work is Σ (occ_v + occ_{v+1}) = 2N - occ_1 - occ_N (since each list appears twice). That's O(N). Yes! Because each occurrence index belongs to two adjacent pairs: for v, it appears in pair (v-1,v) and (v,v+1) (except for v=1 and v=N). So total work O(N). So we can do O(N) merges across all pairs.

Thus we can compute:
- Total = N(N+1)/2.
- sumDist = Σ_v (Total - missing_v) where missing_v = Σ gaps choose 2.
- sumJoin = Σ_{v=1}^{N-1} join_v where join_v = number of subarrays containing both v and v+1.

Then answer = sumDist - sumJoin.

Check with sample: N=4, A=[1,3,1,4]. Let's compute.
- Total=10.
- Value 1 positions {1,3}, occ=2. gaps: before first 0, between 3-1-1=1, after last 4-3=1. So gaps lengths 0,1,1. missing = C(0,2)+C(1,2)+C(1,2)=0+0+0=0. So value1 contributes 10.
- Value 3 positions {2}, gaps: before 1, after 2 (4-2=2). gaps:1,2 => C(1,2)=0, C(2,2)=1 => missing=1. contributes 9.
- Value 4 positions {4}, gaps: before 3, after 0 => C(3,2)=3 => missing=3, contributes 7.
- Value 2 has no positions, occ=0, missing = gaps = N choose 2 = C(4,2)=6. contributes 4.
- sumDist = 10+9+7+4 = 30. Wait check: values with zero occurrences still considered? Actually f(L,R) counts components of distinct values present. If a value does not appear, it doesn't affect components. So we should not sum over values with zero occurrence? Let's verify formula f = |S| - #joins, where |S| is number of distinct values present. For a subarray, the sum over all v (including those not present) of indicator(v∈S) = |S|. So we need to sum over all v that appear at least once? But indicator(v∈S) = 0 if v not in S, so including those values gives zero contribution. So indeed we need to sum over all possible v (1..N) the indicator. However, we can restrict to v with occ>0, because missing_v = total, so contribution would be 0? Let's check: for v=2, occ=0, missing_v = number of subarrays missing v = all subarrays = total, so contribution = total - total = 0. So including them gives zero, no effect. So sumDist = Σ_v max(occ,0) contribution = same.

Now sumJoin for v=1: pair (1,2). positions: 1 has {1,3}, 2 has {}. Subarrays containing both? Since 2 never appears, join=0.
v=2: (2,3). positions 2 empty, 3 {2}. join=0.
v=3: (3,4). 3 {2}, 4 {4}. Need subarrays covering both positions. Subarrays: [L,R] with L≤2 and R≥4 => only [1,4] and [2,4]? Actually need contain at least one of each. Positions: 2 and 4. So subarrays must include index 2 and index 4. L can be 1 or 2; R can be 3 or 4. So subarrays: (1,2..4) any with L≤2,R≥4: possibilities: L=1,R=3 includes 2 but not 4. L=1,R=4 includes both. L=2,R=3 includes 2 but not 4. L=2,R=4 includes both. So two subarrays: [1,4] and [2,4]. So join=2. Then sumJoin = 2.

Thus answer = sumDist - sumJoin = 30 - 2 = 28. But expected 16. Something is off. Let's recompute. Wait our formula f = |S| - #joins, but is that correct? Let's test on subarray [1,4] in sample: distinct set = {1,3,4}. Adjacent pairs: (1,2) not both, (2,3) not both, (3,4) both. So #joins = 1. |S| = 3. So f = 3-1=2. Good. For [1,3] = indices 1..3, values 1,3,1 => distinct {1,3}. Adjacent pairs: (1,2) no, (2,3) no, (3,4) no (4 absent). #joins = 0, |S|=2 => f=2. Actually can we erase 1 and 3 separately? Since they are not adjacent, yes need 2 operations. So f=2. For [2,4] = 3,1,4 => distinct {1,3,4}, #joins=1, f=2. For [1,2] = 1,3 => distinct {1,3}, #joins=0, f=2. For [1,1] distinct {1}, f=1. For [2,2] {3}, f=1. [3,3] {1}, f=1. [4,4] {4}, f=1. [2,3] 3,1 => distinct {1,3}, f=2. [3,4] 1,4 => distinct {1,4}, not adjacent, f=2? Wait 1 and 4 not adjacent, need two operations, yes. So sum f over all 10 subarrays: [1,1]=1, [2,2]=1, [3,3]=1, [4,4]=1 => 4. [1,2]=2, [2,3]=2, [3,4]=2 =>6. [1,3]=2, [2,4]=2, [1,4]=2 =>6. Total = 4+6+6=16. Good.

Now our computed sumDist = 30. Let's compute sumDist manually: sum over subarrays of |S|. Count distinct per subarray:
[1,1] size1 =>1
[2,2] =>1
[3,3] =>1
[4,4] =>1
[1,2] =>2
[2,3] =>2
[3,4] =>2
[1,3] =>2
[2,4] =>3
[1,4] =>3
Sum = 1+1+1+1+2+2+2+2+3+3 = 18. So sumDist should be 18. Let's compute via our formula: Σ_v contribution_v (Total - missing_v) = ?
- v=1: missing_v =0, contrib=10
- v=2: missing_v=6, contrib=4
- v=3: missing_v=1, contrib=9
- v=4: missing_v=3, contrib=7
Sum=10+4+9+7=30. That's too high. Something wrong: For v=2, since it never appears, indicator(v∈S)=0 for all subarrays, so contribution to sumDist is 0, not 4. Our formula gave 4 because we subtracted missing_v from total, but missing_v counted subarrays missing v = all subarrays, so total - missing_v = 0. Wait we earlier said v=2 missing = total (6), so contribution = total - total = 0. But we computed 4. Let's recalc: N=4, total subarrays = 4*5/2 = 10. missing_v for v=2: all subarrays missing 2 = 10. So contribution = 10 - 10 = 0. But we wrote 4 erroneously because we used C(4,2)=6. That's the number of subarrays of length 2? No, missing_v should be count of subarrays [L,R] such that no occurrence of v in A[L..R]. Since v never appears, that count is total = 10, not 6. Our earlier gap method: for v with no positions, there is one "gap" covering whole array of length N, so missing = C(N+1,2)? Let's recompute formula.

General: For a value v with occurrence positions sorted: p1 < p2 < ... < pk. Define gaps:
- gap0 = p1 - 1 (positions before first)
- for j=1..k-1: gapj = p_{j+1} - p_j - 1 (positions between consecutive occurrences)
- gapk = N - p_k (positions after last)
Then any subarray [L,R] missing v must lie entirely within one gap (i.e., L,R both in same gap interval). The number of subarrays fully inside a gap of length g is C(g+1,2) = g*(g+1)/2. Because there are g+1 positions? Wait indices: gap of length g means there are g indices (positions) that are not v. The subarray indices L,R must be chosen from these g indices, with 1 ≤ L ≤ R ≤ g. Number of subarrays = g*(g+1)/2. So missing_v = Σ_j C(gap_j+1, 2). If k=0 (no occurrence), there is one gap of length N, missing = C(N+1,2) = N(N+1)/2 = total. Yes.

Our earlier formula used C(gap,2) (g*(g-1)/2) which was wrong. For v=2, gap=4, C(4+1,2)=C(5,2)=10. Good. For v=1: positions {1,3}. gaps: before first: p1-1 =0, between: 3-1-1=1, after: 4-3=1. So gap lengths: 0,1,1. missing = C(0+1,2)+C(1+1,2)+C(1+1,2) = C(1,2)+C(2,2)+C(2,2) = 0+1+1=2. Wait C(1,2)=0, C(2,2)=1. So missing=2. Then contribution = total - missing = 10-2=8. For v=3: positions {2}. gaps: before 1, after 2. missing = C(1+1,2)+C(2+1,2)=C(2,2)+C(3,2)=1+3=4. Contribution = 10-4=6. v=4: positions {4}. gaps before 3, after 0. missing = C(3+1,2)+C(0+1,2)=C(4,2)+C(1,2)=6+0=6. Contribution = 10-6=4. Sum = 8+6+4 = 18. Great matches.

So formula: missing_v = Σ_{gaps} C(g+1, 2) = Σ g(g+1)/2.

Now sumJoin: join_v = number of subarrays containing both v and v+1. Compute similarly: For two sets of positions P (v) and Q (v+1), sorted merged list. We need subarrays that intersect both sets. Equivalent to: total subarrays - subarrays missing v - subarrays missing v+1 + subarrays missing both.

But we can compute directly: number of subarrays that contain at least one element from P and at least one from Q. Let union sorted list U of P∪Q. Let gaps be maximal intervals of indices not in U. Also define also intervals before first and after last. The subarrays missing both are those lying entirely in a gap of the union. So missing_both = Σ C(g+1,2) where g are lengths of gaps in union. Then join_v = total - missing_v - missing_{v+1} + missing_both.

We can compute missing_v and missing_{v+1} already from the per-value gap sums. For each pair, we also need missing_both. We can compute this efficiently while merging the two sorted lists.

Implementation plan:

1. Read N and array A[1..N].
2. Build vector positions for each value 1..N: store indices where A_i = val. (Since A_i ≤ N, we can allocate list of size N+1). Complexity O(N).
3. Precompute for each v: missing_v = Σ_{gaps} g*(g+1)/2.
   - For each v, if positions[v] is empty: missing_v = N*(N+1)//2.
   - Else: let prev = 0. For each pos in positions[v]: gap = pos - prev - 1; missing += gap*(gap+1)//2; prev = pos.
   - After loop: gap = N - prev; missing += gap*(gap+1)//2.
4. sumDist = Σ_v (total - missing_v) = N*occ_with_nonzero? Actually we sum over v=1..N, using total = N*(N+1)//2. But we can just compute sumDist = Σ_v (total - missing_v). Since total is constant, sumDist = N*total - Σ_v missing_v. But Σ_v missing_v includes all values, we can compute.

5. For each v from 1 to N-1:
   - Let P = positions[v], Q = positions[v+1].
   - If either empty: join_v = 0 (since need both). Actually if one empty, join_v=0. Because subarray cannot contain both if one missing.
   - Else:
       - missing_v, missing_{v+1} already known.
       - Compute missing_both via merging P and Q.
         Merge: two-pointer i=0,j=0, prev=0.
         While i<P.size or j<Q.size:
            cur = min(P[i] if i<|P| else INF, Q[j] if j<|Q| else INF)
            gap = cur - prev - 1
            missing_both += gap*(gap+1)//2
            prev = cur
            if P[i]==cur: i++ else j++
         After loop: gap = N - prev; missing_both += gap*(gap+1)//2
       - join_v = total - missing_v - missing_{v+1} + missing_both
   - sumJoin += join_v

6. Answer = sumDist - sumJoin.

We need to ensure O(N) time. The merging across all pairs: total work = Σ (|P|+|Q|) = O(N). Because each list appears in two merges (except boundaries). Indeed each occurrence index belongs to two values? Actually each index i has value A_i. That value v belongs to pairs (v-1,v) and (v,v+1). So each index contributes to merging of at most two pairs. Thus total merges O(N). Good.

Edge Cases: When both P and Q are non-empty but the merged gaps may produce large numbers, but still within 64-bit. N up to 3e5, total subarrays up to ~4.5e10, fits in 64-bit (signed 2^63-1 ~9e18). Summations may be up to O(N^2) ~ 9e10, safe in 64-bit.

Let's test with sample.

We'll implement in Python, careful with integer division. Use //2.

Let's manually test the algorithm for sample 1.

N=4, total=10.

Positions:
1: [1,3]
2: []
3: [2]
4: [4]

Compute missing:
v=1: gaps: before pos1=0, between 3-1-1=1, after 4-3=1. missing = 0*1/2 + 1*2/2 + 1*2/2 = 0 + 1 + 1 = 2.
v=2: empty => missing = 10.
v=3: pos2: gaps before 1, after 2 => 1*2/2=1, 2*3/2=3 => total 4.
v=4: pos4: gaps before 3, after 0 => 3*4/2=6, 0 => 6.

Sum missing = 2+10+4+6 = 22. sumDist = N*total - sumMissing = 4*10 - 22 = 40 - 22 = 18. Good.

Now sumJoin:
v=1: P=[1,3], Q=[] => join=0.
v=2: P=[] => join=0.
v=3: P=[2], Q=[4]. Missing_v (v=3) = 4, missing_{v+1}=6.
Compute missing_both: merge [2,4] => gaps: before first: 2-1-1=0? Actually prev=0, cur=2 => gap = 2-0-1 = 1. Wait positions are 1-indexed. The gap before first occurrence is 2-1-1=0? Let's compute precisely: prev = 0 (position before start). cur = 2 => gap = 2 - 0 - 1 = 1 (index 1). So missing += 1*2/2=1. prev=2. Next cur=4 => gap = 4-2-1=1 => missing +=1*2/2=1. prev=4. After loop: gap = N - prev = 4-4=0 => missing +=0. So missing_both = 2.
join = total - missing_v - missing_{v+1} + missing_both = 10 - 4 - 6 + 2 = 2. Good. sumJoin=2.

Answer = sumDist - sumJoin = 18 - 2 = 16. Matches.

Test sample 2: N=5, A=[3,1,4,2,4].
Compute manually maybe using code later.

Now we need to ensure algorithm works for N up to 3e5. Memory: storing positions for each value. Since A_i <= N, we can allocate list of length N+1, each a Python list. Sum of lengths = N. Append indices.

Merging: We'll need to iterate over each pair. For each pair, we need to merge P and Q. Using while loops with indices.

Potential micro-optimizations: Use local variables, but fine.

Now ensure that missing_both calculation matches the earlier formula for missing_v when one list empty: if P empty, join = 0. So we can early continue.

Edge Cases: When both lists non-empty but the union covers whole array (i.e., no gaps), missing_both = 0, join = total - missing_v - missing_{v+1}.

Now answer may be large: O(N^2) ~ 4.5e10, fits in 64-bit. In Python, int unlimited.

Now confirm with sample 2.

We'll code a quick test mentally or trust.

Potential issues: The algorithm uses positions as 1-indexed. Gap calculation uses cur - prev - 1, where prev initially 0 (position before first). After processing all positions, final gap = N - prev. This matches because indices range 1..N. Example: P=[1], N=4. prev=0, cur=1 => gap=1-0-1=0 (none before). After loop, gap=N-1=3 (positions 2,3,4). missing = 0 + 3*4/2 = 6. Indeed missing_v = C(3+1,2)=6. Good.

Now we must confirm that the formula f = |S| - #joins is correct for any subarray. Let's prove quickly: S is set of distinct values. Define graph on S where edges connect v and v+1 if both present. Since edges only between consecutive integers, each connected component is a maximal interval of consecutive integers. Number of components = |S| - (#edges). Since graph is a forest (actually a path) for each component (consecutive integers). Indeed edges are only between consecutive numbers, so each component is a path. Number of components = |S| - (number of edges). Because a forest with C components, V nodes, E edges: C = V - E. Here each component is a path (no cycles). So f = components. Good.

Thus answer = Σ (|S| - edges) = Σ|S| - Σ edges. Edge contributions correspond to pairs (v,v+1) both present.

Now we have correct decomposition.

Thus algorithm yields answer.

Now complexity O(N). Good.

Now we need to implement solve() accordingly.

Implementation Steps:

```python
def solve():
    import sys
    input = sys.stdin.readline
    N = int(input().strip())
    A = list(map(int, input().split()))