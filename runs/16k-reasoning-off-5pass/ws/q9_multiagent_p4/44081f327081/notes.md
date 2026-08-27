
## ideation
**Core Difficulty**:
The problem asks for $N$ queries, each requiring the maximum GCD of a subset of size $K$ containing a specific element $A_i$.
- Naive approach: For each $i$, iterate all subsets of size $K$ containing $A_i$ (impossible, $N$ is up to $1.2 \times 10^6$).
- Even iterating multiples: If we fix $A_i$, we need to find the largest $g$ such that $g | A_i$ and there are at least $K-1$ other multiples of $g$ in the array.
- Constraints: $N, \max(A_i) \le 1.2 \times 10^6$. An $O(N \sqrt{N})$ or $O(N \cdot \text{something large})$ per query is too slow. We need something close to $O(V \log V + N)$ where $V = \max(A_i)$.

**Candidate Approaches**:
1.  **Frequency Array + Sieve-like Counting**:
    -   Create a frequency array `cnt` where `cnt[x]` is the number of times `x` appears in $A$.
    -   For every possible GCD value $g$ from $1$ to $V$, calculate `total_multiples[g]`, which is the count of numbers in $A$ divisible by $g$. This can be done efficiently:
        ```python
        for g in range(1, V+1):
            count = 0
            for multiple in range(g, V+1, g):
                count += cnt[multiple]
            total_multiples[g] = count
        ```
        Complexity: $O(V \log V)$ (harmonic series). With $V=10^6$, this is approx $1.4 \times 10^7$ operations, which is fast.
    -   **Answering Queries**: For a specific $A_i$, we need the largest $g$ such that:
        1.  $g$ divides $A_i$.
        2.  `total_multiples[g]` $\ge K$.
    -   To answer this quickly for all $i$:
        -   Instead of checking divisors for each $A_i$ (which could be slow if many divisors), we can precompute an array `ans[g]` = "Is $g$ a valid GCD for some subset of size $K$?" (i.e., `total_multiples[g] >= K`).
        -   However, we need the *maximum* such $g$ for each $A_i$.
        -   Optimization: Let `max_valid[g]` be the largest integer $x \le g$ such that `total_multiples[x] >= K`. We can compute this using a suffix maximum scan: `max_valid[g] = g if total_multiples[g] >= K else max_valid[g-1]`.
        -   For a query $A_i$, the answer is simply the largest divisor of $A_i$ that is $\le$ `max_valid[A_i]`? No, that's not quite right.
        -   Correct Logic: The answer for $A_i$ is the largest $g$ such that $g | A_i$ AND `total_multiples[g] >= K`.
        -   Since we have `total_multiples` precomputed, we can just check all divisors of $A_i$. The number of divisors for numbers up to $10^6$ is small (max 240 for 720720). $240 \times 1.2 \times 10^6 \approx 2.8 \times 10^8$, which might be slightly tight for Python (usually limit is $10^8$ ops/sec, time limit often 2s).
        -   Better Optimization: We can precompute `best[g]` = the largest multiple of $g$ that is $\le V$ and satisfies the condition? No.
        -   Alternative: Iterate $g$ from $V$ down to 1. If `total_multiples[g] >= K`, then for all multiples $m$ of $g$, $g$ is a candidate. We want the largest such $g$ for each $m$.
        -   Let `res[m]` store the answer for value $m$. Initialize `res` with 0 or 1.
        -   Iterate $g$ from $V$ down to 1:
            -   If `total_multiples[g] >= K`:
                -   For every multiple $m$ of $g$ ($m = g, 2g, \dots$):
                    -   `res[m] = max(res[m], g)`
        -   Complexity: Still $O(V \log V)$ because the inner loop runs $V/g$ times. Sum of $V/g$ is $V \log V$.
        -   This approach fills `res[x]` with the largest valid $g$ that divides $x$.
        -   Finally, for each $A_i$, output `res[A_i]`.
        -   Total Complexity: $O(V \log V + N)$. This is optimal and safe for Python.

2.  **Pitfalls**:
    -   **Python Speed**: Loops in Python can be slow. $1.4 \times 10^7$ iterations for the sieve part is fine, but doing nested loops for the "filling `res`" part needs to be efficient.
    -   The "filling `res`" part:
        ```python
        for g in range(V, 0, -1):
            if total_multiples[g] >= K:
                for m in range(g, V+1, g):
                    res[m] = g
        ```
        This is exactly $O(V \log V)$. In C++, this is trivial. In Python, $1.4 \times 10^7$ simple assignments might take 1-2 seconds. We need to ensure the inner loop is as fast as possible.
    -   **Edge Cases**: $K=1$ (answer is $A_i$), $K=N$, all $A_i$ same.
    -   **Memory**: Arrays of size $10^6$ are fine.

