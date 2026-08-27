The problem asks for the minimum operations to empty the array using swaps and prefix deletions of identical values. The key insight is that a prefix deletion operation can remove a block of identical numbers only if they are contiguous at the start. Swaps allow us to reorder elements, but since we want to minimize operations, we should think about grouping identical numbers together. Specifically, if we have $k$ occurrences of a number $x$, we can potentially delete them in one go if we move them all to the front. However, the constraint is that we can only delete a prefix. This suggests a dynamic programming approach or a greedy strategy based on the positions of identical elements. Actually, the optimal strategy involves realizing that we can treat the array as a sequence of blocks. If we decide to delete a specific value $x$, we must bring all instances of $x$ to the front. The cost to bring $x$ to the front is related to the number of other elements we need to swap past. But wait, we can interleave deletions. Let's reconsider: The operation "delete prefix of identical values" is powerful. If we have a sequence like `1 2 1 2`, we can swap to get `1 1 2 2`, then delete `1 1` (cost 1), then delete `2 2` (cost 1), total 3 ops (2 swaps + 2 deletes? No, swaps count as ops).
Actually, let's look at the sample cases.
Sample 1: `1 1 2 1 2`. Answer 3.
Strategy: Swap (3rd, 4th) -> `1 1 1 2 2` (1 op). Delete `1 1 1` (1 op). Delete `2 2` (1 op). Total 3.
Sample 2: `4 2 1 3`. Answer 4.
Strategy: Delete `4` (1), `2` (1), `1` (1), `3` (1). Total 4. Swapping doesn't help here because they are all distinct.
Sample 3: `1 2 1 2 1 2 1 2 1 2 1`. Answer 8.
Here we have six `1`s and five `2`s. Total 11 elements.
If we group all `1`s: `1 1 1 1 1 1 2 2 2 2 2`. Delete `1`s (1 op), delete `2`s (1 op). Total 2 ops? No, we need swaps.
To move the first `2` past the first `1`? No, we want to group `1`s.
Original: `1 2 1 2 1 2 1 2 1 2 1`.
We need to move the `2`s to the right of the `1`s.
There are 5 `2`s. Each `2` is currently at index 2, 4, 6, 8, 10 (1-based).
To group all `1`s at the start, we need to swap every `2` past every `1` that is to its right? No, we just need to move all `2`s to the right of all `1`s.
Number of inversions between `1` and `2`?
Positions of `1`: 1, 3, 5, 7, 9, 11.
Positions of `2`: 2, 4, 6, 8, 10.
Every `2` is to the right of some `1`s, but some `1`s are to the right of `2`s.
Specifically, `2` at pos 2 is after `1` at pos 1. `2` at pos 4 is after `1` at pos 3.
Actually, the pattern is alternating. To group all `1`s, we need to swap each `2` with the `1` immediately to its left?
Let's trace the sample 1 logic again. `1 1 2 1 2`.
We swapped `2` (at 3) and `1` (at 4). This moved the `1` to the left of the `2`.
The goal is to form a prefix of identical elements.
If we have $N$ elements, and we decide to delete value $x$ first, we must move all $x$'s to the front. The number of swaps required is the number of non-$x$ elements that are currently before the last $x$? No.
The number of swaps to move a set of elements to the front is equal to the number of elements that are NOT in that set and are currently before the target position?
Actually, the minimum number of swaps to make all instances of value $x$ contiguous at the beginning is equal to the number of elements that are NOT $x$ and appear before the last instance of $x$? No.
It is simply the number of non-$x$ elements that are currently to the left of the rightmost $x$? No.
Consider `1 2 1`. To make `1 1 2`, we swap `2` and `1`. 1 swap. The non-`1` element is at index 2. It is before the last `1` (index 3).
Consider `1 2 3 1`. To make `1 1 2 3`, we need to move the last `1` to the front. It passes `3` and `2`. 2 swaps.
Generally, to gather all $x$'s to the front, the cost is the number of non-$x$ elements that are to the left of the rightmost $x$? No, that's not right either.
The cost to gather all $x$'s to the front is the number of non-$x$ elements that are to the left of the *last* $x$?
Wait, if we have `1 2 3 1`, the non-1s are 2, 3. Both are to the left of the last 1. Cost = 2.
If we have `1 1 2`, non-1s to left of last 1: 0. Cost 0.
If we have `2 1 1`, non-1s to left of last 1: 1 (the 2). Cost 1.
So the cost to gather all $x$'s to the front is the count of non-$x$ elements appearing before the last occurrence of $x$.
BUT, we can perform deletions in between.
In Sample 1: `1 1 2 1 2`.
If we just gather `1`s: Last `1` is at index 4. Non-1s before it: `2` at index 3. Count = 1.
After gathering `1`s: `1 1 1 2 2`. Delete `1`s (1 op). Remaining `2 2`. Delete `2`s (1 op). Total = 1 (swap) + 1 + 1 = 3.
What if we gather `2`s? Last `2` is at index 5. Non-2s before it: `1, 1, 1`. Count = 3.
Total = 3 (swap) + 1 (delete 2s) + 1 (delete 1s) = 5. Worse.
Is it possible to do better by interleaving?
Suppose we delete some prefix, then swap, then delete?
The sample explanation says: Swap (3,4) -> `1 1 1 2 2`. Then delete `1`s, then `2`s.
This implies the strategy is: Choose a permutation of distinct values present in the array, say $v_1, v_2, \dots, v_k$.
For each $v_i$, we move all instances of $v_i$ to the front of the current array (which consists of remaining elements), then delete them.
The cost to move all $v_i$ to the front of the current array is the number of elements currently in the array that are NOT $v_i$.
Wait, if the array is $S$, and we want to move all $x \in S$ to the front. The number of swaps is $|S| - (\text{count of } x \text{ in } S)$.
Because every non-$x$ element must be swapped past the $x$'s to get them to the right?
Actually, to move all $x$'s to the front, we just need to swap every non-$x$ element that is currently to the left of some $x$?
No. Consider `1 2 1`. To get `1 1 2`.
We swap `2` and `1`. `2` moves right, `1` moves left.
The number of swaps is exactly the number of non-$x$ elements that are to the left of the *rightmost* $x$?
Let's re-evaluate `1 2 1`. Non-1s before last 1: `2`. Count 1. Correct.
`1 2 3 1`. Non-1s before last 1: `2, 3`. Count 2. Correct.
`2 1 1`. Non-1s before last 1: `2`. Count 1. Correct.
So the cost to gather $x$ is the number of non-$x$ elements before the last $x$.
BUT, this assumes we do it on the original array.
If we delete some elements first, the "last $x$" might change relative to the remaining elements?
Actually, the relative order of remaining elements is preserved.
If we decide to delete values in order $v_1, v_2, \dots, v_k$.
Step 1: Gather all $v_1$ to front. Cost = (number of elements in original array that are not $v_1$ and appear before the last $v_1$).
Wait, if we delete $v_1$ immediately after gathering, we remove all $v_1$'s.
Then we gather $v_2$. The cost is the number of elements remaining (which are not $v_1$) that are not $v_2$ and appear before the last $v_2$ (in the original array, considering only non-$v_1$ elements).
This looks like we are calculating the number of inversions or something similar.
Let's formalize.
Let the distinct values be $u_1, u_2, \dots, u_m$.
We choose an ordering of these values.
For the first value $u_{p_1}$, we pay $C_1 = $ count of elements in $A$ that are not $u_{p_1}$ and appear before the last occurrence of $u_{p_1}$.
Then we remove all $u_{p_1}$.
For the second value $u_{p_2}$, we pay $C_2 = $ count of elements in $A \setminus \{u_{p_1}\}$ that are not $u_{p_2}$ and appear before the last occurrence of $u_{p_2}$ (in the original array).
And so on.
Total cost = $\sum C_i + m$ (since each gathering is followed by 1 delete op).
Wait, is the cost simply the number of non-target elements before the last target?
Let's check Sample 1: `1 1 2 1 2`.
Order `1`, then `2`.
1. Target `1`. Last `1` is at index 4. Elements before index 4: `1, 1, 2`. Non-1s: `2`. Count = 1.
   Remove `1`s. Remaining: `2, 2`.
