
## ideation
The core difficulty is efficiently determining, for each element $A_i$, the largest divisor $g$ of $A_i$ such that there are at least $K$ elements in the entire array $A$ divisible by $g$.

Key observations:
1. If a GCD value $g$ is achievable for a subset including $A_i$, then $g$ must divide $A_i$. Furthermore, there must be at least $K$ numbers in $A$ that are multiples of $g$.
2. We can precompute for every possible $g$ (from 1 to $10^6$) the count of numbers in $A$ that are divisible by $g$. Let's call this `count[g]`.
3. A value $g$ is "feasible" if `count[g] >= K`.
4. For each $A_i$, the answer is the largest divisor $d$ of $A_i$ such that `count[d] >= K`.

Algorithm steps:
1. Read input $N, K$ and array $A$.
2. Compute frequency of each number in $A$. Let `freq[x]` be the number of times $x$ appears in $A$.
3. For each $g$ from 1 to $MAX\_VAL$ ($10^6$), compute `count[g]` by summing `freq[m]` for all multiples $m = g, 2g, 3g, \dots \le MAX\_VAL$. This can be done in $O(MAX\_VAL \log MAX\_VAL)$ time using a harmonic series approach.
4. Identify all feasible $g$ values where `count[g] >= K`.
5. For each $A_i$, find its divisors and check which ones are feasible. Return the maximum feasible divisor.
   - To optimize, we can precompute the answer for each possible value $v$ (1 to $MAX\_VAL$) by finding the largest feasible divisor of $v$. Let `ans[v]` be this value.
   - Then for each $A_i$, the answer is simply `ans[A_i]`.
   - To compute `ans[v]` for all $v$:
     - Initialize `ans[v] = 1` for all $v$ (since 1 is always feasible if $K \le N$, which is given).
     - Iterate $g$ from $MAX\_VAL$ down to 1. If $g$ is feasible (`count[g] >= K`), then for all multiples $m = g, 2g, \dots$, we can potentially update `ans[m]` to be at least $g$. Since we iterate $g$ downwards, the first time we set `ans[m]` it will be the largest feasible divisor? No, that's not quite right because a multiple $m$ might have a larger feasible divisor that is not a multiple of $g$.
     - Better approach for step 5: For each $v$, iterate through its divisors. The number of divisors is small on average. For $10^6$, max divisors is 240 (for 720720). So iterating divisors for each $A_i$ is feasible.
     - Precompute divisors for all numbers up to $10^6$? Or compute on the fly? Computing on the fly for each $A_i$ using trial division up to $\sqrt{A_i}$ is $O(\sqrt{A_i})$ per element, total $O(N \sqrt{MAX\_VAL})$. With $N=1.2 \times 10^6$ and $\sqrt{MAX\_VAL}=1000$, this is $1.2 \times 10^9$ operations, which might be too slow for Python.
     - Alternative: Precompute the largest feasible divisor for each number $v \in [1, MAX\_VAL]$.
       - Let `best[v]` be the largest feasible divisor of $v$.
       - Initialize `best[v] = 1` for all $v$.
       - For each feasible $g$, update `best[m] = max(best[m], g)` for all multiples $m$ of $g$.
       - This is $O(MAX\_VAL \log MAX\_VAL)$ again.
       - Then answer for $A_i$ is `best[A_i]`.

This approach is efficient:
- Frequency count: $O(N)$
- Count multiples: $O(MAX\_VAL \log MAX\_VAL)$
- Update best: $O(MAX\_VAL \log MAX\_VAL)$
- Output: $O(N)$

Total time complexity: $O(N + MAX\_VAL \log MAX\_VAL)$, which is well within limits.

Pitfalls:
- Memory: Arrays of size $10^6$ are fine in Python.
- Time: Python might be slow with tight loops. Need to ensure the inner loops are efficient. Using list comprehensions or simple for loops with range steps is good.

## worker: Implement the solution in Python.
The solution efficiently solves the problem by leveraging the harmonic series property for counting multiples. Here's the breakdown:

1. **Frequency Count**: We first count how many times each number appears in the input array `A`. This takes $O(N)$ time.

2. **Count Multiples**: For each possible GCD value `g` from 1 to $10^6$, we compute how many elements in `A` are divisible by `g`. This is done by iterating through all multiples of `g` and summing their frequencies. The total time for this step is $O(MAX\_VAL \log MAX\_VAL)$ due to the harmonic series.

3. **Find Best Feasible Divisor**: For each number `v` from 1 to $10^6$, we want to find the largest divisor `g` of `v` such that at least `K` elements in `A` are divisible by `g`. We iterate `g` from $10^6$ down to 1. If `g` is feasible (i.e., `count[g] >= K`), we update `best[m] = g` for all multiples `m` of `g`. Since we iterate from largest to smallest, the first time we set `best[m]`, it will be the largest feasible divisor. This step also takes $O(MAX\_VAL \log MAX\_VAL)$ time.

4. **Output Results**: For each element `A_i`, the answer is simply `best[A_i]`. This takes $O(N)$ time.

The overall time complexity is $O(N + MAX\_VAL \log MAX\_VAL)$, which is efficient enough for the given constraints. The space complexity is $O(MAX\_VAL)$ for the frequency, count, and best arrays.
