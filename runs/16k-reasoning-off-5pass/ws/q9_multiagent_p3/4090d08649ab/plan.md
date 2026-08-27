The problem asks for the sum of the minimum operations $f(L,R)$ to erase a subarray. This operation allows removing all occurrences of a value if they form a contiguous range of indices (relative to the current set of indices). This structure implies that $f(L,R)$ is related to the number of "connected components" of identical values when considering the constraints of the operation. Specifically, we can model this using a Disjoint Set Union (DSU) or by observing that the cost is related to the number of times a value "starts" a new necessary operation block. A more robust approach for the sum is to count how many times each subarray contributes $+1$ to the total sum. A subarray $(L,R)$ contributes $k$ to the sum if it requires $k$ operations. We can rephrase this: $f(L,R) = 1 + \sum_{i=L}^{R-1} [ \text{operation needed at } i ]$. The condition for needing a new operation at index $i$ (splitting $[L, i]$ from $[i+1, R]$) is complex due to the "erase all occurrences" rule. However, a known property for this specific "erase contiguous range of values" game is that $f(L,R)$ equals the number of "blocks" of identical values in the subarray if we merge adjacent identical values? No, the sample shows `1 3 1 4` -> 2 ops. Blocks: `1`, `3`, `1`, `4`. If we treat identical values as mergeable only if they are adjacent, we get 4 blocks. But we can remove `1`s at indices 1 and 3 together because the range $(1,3)$ covers them? Wait, the rule says: choose $l, r$ such that *every integer from $l$ through $r$ appears at least once*. Then erase all occurrences of values in that range? No, "erase all integers from $l$ through $r$ that are on the blackboard". This means we pick a range of *indices* $[l, r]$ (relative to the current sequence positions? Or original values?). The example says: "Choose $(l,r)=(1,1)$ and erase all occurrences of 1". This implies $l, r$ refer to the *values* present? No, "integers from $l$ through $r$". If the board has $\{1, 3, 1, 4\}$, and we pick $l=1, r=1$, we erase all $1$s. The remaining is $\{3, 4\}$. Then pick $l=3, r=4$, erase 3 and 4.
Actually, the standard interpretation of this specific problem (AtCoder ABC 348 F? No, likely a specific contest problem) is that we can remove a set of values $V$ if the indices of all occurrences of values in $V$ form a contiguous interval in the current array.
Let's re-read carefully: "Choose integers $l, r$ ... such that every integer from $l$ through $r$ appears at least once on the blackboard." This means the set of values $\{v \mid l \le v \le r\}$ must be a subset of the values currently on the board. Then we erase all instances of these values.
This is equivalent to: We can remove a set of values $S$ if $\min(S) \ge l$ and $\max(S) \le r$ and all values in $[l, r]$ are present.
Actually, the example logic: Board `1, 3, 1, 4`. Values present: $\{1, 3, 4\}$.
Op 1: Choose $l=1, r=1$. Values in $[1,1]$ is $\{1\}$. Is $\{1\} \subseteq \{1, 3, 4\}$? Yes. Erase all 1s. Board: `3, 4`.
Op 2: Choose $l=3, r=4$. Values in $[3,4]$ are $\{3, 4\}$. Is $\{3, 4\} \subseteq \{3, 4\}$? Yes. Erase all.
So the strategy is: Pick a range of values $[l, r]$ such that all values in that range are currently present on the board. Remove all instances of those values.
Goal: Minimize operations.
This is equivalent to finding the minimum number of steps to cover the set of values present in the subarray $A[L..R]$ using intervals $[l_k, r_k]$ such that for each step, the union of values in $[l_k, r_k]$ is a subset of the current values, and we remove them.
Actually, since we can pick any $l, r$ as long as all values in between are present, this is equivalent to: In one step, we can remove a contiguous range of values $[l, r]$ provided that *every* value between $l$ and $r$ exists in the current subarray.
Let $S$ be the set of distinct values in $A[L..R]$. Let $min\_val = \min(S)$ and $max\_val = \max(S)$.
If we pick $[min\_val, max\_val]$, we need all values between $min\_val$ and $max\_val$ to be in $S$. If there is a missing value $x$ ($min < x < max$) not in $S$, we cannot pick $[min, max]$ in one go. We must split.
This looks like finding the minimum number of intervals to cover $S$ such that each interval $[l, r]$ has no "holes" (missing values) relative to the range $[l, r]$.
Wait, if we pick $[l, r]$, we remove all occurrences of values in $[l, r]$. The next step operates on the remaining values.
Crucially, the set of values available only shrinks. The "holes" (missing values) never disappear; they were never there.
So, if the set of values in $A[L..R]$ is $S$, and we want to cover $S$ with intervals $I_1, I_2, \dots, I_k$ such that each $I_j$ contains no values outside $S$, and the union is $S$.
Actually, the condition is: For an interval $[l, r]$ to be valid, $\{v \in \mathbb{Z} \mid l \le v \le r\} \subseteq S$.
This means $[l, r]$ must be a subset of the "connected components" of $S$ when viewed on the number line.
Let the distinct values in $A[L..R]$ sorted be $v_1 < v_2 < \dots < v_m$.
The values form several contiguous blocks on the number line. For example, if $S=\{1, 2, 4, 5, 7\}$, the blocks are $[1,2], [4,5], [7,7]$.
In one operation, we can pick any $[l, r]$ that is fully contained within one of these blocks. Since we want to minimize operations, we should pick the maximal possible intervals.
Can we pick $[1, 2]$? Yes. Removes 1 and 2.
Can we pick $[4, 5]$? Yes. Removes 4 and 5.
Can we pick $[7, 7]$? Yes.
So the number of operations is simply the number of contiguous blocks of values in the set $S$.
Let's verify with Sample 1: `1 3 1 4`. Subarray $L=1, R=4$. Values: $\{1, 3, 4\}$. Sorted: $1, 3, 4$.
Blocks: $[1,1]$ (since 2 is missing), $[3,4]$ (3 and 4 are adjacent).
Number of blocks = 2. Output $f(1,4)=2$. Correct.
Sample 1, $L=2, R=4$: `3 1 4`. Values $\{1, 3, 4\}$. Same blocks. $f=2$.
$L=1, R=3$: `1 3 1`. Values $\{1, 3\}$. Blocks $[1,1], [3,3]$. $f=2$.
$L=1, R=2$: `1 3`. Values $\{1, 3\}$. $f=2$.
$L=2, R=2$: `3`. Values $\{3\}$. $f=1$.
Sum:
(1,1): {1} -> 1
(1,2): {1,3} -> 2
(1,3): {1,3} -> 2
(1,4): {1,3,4} -> 2
(2,2): {3} -> 1
(2,3): {3,1}->{1,3} -> 2
(2,4): {3,1,4}->{1,3,4} -> 2
(3,3): {1} -> 1
(3,4): {1,4} -> 2
(4,4): {4} -> 1
Total: 1+2+2+2 + 1+2+2 + 1+2 + 1 = 16. Matches sample.

