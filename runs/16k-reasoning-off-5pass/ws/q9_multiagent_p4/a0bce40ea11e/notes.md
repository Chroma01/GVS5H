
## ideation
**Core Difficulty**: The problem asks for the sum of $B^p$ modulo $p$. The key insight is applying Fermat's Little Theorem ($x^p \equiv x \pmod p$) to simplify the matrix power operation. Without this, calculating $B^p$ for all $(p-1)^K$ matrices would be computationally infeasible given $p$ can be up to $10^9$.

**Candidate Approaches**:
1.  **Direct Application of Fermat's Little Theorem**:
    -   Recognize that for any integer $x$, $x^p \equiv x \pmod p$.
    -   Therefore, the matrix sum $\sum B^p \equiv \sum B \pmod p$.
    -   The problem reduces to summing all possible matrices $B$ element-wise.
    -   Calculate the number of zeros $K$ in $A$.
    -   For each cell $(i, j)$:
        -   If $A_{i,j} \neq 0$: It is fixed. Contribution = $A_{i,j} \times (p-1)^K$.
        -   If $A_{i,j} = 0$: It takes values $1, \dots, p-1$. Each value appears $(p-1)^{K-1}$ times. Contribution = $(p-1)^{K-1} \times \sum_{x=1}^{p-1} x$.
    -   Sum of $1 \dots p-1$ is $p(p-1)/2$.
        -   If $p > 2$, this sum is $0 \pmod p$.
        -   If $p = 2$, this sum is $1 \pmod 2$.
    -   Final answer for each cell is the calculated contribution modulo $p$.

2.  **Verification**:
    -   Check Sample 1 ($p=3$): Sum of $1..2$ is $3 \equiv 0 \pmod 3$. Zeros contribute 0. Non-zeros contribute $val \times 2^2 = 4 \times val \equiv val \pmod 3$.
    -   Check Sample 2 ($p=2$): Sum of $1..1$ is $1$. Zeros contribute $1 \times 1^{K-1} = 1$. Non-zeros contribute $val \times 1^K = val$.
    -   This logic holds and is $O(N^2)$, which fits the constraints ($N \le 100$).

## worker: Read input $N$ and $p$, then read the $N \times N$
The problem requires calculating the sum of $B^p$ modulo $p$ over all valid matrices $B$.
1.  **Fermat's Little Theorem**: For any integer $x$, $x^p \equiv x \pmod p$. This allows us to replace the matrix power operation $B^p$ with just $B$ in the summation modulo $p$. The problem simplifies to finding the sum of all possible matrices $B$ element-wise modulo $p$.
2.  **Element-wise Summation**:
    -   Let $K$ be the number of zeros in the initial matrix $A$.
    -   There are $(p-1)^K$ total matrices $B$.
    -   For a specific cell $(i, j)$:
        -   If $A_{i,j} \neq 0$: The value is fixed at $A_{i,j}$ for all $K$ variations. It contributes $A_{i,j} \times (p-1)^K$ to the sum.
        -   If $A_{i,j} = 0$: The value can be any integer from $1$ to $p-1$. Each value appears $(p-1)^{K-1}$ times. The contribution is $(p-1)^{K-1} \times \sum_{x=1}^{p-1} x$.
3.  **Summation Logic**:
    -   The sum $\sum_{x=1}^{p-1} x = \frac{p(p-1)}{2}$.
    -   If $p > 2$: Since $p$ is prime, $p$ does not divide 2. However, $p$ divides the numerator $p(p-1)$, so the sum is $0 \pmod p$. Thus, any cell that was originally 0 contributes 0 to the final sum.
    -   If $p = 2$: The sum is $1$. The term $(p-1)^{K-1} = 1^{K-1} = 1$. So a zero cell contributes $1 \times 1 = 1$. A non-zero cell (which must be 1) contributes $1 \times 1^K = 1$. Thus, for $p=2$, every cell in the result is 1.
4.  **Implementation**:
    -   Count zeros ($K$).
    -   If $p=2$, output a matrix of all 1s.
    -   If $p>2$, compute $T = (p-1)^K \pmod p$. For each cell, if it was 0, output 0; otherwise, output $(A_{i,j} \times T) \pmod p$.

## worker: Run the code against the provided sample inputs to
The code implements the derived logic:
1.  **Fermat's Little Theorem**: $x^p \equiv x \pmod p$. This simplifies the problem from summing $B^p$ to summing $B$.
2.  **Case $p=2$**: The sum of values $1$ to $p-1$ is $1$. The multiplier for zeros is $1^{K-1}=1$. Non-zeros are $1$, multiplier is $1^K=1$. Result is all $1$s.
3.  **Case $p>2$**: The sum of values $1$ to $p-1$ is $p(p-1)/2$, which is $0 \pmod p$. Thus, any cell that was originally $0$ contributes $0$ to the sum. Cells that were non-zero contribute $A_{i,j} \times (p-1)^K \pmod p$.
4.  **Complexity**: $O(N^2)$ to read input and compute the result. $N \le 100$, so this is extremely fast. Modular exponentiation is $O(\log K)$.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the logic derived from Fermat's Little Theorem ($x^p \equiv x \pmod p$).
1.  **Case $p=2$**: The sum of $1 \dots p-1$ is $1$. The multiplier for zeros is $1^{K-1}=1$. Non-zeros are $1$, multiplier is $1^K=1$. Thus, every cell in the result is $1$.
2.  **Case $p>2$**: The sum of $1 \dots p-1$ is $p(p-1)/2$, which is $0 \pmod p$. Thus, any cell that was originally $0$ contributes $0$ to the sum. Cells that were non-zero contribute $A_{i,j} \times (p-1)^K \pmod p$.
The implementation correctly handles reading input, counting zeros, applying modular exponentiation, and printing the result.

## worker: Run the provided code against Sample 1, Sample 2, 
The code implements the logic derived from Fermat's Little Theorem ($x^p \equiv x \pmod p$).
1.  **Case $p=2$**: The sum of values $1 \dots p-1$ is $1$. The multiplier for zeros is $1^{K-1}=1$. Non-zeros are $1$, multiplier is $1^K=1$. Thus, every cell in the result is $1$.
2.  **Case $p>2$**: The sum of values $1 \dots p-1$ is $p(p-1)/2$, which is $0 \pmod p$. Thus, any cell that was originally $0$ contributes $0$ to the sum. Cells that were non-zero contribute $A_{i,j} \times (p-1)^K \pmod p$.
The implementation correctly handles reading input, counting zeros, applying modular exponentiation, and printing the result.

## worker: finalize
The solution leverages Fermat's Little Theorem ($x^p \equiv x \pmod p$) to simplify the problem from summing $B^p$ to summing $B$.
1.  **Case $p=2$**: The sum of values $1 \dots p-1$ is $1$. The multiplier for zeros is $1^{K-1}=1$. Non-zeros are $1$, multiplier is $1^K=1$. Thus, every cell in the result is $1$.
2.  **Case $p>2$**: The sum of values $1 \dots p-1$ is $p(p-1)/2$, which is $0 \pmod p$. Thus, any cell that was originally $0$ contributes $0$ to the sum. Cells that were non-zero contribute $A_{i,j} \times (p-1)^K \pmod p$.
The implementation correctly handles reading input, counting zeros, applying modular exponentiation, and printing the result.
