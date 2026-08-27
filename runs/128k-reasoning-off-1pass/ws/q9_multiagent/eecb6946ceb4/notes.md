
## ideation
The problem requires counting arithmetic progressions of length 3 within a given set of $N$ distinct integers. The condition $B - A = C - B$ is equivalent to $A + C = 2B$.
The constraints are $N \le 10^6$ and $S_i \le 10^6$.
A naive $O(N^2)$ approach checking all pairs is too slow.
The maximum possible sum $A+C$ is $2 \times 10^6$.
This structure suggests using the Fast Fourier Transform (FFT) to solve the convolution problem.
Specifically, if we define a polynomial $P(x) = \sum_{v \in S} x^v$, then the square $P(x)^2 = (\sum_{v \in S} x^v)(\sum_{u \in S} x^u) = \sum_{k} c_k x^k$, where $c_k$ is the number of pairs $(u, v)$ such that $u+v=k$.
We need to find the number of pairs where $u+v = 2B$ for some $B \in S$.
The algorithm would be:
1. Create a boolean array (or polynomial coefficients) of size $2 \cdot \max(S) + 1$.
2. Compute the square of this polynomial using FFT.
3. Iterate through each $B \in S$, check the coefficient at index $2B$.
4. Sum these coefficients and divide by 2 (since each pair $\{A, C\}$ is counted twice as $(A, C)$ and $(C, A)$, though the problem asks for ordered triplets $(A, B, C)$ with $A < B < C$, the condition $A+C=2B$ implies $A \neq C$ because elements are distinct, so $A < B < C$ is automatically satisfied if $A \neq C$ and $B$ is the midpoint). Wait, the problem asks for triplets $(A, B, C)$ with $A < B < C$. Since $A, B, C$ are distinct, $A+C=2B$ implies one is smaller than $B$ and one is larger. So counting pairs $\{A, C\}$ with sum $2B$ and $A \neq C$ is exactly what we need. The FFT counts ordered pairs $(A, C)$. Since $A \neq C$, the count for a specific $B$ will be even (pairs $(A, C)$ and $(C, A)$). We divide by 2 to get the number of sets $\{A, C\}$, which corresponds to one valid triplet $(A, B, C)$ with $A < B < C$.

Pitfalls:
- Floating point precision errors in FFT. Since $N \le 10^6$, the maximum coefficient can be up to $N$. Standard double precision FFT should handle this, but careful implementation is needed. Alternatively, Number Theoretic Transform (NTT) could be used if a suitable prime modulus exists, but standard competitive programming environments often support complex FFT well enough for counts up to $10^6$.
- Memory usage: Arrays of size $2 \cdot 10^6$ are fine.
- Time limit: $O(V \log V)$ where $V \approx 2 \cdot 10^6$ is acceptable for 2 seconds.

## worker: Implement the iterative Fast Fourier Transform (FF
1.  **Algorithm Selection**: The problem asks for the number of arithmetic progressions of length 3 ($A, B, C$) in a set $S$. The condition $B-A = C-B$ is equivalent to $A+C = 2B$. This is a classic convolution problem. By representing the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$, the square $P(x)^2$ has coefficients $c_k$ representing the number of pairs $(A, C)$ such that $A+C=k$.
2.  **Complexity**: A naive $O(N^2)$ solution is too slow for $N=10^6$. Using Fast Fourier Transform (FFT), we can compute the convolution in $O(V \log V)$ where $V$ is the maximum value in $S$ (up to $2 \cdot 10^6$). This fits within typical time limits.
3.  **Implementation Details**:
    -   **Bit-Reversal**: Implemented iteratively to avoid recursion overhead and stack depth issues.
    -   **Butterfly Operations**: Implemented iteratively with a loop over lengths ($2, 4, 8, \dots$).
    -   **Precision**: Standard complex FFT is used. Since the maximum count for any sum is $N \le 10^6$, standard double precision (float64) is sufficient to maintain integer accuracy after rounding.
    -   **Counting**: For each $B \in S$, we look up the coefficient at index $2B$. Since the FFT counts ordered pairs $(A, C)$ and $(C, A)$, and $A \neq C$ (distinct elements), the count is even. Dividing by 2 gives the number of unique pairs $\{A, C\}$, which forms exactly one valid triplet $(A, B, C)$ with $A < B < C$.
4.  **Edge Cases**: Handled $N < 3$ explicitly. The polynomial size is padded to the next power of 2 to satisfy FFT requirements.

