
## ideation
The core difficulty lies in efficiently computing $f(L,R)$ for all pairs $(L,R)$ and summing them up. $N$ is up to $3 \times 10^5$, so an $O(N^2)$ solution is impossible.
The key insight is that $f(L,R)$ equals the number of connected components of the union of intervals $[first(v), last(v)]$ for all distinct values $v$ in $A[L..R]$.
We can iterate $R$ from 1 to $N$ and maintain the value of $f(L,R)$ for all $L \le R$.
When moving from $R-1$ to $R$:
1. Let $v = A[R]$.
2. If $v$ has appeared before at index $p = prev[R]$, the interval for $v$ extends from $[first(v), R-1]$ to $[first(v), R]$. This extension might merge the component containing $p$ with other components that overlap with the new range $[first(v), R]$. Specifically, any component whose interval ends at or after $first(v)$ and starts before $R$ (and is disjoint from the component containing $p$) will be merged.
3. If $v$ is new, it starts a new interval $[R, R]$. This adds 1 to the component count for all $L$ such that no existing interval covers $R$. Since existing intervals end at $\le R-1$, they never cover $R$ as an interior point, but they might end at $R-1$. However, the interval is $[first(v), last(v)]$. A new value $v$ at $R$ creates interval $[R,R]$. This interval is disjoint from all previous intervals $[first(u), last(u)]$ because $last(u) \le R-1 < R$. Thus, for all $L$, the number of components increases by 1.

The challenge is efficiently updating the counts for all $L$.
We can use a Segment Tree to maintain the values $f(L,R)$ for current $R$.
When $v$ is new:
- Increment $f(L,R)$ by 1 for all $L \in [1, R]$. This is a range add operation.

