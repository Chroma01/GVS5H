The problem requires splitting an array into three non-empty contiguous subarrays to maximize the sum of distinct elements in each. A brute-force $O(N^2)$ approach checking all split points $(i, j)$ is too slow given $N \le 3 \times 10^5$. Instead, we can fix the middle split point $j$ and optimize the choice of $i$. For a fixed $j$, the right part's distinct count is constant. The left part's distinct count can be precomputed or queried efficiently. The optimal strategy involves iterating $j$ from $2$ to $N-1$, maintaining the distinct count of the prefix ending at $i$ (where $1 \le i < j$) and the distinct count of the suffix starting at $j+1$. To do this efficiently, we can precompute the distinct count for every possible prefix and suffix. Then, for each $j$, we need $\max_{1 \le i < j} (\text{distinct}(A[1..i])) + \text{distinct}(A[j+1..N])$. However, simply taking the global max prefix distinct count for a given $j$ isn't enough because the split $i$ must be strictly less than $j$. We can precompute an array `max_dist_prefix[k]` which stores $\max_{1 \le x \le k} (\text{distinct count of } A[1..x])$. Then for each $j$, the answer is `max_dist_prefix[j-1]` + `distinct(A[j+1..N])` + `distinct(A[j+1..N])`? No, the formula is `distinct(A[1..i])` + `distinct(A[i+1..j])` + `distinct(A[j+1..N])`.
Actually, a better approach: Iterate $j$ from $2$ to $N-1$. The term `distinct(A[j+1..N])` is fixed for a specific $j$. We need to maximize `distinct(A[1..i]) + distinct(A[i+1..j])` for $1 \le i < j$. This sub-problem is still tricky.
Alternative efficient approach:
1. Precompute `pref[k]` = distinct count in $A[1..k]$.
2. Precompute `suff[k]` = distinct count in $A[k..N]$.
3. Iterate $j$ from $2$ to $N-1$. The right part is fixed: `suff[j+1]`.
4. We need to maximize `distinct(A[1..i]) + distinct(A[i+1..j])` for $1 \le i < j$.
   Notice that `distinct(A[i+1..j])` = `pref[j] - pref[i]` is false because distinct counts don't subtract linearly.
   
