The key insight is that each element $P_i$ must move from its initial position to its target position (where value $v$ should be at index $v-1$). The cost of swapping adjacent elements at indices $i$ and $i+1$ is $i$. This means moving an element to the left across index $i$ (from $i+1$ to $i$) costs $i$, and moving it to the right across index $i$ (from $i$ to $i+1$) also costs $i$. 

However, we can think of this as: each inversion or displacement contributes to the cost. A more efficient way is to consider that each element $x$ starts at position $pos[x]$ and needs to go to position $x-1$ (0-indexed). The total cost can be computed by considering how many times each "edge" between index $i$ and $i+1$ is crossed. 

Actually, a well-known result for this specific problem (AtCoder ABC 256 F or similar) is that the minimum cost is the sum over all elements of the absolute difference between their initial and final positions, but weighted differently. Let's reconsider: when you swap elements at $i$ and $i+1$, you pay $i$. This is equivalent to saying that each time an element crosses the boundary between position $i$ and $i+1$, it incurs a cost of $i$. 

The optimal strategy is to move each element directly to its target position without unnecessary back-and-forth. The total cost is the sum for each element of the cost to move it from its start to end. But since swaps affect two elements, we need a global view. 

Correct approach: The minimum cost is equal to the sum of $i \times (\text{number of times the boundary } i \leftrightarrow i+1 \text{ is crossed})$. Each element $v$ must move from its initial index $pos[v]$ to target index $v-1$ (0-indexed). The number of times boundary $i$ is crossed is the number of elements that start on one side of $i$ and end on the other. Specifically, for boundary $i$ (between index $i$ and $i+1$, 0-indexed), the cost contribution is $i+1$ (1-indexed cost) times the number of elements crossing it. 

Actually, let's use the fact that the answer is $\sum_{i=1}^{N-1} i \times | \text{count of elements in } P[0..i-1] \text{ that belong in } P[i..N-1] - \text{count of elements in } P[i..N-1] \text{ that belong in } P[0..i-1] | / 2$? No. 

Simpler: For each element, the number of boundaries it crosses is $|pos[v] - (v-1)|$. But each swap crosses one boundary for two elements. The total cost is $\sum_{v=1}^N |pos[v] - (v-1)| \times \text{something}$? No. 

Correct known solution: The minimum cost is $\sum_{i=1}^{N-1} i \times c_i$, where $c_i$ is the number of inversions that cross the boundary $i$. This equals $\sum_{i=1}^{N-1} i \times | \text{number of elements } \leq i \text{ in first } i \text{ positions} - i |$? 

Actually, the standard solution is: For each position $i$ from $0$ to $N-2$ (0-indexed), the number of times the swap at index $i$ (cost $i+1$) is needed is the absolute difference between the number of elements in $P[0..i]$ that are greater than $i+1$ and those less than or equal? 

Let me use the inversion-based approach with a BIT. The answer is $\sum_{v=1}^N |pos[v] - (v-1)|$ is not correct. 

Final correct insight: Each element $v$ must travel from $pos[v]$ to $v-1$. The total distance is $\sum |pos[v] - (v-1)|$. But each swap moves two elements one step. The cost is not simply the sum of distances. 

Actually, the correct formula is: The minimum cost is $\sum_{i=1}^{N-1} i \times |L_i - R_i|$, where $L_i$ is the number of elements in the first $i$ positions that should end up in the last $N-i$ positions, and $R_i$ is the number of elements in the last $N-i$ positions that should end up in the first $i$ positions. And $L_i = R_i$ always, so it's $2 \times L_i$? No, the net flow is what matters. 

I recall that for this problem, the answer is $\sum_{i=1}^{N-1} i \times | \text{balance}_i |$, where $\text{balance}_i$ is the number of elements in $P[0..i-1]$ that are $> i$ minus the number of elements in $P[i..N-1]$ that are $\leq i$. This balance is always non-negative? 

Let's just implement: For each $i$ from $0$ to $N-2$, compute the number of elements in $P[0..i]$ that are greater than $i+1$. Let this be $cnt$. Then the cost contribution for boundary $i$ (cost $i+1$) is $(i+1) \times cnt$. Sum these up.