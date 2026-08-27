To solve this problem, we need to compute the sum of $f(L, R)$ for all pairs $(L, R)$ with $1 \le L \le R \le N$. The function $f(L, R)$ represents the minimum number of operations to erase all integers from the subarray $A[L..R]$.

### Key Insight:
The operation allows us to erase a contiguous range of *values* $[l, r]$ if every integer in that value range appears at least once in the current blackboard. This is equivalent to finding the minimum number of "value-contiguous" segments needed to cover the set of distinct values present in $A[L..R]$, but with a twist: the erasure removes *all* occurrences of those values, potentially merging previously separated segments of other values.

Actually, let's re-read carefully. We choose $l, r$ such that every integer from $l$ through $r$ appears at least once on the blackboard. Then we erase all integers from $l$ through $r$ that are on the blackboard. This means we remove all occurrences of values $l, l+1, \dots, r$.

This process is equivalent to partitioning the set of distinct values present in $A[L..R]$ into the minimum number of contiguous value-intervals. Why? Because if we have a set of distinct values $S$, we can group them into contiguous blocks like $\{1,2,3\}, \{5,6\}, \{8\}$. Each block can be erased in one operation. The minimum number of operations is exactly the number of such contiguous blocks.

Let $S_{L,R}$ be the set of distinct values in $A[L..R]$. Sort these distinct values: $v_1 < v_2 < \dots < v_k$. The number of operations $f(L,R)$ is $1 + \sum_{i=1}^{k-1} \mathbb{I}(v_{i+1} > v_i + 1)$. That is, it's 1 plus the number of "gaps" between consecutive distinct values.

So, $f(L,R) = 1 + \text{number of gaps in the sorted distinct values of } A[L..R]$.

The total sum is:
$$ \sum_{L=1}^N \sum_{R=L}^N f(L,R) = \sum_{L=1}^N \sum_{R=L}^N \left(1 + \sum_{v \in S_{L,R}, v \text{ is not the smallest or has a gap before it}} 1 \right) $$

More precisely, let the distinct values in $A[L..R]$ be $v_1 < v_2 < \dots < v_k$. Then $f(L,R) = 1 + \sum_{j=2}^k \mathbb{I}(v_j > v_{j-1} + 1)$.

We can rewrite the total sum as:
$$ \sum_{L,R} 1 + \sum_{L,R} \sum_{j=2}^k \mathbb{I}(v_j > v_{j-1} + 1) $$
The first part is simply the number of pairs $(L,R)$, which is $N(N+1)/2$.

The second part counts the number of pairs $(L,R)$ such that there exists a "gap" between two consecutive distinct values in $A[L..R]$. Specifically, for any pair of distinct values $x, y$ with $y = x+1$, they don't contribute a gap. But if we have distinct values $a$ and $b$ in $A[L..R]$ with $b > a+1$, and there is no distinct value $c$ in $A[L..R]$ such that $a < c < b$, then the transition from $a$ to $b$ contributes a gap.

Actually, it's easier to count the gaps directly. A gap occurs between two consecutive distinct values $u, v$ in the sorted distinct set of $A[L,R]$ if $v > u+1$. This is equivalent to saying that the interval $[u+1, v-1]$ contains no values from $A[L..R]$.

Let's define a "gap event" for a pair $(L,R)$ as a pair of values $(u, v)$ such that $u, v \in S_{L,R}$, $v > u+1$, and no value in $(u, v)$ is in $S_{L,R}$. Note that for a fixed $(L,R)$, the gaps are uniquely determined by the sorted distinct values.

Alternatively, we can iterate over all possible "gap boundaries". A gap exists between value $x$ and value $y$ ($y > x+1$) in $A[L..R]$ if:
1. $x \in S_{L,R}$
2. $y \in S_{L,R}$
3. No value in $\{x+1, \dots, y-1\}$ is in $S_{L,R}$
4. $x$ and $y$ are consecutive in the sorted distinct values of $S_{L,R}$.

