The key observation is that to move an element from position `i` to position `j` (where `i < j`), it must be swapped with every element in between. The cost of swapping adjacent elements at indices `k` and `k+1` is `k`. If we move an element from index `i` to `j` (`i < j`) by swapping it rightwards, the total cost is $\sum_{k=i}^{j-1} k$. Similarly, moving leftwards from `j` to `i` costs $\sum_{k=i}^{j-1} k$.

However, we don't just move one element. We need to sort the entire permutation. A crucial insight is that the relative order of inversions matters. Specifically, consider the contribution of each pair of elements that are inverted. But a simpler way to think about it is: each element `P[i]` needs to move to its target position `pos[P[i]]`. The cost of moving an element past another depends on the index of the swap.

Actually, a more robust approach is to realize that the total cost is the sum over all inversions $(i, j)$ with $i < j$ and $P[i] > P[j]$ of the cost to swap them. But swaps interact. 

Let's reconsider. When we swap $P_k$ and $P_{k+1}$, we pay $k$. This swap resolves the inversion between these two elements if they are inverted. However, moving an element past multiple others accumulates costs. 

Consider the final position of each element. Let $pos[v]$ be the current position of value $v$. The element $v$ needs to go to position $v$ (since the sorted array is $1, 2, \dots, N$). The cost to move an element from index $i$ to $j$ is not independent because other elements are also moving.

A known result for this specific problem (AtCoder ABC 256 F or similar) is that the minimum cost is the sum over all $i$ from $1$ to $N$ of $i \times (\text{number of inversions involving the swap at index } i)$. This is hard to count directly.

Alternative Insight: 
Think about the process in reverse or use the property that each swap at index $i$ costs $i$. The total cost is $\sum_{i=1}^{N-1} i \times (\text{number of times we swap at index } i)$.
To minimize cost, we should avoid expensive swaps. 
Actually, there is a simpler formula. The minimum cost to sort the permutation is equal to the sum of $i \times |P[i] - i|$? No, that's for uniform cost.

Let's look at Sample 1: `3 2 1`. 
Target: `1 2 3`.
1 is at pos 3, needs to go to pos 1. Distance 2 left.
2 is at pos 2, needs to go to pos 2. Distance 0.
3 is at pos 1, needs to go to pos 3. Distance 2 right.

The sample explanation uses 3 swaps. Total cost 4.
Swaps: (1,2) cost 1, (2,3) cost 2, (1,2) cost 1.

Key realization: Each inversion $(i, j)$ with $i < j$ and $P[i] > P[j]$ must be resolved. The cost of resolving an inversion between two specific values depends on when they are swapped. However, it turns out that the minimum total cost is simply the sum over all $i$ from $1$ to $N$ of $i \times (\text{number of elements to the right of } i \text{ that are smaller than } P[i])$? No, that's just counting inversions weighted by index, which isn't quite right because elements move.

Correct Approach: 
The problem is equivalent to finding the minimum cost to sort. It is known that for this specific cost function (cost $i$ for swap at $i$), the minimum cost is the sum of $i \times c_i$ where $c_i$ is the number of times a swap occurs at index $i$. 
In any sorting process using adjacent swaps, the number of times we swap at index $i$ is determined by the net flow of elements across the boundary between $i$ and $i+1$. Specifically, if $k$ elements end up to the right of the boundary that started to the left, and $m$ elements end up to the left that started to the right, the net number of swaps is $|k-m|$. But actually, the total number of swaps at index $i$ is exactly the number of inversions between the set of elements initially at indices $1 \dots i$ and the set of elements initially at indices $i+1 \dots N$. 
Let $S_i$ be the set of values $\{P_1, \dots, P_i\}$. Let $T_i$ be the set of values $\{P_{i+1}, \dots, P_N\}$. In the sorted array, the first $i$ positions contain values $\{1, \dots, i\}$. The number of elements from $S_i$ that are greater than $i$ (and thus must move to the right of the boundary) must be matched by elements from $T_i$ that are $\le i$ (and must move to the left). The number of such elements is the same. Let this count be $C_i$. Then, exactly $C_i$ swaps must occur across the boundary between $i$ and $i+1$. 
Therefore, the total cost is $\sum_{i=1}^{N-1} i \times C_i$, where $C_i$ is the number of elements in $P[1 \dots i]$ that are greater than $i$.