When $v$ appeared at $p$:
- The interval for $v$ becomes $[first(v), R]$.
- Previously, for a given $L$, if $L \le first(v)$, the interval was $[first(v), R-1]$. Now it is $[first(v), R]$.
- This extension might merge the component containing $first(v)$ with other components.
- Specifically, we need to identify which components are merged. The components are defined by the sorted list of disjoint intervals.
- A simpler way: The number of components is $K$. When we extend the interval of $v$ to $R$, we might merge the component containing $first(v)$ with any component that overlaps with $[first(v), R]$.
- Note that any component overlapping with $[first(v), R]$ must have an interval $[s, e]$ such that $s \le R$ and $e \ge first(v)$. Since we are at step $R$, all existing intervals end $\le R-1$. So the condition is $e \ge first(v)$.
- Also, the component containing $first(v)$ is the one that "owns" the value $v$ at $first(v)$.
- We can maintain the "rightmost end" of each component.
- Actually, a known technique for this problem is:
  $f(L,R) = (\text{number of distinct values in } A[L..R]) - (\text{number of merges})$.
  Alternatively, $f(L,R) = 1 + \sum_{i=L}^{R} \mathbb{I}(A[i] \text{ starts a new component})$.
  $A[i]$ starts a new component if it is the first occurrence of $A[i]$ in $A[L..i]$ AND it does not overlap with the previous component.
  
  Let's stick to the segment tree approach with "range add" and "range set" or "point update".
  
  Refined Algorithm:
  1. Precompute `prev[i]` for each $i$.
  2. Initialize a segment tree for range $[1, N]$ with zeros.
  3. Iterate $R$ from 1 to $N$:
     - Let $v = A[R]$.
     - If $v$ is new (no previous occurrence):
       - Add 1 to $f(L,R)$ for all $L \in [1, R]$. (Range Add +1 on $[1, R]$)
     - If $v$ occurred at $p = prev[R]$:
       - Let $first = first\_occurrence[v]$.
       - The interval for $v$ was $[first, R-1]$ (conceptually, for $L \le first$). Now it is $[first, R]$.
       - This extension might merge the component containing $first$ with other components.
       - Which components are merged? Those components that have an interval overlapping $[first, R]$.
       - Since all intervals end $\le R-1$, an interval $[s, e]$ overlaps $[first, R]$ iff $e \ge first$.
       - Also, we must ensure we don't double count or merge the same component twice.
       - The components are disjoint. The component containing $first$ is the one that includes $first$.
       - Any other component that overlaps $[first, R]$ must have $s < first$ (since if $s > first$, it would be disjoint from $first$'s component unless connected, but components are maximal disjoint sets). Wait, if $s > first$, it is to the right. If it overlaps $[first, R]$, then $s \le R$. But since components are disjoint, if it's to the right, it must start after the end of the component containing $first$.
       - Let $E$ be the end of the component containing $first$. Initially $E = R-1$ (from previous step). Now it becomes $R$.
       - Any component with start $s$ and end $e$ such that $s \le R$ and $e \ge first$ will merge? No.
       - The merge happens if the new interval $[first, R]$ overlaps with another interval $[s, e]$. Overlap means $\max(first, s) \le \min(R, e)$.
       - Since $e \le R-1$, this simplifies to $s \le R$ and $e \ge first$.
       - We need to find all such components and merge them into the component containing $first$.
       - Each merge reduces the total component count by 1.
       - We need to subtract 1 from $f(L,R)$ for all $L$ that are affected by this merge.
       - Which $L$ are affected? Those $L$ for which both the component containing $first$ and the other component are "active" in the subarray $A[L..R]$.
       - A component defined by interval $[s, e]$ is active for $L$ if $L \le s$. (Because the interval must start at or after $L$ to be part of the subarray? No, the interval is $[first(v), last(v)]$ within $A[L..R]$. If $L > first(v)$, the interval changes.
       
       This is getting complicated. Let's look at the standard solution for "Sum of f(L,R)".
       
       Standard Solution:
       $f(L,R)$ is the number of connected components.
       We can compute the contribution of each "merge" event.
       Or, we can maintain the answer directly.
       
       Let $ans[L]$ be $f(L,R)$.
       When $R$ increases:
       - If $A[R]$ is new: $ans[L] \leftarrow ans[L] + 1$ for all $L \le R$.
       - If $A[R]$ is old, at $p$:
         - The interval for $A[R]$ extends to $R$.
         - This may merge the component containing $first(A[R])$ with other components.
         - Let the components be $C_1, C_2, \dots$.
         - The component containing $first(A[R])$ is $C_k$.
         - We merge $C_k$ with any $C_j$ that overlaps with $[first(A[R]), R]$.
         - The number of merges is $M$.
         - For each merge, the total component count decreases by 1.
         - This decrease applies to all $L$ such that the merged components are both present in $A[L..R]$.
         - A component with interval $[s, e]$ is present if $L \le s$.
         - So, for a merge between $C_k$ (interval $[s_k, e_k]$) and $C_j$ (interval $[s_j, e_j]$), the decrease applies to $L \le \min(s_k, s_j)$.
         - We need to subtract 1 from $ans[L]$ for $L \in [1, \min(s_k, s_j)]$.
         
       So the algorithm is:
       1. Maintain a segment tree for range adds and range sums.
       2. Maintain a data structure to track components. Since components are intervals, we can use a set of disjoint intervals.
       3. For each $R$:
          - If $A[R]$ new: Range Add +1 on $[1, R]$. Add new interval $[R, R]$ to set.
          - If $A[R]$ old at $p$:
            - Let $s = first(A[R])$.
            - The interval for $A[R]$ was $[s, R-1]$. Now it is $[s, R]$.
            - Find all intervals in the set that overlap with $[s, R]$.
            - Merge them into one interval $[s, R]$.
            - For each merged interval (except the one containing $s$), let its interval be $[s_j, e_j]$.
            - The merge reduces the component count by 1 for all $L \le \min(s, s_j) = s_j$ (since $s_j > s$ usually? No, $s$ is the start of the component containing $s$. Other components might start before $s$? No, if they started before $s$ and overlapped, they would have been merged already. So other components must start after the end of the previous component containing $s$? No.
            - Actually, the components are disjoint. The component containing $s$ is $[S, E]$. We extend $E$ to $R$.
            - Any component $[s_j, e_j]$ with $s_j \le R$ and $e_j \ge S$ will merge.
            - Since components are disjoint and sorted, these are the components immediately to the right of $[S, E]$ that overlap $[S, R]$.
            - Let the merged components be $C_1, \dots, C_m$.
            - For each $C_i$ (except the one containing $s$), we subtract 1 from $ans[L]$ for $L \in [1, s_i]$.
            - Update the set of intervals.

       This seems feasible. $N=3 \times 10^5$. Using a `std::set` or similar to manage intervals, and a Segment Tree for the array $ans$.

## worker: Worker 1: Implement the logic to compute `prev[i]`
The problem asks for the sum of $f(L,R)$ over all subarrays. $f(L,R)$ is the number of connected components of the union of intervals $[first(v), last(v)]$ for all distinct values $v$ in $A[L..R]$.

We iterate $R$ from $0$ to $N-1$ and maintain the values $f(L,R)$ for all $L \le R$ in a Segment Tree.
1. **New Value**: If $A[R]$ is a new value, it starts a new interval $[R, R]$. This interval is disjoint from all previous intervals (which end $\le R-1$). Thus, it adds 1 to the component count for all $L \in [0, R]$. We perform a range add $+1$ on $[0, R]$ in the segment tree.
2. **Old Value**: If $A[R]$ is a value that last appeared at $p$, its interval extends from $[first(A[R]), R-1]$ to $[first(A[R]), R]$. Let $S = first(A[R])$. The component containing $S$ is extended to $R$. This extension may cause this component to overlap with other components to its right. Specifically, any component $[s_j, e_j]$ with $s_j \le R$ will overlap with $[S, R]$ (since $e_j \ge s_j > E_{prev} \ge S$ is not necessarily true, but $e_j \ge S$ is required for overlap with $[S, R]$? No. Overlap condition for $[S, R]$ and $[s_j, e_j]$ is $\max(S, s_j) \le \min(R, e_j)$. Since $s_j > E_{prev}$ and $E_{prev} \ge S$, we have $s_j > S$. So $\max(S, s_j) = s_j$. Condition becomes $s_j \le e_j$ (always true) and $s_j \le R$. So any component with $s_j \le R$ merges.
   When two components merge, the total component count decreases by 1. This decrease applies to all $L$ such that both components are present in $A[L..R]$ and their intervals overlap. As derived, this is $L \in [0, s_j]$. We perform a range add $-1$ on $[0, s_j]$ for each merged component.

The segment tree supports range add and range sum. The components are maintained in a sorted list. Merging involves finding the component containing $S$, identifying subsequent components that start $\le R$, and updating the segment tree and the component list.

Complexity: Each element is added once and merged at most once. The segment tree operations are $O(\log N)$. Total time $O(N \log N)$.