Algorithm:
For each subarray, calculate the number of contiguous blocks of distinct values.
$f(L,R) = \text{count of } i \text{ such that } v_i \text{ is the start of a block}$.
$v_i$ is a start of a block if $v_i = v_{i-1} + 1$ is FALSE (or $i=1$).
Basically, $f(L,R) = |S| - (\text{number of adjacent pairs } (u, v) \in S \text{ such that } v = u+1)$.
Wait, $|S|$ is the number of distinct elements. If we have a block of size $k$, it contributes 1 to the count. The number of adjacent pairs in that block is $k-1$.
So $1 = k - (k-1)$. Summing over blocks: $\sum (k_j - (k_j-1)) = \sum k_j - \sum (k_j-1) = |S| - (\text{total adjacent pairs})$.
Yes. $f(L,R) = (\text{number of distinct values in } A[L..R]) - (\text{number of pairs } (u, v) \text{ in distinct values such that } v = u+1)$.
We need to sum this over all $L, R$.
Total Sum = $\sum_{L,R} (\text{distinct count}) - \sum_{L,R} (\text{adjacent pairs count})$.
Part 1: Sum of distinct counts over all subarrays. This is a standard problem solvable in $O(N \log N)$ or $O(N)$.
Part 2: Sum of adjacent pairs. A pair of values $(x, x+1)$ contributes to the count for a subarray $A[L..R]$ if and only if:
1. Both $x$ and $x+1$ appear in $A[L..R]$.
2. They are "adjacent" in the set of distinct values. This just means $x$ and $x+1$ are both present. The condition "adjacent in sorted distinct values" is automatically satisfied if $x$ and $x+1$ are both present (since there is no integer between them).
So we need to count, for each $x \in [1, N-1]$, how many subarrays $A[L..R]$ contain both $x$ and $x+1$.
Let $pos[x]$ be the list of indices where value $x$ appears.
For a fixed $x$, we need to count pairs $(L, R)$ such that $L \le \min(idx_x, idx_{x+1})$ and $R \ge \max(idx_x, idx_{x+1})$ for some occurrence of $x$ and some occurrence of $x+1$ within $[L, R]$.
Actually, simpler: A subarray $[L, R]$ contains both $x$ and $x+1$ iff $L \le \text{last\_occurrence\_before\_R}(x)$? No.
Condition: $\exists i, j$ such that $L \le i \le R$ and $A[i]=x$, and $L \le j \le R$ and $A[j]=x+1$.
This is equivalent to: $L \le \max(\text{indices of } x \text{ in } [L,R])$? No.
It is equivalent to: $L \le \min(\text{index of } x \text{ in } [L,R], \text{index of } x+1 \text{ in } [L,R])$ and $R \ge \max(\dots)$.
Let's rephrase: For a fixed $x$, consider all pairs of indices $(i, j)$ such that $A[i]=x$ and $A[j]=x+1$. The subarray $[L, R]$ covers both if $L \le \min(i, j)$ and $R \ge \max(i, j)$.
However, we must avoid double counting if a subarray contains multiple pairs of $(x, x+1)$.
Actually, the condition "contains both $x$ and $x+1$" is binary for a subarray. It doesn't matter how many pairs.
So for each $x$, we need to count subarrays containing at least one $x$ and at least one $x+1$.
Total subarrays = $N(N+1)/2$.
Subarrays NOT containing $x$ OR NOT containing $x+1$.
Count = Total - (Subarrays missing $x$) - (Subarrays missing $x+1$) + (Subarrays missing both).
This seems complicated to do for every $x$ efficiently ($O(N^2)$ worst case if many occurrences).
Alternative approach for Part 2:
Iterate through the array. For each $x$, find the nearest occurrence of $x+1$ to the left and right?
Let's use the contribution technique.
For a fixed $x$, let the positions of $x$ be $p_1, p_2, \dots$ and $x+1$ be $q_1, q_2, \dots$.
A subarray $[L, R]$ contains both iff $L \le \min(p_a, q_b)$ and $R \ge \max(p_a, q_b)$ for some $a, b$.
This is equivalent to: The range $[L, R]$ intersects the set of indices of $x$ AND intersects the set of indices of $x+1$.
Let $S_x$ be the set of indices of $x$, $S_{x+1}$ be indices of $x+1$.
We want to count pairs $(L, R)$ such that $[L, R] \cap S_x \neq \emptyset$ and $[L, R] \cap S_{x+1} \neq \emptyset$.
This is equal to: Total - (pairs disjoint from $S_x$) - (pairs disjoint from $S_{x+1}$) + (pairs disjoint from both).
Disjoint from $S_x$: $L > \max(S_x \cap [1, R])$.
Actually, simpler:
For a fixed $x$, let's iterate over the array and maintain the last seen position of $x$ and $x+1$.
But we need the sum over all $L, R$.
Let's use the property: $f(L,R) = \text{distinct} - \text{adjacent\_pairs}$.
Sum of distinct: Standard problem.
Sum of adjacent pairs: For each $x$, count subarrays containing $x$ and $x+1$.
Let $cnt(x)$ be the number of subarrays containing both $x$ and $x+1$.
We can compute $cnt(x)$ by iterating over the array and tracking the last seen positions.
Actually, there is a simpler way.
For a fixed $x$, let the occurrences of $x$ be $u_1, u_2, \dots$ and $x+1$ be $v_1, v_2, \dots$.
The condition "contains both" is satisfied if $L \le \min(u_i, v_j)$ and $R \ge \max(u_i, v_j)$ for some $i, j$.
This is equivalent to: $L \le \text{something}$ and $R \ge \text{something}$.
Consider the array of booleans $B$ where $B[i]=1$ if $A[i] \in \{x, x+1\}$, else 0.
We need subarrays that contain at least one $x$ and at least one $x+1$.
This is hard because we need to distinguish which is which.
Better approach:
For each $x$, iterate through the array. Maintain `last_x` and `last_x_plus_1`.
When we are at index $i$ (considering $R=i$), we want to count how many $L \le i$ satisfy the condition.
Condition: $[L, i]$ contains $x$ and $x+1$.
This requires $L \le \text{last\_seen}(x)$ AND $L \le \text{last\_seen}(x+1)$.
So $L \le \min(\text{last\_seen}(x), \text{last\_seen}(x+1))$.
The number of such $L$ is $\min(\text{last\_seen}(x), \text{last\_seen}(x+1))$.
Wait, this counts subarrays ending at $i$ that contain $x$ and $x+1$.
But we must ensure that $x$ and $x+1$ have appeared *before or at* $i$.
If either hasn't appeared yet, count is 0.
So, for each $x \in [1, N-1]$:
Initialize `last_x = -1`, `last_x_plus_1 = -1`.
Iterate $i$ from 1 to $N$:
  If $A[i] == x$: `last_x = i`
  If $A[i] == x+1$: `last_x_plus_1 = i`
  If `last_x != -1` and `last_x_plus_1 != -1`:
    `count += min(last_x, last_x_plus_1)`
