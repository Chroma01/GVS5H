
## ideation
**Core Difficulty**: The problem requires summing $B^p$ over all possible completions of a partially filled matrix $A$. The key insight is that the summation over the "free" variables (those originally 0) interacts with the matrix multiplication structure. Specifically, for any term in the expansion of $(B^p)_{i,j}$ that involves a product of entries, if any entry in that product corresponds to a position that was originally 0 in $A$, the sum over all possible values for that entry ($1$ to $p-1$) is $\sum_{x=1}^{p-1} x = \frac{p(p-1)}{2} \equiv 0 \pmod p$. Therefore, only paths in the matrix multiplication where every step corresponds to a non-zero entry in the original matrix $A$ contribute to the final sum.

**Candidate Approaches**:
1.  **Matrix Power with Zero Handling**: Construct a matrix $M$ identical to $A$, but treat any $0$ in $A$ as $0$ in $M$ (effectively removing those edges). Compute $M^p$ using binary exponentiation (matrix exponentiation). The result will be the sum of products of paths of length $p$ using only non-zero entries.
2.  **Scaling Factor**: Calculate the number of zeros $K$ in $A$. The total number of matrices $B$ is $(p-1)^K$. Each valid path (using only non-zero entries) appears in exactly $(p-1)^K$ matrices $B$ (since the non-zero entries are fixed, and the $K$ zero entries can be anything). Thus, the total sum is $(p-1)^K \times (M^p)_{i,j} \pmod p$. Note that $(p-1) \equiv -1 \pmod p$, so the factor is $(-1)^K$.
3.  **Edge Cases**:
    *   $p=2$: $(p-1)^K = 1^K = 1$.
    *   $N$ is small ($100$), $p$ is large ($10^9$). Matrix multiplication is $O(N^3 \log p)$, which is feasible ($100^3 \times 30 \approx 3 \times 10^7$ operations).
    *   Modulo arithmetic at every step to prevent overflow.

## worker: Read input $N$, $p$, and the matrix $A$. Count the
The problem asks for the sum of $B^p$ over all matrices $B$ formed by replacing zeros in $A$ with values from $1$ to $p-1$.
1.  **Linearity of Expectation/Summation**: The $(i, j)$-th element of the sum is the sum of $(B^p)_{i,j}$ over all valid $B$.
2.  **Matrix Power Expansion**: $(B^p)_{i,j} = \sum_{k_1, \dots, k_{p-1}} B_{i,k_1} B_{k_1, k_2} \cdots B_{k_{p-1}, j}$.
3.  **Zero Contribution**: If any entry $B_{u,v}$ in the product corresponds to a position that was $0$ in $A$, then $B_{u,v}$ can be any value in $\{1, \dots, p-1\}$. The sum of these values is $\sum_{x=1}^{p-1} x = \frac{p(p-1)}{2}$. Since $p$ is prime and $p \ge 2$, this sum is $0 \pmod p$. Thus, any path containing a zero-entry from $A$ contributes $0$ to the total sum.
4.  **Non-Zero Paths**: Only paths where every step corresponds to a non-zero entry in $A$ contribute. For such paths, the values are fixed.
5.  **Counting**: There are $K$ zeros in $A$. Each valid path (using only non-zero entries) appears in exactly $(p-1)^K$ matrices $B$ (since the $K$ zero entries can be chosen freely).
6.  **Final Formula**: The total sum for $(i, j)$ is $(p-1)^K \times (A^p)_{i,j} \pmod p$, where $A^p$ is computed treating $0$s as $0$ (which naturally happens if we just use the given $A$).
7.  **Modulo Arithmetic**: $(p-1) \equiv -1 \pmod p$. So $(p-1)^K \equiv (-1)^K \pmod p$. If $K$ is even, factor is $1$; if $K$ is odd, factor is $p-1$.
8.  **Complexity**: Matrix multiplication is $O(N^3)$. Exponentiation takes $O(N^3 \log p)$. With $N \le 100$ and $p \le 10^9$, this is well within time limits.

## worker: Run the code against the provided sample inputs to
The code implements the derived logic:
1.  **Input Parsing**: Reads $N$, $p$, and the matrix $A$.
2.  **Zero Counting**: Counts $K$, the number of zeros in $A$.
3.  **Scaling Factor**: Computes $(-1)^K \pmod p$. If $K$ is even, factor is 1; if odd, factor is $p-1$.
4.  **Matrix Exponentiation**: Computes $A^p \pmod p$ using binary exponentiation. The matrix multiplication function skips zeros to optimize, though standard multiplication would also work since $0 \times x = 0$.
5.  **Final Calculation**: Multiplies each element of $A^p$ by the scaling factor modulo $p$.
6.  **Output**: Prints the resulting matrix.

