1. **Leverage Fermat's Little Theorem and Matrix Properties**: For any integer $x$, $x^p \equiv x \pmod p$. However, this applies to elements, not matrices directly. But for a matrix $B$ over $\mathbb{F}_p$, $B^p$ is not simply element-wise power. We need to sum $B^p$ over all completions.
2. **Linearity of Expectation/Summation**: The sum $\sum_B B^p$ can be computed by considering the contribution of each term in the matrix power expansion. However, a more direct approach uses the fact that the sum is over all assignments of zeros.
3. **Key Insight**: If $A$ has no zeros, the answer is simply $A^p \pmod p$. If $A$ has zeros, we can use the linearity of the sum. Specifically, we can consider the sum as a multilinear function in the entries that are zero.
4. **Handling Zeros**: Let $Z$ be the set of positions $(i,j)$ where $A_{i,j} = 0$. For each such position, we sum over $v \in \{1, \dots, p-1\}$. Note that $\sum_{v=1}^{p-1} v^k \pmod p$ is $-1$ if $p-1 | k$ and $k > 0$, and $0$ if $p-1 \nmid k$ and $k > 0$. For $k=0$, the sum is $p-1 \equiv -1$.
5. **Efficient Computation**: Since $N \le 100$, we cannot iterate over all $B$. We use the fact that the sum over all $B$ can be decomposed. A powerful technique is to note that $\sum_{B} B^p = \sum_{B} B \cdot B^{p-1}$. This is still hard.
6. **Alternative Insight**: Consider the polynomial $P(X) = \sum_{B} B^p$. Since the sum is over all replacements, and the operation is linear in the "zero" variables if we expand carefully, we can use generating functions or dynamic programming. However, there is a simpler property:
   - If $p=2$, the only non-zero value is 1. So $B$ is uniquely determined if no zeros, or if zeros are replaced by 1.
   - For general $p$, note that $\sum_{v=0}^{p-1} v^k \equiv 0 \pmod p$ for $0 < k < p-1$, and $\equiv -1$ for $k=p-1$ or $k=0$ (if we include 0). But our sum is over $1 \dots p-1$.
   - Let $S_k = \sum_{v=1}^{p-1} v^k$. Then $S_k \equiv -1 \pmod p$ if $p-1 | k$, else $0$.
   - The matrix power $B^p$ involves products of entries. The sum over all $B$ will factorize if the indices don't mix in a way that couples the zero-positions. But matrix multiplication mixes rows and columns.
7. **Correct Approach**: Use the fact that the sum is over all $B$. We can write $B = A + D$, where $D$ has zeros where $A$ is non-zero, and $D_{i,j} \in \{1, \dots, p-1\}$ where $A_{i,j}=0$. This is complex.
8. **Simpler Observation**: If there are no zeros, output $A^p \pmod p$. If there are zeros, we can use the following:
   - The sum $\sum_B B^p$ can be computed by iterating over the zero positions? No, too many.
   - Key realization: For $p > N$, the sum of powers might simplify. But $p$ can be small.
   - Let's use the property: $\sum_{x=0}^{p-1} x^k \equiv 0$ for $0 < k < p-1$.
   - We can extend the sum to include 0 and subtract the cases where some zero is replaced by 0. But the problem says $1 \dots p-1$.
   - Let $S = \sum_{B: A_{ij}=0 \implies B_{ij} \in \{1,\dots,p-1\}} B^p$.
   - Let $T = \sum_{B: A_{ij}=0 \implies B_{ij} \in \{0,\dots,p-1\}} B^p$.
   - Then $S = T - \sum_{\text{at least one zero is 0}} B^p$. This inclusion-exclusion is complex.
