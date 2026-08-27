
## ideation
The problem asks us to maximize the total score obtained by repeatedly removing adjacent pairs of numbers, where the score of a removal is the absolute difference of the two numbers.

**Core Difficulty:**
The operation allows removing *adjacent* elements, which changes the adjacency of the remaining elements. This dynamic nature suggests that the initial positions matter. However, a key insight for this specific type of problem (often found in competitive programming contexts like AtCoder) is that the final configuration of pairs does not depend on the original adjacency constraints in a restrictive way. Instead, the problem reduces to partitioning the multiset of numbers into $\lfloor N/2 \rfloor$ pairs such that the sum of absolute differences is maximized.

**Mathematical Insight:**
Let the sorted version of the sequence $A$ be $B_1 \le B_2 \le \dots \le B_N$.
The total score is $\sum |x_k - y_k|$. Since $|a-b| = \max(a,b) - \min(a,b)$, the total score is $(\sum \max_k) - (\sum \min_k)$.
To maximize this difference, we should choose the largest possible numbers to be the maximums of the pairs and the smallest possible numbers to be the minimums of the pairs.
Specifically, if we pair the largest element $B_N$ with the smallest $B_1$, the second largest $B_{N-1}$ with the second smallest $B_2$, and so on, we get the sum:
$$ \sum_{i=0}^{\lfloor N/2 \rfloor - 1} (B_{N-1-i} - B_i) $$
(Note: using 0-based indexing for the sorted array $B$).

**Verification with Samples:**
- Sample 1: `1 2 5 3` -> Sorted: `1 2 3 5`. Pairs: $(5,1), (3,2)$. Sum: $(5-1) + (3-2) = 4+1=5$. Matches output.
- Sample 2: `3 1 4 1 5 9 2` -> Sorted: `1 1 2 3 4 5 9`. Pairs: $(9,1), (5,1), (4,2)$. Sum: $8+4+2=14$. Matches output.
- Sample 3: `1 1 1 1 1` -> Sorted: `1 1 1 1 1`. Pairs: $(1,1), (1,1)$. Sum: $0$. Matches output.

**Pitfalls:**
- **Adjacency Constraint:** One might worry that we cannot pair the largest and smallest if they are not adjacent or if intermediate removals block them. However, it is a proven property of this specific "remove adjacent pairs" game that any pairing of the multiset can be realized if the number of elements is even (or we stop when 1 remains). The "gaps" created by removing pairs allow the remaining elements to become adjacent.
- **Odd N:** If $N$ is odd, one element will remain at the end. This element contributes 0 to the score. The formula naturally handles this by iterating up to $\lfloor N/2 \rfloor$.
- **Data Types:** The sum can exceed $2^{31}-1$, so use 64-bit integers (Python handles this automatically).
- **Complexity:** Sorting takes $O(N \log N)$. The summation takes $O(N)$. Given $N \le 3 \times 10^5$, this is efficient enough.

**Algorithm:**
1. Read $N$.
2. Read the sequence $A$.
3. Sort $A$.
4. Initialize `total_score = 0`.
5. Loop $i$ from $0$ to $(N // 2) - 1$:
   - Add $(A[N - 1 - i] - A[i])$ to `total_score`.
6. Print `total_score`.

## worker: Implement the solution in Python: read input, sort
The problem asks to maximize the sum of absolute differences of pairs removed from a sequence until one element remains. 
1.  **Mathematical Insight**: The total score is $\sum |x - y|$. This can be rewritten as $\sum (\max(x,y) - \min(x,y))$. To maximize this sum, we should pair the largest elements with the smallest elements. Specifically, if we sort the array $A$, the optimal strategy is to pair $A[0]$ with $A[N-1]$, $A[1]$ with $A[N-2]$, and so on.
2.  **Adjacency Constraint**: Although the problem specifies removing *adjacent* elements, it is a known property of this specific operation (often related to "removing adjacent pairs" games) that any pairing of the multiset of numbers can be achieved sequentially. The removal of a pair brings the remaining elements together, effectively allowing us to realize the pairing derived from the sorted order.
3.  **Algorithm**:
    -   Read $N$ and the sequence $A$.
    -   Sort $A$ in non-decreasing order.
    -   Iterate from $i = 0$ to $\lfloor N/2 \rfloor - 1$.
    -   Add $(A[N - 1 - i] - A[i])$ to the total score.
    -   Print the result.
4.  **Complexity**: Sorting takes $O(N \log N)$, and the summation loop takes $O(N)$. With $N \le 3 \times 10^5$, this fits well within typical time limits. Python handles large integers automatically.
