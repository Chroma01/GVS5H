
## ideation
The core difficulty lies in correctly accounting for the varying lengths of decimal representations of numbers $1$ to $N$. A naive simulation is $O(N! \cdot N \cdot \log N)$, which is infeasible. The key insight is using linearity of expectation (or summation) over all permutations.

1.  **Decomposition**: The total sum is $\sum_{P} f(P)$. We can swap the summation order to consider the contribution of each number $k \in \{1, \dots, N\}$ to the total sum.
2.  **Contribution of a single number $k$**: In any permutation $P$, number $k$ appears at some position $i$. Its decimal string $T_k$ is appended to the current string. The value contributed by $k$ is $k \times 10^{L_{suffix}}$, where $L_{suffix}$ is the total number of digits in all numbers appearing *after* $k$ in the permutation.
3.  **Summing over permutations**:
    *   For a fixed $k$, it appears at any specific position in $(N-1)!$ permutations.
    *   However, the "suffix" consists of the other $N-1$ numbers in some order. The total number of digits in the suffix is the sum of the lengths of all numbers in $\{1, \dots, N\} \setminus \{k\}$.
    *   Crucially, the *order* of the suffix numbers does not affect the *total length* of the suffix, only their concatenation order. But wait, $f(P)$ depends on the concatenation.
    *   Let's re-evaluate. $f(P)$ is the integer formed by concatenating $P_1, P_2, \dots, P_N$.
    *   The contribution of $P_i$ to the final integer is $P_i \times 10^{\sum_{j=i+1}^N \text{len}(P_j)}$.
    *   Summing over all permutations $P$:
        $$ \text{Total Sum} = \sum_{P} \sum_{i=1}^N P_i \cdot 10^{\sum_{j=i+1}^N \text{len}(P_j)} $$
    *   Swap sums:
        $$ \text{Total Sum} = \sum_{i=1}^N \sum_{k=1}^N \sum_{P: P_i=k} k \cdot 10^{\sum_{j=i+1}^N \text{len}(P_j)} $$
    *   For a fixed $i$ and fixed $k$, there are $(N-1)!$ permutations where $P_i=k$. The suffix $P_{i+1}, \dots, P_N$ is a permutation of the set $S_k = \{1, \dots, N\} \setminus \{k\}$.
    *   The term $10^{\sum_{j=i+1}^N \text{len}(P_j)}$ depends only on the *set* of numbers in the suffix, not their order, because addition is commutative. The sum of lengths is constant for any permutation of the same set.
    *   The set of suffix numbers is always $S_k$. The size of the suffix is $N-i$.
    *   Wait, the suffix is a permutation of *all* remaining $N-1$ numbers if $i=1$? No, the suffix is the numbers at positions $i+1$ to $N$. The set of numbers in the suffix is a subset of size $N-i$ from $S_k$.
    *   This implies the previous "Key Insight" in the plan was slightly flawed or required careful interpretation. Let's look at the plan's conclusion:
        $$ \text{Answer} = (N-1)! \sum_{k=1}^N k \prod_{j \neq k} (1 + 10^{\text{len}(j)}) $$
        Let's verify this formula.
        The plan states: $\sum_{i=1}^N [\text{coeff of } y^{N-i} \text{ in } P_k(y)] = P_k(1)$.
        $P_k(y) = \prod_{j \neq k} (1 + y \cdot 10^{\text{len}(j)})$.
        The coefficient of $y^m$ in $P_k(y)$ is the sum of $10^{\text{total len of subset of size } m}$ over all subsets of size $m$ from $S_k$.
        In the permutation sum, for a fixed $k$ at position $i$, the suffix has size $N-i$. The numbers in the suffix are a random subset of size $N-i$ from $S_k$, and they are permuted.
        The contribution for a specific subset $S_{sub} \subset S_k$ of size $N-i$ is:
        Number of ways to choose the subset $\times$ Number of permutations of the subset $\times$ Number of permutations of the prefix.
        Actually, it's easier:
        Fix $k$ at position $i$. The remaining $N-1$ positions are filled by $S_k$.
        The positions $i+1 \dots N$ (suffix) contain a subset $S_{sub}$ of size $N-i$.
        The positions $1 \dots i-1$ (prefix) contain the remaining $S_k \setminus S_{sub}$ of size $i-1$.
        For a fixed subset $S_{sub}$, the number of permutations where the suffix is exactly the set $S_{sub}$ is $(i-1)! (N-i)!$.
        The term contributed is $k \cdot 10^{\sum_{j \in S_{sub}} \text{len}(j)}$.
        So, for fixed $k$ and fixed $i$, the sum over all permutations with $P_i=k$ is:
        $$ (i-1)! (N-i)! \cdot k \cdot \sum_{S_{sub} \subset S_k, |S_{sub}|=N-i} 10^{\sum_{j \in S_{sub}} \text{len}(j)} $$
        The inner sum is the coefficient of $y^{N-i}$ in $P_k(y) = \prod_{j \neq k} (1 + y \cdot 10^{\text{len}(j)})$.
        Let $C_{k, m}$ be the coefficient of $y^m$ in $P_k(y)$.
        Total Sum $= \sum_{k=1}^N k \sum_{i=1}^N (i-1)! (N-i)! C_{k, N-i}$.
        
        The plan simplified this to $(N-1)! \sum k \prod (1+10^{\text{len}(j)})$.
        This simplification assumes $\sum_{i=1}^N (i-1)! (N-i)! C_{k, N-i} = (N-1)! P_k(1)$.
        Is $\sum_{m=0}^{N-1} (N-1-m)! m! C_{k, m} = (N-1)! \sum_{m=0}^{N-1} C_{k, m}$?
        Generally, NO. $(N-1-m)! m!$ is not constant. It is maximized at $m \approx N/2$.
        So the plan's "Key Insight" derivation contains a logical error in the final step where it collapses the sum over positions. The weights $(i-1)! (N-i)!$ depend on the position $i$ (and thus the subset size $m=N-i$).

        **Correct Approach**:
        We need to compute $W_m = (N-1-m)! m!$ for each subset size $m$.
        Let $A_k = \sum_{m=0}^{N-1} W_{N-m} C_{k, m}$.
        Then Answer $= \sum_{k=1}^N k A_k$.
        
        Calculating $C_{k, m}$ for each $k$ is too slow ($O(N^2)$).
        However, note that $P_k(y)$ is almost the same for all $k$.
        Let $P(y) = \prod_{j=1}^N (1 + y \cdot 10^{\text{len}(j)})$.
        Then $P_k(y) = P(y) / (1 + y \cdot 10^{\text{len}(k)})$.
        
        We can compute the coefficients of $P(y)$ in $O(N \log N)$ or $O(N \cdot \max(\text{len}))$?
        The number of distinct lengths is small ($\le 6$ for $N \le 2 \cdot 10^5$).
        Let $Count_d$ be the number of integers in $1 \dots N$ with length $d$.
        $P(y) = \prod_{d} (1 + y \cdot 10^d)^{Count_d}$.
        We can compute the coefficients of $P(y)$ using divide and conquer or simply expanding the product since the degree is $N$.
        Since $N$ is up to $2 \cdot 10^5$, we can compute the polynomial $P(y)$ of degree $N$ in $O(N \log N)$ using FFT/NTT.
        
        Once we have coefficients $C_m$ of $P(y)$, we need $C_{k, m}$ for each $k$.
        $C_{k, m}$ is the coefficient of $y^m$ in $P(y) \cdot (1 + y \cdot 10^{\text{len}(k)})^{-1}$.
        This division is tricky.
        
        Alternative:
        Group numbers by length.
        Let $L$ be the set of lengths.
        For a number $k$ with length $d$, $P_k(y) = P(y) \cdot (1 + y \cdot 10^d)^{-1}$.
        Let $Q_d(y) = P(y) \cdot (1 + y \cdot 10^d)^{-1}$.
        We can compute $Q_d(y)$ for each distinct length $d$.
        There are only $\approx 6$ distinct lengths.
        For each $d$, we compute the polynomial $Q_d(y)$.
        Then for all $k$ with length $d$, the contribution is $k \cdot \sum_{m=0}^{N-1} W_{N-m} [y^m] Q_d(y)$.
        Let $S_d = \sum_{m=0}^{N-1} W_{N-m} [y^m] Q_d(y)$.
        Then Answer $= \sum_{d} S_d \sum_{k: \text{len}(k)=d} k$.
        
        How to compute $Q_d(y)$?
        $Q_d(y) (1 + y \cdot 10^d) = P(y)$.
        Let $Q_d(y) = \sum q_m y^m$.
        $q_m + 10^d q_{m-1} = C_m$ (coeff of $P(y)$).
        So $q_m = C_m - 10^d q_{m-1}$, with $q_{-1}=0$.
        This allows computing coefficients of $Q_d(y)$ in $O(N)$.
        
        Algorithm:
        1. Count frequencies of each length $d$ for numbers $1 \dots N$.
        2. Compute polynomial $P(y) = \prod_{d} (1 + y \cdot 10^d)^{Count_d}$.
           Since exponents are large, use binary exponentiation for polynomials? Or just multiply them out.
           Degree is $N$. Multiplication of two polynomials of degree $A$ and $B$ takes $O((A+B) \log (A+B))$.
           We can compute $P(y)$ by iteratively multiplying factors $(1 + y \cdot 10^d)$.
           Since there are only few distinct $d$, we can compute $(1 + y \cdot 10^d)^{Count_d}$ efficiently using binary exponentiation (square and multiply) in $O(N \log N \log Count_d)$.
           Then multiply these few polynomials together.
        3. For each distinct length $d$:
           a. Compute coefficients $q_m$ of $Q_d(y)$ using recurrence $q_m = C_m - 10^d q_{m-1}$.
           b. Compute $S_d = \sum_{m=0}^{N-1} (N-1-m)! m! q_m$.
           c. Compute sum of $k$ for all $k$ with length $d$.
           d. Add $S_d \times (\text{sum of } k)$ to total.
        4. Print total modulo 998244353.

        Complexity:
        - Computing $P(y)$: $O(N \log^2 N)$ or $O(N \log N)$ with careful implementation.
        - Computing $Q_d$: $O(N)$ per distinct length.
        - Total time: $O(N \log^2 N)$, which fits for $N=2 \cdot 10^5$.

