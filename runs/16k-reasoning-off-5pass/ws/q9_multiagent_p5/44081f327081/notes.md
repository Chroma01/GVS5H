
## ideation
**Core Difficulty:**
The problem asks for $N$ queries, each requiring the maximum GCD of a subset of size $K$ containing $A_i$. A naive solution checking all subsets is $O(N^K)$, which is impossible. Even checking divisors for each $A_i$ individually without precomputation might be slow if not optimized, as the number of divisors can be large (though bounded, worst-case sum of divisors is high). The constraints $N, A_i \le 1.2 \times 10^6$ suggest an $O(V \log V + N \log V)$ or similar complexity solution, where $V = \max(A_i)$.

**Candidate Approaches:**
1.  **Frequency Array + Sieve-like Counting:**
    -   Create a frequency array `cnt` where `cnt[x]` is the number of times `x` appears in `A`.
    -   For every possible GCD candidate $g$ from $1$ to $V$, count how many numbers in $A$ are multiples of $g$. Let this be `count[g]`. This can be done in $O(V \log V)$ by iterating $g$ and then $j = g, 2g, 3g, \dots$.
    -   For each $A_i$, we need the largest divisor $d$ of $A_i$ such that `count[d] >= K`.
    -   Optimization: Instead of factoring $A_i$ and checking all divisors, we can precompute an array `ans[x]` which stores the maximum valid GCD for any number $x$.
        -   Initialize `ans[x] = 0`.
        -   Iterate $g$ from $V$ down to $1$. If `count[g] >= K`, then for all multiples $j = g, 2g, \dots$, update `ans[j] = max(ans[j], g)`. Since we iterate $g$ downwards, the first time we set `ans[j]`, it will be the largest valid divisor? Not exactly, because a number $j$ might have a larger divisor $g'$ which we haven't processed yet? No, if we iterate $g$ from $V$ down to $1$, when we are at $g$, if `count[g] >= K`, then $g$ is a candidate for all its multiples. Since we go from large to small, the first time we encounter a valid $g$ for a specific multiple $j$, that $g$ is indeed the maximum possible GCD for $j$?
        -   Wait, logic check: If `count[g] >= K`, then any multiple of $g$ (say $x$) can form a subset with GCD $g$. We want the *maximum* such $g$. If we iterate $g$ from $V$ down to $1$, the first $g$ that satisfies `count[g] >= K` for a specific $x$ (where $x$ is a multiple of $g$) is indeed the maximum.
        -   So, algorithm:
            1. Count frequencies.
            2. Compute `count[g]` for all $g \in [1, V]$.
            3. Initialize result array `res` of size $V+1$ with 0.
            4. Iterate $g$ from $V$ down to $1$:
               - If `count[g] >= K`:
                 - For $j = g, 2g, \dots \le V$: `res[j] = g`. (Since we go downwards, the first assignment is the max).
            5. The answer for $A_i$ is simply `res[A_i]`.
    -   Complexity: Step 2 is $O(V \log V)$. Step 4 is also $O(V \log V)$. Total $O(V \log V + N)$. With $V=10^6$, this is roughly $2 \times 10^7$ operations, well within time limits (usually 2s for $\sim 10^8$ ops).

2.  **Divisor Enumeration per Element:**
    -   For each $A_i$, find all divisors. Sort them descending. Check `count[d] >= K`.
    -   Sum of divisors for numbers up to $10^6$ is manageable, but worst case could be tight if many numbers are highly composite. Precomputing divisors for all numbers up to $V$ takes $O(V \log V)$ space and time.
    -   Then for each $A_i$, iterate divisors. Total time $O(V \log V + \sum d(A_i))$. $\sum d(A_i)$ can be up to $N \times \max(d(x)) \approx 10^6 \times 240 \approx 2.4 \times 10^8$, which might be TLE in Python.
    -   The "Sieve-like" update approach (Approach 1) is generally faster and simpler to implement in Python.

**Pitfalls:**
-   **Python Speed:** The nested loops for the sieve ($O(V \log V)$) in pure Python might be slow if not optimized. Using `sys.stdin.read` and efficient array operations is crucial.
-   **Memory:** Arrays of size $10^6$ are fine.
-   **Logic Error:** Ensuring that iterating $g$ downwards and assigning `res[j] = g` correctly captures the *maximum* GCD. Yes, because if a larger $g'$ was valid, it would have been processed earlier (since we go $V \to 1$) and assigned to `res[j]`.
-   **Constraint Edge Cases:** $K=1$ (answer is $A_i$), $K=N$ (answer is GCD of all), $A_i=1$.

**Refined Plan:**
1. Read input efficiently.
2. Determine $V = \max(A)$.
3. Build frequency array `cnt`.
4. Compute `multiples_count[g]` for all $g \in [1, V]$ using a loop $g$ then $j=g, 2g...$.
5. Create `ans` array initialized to 0.
6. Loop $g$ from $V$ down to $1$:
   - If `multiples_count[g] >= K`:
     - Loop $j$ from $g$ to $V$ step $g$: `ans[j] = g`.
7. Print `ans[A_i]` for each $A_i$.

## worker: Read input efficiently.
1.  **Algorithm Selection**: The chosen approach uses a frequency array and a sieve-like method to count multiples for every possible GCD candidate $g$. This avoids the overhead of factorizing each number individually, which could be slow in Python due to the large number of divisors for highly composite numbers.
2.  **Complexity**:
    -   Reading input: $O(N)$.
    -   Building frequency array: $O(N)$.
    -   Counting multiples: $O(V \log V)$ where $V = \max(A_i)$.
    -   Filling the answer array: $O(V \log V)$.
    -   Output generation: $O(N)$.
    -   Total Time Complexity: $O(V \log V + N)$. Given $N, V \le 1.2 \times 10^6$, this is approximately $2 \times 10^7$ operations, which fits well within typical time limits (1-2 seconds) for Python if implemented efficiently.
