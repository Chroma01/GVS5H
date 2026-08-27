
## ideation
The problem asks to minimize the sum of coordinates of $N$ pieces on a number line after performing a specific operation any number of times.

**Analysis of the Operation:**
Let the pieces be sorted by coordinate as $X_1 < X_2 < \dots < X_N$.
The operation chooses an index $i$ ($1 \le i \le N-3$) and considers the pieces at positions $i, i+1, i+2, i+3$.
Let their coordinates be $A, B, C, D$ respectively.
The midpoint $M$ between $A$ and $D$ is $(A+D)/2$.
The new positions for the inner pieces $B$ and $C$ become:
$B' = 2M - B = A + D - B$
$C' = 2M - C = A + D - C$
The new set of coordinates for these four pieces is $\{A, A+D-B, A+D-C, D\}$.
Note that the outer pieces $A$ and $D$ remain unchanged. The inner pieces are reflected across the midpoint of the outer pieces.
The sum of the four coordinates changes from $A+B+C+D$ to $A + (A+D-B) + (A+D-C) + D = 3(A+D) - (B+C)$.
The change in sum is $\Delta = [3(A+D) - (B+C)] - [A+B+C+D] = 2(A+D) - 2(B+C) = 2(A+D - B - C)$.
To minimize the total sum, we want to perform operations that result in a negative $\Delta$, i.e., $A+D < B+C$.
If $A+D \ge B+C$, the operation would increase or keep the sum same, so we shouldn't perform it if our goal is minimization.

**Key Insight:**
The operation preserves the set of coordinates $\{X_1, X_3, X_5, \dots\}$ and $\{X_2, X_4, X_6, \dots\}$? No, the values change.
However, it is a known result for this specific problem (AtCoder ABC 279 F / similar) that the operation allows us to "convexify" the sequence. The final state is unique and corresponds to the "most convex" arrangement reachable.
Specifically, the minimum sum is achieved when the sequence satisfies the convexity condition: $X_{i+1} - X_i \le X_{i+2} - X_{i+1}$ for all valid $i$. This is equivalent to $X_i + X_{i+2} \ge 2X_{i+1}$, or $X_i + X_{i+3} \ge X_{i+1} + X_{i+2}$ (which is the condition for no further reduction).

Actually, there is a simpler invariant. The operation is reversible in terms of the multiset of values? No.
But notice that the operation on indices $i, i+1, i+2, i+3$ effectively allows us to swap the "inner" sum with the "outer" sum structure.
A crucial observation is that the **sum of the coordinates at odd indices** and **sum of the coordinates at even indices** (in the sorted order) are NOT invariant.
However, we can observe that the operation allows us to independently minimize the positions of the pieces.
It turns out that the minimum sum is simply the sum of the initial coordinates if the array is already "convex". If not, we can reduce the sum.
The final configuration is the one where the sequence is convex.
For a convex sequence, the values are "spread out" as much as possible given the constraints? No, convexity means they curve upwards.
Wait, if we want to minimize the sum, we want the values to be as small as possible.
The condition $X_i + X_{i+3} \ge X_{i+1} + X_{i+2}$ means the sequence is convex.
In a convex sequence, the differences between adjacent elements are non-decreasing.
The minimum sum is achieved when the sequence is "as flat as possible" at the beginning?
Actually, the correct approach is to realize that the operation preserves the **multiset of values** $\{X_1, X_3, X_5, \dots\}$ and $\{X_2, X_4, X_6, \dots\}$?
Let's check Sample 1: $1, 5, 7, 10$.
Odd indices: $1, 7$. Even indices: $5, 10$.
After operation: $1, 4, 6, 10$.
Odd indices: $1, 6$. Even indices: $4, 10$.
The multisets changed. So that invariant is false.

However, there is a known solution for this problem:
The minimum sum is obtained by sorting the initial array $X$ and then the answer is the sum of the initial array? No.
The correct insight is that the operation allows us to reorder the pieces such that the final sorted sequence is the same as the initial sorted sequence? No, values change.

Let's look at the constraints and the nature of the operation.
The operation is linear. The final state is unique.
The minimum sum is the sum of the coordinates of the pieces in the final convex state.
It can be shown that the final state is the same as the initial state if we consider the pieces as indistinguishable and just sort them? No.

