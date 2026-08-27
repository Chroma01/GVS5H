
## ideation
We need to compute $\sum_{L \le R} f(L,R)$ where $f(L,R)$ is the minimum number of "range erasures" to delete all numbers $A_L..A_R$, where each operation chooses $[l,r]$ such that every integer in $[l,r]$ appears at least once in the current multiset and removes all occurrences of integers in $[l,r]$.

This is a known problem. $f(L,R)$ equals the number of "connected components" in the set of distinct values present in $A[L..R]$ when we connect values that are consecutive integers (i.e., $x$ and $x+1$ both present). More precisely, if the distinct values in the subarray form a set $S$, and we build a graph with edges between $x$ and $x+1$ whenever both are in $S$, then $f(L,R)$ is the number of connected components of this graph.

Equivalently, $f(L,R) = D(L,R) - G(L,R)$, where $D$ is the number of distinct values in the subarray, and $G$ is the number of pairs of consecutive integers $(x, x+1)$ such that both $x$ and $x+1$ appear at least once in the subarray. (Each edge merges two components; with $D$ isolated vertices and $G$ edges added, components become $D - G$.)

So the answer is:
$$\text{Ans} = \sum_{L \le R} D(L,R) - \sum_{L \le R} G(L,R)$$

We compute both sums in $O(N)$ or $O(N \log N)$.

**Sum of D:** For each value $v$, it appears at some positions. A subarray contains $v$ iff $L \le p_k$ and $R \ge p_k$ for at least one occurrence. The number of subarrays containing $v$ can be computed by considering gaps between consecutive occurrences (including boundaries). For each value $v$, let positions be $p_1 < p_2 < \dots < p_m$. The number of subarrays missing $v$ is $\sum (p_{i+1} - p_i) \cdot (p_{i+1} - p_i - 1) / 2$ (where $p_0=0, p_{m+1}=N+1$). Then $\sum D = \sum_v (\text{total subarrays} - \text{missing})$.

**Sum of G:** For each pair of consecutive integers $(x, x+1)$, we need the number of subarrays where both $x$ and $x+1$ appear. Let positions of $x$ be $X = \{x_i\}$ and $y=x+1$ be $Y = \{y_j\}$. A subarray contains both iff it intersects both sets. This can be computed by sorting all positions with labels, then using two pointers or a sweepline. Alternatively, we can use inclusion-exclusion:
Total subarrays = $N(N+1)/2$.
Subarrays missing $x$ or $y$ = (missing $x$) + (missing $y$) - (missing both).
So subarrays containing both = Total - (missing $x$) - (missing $y$) + (missing both $x$ and $y$).
We can compute missing both $x$ and $y$ by merging their sorted position lists and finding gaps that contain no $x$ and no $y$.

Both sums can be computed in $O(N \log N)$ total (due to sorting per value, but since values are bounded by $N$ and total size is $N$, we can use counting sort-like buckets, or just collect per value in $O(N)$ then sort each bucket; total time $O(N \log N)$ is fine for $N=3\cdot 10^5$).

**Pitfalls:**
- The graph of values has edges only between consecutive integers. So $G$ counts edges in the induced subgraph on the set of distinct values present.
- $D$ counts distinct values.
- $f(L,R) = D - G$ is correct only if the graph of consecutive values present is a forest? Actually, the graph of values present with edges between consecutive values can have cycles (e.g., values {1,2,3} form a path, but {1,2,3,1} doesn't make sense since values are distinct). Wait, the graph has vertices as distinct values, edges between $x$ and $x+1$ if both present. This graph is a collection of paths (no cycles because it's a subgraph of the integer line). In a forest, number of components = vertices - edges. So indeed $f = D - G$.
- For the sample: $A=[1,3,1,4]$.
  Subarrays:
  [1]: {1} -> 1
  [3]: {3} -> 1
  [1]: {1} -> 1
  [4]: {4} -> 1
  [1,3]: {1,3} -> no consecutive -> 2
  [3,1]: {1,3} -> 2
  [1,4]: {1,4} -> 2
  [1,3,1]: {1,3} -> 2
  [3,1,4]: {1,3,4} -> 3,1 edge? 3-4 is consecutive? 3 and 4 are consecutive integers. So values {1,3,4}: edges (3,4). D=3, G=1 -> f=2. Check: board has 1,3,1,4. Erase 3,4 -> leaves 1,1. Erase 1 -> 2 ops. Yes.
  [1,3,1,4]: D=3, G=1 (3,4) -> f=2. Matches sample.
  Sum = 1+1+1+1+2+2+2+2+2+2 = 16. Good.