9. **Practical Solution for CP**: Given $N \le 100$, we can compute $A^p \pmod p$ easily. If there are no zeros, we are done. If there are zeros, we can use the linearity of the sum over the choices. Specifically, the sum is a multilinear function in the variables corresponding to zeros. We can compute the sum by considering the contribution of each subset of zeros being non-zero? No.
10. **Final Strategy**: 
    - Compute $M = A^p \pmod p$ if no zeros.
    - If there are zeros, note that the sum over all $B$ of $B^p$ can be computed by dynamic programming or by exploiting the structure. However, a known result is that $\sum_{B} B^p \equiv 0 \pmod p$ if there is at least one zero? No, Sample 1 output is not all zeros.
    - Let's re-read Sample 1: $N=2, p=3$. Zeros at (1,1) and (2,1). Output: `0 2` and `1 2`.
    - We can compute the sum by iterating over all $B$ if the number of zeros is small. But $K$ can be up to $N^2$.
    - Correct approach: Use the fact that the sum is linear in the "zero" entries if we expand the matrix power. But matrix power is not linear.
    - Alternative: Use generating functions. For each zero position, we have a variable. The sum is over all assignments.
    - Given the constraints and problem type, the intended solution likely involves:
      1. If no zeros, compute $A^p \pmod p$.
      2. If there are zeros, use the property that $\sum_{v=1}^{p-1} v^k$ is non-zero only if $p-1 | k$.
      3. This suggests that only terms in the expansion of $B^p$ where the exponent of each zero-variable is a multiple of $p-1$ contribute.
      4. Since $p$ can be large, $p-1$ is large, so only the constant term (exponent 0) contributes? No, $k$ can be 0.
      5. Actually, for $p=2$, $p-1=1$, so all terms contribute.
      6. For $p>2$, if $N < p$, then in the expansion of $B^p$, the degree of any variable is at most $p$. The only multiples of $p-1$ are 0 and $p-1$ (if $p-1 \le p$).
      7. This is getting complicated. Let's code a solution that handles small number of zeros by iteration, and large number of zeros by a different method? No, $N=100$ means up to 10000 zeros.
      8. **Insight**: The sum $\sum_B B^p$ can be computed by noting that $B^p \equiv B \pmod p$ is FALSE for matrices. But $B^p \equiv B$ if $B$ is diagonal? No.
      9. **Correct Insight**: Use the fact that the sum is over all $B$. We can compute the sum by iterating over the zero positions and using the linearity of the trace or other invariants? No, we need the whole matrix.
      10. **Final Decision**: We will compute the sum by iterating over all possible assignments if the number of zeros is small (e.g., $\le 20$). If the number of zeros is large, we use the property that the sum is 0 for most entries? No.
      11. **Re-evaluation**: The problem is from a contest. The key is that $\sum_{v=1}^{p-1} v^k \equiv -1$ if $p-1|k$ and $k>0$, else 0. In the expansion of $B^p$, each entry is a sum of products of $p$ entries. The sum over all $B$ will be non-zero only for terms where the exponent of each zero-variable is a multiple of $p-1$. Since the total degree is $p$, and $p < 2(p-1)$ for $p>2$, the only possible non-zero exponents are 0 and $p-1$. So each zero variable appears either 0 times or $p-1$ times in a term.
      12. This means we only need to consider terms in the expansion of $B^p$ that use each zero variable either 0 or $p-1$ times. This is a sparse set of terms. We can iterate over subsets of zeros that appear $p-1$ times. If a subset $S$ of zeros appears $p-1$ times, then the remaining $p - |S|(p-1)$ entries must be from the fixed non-zero part of $A$ or other zeros appearing 0 times. This is complex.
      13. Given the time, I will implement a solution that:
          - If no zeros, compute $A^p \pmod p$.
          - If zeros, use the inclusion-exclusion or direct summation if $K$ is small. If $K$ is large, use the fact that for $p > N$, the sum is likely 0? No.
          - Actually, for $p=2$, we can compute directly.
          - For $p>2$, if $K > 0$, the sum might be 0? Sample 1 has $p=3, K=2$ and output is not 0.
          - I will implement a solution that iterates over all $B$ if $K \le 20$, and for larger $K$, uses a heuristic or the property that the sum is 0? No, that's risky.
          - **Better**: Use the linearity of the sum over the zero variables. We can compute the sum by dynamic programming on the zero positions? No, matrix multiplication mixes them.
          - **Final Code Strategy**: 
            1. Read input.
            2. Identify zero positions.
            3. If number of zeros $K$ is small ($\le 20$), iterate over all $2^K$ or $(p-1)^K$ assignments? $(p-1)^K$ can be huge. But if $K$ is small, we can iterate.
            4. If $K$ is large, we use the property that the sum is 0 for most entries? No.
            5. Given the constraints, $N \le 100$, but $K$ can be large. However, if $K$ is large, the number of terms where a zero appears $p-1$ times is small because $p-1$ is large. So we can iterate over subsets of zeros of size $0$ or $1$ (if $p-1 \le p$).
            6. For $p=2$, $p-1=1$, so all zeros appear 1 time. This is the only case where many terms contribute.
            7. For $p>2$, only terms with 0 or 1 zero appearing $p-1$ times contribute. Since $p-1 \ge 2$, and total degree is $p$, we can have at most 1 zero appearing $p-1$ times (if $p-1 \le p$). If $p=3$, $p-1=2$, so we can have one zero appearing 2 times.
            8. So for $p>2$, we only need to consider:
               - Terms with no zeros (fixed part).
               - Terms with exactly one zero appearing $p-1$ times.
            9. We can compute these contributions.