2. Target `2`. Last `2` is at index 2 (in original, but now it's the only element).
   Wait, in the remaining array `2, 2`, the last `2` is at index 2. Elements before it: `2`. Non-2s: 0. Count = 0.
   Total swaps = 1 + 0 = 1.
   Total deletes = 2.
   Total ops = 3. Matches sample.

Order `2`, then `1`.
1. Target `2`. Last `2` is at index 5. Elements before: `1, 1, 2, 1`. Non-2s: `1, 1, 1`. Count = 3.
   Remove `2`s. Remaining: `1, 1, 1`.
2. Target `1`. Last `1` is at index 3. Elements before: `1, 1`. Non-1s: 0. Count = 0.
   Total swaps = 3.
   Total ops = 3 + 2 = 5.

So the strategy is: Find a permutation of distinct values to minimize the sum of costs.
Cost for value $v$ given a set of already removed values $R$:
Count elements $x$ in $A$ such that $x \notin R$, $x \neq v$, and $x$ appears before the last occurrence of $v$.
This is equivalent to: (Total elements before last $v$) - (Count of $v$ before last $v$) - (Count of $R$ before last $v$).
Actually, simpler:
Let $L_v$ be the index of the last occurrence of $v$.
Let $Pre(i)$ be the number of elements in $A[1 \dots i]$ that are not $v$.
The cost to gather $v$ (assuming $R$ are already removed) is the number of elements in $A[1 \dots L_v]$ that are not $v$ AND not in $R$.
Let $TotalNonV(L_v)$ be the count of elements in $A[1 \dots L_v]$ that are not $v$.
Let $CountR(L_v)$ be the count of elements in $A[1 \dots L_v]$ that are in $R$.
Cost = $TotalNonV(L_v) - CountR(L_v)$.
Note that $TotalNonV(L_v) = L_v - (\text{count of } v \text{ in } A[1 \dots L_v])$.
Since $L_v$ is the last occurrence, all $v$'s are in $A[1 \dots L_v]$.
So $TotalNonV(L_v) = L_v - (\text{total count of } v)$.
Let $cnt[v]$ be the total count of $v$.
Cost($v, R$) = $L_v - cnt[v] - CountR(L_v)$.
We want to minimize $\sum_{v} (L_v - cnt[v] - CountR(L_v)) + m$.
The term $\sum (L_v - cnt[v])$ is constant regardless of order.
We need to maximize $\sum_{v} CountR(L_v)$.
$CountR(L_v)$ is the number of elements in $R$ that appear before $L_v$.
So we want to order the values $v$ such that if $u$ comes before $v$ in our deletion order, we gain points?
Wait, $R$ grows.
Let the order be $p_1, p_2, \dots, p_m$.
For $p_1$: $R = \emptyset$. Gain = 0.
For $p_2$: $R = \{p_1\}$. Gain = count of $p_1$ before $L_{p_2}$.
For $p_3$: $R = \{p_1, p_2\}$. Gain = count of $p_1, p_2$ before $L_{p_3}$.
...
Total Gain = $\sum_{i=2}^m \sum_{j=1}^{i-1} (\text{count of } p_j \text{ before } L_{p_i})$.
This is equivalent to: For every pair of distinct values $(u, v)$, if $u$ is deleted before $v$, we add (count of $u$ before $L_v$) to the gain.
We want to maximize this sum.
This is a classic "minimize/maximize by sorting" problem.
Consider two adjacent values in the optimal order, $u$ and $v$.
Suppose we have a sequence $\dots, u, v, \dots$.
Contribution from pair $(u, v)$: $u$ is before $v$, so we add $Count(u \text{ before } L_v)$.
Contribution from pair $(v, u)$: $v$ is before $u$, so we add $Count(v \text{ before } L_u)$.
All other pairs involving other elements $w$ contribute the same regardless of whether $u$ is before $v$ or $v$ before $u$ (since $w$ is either before both, after both, or the interaction with $u$ vs $v$ is independent of the relative order of $u, v$? No).
Let's check.
If $w$ is before both $L_u$ and $L_v$:
Order $u, v$: $w$ contributes to $u$'s cost (no gain), $w$ contributes to $v$'s cost (gain 1).
Order $v, u$: $w$ contributes to $v$'s cost (no gain), $w$ contributes to $u$'s cost (gain 1).
Same.
If $w$ is after both:
No contribution to gain.
If $w$ is between $L_u$ and $L_v$ (assume $L_u < L_w < L_v$):
Order $u, v$: $w$ is after $L_u$ (no gain for $u$), $w$ is before $L_v$ (gain 1 for $v$). Total gain 1.
Order $v, u$: $w$ is after $L_v$ (no gain for $v$), $w$ is after $L_u$ (no gain for $u$). Total gain 0.
Wait, the condition is "count of $w$ before $L_{target}$".
If $w$ is before $L_v$, it adds to the gain when $v$ is processed (if $w \in R$).
So if $L_u < L_w < L_v$:
Order $u, v$: $u$ processed first. $w$ not in $R$. No gain from $w$ for $u$.
Then $v$ processed. $u \in R$. $w \notin R$. Gain from $u$? Yes, if $u$ is before $L_v$.
Gain from $w$? No, $w$ not in $R$.
Wait, the gain is $\sum_{j < i} Count(p_j \text{ before } L_{p_i})$.
So for pair $(u, v)$:
If $u$ before $v$: Gain += $Count(u \text{ before } L_v)$.
If $v$ before $u$: Gain += $Count(v \text{ before } L_u)$.
Other elements $w$ don't affect the comparison between $u$ and $v$ directly, except that their positions determine if they are counted in the "before" checks? No, the check is specifically for $u$ and $v$.
So we just compare $Count(u \text{ before } L_v)$ vs $Count(v \text{ before } L_u)$.
We should place $u$ before $v$ if $Count(u \text{ before } L_v) > Count(v \text{ before } L_u)$.
This defines a strict weak ordering (or similar).
Let's verify transitivity.
Define $u \prec v$ if $Count(u \text{ before } L_v) > Count(v \text{ before } L_u)$.
Is this transitive?
$Count(u \text{ before } L_v) = \sum_{k=1}^{L_v} [A_k \neq v \land A_k = u]$.
Actually, simpler: $Count(u \text{ before } L_v)$ is the number of $u$'s that appear before the last $v$.
Let $last[u]$ be the index of the last occurrence of $u$.
We sort the distinct values based on this criterion.
Then calculate the total cost.

Algorithm:
1. Identify all distinct values present in $A$.
2. For each distinct value $v$, find $last[v]$ (last index) and $cnt[v]$ (total count).
3. Define a comparison function for two values $u, v$:
   $score(u, v) = (\text{number of } u \text{'s before } last[v]) - (\text{number of } v \text{'s before } last[u])$.
   If $score(u, v) > 0$, $u$ should come before $v$.
   Note: "number of $u$'s before $last[v]$" is simply the count of $u$ in $A[1 \dots last[v]-1]$.
   Since we know the total count of $u$, this is $cnt[u] - (\text{number of } u \text{'s after } last[v])$. But $last[v]$ is the last $v$, so any $u$ after $last[v]$ is just after.
   Actually, we can precompute prefix sums or just iterate. Since $N$ is up to $2 \cdot 10^5$, $O(N \log N)$ or $O(N)$ is needed.
   We can compute for each $v$, the number of $u$'s before $last[v]$ efficiently?
   Actually, we can just store the positions of each number.
   For each $v$, $last[v]$ is known.
   For each pair $(u, v)$, we need $count(u, 1, last[v]-1)$.
   This can be done by storing a list of positions for each number and using binary search (bisect_right) to find how many are $< last[v]$.
   Or, since we need to sort all distinct values, we can define a key.
   Is the relation transitive?
   Let's assume it is (it's a standard result for this type of problem).
   We can use `sort_with_key` in Python. But Python's sort is stable and requires a key.
   We can define a custom comparator using `functools.cmp_to_key`.
   Comparison of $u$ and $v$:
   $c_u = \text{count of } u \text{ before } last[v]$
   $c_v = \text{count of } v \text{ before } last[u]$
   If $c_u > c_v$, $u < v$ (u comes first).
   If $c_u < c_v$, $u > v$.
   If equal, order doesn't matter.
4. Sort the distinct values.
5. Calculate the total cost:
   Base cost = $\sum (last[v] - cnt[v]) + m$.
   Subtract the gain: $\sum_{i=2}^m \sum_{j=1}^{i-1} (\text{count of } p_j \text{ before } last[p_i])$.
   Alternatively, calculate cost directly in the sorted order:
   Initialize `current_removed_count` array (or just a set).
   For each $v$ in sorted order:
     Cost += (number of elements in $A[1 \dots last[v]]$ that are not $v$ and not yet removed).
     Mark $v$ as removed.
   This simulation is $O(m \cdot N)$ which is too slow if $m$ is large.
   We need a faster way to calculate the sum.
   Total Cost = $\sum_{v} (last[v] - cnt[v]) + m - \sum_{v} (\text{count of previously removed elements before } last[v])$.
   Let $G = \sum_{v} (\text{count of previously removed elements before } last[v])$.
   We can compute $G$ efficiently.
   Iterate $v$ in sorted order.
   For each $v$, we need the number of already processed elements $u$ such that $last[u] < last[v]$? No.
   We need the number of occurrences of $u$ in $A[1 \dots last[v]]$.
   Let $pos[u]$ be the list of positions of $u$.
   For a fixed $v$, and a set of processed $u$'s, we need $\sum_{u \in Processed} (\text{count of } u \text{ in } A[1 \dots last[v]])$.
   This is $\sum_{u \in Processed} (\text{bisect\_right}(pos[u], last[v]) - \text{bisect\_left}(pos[u], last[v]))$.
   Since we process in order, we can maintain a data structure?
   Actually, notice that $\sum_{u \in Processed} (\text{count of } u \text{ in } A[1 \dots last[v]]) = \sum_{u \in Processed} (\text{total count of } u \text{ before } last[v])$.
   This looks like we can just accumulate.
   Wait, the total number of operations is $\sum (last[v] - cnt[v]) + m - G$.
   $G = \sum_{v} \sum_{u \prec v} (\text{count of } u \text{ before } last[v])$.
   This is exactly the sum we wanted to maximize.
   Can we compute $G$ in $O(m \log m)$ or $O(m \log N)$?
   Yes.
   We have pairs $(u, last[u])$ and $(v, last[v])$.
   For each $v$, we want $\sum_{u \prec v} (\text{count of } u \text{ before } last[v])$.
   Let $f(u, x) = \text{count of } u \text{ in } A[1 \dots x]$.
   We need $\sum_{u \prec v} f(u, last[v])$.
   This is hard because $f(u, x)$ depends on $u$.
   However, note that $f(u, last[v]) = \text{total count of } u - (\text{count of } u \text{ after } last[v])$.
   Count of $u$ after $last[v]$ is easy if we know the positions.
   But the sum is over $u \prec v$.
   Maybe we can rewrite the total cost?
   Total Cost = $\sum_{v} (last[v] - cnt[v]) + m - \sum_{v} \sum_{u \prec v} f(u, last[v])$.
   Let's swap sums?
   $\sum_{v} \sum_{u \prec v} f(u, last[v]) = \sum_{u} \sum_{v \succ u} f(u, last[v])$.
   For a fixed $u$, we sum $f(u, last[v])$ for all $v$ that come after $u$ in the sorted order.
   $f(u, last[v])$ is the number of $u$'s before $last[v]$.
   This is $\min(cnt[u], \text{number of } u \text{ before } last[v])$. Actually just the count.
   This still seems $O(m^2)$ if we do it naively.
   But $m \le N$. $O(N^2)$ is too slow.
   We need a linear or log-linear approach.
   
   Alternative view:
   The cost to gather $v$ is $last[v] - cnt[v] - (\text{count of removed elements before } last[v])$.
   Sum of costs = $\sum (last[v] - cnt[v]) + m - \sum_{v} (\text{count of removed elements before } last[v])$.
   Let $S$ be the set of removed elements.
   Term to maximize: $\sum_{v} \sum_{u \in S, u \prec v} f(u, last[v])$.
   Wait, $f(u, last[v])$ is the number of $u$'s in $A[1 \dots last[v]]$.
   Let's consider the contribution of each position $i$ in $A$.
   Suppose $A[i] = x$.
   This element $x$ at $i$ contributes to the "count of removed elements before $last[v]$" if $i < last[v]$ and $x$ is removed before $v$.
   So, for each position $i$, let $x = A[i]$.
   This $x$ contributes 1 to the gain for every $v$ such that:
   1. $last[v] > i$.
   2. $x$ is removed before $v$.
   So Gain = $\sum_{i=1}^N \sum_{v: last[v] > i, \text{order}(x) < \text{order}(v)} 1$.
   Here $\text{order}(x)$ is the rank of value $x$ in our sorted deletion order.
   We want to maximize this sum.
   Let's fix the order.
   For a fixed $i$ with value $x$, we gain 1 for each $v$ such that $last[v] > i$ and $v$ comes after $x$.
   Let $S_i = \{ v \mid last[v] > i \}$.
   We want to choose an ordering of values to maximize $\sum_{i} \sum_{v \in S_i} [v \text{ after } x]$.
   This looks like we can determine the order greedily.
   Consider two values $u, v$.
   Suppose we swap their relative order. How does the total gain change?
   The gain change is due to pairs $(i, u)$ and $(i, v)$.
   Actually, let's look at the condition $last[v] > i$.
   Let $C_u = \{ i \mid A[i] = u \}$.
   The term for $u$ is $\sum_{i \in C_u} \sum_{v: last[v] > i} [v \text{ after } u]$.
   If we swap $u$ and $v$:
   Old gain part involving $u, v$:
   For $i \in C_u$: if $last[v] > i$, we get 1 (since $v$ after $u$).
   For $i \in C_v$: if $last[u] > i$, we get 1 (since $u$ after $v$).
   New gain part (swapped):
   For $i \in C_u$: if $last[v] > i$, we get 0 (since $v$ before $u$).
   For $i \in C_v$: if $last[u] > i$, we get 1 (since $u$ after $v$).
   Wait, the condition is $v$ after $u$.
   Old: $u$ before $v$.
   Gain from $i \in C_u$: $v$ after $u$? Yes. So if $last[v] > i$, +1.
   Gain from $i \in C_v$: $v$ after $u$? No, $v$ is the current element. We check if $v$ after $u$. No, we check if $v$ is after $u$ in the list.
   Wait, the sum is over $v$ (target) and $x$ (removed).
   Gain = $\sum_{i} \sum_{v} [last[v] > i \land \text{order}(A[i]) < \text{order}(v)]$.
   Let's swap $u$ and $v$.
   Change = (Gain with $u<v$) - (Gain with $v<u$).
   Terms involving only $u$ and $v$:
   Case 1: $i$ such that $A[i] = u$.
     If $last[v] > i$:
       $u < v$: $u$ removed before $v$. Condition met. +1.
       $v < u$: $u$ removed after $v$. Condition failed. +0.
     If $last[v] \le i$: 0.
   Case 2: $i$ such that $A[i] = v$.
     If $last[u] > i$:
       $u < v$: $v$ removed after $u$. Condition ($u$ before $v$) met? No, we need $A[i]$ (which is $v$) before $v$? No.
       The condition is: $A[i]$ removed before $v$.
       If $A[i] = v$, then we need $v$ removed before $v$. Impossible.
       So for $i \in C_v$, the term is always 0?
       Wait, the sum is over $v$ (the target to delete) and $x = A[i]$ (the removed element).
       If $x = v$, then $x$ is removed at the same time as $v$? No, $v$ is the target.
       The removed elements are those deleted *before* $v$.
       So if $A[i] = v$, then $x=v$. $v$ is not removed before $v$.
       So for $i \in C_v$, the contribution is always 0.
   So only $i \in C_u$ matter?
   Wait, what if $A[i] = w$ (neither $u$ nor $v$)?
   Then we need $w$ removed before $v$.
   If $w$ is before both $u, v$:
     $u<v$: $w$ before $v$. If $last[v]>i$, +1.
     $v<u$: $w$ before $v$. If $last[v]>i$, +1.
     Same.
   If $w$ is after both: 0.
   If $w$ is between?
     $last[u] < i < last[v]$.
     $u<v$: $w$ before $v$. If $last[v]>i$, +1.
     $v<u$: $w$ before $v$. If $last[v]>i$, +1.
     Same.
   So only the relative order of $u$ and $v$ matters for the pair $(u, v)$?
   Wait, the condition is $order(A[i]) < order(v)$.
   If $A[i] = u$, we need $order(u) < order(v)$.
   If $A[i] = v$, we need $order(v) < order(v)$ (False).
   If $A[i] = w$, we need $order(w) < order(v)$.
   So the gain from $i \in C_u$ is $1$ if $last[v] > i$ and $u$ before $v$.
   The gain from $i \in C_v$ is 0.
   The gain from $i \in C_w$ depends on $order(w)$ vs $order(v)$.
   This suggests that the decision for $u$ vs $v$ is independent of $w$?
   No, because $order(w)$ might be affected by $u, v$? No, we are comparing two adjacent swaps.
   So, swapping $u$ and $v$ changes the gain by:
   $\Delta = (\text{count of } i \in C_u \text{ s.t. } last[v] > i) - (\text{count of } i \in C_u \text{ s.t. } last[v] > i \text{ and } v \text{ before } u \text{?})$.
   Actually, if $u$ before $v$: Gain += $\sum_{i \in C_u, last[v]>i} 1$.
   If $v$ before $u$: Gain += $\sum_{i \in C_v, last[u]>i} 1$? No, $A[i]=v$ gives 0.
   Wait, if $v$ before $u$, then for $i \in C_u$, we need $u$ before $v$ (False). So 0.
   For $i \in C_v$, we need $v$ before $v$ (False). So 0.
   So swapping $u$ and $v$ only affects terms where $A[i]=u$ and target is $v$, OR $A[i]=v$ and target is $u$.
   Wait, the sum is $\sum_{i} \sum_{v} [last[v] > i \land order(A[i]) < order(v)]$.
   If we swap $u, v$:
   Terms where $A[i]=u$:
     Target $v$: $order(u) < order(v)$?
       If $u<v$: True. Count += $\sum_{i \in C_u, last[v]>i} 1$.
       If $v<u$: False. Count += 0.
     Target $u$: $order(u) < order(u)$? False.
   Terms where $A[i]=v$:
     Target $u$: $order(v) < order(u)$?
       If $u<v$: False.
       If $v<u$: True. Count += $\sum_{i \in C_v, last[u]>i} 1$.
     Target $v$: False.
   So the difference is:
   Gain($u<v$) - Gain($v<u$) = $\sum_{i \in C_u, last[v]>i} 1 - \sum_{i \in C_v, last[u]>i} 1$.
   We should choose $u < v$ if $\sum_{i \in C_u, last[v]>i} 1 > \sum_{i \in C_v, last[u]>i} 1$.
   This is exactly the same condition as before!
   $Count(u \text{ before } last[v]) > Count(v \text{ before } last[u])$.
   So the sorting criterion is correct.
   And the calculation of the total gain can be done by:
   Total Gain = $\sum_{i=1}^N \sum_{v: last[v] > i} [order(A[i]) < order(v)]$.
   We can compute this by iterating $i$ from 1 to $N$.
   Let $x = A[i]$.
   We need to count how many $v$ satisfy $last[v] > i$ and $order(v) > order(x)$.
   This is a 2D range query?
   Points $(order(v), last[v])$. We want count of points with $y > i$ and $x > order(x)$.
   Since we sort the values, $order(v)$ is the index in the sorted list.
   We can use a Fenwick tree (BIT) or Segment Tree.
   Iterate $i$ from 1 to $N$.
   $x = A[i]$.
   Query BIT for count of values with $order > order(x)$ and $last > i$.
   Then update BIT?
   Wait, the condition is $last[v] > i$. As $i$ increases, the set of valid $v$ shrinks.
   Better: Iterate $i$ from $N$ down to 1?
   Or iterate $i$ from 1 to $N$, and maintain a data structure of $v$ with $last[v] > i$.
   Initially, all $v$ with $last[v] > 1$ are in the structure.
   As $i$ increases, we remove $v$ where $last[v] == i$.
   For each $i$, $x = A[i]$. We need count of active $v$ with $order(v) > order(x)$.
   This is a standard problem.
   Data structure: BIT over the ranks $1 \dots m$.
   Initially, add all $v$ to BIT at position $order(v)$.
   When $i$ increments, if there are any $v$ with $last[v] == i$, remove them from BIT (add -1 at $order(v)$).
   Then query BIT for sum in range $(order(x)+1, m)$.
   This takes $O(N \log m)$.
   Total complexity: Sorting $O(m \log m)$, BIT operations $O(N \log m)$.
   This fits within limits.