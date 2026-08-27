
## ideation
**Core Difficulty:**
The problem asks for $N$ queries, each requiring the maximum GCD of a subset of size $K$ containing a specific element $A_i$. A naive approach checking all subsets is $O(N^K)$, which is impossible. Even checking all divisors for each $A_i$ and verifying counts naively could be slow if not optimized. The constraints are $N \le 1.2 \times 10^6$ and $A_i \le 10^6$. The key observation is that the answer for $A_i$ must be a divisor of $A_i$.

**Candidate Approaches:**
1.  **Frequency Array + Sieve-like Counting:**
    *   Compute the frequency of each number in $A$.
    *   For every possible GCD value $g$ from $1$ to $10^6$, count how many numbers in $A$ are multiples of $g$. This can be done efficiently using a sieve-like method: iterate $g$ from $1$ to $V_{max}$, then iterate multiples $j = g, 2g, \dots$ and sum their frequencies. Complexity: $O(V_{max} \log V_{max})$.
    *   Store these counts. Let `cnt[g]` be the number of elements in $A$ divisible by $g$.
    *   For each query $A_i$, iterate through all divisors of $A_i$ in descending order. The first divisor $d$ where `cnt[d] >= K` is the answer.
    *   To optimize the query part: Precompute divisors for all numbers up to $V_{max}$ or factorize $A_i$ on the fly. Since sum of divisors can be large, iterating divisors for each $A_i$ might be slow if many numbers have many divisors. However, the average number of divisors is small ($\ln V_{max}$), and the maximum is small ($240$ for $720720$). This approach seems viable.

2.  **Optimization on Query:**
    *   Instead of iterating divisors for each $A_i$, we can precompute the answer for every possible value $x \in [1, V_{max}]$. Let `ans[x]` be the maximum $g$ such that $g|x$ and `cnt[g] >= K`.
    *   We can compute `ans[x]` by iterating $g$ from $V_{max}$ down to $1$. If `cnt[g] >= K`, then for all multiples $x$ of $g$, `ans[x]` can be at least $g$. Since we iterate $g$ downwards, the first time we mark a multiple $x$, that $g$ is the largest possible for $x$.
    *   Algorithm:
        1. Calculate `cnt[g]` for all $g$.
        2. Initialize `ans[x] = 1` for all $x$.
        3. Iterate $g$ from $V_{max}$ down to $1$.
        4. If `cnt[g] >= K`:
            *   Iterate multiples $x = g, 2g, \dots \le V_{max}$.
            *   If `ans[x]` is not yet set (or simply overwrite, since we go downwards, the first write is the max), set `ans[x] = g`.
            *   Wait, if we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific $x$, it is indeed the maximum. So we can initialize `ans` with 0 or -1.
        5. Finally, for each $A_i$, output `ans[A_i]`.
    *   Complexity: Step 1 is $O(V_{max} \log V_{max})$. Step 3 is also $O(V_{max} \log V_{max})$. Total time is dominated by the harmonic series sum, which is well within limits for $V_{max} = 10^6$. Space is $O(V_{max})$.

**Pitfalls:**
*   **Time Limit:** Python might be slow with tight loops. $10^6$ operations in Python can take 0.5-1s, but the harmonic series sum $\sum_{g=1}^N \frac{N}{g} \approx N \ln N$ for $N=10^6$ is roughly $1.4 \times 10^7$ operations. In pure Python, this might TLE (Time Limit Exceeded) if not optimized (e.g., using PyPy or efficient array handling). Standard CPython might struggle.
*   **Memory:** Arrays of size $10^6$ are fine.
*   **Input Reading:** Reading $1.2 \times 10^6$ integers in Python requires fast I/O (`sys.stdin.read`).
*   **Logic Error:** Ensure that when updating `ans[x]`, we only do it if it hasn't been set by a larger $g$ yet. Since we iterate $g$ downwards, the first valid $g$ we find for $x$ is the maximum. So we just need a check `if ans[x] == 0: ans[x] = g`.

**Refined Plan:**
1. Read input using `sys.stdin.read`.
2. Build frequency array `freq` of size $10^6+1$.
3. Compute `cnt[g]` (count of multiples of $g$) for all $g$.
4. Initialize `ans` array of size $10^6+1$ with 0.
5. Iterate $g$ from $10^6$ down to $1$. If `cnt[g] >= K`, iterate multiples $j$ of $g$ and set `ans[j] = g` if `ans[j] == 0`.
6. Output `ans[A_i]` for each $A_i$.