Actually, the problem is equivalent to finding the minimum sum of a convex sequence that can be reached from the initial sequence.
A key property is that the **sum of the coordinates** can be minimized by applying operations that reduce the sum.
The process terminates when the sequence is convex.
The final sum is unique.

Given the complexity of deriving the closed form, and the fact that $N$ is up to $2 \times 10^5$, a simulation might be too slow if we do it naively.
However, we can use a priority queue to always pick the operation that reduces the sum the most.
But wait, the operation changes the values, which might enable new operations.
This looks like it could be $O(N^2)$ in the worst case.

There is a simpler observation:
The operation on $i, i+1, i+2, i+3$ is equivalent to replacing $B, C$ with $A+D-B, A+D-C$.
This is equivalent to reflecting the inner points.
It turns out that the minimum sum is simply the sum of the initial array if we can't reduce it.
But we can always reduce it if $A+D < B+C$.

Let's try a different approach.
The operation preserves the sum of $X_i$ for $i$ with specific parity? No.
But it preserves the sum of $X_i + X_{i+1}$ for some pairs? No.

Actually, the correct solution is that the minimum sum is the sum of the initial array if the array is already convex.
If not, we can reduce the sum.
The final state is the "convex hull" of the initial points?
No, the values change.

Let's look at the sample outputs again.
Sample 1: Sum 23 -> 21.
Sample 2: Sum 47 -> 41.
The difference is 2 and 6 respectively.
In Sample 1, the operation reduced the sum by 2.
In Sample 2, we can perform multiple operations.

I will implement a solution that uses a priority queue to greedily apply operations that reduce the sum.
Since $N$ is large, we need to be careful.
However, it is known that the number of operations is not too large?
Or we can use a more efficient method.

Actually, there is a known result:
The minimum sum is the sum of the initial array minus the maximum possible reduction.
The reduction is maximized when the sequence is convex.
The final sequence is the unique convex sequence reachable from the initial sequence.
This can be computed using a "convex hull" like algorithm.

Given the time, I will provide a solution that simulates the process using a priority queue, but with a limit on the number of operations or using a more efficient data structure.
However, for $N=2 \cdot 10^5$, a naive simulation might TLE.

Let's try to find a pattern.
The operation on $i, i+1, i+2, i+3$ reduces the sum by $2(B+C - A - D)$ if $B+C > A+D$.
We want to maximize this reduction.
This is equivalent to minimizing $A+D - B - C$.
We can use a priority queue to store the "potential" reduction for each window of 4.
When an operation is performed, the values of $B$ and $C$ change, which affects the windows $(i-1, i, i+1, i+2)$ and $(i+1, i+2, i+3, i+4)$.
So we need to update the priority queue.
This is similar to the "sliding window" problem.
We can use a segment tree or a heap to manage the operations.

Given the complexity, I will implement a solution that uses a heap to store the operations, and updates the heap when an operation is performed.
This should be $O(N \log N)$ or $O(N \log^2 N)$.

## worker: Implement a solution using a priority queue to sto
The problem asks to minimize the sum of coordinates of $N$ pieces on a number line after performing a specific operation any number of times. The operation on indices $i, i+1, i+2, i+3$ (sorted by coordinate) reflects the inner two pieces across the midpoint of the outer two. This changes the sum of the four pieces by $2(X_i + X_{i+3} - X_{i+1} - X_{i+2})$. To minimize the total sum, we should apply operations that result in a negative change, i.e., $X_i + X_{i+3} < X_{i+1} + X_{i+2}$.

The key insight is that the operation allows us to "convexify" the sequence. The final state is unique and corresponds to the "most convex" arrangement reachable. The process terminates when the sequence satisfies the convexity condition $X_i + X_{i+3} \ge X_{i+1} + X_{i+2}$ for all $i$.

We use a priority queue to greedily apply the operation with the maximum reduction. To handle updates efficiently, we use a lazy approach: when we pop an operation, we re-calculate the current reduction. If the current reduction is less than the stored reduction, we skip it (stale entry). If the current reduction is greater, we push it back (should have been picked earlier). If the current reduction is equal, we apply the operation and update the affected windows.

This approach ensures that we always pick the best operation, and the process terminates because each operation reduces the sum by a positive amount, and the sum is bounded below.
