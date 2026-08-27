The key observation is that the final rating depends on how many contests cause an increase. A contest $i$ increases the rating if the current rating $r$ satisfies $L_i \le r \le R_i$. Since the rating only increases, the set of contests that trigger an increase for a starting rating $X$ is not trivially independent because the rating changes during the process. However, note that the condition for contest $i$ depends on the *current* rating at the time of the contest.

Let's reframe: We start with rating $X$. We process contests $1$ to $N$ in order. For each contest, if $L_i \le \text{current\_rating} \le R_i$, we increment the rating. We need to find the final rating for $Q$ different starting values $X$.

Since $N, Q$ are up to $2 \cdot 10^5$ and $3 \cdot 10^5$, and the rating range is up to $5 \cdot 10^5 + N \approx 7 \cdot 10^5$, we cannot simulate each query individually ($O(NQ)$ is too slow).

However, notice that the function $f(X) = \text{final rating given start } X$ is monotonic and "close" to $X + N$. Specifically, if we start with a higher rating, we might trigger more or fewer contests? Actually, if you start higher, you might exceed some $R_i$ and miss an increase, or you might be within more ranges. But generally, the behavior is complex.

Alternative approach: The maximum possible rating is $5 \cdot 10^5 + 2 \cdot 10^5 = 7 \cdot 10^5$. The minimum is $1$. We can precompute the result for all possible starting ratings in the range $[1, 5 \cdot 10^5]$. Let $M = 500000$. We can simulate the process for all $X \in [1, M]$ simultaneously? No, that's $O(M \cdot N)$ which is too slow.

Better approach: Notice that the transitions are piecewise linear. Or, we can use the fact that the rating only increases. Let's consider the difference between starting at $X$ and $X+1$. If we start at $X+1$, at any step, the rating is either equal to or 1 greater than the rating if we started at $X$ (since increments are +1). Let $r_X(t)$ be the rating after $t$ contests starting from $X$. Then $r_{X+1}(t) \ge r_X(t)$. In fact, $r_{X+1}(t) - r_X(t)$ is either 0 or 1? Not necessarily, it can grow. But wait, if $r_{X+1}(t) > r_X(t) + 1$, that would imply a divergence. However, since each contest adds at most 1, the difference can grow by at most 1 per contest. But actually, if $r_X(t) < L_i$, then $r_{X+1}(t)$ might be in $[L_i, R_i]$ while $r_X(t)$ is not, causing $r_{X+1}$ to increase and $r_X$ not, increasing the gap. Conversely, if $r_X(t) \le R_i$ and $r_{X+1}(t) > R_i$, then $r_X$ increases and $r_{X+1}$ doesn't, decreasing the gap.

Actually, there is a simpler observation: The final rating is $X + \text{count of contests where the rating was in } [L_i, R_i]$.
Let's define $g(X)$ as the number of increases. We want $X + g(X)$.
We can compute $g(X)$ for all $X$ using a sweep-line or difference array technique if the condition was static, but it's dynamic.

Wait, look at the constraints: Max rating is $5 \cdot 10^5$. Max initial $X$ is $5 \cdot 10^5$. Max final rating is $7 \cdot 10^5$.
We can simulate the process for ALL possible starting ratings in parallel?
Let $dp[v]$ be the number of times a rating of $v$ is "used" to trigger an increase? No.

Let's try this: Let $A[v]$ be the number of contests where the rating $v$ causes an increase. But the rating changes.
However, note that if we start at $X$, the rating at step $i$ is $X + (\text{number of increases in steps } 1 \dots i-1)$.
This looks like we can compute the answer for all $X$ in $O(N + M)$ or $O((N+M) \log M)$ where $M$ is the max rating.

Consider the function $h_i(X) = $ rating after contest $i$ starting from $X$.
$h_0(X) = X$.
$h_i(X) = h_{i-1}(X) + 1$ if $L_i \le h_{i-1}(X) \le R_i$, else $h_{i-1}(X)$.

Since $h_{i-1}(X)$ is a non-decreasing function of $X$, the condition $L_i \le h_{i-1}(X) \le R_i$ defines an interval of $X$ values for which the rating increases. Because $h_{i-1}$ is non-decreasing, the set of $X$ such that $h_{i-1}(X) \in [L_i, R_i]$ is an interval (possibly empty). Let this interval be $[A_i, B_i]$. Then for $X \in [A_i, B_i]$, the rating increases by 1, otherwise it stays same.
So, $h_i(X) = h_{i-1}(X) + 1$ if $X \in [A_i, B_i]$, else $h_{i-1}(X)$.
This means $h_i(X)$ is obtained by adding 1 to $h_{i-1}(X)$ on the interval $[A_i, B_i]$.

We can maintain the function $h(X)$ as a piecewise linear function or simply an array since the domain is small ($1 \dots 500000$).
Initially $h(X) = X$.
For each contest $i$, we need to find the interval $[A_i, B_i]$ such that $L_i \le h_{i-1}(X) \le R_i$.
Since $h_{i-1}$ is non-decreasing, we can find $A_i$ as the smallest $X$ such that $h_{i-1}(X) \ge L_i$, and $B_i$ as the largest $X$ such that $h_{i-1}(X) \le R_i$.
We can use binary search (specifically `bisect_left` and `bisect_right`) on the array $h$ to find these indices.
Then we add 1 to $h(X)$ for all $X \in [A_i, B_i]$. This is a range add operation.
We can use a difference array or a Fenwick tree / Segment Tree to handle range adds and point queries. Since we need the final values, a difference array is sufficient if we do all updates first? No, the updates depend on the current state of $h$. We must process contests sequentially.
So for each contest, we:
1. Query the current $h$ array to find $A_i, B_i$ via binary search.
2. Perform a range add of +1 on $[A_i, B_i]$ in $h$.

To support point query and range add efficiently, we can use a Fenwick tree (BIT) or Segment Tree. The array size is $M=500000$.
Operations:
- Binary search on $h$: We need to query values of $h$. With a BIT, point query is $O(\log M)$. Binary search takes $O(\log M \cdot \log M)$ or $O(\log M)$ if we walk the tree.
- Range add: $O(\log M)$.

Total time: $N \cdot (\log M + \log M) = O(N \log M)$. With $N=2 \cdot 10^5, M=5 \cdot 10^5$, this is roughly $2 \cdot 10^5 \cdot 19 \approx 4 \cdot 10^6$ operations, which is well within time limits.

Steps:
1. Initialize a data structure representing $h(X) = X$ for $X \in [1, M]$. We can use a BIT for range updates and point queries. Note that initial values are not zero. We can store $h(X) - X$ in the BIT, initially all 0. Then $h(X) = X + \text{query}(X)$.
2. For each contest $(L_i, R_i)$:
   a. Find smallest $A_i$ such that $h(A_i) \ge L_i$. Since $h$ is non-decreasing, we can binary search over $X \in [1, M]$.
   b. Find largest $B_i$ such that $h(B_i) \le R_i$. Similarly binary search.
   c. If $A_i \le B_i$, perform range add +1 on $[A_i, B_i]$ in the BIT.
3. After processing all contests, for each query $X$, output $X + \text{query}(X)$.

Note: The max rating can exceed $M$. The queries are only for $X \in [1, M]$. The intermediate ratings can go up to $M+N$. The binary search for $A_i, B_i$ should be over the domain of starting ratings $[1, M]$. The condition $h(X) \ge L_i$ is checked for $X \in [1, M]$.