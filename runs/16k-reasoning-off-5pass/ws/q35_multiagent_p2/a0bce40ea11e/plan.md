1. **Key Insight**: By Fermat's Little Theorem, for any scalar $x$, $x^p \equiv x \pmod p$. However, this does not directly apply to matrices. But we can use the linearity of expectation/sum and properties of matrix powers modulo $p$.
2. **Linearity and Independence**: The sum $\sum_B B^p$ can be computed by considering each entry of $B^p$ separately. Since the replacements for zeros are independent, we can use generating functions or combinatorial arguments.
3. **Critical Observation**: For a prime $p$, and a matrix $B$ with entries in $\mathbb{F}_p$, if we sum $B^p$ over all possible replacements of zeros, we can leverage the fact that the map $x \mapsto x^p$ is the identity on $\mathbb{F}_p$. However, matrix multiplication is non-commutative and complex.
4. **Simpler Approach using Linear Algebra**: Notice that $B^p \pmod p$ for a matrix $B$ over $\mathbb{F}_p$ is not simply $B$. But there is a known result: if we sum $B^k$ over all $B$ in a certain space, symmetries often kill off terms.
5. **Refined Insight**: Actually, for any matrix $B$ over $\mathbb{F}_p$, $B^p$ is not necessarily $B$. However, consider the sum over all possible values. The key is that the replacements are uniform over $\{1, \dots, p-1\}$. The sum of $x^k$ for $x \in \{1, \dots, p-1\}$ is $-1$ if $p-1 \mid k$ and $0$ otherwise (for $k \ge 1$).
6. **Final Strategy**: The problem is equivalent to computing the sum of $B^p$ where each zero is replaced by $x \in \{1, \dots, p-1\}$. Due to the high power $p$, and the structure of the sum, most terms vanish. Specifically, it turns out that the sum is diagonal-like or zero in many cases. However, a more robust method is to realize that for $p > N$, the sum might be zero, but for small $p$, it's complex.
7. **Correct Mathematical Approach**: Use the fact that $\sum_{x=1}^{p-1} x^k \equiv -1 \pmod p$ if $(p-1) \mid k$ and $0$ otherwise. The entries of $B^p$ are polynomials in the entries of $B$. We need to sum these polynomials. Since $N$ is small ($N \le 100$), but $p$ is large, we cannot iterate. However, note that if any zero is replaced, the term involves powers of the replacement variable. If the total degree of a variable in a term is not a multiple of $p-1$, the sum over that variable is 0.
8. **Practical Solution**: Given the constraints and the nature of competitive programming problems, there is a trick. For $B^p$, if we consider the sum over all $B$, the result is often related to the original matrix $A$ with zeros handled specially. In fact, for many such problems, the answer is $0$ unless the matrix has specific structure. Let's look at Sample 1: Output is `0 2 / 1 2`. Sample 2: All 1s.
9. **Re-evaluating**: Actually, a known result is that $\sum_{B} B^p \equiv 0 \pmod p$ for many cases, but not all. The correct approach is to use the linearity and the fact that the sum of $x^k$ over $x \in \mathbb{F}_p^*$ is $-1$ if $p-1 \mid k$ else $0$. We can expand $B^p$ using the multinomial theorem or by considering the contribution of each path in the matrix multiplication. Since $p$ can be large, we only care about terms where the exponent of each variable is a multiple of $p-1$.
10. **Implementation Plan**: Given $N \le 100$, we can't do exponential work. However, note that if $p > N$, then $p-1 > N-1$. The degree of any entry in $B^p$ is $p$. If $p > N$, it's possible that no single variable appears with degree $p$ (since max degree in a product of $p$ matrices is limited by the path length, but actually each entry of $B^p$ is a sum of products of $p$ entries). Wait, the degree of each term in $(B^p)_{i,j}$ is exactly $p$. For the sum over a variable $x$ (replacing a zero) to be non-zero, the exponent of $x$ in that term must be a multiple of $p-1$. Since the total degree is $p$, the exponent of $x$ can be $0, 1, \dots, p$. The only multiples of $p-1$ in this range are $0$ and $p-1$ (if $p-1 \le p$, which is true). So we need terms where $x$ appears with exponent $0$ or $p-1$.
    - If exponent is $0$: The term does not depend on $x$. Summing over $x \in \{1, \dots, p-1\}$ gives $(p-1) \times \text{term} \equiv -1 \times \text{term}$.
    - If exponent is $p-1$: Sum is $\sum_{x=1}^{p-1} x^{p-1} \equiv \sum_{x=1}^{p-1} 1 = p-1 \equiv -1$.
    - If exponent is $p$: Sum is $\sum_{x=1}^{p-1} x^p = \sum x \equiv 0$ (since $p \ge 2$, sum of $1 \dots p-1$ is $p(p-1)/2 \equiv 0$ if $p>2$, and if $p=2$, $1^2=1$, sum=1, but $p-1=1$, so exponent 1 is multiple of 1. Wait. For $p=2$, $p-1=1$. Exponents $0,1,2$. Multiples of 1: all. So all terms contribute.
    
    This is getting complex. Let's use a simpler observation: **If $p > N$, the answer is often 0 or related to diagonal**. But Sample 1 has $p=3, N=2$ and non-zero output.
    
    Actually, there is a much simpler property: **For any matrix $B$ over $\mathbb{F}_p$, $B^p \equiv B^{(p)} \pmod p$ is not helpful. But consider the sum.**
    
    Let's just implement the brute force for small $N$ and small $p$ to find a pattern? No, $p$ is large.
    
    **Correct Insight**: The sum $\sum_B B^p$ is equal to $0$ if there is at least one zero in the matrix? No, Sample 1 has zeros and non-zero output.
    
    Let's look at the structure. The problem is from a contest. The solution involves **linear algebra over finite fields** and **generating functions**.
    
    However, a known result for this specific problem (AtCoder ABC 274 F or similar) is that the answer is **0** for all entries if $p > N$ and there is at least one zero? No.
    
    Let's try a different angle. **If $p=2$**, $B^2$ sum. Sample 2: $N=3, p=2$. Output all 1s.
    
    Given the complexity, I will provide a solution that uses the property:
    $\sum_{x=1}^{p-1} x^k \equiv -1 \pmod p$ if $(p-1) \mid k$ and $k>0$, and $p-1 \equiv -1$ if $k=0$.
    
    We can compute the polynomial for each entry of $B^p$ symbolically? No, degree $p$ is too high.
    
    **Final Plan**: Use the fact that for $p > N$, the only terms that survive are those where each variable's exponent is 0 or $p-1$. Since the total degree is $p$, and $p-1 > N-1$ (for $p > N+1$), it's impossible to have a variable with exponent $p-1$ unless $N=1$. For $N=1$, $B=[x]$, $B^p = x^p = x$. Sum $x$ for $x=1..p-1$ is $-1$.
    
    For $N \ge 2$ and $p > N$, the answer is likely **0**.
    Let's check Sample 1: $N=2, p=3$. $p-1=2$. Degree 3. Exponents can be 2. $3 = 2+1$. So a term like $x^2 y$ has $x$ exponent 2 (multiple of 2). Sum over $x$: $-1 \cdot y$. Then sum over $y$: if $y$ is fixed, it's just $-y$. If $y$ is also a variable, we continue.
    
    I will write a solution that handles small $N$ and general $p$ by expanding the polynomial for small degrees if $p$ is small, and using the "zero if $p > N$" heuristic if $p$ is large? No, that's risky.
    
    Actually, for $N \le 100$, we can use **dynamic programming** or **matrix tree theorem** analogs? No.
    
    Let's just implement the **brute force for small $p$** and **theoretical zero for large $p$**?
    If $p > N$, is the answer always 0?
    Sample 1: $N=2, p=3$. $p > N$ is false ($3 > 2$). Answer non-zero.
    Sample 3: $N=4, p=13$. $13 > 4$. Output non-zero.
    So the "zero if $p > N$" hypothesis is **false**.

    I will provide a Python solution that uses the **generating function** approach with **multivariate polynomial multiplication** but truncated. Since $N$ is up to 100, this is still hard.
    
    Given the time, I'll provide a solution that works for the constraints by using the fact that we only need the sum modulo $p$.