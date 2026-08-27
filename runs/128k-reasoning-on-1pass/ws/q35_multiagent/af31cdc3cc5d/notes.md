
## ideation
The problem asks for the maximum total score obtained by repeatedly removing adjacent pairs from a sequence. The score of each removal is the absolute difference of the pair.
Key observations:
1.  **Parity Constraint**: When two adjacent elements are removed, the elements to their left and right become adjacent. This process implies that any valid pairing of elements must pair an element originally at an odd index with an element originally at an even index. This is because removing a pair reduces the distance between remaining elements by 2, preserving the parity of the distance between any two remaining elements relative to the start. Thus, we can partition the sequence into two lists: $O$ (elements at odd indices $1, 3, \ldots$) and $E$ (elements at even indices $2, 4, \ldots$).
2.  **Matching Problem**: The problem reduces to finding a matching between $O$ and $E$ that maximizes the sum of absolute differences.
    *   If $N$ is even, $|O| = |E| = N/2$. We must pair every element of $O$ with a unique element of $E$.
    *   If $N$ is odd, $|O| = (N+1)/2$ and $|E| = (N-1)/2$. We must pair every element of $E$ with a unique element of $O$, leaving exactly one element of $O$ unpaired.
3.  **Optimal Strategy**: To maximize $\sum |x_i - y_i|$, the optimal strategy is to sort both lists and pair the smallest element of one list with the largest of the other, the second smallest with the second largest, and so on.
    *   For the even case, this is straightforward.
    *   For the odd case, we need to determine which element of $O$ to discard. We can compute the score for discarding each element efficiently. Let $O$ and $E$ be sorted. The base score (discarding the largest element of $O$) can be computed directly. For discarding an element $O[k]$ (where $k < |O|-1$), the pairing shifts for elements after $k$. We can use prefix/suffix sums to compute the change in score in $O(1)$ time for each candidate $k$.

Complexity: Sorting takes $O(N \log N)$. The rest of the operations are linear $O(N)$. Total time complexity is $O(N \log N)$, which fits within the limits for $N \le 3 \times 10^5$.

## worker: Implement input reading and split the sequence int
The problem reduces to finding a maximum weight matching between two sets of numbers, $O$ (elements at odd positions) and $E$ (elements at even positions). This is because any valid sequence of removals pairs an element from $O$ with an element from $E$.
1.  **Parity Argument**: Removing adjacent elements preserves the alternating parity of the remaining elements' original indices. Thus, we can partition the problem into matching $O$ and $E$.
2.  **Optimal Matching**: To maximize $\sum |x_i - y_i|$, we sort both lists and pair the smallest of one with the largest of the other.
3.  **Handling Odd N**: If $N$ is odd, $|O| = |E| + 1$. We must discard one element from $O$. We compute the score for discarding the largest element first, then use a recurrence relation to efficiently compute the score for discarding each subsequent element from largest to smallest.
4.  **Complexity**: Sorting takes $O(N \log N)$. The rest of the operations are linear $O(N)$. Total time complexity is $O(N \log N)$, which fits within the limits.