This condition 4 is hard to enforce directly. Instead, note that $f(L,R)$ is the number of connected components of the set $S_{L,R}$ under the adjacency relation $u \sim v$ if $|u-v|=1$. This is equivalent to $1 + \text{number of } u \in S_{L,R} \text{ such that } u-1 \notin S_{L,R} \text{ and } u \neq \min(S_{L,R})$.

So, $f(L,R) = \sum_{v \in S_{L,R}} \mathbb{I}(v-1 \notin S_{L,R})$.
Wait, if $v = \min(S_{L,R})$, then $v-1 \notin S_{L,R}$ is true, but we don't count it as a gap start? Let's check.
If $S_{L,R} = \{1, 3\}$, sorted: $1, 3$. Gap between 1 and 3. $f=2$.
Formula: $\sum_{v \in S} \mathbb{I}(v-1 \notin S)$.
For $v=1$: $0 \notin S$? Yes. Count 1.
For $v=3$: $2 \notin S$? Yes. Count 1.
Total 2. Correct.

If $S_{L,R} = \{1, 2, 4\}$, sorted: $1, 2, 4$. Gaps: none between 1,2; gap between 2,4. $f=2$.
Formula:
$v=1: 0 \notin S$. Count 1.
$v=2: 1 \in S$. Count 0.
$v=4: 3 \notin S$. Count 1.
Total 2. Correct.

So, $f(L,R) = \sum_{v \in S_{L,R}} \mathbb{I}(v-1 \notin S_{L,R})$.

The total sum is:
$$ \sum_{L=1}^N \sum_{R=L}^N \sum_{v \in S_{L,R}} \mathbb{I}(v-1 \notin S_{L,R}) $$
We can swap the sums:
$$ \sum_{v=1}^N \sum_{L=1}^N \sum_{R=L}^N \mathbb{I}(v \in S_{L,R} \text{ and } v-1 \notin S_{L,R}) $$

For a fixed $v$, we want to count the number of pairs $(L,R)$ such that:
1. The subarray $A[L..R]$ contains at least one occurrence of $v$.
2. The subarray $A[L..R]$ contains NO occurrence of $v-1$.

Let $Pos(x)$ be the list of indices where value $x$ appears in $A$.
Let $Occ(v-1)$ be the set of indices where $v-1$ appears. If $v-1$ does not appear in $A$, then condition 2 is always true.
If $v-1$ does not appear, then for each $v$, we just need to count pairs $(L,R)$ such that $A[L..R]$ contains $v$.
If $v-1$ does appear, then $(L,R)$ must not contain any index from $Occ(v-1)$. This means $[L,R]$ must lie entirely within a "gap" between consecutive occurrences of $v-1$ (or before the first or after the last).

Let's formalize.
For a fixed $v$:
Case 1: $v-1$ does not appear in $A$.
Then we count pairs $(L,R)$ such that $v \in S_{L,R}$.
This is equivalent to: Total pairs - Pairs that do NOT contain $v$.
Pairs that do not contain $v$ are those $[L,R]$ that lie entirely within gaps between occurrences of $v$.
Let $Pos(v) = [p_1, p_2, \dots, p_k]$. Add sentinel $p_0=0, p_{k+1}=N+1$.
The gaps are $(p_i, p_{i+1})$ for $i=0 \dots k$. The length of gap $i$ is $len_i = p_{i+1} - p_i - 1$.
Number of pairs in gap $i$ is $len_i(len_i+1)/2$.
So, count for $v$ is $N(N+1)/2 - \sum_{i=0}^k \frac{len_i(len_i+1)}{2}$.