Sum these counts for all $x$.
This is $O(N)$ per $x$, total $O(N^2)$. Too slow ($N=3 \cdot 10^5$).
We need $O(N)$ or $O(N \log N)$.
Notice that we are summing $\min(last\_x, last\_x+1)$ over $i$.
This looks like we can process all $x$ simultaneously? No.
Wait, the total number of pairs $(x, x+1)$ is $N$. But the occurrences can be many.
Is there a way to optimize?
Actually, the sum of distinct elements can be computed in $O(N \log N)$.
The sum of adjacent pairs:
Let's reconsider the structure.
We need $\sum_{x} \sum_{i} [\text{both seen}] \times \min(last\_x, last\_x+1)$.
This is still hard.
Alternative view:
Total Sum = $\sum_{L,R} f(L,R)$.
$f(L,R)$ is the number of "blocks".
A block starts at value $v$ if $v$ is in the subarray, and $v-1$ is NOT in the subarray (or $v=1$).
So $f(L,R) = \sum_{v} [v \in S \text{ and } (v-1 \notin S \text{ or } v=1)]$.
Sum over all $L,R$:
$\sum_{v} \sum_{L,R} [v \in A[L..R] \text{ and } (v-1 \notin A[L..R] \text{ or } v=1)]$.
For $v=1$: Count subarrays containing 1.
For $v > 1$: Count subarrays containing $v$ AND NOT containing $v-1$.
Let $Count(v)$ be the number of subarrays containing $v$.
Let $Count(v, \neg (v-1))$ be the number of subarrays containing $v$ but not $v-1$.
Then Answer = $\sum_{v=1}^N Count(v, \neg (v-1))$. (With $Count(1, \neg 0) = Count(1)$).
How to compute $Count(v, \neg (v-1))$ efficiently?
For a fixed $v$, we need subarrays that contain at least one $v$ and no $v-1$.
Let the positions of $v-1$ be $P_{v-1}$ and positions of $v$ be $P_v$.
We need $[L, R]$ such that $[L, R] \cap P_v \neq \emptyset$ and $[L, R] \cap P_{v-1} = \emptyset$.
This means the entire subarray must lie within a gap between occurrences of $v-1$.
Let the gaps defined by $v-1$ be intervals $[g_1, g_2], [g_2+1, g_3], \dots$.
Specifically, if $v-1$ is at indices $q_1, q_2, \dots, q_k$, then the valid ranges for $L, R$ must be within $[1, q_1-1]$, $[q_1+1, q_2-1]$, ..., $[q_k+1, N]$.
Within each such gap interval $[a, b]$, we need to count subarrays that contain at least one $v$.
Let the occurrences of $v$ inside $[a, b]$ be $u_1, u_2, \dots, u_m$.
The number of subarrays in $[a, b]$ containing at least one $u_j$ is:
(Total subarrays in $[a, b]$) - (Subarrays in $[a, b]$ containing NO $v$).
Total subarrays in $[a, b]$ is $(b-a+1)(b-a+2)/2$.
Subarrays containing no $v$ are those entirely within the gaps between $u_j$'s inside $[a, b]$.
If $u_j$ are the occurrences of $v$ in $[a, b]$, then the "no $v$" subarrays are unions of subarrays in $[a, u_1-1]$, $[u_1+1, u_2-1]$, ..., $[u_m+1, b]$.
This can be computed for each gap of $v-1$.
Since each index belongs to exactly one gap of $v-1$, and we iterate $v$, the total complexity?
Sum of lengths of gaps for a fixed $v$ is $N$.
We do this for each $v$. Total complexity $O(N^2)$. Still too slow.
We need a linear scan.
Let's go back to: $f(L,R) = \text{distinct} - \text{adjacent\_pairs}$.
Sum of distinct: $O(N \log N)$ or $O(N)$.
Sum of adjacent pairs: $\sum_{x} (\text{subarrays containing } x \text{ and } x+1)$.
Let's try to optimize the "subarrays containing $x$ and $x+1$" calculation.
For a fixed $x$, let $pos[x]$ be the list of indices.
We want to count pairs $(L, R)$ such that $[L, R]$ hits $pos[x]$ and $pos[x+1]$.
This is equivalent to: Total subarrays - (subarrays missing $x$) - (subarrays missing $x+1$) + (subarrays missing both).
Let $Missing(S)$ be the number of subarrays that do not contain any element of set $S$.
$Missing(S) = \sum_{\text{gaps in } S} \text{len}(gap)(\text{len}(gap)+1)/2$.
So for each $x$, we need:
$Total - Missing(\{x\}) - Missing(\{x+1\}) + Missing(\{x, x+1\})$.
$Missing(\{x, x+1\})$ is the number of subarrays containing neither $x$ nor $x+1$.
This is the sum of subarray counts in the gaps formed by the union of positions of $x$ and $x+1$.
Let $U_x = pos[x] \cup pos[x+1]$. Sort $U_x$.
The gaps are intervals between consecutive elements of $U_x$.
We need to sum $\frac{k(k+1)}{2}$ for all gap lengths $k$.
Can we do this for all $x$ efficiently?
The union of positions changes as $x$ increments.
However, note that $pos[x]$ and $pos[x+1]$ are independent.
Maybe we can iterate over the array once and maintain something?
Actually, the constraints $N=3 \cdot 10^5$ suggest $O(N \log N)$.
The term $Missing(\{x, x+1\})$ is the tricky part.
But notice: $Missing(\{x, x+1\})$ is the number of subarrays that avoid both $x$ and $x+1$.
Let $B_i = 1$ if $A[i] \in \{x, x+1\}$ else 0.
We need sum of $(len+1)len/2$ for contiguous segments of 0s in $B$.
This is equivalent to: Total subarrays - (subarrays with at least one 1).
Subarrays with at least one 1 = Total - Subarrays with all 0s.
So we are back to counting subarrays with at least one $x$ and at least one $x+1$.
Let's use the contribution of each pair of indices $(i, j)$ with $A[i]=x, A[j]=x+1$.
No, that's double counting.
Let's use the "last seen" idea but aggregate.
For each $x$, we want $\sum_{i} \min(last\_x(i), last\_{x+1}(i))$ where $last\_x(i)$ is the last index $\le i$ with value $x$.
This sum is over all $i$.
Let's define $L_x[i]$ = last index $\le i$ with value $x$.
We want $\sum_{i=1}^N [L_x[i] \neq -1 \land L_{x+1}[i] \neq -1] \times \min(L_x[i], L_{x+1}[i])$.
This looks like we can process all $x$ in parallel?
No, $L_x$ depends on $x$.
However, notice that for a fixed $i$, the values $A[i]$ is just one number.
Maybe we can iterate $i$ and update the counts for $x = A[i]$ and $x = A[i]-1$?
When we are at $i$, let $u = A[i]$.
Then $L_u[i] = i$.
For the pair $(u-1, u)$, we have updated $L_u$. The term $\min(L_{u-1}[i], L_u[i])$ becomes $\min(L_{u-1}[i], i)$.
Since $L_{u-1}[i]$ is the last occurrence of $u-1$ before $i$, this is just $L_{u-1}[i]$ (if it exists).
So for the pair $(u-1, u)$, at step $i$, we add $L_{u-1}[i]$ to the total count (if $L_{u-1}[i]$ exists).
Similarly, for the pair $(u, u+1)$, we have updated $L_u$. We add $\min(L_{u+1}[i], i) = L_{u+1}[i]$ (if it exists).
Wait, the formula was $\sum_i \min(L_x[i], L_{x+1}[i])$.
At step $i$, if $A[i] = x$, then $L_x[i] = i$. The term is $\min(i, L_{x+1}[i])$.
If $L_{x+1}[i]$ exists, we add $L_{x+1}[i]$.
If $A[i] = x+1$, then $L_{x+1}[i] = i$. The term is $\min(L_x[i], i)$.
If $L_x[i]$ exists, we add $L_x[i]$.
So, we can maintain an array `last_pos[v]` for each value $v$.
Iterate $i$ from 1 to $N$:
  $u = A[i]$
  `last_pos[u] = i`
  // Update pair (u-1, u)
  if `last_pos[u-1]` exists:
      `total_adj += last_pos[u-1]`
  // Update pair (u, u+1)
  if `last_pos[u+1]` exists:
      `total_adj += last_pos[u+1]`
