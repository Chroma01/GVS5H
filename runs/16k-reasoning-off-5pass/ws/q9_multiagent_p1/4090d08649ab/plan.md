The problem asks for the sum of the minimum operations to clear subarrays, where an operation removes all occurrences of a contiguous range of values present in the current multiset. This is equivalent to finding the minimum path cover in a specific DAG or, more simply, recognizing that $f(L,R)$ corresponds to the number of "connected components" if we define connectivity based on value ranges. Specifically, we can model this by building a graph where nodes are indices and edges connect $i$ and $j$ if $A_i$ and $A_j$ can be removed together. However, a more direct combinatorial approach is to realize that $f(L,R)$ is the number of times we must "start" a new operation. An operation starting at value $v$ covers a range $[l, r]$. The optimal strategy is greedy: always pick the largest possible range $[l, r]$ that covers the first remaining element. This transforms the problem into counting how many times a new "chain" of dependencies is initiated. We can solve this by iterating all $L$ and using a monotonic stack or segment tree to efficiently calculate the contribution of each $R$, or by rephrasing the condition: $f(L,R)$ increases by 1 at $R$ if the new element $A_R$ cannot be covered by the range chosen for the previous element in the optimal sequence for $(L, R-1)$. Actually, a simpler property holds: $f(L,R)$ is the number of indices $i \in [L, R]$ such that $A_i$ is the "leftmost" occurrence of its value in the current active set that forces a new operation, or more formally, related to the number of "peaks" in a specific constructed array. Given constraints $N \le 3 \times 10^5$, an $O(N)$ or $O(N \log N)$ solution is required. The standard solution involves calculating for each $i$, the nearest previous index $j < i$ such that $A_j = A_i$ (let's call it $prev[i]$). Then $f(L,R)$ can be derived by counting how many times the "current chain" breaks. Specifically, $f(L,R) = 1 + \sum_{k=L}^{R-1} [ \text{condition} ]$. The condition is that $A_{k+1}$ cannot be grouped with the component containing $A_k$. This happens if the range of values needed to cover $A_k$ (which extends to include all occurrences of values between $A_k$'s value and the next distinct value) does not reach $k+1$. A known result for this specific problem (AtCoder ABC 266 F? No, this is likely a specific contest problem, possibly ARC or similar) is that $f(L,R)$ equals the number of indices $i \in [L, R]$ such that $i$ is the start of a new "segment" in a specific decomposition. Let's refine: The operation removes a range of values $[u, v]$. This removes all instances of numbers in $[u, v]$. The process stops when empty. This is equivalent to finding the minimum number of intervals $[u_k, v_k]$ such that every number in the subarray appears in at least one interval, and the intervals are "nested" or "compatible" in a way that allows sequential removal. Actually, the operation says: choose $l, r$ such that *every integer from $l$ through $r$ appears at least once*. Then erase *all* instances of those integers. This means one operation removes the set of values $S = \{x \mid l \le x \le r\}$. The constraint is that for the chosen $l, r$, every integer in $[l, r]$ must be present in the current multiset. We want to minimize operations. This is equivalent to covering the set of unique values present in $A[L..R]$ with minimum number of intervals $[l_k, r_k]$ such that for each interval, all integers in $[l_k, r_k]$ are present in the union of the sets of values removed in previous steps? No, the condition is on the *current* blackboard.
Let's re-read carefully: "Choose integers $l, r$ such that every integer from $l$ through $r$ appears at least once on the blackboard." Then erase all occurrences of $l \dots r$.
This implies we can only remove a contiguous range of values if *all* of them are currently present.
Strategy: To remove a set of values $V$, we need to find an interval $[l, r]$ covering $V$ such that $[l, r] \subseteq V$ (since if there's a missing value in $[l, r]$, we can't pick it). Thus, one operation can only remove a set of values that forms a contiguous range of integers.
So, $f(L,R)$ is the minimum number of contiguous ranges of integers needed to cover the set of unique values present in $A[L..R]$.
Wait, if we remove a range $[l, r]$, we remove all instances. The next operation works on the remaining values.
Example 1: 1, 3, 1, 4. Unique values: {1, 3, 4}.
Can we remove [1, 4]? No, because 2 is missing.
Can we remove [1, 1]? Yes (1 is present). Remaining: 3, 4.
Now remove [3, 4]? Yes (3 and 4 are present). Done. Total 2.
Is it just the number of contiguous segments of unique values?
Unique values sorted: 1, 3, 4. Gaps: (1,3) missing 2. (3,4) no gap.
Segments: {1}, {3, 4}. Count = 2.
Example 2: 3, 1, 4, 2, 4. Unique: 1, 2, 3, 4. Contiguous? Yes. Count = 1?
Sample output says sum is 23. Let's check $f(1,5)$ for Sample 2.
Values: 3, 1, 4, 2, 4. Unique: {1, 2, 3, 4}.
Can we remove [1, 4]? Yes, all 1,2,3,4 are present. 1 op.
So $f(1,5)=1$.
What about $f(1,4)$? Values 3, 1, 4, 2. Unique {1,2,3,4}. 1 op.
$f(2,4)$? Values 1, 4, 2. Unique {1,2,4}. Missing 3.
Segments: {1}, {2}, {4}? Or {1}, {2,4}? No, {2,4} is not contiguous (missing 3).
So segments: {1}, {2}, {4}. Count 3?
Let's trace: Remove [1,1] -> rem {2,4}. Remove [2,2] -> rem {4}. Remove [4,4] -> empty. Total 3.
Can we do better? Remove [1,2]? Missing 3. No.
So $f(2,4)=3$.
The pattern seems to be: $f(L,R)$ is the number of connected components of the set of unique values in $A[L..R]$ under the relation $x \sim y$ if $|x-y|=1$.
Basically, sort unique values $u_1 < u_2 < \dots < u_k$. Count $1 + \sum_{i=1}^{k-1} [u_{i+1} \neq u_i + 1]$.
This is equivalent to: Count how many $x$ in the unique set are such that $x-1$ is NOT in the unique set.
So $f(L,R) = \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)]$.
This simplifies the problem immensely. We need to compute $\sum_{L,R} \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)]$.
We can swap sums: $\sum_{x=1}^N \sum_{L,R} [x \in \text{Unique}(L,R) \land x-1 \notin \text{Unique}(L,R)]$.
Condition $x \in \text{Unique}(L,R)$ means $L \le \text{first\_pos}(x) \le \text{last\_pos}(x) \le R$? No, it means there is at least one occurrence of $x$ in $A[L..R]$.
Condition $x-1 \notin \text{Unique}(L,R)$ means there are NO occurrences of $x-1$ in $A[L..R]$.
Let $first(x)$ and $last(x)$ be the first and last indices of value $x$.
$x \in \text{Unique}(L,R) \iff L \le last(x) \text{ and } first(x) \le R$. (Actually, just existence: $\exists i \in [L,R], A_i=x$. This is equivalent to $L \le last(x)$ and $first(x) \le R$).
$x-1 \notin \text{Unique}(L,R) \iff$ no occurrence of $x-1$ in $[L,R]$.
Let $prev\_occ(x-1)$ be the largest index $< R$ where $x-1$ appears? No, we need the range $[L,R]$ to avoid $x-1$.
Let $P(x-1)$ be the set of positions of $x-1$. The condition is $[L,R] \cap P(x-1) = \emptyset$.
This means $R < \min(P(x-1) \cap [L, \infty))$ or $L > \max(P(x-1) \cap (-\infty, R])$.
Actually, simpler: For a fixed $x$, we sum over all pairs $(L,R)$ such that $x$ is present and $x-1$ is absent.
Total pairs $(L,R)$ where $x$ is present: $(last(x) - first(x) + 1) \times (last(x) - first(x) + 1)$? No.
Number of pairs $(L,R)$ containing at least one $x$:
Total pairs $N(N+1)/2$. Pairs NOT containing $x$: Sum of $(len)$ for gaps between occurrences.
Alternatively, count directly: $L \le last(x)$ and $R \ge first(x)$.
Number of such pairs: $last(x) \times (N - first(x) + 1)$.
Wait, $L$ can be anything from $1$ to $last(x)$, $R$ from $first(x)$ to $N$. But we need $L \le R$.
Intersection of $[1, last(x)] \times [first(x), N]$ with $L \le R$.
Since $first(x) \le last(x)$, the rectangle is valid.
Count = $\sum_{L=1}^{last(x)} \sum_{R=\max(L, first(x))}^{N} 1$.
If $L \le first(x)$, $R \in [first(x), N]$. Count $N - first(x) + 1$. (There are $first(x)$ such $L$'s).
If $L > first(x)$, $R \in [L, N]$. Count $(N - L + 1)$. (There are $last(x) - first(x)$ such $L$'s).
Total present = $first(x)(N - first(x) + 1) + \sum_{L=first(x)+1}^{last(x)} (N - L + 1)$.
Now subtract cases where $x-1$ is also present.
We need count where ($x$ present) AND ($x-1$ absent).
Let $S_x$ be the set of pairs $(L,R)$ where $x$ is present.
Let $S_{x-1}$ be the set of pairs where $x-1$ is present.
We want $|S_x \setminus S_{x-1}| = |S_x| - |S_x \cap S_{x-1}|$.
$S_x \cap S_{x-1}$ is pairs where BOTH $x$ and $x-1$ are present.
This requires $[L,R]$ to contain at least one $x$ and at least one $x-1$.
This is equivalent to: $L \le \min(\text{pos}(x), \text{pos}(x-1))$? No.
$L \le \max(\text{pos}(x) \text{ in range?})$.
Actually, $x$ present $\iff L \le last(x) \land R \ge first(x)$.
$x-1$ present $\iff L \le last(x-1) \land R \ge first(x-1)$.
Intersection: $L \le \min(last(x), last(x-1))$ and $R \ge \max(first(x), first(x-1))$.
Also need $L \le R$.
Let $L_{max} = \min(last(x), last(x-1))$ and $R_{min} = \max(first(x), first(x-1))$.
If $L_{max} < R_{min}$, intersection is empty (0).
Otherwise, count is same formula as above with $L_{max}, R_{min}$.
So algorithm:
1. Store first and last occurrence for each value $1..N$.
2. Initialize total = 0.
3. For each $x$ from 1 to $N$:
   a. Calculate $cnt\_x = $ count of $(L,R)$ where $x$ is present.
   b. If $x > 1$:
      Calculate $cnt\_both = $ count of $(L,R)$ where $x$ and $x-1$ are present.
      Add $cnt\_x - cnt\_both$ to total.
   c. If $x == 1$: Add $cnt\_x$ to total.
4. Print total.

Complexity: $O(N)$. Constraints $3 \times 10^5$, fits easily.