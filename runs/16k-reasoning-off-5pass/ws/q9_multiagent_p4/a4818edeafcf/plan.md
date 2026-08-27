To solve this problem efficiently within the constraints ($N \le 3 \times 10^5$), we need an $O(N)$ or $O(N \log N)$ approach. The strategy involves precomputing the number of distinct elements for all possible prefixes and suffixes. We can then iterate through all valid split points $i$ (the end of the first subarray). For each $i$, we fix the first part's distinct count. The second part ends at some $j > i$, and the third part starts at $j+1$. To maximize the sum, for a fixed $i$, we need to find a $j$ that maximizes (distinct in $A[i+1 \dots j]$ + distinct in $A[j+1 \dots N]$). We can precompute the distinct counts for all suffixes. Then, we iterate $i$ from $1$ to $N-2$. For the second part, we can use a sliding window or a two-pointer approach combined with a data structure (like a Fenwick tree or simply managing the active set) to efficiently query the maximum sum of the middle and right segments, or more simply, precompute the maximum value of (distinct in $A[k \dots N]$) for all $k$ and use a segment tree or similar structure to handle the dynamic middle segment. However, a simpler $O(N)$ approach exists: iterate $i$ from $1$ to $N-2$. As we move $i$, the first segment's distinct count is known. We need to maximize $distinct(i+1, j) + distinct(j+1, N)$. We can precompute an array `suff[k]` = distinct count of $A[k \dots N]$. Then we need $\max_{j} (distinct(i+1, j) + suff[j+1])$. We can maintain the distinct count of the current middle segment as we iterate $j$ for a fixed $i$, but doing this naively for every $i$ is $O(N^2)$. Instead, we can iterate $i$ and maintain the optimal $j$. Actually, a better approach is to iterate the split point between the first and second array ($i$) and the split point between the second and third ($j$). We can precompute `suff` array. Then we iterate $i$ from $1$ to $N-2$. We maintain a set of values for the current middle segment as we extend $j$. But we need the max over all $j$. Let's refine: Iterate $i$ from $1$ to $N-2$. We want $\max_{j \in [i+1, N-1]} (distinct(i+1, j) + suff[j+1])$. We can compute this by iterating $j$ from $i+1$ to $N-1$ and updating the distinct count of the middle segment. This is still $O(N^2)$.
Correct $O(N)$ approach:
1. Precompute `pref[x]`: distinct count in $A[1 \dots x]$.
2. Precompute `suff[x]`: distinct count in $A[x \dots N]$.
3. We need to maximize $distinct(1, i) + distinct(i+1, j) + distinct(j+1, N)$.
4. Iterate $i$ from $1$ to $N-2$. Let $d1 = distinct(1, i)$. We need $\max_{j} (distinct(i+1, j) + suff[j+1])$.
5. Notice that as $i$ increases, the range $[i+1, j]$ shrinks from the left. This suggests we can't easily reuse the middle distinct count calculation directly without a complex structure.
Alternative $O(N)$ logic:
Iterate the split point $i$ (end of first part). The first part is fixed.
We need to choose $j$ to maximize $distinct(i+1, j) + suff[j+1]$.
Let's reverse the thinking. Iterate $j$ from $2$ to $N-1$. The third part is fixed ($suff[j+1]$). We need $\max_{i < j} (distinct(1, i) + distinct(i+1, j))$.
The term $distinct(1, i) + distinct(i+1, j)$ is simply the number of distinct elements in $A[1 \dots j]$ MINUS the number of distinct elements that appear in BOTH $A[1 \dots i]$ and $A[i+1 \dots j]$.
This seems complicated.
Let's go back to the standard solution for this specific problem (AtCoder ABC 278 F / similar):
Precompute `suff` array.
Iterate $i$ from $1$ to $N-2$.
We need $\max_{j} (distinct(i+1, j) + suff[j+1])$.
We can maintain the distinct count of the middle segment as we iterate $j$. But we need the max over all $j$.
Actually, we can iterate $i$ and maintain the best $j$? No.
Let's try iterating $j$ (the end of the second part).
For a fixed $j$, we want $\max_{i < j} (distinct(1, i) + distinct(i+1, j)) + suff[j+1]$.
Let $f(j) = \max_{i < j} (distinct(1, i) + distinct(i+1, j))$.
$distinct(1, i) + distinct(i+1, j)$ is the count of distinct numbers in $A[1 \dots j]$ that appear in $A[1 \dots i]$ plus those that appear only in $A[i+1 \dots j]$.
Actually, $distinct(1, i) + distinct(i+1, j) = distinct(1, j) - (\text{count of numbers appearing in both parts})$.
This is hard to optimize directly.
Wait, there is a simpler observation.
$distinct(1, i) + distinct(i+1, j) = \text{count of distinct in } A[1 \dots j] \text{ where we count an element twice if it appears in both parts}$.
Let's reconsider the constraints and typical solutions.
We can precompute `suff`.
Then we iterate $i$ from $1$ to $N-2$.
We need $\max_{j \in [i+1, N-1]} (distinct(i+1, j) + suff[j+1])$.
We can compute this by iterating $j$ from $i+1$ to $N-1$ and maintaining the distinct count of $A[i+1 \dots j]$.
To make it $O(N)$, we can iterate $j$ from $2$ to $N-1$. As we increase $j$, the range $[i+1, j]$ changes.
Actually, we can iterate $i$ and maintain a data structure? No.
Let's try the other direction: Iterate $j$ from $2$ to $N-1$.
We want $\max_{i < j} (distinct(1, i) + distinct(i+1, j))$.
Let $g(i, j) = distinct(1, i) + distinct(i+1, j)$.
Notice that $g(i, j) = distinct(1, j) - (\text{number of distinct elements in } A[1 \dots j] \text{ that appear in both } A[1 \dots i] \text{ and } A[i+1 \dots j])$.
This doesn't seem to simplify easily.
Let's look at the structure again.
We can precompute `suff`.
Then we iterate $i$ from $1$ to $N-2$.
We need $\max_{j} (distinct(i+1, j) + suff[j+1])$.
We can maintain the distinct count of the middle segment as we slide $i$.
But the middle segment starts at $i+1$.
Let's define $h(j) = suff[j+1]$.
We need $\max_{j} (distinct(i+1, j) + h(j))$.
As $i$ increases, the start of the middle segment moves right.
We can maintain a set of values for the current $i$.
Actually, we can iterate $i$ and update the distinct counts of the middle segment for all $j \ge i+1$.
When moving from $i$ to $i+1$, the element $A[i]$ is removed from the consideration of the middle segment for all $j \ge i+1$.
We can use a Fenwick tree or Segment Tree to maintain the values $distinct(i+1, j) + suff[j+1]$ for all $j$.
Initially, for $i=0$ (conceptually, though $i \ge 1$), we have distinct counts for $A[1 \dots j]$.
When we move $i$ to $i+1$, we remove $A[i]$ from the distinct counts of all segments starting at or after $i+1$.
Specifically, for each $j \ge i+1$, if $A[i]$ was the last occurrence of that value in $A[1 \dots j]$, then removing $A[i]$ decreases the distinct count of $A[i+1 \dots j]$ by 1.
We can precompute the next occurrence of each number.
Let `next_occ[k]` be the index of the next occurrence of $A[k]$ after $k$.
When we move the left boundary of the middle segment from $i+1$ to $i+2$ (i.e., $i \to i+1$), we are effectively removing $A[i]$ from the set of elements in $A[i+1 \dots j]$ for all $j \ge i+1$.
The distinct count of $A[i+1 \dots j]$ decreases by 1 if and only if $A[i]$ does not appear again in $A[i+1 \dots j]$. That is, if $next\_occ[i] > j$.
So, for a fixed $i$, we want to maximize $distinct(i+1, j) + suff[j+1]$.
Let $val[j] = distinct(i+1, j) + suff[j+1]$.
When moving from $i$ to $i+1$, for all $j$ such that $next\_occ[i] > j$, $distinct(i+1, j)$ decreases by 1.
So $val[j]$ decreases by 1 for $j \in [i+1, next\_occ[i]-1]$.
We can maintain these values in a Segment Tree.
Algorithm:
1. Precompute `suff` array.
2. Precompute `next_occ` array for each position.
3. Initialize a Segment Tree of size $N$. The leaves represent $j$ from $2$ to $N-1$.
   Initially, for $i=1$, the middle segment is $A[2 \dots j]$.
   We can compute $distinct(2, j)$ for all $j$ initially using a simple pass.
   Set leaf $j$ to $distinct(2, j) + suff[j+1]$.
4. Iterate $i$ from $1$ to $N-2$.
   Current answer candidate: $distinct(1, i) + \max_{j \in [i+1, N-1]} (val[j])$.
   Update the Segment Tree: For $j$ in range $[i+1, next\_occ[i]-1]$, decrement the value by 1.
   (Note: if $next\_occ[i] \le i+1$, the range is empty, no update needed).
5. Keep track of the global maximum.

This is $O(N \log N)$.