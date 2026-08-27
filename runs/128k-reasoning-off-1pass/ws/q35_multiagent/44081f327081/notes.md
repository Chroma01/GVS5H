
## ideation
The core difficulty is efficiently finding, for each element $A_i$, the largest divisor $d$ of $A_i$ such that there are at least $K$ elements in the array $A$ divisible by $d$.

Key observations:
1. If a GCD value $g$ is achievable for a group including $A_i$, then $g$ must divide $A_i$, and there must be at least $K$ elements in $A$ that are multiples of $g$.
2. We can precompute `count[g]` = number of elements in $A$ divisible by $g$ for all $g$ from 1 to $M = \max(A)$. This can be done efficiently using a sieve-like approach: for each $g$, iterate through multiples $g, 2g, 3g, \dots$ and sum up the frequencies of those values in $A$.
3. For each $A_i$, we need to find the largest divisor $d$ of $A_i$ such that `count[d] >= K`.
4. Since $A_i \leq 10^6$, we can precompute divisors for all numbers up to $10^6$, or compute them on the fly. Given $N$ up to $1.2 \times 10^6$, we need an efficient way to find the answer for each $A_i$.
5. Alternative approach: For each $g$ from $M$ down to 1, if `count[g] >= K`, then $g$ is a candidate answer for all $A_i$ that are multiples of $g$. But we need the *largest* such $g$ for each $A_i$. We can use a "sweep" approach: initialize `ans[v] = 0` for all $v$. For $g$ from $M$ down to 1, if `count[g] >= K`, then for all multiples $v = g, 2g, 3g, \dots$, if `ans[v]` is not yet set, set `ans[v] = g`. This works because we process $g$ in decreasing order, so the first time we set `ans[v]`, it's the largest valid $g$ dividing $v$.

This sweep approach is efficient: the total number of operations is $\sum_{g=1}^{M} \frac{M}{g} = O(M \log M)$, which is feasible for $M = 10^6$.

Pitfalls:
- The sieve-like counting must be done correctly.
- The sweep must process $g$ from largest to smallest.
- Need to handle the case where no $g > 1$ works (answer is 1, which always works since `count[1] = N >= K`).

## worker: (None)
The solution uses a sieve-like approach to efficiently solve the problem:

1. **Frequency counting**: We first count how many times each number appears in the input array.

2. **Counting multiples**: For each possible GCD value `g` from 1 to `max(A)`, we count how many elements in the array are divisible by `g`. This is done by iterating through all multiples of `g` and summing their frequencies. The total complexity is O(M log M) where M = max(A) ≤ 10^6.

3. **Finding the best GCD for each value**: We iterate `g` from `max_A` down to 1. For each `g` where at least `K` elements are divisible by `g`, we mark all multiples of `g` as having `g` as their answer (if not already marked). Since we process from largest to smallest, the first time we mark a value, it's with the largest valid GCD. This also takes O(M log M) total time.

4. **Output**: For each element A_i, we look up `ans[A_i]` which gives the maximum GCD achievable when A_i is included in a group of K elements.

The overall time complexity is O(M log M + N) where M = max(A) and N is the array length, which fits within the constraints.