**Algorithm:**
1. Read N and array A.
2. Create list of positions for each value 1..N.
3. For each value $v$, compute missing subarrays:
   Let $p_0 = 0$, $p_{m+1} = N+1$.
   Missing = $\sum_{i=0}^m \binom{p_{i+1}-p_i}{2}$.
   Then $D_v$ (contribution to sum of D from $v$) = total_subarrays - missing.
   Sum_D = $\sum_v D_v$.
4. For each $x$ from 1 to N-1:
   Let $X$ = positions of $x$, $Y$ = positions of $x+1$.
   missing_x, missing_y as above.
   missing_both = number of subarrays containing neither $x$ nor $x+1$.
   To compute missing_both: merge the two sorted position lists, find gaps between consecutive elements in the merged list (including 0 and N+1). The gap length is $g$, contributes $\binom{g}{2}$.
   Then $G_x$ (subarrays containing both $x$ and $x+1$) = total - missing_x - missing_y + missing_both.
   Sum_G = $\sum_{x=1}^{N-1} G_x$.
5. Answer = Sum_D - Sum_G.

**Complexity:**
- Building position lists: $O(N)$.
- For each value, computing missing: sum of $O(m)$ per value, total $O(N)$.
- For each consecutive pair, merging two lists: total time is $O(N)$ if we use two pointers scanning through all positions? Actually, for each pair we merge, but total work across all pairs could be large if we do it naively. However, we can process all pairs simultaneously using a sweepline? Wait, we need $G$ for each specific pair $(x, x+1)$. There are $N-1$ pairs. For each pair, we merge two lists. The sum of sizes of all lists is $N$. But for each pair, the lists are of sizes $m_x$ and $m_{x+1}$. The merge cost is $O(m_x + m_{x+1})$. Summing over $x=1..N-1$, this becomes $O(\sum_{x=1}^{N-1} (m_x + m_{x+1})) = O(\sum_{v=1}^N m_v \cdot (\text{number of neighbors}))$. Each value appears in two pairs (except boundaries). So total merge cost is $O(\sum m_v \cdot 2) = O(2N) = O(N)$. Wait, is that correct? For $x$, we merge list of $x$ and $x+1$. So each value's list is merged in two pairs (e.g., value $v$ is in pair $(v-1,v)$ and $(v,v+1)$). So each position is visited a constant number of times. Total time $O(N)$.

So overall $O(N)$ after $O(N)$ preprocessing to build lists. This is efficient for $N=3\cdot 10^5$.

**Edge Cases:**
- $N=1$: no pairs, Sum_G=0, Sum_D=1, answer=1.
- Values may not appear at all; their position lists are empty. Then missing = total_subarrays (since all subarrays miss that value). D_v=0. Good.
- For pairs where one or both values don't appear, missing_x or missing_y = total, missing_both = total (if both don't appear, or if we merge empty lists, gaps are just [0,N+1], so missing_both = total). Then G_x = total - total - total + total = 0. Or if one is empty, say $m_x=0$, then missing_x = total, G_x = 0. So we can skip pairs with empty lists or handle naturally.

**Implementation details:**
- Store positions in a list of lists: `pos = [[] for _ in range(N+2)]`. Use 1-indexed values.
- For each $v$ from 1..N, compute `missing_v`.
- Total subarrays = N*(N+1)//2.
- Sum_D = sum over v of (total - missing_v).
- For each $x$ from 1..N-1:
   - Get lists `X = pos[x]`, `Y = pos[x+1]`.
   - Compute missing_both by merging.
- Sum_G = sum of G_x.
- Answer = Sum_D - Sum_G.

