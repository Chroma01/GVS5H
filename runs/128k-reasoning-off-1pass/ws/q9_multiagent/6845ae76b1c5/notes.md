
## ideation
The problem asks for the sum of absolute differences between elements of two prefixes $A[1..X_k]$ and $B[1..Y_k]$ for $K$ queries.
A naive $O(N \cdot K)$ solution is too slow given $N=10^5, K=10^4$.
The key insight is that $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j| = \int_{-\infty}^{\infty} | \text{count}(A[1..X] > t) - \text{count}(B[1..Y] > t) | dt$.
The function $f(t) = \text{count}(A[1..X] > t) - \text{count}(B[1..Y] > t)$ is a step function that is monotonically decreasing (as $t$ increases, the counts decrease).
Since it is monotonic, it crosses zero at most once. Let $v^*$ be the point where $f(t)$ changes from non-negative to negative.
Then the integral splits into two parts:
1. $\int_{-\infty}^{v^*} (f(t)) dt = \sum_{a \in A[1..X]} \min(a, v^*) - \sum_{b \in B[1..Y]} \min(b, v^*)$
2. $\int_{v^*}^{\infty} (-f(t)) dt = \sum_{b \in B[1..Y]} \max(0, b - v^*) - \sum_{a \in A[1..X]} \max(0, a - v^*)$

To compute these efficiently:
1. Coordinate compress all values in $A$ and $B$.
2. Build two Persistent Segment Trees (PST): one for $A$ and one for $B$. Each node in the PST will store the count of numbers and the sum of numbers in the range covered by that node.
3. For each query $(X, Y)$:
   - Find the pivot $v^*$ where the cumulative counts switch order. This can be done by walking down the two PSTs simultaneously in $O(\log N)$.
   - Query the PSTs to get $\sum \min(val, v^*)$ and $\sum \max(0, val - v^*)$ in $O(\log N)$.
   - Combine results.

Pitfalls:
- Handling the coordinate compression correctly (values can be up to $2 \cdot 10^8$).
- The pivot $v^*$ might not be an exact value from the array, but the integral calculation holds for any $v^*$ in the interval where the sign doesn't change. We can pick the largest value $u$ such that $cntA(u) \ge cntB(u)$ as the split point.
- Large numbers require 64-bit integers.
- Edge cases where one prefix is empty (though constraints say $X, Y \ge 1$).

## worker: Implement the coordinate compression logic and the
1.  **Algorithm**: The solution uses the integral representation of the sum of absolute differences: $\sum |a-b| = \int |count_A(t) - count_B(t)| dt$. Since the difference in counts is monotonic, it crosses zero at most once. We find this pivot point $v^*$ and split the integral into two parts where the sign is constant.
2.  **Data Structure**: Persistent Segment Trees (PST) are used to maintain the frequency and sum of values for prefixes of $A$ and $B$. This allows $O(\log N)$ queries for count and sum in any range.
3.  **Coordinate Compression**: Since values are large ($2 \cdot 10^8$), we compress them to ranks $1 \dots M$ based on sorted unique values.
4.  **Pivot Finding**: We traverse both PSTs simultaneously to find the largest rank where the count of $A$ is greater than or equal to the count of $B$.
5.  **Complexity**:
    -   Building PSTs: $O(N \log N)$.
    -   Per Query: $O(\log N)$ for finding pivot and $O(\log N)$ for sum queries.
    -   Total: $O((N+K) \log N)$.
6.  **Edge Cases**: Handled the case where $count_A < count_B$ everywhere (pivot index 0) by directly computing $Sum(B) - Sum(A)$.

## worker: Run the code against Sample 1 and Sample 2 to veri
The solution implements the integral representation of the sum of absolute differences: $\sum |a-b| = \int |count_A(t) - count_B(t)| dt$. Since the difference in counts is monotonic, it crosses zero at most once. We find this pivot point $v^*$ using a Persistent Segment Tree (PST) and split the integral into two parts where the sign is constant. The PSTs store the frequency and sum of values for prefixes of $A$ and $B$, allowing $O(\log N)$ queries. Coordinate compression is used to handle large values. The logic handles the edge case where the pivot is before the smallest element (countA < countB everywhere) separately.

## worker: finalize
The solution implements the integral representation of the sum of absolute differences: $\sum |a-b| = \int |count_A(t) - count_B(t)| dt$. Since the difference in counts is monotonic, it crosses zero at most once. We find this pivot point $v^*$ using a Persistent Segment Tree (PST) and split the integral into two parts where the sign is constant. The PSTs store the frequency and sum of values for prefixes of $A$ and $B$, allowing $O(\log N)$ queries. Coordinate compression is used to handle large values. The logic handles the edge case where the pivot is before the smallest element (countA < countB everywhere) separately.
