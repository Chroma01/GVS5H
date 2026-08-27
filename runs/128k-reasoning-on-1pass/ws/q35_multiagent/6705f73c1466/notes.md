
## ideation
The problem asks for the minimum number of adjacent swaps to make all `1`s contiguous. This is equivalent to moving the `1`s to a contiguous block of length `k` (where `k` is the count of `1`s) such that the total distance each `1` travels is minimized. Since the `1`s are indistinguishable, the optimal strategy is to move the `j`-th `1` (from left to right) to the `j`-th position of the target block.

Let the original positions of the `1`s be $p_0, p_1, \dots, p_{k-1}$. If we choose the target block to start at index $x$, the target positions are $x, x+1, \dots, x+k-1$. The cost is $\sum_{j=0}^{k-1} |p_j - (x+j)|$.
Rearranging terms, this becomes $\sum_{j=0}^{k-1} |(p_j - j) - x|$.
Let $q_j = p_j - j$. The problem reduces to finding an integer $x$ that minimizes $\sum |q_j - x|$. This is a classic problem where the optimal $x$ is the median of the values $q_j$. Since $p_j$ are sorted, $q_j$ is also non-decreasing, so the median is simply $q_{k//2}$.
The algorithm runs in $O(N)$ time and $O(N)$ space, which easily satisfies the constraints $N \le 5 \times 10^5$.

## worker: Read input $N$ and string $S$ from standard input.
The problem asks for the minimum adjacent swaps to make all `1`s contiguous. Adjacent swaps correspond to moving elements by distance, so the total swaps equal the sum of distances each `1` travels. Since `1`s are indistinguishable, the optimal strategy preserves their relative order: the $j$-th `1` from the left moves to the $j$-th position of the target contiguous block.

Let the original positions of `1`s be $p_0, p_1, \dots, p_{k-1}$. If the target block starts at index $x$, the target positions are $x, x+1, \dots, x+k-1$. The cost is $\sum_{j=0}^{k-1} |p_j - (x+j)| = \sum_{j=0}^{k-1} |(p_j - j) - x|$.
Defining $q_j = p_j - j$, we need to find $x$ minimizing $\sum |q_j - x|$. This is minimized when $x$ is the median of $q_j$. Since $p_j$ are sorted, $q_j$ is sorted, so the median is simply $q_{k//2}$. The algorithm runs in $O(N)$ time and $O(N)$ space, well within the constraints.