**Refined Plan**:
1.  Read $N, K$ and array $A$.
2.  Compute frequency array `cnt` for values in $A$.
3.  Compute `total_multiples[g]` for $g \in [1, V]$ using a harmonic loop.
4.  Initialize `ans` array of size $V+1$ with 0 (or 1, since GCD $\ge 1$).
5.  Iterate $g$ from $V$ down to 1:
    -   If `total_multiples[g] >= K`:
        -   Update `ans` for all multiples of $g$.
        -   *Optimization*: Since we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific multiple $m$, that is the largest possible $g$ for $m$. We can stop updating for a specific $m$ once it's set? No, we iterate $g$, so we naturally find larger $g$ first. But we still iterate all multiples.
        -   Actually, we can optimize: We only care about updating `ans[m]` if it hasn't been set yet? No, we want the largest. Since we go $V \to 1$, the first valid $g$ we hit for a multiple $m$ is the largest. So we can skip if `ans[m]` is already set?
        -   Wait, the loop structure is:
            ```python
            ans = [0]*(V+1)
            for g in range(V, 0, -1):
                if total_multiples[g] >= K:
                    for m in range(g, V+1, g):
                        if ans[m] == 0: # If not set yet, set it
                             ans[m] = g
            ```
            Does this work? Yes. Because we process $g$ from largest to smallest. The first time we see a multiple $m$ that is valid, it must be via the largest possible $g$.
            However, checking `if ans[m] == 0` inside the inner loop adds a branch. In C++ this is negligible. In Python, function calls or complex logic slow things down.
            Is there a way to avoid the `if`?
            Actually, the standard loop `for m in range(g, V+1, g): ans[m] = g` overwrites with smaller $g$ if we don't check. But we want the *largest*.
            If we iterate $g$ from $V$ down to 1, and we do `ans[m] = g`, then later (smaller $g$) we overwrite it. That's wrong.
            So we MUST check `if ans[m] == 0`.
            Can we optimize the inner loop?
            Maybe not strictly necessary if $V=10^6$. $1.4 \times 10^7$ iterations with a simple check is likely acceptable in PyPy, maybe risky in CPython.
            Let's reconsider the logic.
            We need `ans[x]` = max $g$ such that $g|x$ and count($g$) $\ge K$.
            Alternative: For each $x$, find its divisors. Sort divisors descending. Check count. First one that satisfies is the answer.
            Precomputing divisors for all numbers up to $10^6$ takes memory and time.
            Generating divisors on the fly for each $A_i$:
            Max divisors = 240. $N = 1.2 \times 10^6$. Total checks = $2.8 \times 10^8$. Too slow for Python.
            
            Back to the sieve method.
            Is there a way to do the update faster?
            We can use a "difference array" or similar? No, it's a max query over divisors.
            
            Let's trust the $O(V \log V)$ with the `if` check.
            Wait, if `ans[m]` is already set, we skip.
            The number of times `ans[m]` is set is exactly 1 (when the largest valid $g$ is processed).
            The number of times we *visit* `m` in the inner loop is $\sum_{g: g|m} 1 = d(m)$.
            So the total number of iterations is $\sum_{m=1}^V d(m) \approx V \ln V$.
            The `if` check happens $V \ln V$ times. The assignment happens $V$ times (at most).
            So complexity is dominated by the loop overhead.
            $1.4 \times 10^7$ iterations. In Python, a simple loop with an `if` might take 2-3 seconds.
            Is there a faster way?
            
            What if we don't iterate $g$ downwards?
            What if we compute `ans` differently?
            For each $g$ where `total_multiples[g] >= K`, we mark all its multiples.
            We want the largest $g$.
            This is equivalent to: `ans[x] = max { g | g divides x AND total_multiples[g] >= K }`.
            
            Maybe we can optimize the Python code by using list comprehensions or slicing?
            `ans[g::g]` creates a slice.
            If we have a boolean array `valid[g]` (True if `total_multiples[g] >= K`), we can do:
            For each $g$ where `valid[g]` is True:
               `ans[g::g] = [g] * len(ans[g::g])` ?
               No, because we want the *largest* $g$. If we process $g$ from $V$ down to 1, the first assignment to a slice overwrites previous (smaller) values? No, we want to keep the largest.
               If we process $V \to 1$, and we do `ans[g::g] = g`, we are overwriting with smaller values.
               So we should process $1 \to V$?
               If $1 \to V$:
               For $g=1$: `ans[1::1] = 1`. All become 1.
               For $g=2$: `ans[2::2] = 2`. Multiples of 2 become 2.
               ...
               For $g=V$: `ans[V::V] = V`.
               This works! The last assignment (largest $g$) wins.
               And we only update if `valid[g]` is True.
               So:
               ```python
               ans = [0] * (V + 1)
               for g in range(1, V + 1):
                   if total_multiples[g] >= K:
                       # Assign g to all multiples of g
                       # But we need to be careful not to overwrite with smaller g if we process in increasing order?
                       # Wait. If we process 1, then 2, then 3...
                       # Multiples of 2 get set to 2.
                       # Multiples of 4 get set to 4.
                       # Multiples of 6 get set to 6.
                       # If 6 is valid, ans[6] becomes 6.
                       # If 3 is valid, ans[6] becomes 3. (Overwrites 6).
                       # We want the MAXIMUM.
                       # So if we process in INCREASING order, the LAST valid divisor sets the value.
                       # But we want the largest divisor.
                       # So if we process 1..V, the value at index m will be the largest valid divisor processed SO FAR?
                       # No.
                       # Example: m=6. Divisors: 1, 2, 3, 6.
                       # g=1: ans[6]=1.
                       # g=2: ans[6]=2.
                       # g=3: ans[6]=3.
                       # g=6: ans[6]=6.
                       # Result: 6. Correct.
                       # So increasing order works perfectly. The last valid g encountered is the largest.
               ```
               This avoids the `if ans[m] == 0` check inside the loop!
               We just blindly assign.
               However, `ans[g::g] = [g] * count` creates a new list of size $V/g$.
               Total memory allocation: $\sum V/g = V \ln V$.
               This involves creating many lists. In Python, list creation has overhead.
               But it might be faster than a Python `for` loop with `if`.
               Actually, `ans[g::g] = [g] * ((V - g) // g + 1)` is very fast in CPython because the assignment is done in C.
               Let's verify the logic again.
               We want `ans[m] = max(g)` such that `g|m` and `valid[g]`.
               If we iterate $g$ from 1 to $V$:
               When we are at $g$, we set `ans[m] = g` for all multiples $m$.
               Since $g$ increases, if $m$ has multiple valid divisors, the larger one will overwrite the smaller one later.
               Example: $m=12$, valid divisors $\{1, 2, 3, 4, 6, 12\}$.
               $g=1 \to ans[12]=1$
               $g=2 \to ans[12]=2$
               $g=3 \to ans[12]=3$
               $g=4 \to ans[12]=4$
               $g=6 \to ans[12]=6$
               $g=12 \to ans[12]=12$
               Final: 12. Correct.
               
               What if $g=12$ is NOT valid?
               Then at $g=12$, we do nothing.
               $ans[12]$ remains 6. Correct.
               
               So the algorithm:
               1. `cnt` array.
               2. `total_multiples` array (sieve).
               3. `ans` array initialized to 0.
               4. Loop $g$ from 1 to $V$:
                  If `total_multiples[g] >= K`:
                      `ans[g::g] = [g] * len(ans[g::g])`
               5. Print `ans[A_i]` for each $i$.
               
               Complexity:
               - Sieve: $O(V \log V)$.
               - Assignment loop: $\sum_{g=1}^V (V/g) = O(V \log V)$.
               - List creation overhead: Creating a list of size $L$ takes $O(L)$. Total time $O(V \log V)$.
               - This should be very fast in Python because the inner operations are in C (slice assignment).
               
               One detail: `len(ans[g::g])` is `(V - g) // g + 1`.
               We can compute this directly.
               
               This seems to be the optimal Python approach.

