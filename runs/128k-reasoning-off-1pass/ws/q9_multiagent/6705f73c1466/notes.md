
## ideation
**Core Difficulty:**
The problem asks for the minimum number of swaps to make all '1's contiguous. Since a swap between adjacent elements reduces the distance of one element to its target by exactly 1 (or increases it), the minimum number of swaps required to move a set of items to specific target positions is equal to the sum of the absolute differences between their initial positions and their final target positions.

**Key Insight:**
1.  Let $K$ be the total count of '1's in the string.
2.  The final state will have '1's occupying a contiguous block of length $K$. Let this block start at index $l$ (0-indexed). The indices occupied will be $l, l+1, \dots, l+K-1$.
3.  We need to find the optimal starting position $l$ such that the total displacement cost is minimized.
4.  Let the initial indices of the '1's be $p_1, p_2, \dots, p_K$ (sorted).
5.  If the target block starts at $l$, the $i$-th '1' (originally at $p_i$) should move to $l + (i-1)$.
6.  The cost for a fixed $l$ is $\sum_{i=1}^{K} |p_i - (l + i - 1)| = \sum_{i=1}^{K} |(p_i - (i-1)) - l|$.
7.  Let $q_i = p_i - (i-1)$. The problem reduces to finding an integer $l$ that minimizes $\sum |q_i - l|$.
8.  The value $l$ that minimizes the sum of absolute differences is the **median** of the sequence $q$.
9.  However, we must also consider constraints on $l$. The block must fit within the string boundaries: $0 \le l$ and $l+K-1 < N$.
10. Since $N$ is up to $5 \times 10^5$, an $O(N)$ or $O(N \log N)$ solution is required. Calculating the median is $O(K)$ (or $O(N)$), and computing the sum is $O(K)$. We don't even need to iterate all possible $l$; we just find the median of $q$ and clamp it to the valid range $[0, N-K]$.

**Candidate Approaches:**
1.  **Median Approach (Optimal):**
    *   Extract indices of all '1's into a list `ones`.
    *   Construct a new list `adjusted` where `adjusted[i] = ones[i] - i`.
    *   Find the median of `adjusted`. Let this be `opt_l`.
    *   Clamp `opt_l` to the range $[0, N - K]$.
    *   Calculate the total cost using this clamped `opt_l`.

2.  **Iterative Check (Sliding Window / Prefix Sums):**
    *   Iterate over all possible start positions $l$ from $0$ to $N-K$.
    *   For each $l$, calculate cost. This would be $O(N \cdot K)$, which is too slow ($O(N^2)$ worst case).
    *   Optimization: Use prefix sums to calculate the cost in $O(1)$ after $O(N)$ preprocessing.
    *   Cost function $f(l) = \sum |p_i - (l+i)|$. This is a convex function. We can use ternary search or simply find the minimum via the derivative (which relates to the median logic above). The median approach is essentially finding the minimum of this convex function directly.

**Pitfalls:**
*   **Off-by-one errors:** Careful with 0-based vs 1-based indexing. The problem uses 1-based in description but standard implementation uses 0-based.
*   **Median definition:** If the number of elements is even, any integer between the two middle elements (inclusive) minimizes the sum. We can pick either or the average (floored).
*   **Boundary conditions:** The calculated optimal $l$ might be outside $[0, N-K]$. We must clamp it.
*   **Large inputs:** Ensure integer types can handle the sum (Python handles large integers automatically, but logic must be efficient).

**Algorithm Selection:**
The Median approach is $O(N)$ and simplest to implement correctly.
1. Read $N$ and $S$.
2. Collect indices of '1's into list `P`.
3. Compute `Q = [P[i] - i for i in range(len(P))]`.
4. Find median of `Q`.
5. Clamp median to $[0, N - len(P)]$.
6. Compute total distance.

## worker: Implement the solution using the Median approach: 
The solution implements the median approach derived in the ideation phase.
1.  **Input Parsing**: Reads $N$ and string $S$ efficiently.
2.  **Index Extraction**: Identifies the 0-based indices of all '1's.
3.  **Transformation**: Computes `adjusted_indices` where `adjusted[i] = ones[i] - i`. This transformation accounts for the relative spacing required in the final contiguous block. Specifically, if the block starts at `l`, the $i$-th '1' (0-indexed in the list of ones) should end up at `l + i`. The cost to move it from `ones[i]` to `l + i` is `|ones[i] - (l + i)| = |(ones[i] - i) - l|`.
4.  **Optimization**: The problem reduces to finding an integer `l` that minimizes $\sum |q_i - l|$, which is a classic property of the median.
5.  **Constraints Handling**: The calculated median might fall outside the valid range $[0, N-K]$ where the block of 1s fits. We clamp the median to this range.
6.  **Complexity**: 
    -   Finding indices: $O(N)$.
    -   Sorting/Selecting median: $O(N)$ (using `sort` or `nth_element` logic; Python's sort is $O(N \log N)$ which is acceptable for $5 \times 10^5$).
    -   Calculating cost: $O(N)$.
    -   Total Time Complexity: $O(N \log N)$ due to sorting, which fits well within typical time limits (usually 1-2 seconds for $5 \times 10^5$).
    -   Space Complexity: $O(N)$ to store indices.

## worker: Verify logic with provided sample inputs mentally 
The logic follows the median approach derived in the ideation phase.
1.  **Input Parsing**: Correctly reads $N$ and $S$.
2.  **Index Extraction**: Collects 0-based indices of '1's.
3.  **Transformation**: Computes `adjusted_indices` where `adjusted[i] = ones[i] - i`. This effectively shifts the coordinate system so that the relative positions of the '1's in the final contiguous block (starting at $l$) correspond to $0, 1, \dots, K-1$. The cost to move the $i$-th '1' to position $l+i$ is $|ones[i] - (l+i)| = |(ones[i]-i) - l|$.
4.  **Optimization**: The problem reduces to finding $l$ that minimizes $\sum |q_i - l|$, which is solved by the median of $q$.
5.  **Constraints**: The calculated median is clamped to $[0, N-K]$ to ensure the resulting block of '1's fits within the string boundaries.
6.  **Complexity**: Sorting is not explicitly needed if we just pick the median, but `adjusted_indices` is already sorted because `ones_indices` is sorted and we subtract an increasing sequence ($i$). Thus, `adjusted_indices` is sorted, and the median is simply at index `k // 2`. The complexity is $O(N)$ for scanning the string and $O(K)$ for the rest, which is optimal.

**Dry Run Sample 1**:
$N=7, S=0101001$
Indices of '1': $[1, 3, 6]$ ($K=3$)
Adjusted: $[1-0, 3-1, 6-2] = [1, 2, 4]$
Median of $[1, 2, 4]$ is $2$.
Range for $l$: $[0, 7-3] = [0, 4]$. Median $2$ is in range.
Cost: $|1-2| + |2-2| + |4-2| = 1 + 0 + 2 = 3$. Correct.

**Dry Run Sample 2**:
$N=3, S=100$
Indices: $[0]$ ($K=1$)
Output 0. Correct.

**Dry Run Sample 3**:
$N=10, S=0101001001$
Indices: $[1, 3, 6, 9]$ ($K=4$)
Adjusted: $[1-0, 3-1, 6-2, 9-3] = [1, 2, 4, 6]$
Median (even count): index $4//2 = 2$, value $4$.
Range for $l$: $[0, 10-4] = [0, 6]$. Median $4$ is in range.
Cost: $|1-4| + |2-4| + |4-4| + |6-4| = 3 + 2 + 0 + 2 = 7$. Correct.
