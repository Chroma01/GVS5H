
## ideation
The core difficulty lies in efficiently determining, for each element $A_i$, the largest divisor $g$ of $A_i$ such that at least $K$ elements in the entire array $A$ are divisible by $g$.

1.  **Counting Multiples**: We can use a sieve-like method to count how many numbers in $A$ are divisible by each integer $g$ from 1 to $10^6$. Let `count[g]` be this number. This takes $O(M \log M)$ time where $M = 10^6$.
2.  **Querying for Each $A_i$**: For each $A_i$, we need to find $\max \{ g : g | A_i \text{ and } \text{count}[g] \ge K \}$.
    *   Iterating all divisors for each $A_i$ might be slow if done naively for $1.2 \times 10^6$ elements, although the number of divisors is small on average. The maximum number of divisors for a number $\le 10^6$ is 240 (for 720720). $1.2 \times 10^6 \times 240 \approx 2.88 \times 10^8$ operations, which might be tight for Python but feasible in C++. In Python, this could TLE.
    *   **Optimization**: Instead of finding divisors for each $A_i$ individually, we can precompute the answer for every possible value $v \in [1, 10^6]$. Let `ans[v]` be the maximum divisor $g$ of $v$ such that `count[g] >= K`.
    *   To compute `ans[v]` for all $v$:
        *   Initialize `ans[v] = 1` for all $v$.
        *   Iterate $g$ from $M$ down to 1. If `count[g] >= K`, then for all multiples $j \cdot g$ of $g$, we can potentially update `ans[j*g]` with $g$. Since we iterate $g$ from largest to smallest, the first time we visit a multiple $v$ via a divisor $g$, that $g$ is the largest valid divisor for $v$? No, that's not quite right because a larger divisor might not satisfy the count condition.
        *   Actually, if we iterate $g$ from $M$ down to 1, and if `count[g] >= K`, we can mark all multiples of $g$ as having at least $g$ as a candidate answer. Since we go from large $g$ to small, the first valid $g$ that divides $v$ is the maximum. So we can initialize `ans` array with 0. Iterate $g$ from $M$ down to 1. If `count[g] >= K`, then for all multiples $m = g, 2g, \dots \le M$, if `ans[m]` is not yet set, set `ans[m] = g`.
        *   This approach is $O(M \log M)$ because we iterate multiples for each valid $g$. In the worst case (all counts >= K), it's the same harmonic series sum. This is very efficient.

3.  **Pitfalls**:
    *   Memory usage: Arrays of size $10^6$ are fine.
    *   Time limit: Python might be slow with tight loops. Using efficient I/O and minimizing inner loop overhead is crucial. The nested loop `for m in range(g, M+1, g)` is efficient in Python if done correctly.
    *   Edge case: $K=1$. The answer is always $A_i$ itself because we can just pick $A_i$. The logic holds: `count[A_i] >= 1` is true, and since we iterate downwards, $A_i$ will be assigned to `ans[A_i]` before any smaller divisor.

4.  **Plan**:
    *   Read input.
    *   Compute frequency of each number in $A$.
    *   Compute `count[g]` for $g \in [1, 10^6]$ using sieve-like iteration over multiples.
    *   Initialize `ans` array of size $10^6+1$ with 0.
    *   Iterate $g$ from $10^6$ down to 1. If `count[g] >= K`, iterate through multiples $m$ of $g$. If `ans[m]` is 0, set `ans[m] = g`.
    *   For each $A_i$, print `ans[A_i]`.

## worker: Implement the frequency count and `count[g]` calcu
The solution follows the optimized plan:
1.  **Frequency Array**: We first count the occurrences of each number in the input array `A`. This takes $O(N)$ time.
2.  **Count Multiples**: We compute `count[g]`, which is the number of elements in `A` divisible by `g`. This is done using a sieve-like approach, iterating through multiples of each `g`. The complexity is $O(M \log M)$ where $M = 10^6$, due to the harmonic series sum $\sum_{g=1}^M \frac{M}{g} \approx M \log M$.
3.  **Determine Answers**: We initialize an `ans` array. We iterate `g` from $M$ down to 1. If `count[g] >= K`, it means `g` is a valid GCD candidate. For every multiple `m` of `g`, if `ans[m]` hasn't been set yet, we set `ans[m] = g`. Since we iterate `g` from largest to smallest, the first valid `g` that divides `m` is the maximum possible GCD for any number equal to `m`. This step also takes $O(M \log M)$ in the worst case (if all `count[g] >= K`), but typically much faster if few `g` satisfy the condition.
4.  **Output**: Finally, we look up the precomputed answer for each element in `A` and print them.

This approach is efficient enough for $N, M \le 10^6$ in Python, provided the inner loops are not too heavy. The use of `sys.stdin.read` and `sys.stdout.write` helps with I/O performance.