Wait, is this correct?
The term for pair $(x, x+1)$ at step $i$ is $\min(L_x[i], L_{x+1}[i])$.
If $A[i] = x$, $L_x[i] = i$. Term = $\min(i, L_{x+1}[i]) = L_{x+1}[i]$ (since $L_{x+1}[i] \le i$).
If $A[i] = x+1$, $L_{x+1}[i] = i$. Term = $\min(L_x[i], i) = L_x[i]$.
If $A[i]$ is neither, then $L_x[i] = L_x[i-1]$ and $L_{x+1}[i] = L_{x+1}[i-1]$. The term is $\min(L_x[i-1], L_{x+1}[i-1])$.
My proposed update only adds when $A[i]$ is one of the pair. It misses the cases where $A[i]$ is neither, but both have appeared before.
Example: $x=1, x+1=2$. Array: `1 2 3`.
$i=1, A[1]=1$. $L_1=1, L_2=-1$. Add 0.
$i=2, A[2]=2$. $L_2=2, L_1=1$. Add $L_1=1$. Total=1.
$i=3, A[3]=3$. $L_1=1, L_2=2$. Term $\min(1, 2)=1$.
My logic: At $i=3$, $A[3]=3$. Neither 1 nor 2. No update.
So I miss the contribution at $i=3$.
The contribution at $i$ is $\min(L_x[i], L_{x+1}[i])$.
This value is non-decreasing as $i$ increases? No, $L_x[i]$ is non-decreasing.
Actually, $L_x[i]$ stays constant until we see $x$.
So the term $\min(L_x[i], L_{x+1}[i])$ is constant between updates.
We can't just sum the updates.
We need to sum the values.
But note: The sum is $\sum_{i} \min(L_x[i], L_{x+1}[i])$.
This is equivalent to: For each $i$, add $\min(L_x[i], L_{x+1}[i])$.
Since $L_x[i]$ only changes when $A[i]=x$, we can maintain the current min.
Let $m_x = \min(L_x[i], L_{x+1}[i])$.
When $A[i] = x$, $L_x$ becomes $i$, so $m_x$ becomes $\min(i, L_{x+1}[i]) = L_{x+1}[i]$.
When $A[i] = x+1$, $L_{x+1}$ becomes $i$, so $m_x$ becomes $\min(L_x[i], i) = L_x[i]$.
When $A[i]$ is neither, $m_x$ stays the same.
So we can maintain $m_x$ for all $x$.
Initialize $m_x = 0$ for all $x$.
Iterate $i$:
  $u = A[i]$
  `last_pos[u] = i`
  // Update $m_{u-1}$ (pair u-1, u)
  if $u > 1$:
     new_m = min(last_pos[u-1], last_pos[u]) // last_pos[u] is i
     // But we need to add the difference?
     // We need to add the value of $m_{u-1}$ for all steps from prev_i to i-1?
     // No, we are summing over $i$.
     // Let's restructure: We want $\sum_i m_x(i)$.
     // $m_x(i)$ is the value at step $i$.
     // When $A[i] = u$, $m_{u-1}$ updates from $\min(L_{u-1}, L_u^{old})$ to $\min(L_{u-1}, i) = L_{u-1}$.
     // $m_u$ updates from $\min(L_u^{old}, L_{u+1})$ to $\min(i, L_{u+1}) = L_{u+1}$.
     // This is getting complicated to track sums.

