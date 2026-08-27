The problem asks for the sum of the minimum operations to erase a subarray, where one operation removes all occurrences of a contiguous range of values $[l, r]$ present in the current set. This is equivalent to finding the minimum number of colors needed to color the subarray such that no two adjacent elements have the same color, but with a twist: we can remove a range $[l, r]$ if all values in that range appear in the current set. Actually, a simpler interpretation is that $f(L,R)$ is the size of the minimum path cover or related to the chromatic number of a specific graph. However, looking at the operation: we pick a value range $[l, r]$ and remove all instances of values $v \in [l, r]$ currently on the board. This is exactly the problem of finding the minimum number of steps to clear the array where in one step we can remove all occurrences of a set of values forming an interval. This is known to be equal to the maximum number of disjoint intervals of values that can be formed? No.

Let's re-evaluate based on Sample 1: `1 3 1 4`.
Subarray `1 3 1 4`. Values present: $\{1, 3, 4\}$.
Op 1: Pick range $[1, 1]$. Removes all $1$s. Board: `3 4`.
Op 2: Pick range $[3, 4]$. Removes all $3, 4$. Board: empty. Total 2.
Notice that the values removed in step 1 were $\{1\}$, step 2 were $\{3, 4\}$. These sets are disjoint and their union is $\{1, 3, 4\}$. The key constraint is that the chosen sets of values must be intervals of integers.
So $f(L,R)$ is the minimum number of intervals needed to cover the set of unique values present in $A[L \dots R]$, such that the intervals are disjoint? No, the operation removes *all* occurrences. So if we pick interval $[l, r]$, we remove every instance of any value $v \in [l, r]$ currently on the board.
This means we are partitioning the set of unique values $U = \{A_i \mid L \le i \le R\}$ into the minimum number of contiguous integer intervals $I_1, I_2, \dots, I_k$ such that $\bigcup I_j = U$.
Wait, is it just the number of connected components of the set $U$ under the adjacency relation $x \sim x+1$?
In Sample 1, $U=\{1, 3, 4\}$. Components: $\{1\}$ and $\{3, 4\}$. Count = 2. Correct.
Sample 2: `3 1 4 2 4`.
Subarray `3 1 4 2 4`. $U=\{1, 2, 3, 4\}$. Connected: $\{1, 2, 3, 4\}$. Count = 1?
Let's check the sample output logic. The sample output says total sum is 23.
If $f(L,R)$ is just the number of connected components of unique values, let's calculate for Sample 2 manually.
Array: 3, 1, 4, 2, 4.
(1,1): {3} -> 1
(1,2): {3,1} -> {1,3} (gap 2) -> 2
(1,3): {3,1,4} -> {1,3,4} (gap 2) -> 2 ({1}, {3,4})
(1,4): {3,1,4,2} -> {1,2,3,4} -> 1
(1,5): {3,1,4,2} -> 1
(2,2): {1} -> 1
(2,3): {1,4} -> 2
(2,4): {1,4,2} -> {1,2,4} -> 2 ({1,2}, {4})
(2,5): {1,4,2} -> 2
(3,3): {4} -> 1
(3,4): {4,2} -> 2
(3,5): {4,2} -> 2
(4,4): {2} -> 1
(4,5): {2,4} -> 2
(5,5): {4} -> 1
Sum: 1+2+2+1+1 + 1+2+2+2 + 1+2+2 + 1+2 + 1 = 23.
Matches Sample 2 perfectly.
So the problem reduces to: For each subarray, count the number of connected components of its unique values, where connectivity is defined by $x \sim x+1$.
The number of components is $|U| - (\text{number of pairs } (x, x+1) \text{ such that } x, x+1 \in U)$.
Alternatively, it is $1 + \sum_{x \in U} [x-1 \notin U]$. Or simply, iterate through sorted unique values and count gaps.
Since we need the sum over all $L, R$, we can use a contribution technique or a sliding window / two pointers approach with a data structure.
Specifically, $f(L,R) = \text{count of unique values in } A[L..R] - \text{count of pairs } (v, v+1) \text{ both present in } A[L..R]$.
Wait, if $U = \{1, 3, 4\}$, unique count = 3. Pairs $(v, v+1)$ in $U$: $(3,4)$. Count = 1. Result $3-1=2$. Correct.
If $U = \{1, 2, 4\}$, unique count = 3. Pairs: $(1,2)$. Count = 1. Result $3-1=2$. Correct.
So $f(L,R) = \text{Unique}(L,R) - \text{Pairs}(L,R)$.
We need $\sum_{L,R} (\text{Unique}(L,R) - \text{Pairs}(L,R))$.
This splits into two independent problems:
1. Sum of number of unique elements in all subarrays.
2. Sum of number of pairs $(v, v+1)$ present in all subarrays.

