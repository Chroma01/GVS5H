
## ideation
The problem asks us to count the number of arithmetic progressions of length 3 (fine triplets) within a given set of distinct integers $S$. The condition $B-A = C-B$ is equivalent to $A+C = 2B$.
Given the constraints $N, S_i \le 10^6$, an $O(N^2)$ solution is too slow.
The standard efficient approach for this type of problem (counting pairs with a specific sum) is using Fast Fourier Transform (FFT).
We can represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The coefficient of $x^k$ in $P(x)^2$ represents the number of pairs $(u, v) \in S \times S$ such that $u+v=k$.
By computing the convolution of the indicator array of $S$ with itself using FFT, we can find the number of pairs $(A, C)$ such that $A+C = 2B$ for any $B$.
Specifically, for each $B \in S$, the number of valid pairs $(A, C)$ with $A < B < C$ is derived from the coefficient at $2B$ in the squared polynomial:
1. The convolution count includes the pair $(B, B)$ (where $A=C=B$).
2. It counts both $(A, C)$ and $(C, A)$.
3. We need distinct $A, C$ with $A < C$.
Thus, for a fixed $B$, the number of valid triplets is `(conv[2*B] - 1) // 2`.
The complexity will be $O(M \log M)$ where $M = \max(S)$, which fits within the time limits for $M=10^6$ if implemented efficiently in Python.

## worker: Implement the FFT-based solution: read input, cons
1.  **Algorithm Selection**: The problem asks for the number of arithmetic progressions of length 3 ($A, B, C$) in a set $S$. The condition is $A+C = 2B$. Given constraints $N, S_i \le 10^6$, an $O(N^2)$ approach is too slow. The optimal approach is using Fast Fourier Transform (FFT) to compute the convolution of the set's indicator function with itself.
2.  **Complexity**:
    -   Sorting/Reading: $O(N \log N)$ or $O(N)$.
    -   FFT: $O(M \log M)$ where $M$ is the size of the polynomial (next power of 2 greater than $2 \times \max(S_i)$). With $\max(S_i) = 10^6$, $M \approx 2^{21} \approx 2 \times 10^6$. This fits within typical time limits (usually 2 seconds) for Python if implemented efficiently.
    -   Counting: $O(N)$.
3.  **Implementation Details**:
    -   Used a custom iterative FFT implementation to avoid recursion depth issues and overhead.
    -   Used `cmath.exp` for complex number operations.
    -   The convolution result `poly[k]` gives the number of pairs $(A, C)$ such that $A+C=k$.
    -   For each $B \in S$, we look at `poly[2*B]`. This value includes the pair $(B, B)$ and both $(A, C)$ and $(C, A)$ for $A \neq C$. Since we need $A < B < C$, we exclude $(B, B)$ and divide by 2 to account for the symmetry.
    -   Floating point precision: Used `round` to convert the real part of the complex number to an integer, as FFT results are theoretically integers but suffer from small precision errors.
4.  **Edge Cases**:
    -   $N < 3$: Handled explicitly.
    -   No triplets: The logic naturally results in 0.
    -   Large values: The polynomial size is adjusted to cover the maximum possible sum ($2 \times 10^6$).

## worker: Run the provided solution against the sample input
1.  **Algorithm Verification**: The provided solution uses the Fast Fourier Transform (FFT) to solve the problem in $O(M \log M)$ time, where $M$ is the maximum value in $S$ (scaled to the next power of 2). This is necessary because $N$ and $S_i$ can be up to $10^6$, making an $O(N^2)$ solution infeasible.
2.  **Logic Check**:
    -   The problem asks for triplets $(A, B, C)$ such that $B-A = C-B \implies A+C = 2B$.
    -   We construct a polynomial where the coefficient of $x^k$ is 1 if $k \in S$, else 0.
    -   Squaring this polynomial gives a new polynomial where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A+C=k$.
    -   For each $B \in S$, we check the coefficient at $x^{2B}$. Let this be $K$.
    -   $K$ counts pairs $(A, C)$ where $A+C=2B$. This includes $(B, B)$ and both $(A, C)$ and $(C, A)$ for $A \neq C$.
    -   We need $A < B < C$. Since $A+C=2B$, $A < B \iff C > B$. So we just need $A \neq B$ and $A < C$.
    -   The number of such pairs is $(K - 1) / 2$. We subtract 1 for the $(B, B)$ case and divide by 2 because the convolution counts both $(A, C)$ and $(C, A)$.
3.  **Implementation Details**:
    -   Used an iterative FFT implementation to avoid recursion depth issues and overhead.
    -   Used `cmath.exp` for roots of unity.
    -   Used `round()` to convert the real part of the complex result to an integer, mitigating floating-point precision errors.
    -   Input reading is optimized using `sys.stdin.read().split()`.
4.  **Complexity**:
    -   Time: $O(M \log M)$ where $M \approx 2 \times 10^6$. With $M=2^{21}$, operations are roughly $2 \times 10^6 \times 21 \approx 4.2 \times 10^7$, which should pass within typical time limits (2s) for Python if the constant factor is small.
    -   Space: $O(M)$ for the complex array.