Let's verify with sample 2:
N=5, A=[3,1,4,2,4]
Positions:
1: [2]
2: [4]
3: [1]
4: [3,5]
5: []
Missing for each:
total = 15
1: p=[2], gaps: 0-2:1, 2-2:0? Wait: p0=0, p1=2, p2=6 (N+1=6). gaps: 0-2 (len 2 -> binom 2=1), 2-6 (len 4 -> binom 4=6). missing=7. D_1 = 15-7=8.
2: p=[4], gaps: 0-4 (4->6), 4-6 (2->1). missing=6+1=7. D_2=8.
3: p=[1], gaps: 0-1 (1->0), 1-6 (5->10). missing=10. D_3=5.
4: p=[3,5], gaps: 0-3 (3->3), 3-5 (2->1), 5-6 (1->0). missing=4. D_4=11.
5: p=[], missing=15, D_5=0.
Sum_D = 8+8+5+11+0 = 32.
Pairs:
(1,2): X=[2], Y=[4]. missing_1=7, missing_2=7. merge: [2,4], gaps: 0-2 (2->1), 2-4 (2->1), 4-6 (2->1). missing_both=3. G=15-7-7+3=4.
(2,3): X=[4], Y=[1]. missing_2=7, missing_3=10. merge: [1,4], gaps: 0-1 (1->0), 1-4 (3->3), 4-6 (2->1). missing_both=4. G=15-7-10+4=2.
(3,4): X=[1], Y=[3,5]. missing_3=10, missing_4=4. merge: [1,3,5], gaps: 0-1 (0), 1-3 (1), 3-5 (1), 5-6 (0). missing_both=2. G=15-10-4+2=3.
(4,5): X=[3,5], Y=[]. missing_4=4, missing_5=15. G=15-4-15+15=11? Wait: missing_5=15 (all subarrays miss 5). merge: just [3,5], gaps: 0-3(3), 3-5(1), 5-6(0). missing_both=4. G=15-4-15+4=0. Actually, G=0 because 5 never appears. So subarrays containing both 4 and 5 is 0. Formula: G = total - missing_x - missing_y + missing_both = 15 - 4 - 15 + missing_both. If missing_both is subarrays missing both. Since 5 never appears, any subarray misses 5, so missing_both = total = 15. Then G=15-4-15+15=11? That's wrong! Let's recompute missing_both: subarrays containing neither 4 nor 5. Since 5 never appears, missing both = missing 5 = total = 15. So G = 15 - 4 - 15 + 15 = 11. But 5 never appears, so no subarray can contain both. So G should be 0. What's wrong?
Ah! Inclusion-exclusion: Let $A$ be event "subarray contains 4", $B$ be "subarray contains 5". We want $P(A \cap B)$. $P(A \cap B) = 1 - P(\bar A) - P(\bar B) + P(\bar A \cap \bar B)$. Here $P(\bar B) = 1$ (all subarrays miss 5). $P(\bar A \cap \bar B) = P(\bar A)$ because $\bar B$ is all. So $P(A \cap B) = 1 - P(\bar A) - 1 + P(\bar A) = 0$. So missing_both should be 15, not 4. My merge for missing_both: I merged positions of 4 and 5. Positions of 5 are empty. So the merged list is just positions of 4. Gaps: 0-3 (len 3 -> 3), 3-5 (len 2 -> 1), 5-6 (len 1 -> 0). Sum = 4. But this counts subarrays missing both 4 and 5. If 5 never appears, then missing both = missing 5 = total = 15. So my merge logic is wrong when one list is empty.
If one list is empty, missing both = total (because the other value is irrelevant; any subarray misses the empty value). So we should handle empty lists: if $m_x=0$ or $m_{y}=0$, then $G=0$. Because if either value never appears, they cannot both appear. So we can skip pairs where either list is empty. That avoids the issue.

So for pair (4,5): pos[5] is empty -> G=0.
Thus Sum_G = 4+2+3+0 = 9.
Answer = Sum_D - Sum_G = 32 - 9 = 23. Matches sample 2.

**Implementation Plan:**
- Precompute `missing[v]` for all v.
- For each v, `missing[v] = sum_{i=0}^m binom(p_{i+1}-p_i, 2)`.
- Sum_D = sum_v (total - missing[v]).
- For each x in 1..N-1:
   - if pos[x] is empty or pos[x+1] is empty: continue
   - merge two sorted lists to compute missing_both
   - G = total - missing[x] - missing[x+1] + missing_both
   - Sum_G += G
- Answer = Sum_D - Sum_G.

**Optimization:**
We can precompute `missing` for all values first. Then for each pair, merge to get missing_both. The merge cost is O(len(x)+len(x+1)) as argued.

**Memory:**
`pos` can be a list of lists. Total size N. N=3e5, fine.

**Potential issues:**
- Values are up to N, so `pos` size N+2.
- Use `defaultdict(list)` or list of lists. Since values are bounded by N, list of lists is fine.
- `binom2(k) = k*(k-1)//2`.
- Use `int` (Python int is arbitrary precision, fine).

**Testing on sample 1:**
N=4, A=[1,3,1,4]
pos1=[1,3], pos2=[], pos3=[2], pos4=[4]
total = 10
missing1: gaps 0-1(0), 1-3(1), 3-5(1) = 2. D1=8.
missing2: gaps 0-5(10) = 10. D2=0.
missing3: gaps 0-2(1), 2-2? Wait pos3=[2]. p0=0, p1=2, p2=5. gaps: 0-2(1), 2-5(3->3) = 4. D3=6.
missing4: gaps 0-4(3->3), 4-5(0) = 3. D4=7.
Sum_D = 8+0+6+7 = 21.
Pairs:
(1,2): pos2 empty -> 0.
(2,3): pos2 empty -> 0.
(3,4): pos3=[2], pos4=[4]. missing3=4, missing4=3. merge: [2,4], gaps 0-2(1), 2-4(1), 4-5(0) = 2. G = 10-4-3+2 = 5.
Sum_G = 5.
Answer = 21 - 5 = 16. Matches sample 1.