## worker: Implement the solution using `sys.stdin`. Compute 
1.  **Algorithm Selection**: The problem requires finding the maximum GCD of a subset of size $K$ containing $A_i$. The constraints ($N, A_i \le 1.2 \times 10^6$) suggest an approach better than $O(N \cdot \sqrt{A_i})$ or $O(N \cdot \text{divisors})$.
2.  **Frequency & Sieve**: We first count the frequency of each number. Then, for every possible GCD value $g$, we count how many numbers in the array are multiples of $g$. This is done efficiently in $O(V \log V)$ where $V = \max(A)$.
3.  **Optimization**: Instead of checking divisors for each $A_i$ (which could be slow), we precompute the answer for every possible value $x \in [1, V]$. We iterate $g$ from 1 to $V$. If $g$ is a valid GCD (i.e., there are at least $K$ multiples of $g$ in the array), we update the answer for all multiples of $g$.
4.  **Slice Assignment**: To efficiently update multiples of $g$, we use Python's slice assignment `ans[g::g] = [g] * count`. Since we iterate $g$ in increasing order, the last valid $g$ that divides a number $x$ will overwrite any previous smaller valid $g$, ensuring `ans[x]` holds the maximum valid GCD. This leverages C-level optimizations for list slicing and assignment, keeping the complexity within limits for Python.
5.  **Complexity**: The sieve part takes $O(V \log V)$. The update part also takes $O(V \log V)$ due to the harmonic series sum of slice lengths. Total time complexity is $O(V \log V + N)$, which fits well within the time limits for $V=10^6$.