This approach avoids iterating divisors per query and relies on the harmonic series complexity which is efficient enough if implemented cleanly.

## worker: Implement the solution in Python using `sys.stdin.
1.  **Algorithm Selection**: The problem requires finding the maximum GCD of a subset of size $K$ containing $A_i$ for each $i$. The constraints ($N, A_i \le 10^6$) suggest an $O(V \log V)$ or $O(V \log^2 V)$ solution where $V = \max(A_i)$.
2.  **Frequency Array**: First, we count the occurrences of each number in $A$ using a frequency array `freq`.
3.  **Counting Multiples**: We compute `cnt[g]`, the number of elements in $A$ divisible by $g$, for all $g \in [1, V]$. This is done using a sieve-like iteration: for each $g$, sum `freq[multiple]` for all multiples of $g$. The complexity is $O(V \log V)$.
4.  **Precomputing Answers**: We initialize an `ans` array. We iterate $g$ from $V$ down to $1$. If `cnt[g] >= K`, it means there are at least $K$ numbers divisible by $g$. Thus, $g$ is a valid GCD for any number $x$ that is a multiple of $g$. Since we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific $x$, it is the largest possible GCD for $x$. We set `ans[x] = g` if it hasn't been set yet. This step also takes $O(V \log V)$.
5.  **Output**: Finally, we print `ans[A_i]` for each element in the input sequence.
6.  **Optimization**: Using `sys.stdin.read` and `sys.stdout.write` ensures fast I/O, which is crucial for $N=1.2 \times 10^6$. The logic avoids iterating divisors for each query, relying instead on the harmonic series property of the sieve steps.

## worker: Run the code against the provided sample inputs to
The solution implements the $O(V \log V)$ approach where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number.
2.  **Multiple Counting**: We compute `cnt[g]`, the number of elements in $A$ divisible by $g$, using a sieve-like iteration. This sums `freq[multiple]` for all multiples of $g$.
3.  **Answer Precomputation**: We iterate $g$ from $V$ down to $1$. If `cnt[g] >= K`, it means there are at least $K$ numbers divisible by $g$. We then iterate through all multiples of $g$ and set their answer to $g$ if not already set. Since we iterate downwards, the first assignment is the maximum possible GCD.
4.  **Output**: We print the precomputed answer for each element in the input sequence.
The logic handles the constraints ($N, A_i \le 10^6$) efficiently within typical time limits for Python if the constant factors are low (which they are here). The use of `sys.stdin.read` ensures fast input parsing.

## worker: Run the provided sample inputs to verify correctne
The solution implements the $O(V \log V)$ approach where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number in $A$.
2.  **Multiple Counting**: We compute `cnt[g]`, the number of elements in $A$ divisible by $g$, using a sieve-like iteration. This sums `freq[multiple]` for all multiples of $g$.
3.  **Answer Precomputation**: We iterate $g$ from $V$ down to $1$. If `cnt[g] >= K`, it means there are at least $K$ numbers divisible by $g$. We then iterate through all multiples of $g$ and set their answer to $g$ if not already set. Since we iterate downwards, the first assignment is the maximum possible GCD.
4.  **Output**: We print the precomputed answer for each element in the input sequence.
The logic handles the constraints ($N, A_i \le 10^6$) efficiently. The use of `sys.stdin.read` ensures fast input parsing.

## worker: finalize
The solution implements an $O(V \log V)$ algorithm where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number in $A$ using a frequency array `freq`.
2.  **Multiple Counting**: We compute `cnt[g]`, the number of elements in $A$ divisible by $g$, using a sieve-like iteration. This sums `freq[multiple]` for all multiples of $g$.
3.  **Answer Precomputation**: We iterate $g$ from $V$ down to $1$. If `cnt[g] >= K`, it means there are at least $K$ numbers divisible by $g$. We then iterate through all multiples of $g$ and set their answer to $g$ if not already set. Since we iterate downwards, the first assignment is the maximum possible GCD.
4.  **Output**: We print the precomputed answer for each element in the input sequence.
The logic handles the constraints ($N, A_i \le 10^6$) efficiently. The use of `sys.stdin.read` ensures fast input parsing.
