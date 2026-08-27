
## ideation
**Core Difficulty**:
The problem asks to count arithmetic progressions $(A, B, C)$ from a set $S$ of size $N$ where $N, S_i \le 10^6$. A naive $O(N^2)$ approach checking all pairs or iterating differences is too slow ($10^{12}$ operations). We need an approach close to $O(N)$ or $O(M \log M)$ where $M = \max(S_i)$.

**Candidate Approaches**:
1.  **Polynomial Multiplication (FFT)**:
    -   Represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$.
    -   Compute $Q(x) = P(x)^2$. The coefficient of $x^k$ in $Q(x)$ represents the number of pairs $(A, C)$ such that $A+C=k$.
    -   For each $B \in S$, the number of valid triplets with middle element $B$ is the coefficient of $x^{2B}$ in $Q(x)$ minus 1 (to exclude the case $A=C=B$).
    -   Complexity: $O(M \log M)$ using FFT. With $M=10^6$, this is feasible.
    -   Pitfall: Implementing FFT efficiently in Python. Standard recursive FFT is too slow; iterative FFT with precomputed roots is necessary. Floating-point precision errors must be handled (rounding).

2.  **Two Pointers / Hashing**:
    -   Iterate $B \in S$, use two pointers to find pairs summing to $2B$.
    -   Complexity: $O(N^2)$ in worst case (dense array). Not acceptable.

3.  **Difference Iteration**:
    -   Iterate difference $d$, check existence of $B-d$ and $B+d$.
    -   Complexity: $O(M^2)$ or $O(N \cdot \text{avg\_diff})$. Worst case is bad.

## worker: [todo] **Worker 1**: Implement the iterative FFT a
The solution uses the Fast Fourier Transform (FFT) to efficiently count arithmetic progressions.
1.  **Problem Transformation**: The problem asks for the number of triplets $(A, B, C)$ such that $A + C = 2B$. This is equivalent to finding pairs $(A, C)$ in the set $S$ that sum to $2B$ for each $B \in S$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $Q(x) = P(x)^2$, has coefficients where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **FFT Implementation**: Since $N$ and $S_i$ can be up to $10^6$, an $O(N^2)$ solution is too slow. We use FFT to compute the convolution in $O(M \log M)$ time, where $M$ is the maximum value in $S$ (scaled to the next power of 2).
4.  **Algorithm**:
    -   Construct a binary array `a` where `a[i] = 1` if $i \in S$.
    -   Apply FFT to `a`.
    -   Square the resulting complex numbers point-wise.
    -   Apply Inverse FFT to get the coefficients of the squared polynomial.
    -   For each $B \in S$, the number of valid triplets with middle element $B$ is `coeff[2*B] - 1` (subtracting 1 to exclude the case $A=C=B$).
5.  **Complexity**: The FFT size is at most $2^{21} \approx 2 \times 10^6$. The complexity is roughly $O(M \log M)$, which fits within typical time limits for Python if implemented iteratively to avoid recursion overhead.

## worker: [todo] **Worker 1**: Test the solution against the
The provided solution implements the Fast Fourier Transform (FFT) to solve the problem of counting arithmetic progressions (fine triplets) efficiently.

**Algorithm Logic:**
1.  **Problem Transformation**: A triplet $(A, B, C)$ is a "fine triplet" if $B - A = C - B$, which simplifies to $A + C = 2B$. We need to count such triplets where $A, B, C \in S$ and $A < B < C$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $Q(x) = P(x)^2$, has coefficients where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **Counting**: For each $B \in S$, the number of valid pairs $(A, C)$ summing to $2B$ is given by the coefficient of $x^{2B}$ in $Q(x)$. Since the problem requires distinct elements ($A < B < C$), we must exclude the case where $A = C = B$. Thus, for each $B$, we add `(coefficient[2*B] - 1)` to the total count.
4.  **FFT Implementation**:
    -   We construct a binary array `a` of size $2^k$ (where $2^k > 2 \times \max(S)$) such that `a[i] = 1` if $i \in S$.
    -   We apply the iterative FFT to `a`.
    -   We square the resulting complex numbers point-wise.
    -   We apply the Inverse FFT to retrieve the coefficients of the squared polynomial.
    -   We sum the required values, rounding to the nearest integer to mitigate floating-point precision errors.

## worker: Run the provided code against Sample 1, Sample 2, 
The provided code implements the Fast Fourier Transform (FFT) to solve the problem efficiently.
1.  **Logic**: The problem asks for the number of triplets $(A, B, C)$ such that $A + C = 2B$. This is equivalent to finding pairs $(A, C)$ in the set $S$ that sum to $2B$ for each $B \in S$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $Q(x) = P(x)^2$, has coefficients where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **FFT**: Since $N$ and $S_i$ can be up to $10^6$, an $O(N^2)$ solution is too slow. We use FFT to compute the convolution in $O(M \log M)$ time, where $M$ is the maximum value in $S$ (scaled to the next power of 2).
4.  **Counting**: For each $B \in S$, the number of valid pairs $(A, C)$ summing to $2B$ is given by the coefficient of $x^{2B}$ in $Q(x)$. Since the problem requires distinct elements ($A < B < C$), we must exclude the case where $A = C = B$. Thus, for each $B$, we add `(coefficient[2*B] - 1)` to the total count.
5.  **Implementation**: The code uses an iterative FFT implementation to avoid recursion overhead and precomputes roots of unity. It handles floating-point precision by rounding the real part of the result.

## worker: finalize
The solution uses the Fast Fourier Transform (FFT) to efficiently count arithmetic progressions (fine triplets) in $O(M \log M)$ time, where $M$ is the maximum value in the input set $S$.

1.  **Problem Transformation**: A triplet $(A, B, C)$ is a "fine triplet" if $B - A = C - B$, which simplifies to $A + C = 2B$. We need to count such triplets where $A, B, C \in S$ and $A < B < C$.
2.  **Polynomial Multiplication**: We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The square of this polynomial, $Q(x) = P(x)^2$, has coefficients where the coefficient of $x^k$ is the number of pairs $(A, C)$ such that $A + C = k$.
3.  **FFT Implementation**: Since $N$ and $S_i$ can be up to $10^6$, an $O(N^2)$ solution is too slow. We use FFT to compute the convolution in $O(M \log M)$ time. The code implements an iterative FFT to avoid recursion overhead and precomputes roots of unity.
4.  **Counting**: For each $B \in S$, the number of valid pairs $(A, C)$ summing to $2B$ is given by the coefficient of $x^{2B}$ in $Q(x)$. Since the problem requires distinct elements ($A < B < C$), we must exclude the case where $A = C = B$. Thus, for each $B$, we add `(coefficient[2*B] - 1)` to the total count.
5.  **Complexity**: The FFT size is at most $2^{21} \approx 2 \times 10^6$. The complexity is roughly $O(M \log M)$, which fits within typical time limits for Python if implemented iteratively.
