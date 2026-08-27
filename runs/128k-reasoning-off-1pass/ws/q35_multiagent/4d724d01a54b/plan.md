The key insight is that to move an element from position `i` to position `j` (where `i < j`), it must swap with every element in between. The cost of swapping adjacent elements at indices `k` and `k+1` is `k`. Therefore, moving an element from index `i` to `j` (`i < j`) costs $\sum_{k=i}^{j-1} k$. Similarly, moving from `j` to `i` (`j > i`) costs $\sum_{k=i}^{j-1} k$. Notice that the cost depends only on the range of indices traversed, not on the values themselves.

However, a more efficient way to think about this is to consider the contribution of each swap. Alternatively, we can observe that the total cost is the sum over all pairs of inversions, but weighted by the index of the swap. A better approach: consider that each element $P_i$ needs to move to its target position $pos[P_i]$. The cost of moving an element from $a$ to $b$ is the sum of indices of the swaps it participates in. 

Actually, there's a known result for this problem: the minimum cost is the sum over all $i$ of $i \times (\text{number of elements to the left of } i \text{ that are greater than } P_i)$ plus something? No.

Let's reconsider. Each swap at index $i$ (swapping $P_i, P_{i+1}$) costs $i$. We want to sort the array. This is equivalent to counting inversions but with weighted costs. Specifically, if we use bubble-sort-like logic, the cost depends on the order of swaps. 

A crucial observation: The problem is equivalent to finding the minimum cost to sort, which can be solved by noting that each element $x$ at initial position $i$ must end up at position $x$. The path it takes contributes to the cost. However, swaps can be interleaved. 

Actually, the optimal strategy is to move each element to its correct position independently, but this isn't quite right because swaps affect two elements. 

Correct approach: The total cost is the sum for each $i$ from $1$ to $N-1$ of $i \times (\text{number of swaps performed at index } i)$. We need to determine the minimum number of swaps at each index. 

It turns out that the minimum total cost is $\sum_{i=1}^N i \times |P_i - i|$? No, sample 1: $3,2,1$. $1\times|3-1| + 2\times|2-2| + 3\times|1-3| = 2 + 0 + 6 = 8 \neq 4$.

Another known solution: The answer is $\sum_{i=1}^N \text{cost to move } P_i \text{ to position } i$. But swaps are shared.

Actually, the correct insight is: Consider the inversion table. The cost of swapping adjacent elements at index $i$ is $i$. The minimum cost to sort is the sum over all inversions $(i, j)$ with $i < j$ and $P_i > P_j$ of the index of the swap that resolves it. 

There is a simpler formula: The minimum cost is $\sum_{i=1}^N i \times (\text{number of elements greater than } P_i \text{ to the left of } i)$? Let's check sample 1: $P=[3,2,1]$.
$i=1, P_1=3$: 0 greater to left.
$i=2, P_2=2$: 1 greater (3) to left. Cost += $2 \times 1 = 2$.
$i=3, P_3=1$: 2 greater (3,2) to left. Cost += $3 \times 2 = 6$. Total 8. Wrong.

Let's try: sum over $i$ of (number of elements smaller than $P_i$ to the right) $\times i$? 
Sample 1:
$i=1, P_1=3$: 2 smaller to right (2,1). Cost += $1 \times 2 = 2$.
$i=2, P_2=2$: 1 smaller to right (1). Cost += $2 \times 1 = 2$.
$i=3, P_3=1$: 0. Total 4. Correct!

Sample 2: $P=[2,4,1,3,5]$
$i=1, P_1=2$: smaller to right: 1. Count=1. Cost += $1 \times 1 = 1$.
$i=2, P_2=4$: smaller to right: 1,3. Count=2. Cost += $2 \times 2 = 4$.
$i=3, P_3=1$: smaller to right: 0. Cost += 0.
$i=4, P_4=3$: smaller to right: 0. Cost += 0.
$i=5, P_5=5$: smaller to right: 0. Cost += 0.
Total = 5. But sample output is 6. So this is wrong.

