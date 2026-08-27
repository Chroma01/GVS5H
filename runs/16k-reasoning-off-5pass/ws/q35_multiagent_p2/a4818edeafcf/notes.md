
## ideation
The problem requires splitting an array $A$ of length $N$ into three non-empty contiguous subarrays by choosing two split points $i$ and $j$ ($1 \le i < j \le N-1$). The goal is to maximize the sum of the number of distinct elements in each subarray: $D(A[1..i]) + D(A[i+1..j]) + D(A[j+1..N])$.

A naive $O(N^2)$ approach checking all pairs $(i,j)$ is too slow for $N \le 3 \times 10^5$. We need an $O(N \log N)$ or $O(N)$ solution.

Key observations:
1. Let `pre[i]` be the number of distinct elements in $A[1..i]$.
2. Let `suf[j]` be the number of distinct elements in $A[j..N]$.
3. The middle term is $D(A[i+1..j])$.
4. The total score for a pair $(i,j)$ is `pre[i] + D(A[i+1..j]) + suf[j+1]`.

We can iterate over the right boundary $j$ of the middle segment (from $2$ to $N-1$ in 1-based indexing, or $1$ to $N-2$ in 0-based). For a fixed $j$, we want to maximize `pre[i] + D(A[i+1..j])` for $0 \le i < j-1$ (ensuring the first subarray is non-empty, so $i \ge 1$ in 1-based, which means $i \ge 0$ in 0-based index for the split point before the middle segment starts? Let's stick to 0-based indexing for implementation).

Let's use 0-based indexing for the array $A[0 \dots N-1]$.
Split points are $i$ and $j$ such that the subarrays are $A[0 \dots i]$, $A[i+1 \dots j]$, $A[j+1 \dots N-1]$.
Constraints: $0 \le i < j \le N-2$.
Score: `pre[i] + D(A[i+1 \dots j]) + suf[j+1]`.
Here `pre[i]` is distinct count in $A[0 \dots i]$.
`suf[j+1]` is distinct count in $A[j+1 \dots N-1]$.

Let $f(j) = \max_{0 \le i \le j-1} (\text{pre}[i] + D(A[i+1 \dots j]))$.
Then the answer is $\max_{1 \le j \le N-2} (f(j) + \text{suf}[j+1])$. Note that $j$ must be at least 1 so that the first subarray $A[0 \dots i]$ can be non-empty (since $i \ge 0$). Also $j$ must be at most $N-2$ so the last subarray is non-empty.

To compute $f(j)$ efficiently:
Let $g(i, j) = D(A[i+1 \dots j])$.
When moving from $j$ to $j+1$, we consider the element $A[j+1]$.
Let $L$ be the last position of $A[j+1]$ before index $j+1$.
If $A[j+1]$ has not appeared before, $L = -1$.
The distinct count $D(A[i+1 \dots j+1])$ increases by 1 compared to $D(A[i+1 \dots j])$ if and only if $A[j+1]$ is NOT in $A[i+1 \dots j]$.
$A[j+1]$ is in $A[i+1 \dots j]$ if and only if $i+1 \le L \le j$, i.e., $i \le L-1$.
So, if $i \le L-1$, the count does not increase.
If $i \ge L$, the count increases by 1.
Wait, let's re-verify.
Range is $A[i+1 \dots j]$. We add $A[j+1]$.
If $A[j+1]$ is already in $A[i+1 \dots j]$, distinct count doesn't change.
$A[j+1]$ is in $A[i+1 \dots j]$ iff its last occurrence $L$ satisfies $i+1 \le L \le j$.
So if $i+1 \le L \implies i \le L-1$, then $A[j+1]$ is in the range.
If $i \ge L$, then $i+1 > L$, so the last occurrence $L$ is not in the range $A[i+1 \dots j]$. Thus $A[j+1]$ is new.
So:
$g(i, j+1) = g(i, j) + 1$ if $i \ge L$.
$g(i, j+1) = g(i, j)$ if $i < L$.

Therefore, the value $V_i(j) = \text{pre}[i] + g(i, j)$ updates as:
$V_i(j+1) = V_i(j) + 1$ if $i \ge L$.
$V_i(j+1) = V_i(j)$ if $i < L$.

We can maintain the values $V_i$ in a Segment Tree that supports range add and range max query.
Initially, for $j=0$ (middle segment empty? No, middle segment must be non-empty).
Let's start with $j=1$. The middle segment is $A[1 \dots 1]$.
$i$ can be $0$.
$V_0(1) = \text{pre}[0] + D(A[1 \dots 1]) = 1 + 1 = 2$.
We can initialize the segment tree for indices $i$ from $0$ to $N-2$.
For a general step $j$ (computing $f(j)$), we have updated the segment tree based on transitions from $j-1$ to $j$.
Actually, it's easier to iterate $j$ from $1$ to $N-2$.
Before processing $j$, the segment tree should contain $V_i(j)$ for all valid $i < j$.
Base case: $j=1$.
$i=0$. $V_0(1) = \text{pre}[0] + D(A[1 \dots 1])$.
We can build the initial state for $j=1$.
Then for each $j$, we query max over $i \in [0, j-1]$.
Then we prepare for $j+1$ by updating the segment tree: find $L = \text{last\_pos}[A[j+1]]$. Add 1 to range $[L, j]$. Note that $i$ goes up to $j$ for the next step?
For $f(j+1)$, we need max over $i \in [0, j]$.
The update rule applies to all $i$. Specifically, for $i \ge L$, $V_i$ increases by 1.
The range of $i$ we care about is $0 \dots N-2$.
When moving from $j$ to $j+1$, we add 1 to $V_i$ for all $i \in [L, j]$.
Why $[L, j]$? Because for $i > j$, $V_i$ is not yet defined/valid for the current middle segment ending at $j$. But we can initialize them to $-\infty$ or handle bounds.
Actually, we only query max over $0 \dots j-1$ for $f(j)$.
When moving to $j+1$, we need $V_i$ for $i \in 0 \dots j$.
The update affects $i \in [L, N-1]$ effectively, but we only care about $i \le j$.
So we update range $[L, j]$ by adding 1.
Then we insert $V_j(j+1)$?
$V_j(j+1) = \text{pre}[j] + D(A[j+1 \dots j+1]) = \text{pre}[j] + 1$.
This value $V_j$ is new for the next step. We can set it in the segment tree.

Algorithm:
1. Compute `pre` array. `pre[i]` = distinct in $A[0 \dots i]$.
2. Compute `suf` array. `suf[i]` = distinct in $A[i \dots N-1]$.
3. Initialize Segment Tree of size $N$.
4. `last_pos` map/array.
5. Base case $j=1$:
   - $i=0$: $V_0 = \text{pre}[0] + 1$.
   - Set `tree[0] = V_0`.
   - Query max for $j=1$: `max_val = tree.query(0, 0)`.
   - `ans = max_val + suf[2]`.
6. Loop $j$ from $1$ to $N-3$ (preparing for next $j' = j+1$):
   - Current middle end is $j$. Next middle end is $j+1$.
   - Element to add is $A[j+1]$.
   - Find $L = \text{last\_pos}[A[j+1]]$. If not present, $L = -1$.
   - Update range $[L, j]$ in segment tree: add 1. (Indices $i$ such that $i \ge L$).
     - Note: if $L < 0$, update $[0, j]$.
     - If $L > j$, update nothing (shouldn't happen as $L < j+1$).
   - Now the tree reflects $V_i(j+1)$ for $i \le j$.
   - We need to add the new candidate $i=j$ for the next step.
   - $V_j(j+1) = \text{pre}[j] + D(A[j+1 \dots j+1]) = \text{pre}[j] + 1$.
   - Update `tree[j] = V_j(j+1)`. (Note: previous value at $j$ was invalid or $-\infty$).
   - Now compute $f(j+1) = \text{tree.query}(0, j)$.
   - `ans = max(ans, f(j+1) + suf[j+2])`.
7. Print `ans`.

Corner cases: $N=3$.
$j$ ranges from $1$ to $1$.
Loop for $j$ from $1$ to $0$ doesn't run.
Base case handles $j=1$.
`ans = (pre[0]+1) + suf[2]`.
Correct.

Pitfalls:
- Segment tree implementation details (1-based vs 0-based indexing).
- Handling $L=-1$.
- Ensuring subarrays are non-empty.
  - First subarray $A[0 \dots i]$ non-empty $\implies i \ge 0$.
  - Middle subarray $A[i+1 \dots j]$ non-empty $\implies i < j$.
  - Last subarray $A[j+1 \dots N-1]$ non-empty $\implies j \le N-2$.
  - So $0 \le i \le j-1$ and $1 \le j \le N-2$.

## worker: Implement the Segment Tree with Range Add and Rang
The solution uses a Segment Tree with Range Add and Range Max Query to efficiently compute the maximum sum of distinct counts for the three subarrays.

1.  **Precomputation**: We compute `pre[i]` (distinct count in $A[0 \dots i]$) and `suf[i]` (distinct count in $A[i \dots N-1]$) in $O(N)$ time.
2.  **Segment Tree**: We maintain values $V_i(j) = \text{pre}[i] + D(A[i+1 \dots j])$ in a segment tree. The tree supports:
    *   **Range Add**: When moving from $j$ to $j+1$, if the new element $A[j+1]$ has its last occurrence at $L$, then for all $i \ge L$, the distinct count of the middle segment increases by 1. Thus, we add 1 to $V_i$ for all $i \in [L, j]$.
    *   **Point Update**: When moving to $j+1$, a new split point $i=j$ becomes available. We set $V_j(j+1) = \text{pre}[j] + 1$.
    *   **Range Max Query**: For each $j$, we query the maximum $V_i(j)$ for $0 \le i \le j-1$.
3.  **Complexity**: Each step involves $O(\log N)$ operations for the segment tree updates and queries. With $N$ steps, the total time complexity is $O(N \log N)$, which fits within the constraints for $N \le 3 \times 10^5$.
4.  **Edge Cases**: The code handles $N=3$ correctly via the base case and loop bounds. The segment tree is initialized with a very small number to represent invalid states.