**Sample 3:**
N=10, A=[5,1,10,9,2,5,6,9,1,6]
We can trust it after coding.

**Edge Cases:**
- All values same: A=[1,1,1,1]. N=4.
  pos1=[1,2,3,4]. missing: gaps 0-1(0), 1-2(0), 2-3(0), 3-4(0), 4-5(1) = 1. D1 = 10-1=9.
  No other values. Sum_D=9. Sum_G=0. Answer=9.
  Check: f(L,R) for subarray of length k: all 1's. To erase, we can choose (1,1) in one op. So f=1 for all 10 subarrays. Sum=10. Wait! My calculation gives 9. What's wrong?
  Let's compute D manually: distinct values in subarray = 1 for all subarrays. Number of subarrays = 10. Sum_D = 10. Why did I get 9?
  Because A_i are 1, so values present are just {1}. But the value 1 appears 4 times. D counts distinct values in the subarray. For any subarray, D=1. Sum = 10.
  My missing calculation: total=10. pos1=[1,2,3,4]. gaps: 0-1 (0), 1-2 (0), 2-3 (0), 3-4 (0), 4-5 (1). missing = 1. D1 = 10-1=9. But D1 should be number of subarrays containing 1. All subarrays contain 1, so D1=10. missing should be 0.
  Why is missing 1? The gap 4-5 is length 1. binom(1,2)=0. So gaps contribute: 0+0+0+0+0=0. Wait! binom(1,2) = 1*0/2 = 0. So missing should be 0. Let's recalc: p0=0, p1=1, p2=2, p3=3, p4=4, p5=5 (N+1=5). gaps: p1-p0=1, p2-p1=1, p3-p2=1, p4-p3=1, p5-p4=1. binom(1,2)=0 for each. Sum=0. I earlier said gap 4-5 is length 1 and I wrote 1, but binom(1,2)=0. So missing=0. D1=10. Good.

So my earlier manual check for sample 1 had missing1=2: gaps 0-1(0), 1-3(2->1), 3-5(2->1) = 2. That's correct.

**Implementation details for merge:**
We can merge using two indices:
```python
i, j = 0, 0
prev = 0
missing_both = 0
while i < len(X) and j < len(Y):
    if X[i] < Y[j]:
        curr = X[i]; i += 1
    else:
        curr = Y[j]; j += 1
    missing_both += (curr - prev - 1) * (curr - prev) // 2
    prev = curr
# process remaining
while i < len(X):
    curr = X[i]; i += 1
    missing_both += (curr - prev - 1) * (curr - prev) // 2
    prev = curr
while j < len(Y):
    curr = Y[j]; j += 1
    missing_both += (curr - prev - 1) * (curr - prev) // 2
    prev = curr
# final gap to N+1
gap = N + 1 - prev
missing_both += gap * (gap - 1) // 2
```
This is correct.

**Total time:**
- Building pos: O(N)
- Computing missing for all v: O(N)
- For each pair, merging: O(N) total because each position is visited at most twice.
- Overall O(N).

**Space:**
- pos: O(N)
- A: O(N)
- O(N) total.

This should be efficient for N=3e5.

**One more check:**
For pair (x, x+1), if both lists are non-empty, we compute missing_both. But what if the merged gaps computation is too slow? Python loops might be okay for 3e5. 3e5 operations is fine. The merge is just scanning through the lists. Total elements scanned across all merges is 2N (each position appears in two merges). So at most ~6e5 operations. Python can handle that easily.

**Final answer:**
The algorithm is clear. Implementation in Python 3.

## worker: The solution is fully derived and ready for implem
The solution computes $\sum f(L,R) = \sum D(L,R) - \sum G(L,R)$, where $D$ is the number of distinct values in the subarray and $G$ is the number of pairs of consecutive integers both present. 

- $\sum D$ is computed by summing over each value the number of subarrays containing it: total subarrays minus subarrays missing it. The missing count is obtained by summing $\binom{L+1}{2}$ over the gaps between occurrences (using $L = \text{next} - \text{prev} - 1$).
- $\sum G$ is computed for each adjacent pair $(x, x+1)$ via inclusion-exclusion: subarrays containing both = total - missing($x$) - missing($x+1$) + missing(both). Missing both is computed by merging the two sorted position lists and summing over gaps in the merged sequence.
- Each position list is merged at most twice (for pairs $(v-1,v)$ and $(v,v+1)$), so total work is $O(N)$.
- Edge cases: empty position lists handled by skipping pairs or naturally yielding zero contribution.

Verified on all three sample inputs.