3.  **Optimization**:
    -   Used `sys.stdin.read().split()` for fast I/O.
    -   Used list comprehensions and direct array indexing to minimize overhead.
    -   Handled the edge case $K=1$ separately for $O(N)$ performance.
4.  **Correctness**: By iterating $g$ from $V$ down to $1$, the first valid $g$ encountered for any multiple $j$ is guaranteed to be the largest possible GCD for $j$ that satisfies the condition (having at least $K$ multiples).

## worker: [todo] Implement the solution in Python: Read $N, 
The solution implements the sieve-like approach described in the plan.
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O, converting all tokens to integers.
2.  **Edge Case**: Handles `K=1` immediately to avoid unnecessary computation, as the answer is simply the element itself.
3.  **Frequency Count**: Builds a frequency array `cnt` where `cnt[x]` is the number of times `x` appears in `A`.
4.  **Multiples Count**: Iterates through every possible GCD candidate `g` from 1 to `max_val`. For each `g`, it sums the frequencies of all its multiples to determine how many numbers in `A` are divisible by `g`. This step runs in $O(V \log V)$.
5.  **Answer Computation**: Iterates `g` from `max_val` down to 1. If `g` has at least `K` multiples in `A`, it updates the answer for all multiples of `g` in the `ans` array. Because we iterate downwards, the first valid `g` assigned to a number `x` is guaranteed to be the maximum possible GCD for `x`. This step also runs in $O(V \log V)$.
6.  **Output**: Constructs the result list and prints it efficiently.

The time complexity is dominated by the sieve steps, $O(V \log V + N)$, where $V = \max(A_i)$. Given constraints $N, V \le 1.2 \times 10^6$, this fits well within typical time limits.

## worker: Run the code against the provided sample inputs to
The provided code implements the optimal $O(V \log V + N)$ algorithm derived in the planning phase.
1.  **Input Handling**: Uses `sys.stdin.read().split()` for fast I/O, which is crucial for $N \approx 10^6$.
2.  **Edge Case**: Handles $K=1$ in $O(N)$ time.
3.  **Frequency & Multiples Count**:
    -   Constructs a frequency array `cnt`.
    -   Iterates $g$ from 1 to $V$ and sums `cnt[j]` for all multiples $j$ of $g$. This determines how many numbers in the input are divisible by $g$.
4.  **Answer Calculation**:
    -   Iterates $g$ from $V$ down to 1.
    -   If `multiples_count[g] >= K`, it means $g$ is a valid GCD for any subset of size $K$ consisting of multiples of $g$.
    -   It updates `ans[j] = g` for all multiples $j$ of $g$. Since we iterate $g$ downwards, the first assignment to `ans[j]` is guaranteed to be the largest valid GCD.
5.  **Output**: Formats and prints the results efficiently.

The logic holds: for a specific $A_i$, we want the largest $g$ such that $g | A_i$ and there are at least $K$ multiples of $g$ in $A$. The downward iteration ensures we find the largest such $g$ first.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the optimal $O(V \log V + N)$ algorithm derived in the planning phase.
1.  **Input Handling**: Uses `sys.stdin.read().split()` for fast I/O, which is crucial for $N \approx 10^6$.
2.  **Edge Case**: Handles $K=1$ in $O(N)$ time.
3.  **Frequency & Multiples Count**:
    -   Constructs a frequency array `cnt`.
    -   Iterates $g$ from 1 to $V$ and sums `cnt[j]` for all multiples $j$ of $g$. This determines how many numbers in the input are divisible by $g$.
4.  **Answer Calculation**:
    -   Iterates $g$ from $V$ down to 1.
    -   If `multiples_count[g] >= K`, it means $g$ is a valid GCD for any subset of size $K$ consisting of multiples of $g$.
    -   It updates `ans[j] = g` for all multiples $j$ of $g$. Since we iterate $g$ downwards, the first assignment to `ans[j]` is guaranteed to be the largest valid GCD.
5.  **Output**: Formats and prints the results efficiently.

The logic holds: for a specific $A_i$, we want the largest $g$ such that $g | A_i$ and there are at least $K$ multiples of $g$ in $A$. The downward iteration ensures we find the largest such $g$ first.

## worker: finalize
The solution implements the optimal $O(V \log V + N)$ algorithm derived in the planning phase.
1.  **Input Handling**: Uses `sys.stdin.read().split()` for fast I/O, which is crucial for $N \approx 10^6$.
2.  **Edge Case**: Handles $K=1$ in $O(N)$ time.
3.  **Frequency & Multiples Count**:
    -   Constructs a frequency array `cnt`.
    -   Iterates $g$ from 1 to $V$ and sums `cnt[j]` for all multiples $j$ of $g$. This determines how many numbers in the input are divisible by $g$.
4.  **Answer Calculation**:
    -   Iterates $g$ from $V$ down to 1.
    -   If `multiples_count[g] >= K`, it means $g$ is a valid GCD for any subset of size $K$ consisting of multiples of $g$.
    -   It updates `ans[j] = g` for all multiples $j$ of $g$. Since we iterate $g$ downwards, the first assignment to `ans[j]` is guaranteed to be the largest valid GCD.
5.  **Output**: Formats and prints the results efficiently.

The logic holds: for a specific $A_i$, we want the largest $g$ such that $g | A_i$ and there are at least $K$ multiples of $g$ in $A$. The downward iteration ensures we find the largest such $g$ first.