## worker: Implement polynomial multiplication using NTT (Num
The problem asks for the sum of $f(P)$ over all permutations $P$ of $(1, \dots, N)$.
$f(P)$ is the integer formed by concatenating the decimal representations of the elements of $P$.

1.  **Linearity of Summation**: We can compute the total sum by considering the contribution of each number $k \in \{1, \dots, N\}$ to the final concatenated integer.
2.  **Contribution of $k$**: If $k$ is at position $i$ in a permutation, its value $k$ is shifted left by the total number of digits in all numbers appearing *after* it. Let $L_{suffix}$ be this total length. The contribution is $k \cdot 10^{L_{suffix}}$.
3.  **Summing over Permutations**: For a fixed $k$, it appears at any position $i$ in $(N-1)!$ permutations? No, more precisely, for a fixed position $i$ and fixed $k$, there are $(N-1)!$ permutations where $P_i = k$. However, the suffix length depends on *which* numbers are in the suffix.
4.  **Polynomial Formulation**:
    *   Let $len(j)$ be the number of digits in $j$.
    *   The sum of $10^{L_{suffix}}$ over all permutations where $k$ is at position $i$ (with suffix size $m = N-i$) involves summing $10^{\sum_{j \in S} len(j)}$ over all subsets $S$ of size $m$ from $\{1, \dots, N\} \setminus \{k\}$.
    *   This is the coefficient of $y^m$ in the polynomial $P_k(y) = \prod_{j \neq k} (1 + y \cdot 10^{len(j)})$.
    *   The total contribution of $k$ is $\sum_{i=1}^N (i-1)! (N-i)! \cdot k \cdot [y^{N-i}] P_k(y)$.
    *   Let $m = N-i$. The weight is $(N-1-m)! m!$.
    *   Total Sum $= \sum_{k=1}^N k \sum_{m=0}^{N-1} (N-1-m)! m! [y^m] P_k(y)$.
5.  **Efficient Computation**:
    *   Group numbers by length $d$. Let $Count_d$ be the count of numbers with length $d$.
    *   $P(y) = \prod_{d} (1 + y \cdot 10^d)^{Count_d}$.
    *   $P_k(y) = P(y) / (1 + y \cdot 10^{len(k)})$.
    *   For each distinct length $d$, we compute $Q_d(y) = P(y) / (1 + y \cdot 10^d)$.
    *   The coefficients $q_m$ of $Q_d(y)$ satisfy $q_m = C_m - 10^d q_{m-1}$, where $C_m$ are coefficients of $P(y)$.
    *   We compute $P(y)$ using NTT-based polynomial multiplication. Since there are few distinct lengths, we compute $(1 + y \cdot 10^d)^{Count_d}$ via binary exponentiation and multiply them.
    *   Finally, we sum the contributions for each length group.

Complexity: $O(N \log^2 N)$ due to polynomial multiplications.