Let's reconsider the structure. We want $\max_{1 \le i < j \le N-1} (D(1, i) + D(i+1, j) + D(j+1, N))$.
Fix $j$. We need $\max_{1 \le i < j} (D(1, i) + D(i+1, j))$.
$D(i+1, j)$ is the number of distinct elements in the range $[i+1, j]$.
This looks like we can iterate $j$ and maintain the best $i$.
Actually, there is a known optimization for this specific "3-partition distinct" problem.
We can iterate $j$ from $2$ to $N-1$.
For a fixed $j$, we want to maximize $D(1, i) + D(i+1, j)$.
Note that $D(i+1, j) \le D(1, j) - D(1, i)$ is not true.
However, observe that $D(1, i) + D(i+1, j) \le D(1, j) + (\text{something})$.
Wait, the maximum possible value for $D(1, i) + D(i+1, j)$ is bounded by $D(1, j)$ if the sets are disjoint, but they are subsets of $A[1..j]$.
Actually, the maximum sum of distinct counts for a split into two parts $[1, i]$ and $[i+1, j]$ is simply $D(1, j)$ if we could pick $i$ such that the sets are disjoint? No, the sets are contiguous.
Let's try a different angle.
Total distinct in $A[1..j]$ is $D(1, j)$.
$D(1, i) + D(i+1, j) = D(1, j) - (\text{elements in } 1..i \cap i+1..j \text{ counted twice?})$. No.
$D(1, i) + D(i+1, j) = |S_1| + |S_2|$. Since $S_1 \cup S_2 = S_{total}$, $|S_1| + |S_2| = |S_{total}| + |S_1 \cap S_2|$.
So we want to maximize $|S_1 \cap S_2|$. The intersection is the set of elements that appear in both $[1, i]$ and $[i+1, j]$.
An element $x$ contributes to the intersection if its last occurrence in $[1, j]$ is $\ge i+1$ and its first occurrence in $[1, j]$ is $\le i$.
Actually, simpler: For a fixed $j$, as we decrease $i$ from $j-1$ down to $1$, $D(1, i)$ decreases (or stays same) and $D(i+1, j)$ increases (or stays same).
We can precompute `pref[k]` = distinct count in $A[1..k]$.
We can precompute `suff[k]` = distinct count in $A[k..N]$.
Now, for each $j$, we need $\max_{1 \le i < j} (D(1, i) + D(i+1, j))$.
Let's define $f(j) = \max_{1 \le i < j} (D(1, i) + D(i+1, j))$.
Can we compute $f(j)$ efficiently?
Notice that $D(i+1, j) = D(1, j) - D(1, i) + \text{overlap}$. Not helpful.
Let's use the property that $N$ is up to $3 \cdot 10^5$. $O(N \log N)$ or $O(N)$ is needed.
We can iterate $j$ from $2$ to $N-1$.
Maintain a data structure or use a monotonic property?
Actually, consider the contribution of each element.
Let's flip the problem: Iterate the split point $i$ first? No, $j$ is the second split.
Let's try to compute $g[i] = D(1, i)$.
Then for a fixed $j$, we want $\max_{i < j} (g[i] + D(i+1, j))$.
$D(i+1, j)$ is the number of distinct elements in $A[i+1 \dots j]$.
This is equivalent to: count unique elements in $A[i+1 \dots j]$.
This looks like we can use a Segment Tree or similar.
For a fixed $j$, as $i$ decreases, the range $[i+1, j]$ grows.
$D(i+1, j)$ increases. $g[i]$ decreases.
We want to maximize the sum.
We can iterate $j$ from $2$ to $N-1$.
We need to query $\max_{1 \le i < j} (g[i] + \text{distinct}(i+1, j))$.
Let's maintain a segment tree over indices $1 \dots N$.
The value at index $i$ in the segment tree would represent $g[i] + \text{distinct}(i+1, j)$.
But $\text{distinct}(i+1, j)$ changes as $j$ changes.
When moving from $j$ to $j+1$:
The range $[i+1, j+1]$ includes $A[j+1]$.
If $A[j+1]$ is new in the range $[i+1, j+1]$, then $\text{distinct}(i+1, j+1) = \text{distinct}(i+1, j) + 1$.
If $A[j+1]$ was already present in $[i+1, j]$, the count doesn't change.
Specifically, let $last[x]$ be the last position of value $x$ seen so far (up to $j$).
When we move to $j+1$, for all $i$ such that $i+1 \le last[A[j+1]]$, the element $A[j+1]$ is already in $A[i+1 \dots j]$, so the distinct count doesn't increase.
For $i$ such that $i+1 > last[A[j+1]]$ (i.e., $i \ge last[A[j+1]]$), the element $A[j+1]$ is NOT in $A[i+1 \dots j]$, so adding $A[j+1]$ increases the distinct count by 1.
Wait, $last[A[j+1]]$ is the index of the previous occurrence.
Let $p = last[A[j+1]]$.
For any $i$ where the range $[i+1, j]$ does NOT contain $p$, i.e., $i+1 > p \implies i \ge p$, the new element $A[j+1]$ is distinct from everything in $[i+1, j]$. So distinct count increases by 1.
For $i < p$, the range $[i+1, j]$ includes $p$, so $A[j+1]$ is already counted. Distinct count stays same.
So, when moving from $j$ to $j+1$:
1. Update the "distinct count" term for the range of $i$'s.
   The term is $D(i+1, j)$.
   For $i \in [p, j-1]$, $D(i+1, j+1) = D(i+1, j) + 1$.
   For $i \in [1, p-1]$, $D(i+1, j+1) = D(i+1, j)$.
   Note: $i$ must be $< j+1$, so $i$ goes up to $j$. But we only care about $i < j+1$.
   Actually, we are building the solution for $j$ using data from $j-1$.
   Let's refine the iteration.
   We iterate $j$ from $2$ to $N-1$.
   We maintain a data structure that stores values $V_i = g[i] + D(i+1, j)$ for $1 \le i < j$.
   Initially for $j=2$: $i=1$. $V_1 = D(1,1) + D(2,2)$.
   Transition $j \to j+1$:
   We need to update $V_i$ for $1 \le i < j+1$.
   The new term is $D(i+1, j+1)$.
   Let $p = last\_pos[A[j+1]]$.
   If $p$ exists (i.e., $A[j+1]$ appeared before):
     For $i \ge p$: $D(i+1, j+1) = D(i+1, j) + 1$. So $V_i \leftarrow V_i + 1$.
     For $i < p$: $D(i+1, j+1) = D(i+1, j)$. So $V_i$ unchanged.
   If $p$ does not exist:
     For all $i < j+1$: $D(i+1, j+1) = D(i+1, j) + 1$. So $V_i \leftarrow V_i + 1$.
   Also, we need to add the new candidate $i = j$ (since now $i$ can be $j$ for the next step? No, for current $j$, $i$ goes up to $j-1$. For next step $j+1$, $i$ goes up to $j$. So we add $i=j$ with value $g[j] + D(j+1, j+1) = g[j] + 1$).
   
   Algorithm:
   1. Precompute `g[i]` = distinct count in $A[1..i]$ for all $i$.
   2. Precompute `suff[i]` = distinct count in $A[i..N]$ for all $i$.
   3. Initialize a Segment Tree (or Fenwick Tree if operations allow, but range add + range max requires SegTree) of size $N$.
      The tree will store $V_i = g[i] + D(i+1, j)$ for valid $i$.
      Initially $j=2$. Valid $i \in [1, 1]$.
      Compute $D(2, 2)$. Set $V_1 = g[1] + D(2, 2)$.
      Update SegTree at index 1 with $V_1$.
   4. Initialize `last_pos` map.
   5. Loop $j$ from $2$ to $N-1$:
      a. Current max for this $j$ is `query_max(1, j-1)` + `suff[j+1]`.
      b. Update for next $j+1$:
         Identify $p = last\_pos[A[j+1]]$.
         If $p$ exists:
           Range add $+1$ to indices $[p, j]$. (Note: $i$ can go up to $j$ for the next step).
           Wait, the range of $i$ we maintain is $1 \dots j$.
           For the current step $j$, we query $1 \dots j-1$.
           Then we prepare for $j+1$. The valid $i$'s will be $1 \dots j$.
           We need to update existing $i \in [1, j-1]$ and add new $i=j$.
           The update logic:
           For $i \in [p, j-1]$, $D(i+1, j+1) = D(i+1, j) + 1$. So add 1.
           For $i \in [1, p-1]$, no change.
           Also, we need to consider $i=j$ for the next step?
           Actually, the loop structure:
           Start with $j=2$.
           Query max over $i \in [1, 1]$.
           Then prepare for $j=3$.
           Update range $[p, 1]$? No, $i$ goes up to $j-1$.
           Let's trace carefully.
           State at start of loop body for $j$:
           SegTree contains $V_i = g[i] + D(i+1, j-1)$ for $1 \le i \le j-1$.
           Wait, if we define state at start of loop $j$ as having $V_i$ for $D(i+1, j-1)$, then we need to update to $D(i+1, j)$ before querying?
           Let's redefine:
           Before loop $j=2$:
           We need $V_i = g[i] + D(i+1, 2)$ for $i=1$.
           $D(2, 2) = 1$. $g[1] = D(1,1)$.
           So initialize SegTree with $V_1 = g[1] + 1$.
           Loop $j$ from $2$ to $N-1$:
             1. `ans = max(ans, query_max(1, j-1) + suff[j+1])`
             2. Prepare for $j+1$:
                We need to update $V_i$ to reflect $D(i+1, j)$.
                Current $V_i$ reflects $D(i+1, j-1)$.
                Let $p = last\_pos[A[j]]$.
                For $i \in [p, j-1]$, $D(i+1, j) = D(i+1, j-1) + 1$.
                For $i \in [1, p-1]$, $D(i+1, j) = D(i+1, j-1)$.
                So, range add $+1$ to $[p, j-1]$.
                Also, we need to add the new index $i=j$.
                $V_j = g[j] + D(j+1, j) = g[j] + 1$.
                Update point $j$ with $V_j$.
                Update `last_pos[A[j]] = j`.
   
   Complexity: $O(N \log N)$ due to segment tree operations.
   Constraints $N=3 \cdot 10^5$, this fits.