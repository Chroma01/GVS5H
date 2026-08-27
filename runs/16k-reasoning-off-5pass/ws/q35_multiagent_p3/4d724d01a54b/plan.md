The key insight is that each element $P_i$ must move from its initial position to its target position (where value $v$ should be at index $v-1$). Since we can only swap adjacent elements, the number of swaps an element participates in is determined by how far it needs to travel. However, the cost depends on the index of the swap. A swap at index $i$ costs $i$. 

We can think of this as: each element $x$ starts at position $pos[x]$ and needs to go to position $x-1$ (0-indexed). The total cost is the sum over all swaps. Notice that if an element moves left past index $i$, it contributes $i$ to the cost. If it moves right past index $i$, it also contributes $i$ to the cost. 

A more efficient approach: Consider that each inversion must be resolved. But the cost is not just the number of inversions. Instead, observe that the minimum cost is achieved when we move each element directly to its target position without unnecessary back-and-forth. The cost for moving an element from position $j$ to position $k$ involves swaps at various indices. 

Actually, a well-known result for this problem: The minimum cost is the sum over all elements $i$ of $|initial\_position[i] - target\_position[i]| \times \text{something}$? No.

Let's reconsider: Each swap of adjacent elements at index $i$ (1-indexed) costs $i$. This is equivalent to: the total cost is the sum for each element of the sum of indices where it was swapped. 

An optimal strategy is to move each element to its correct position. The total cost can be computed by considering that each time an element crosses a boundary between index $i$ and $i+1$, it pays cost $i$. The number of times the boundary between $i$ and $i+1$ is crossed is equal to the number of inversions across that boundary? Not exactly.

Actually, the correct approach: The minimum cost is $\sum_{i=1}^{N} |P_i - i| \times \text{weight}$? No.

Let's use the fact that the problem is equivalent to: each element $v$ needs to move from its initial position to position $v-1$ (0-indexed). The cost of moving an element from $a$ to $b$ is not simply $|a-b|$ because the cost depends on the index. 

However, note that the total cost is equal to the sum over all $i$ from $1$ to $N-1$ of $i \times (\text{number of times a swap at index } i \text{ is performed})$. The number of swaps at index $i$ is determined by how many elements need to cross from left to right or right to left across the boundary between $i$ and $i+1$. Specifically, if we consider the final configuration, the number of elements that are initially to the left of the boundary and end up to the right, plus those initially to the right and end up to the left, divided by 2? Actually, the net flow must be zero, but the total crossings is the number of inversions across that boundary.

Wait, a simpler insight: The minimum total cost is $\sum_{i=1}^{N} |P_i - i| \times \text{something}$? Let's check sample 1: P = [3,2,1]. 
- Element 1: starts at pos 2 (0-indexed), target 0. Distance 2.
- Element 2: starts at pos 1, target 1. Distance 0.
- Element 3: starts at pos 0, target 2. Distance 2.
Sum of distances = 4. Output is 4.

Sample 2: P = [2,4,1,3,5] (0-indexed positions)
- Element 1: pos 2, target 0. Dist 2.
- Element 2: pos 0, target 1. Dist 1.
- Element 3: pos 3, target 2. Dist 1.
- Element 4: pos 1, target 3. Dist 2.
- Element 5: pos 4, target 4. Dist 0.
Sum = 2+1+1+2+0 = 6. Output is 6.

So the answer is simply $\sum_{i=1}^{N} |P_i - i|$? Wait, in 1-indexed: $P_i$ is the value, and it should be at position $P_i$. So the initial position of value $v$ is the index $j$ such that $P_j = v$. The target position is $v$ (1-indexed). So cost = $\sum_{v=1}^{N} |initial\_pos[v] - v|$.

Yes! This matches both samples. So the algorithm is:
1. Read $N$ and $P$.
2. For each value $v$ from 1 to $N$, find its initial position (0-indexed or 1-indexed consistently).
3. Sum $|initial\_pos[v] - v|$ (using 1-indexed positions for both).