## worker: Run the provided solution against Sample 1, Sample
The provided solution implements the Fast Fourier Transform (FFT) approach to solve the problem of counting arithmetic progressions of length 3.
1.  **Algorithm**: It constructs a polynomial where the coefficient of $x^k$ is 1 if $k \in S$ and 0 otherwise. Squaring this polynomial via FFT gives a new polynomial where the coefficient of $x^k$ represents the number of pairs $(A, C)$ such that $A+C=k$.
2.  **Logic**: For each $B \in S$, we check the coefficient at $x^{2B}$. This value includes the pair $(B, B)$ and both $(A, C)$ and $(C, A)$ for $A \neq C$. Since we require $A < B < C$, we subtract 1 (for $B, B$) and divide by 2 (to account for symmetry).
3.  **Complexity**: The time complexity is dominated by the FFT, which is $O(M \log M)$ where $M$ is the next power of 2 greater than $2 \times \max(S)$. Given constraints $S_i \le 10^6$, $M \approx 2 \times 10^6$, which fits within typical time limits.
4.  **Verification**: The code has been tested against Sample 1, Sample 2, and Sample 3.
    -   Sample 1: Input `5 \n 8 3 1 5 2` -> Output `3`. Correct.
    -   Sample 2: Input `7 \n 300000 100000 499998 499999 200000 400000 500000` -> Output `5`. Correct.
    -   Sample 3: Input `10 \n 13 1 16 15 12 4 7 10 2 19` -> Output `10`. Correct.
5.  **Edge Cases**: Handles $N < 3$ explicitly. Handles large values up to $10^6$. Uses `round()` to mitigate floating-point precision errors inherent in FFT.

## worker: Run the solution against the provided sample input
The provided solution implements the Fast Fourier Transform (FFT) approach to solve the problem of counting arithmetic progressions of length 3.
1.  **Algorithm**: It constructs a polynomial where the coefficient of $x^k$ is 1 if $k \in S$ and 0 otherwise. Squaring this polynomial via FFT gives a new polynomial where the coefficient of $x^k$ represents the number of pairs $(A, C)$ such that $A+C=k$.
2.  **Logic**: For each $B \in S$, we check the coefficient at $x^{2B}$. This value includes the pair $(B, B)$ and both $(A, C)$ and $(C, A)$ for $A \neq C$. Since we require $A < B < C$, we subtract 1 (for $B, B$) and divide by 2 (to account for symmetry).
3.  **Complexity**: The time complexity is dominated by the FFT, which is $O(M \log M)$ where $M$ is the next power of 2 greater than $2 \times \max(S)$. Given constraints $S_i \le 10^6$, $M \approx 2 \times 10^6$, which fits within typical time limits.
4.  **Verification**: The code has been tested against Sample 1, Sample 2, and Sample 3.
    -   Sample 1: Input `5 \n 8 3 1 5 2` -> Output `3`. Correct.
    -   Sample 2: Input `7 \n 300000 100000 499998 499999 200000 400000 500000` -> Output `5`. Correct.
    -   Sample 3: Input `10 \n 13 1 16 15 12 4 7 10 2 19` -> Output `10`. Correct.
5.  **Edge Cases**: Handles $N < 3$ explicitly. Handles large values up to $10^6$. Uses `round()` to mitigate floating-point precision errors inherent in FFT.

## worker: finalize
The solution uses the Fast Fourier Transform (FFT) to efficiently count the number of arithmetic progressions of length 3 (fine triplets) in the given set $S$.
1.  **Problem Analysis**: A triplet $(A, B, C)$ is "fine" if $B - A = C - B$, which simplifies to $A + C = 2B$. We need to count such triplets where $A, B, C \in S$ and $A < B < C$.
2.  **Algorithm**:
    -   Construct a polynomial $P(x)$ where the coefficient of $x^k$ is 1 if $k \in S$ and 0 otherwise.
    -   Compute $Q(x) = P(x)^2$ using FFT. The coefficient of $x^k$ in $Q(x)$ represents the number of pairs $(A, C)$ such that $A + C = k$.
    -   For each $B \in S$, we look at the coefficient of $x^{2B}$ in $Q(x)$. Let this be $K$.
    -   $K$ counts all pairs $(A, C)$ summing to $2B$. This includes the pair $(B, B)$ and both $(A, C)$ and $(C, A)$ for $A \neq C$.
    -   Since we require $A < B < C$, we must exclude the case $A=B$ (which implies $C=B$) and account for the symmetry. The number of valid pairs is $(K - 1) / 2$.
3.  **Complexity**: The FFT runs in $O(M \log M)$ where $M$ is the size of the polynomial (next power of 2 greater than $2 \times \max(S)$). With $\max(S) \le 10^6$, $M \approx 2 \times 10^6$, which fits within the time limits.
4.  **Implementation Details**:
    -   An iterative FFT implementation is used to avoid recursion depth issues.
    -   Floating-point precision errors are handled by rounding the real part of the result to the nearest integer.
    -   Input reading is optimized using `sys.stdin.read().split()`.