Alternative:
The sum $\sum_i \min(L_x[i], L_{x+1}[i])$ can be rewritten.
Let $p_1, p_2, \dots$ be positions of $x$.
Let $q_1, q_2, \dots$ be positions of $x+1$.
For any $i$, $L_x[i] = p_k$ where $p_k \le i < p_{k+1}$.
$L_{x+1}[i] = q_j$ where $q_j \le i < q_{j+1}$.
$\min(p_k, q_j)$.
This is a standard problem: Sum of $\min(L_x[i], L_{x+1}[i])$ over all $i$.
This is equal to $\sum_{k, j} \text{length of interval where } L_x=p_k, L_{x+1}=q_j \times \min(p_k, q_j)$.
The interval is $[\max(p_k, q_j), \min(p_{k+1}-1, q_{j+1}-1)]$.
Length = $\max(0, \min(p_{k+1}-1, q_{j+1}-1) - \max(p_k, q_j) + 1)$.
This is still $O(N^2)$ in worst case (e.g., alternating 1, 2, 1, 2).
But wait, we can use a segment tree or simply observe the structure.
Actually, there is a simpler formula for $\sum_i \min(L_x[i], L_{x+1}[i])$.
It is equal to $\sum_{k} \sum_{j} \min(p_k, q_j) \times \text{overlap}(p_k, q_j)$.
This is hard.

