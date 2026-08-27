
## ideation
The problem asks for the minimum number of swaps to make all '1's contiguous. Swapping adjacent elements is equivalent to moving an element past another, and the cost is the distance moved. Since we only care about the relative order of '1's (they don't need to be permuted among themselves, just grouped), we can think of moving the $i$-th '1' (from left to right) to a target position.

Let the positions of the '1's be $p_0, p_1, \dots, p_{k-1}$ (0-indexed).
If we decide that the block of '1's will end up at positions $l, l+1, \dots, l+k-1$, then the $i$-th '1' (originally at $p_i$) must move to position $l+i$.
The cost for this specific '1' is $|p_i - (l+i)|$.
The total cost is $\sum_{i=0}^{k-1} |p_i - (l+i)| = \sum_{i=0}^{k-1} |(p_i - i) - l|$.

Let $q_i = p_i - i$. The problem reduces to finding an integer $l$ that minimizes $\sum_{i=0}^{k-1} |q_i - l|$.
This is a classic problem: the value $l$ that minimizes the sum of absolute differences is the **median** of the values $q_i$.

So the algorithm is:
1. Find all indices where $S[i] == '1'$. Let these be $p_0, p_1, \dots, p_{k-1}$.
2. Compute $q_i = p_i - i$ for each $i$.
3. Find the median of the list $q$. If $k$ is odd, the median is the middle element. If $k$ is even, any integer between the two middle elements (inclusive) works; typically we can pick either one (e.g., $q_{k//2}$ or $q_{k//2 - 1}$). Let's pick $q_{k//2}$ for simplicity.
4. Calculate the total cost $\sum |q_i - \text{median}|$.

Constraints: $N \le 5 \times 10^5$. The number of 1s $k$ is at most $N$. Finding positions is $O(N)$. Sorting $q$ takes $O(k \log k)$. Calculating the sum takes $O(k)$. This is efficient enough.

Pitfalls:
- 0-indexing vs 1-indexing. The problem uses 1-based indexing for description but standard string indexing is 0-based. The relative distances remain the same regardless of base, as long as we are consistent. Using 0-based indices for $p_i$ is fine.
- Median selection for even $k$. The function $\sum |q_i - l|$ is convex and piecewise linear. The minimum is achieved for any $l$ in the interval $[q_{k/2 - 1}, q_{k/2}]$ (for 0-indexed sorted $q$). Picking either endpoint is sufficient.

## worker: none
The problem reduces to finding a target contiguous block of length $k$ (where $k$ is the count of '1's) such that the total distance moved by all '1's to reach their respective positions in this block is minimized.

Let the original positions of the '1's be $p_0, p_1, \ldots, p_{k-1}$ (0-indexed).
If the target block starts at index $l$, the '1's will occupy positions $l, l+1, \ldots, l+k-1$.
The $i$-th '1' moves from $p_i$ to $l+i$. The cost is $|p_i - (l+i)| = |(p_i - i) - l|$.
Let $q_i = p_i - i$. The total cost is $\sum_{i=0}^{k-1} |q_i - l|$.
This sum is minimized when $l$ is the median of the values $q_i$.
The algorithm:
1. Collect indices of all '1's.
2. Compute $q_i = p_i - i$.
3. Sort $q$ and pick the median.
4. Sum the absolute differences from the median.

Time Complexity: $O(N)$ to find positions, $O(k \log k)$ to sort $q$ (where $k \le N$), and $O(k)$ to compute the sum. Overall $O(N \log N)$ in the worst case, which is efficient for $N \le 5 \times 10^5$.
Space Complexity: $O(N)$ to store positions and $q$.
