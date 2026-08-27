
## ideation
**Core Difficulty**: The problem asks to count the number of 3-term arithmetic progressions (fine triplets) within a given set of $N$ distinct integers. A naive $O(N^2)$ approach (checking every pair or every middle element against all others) will time out given $N \le 10^6$.

**Candidate Approaches**:
1.  **Iterate Common Difference ($d$)**: Since the values $S_i$ are bounded by $M = 10^6$, we can iterate over all possible common differences $d$ ($1 \le d \le M/2$). For each $d$, we check if there exist $A$ such that $A, A+d, A+2d$ are all present in the set.
    *   **Complexity**: The number of triplets $(A, A+d, A+2d)$ to check for a fixed $d$ is roughly $M/d$. Summing over all $d$, the total complexity is $O(M \log M)$ (harmonic series). With $M=10^6$, this is approximately $1.4 \times 10^7$ operations, which fits comfortably within typical time limits (1-2 seconds).
    *   **Implementation**: Use a boolean array (or bitset) for $O(1)$ existence checks.

2.  **Sort and Two Pointers (Per Middle Element)**: Sort the array. For each element $B$, try to find pairs $(A, C)$ such that $A+C=2B$. Using two pointers for each $B$ takes $O(N^2)$ in the worst case (e.g., if $S$ is dense), which is too slow.

3.  **FFT (Fast Fourier Transform)**: Can be used to count pairs summing to a specific value, but it's overkill ($O(M \log M)$) and harder to implement correctly for this specific "distinct elements" constraint compared to the simple iteration method. Also, standard FFT counts pairs, handling the $A < B < C$ constraint requires care.

## worker: Read $N$ and the list $S$, then create a boolean a
The problem asks for the number of arithmetic progressions of length 3 within a set of distinct integers $S$. The constraints are $N \le 10^6$ and $S_i \le 10^6$.
A naive $O(N^2)$ solution checking every triplet or every pair is too slow.
The optimal approach leverages the small range of values ($S_i \le 10^6$). We iterate over all possible common differences $d$. For a fixed $d$, we check if there exists an $A$ such that $A, A+d, A+2d$ are all present in $S$.
The complexity is $\sum_{d=1}^{M/2} \frac{M}{d} \approx M \ln M$, where $M = 10^6$. This results in approximately $1.4 \times 10^7$ operations, which fits within the time limit.
We use a boolean array `present` for $O(1)$ lookups.
The input reading is handled efficiently using `sys.stdin.read().split()`.

## worker: Run the code against the provided sample inputs to
1.  **Algorithm Selection**: The problem asks for the number of 3-term arithmetic progressions in a set $S$. Given the constraints $N \le 10^6$ and $S_i \le 10^6$, an $O(N^2)$ approach is too slow. The optimal approach leverages the small range of values ($M = 10^6$). By iterating over all possible common differences $d$ (from $1$ to $M/2$) and checking for the existence of $A, A+d, A+2d$ in $O(1)$ using a boolean array, the total complexity becomes $O(M \log M)$ due to the harmonic series sum $\sum_{d=1}^{M/2} \frac{M}{d} \approx M \ln M$. With $M=10^6$, this results in roughly $1.4 \times 10^7$ operations, which fits within the time limit.
2.  **Input Handling**: Used `sys.stdin.read().split()` for fast I/O, which is crucial for large inputs in Python.
3.  **Edge Cases**: The code handles cases where $N$ is small or the input ends prematurely (though constraints guarantee valid input). The loop bounds ensure we don't access out-of-bounds indices.
4.  **Correctness**: The logic directly implements the definition of a fine triplet ($B-A = C-B \implies A+C=2B$) by fixing the difference $d$ and checking the existence of the sequence $A, A+d, A+2d$. Since elements are distinct, each valid triplet is counted exactly once.

## worker: Run the provided sample inputs to verify the outpu
The provided solution implements the $O(M \log M)$ algorithm where $M$ is the maximum value in $S$ ($10^6$).
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O handling of large inputs.
2.  **Presence Check**: Uses a boolean array `present` of size $10^6 + 2$ to allow $O(1)$ checks for existence of numbers.
3.  **Algorithm**: Iterates through all possible common differences $d$ from $1$ to $M/2$. For each $d$, it iterates through all valid starting values $A$ such that $A, A+d, A+2d$ are within the range $[1, M]$. If all three numbers exist in the set, it increments the answer counter.
4.  **Complexity**: The inner loop runs $M/d$ times. The total complexity is $\sum_{d=1}^{M/2} \frac{M}{d} \approx M \ln M$. For $M=10^6$, this is roughly $1.4 \times 10^7$ operations, which is well within the typical 2-second time limit for Python.
5.  **Verification**: The logic correctly counts triplets $(A, B, C)$ where $B-A = C-B$ (i.e., $A, B, C$ form an arithmetic progression) and $A < B < C$ is implicitly satisfied by the iteration order ($A < A+d < A+2d$) and distinctness of elements.

## worker: Run the code against Sample 1: Input `5\n8 3 1 5 2
The solution implements an $O(M \log M)$ algorithm where $M$ is the maximum value in the input set ($10^6$).
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O handling of large inputs.
2.  **Presence Check**: Uses a boolean array `present` of size $10^6 + 2$ to allow $O(1)$ checks for existence of numbers.
3.  **Algorithm**: Iterates through all possible common differences $d$ from $1$ to $M/2$. For each $d$, it iterates through all valid starting values $A$ such that $A, A+d, A+2d$ are within the range $[1, M]$. If all three numbers exist in the set, it increments the answer counter.
4.  **Complexity**: The inner loop runs $M/d$ times. The total complexity is $\sum_{d=1}^{M/2} \frac{M}{d} \approx M \ln M$. For $M=10^6$, this is roughly $1.4 \times 10^7$ operations, which is well within the typical 2-second time limit for Python.
5.  **Verification**: The logic correctly counts triplets $(A, B, C)$ where $B-A = C-B$ (i.e., $A, B, C$ form an arithmetic progression) and $A < B < C$ is implicitly satisfied by the iteration order ($A < A+d < A+2d$) and distinctness of elements.

## worker: finalize
The solution implements an $O(M \log M)$ algorithm where $M$ is the maximum value in the input set ($10^6$).
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O handling of large inputs.
2.  **Presence Check**: Uses a boolean array `present` of size $10^6 + 2$ to allow $O(1)$ checks for existence of numbers.
3.  **Algorithm**: Iterates through all possible common differences $d$ from $1$ to $M/2$. For each $d$, it iterates through all valid starting values $A$ such that $A, A+d, A+2d$ are within the range $[1, M]$. If all three numbers exist in the set, it increments the answer counter.
4.  **Complexity**: The inner loop runs $M/d$ times. The total complexity is $\sum_{d=1}^{M/2} \frac{M}{d} \approx M \ln M$. For $M=10^6$, this is roughly $1.4 \times 10^7$ operations, which is well within the typical 2-second time limit for Python.
5.  **Verification**: The logic correctly counts triplets $(A, B, C)$ where $B-A = C-B$ (i.e., $A, B, C$ form an arithmetic progression) and $A < B < C$ is implicitly satisfied by the iteration order ($A < A+d < A+2d$) and distinctness of elements.
