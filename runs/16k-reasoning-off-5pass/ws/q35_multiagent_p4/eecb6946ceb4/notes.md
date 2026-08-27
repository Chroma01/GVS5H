
## ideation
The problem asks for the number of arithmetic progressions of length 3 (fine triplets) within a given set $S$ of $N$ distinct integers, where all elements are $\le 10^6$.

1.  **Naive Approach ($O(N^2)$)**: Iterating over all pairs $(A, C)$ and checking if the midpoint $B$ exists. With $N=10^6$, this is $10^{12}$ operations, which is too slow.
2.  **Middle Element Iteration ($O(N \cdot M)$)**: Iterating over each $B \in S$ and each possible difference $d$, checking if $B-d$ and $B+d$ exist. The worst-case complexity is proportional to $\sum_{B \in S} \min(B, M-B)$. If $S$ contains all numbers from $1$ to $M$, this sum is $\approx M^2/4 \approx 2.5 \times 10^{11}$, which is too slow for Python (and likely C++ within typical time limits).
3.  **FFT Approach ($O(M \log M)$)**:
    *   Let $P$ be a polynomial (or boolean array) where the coefficient of $x^i$ is 1 if $i \in S$, and 0 otherwise.
    *   We want to count triplets $(A, B, C)$ such that $A, B, C \in S$ and $A+C = 2B$.
    *   Consider the convolution $Q = P * P$. The coefficient $Q[k]$ represents the number of pairs $(A, C)$ such that $A+C=k$.
    *   For each $B \in S$, the number of valid pairs $(A, C)$ with midpoint $B$ is exactly the number of pairs summing to $2B$, which is $Q[2B]$.
    *   However, $Q[2B]$ counts pairs $(A, C)$ where order doesn't matter (i.e., $(A,C)$ and $(C,A)$ are both counted if $A \neq C$) and includes cases where $A=C$ (if $2B \in S+S$ via $B+B$).
    *   Specifically, if we define the polynomial $P(x) = \sum_{s \in S} x^s$, then $P(x)^2 = \sum_{k} (\sum_{a+c=k, a,c \in S} 1) x^k$.
    *   The term for $x^{2B}$ in $P(x)^2$ is the count of pairs $(A, C)$ such that $A+C=2B$.
    *   Since $A < B < C$ is required, we need $A \neq C$. Also, the pair $(A, C)$ is unordered in the convolution sum usually, but let's look closer.
    *   Actually, standard convolution counts ordered pairs. So $Q[2B]$ includes $(A, C)$ and $(C, A)$. If $A \neq C$, it counts 2. If $A=C=B$, it counts 1.
    *   We want distinct $A, B, C$ with $A < B < C$. This corresponds to exactly one ordered pair $(A, C)$ with $A < C$ for each valid triplet.
    *   So, for a fixed $B$, the number of valid triplets with middle element $B$ is $\frac{Q[2B] - (\text{1 if } B \in S \text{ else } 0)}{2}$.
        *   Why subtract 1 if $B \in S$? Because the pair $(B, B)$ contributes 1 to $Q[2B]$ (since $B+B=2B$). We must exclude $A=C=B$.
        *   The remaining count $Q[2B] - 1$ (if $B \in S$) or $Q[2B]$ (if $B \notin S$, but $B$ must be in $S$ for it to be a middle element) counts pairs $(A, C)$ with $A+C=2B$ and $A \neq C$. Since $A \neq C$, these come in pairs $(A, C)$ and $(C, A)$. We want only the ones with $A < C$, so we divide by 2.
    *   Therefore, the answer is $\sum_{B \in S} \frac{Q[2B] - 1}{2}$.
    *   Complexity: FFT takes $O(M \log M)$ where $M = \max(S) \le 10^6$. This is feasible.

4.  **Implementation Details**:
    *   Use `numpy.fft` or a custom FFT implementation. `numpy` is generally available in competitive programming environments or can be imported. If not, a pure Python FFT might be too slow due to overhead, but let's try `numpy` first. If `numpy` is not allowed/available, we might need a pure Python implementation. The prompt doesn't restrict libraries, so `numpy` is a safe bet for speed.
    *   Max value is $10^6$, so the polynomial degree is $10^6$. The convolution will have degree $2 \cdot 10^6$. We need to pad to the next power of 2, which is $2^{21} = 2,097,152$.
    *   Steps:
        1. Read input.
        2. Create a boolean array `exists` of size $10^6 + 1$.
        3. Create a complex array `P` of size $2^{21}$, setting `P[s] = 1` for each $s \in S$.
        4. Compute FFT of `P`.
        5. Square the FFT result element-wise.
        6. Compute Inverse FFT.
        7. Round the real parts to get integer counts $Q$.
        8. Sum $\frac{Q[2B] - 1}{2}$ for all $B \in S$.

5.  **Pitfalls**:
    *   Floating point precision issues with FFT. Using `numpy` with `float64` is usually sufficient for counts up to $N^2 \approx 10^{12}$? Wait, max count for a specific sum is $N$. $Q[k]$ is at most $N$. $10^6$ fits easily in `float64` precision (which has 53 bits of significand, approx 15 decimal digits).
    *   Memory usage: Arrays of size $2^{21}$ complex numbers. $2 \cdot 10^6 \times 16$ bytes $\approx 32$ MB. This is fine.
    *   Time limit: FFT on $2^{21}$ points in Python via NumPy is very fast (sub-second).

## worker: Implement the FFT-based solution using NumPy.
The problem asks for the number of arithmetic progressions of length 3 within a set $S$. An arithmetic progression $(A, B, C)$ satisfies $A+C = 2B$.

1.  **FFT Approach**:
    *   We represent the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$.
    *   The square of this polynomial, $P(x)^2$, has coefficients that represent the number of ways to write an integer $k$ as a sum of two elements from $S$. Specifically, the coefficient of $x^k$ in $P(x)^2$ is the number of pairs $(A, C) \in S \times S$ such that $A+C=k$.
    *   We compute this convolution using Fast Fourier Transform (FFT).
    *   For each $B \in S$, we look at the coefficient of $x^{2B}$ in $P(x)^2$. Let this count be $Q[2B]$.
    *   $Q[2B]$ counts all pairs $(A, C)$ such that $A+C=2B$. This includes:
        *   The pair $(B, B)$, since $B+B=2B$.
        *   Pairs $(A, C)$ with $A \neq C$. Since addition is commutative, both $(A, C)$ and $(C, A)$ are counted.
    *   We want distinct triplets $(A, B, C)$ with $A < B < C$. This corresponds to exactly one pair $(A, C)$ with $A < C$ for each valid triplet.
    *   Therefore, for a fixed $B$, the number of valid triplets is $\frac{Q[2B] - 1}{2}$. We subtract 1 to remove the $(B, B)$ case, and divide by 2 to account for the double counting of distinct pairs.
    *   We sum this value over all $B \in S$.

2.  **Complexity**:
    *   FFT on an array of size $M$ takes $O(M \log M)$ time. Here $M \approx 2 \cdot 10^6$ (next power of 2 above $2 \cdot 10^6$).
    *   This is efficient enough for the given constraints ($N, S_i \le 10^6$).

3.  **Precision**:
    *   Using `numpy` with `float64` provides sufficient precision for counts up to $N=10^6$. The maximum value in the convolution is $N$, which fits well within the 53-bit significand of double precision floats.
