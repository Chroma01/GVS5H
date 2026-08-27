
## ideation


## worker: finalize
The problem asks for the minimum number of operations to empty the sequence. The operations are swapping adjacent elements and deleting a prefix of identical elements.
We hypothesize that the optimal strategy involves deleting all occurrences of each distinct value in a single batch. The order in which we delete these batches matters.
If we decide to delete values in the order $v_1, v_2, \ldots, v_d$, the cost is the sum of swaps needed to bring each $v_i$ to the front plus 1 for the deletion.
The number of swaps to bring $v_i$ to the front is the number of elements not equal to $v_i$ that are currently before the last occurrence of $v_i$.
This cost can be modeled as a Minimum Feedback Arc Set problem on a tournament graph, but with a special structure.
It turns out that sorting the values by their first occurrence index $F_v$ gives the optimal order.
The total cost can be computed as $\sum L_v - \sum_{j} \sum_{i \ge j} \text{Count}(v_j, L_{v_i}) + d$, where $L_v$ is the last occurrence index, and $\text{Count}(u, k)$ is the number of occurrences of $u$ in the prefix of length $k$.
The term $\sum_{i \ge j} \text{Count}(v_j, L_{v_i})$ can be computed efficiently using a Fenwick Tree (BIT) by processing values in reverse order of their first occurrence.
The time complexity is $O(N \log N)$ per test case, which fits within the constraints.
