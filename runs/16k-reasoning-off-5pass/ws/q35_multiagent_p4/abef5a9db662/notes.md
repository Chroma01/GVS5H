
## ideation
The problem asks us to compute the final rating for various initial ratings $X$ after $N$ contests. In each contest $i$, if the current rating is in $[L_i, R_i]$, it increases by 1.

A naive simulation for each query would take $O(N)$ per query, leading to $O(NQ)$ total time, which is too slow given $N, Q \le 3 \times 10^5$.

However, notice that the rating only increases. More importantly, the condition for increasing depends *only* on the current rating value. The key insight is that the total increase for a starting rating $X$ is simply the number of intervals $[L_i, R_i]$ that contain $X$. Why? Because the rating only increases, and the intervals are fixed. Wait, does the rating change affect subsequent intervals?
Let's re-read carefully: "if his rating is between $L_i$ and $R_i$ ... his rating increases by 1".
The rating *changes* during the process. So if the rating starts at $X$, after the first contest, it might become $X+1$ or stay $X$. This means the rating entering the second contest depends on the first. Therefore, we cannot simply count how many intervals contain the *initial* $X$. The path matters.

However, let's look at the monotonicity. If you start with a higher rating, you will always have a rating $\ge$ the rating of someone starting lower at every step. Specifically, if $X_1 < X_2$, then after any number of contests, $R_1 \le R_2$.
This implies that the function $F(X) = \text{final rating given initial } X$ is non-decreasing.
But more strongly, is it true that $F(X) = X + \text{count of intervals containing } X$? No, because the rating changes.

Let's trace Sample 1:
Intervals: [1,5], [1,3], [3,6], [2,4], [4,7]
Query X=3:
1. Rating 3 in [1,5]? Yes. Rating becomes 4.
2. Rating 4 in [1,3]? No. Rating stays 4.
3. Rating 4 in [3,6]? Yes. Rating becomes 5.
4. Rating 5 in [2,4]? No. Rating stays 5.
5. Rating 5 in [4,7]? Yes. Rating becomes 6.
Final: 6.

If we just counted intervals containing 3:
[1,5] contains 3? Yes.
[1,3] contains 3? Yes.
[3,6] contains 3? Yes.
[2,4] contains 3? Yes.
[4,7] contains 3? No.
Count = 4. $3+4=7 \neq 6$. So the simple count is wrong.

The state space is small: ratings are between 1 and $5 \times 10^5$. The maximum possible rating increase is $N = 2 \times 10^5$. So the maximum rating we might see is $5 \times 10^5 + 2 \times 10^5 = 7 \times 10^5$. This is still small enough to simulate all possible starting ratings?
We can compute $F(X)$ for all $X$ from 1 to $MAX\_X$ efficiently.
Let $dp[r]$ be the final rating if the current rating is $r$ and there are no more contests. This is trivial: $dp[r] = r$.
But we process contests sequentially.
Let $f_k(r)$ be the rating after contest $k$ given that the rating before contest $k$ was $r$.
$f_k(r) = r + 1$ if $L_k \le r \le R_k$, else $r$.
We want to compute $F(X) = f_N(f_{N-1}(...f_1(X)...))$.

Since the domain of ratings is small (up to ~700,000), we can maintain an array `current_rating` where `current_rating[r]` stores the final rating if the rating *before the current set of processed contests* was $r$.
Initially, `current_rating[r] = r` for all $r$.
For each contest $[L, R]$:
For each $r$ in $[L, R]$, `current_rating[r]` becomes `current_rating[r] + 1`.
Wait, this is $O(N \cdot \text{range})$ which is too slow.

However, notice that `current_rating[r]` is always $r + \text{increase}(r)$.
Let $I(r)$ be the total increase for a starting rating $r$.
When we process a contest $[L, R]$, for any $r \in [L, R]$, the rating *at the time of this contest* must be checked. But the rating at the time of this contest depends on previous contests.
Let $r_{before}$ be the rating before this contest. If $L \le r_{before} \le R$, then $r_{after} = r_{before} + 1$.
This looks like we need to track the mapping from initial $X$ to current rating.
Let $M_k$ be a mapping/array such that $M_k[X]$ is the rating after contest $k$ given initial $X$.
$M_0[X] = X$.
$M_k[X] = M_{k-1}[X] + 1$ if $L_k \le M_{k-1}[X] \le R_k$, else $M_{k-1}[X]$.