Let's re-read carefully. The cost of swapping $P_i, P_{i+1}$ is $i$. 

Correct approach: This is a classic problem. The minimum cost is the sum over all $i$ of $i \times (\text{number of inversions where the left element is at index } i)$. No.

Actually, the correct solution is: For each element, calculate the number of elements to its right that are smaller than it (this is the standard inversion count contribution). Let this be $R_i$ for element at index $i$. Then the cost is $\sum_{i=1}^N R_i \times i$? We just tried that and got 5 for sample 2, but expected 6.

Wait, let's trace sample 2 manually. $P = [2, 4, 1, 3, 5]$.
One possible way:
Swap index 2 (4,1): cost 2. P=[2,1,4,3,5].
Swap index 1 (2,1): cost 1. P=[1,2,4,3,5].
Swap index 3 (4,3): cost 3. P=[1,2,3,4,5].
Total cost = 2+1+3 = 6.

Inversions: (2,1), (4,1), (4,3).
If we associate each inversion with the index of the left element:
(2,1): left index 1.
(4,1): left index 2.
(4,3): left index 2.
Sum of left indices: $1 + 2 + 2 = 5$. Still 5.

But the cost is not just the sum of left indices. The cost is the sum of the swap indices used. In the optimal sequence above, we used swaps at indices 1, 2, 3. 

Key insight: The minimum cost is equal to the sum over all $i$ of $i \times (\text{number of times a swap occurs at index } i)$. And the number of swaps at index $i$ is determined by how many elements need to cross the boundary between $i$ and $i+1$. Specifically, the number of swaps at index $i$ is the number of elements that start to the left of $i$ and end up to the right of $i$ (or vice versa). This is equal to the number of elements in $P[1..i]$ that are greater than $i$? No.

The number of swaps at index $i$ is exactly the number of elements in the prefix $P[1..i]$ that are greater than $i$? No. It is the number of elements in $P[1..i]$ that are greater than the number of elements in $P[1..i]$? 

Actually, the number of swaps at index $i$ is $| \{ j \leq i : P_j > i \} - \{ j > i : P_j \leq i \} |$? No, it's simpler: the number of swaps at index $i$ is the number of elements that need to cross from left to right or right to left across the boundary $i, i+1$. This is equal to the number of elements in $P[1..i]$ that are greater than $i$? No.

Let $L_i$ be the number of elements in $P[1..i]$ that are greater than $i$. And $R_i$ be the number of elements in $P[i+1..N]$ that are less than or equal to $i$. The number of swaps at index $i$ is $L_i$ (which equals $R_i$). 

For sample 2: $P=[2,4,1,3,5]$.
$i=1$: Prefix [2]. Elements > 1: 2,4,3,5? No, prefix is just [2]. Elements in prefix > 1: 2. So $L_1 = 1$. Swaps at index 1: 1.
$i=2$: Prefix [2,4]. Elements > 2: 4. So $L_2 = 1$. Swaps at index 2: 1.
$i=3$: Prefix [2,4,1]. Elements > 3: 4. So $L_3 = 1$. Swaps at index 3: 1.
$i=4$: Prefix [2,4,1,3]. Elements > 4: none. So $L_4 = 0$. Swaps at index 4: 0.
Total cost = $1\times1 + 2\times1 + 3\times1 + 4\times0 = 6$. Correct!

So the algorithm is: For each $i$ from $1$ to $N-1$, compute $L_i = $ number of elements in $P[1..i]$ that are greater than $i$. The answer is $\sum_{i=1}^{N-1} i \times L_i$.

To compute $L_i$ efficiently, note that $L_i = i - (\text{number of elements in } P[1..i] \text{ that are } \leq i)$. The number of elements in $P[1..i]$ that are $\leq i$ can be computed using a Fenwick tree (BIT) as we iterate $i$ from $1$ to $N-1$. We add $P_i$ to the BIT, then query the number of elements $\leq i$.