Both can be solved efficiently.
For unique elements: Standard technique. For each element $A_i$, count how many subarrays $A[L..R]$ include $A_i$ and where $A_i$ is the *first* occurrence of its value in that subarray (or last, etc.).
Actually, simpler: For a fixed value $v$, let its positions be $p_1, p_2, \dots, p_k$. A subarray $A[L..R]$ contains $v$ if $L \le p_j \le R$ for some $j$. The number of subarrays containing at least one $v$ is total subarrays - subarrays with no $v$.
Subarrays with no $v$ are those strictly between occurrences.
Sum of unique = $\sum_{v} (\text{count of subarrays containing } v)$.
Count of subarrays containing $v$: Let positions of $v$ be $pos_1, pos_2, \dots, pos_k$.
Subarrays NOT containing $v$ are those in intervals $(pos_i, pos_{i+1})$ (exclusive). Length $len = pos_{i+1} - pos_i - 1$. Number of subarrays in this gap is $len(len+1)/2$. Also before $pos_1$ and after $pos_k$.
Total subarrays $N(N+1)/2$. Subtract gaps.
This is $O(N)$ or $O(N \log N)$.

For pairs $(v, v+1)$: We need to count how many subarrays contain both $v$ and $v+1$.
For a specific pair $(v, v+1)$, let positions of $v$ be $P_v$ and $P_{v+1}$.
A subarray contains both if $L \le \max(pos_v, pos_{v+1})$ and $R \ge \min(pos_v, pos_{v+1})$? No.
It must contain at least one $v$ AND at least one $v+1$.
This is equivalent to: Total subarrays - (subarrays with no $v$) - (subarrays with no $v+1$) + (subarrays with neither $v$ nor $v+1$).
This can be computed for each pair $(v, v+1)$. Since $v$ ranges $1 \dots N-1$, and we have $N$ elements, the number of pairs is $O(N)$. We can iterate $v$ from $1$ to $N-1$.
For a fixed $v$, we have lists of positions for $v$ and $v+1$. We need to count pairs of indices $(i, j)$ such that a subarray covers $pos_v[i]$ and $pos_{v+1}[j]$.
Actually, the condition "subarray contains at least one $v$ and at least one $v+1$" is easier:
For a fixed $v$, consider the combined sequence of positions of $v$ and $v+1$. Sort them.
Let the sorted positions be $q_1, q_2, \dots, q_m$.
A subarray $[L, R]$ contains both if it covers at least one $v$ and at least one $v+1$.
This is equivalent to: The subarray must NOT be entirely in a gap between a $v$ and a $v+1$? No.
It's easier to use the inclusion-exclusion principle per pair $(v, v+1)$:
Count = Total - (no $v$) - (no $v+1$) + (no $v$ and no $v+1$).
"No $v$" is calculated by gaps in $P_v$.
"No $v+1$" is calculated by gaps in $P_{v+1}$.
"No $v$ and no $v+1$" is calculated by gaps in the union of positions $P_v \cup P_{v+1}$.
Since we do this for each $v$, and the sum of sizes of $P_v$ and $P_{v+1}$ over all $v$ is $O(N)$, the total complexity will be linear.

Algorithm:
1. Read input, store positions for each value $1 \dots N$.
2. Calculate `SumUnique`:
   For each value $v$, calculate number of subarrays containing $v$.
   Sum these up.
3. Calculate `SumPairs`:
   For each $v$ from $1$ to $N-1$:
     Get positions $P_v$ and $P_{v+1}$.
     Calculate subarrays with no $v$ (using gaps in $P_v$).
     Calculate subarrays with no $v+1$ (using gaps in $P_{v+1}$).
     Calculate subarrays with neither (using gaps in sorted union of $P_v \cup P_{v+1}$).
     Add (Total - no_v - no_vplus1 + neither) to `SumPairs`.
4. Result = `SumUnique` - `SumPairs`.

Complexity: $O(N)$ time and space.