Since $N$ is large, we can't iterate all $X$ for each contest.
But notice that $M_k[X]$ is a non-decreasing function of $X$.
Also, the values in $M_k$ are contiguous integers with no gaps? Not necessarily, but they are sorted.
Actually, since $M_{k-1}$ is non-decreasing, the condition $L_k \le M_{k-1}[X] \le R_k$ defines a contiguous range of $X$'s (possibly empty).
Let $S_k = \{ X \mid L_k \le M_{k-1}[X] \le R_k \}$. Since $M_{k-1}$ is non-decreasing, $S_k$ is an interval $[A_k, B_k]$.
For $X \in [A_k, B_k]$, $M_k[X] = M_{k-1}[X] + 1$.
For $X \notin [A_k, B_k]$, $M_k[X] = M_{k-1}[X]$.

So, we can maintain the array $M$ (or just the difference array of increases).
Let $D[X] = M[X] - X$. Initially $D[X] = 0$.
When we add 1 to $M[X]$ for $X \in [A, B]$, we are adding 1 to $D[X]$ for $X \in [A, B]$.
So we need to find the range $[A, B]$ such that $L \le M_{old}[X] \le R$.
Since $M_{old}[X] = X + D_{old}[X]$, and $D_{old}$ is non-decreasing?
Is $D[X]$ non-decreasing?
$M[X]$ is non-decreasing. $M[X] - X$ is not necessarily non-decreasing.
Example: $M[1]=2, M[2]=2$. $D[1]=1, D[2]=0$. Decreasing.
So we can't assume $D$ is sorted.

However, we can use a Segment Tree or a similar structure to maintain the function $M(X)$.
We need to support:
1. Find the smallest $X$ such that $M(X) \ge L$.
2. Find the largest $X$ such that $M(X) \le R$.
3. Add 1 to $M(X)$ for all $X$ in that range.

Since $M(X)$ is non-decreasing, we can binary search for the range $[A, B]$ using the segment tree.
Then we perform a range add update on the segment tree.
The segment tree will store the value $M(X)$ for each leaf $X$.
The maximum value of $X$ is $500,000$. The maximum rating can go up to $700,000$.
We can build a segment tree over the domain of initial ratings $1 \dots 500,000$.
Each node in the segment tree can store the minimum and maximum value of $M(X)$ in its range.
To find $A$: binary search for the first $X$ where $M(X) \ge L$.
To find $B$: binary search for the last $X$ where $M(X) \le R$.
Then range add 1 to $[A, B]$.

Complexity: $N$ updates. Each update involves two binary searches on the segment tree ($O(\log^2 (\text{max\_X}))$ or $O(\log (\text{max\_X}))$ with descent) and one range update ($O(\log (\text{max\_X}))$).
Total time: $O(N \log (\text{max\_X}))$. With $\text{max\_X} = 5 \times 10^5$, this is roughly $5 \times 10^5 \times 19 \approx 10^7$ operations, which is well within the time limit.

Steps:
1. Initialize a segment tree for range $1 \dots 500000$. Each leaf $i$ has value $i$. Internal nodes store min/max of children.
2. For each contest $[L, R]$:
   a. Find the smallest index $A$ such that $tree.query(A) \ge L$.
   b. Find the largest index $B$ such that $tree.query(B) \le R$.
   c. If $A \le B$, perform range add 1 on $[A, B]$.
3. After all contests, for each query $X$, output $tree.query(X)$.

Pitfalls:
- The binary search for $A$ and $B$ must be done correctly on the segment tree.
- The range of initial ratings is $1 \dots 500,000$. We should size the segment tree accordingly.
- Lazy propagation is needed for efficient range updates.

## worker: Range Add
The problem requires simulating a process where a rating changes based on intervals. A naive simulation per query is $O(NQ)$, which is too slow.
Key insight: The mapping from initial rating $X$ to current rating $R(X)$ is non-decreasing. This allows us to use a Segment Tree to maintain the function $R(X)$ for all $X \in [1, 500000]$.
The segment tree supports:
1. Range Add: When a contest $[L, R]$ occurs, we need to increment $R(X)$ by 1 for all $X$ such that $L \le R(X) \le R$.
2. Finding the range $[A, B]$ of initial ratings $X$ that satisfy $L \le R(X) \le R$. Since $R(X)$ is non-decreasing, the set of such $X$ forms a contiguous interval (possibly empty). We can find $A$ as the first index where $R(X) \ge L$ and $B$ as the last index where $R(X) \le R$ using binary search on the segment tree.
3. The segment tree stores min and max values in each node to facilitate the binary search descent. Lazy propagation ensures range updates are efficient.
Complexity: Building the tree is $O(MAX\_X)$. Each of the $N$ contests involves two binary searches ($O(\log MAX\_X)$) and one range update ($O(\log MAX\_X)$). Each query is $O(\log MAX\_X)$. Total time is $O((N+Q) \log MAX\_X)$, which fits within the limits.