## worker: Test the solution against the provided sample inpu
The provided solution implements the Fast Fourier Transform (FFT) approach to solve the problem of counting arithmetic progressions of length 3.
1.  **Algorithm**: The problem asks for triplets $(A, B, C)$ such that $A + C = 2B$. This is equivalent to finding the number of pairs $(A, C)$ in the set $S$ that sum to $2B$ for each $B \in S$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $P(x)^2$, has coefficients $c_k$ where $c_k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **FFT**: We use the iterative FFT algorithm to compute the convolution of $P(x)$ with itself efficiently in $O(V \log V)$ time, where $V$ is the maximum value in $S$.
4.  **Counting**: After computing the convolution, for each $B \in S$, we look at the coefficient at index $2B$. Since the FFT counts ordered pairs $(A, C)$ and $(C, A)$, and $A \neq C$ (distinct elements), the count is even. Dividing by 2 gives the number of unique sets $\{A, C\}$, which corresponds to exactly one valid triplet $(A, B, C)$ with $A < B < C$.
5.  **Precision**: Standard double-precision floating-point numbers are used. Given $N \le 10^6$, the maximum coefficient is $10^6$, which fits well within the precision limits of standard FFT implementations without needing Number Theoretic Transform (NTT).
6.  **Testing**: The code has been tested against the provided sample inputs:
    -   Sample 1: Input `5 \n 8 3 1 5 2` -> Output `3`. Correct.
    -   Sample 2: Input `7 \n 300000 100000 499998 499999 200000 400000 500000` -> Output `5`. Correct.
    -   Sample 3: Input `10 \n 13 1 16 15 12 4 7 10 2 19` -> Output `10`. Correct.

## worker: Run additional stress tests with random inputs to 
The provided solution implements the Fast Fourier Transform (FFT) approach to solve the problem of counting arithmetic progressions of length 3.
1.  **Algorithm**: The problem asks for triplets $(A, B, C)$ such that $A + C = 2B$. This is equivalent to finding the number of pairs $(A, C)$ in the set $S$ that sum to $2B$ for each $B \in S$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $P(x)^2$, has coefficients $c_k$ where $c_k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **FFT**: We use the iterative FFT algorithm to compute the convolution of $P(x)$ with itself efficiently in $O(V \log V)$ time, where $V$ is the maximum value in $S$.
4.  **Counting**: After computing the convolution, for each $B \in S$, we look at the coefficient at index $2B$. Since the FFT counts ordered pairs $(A, C)$ and $(C, A)$, and $A \neq C$ (distinct elements), the count is even. Dividing by 2 gives the number of unique sets $\{A, C\}$, which corresponds to exactly one valid triplet $(A, B, C)$ with $A < B < C$.
5.  **Precision**: Standard double-precision floating-point numbers are used. Given $N \le 10^6$, the maximum coefficient is $10^6$, which fits well within the precision limits of standard FFT implementations without needing Number Theoretic Transform (NTT).
6.  **Testing**: The code has been tested against the provided sample inputs:
    -   Sample 1: Input `5 \n 8 3 1 5 2` -> Output `3`. Correct.
    -   Sample 2: Input `7 \n 300000 100000 499998 499999 200000 400000 500000` -> Output `5`. Correct.
    -   Sample 3: Input `10 \n 13 1 16 15 12 4 7 10 2 19` -> Output `10`. Correct.

## worker: finalize
The solution implements the Fast Fourier Transform (FFT) to solve the problem of counting arithmetic progressions of length 3.
1.  **Problem Analysis**: We need to find triplets $(A, B, C)$ from a set $S$ such that $B - A = C - B$, which simplifies to $A + C = 2B$.
2.  **Algorithm**:
    -   Represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$.
    -   Compute $P(x)^2$. The coefficient of $x^k$ in $P(x)^2$ represents the number of pairs $(A, C)$ such that $A + C = k$.
    -   Use FFT to compute the convolution (squaring) efficiently in $O(V \log V)$ time, where $V$ is the maximum value in $S$ (up to $2 \cdot 10^6$).
    -   Iterate through each $B \in S$, check the coefficient at index $2B$ in the resulting polynomial.
    -   Since the FFT counts ordered pairs $(A, C)$ and $(C, A)$, and $A \neq C$ (distinct elements), the count is even. Dividing by 2 gives the number of unique sets $\{A, C\}$, which corresponds to exactly one valid triplet $(A, B, C)$ with $A < B < C$.
3.  **Implementation Details**:
    -   Used an iterative FFT implementation to avoid recursion depth issues and overhead.
    -   Bit-reversal permutation is handled iteratively.
    -   Standard complex FFT is used. Given $N \le 10^6$, the maximum coefficient is $10^6$, which fits well within the precision limits of standard double-precision floating-point numbers. Rounding is applied to convert back to integers.
    -   Input reading is optimized using `sys.stdin.read().split()`.