Let's go back to the "blocks" definition.
$f(L,R) = \text{number of blocks}$.
A block starts at $v$ if $v \in S$ and $v-1 \notin S$.
Sum = $\sum_v \sum_{L,R} [v \in S \land v-1 \notin S]$.
For $v=1$: Count subarrays containing 1.
For $v>1$: Count subarrays containing $v$ and NOT $v-1$.
Let $S_v$ be the set of indices of $v$.
Let $S_{v-1}$ be the set of indices of $v-1$.
We need subarrays $[L, R]$ such that $[L, R] \cap S_v \neq \emptyset$ and $[L, R] \cap S_{v-1} = \emptyset$.
This means $[L, R]$ must be contained in a gap of $S_{v-1}$.
Let the gaps of $S_{v-1}$ be $G_1, G_2, \dots$.
For each gap $G = [a, b]$, we count subarrays in $[a, b]$ that contain at least one $v$.
Count = (Total subarrays in $[a, b]$) - (Subarrays in $[a, b]$ with no $v$).
Total subarrays in $[a, b]$ is $T = (b-a+1)(b-a+2)/2$.
Subarrays with no $v$: Sum of $k(k+1)/2$ for gaps between occurrences of $v$ inside $[a, b]$.
Let occurrences of $v$ in $[a, b]$ be $u_1, u_2, \dots, u_m$.
Gaps: $[a, u_1-1], [u_1+1, u_2-1], \dots, [u_m+1, b]$.
Lengths: $l_0, l_1, \dots, l_m$.
Sum of $l_k(l_k+1)/2$.
This can be computed for each gap of $v-1$.
Total complexity: Sum over $v$ of (number of gaps of $v-1$).
Number of gaps of $v-1$ is roughly $|S_{v-1}| + 1$.
Sum of $|S_{v-1}|$ over all $v$ is $N$.
So we iterate over all gaps of all $v-1$.
For each gap, we need to find occurrences of $v$ inside it.
We can precompute the positions of each value.
For a gap $[a, b]$ of $v-1$, we need to sum $l_k(l_k+1)/2$ for segments between $v$'s.
This is equivalent to: Total subarrays in $[a, b]$ minus subarrays avoiding $v$.
Subarrays avoiding $v$ in $[a, b]$ is simply the sum of subarrays in the segments of $[a, b]$ that do not contain $v$.
These segments are defined by the positions of $v$.
We can iterate over all gaps of $v-1$, and for each, iterate over occurrences of $v$.
Since each index belongs to exactly one gap of $v-1$, and we visit each occurrence of $v$ once per gap it falls into?
No, an occurrence of $v$ falls into exactly one gap of $v-1$.
So each pair $(pos(v), gap(v-1))$ is visited once.
Total work: $\sum_v \sum_{gap \in Gaps(v-1)} (\text{occurrences of } v \text{ in } gap)$.
This is exactly $\sum_v |S_v| = N$.
So we can do this in $O(N)$!
Algorithm:
1. Store positions for each value: `pos[v]`.
2. Initialize `ans = 0`.
3. For each $v$ from 1 to $N$:
   a. If $v=1$:
      Count subarrays containing 1.
      Total subarrays - subarrays avoiding 1.
      Avoiding 1: Sum of $k(k+1)/2$ for gaps between 1s (including ends).
      Add to `ans`.
   b. If $v > 1$:
      We need subarrays containing $v$ AND avoiding $v-1$.
      Identify gaps of $v-1$.
      Gaps are intervals between consecutive occurrences of $v-1$.
      Let occurrences of $v-1$ be $q_1, q_2, \dots, q_m$.
      Gaps: $[1, q_1-1], [q_1+1, q_2-1], \dots, [q_m+1, N]$.
      For each gap $[a, b]$:
         Count subarrays in $[a, b]$ that contain at least one $v$.
         This is: Total in $[a, b]$ - (subarrays in $[a, b]$ avoiding $v$).
         To find subarrays avoiding $v$ in $[a, b]$:
            Find occurrences of $v$ in $[a, b]$. Let them be $u_1, \dots, u_k$.
            Segments: $[a, u_1-1], [u_1+1, u_2-1], \dots, [u_k+1, b]$.
            Sum $len(len+1)/2$ for these segments.
         Add (Total - Avoiding) to `ans`.
4. Print `ans`.

Complexity:
Outer loop $v$: $N$ times.
Inner loop over gaps of $v-1$: Number of gaps is $|S_{v-1}| + 1$.
Inner-inner loop over occurrences of $v$ in gap: Total occurrences of $v$ is $|S_v|$.
Each occurrence of $v$ is in exactly one gap of $v-1$.
So total iterations over all $v$ is $\sum_v (|S_{v-1}| + |S_v|) = O(N)$.
Sorting positions? We can store positions in sorted lists.
Finding occurrences of $v$ in $[a, b]$ can be done with binary search (`bisect`) on `pos[v]`.
Total time: $O(N \log N)$ due to binary searches.
This fits within limits.