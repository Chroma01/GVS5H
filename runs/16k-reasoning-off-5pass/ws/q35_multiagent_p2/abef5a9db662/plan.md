The key observation is that the final rating is $X + f(X)$, where $f(X)$ is the number of contests in which the rating was within $[L_i, R_i]$ at the time of the contest. However, the rating changes dynamically, so we cannot simply count static intervals. Instead, we can model the process as: for each contest $i$, if current rating $r \in [L_i, R_i]$, then $r \leftarrow r+1$. This is equivalent to saying that the rating increases by 1 for each contest where the "adjusted" rating falls in a certain range.

A better approach: Notice that the operation is monotonic. If we start with rating $X$, after all contests, the final rating is $X + k$, where $k$ is the number of contests that "triggered" an increase. The challenge is that whether a contest triggers depends on the current rating, which depends on previous triggers.

We can use the idea of "sweeping" or "difference arrays" with a clever transformation. Consider that each contest $i$ adds 1 to the rating if the current rating is in $[L_i, R_i]$. This is similar to a range update problem but sequential.

Actually, we can reverse the thinking: Let $g(X)$ be the final rating given initial rating $X$. We want to compute $g(X)$ for many $X$. Note that $g(X) = X + \text{count of } i \text{ such that during contest } i, \text{rating} \in [L_i, R_i]$.

An efficient solution uses the fact that the function $g(X)$ is piecewise linear with slope 1, and the "breakpoints" are limited. We can simulate the effect of all contests on a difference array. Specifically, we can use a sweep-line approach:

1. Create an array `diff` of size $500002$ (since max rating is $5 \times 10^5$ and it can increase by at most $N=2 \times 10^5$, so max final rating is $7 \times 10^5$, but we only need to track up to $5 \times 10^5 + 2 \times 10^5 = 700000$).
2. For each contest $[L_i, R_i]$, it will cause an increase if the current rating is in $[L_i, R_i]$. The effect of this is that for any initial $X$ such that the rating at contest $i$ is in $[L_i, R_i]$, we add 1.
3. We can process contests in order and maintain a data structure that tells us, for a given initial $X$, what the current rating is. But this is too slow per query.

Alternative efficient approach: Use a difference array to compute how many times each rating value "passes through" a contest interval. Actually, we can use the following trick:
- Let $A$ be an array where $A[r]$ represents the number of contests that have $L_i \leq r \leq R_i$ **if the rating were static**. But it's not static.

Correct approach: We can compute the final rating for all $X$ in $[1, 500000]$ using a sweep-line with a Fenwick tree or simply a difference array with prefix sums, processing contests in a specific order. However, there's a known technique for this problem:

1. Initialize an array `add` of zeros with size $500002$.
2. For each contest $[L_i, R_i]$, we want to mark that if the current rating is in $[L_i, R_i]$, it increases. The key insight is that the condition "current rating in $[L_i, R_i]$" for initial $X$ is equivalent to $X + \text{prefix\_increases}(X, i-1) \in [L_i, R_i]$, where $\text{prefix\_increases}(X, i-1)$ is the number of increases from contests $1$ to $i-1$ for initial $X$. This is circular.

Actually, the standard solution for this AtCoder problem (ABC 259 F or similar) uses the following:
- Create a difference array `D` of size $500002$.
- For each contest $[L, R]$, we do:
  - `D[L] += 1`
  - `D[R+1] -= 1`
- Then compute prefix sums of `D` to get `cnt[r]` = number of contests that cover rating $r$ **statically**.
- But this is incorrect because the rating changes.

Wait, the correct efficient solution is:
1. Let `f[r]` be the number of contests that have $L_i \leq r \leq R_i$. This is computed via difference array.
2. The final rating for initial $X$ is $X + f[X]$? No, because the rating changes.

Actually, I recall that for this specific problem, the answer is simply $X + \text{number of } i \text{ such that } L_i \leq X \leq R_i$ is **wrong** as seen in Sample 1.

Let me re-read Sample 1:
- Contest 1: [1,5]. X=3 -> 4.
- Contest 2: [1,3]. Rating=4, not in [1,3] -> 4.
- Contest 3: [3,6]. Rating=4, in [3,6] -> 5.
- Contest 4: [2,4]. Rating=5, not in [2,4] -> 5.
- Contest 5: [4,7]. Rating=5, in [4,7] -> 6.

So for X=3, answer is 6. Static count for X=3: Contests 1,2,3 cover 3. So static count is 3, but answer is 6=3+3. Wait, 3+3=6. Let's check X=2:
- Contest 1: [1,5], 2->3.
- Contest 2: [1,3], 3->4.
- Contest 3: [3,6], 4->5.
- Contest 4: [2,4], 5 not in [2,4] -> 5.
- Contest 5: [4,7], 5->6.
Answer 6. Static count for X=2: Contests 1,2,4 cover 2. Count=3. 2+3=5 != 6. So static count is wrong.

The correct approach is to use a segment tree or Fenwick tree to simulate the process for all X simultaneously, or use the fact that the function is monotonic and use binary search. However, given constraints, we can use a difference array approach with a twist:

Actually, the intended solution is:
1. Compute an array `C` where `C[r]` is the number of contests with $L_i \leq r \leq R_i$. This is done with a difference array.
2. The final rating is NOT $X + C[X]$.

After research, the correct method is to use a sweep-line with a Fenwick tree to count how many contests are "active" at each step, but this is complex.

Simpler correct approach:
- We can compute the final rating for all $X$ in $[1, 500000]$ by processing contests in order and maintaining a difference array that tracks the "shift".
- Let `D` be a difference array of size $500002$.
- For each contest $[L, R]$, we want to add 1 to all $X$ such that the current rating of $X$ is in $[L, R]$.
- This can be done by maintaining a variable `shift` and using a Fenwick tree to query the number of shifts.

Given time, I'll implement a solution using a Fenwick tree to simulate the process for all queries efficiently.