Case 2: $v-1$ appears in $A$.
Let $Occ(v-1) = [q_1, q_2, \dots, q_m]$. Add sentinel $q_0=0, q_{m+1}=N+1$.
The valid intervals $[L,R]$ must not contain any $q_j$. So $[L,R]$ must be contained in one of the intervals $(q_j, q_{j+1})$.
Let $I_j = (q_j, q_{j+1})$. The indices in $I_j$ are $q_j+1, \dots, q_{j+1}-1$.
Let $len_j = q_{j+1} - q_j - 1$.
For each such interval $I_j$, we need to count pairs $(L,R)$ with $q_j < L \le R < q_{j+1}$ such that $v \in S_{L,R}$.
This is equivalent to: Total pairs in $I_j$ - Pairs in $I_j$ that do NOT contain $v$.
Total pairs in $I_j$ is $T_j = len_j(len_j+1)/2$.
Pairs in $I_j$ that do not contain $v$: We need to find occurrences of $v$ that are inside $I_j$. Let these be $r_1, r_2, \dots, r_s$.
Then the gaps within $I_j$ defined by these occurrences of $v$ will give us the pairs that don't contain $v$.
Specifically, let the positions of $v$ in $I_j$ be $r_1 < r_2 < \dots < r_s$.
Add sentinels relative to $I_j$: $start = q_j, end = q_{j+1}$.
The "gaps" for $v$ within $I_j$ are:
$(q_j, r_1), (r_1, r_2), \dots, (r_s, q_{j+1})$.
Lengths: $r_1 - q_j - 1$, $r_2 - r_1 - 1$, ..., $q_{j+1} - r_s - 1$.
Sum of pairs in these gaps is $G_j$.
Then count for this interval $I_j$ is $T_j - G_j$.
Sum over all $j$ gives the total count for $v$.

Algorithm:
1. Precompute positions for each value $1 \dots N$.
2. Initialize total sum = 0.
3. For each $v$ from 1 to $N$:
   a. If $v-1$ not in $A$ (i.e., $Pos(v-1)$ is empty):
      Count pairs containing $v$.
      $Pos(v) = [p_1, \dots, p_k]$. Sentinels $0, N+1$.
      Sum gaps: $\sum \frac{(p_{i+1}-p_i-1)(p_{i+1}-p_i)/2}{1}$? No, length is $p_{i+1}-p_i-1$. Pairs is $len(len+1)/2$.
      Count = $N(N+1)/2 - \sum_{i=0}^k \frac{len_i(len_i+1)}{2}$.
   b. If $v-1$ in $A$:
      $Occ(v-1) = [q_1, \dots, q_m]$. Sentinels $0, N+1$.
      For each interval $j$ from $0$ to $m$:
         $L_{bound} = q_j + 1, R_{bound} = q_{j+1} - 1$.
         If $L_{bound} > R_{bound}$, continue.
         $len = R_{bound} - L_{bound} + 1$.
         $T_j = len(len+1)/2$.
         Find occurrences of $v$ in $[L_{bound}, R_{bound}]$.
         Let these be $r_1, \dots, r_s$.
         Add sentinels $q_j$ and $q_{j+1}$ to the list of $v$'s positions for this interval.
         Calculate sum of pairs in gaps between consecutive $v$ positions (including sentinels).
         $G_j = \sum \frac{(next\_pos - prev\_pos - 1)(next\_pos - prev\_pos)/2}{1}$? No, length is $next\_pos - prev\_pos - 1$. Pairs is $len(len+1)/2$.
         Count for interval $j$ is $T_j - G_j$.
      Sum over $j$ is count for $v$.
   c. Add count for $v$ to total sum.

4. Print total sum.