## worker: Run the code against the provided sample inputs to
The solution implements the $O(V \log V)$ approach where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number in $A$.
2.  **Sieve for Multiples**: For each potential GCD $g$, we count how many numbers in $A$ are multiples of $g$. This is done by iterating $g$ from 1 to $V$ and summing `cnt[multiple]` for `multiple = g, 2g, ...`.
3.  **Greedy Assignment**: We initialize an `ans` array. We iterate $g$ from 1 to $V$. If $g$ is a valid GCD (i.e., count $\ge K$), we update `ans` for all multiples of $g$. By iterating $g$ in increasing order, if a number $x$ has multiple valid divisors, the largest one will overwrite the smaller ones in `ans[x]`.
4.  **Optimization**: Instead of a Python loop to update multiples, we use slice assignment `ans[g::g] = [g] * length`. This leverages C-level optimizations for list slicing and assignment, significantly speeding up the process compared to a manual loop in Python.
5.  **Output**: Finally, we map each $A_i$ to its precomputed answer `ans[A_i]`.

The complexity is dominated by the harmonic series summation, resulting in $O(V \log V + N)$, which fits well within the time limits for $V, N \le 1.2 \times 10^6$.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the $O(V \log V)$ approach where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number in $A$.
2.  **Sieve for Multiples**: For each potential GCD $g$, we count how many numbers in $A$ are multiples of $g$. This is done by iterating $g$ from 1 to $V$ and summing `cnt[multiple]` for `multiple = g, 2g, ...`.
3.  **Greedy Assignment**: We initialize an `ans` array. We iterate $g$ from 1 to $V$. If $g$ is a valid GCD (i.e., count $\ge K$), we update `ans` for all multiples of $g$. By iterating $g$ in increasing order, if a number $x$ has multiple valid divisors, the largest one will overwrite the smaller ones in `ans[x]`.
4.  **Optimization**: Instead of a Python loop to update multiples, we use slice assignment `ans[g::g] = [g] * length`. This leverages C-level optimizations for list slicing and assignment, significantly speeding up the process compared to a manual loop in Python.
5.  **Output**: Finally, we map each $A_i$ to its precomputed answer `ans[A_i]`.

The complexity is dominated by the harmonic series summation, resulting in $O(V \log V + N)$, which fits well within the time limits for $V, N \le 1.2 \times 10^6$.

## worker: finalize
The solution implements an $O(V \log V + N)$ approach where $V = \max(A_i)$.
1.  **Frequency Count**: We first count occurrences of each number in $A$.
2.  **Sieve for Multiples**: For each potential GCD $g$, we count how many numbers in $A$ are multiples of $g$. This is done by iterating $g$ from 1 to $V$ and summing `cnt[multiple]` for `multiple = g, 2g, ...`.
3.  **Greedy Assignment**: We initialize an `ans` array. We iterate $g$ from 1 to $V$. If $g$ is a valid GCD (i.e., count $\ge K$), we update `ans` for all multiples of $g$. By iterating $g$ in increasing order, if a number $x$ has multiple valid divisors, the largest one will overwrite the smaller ones in `ans[x]`.
4.  **Optimization**: Instead of a Python loop to update multiples, we use slice assignment `ans[g::g] = [g] * length`. This leverages C-level optimizations for list slicing and assignment, significantly speeding up the process compared to a manual loop in Python.
5.  **Output**: Finally, we map each $A_i$ to its precomputed answer `ans[A_i]`.

The complexity is dominated by the harmonic series summation, resulting in $O(V \log V + N)$, which fits well within the time limits for $V, N \le 1.2 \times 10^6$.
