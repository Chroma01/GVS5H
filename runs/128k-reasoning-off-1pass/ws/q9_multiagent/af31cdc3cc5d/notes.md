
## ideation
The problem asks us to maximize the total score obtained by repeatedly removing adjacent pairs of numbers, where the score of each operation is the absolute difference of the pair.

**Core Difficulty**:
The constraint is that we can only remove *adjacent* elements. However, removing a pair brings the elements to its left and right together. This implies that we are effectively partitioning the original sequence into pairs (and possibly leaving one element out if $N$ is odd) such that the pairs can be formed sequentially.
A key insight for this specific problem (often associated with AtCoder problems like "Maximum Score" or similar variations) is that the adjacency constraint does not restrict the set of possible pairings in a way that prevents achieving the theoretical maximum for a static set of numbers. Specifically, if we sort the array $A$, the maximum possible sum of absolute differences for any subset of size $2k$ is achieved by pairing the smallest $k$ elements with the largest $k$ elements (specifically, $i$-th smallest with $i$-th largest).
The question then reduces to: Can we achieve this pairing given the adjacency constraint?
Yes. It can be proven that for any even $N$, we can pair the sorted elements $A_1$ with $A_N$, $A_2$ with $A_{N-1}$, etc., through a sequence of adjacent removals. If $N$ is odd, we leave out the median element (or the one that minimizes the loss) and pair the rest optimally.

**Candidate Approaches**:
1.  **Sorting and Greedy Calculation**:
    *   Sort the array $A$.
    *   If $N$ is even, the maximum score is $\sum_{i=0}^{N/2-1} (A_{N-1-i} - A_i)$. This simplifies to (Sum of largest $N/2$) - (Sum of smallest $N/2$).
    *   If $N$ is odd, we must leave out one element. To maximize the sum, we leave out the element at the median position (index $N//2$ in 0-based sorted array). The score is (Sum of largest $(N-1)/2$) - (Sum of smallest $(N-1)/2$).
    *   This can be unified: Let $k = N // 2$. The answer is `sum(A[N-k:]) - sum(A[:k])`.

2.  **Dynamic Programming**:
    *   Define $DP[i][j]$ as the max score for a subarray from index $i$ to $j$.
    *   Transition: $DP[i][j] = \max(DP[i+1][j-1] + |A[i]-A[j]|, \dots)$.
    *   This is $O(N^3)$ or $O(N^2)$, which is too slow for $N=3 \times 10^5$.

3.  **Simulation**:
    *   Try to simulate the process. But finding the optimal move at each step is hard (greedy doesn't work).

## worker: Write the Python code to read $N$ and the sequence
The problem asks us to maximize the sum of absolute differences of pairs formed by repeatedly removing adjacent elements.
1.  **Observation**: The operation of removing adjacent pairs allows us to effectively pair any two elements in the original sequence, provided the total number of elements removed is even (which it is, since we remove 2 at a time). If $N$ is even, all elements are paired. If $N$ is odd, one element remains unpaired.
2.  **Optimal Pairing**: For a set of $2k$ numbers, the sum of absolute differences $\sum |x_i - y_i|$ is maximized when we pair the smallest number with the largest, the second smallest with the second largest, and so on. The total sum becomes $\sum_{i=1}^k (L_i - S_i)$, where $L$ are the largest $k$ numbers and $S$ are the smallest $k$ numbers.
3.  **Handling Odd $N$**: If $N$ is odd, we must leave one element out. To maximize the remaining sum, we should leave out the element that contributes least to the difference sum. In the sorted array, the optimal element to exclude is the median (the one at index $N//2$).
4.  **Algorithm**:
    *   Sort the array $A$.
    *   Let $k = N // 2$.
    *   The answer is the sum of the last $k$ elements minus the sum of the first $k$ elements.
    *   This logic holds for both even and odd $N$ because integer division $N // 2$ correctly calculates the count of pairs, and the slicing `A[N-k:]` and `A[:k]` automatically excludes the middle element when $N$ is odd.