The logic holds because any path in the matrix multiplication expansion of $B^p$ that includes a position originally 0 in $A$ will sum to 0 modulo $p$ over all possible replacements for that position (since $\sum_{x=1}^{p-1} x \equiv 0 \pmod p$). Only paths consisting entirely of non-zero entries from $A$ contribute, and they are counted $(p-1)^K$ times.

## worker: Run the provided sample inputs to verify correctne
The solution implements the derived logic:
1.  **Input Parsing**: Reads $N$, $p$, and the matrix $A$.
2.  **Zero Counting**: Counts $K$, the number of zeros in $A$.
3.  **Scaling Factor**: Computes $(-1)^K \pmod p$. If $K$ is even, factor is 1; if odd, factor is $p-1$.
4.  **Matrix Exponentiation**: Computes $A^p \pmod p$ using binary exponentiation. The matrix multiplication function skips zeros to optimize, though standard multiplication would also work since $0 \times x = 0$.
5.  **Final Calculation**: Multiplies each element of $A^p$ by the scaling factor modulo $p$.
6.  **Output**: Prints the resulting matrix.

The logic holds because any path in the matrix multiplication expansion of $B^p$ that includes a position originally 0 in $A$ will sum to 0 modulo $p$ over all possible replacements for that position (since $\sum_{x=1}^{p-1} x \equiv 0 \pmod p$). Only paths consisting entirely of non-zero entries from $A$ contribute, and they are counted $(p-1)^K$ times.

## worker: Run the provided sample inputs to verify correctne
The code implements the derived logic:
1.  **Input Parsing**: Reads $N$, $p$, and the matrix $A$.
2.  **Zero Counting**: Counts $K$, the number of zeros in $A$.
3.  **Scaling Factor**: Computes $(-1)^K \pmod p$. If $K$ is even, factor is 1; if odd, factor is $p-1$.
4.  **Matrix Exponentiation**: Computes $A^p \pmod p$ using binary exponentiation. The matrix multiplication function skips zeros to optimize, though standard multiplication would also work since $0 \times x = 0$.
5.  **Final Calculation**: Multiplies each element of $A^p$ by the scaling factor modulo $p$.
6.  **Output**: Prints the resulting matrix.

The logic holds because any path in the matrix multiplication expansion of $B^p$ that includes a position originally 0 in $A$ will sum to 0 modulo $p$ over all possible replacements for that position (since $\sum_{x=1}^{p-1} x \equiv 0 \pmod p$). Only paths consisting entirely of non-zero entries from $A$ contribute, and they are counted $(p-1)^K$ times.

## worker: finalize
The solution relies on the linearity of expectation (or summation) and the properties of modular arithmetic with prime numbers.
1.  **Problem Analysis**: We need to compute $\sum_{B} (B^p)_{i,j} \pmod p$, where $B$ is formed by replacing zeros in $A$ with values from $\{1, \dots, p-1\}$.
2.  **Key Insight**: The term $(B^p)_{i,j}$ is a sum over all paths of length $p$ in the matrix indices. Specifically, $(B^p)_{i,j} = \sum_{k_1, \dots, k_{p-1}} \prod_{m=0}^{p-1} B_{u_m, v_m}$.
3.  **Zero Contribution**: If any entry $B_{u,v}$ in a product term corresponds to a position that was $0$ in $A$, then $B_{u,v}$ can take any value in $\{1, \dots, p-1\}$. The sum of these values is $\sum_{x=1}^{p-1} x = \frac{p(p-1)}{2}$. Since $p$ is prime ($p \ge 2$), this sum is divisible by $p$, so it is $0 \pmod p$. Consequently, any path containing a zero-entry from $A$ contributes $0$ to the total sum.
4.  **Non-Zero Paths**: Only paths where every step corresponds to a non-zero entry in $A$ contribute to the sum. For these paths, the values are fixed in $A$.
5.  **Counting**: There are $K$ zeros in $A$. Each valid path (using only non-zero entries) appears in exactly $(p-1)^K$ matrices $B$ (since the $K$ zero entries can be chosen freely).
6.  **Formula**: The total sum for $(i, j)$ is $(p-1)^K \times (A^p)_{i,j} \pmod p$, where $A^p$ is computed treating $0$s as $0$ (effectively removing edges with 0).
7.  **Modulo Arithmetic**: $(p-1) \equiv -1 \pmod p$. Thus, $(p-1)^K \equiv (-1)^K \pmod p$. If $K$ is even, the factor is $1$; if $K$ is odd, the factor is $p-1$.
8.  **Implementation**: We use binary exponentiation for matrix power $A^p \pmod p$. The matrix multiplication is optimized to skip zeros, though standard multiplication would also yield correct results since $0 \times x = 0$. The complexity is $O(N^3 \log p)$, which fits within the constraints ($N \le 100, p \le 10^9$).