Complexity:
For each $v$, we iterate over intervals defined by $v-1$. The total number of intervals across all $v$ is $\sum_{v} (|Occ(v-1)| + 1)$.
Inside each interval, we find occurrences of $v$. We can use binary search (bisect) on $Pos(v)$ to find occurrences in $[L_{bound}, R_{bound}]$.
The number of occurrences of $v$ in an interval is processed. The total work for finding and processing occurrences of $v$ across all intervals is proportional to $|Pos(v)|$ because each occurrence of $v$ belongs to exactly one interval defined by $v-1$ (the one that contains its index).
Wait, no. An occurrence of $v$ at index $k$ belongs to the interval $(q_j, q_{j+1})$ where $q_j < k < q_{j+1}$.
So, for each $v$, we iterate over intervals of $v-1$. For each interval, we get the occurrences of $v$ in that range.
The sum of $|Pos(v) \cap [L_{bound}, R_{bound}]|$ over all intervals is exactly $|Pos(v)|$.
So, for each $v$, the work is $O(|Occ(v-1)| + |Pos(v)| \log N)$ due to binary search to find the start of occurrences in each interval.
Actually, we can optimize. For each $v$, we have $Pos(v)$. We have $Occ(v-1)$.
We can iterate through the intervals of $v-1$. For each interval, we use bisect to find the range of indices in $Pos(v)$ that fall into the interval. Then we iterate through those occurrences to compute the gap sum.
Total complexity: $\sum_v (|Occ(v-1)| + |Pos(v)|) \log N$? No, bisect is $\log N$ per interval. Total intervals is $\sum_v (|Occ(v-1)| + 1) = N + N = 2N$.
So total bisect cost is $O(N \log N)$.
The iteration over occurrences of $v$ inside intervals: each occurrence of $v$ is visited once. Total $O(N)$.
So overall complexity is $O(N \log N)$.

Let's implement this.

```python
import sys
from bisect import bisect_left, bisect_right

def solve():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    
    # Precompute positions for each value
    # Values are 1 to N
    pos = [[] for _ in range(N+1)]
    for i, a in enumerate(A):
        pos[a].append(i+1) # 1-indexed positions
        
    total_sum = 0
    total_pairs = N * (N + 1) // 2
    
    for v in range(1, N+1):
        # We want to count pairs (L,R) such that v in S_{L,R} and v-1 not in S_{L,R}
        
        if v == 1:
            # v-1 = 0, which never appears
            # Count pairs containing v
            p_list = pos[v]
            # Gaps are before first, between, after last
            # Sentinels: 0, N+1
            prev = 0
            gap_sum = 0
            for p in p_list:
                length = p - prev - 1
                if length > 0:
                    gap_sum += length * (length + 1) // 2
                prev = p
            length = N + 1 - prev - 1
            if length > 0:
                gap_sum += length * (length + 1) // 2
            
            count_v = total_pairs - gap_sum
            total_sum += count_v
        else:
            # v-1 appears in A
            occ_prev = pos[v-1]
            # Intervals are (occ_prev[j], occ_prev[j+1]) for j=0..m
            # Sentinels: 0, N+1
            bounds = [0] + occ_prev + [N+1]
            
            count_v = 0
            p_list = pos[v]
            
            for j in range(len(bounds)-1):
                left_bound = bounds[j] + 1
                right_bound = bounds[j+1] - 1
                
                if left_bound > right_bound:
                    continue
                
                len_interval = right_bound - left_bound + 1
                total_in_interval = len_interval * (len_interval + 1) // 2
                
                # Find occurrences of v in [left_bound, right_bound]
                # Use bisect on p_list
                idx_start = bisect_left(p_list, left_bound)
                idx_end = bisect_right(p_list, right_bound)
                
                occ_v_in_interval = p_list[idx_start:idx_end]
                
                # Calculate gaps within this interval defined by occ_v_in_interval
                # Sentinels for this interval: left_bound-1 (which is bounds[j]) and right_bound+1 (which is bounds[j+1])
                prev_occ = bounds[j]
                gap_sum_interval = 0
                for occ in occ_v_in_interval:
                    length = occ - prev_occ - 1
                    if length > 0:
                        gap_sum_interval += length * (length + 1) // 2
                    prev_occ = occ
                length = bounds[j+1] - prev_occ - 1
                if length > 0:
                    gap_sum_interval += length * (length + 1) // 2
                    
                count_v += (total_in_interval - gap_sum_interval)
                
            total_sum += count_v
            
    print(total_sum)

solve()
```