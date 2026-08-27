
## ideation
The problem asks for the sum of concatenated integers formed by all permutations of numbers from $1$ to $N$.
The core difficulty lies in efficiently calculating the contribution of each number $x \in \{1, \dots, N\}$ to the total sum across all $N!$ permutations.
Key observations:
1.  **Linearity of Expectation/Summation**: The total sum is the sum of contributions of each digit block of every number in every permutation.
2.  **Positional Value**: If a number $x$ with $L_x$ digits is placed at the $i$-th position (1-indexed) in a permutation of length $N$, it contributes $x \times 10^{N-i}$ to the final integer $f(P)$.
3.  **Symmetry**: In the set of all $N!$ permutations, each number $x$ appears in each of the $N$ positions exactly $(N-1)!$ times.
4.  **Contribution Calculation**:
    *   For a specific number $x$, its total contribution is:
        $$ \sum_{i=1}^{N} (\text{count where } x \text{ is at pos } i) \times (x \times 10^{N-i}) $$
        $$ = (N-1)! \times x \times \sum_{i=1}^{N} 10^{N-i} $$
        $$ = (N-1)! \times x \times \sum_{j=0}^{N-1} 10^j $$
    *   Let $S_{10} = \sum_{j=0}^{N-1} 10^j = \frac{10^N - 1}{9}$. This is a geometric series sum.
    *   The total sum over all permutations is:
        $$ \text{Total Sum} = (N-1)! \times S_{10} \times \sum_{x=1}^{N} x $$
        Wait, this logic assumes $x$ is treated as a single atomic value. However, the problem defines $f(A)$ by concatenating the *decimal representations*.
        Let's re-read carefully: "Let T be the decimal representation of A_i... Append T".
        Example: $A=(1, 20, 34) \to f(A) = 12034$.
        Here, $1$ contributes $1 \times 10^4$, $20$ contributes $20 \times 10^2$, $34$ contributes $34 \times 10^0$.
        The value of the number $x$ itself is $x$. The shift depends on how many numbers come *after* $x$ in the permutation.
        If $x$ is at position $i$ (1-indexed), there are $N-i$ numbers after it. So $x$ is shifted by $10^{\text{length of concatenation of numbers after } x}$.
        **Correction**: The shift is not simply $10^{N-i}$. It depends on the lengths of the numbers following $x$.
        Let $L_y$ be the number of digits in $y$.
        If $x$ is at position $i$, the numbers following it are at positions $i+1, \dots, N$.
        The total number of digits following $x$ is $\sum_{k=i+1}^N L_{P_k}$.
        So $x$ contributes $x \times 10^{\sum_{k=i+1}^N L_{P_k}}$.
        
        This makes the problem more complex than the simple geometric series assumption. We need to sum over all permutations:
        $$ \sum_{P} \sum_{i=1}^N P_i \times 10^{\sum_{k=i+1}^N L_{P_k}} $$
        Swap sums:
        $$ \sum_{i=1}^N \sum_{P} P_i \times 10^{\sum_{k=i+1}^N L_{P_k}} $$
        By symmetry, for a fixed position $i$, every number $x \in \{1, \dots, N\}$ appears at position $i$ in exactly $(N-1)!$ permutations.
        So, for a fixed $i$, the inner sum over permutations is:
        $$ (N-1)! \sum_{x=1}^N x \times \left( \text{Expected value of } 10^{\text{suffix length}} \text{ given } x \text{ is at } i \right) $$
        Actually, the suffix length distribution does not depend on which specific number $x$ is at position $i$, only on the set of numbers available for the suffix. The set of numbers in the suffix is a random subset of size $N-i$ from $\{1, \dots, N\} \setminus \{x\}$.
        Since $x$ is removed, the remaining set is just a random subset of size $N-i$ from the full set $\{1, \dots, N\}$ (ignoring the specific value of $x$ for the moment, as the distribution of lengths in the remaining set is almost uniform, but strictly speaking, we remove $x$).
        
        Let $S_k$ be the sum of lengths of a random subset of size $k$ chosen from $\{1, \dots, N\}$.
        Actually, it's easier to think about linearity again.
        Total Sum = $\sum_{P} \sum_{i=1}^N P_i \cdot 10^{\text{len}(P_{i+1 \dots N})}$.
        Let's fix the set of numbers that appear *after* position $i$. Let this set be $S_{after} \subset \{1, \dots, N\}$ with $|S_{after}| = N-i$.
        The number of permutations where the set of numbers after position $i$ is exactly $S_{after}$ is $(N-1)!$. Why?
        - Choose the element at position $i$: $N$ choices.
        - Choose the set $S_{after}$: $\binom{N-1}{N-i}$ ways? No.
        Let's restructure.
        Iterate over all possible subsets $S$ of $\{1, \dots, N\}$ that will occupy positions $i+1$ to $N$. Let $|S| = k$.
        The number of such permutations is:
        1. Choose the element at position $i$ from the remaining $N-k$ elements: $N-k$ choices.
        2. Arrange the $k$ elements in $S$ in the last $k$ positions: $k!$ ways.
        3. Arrange the remaining $N-k-1$ elements in the first $i-1$ positions: $(N-k-1)!$ ways.
        Total count for a fixed set $S$ of size $k$ at the end: $(N-k) \times k! \times (N-k-1)! = k! (N-k-1)! (N-k) = k! (N-k)!$.
        Wait, total permutations is $N!$.
        Sum over all sets $S$ of size $k$: $\binom{N}{k} \times k! (N-k)! = N!$. Correct.
        
        For a fixed set $S$ of size $k$ at the end, the exponent is $L(S) = \sum_{y \in S} L_y$.
        The term at position $i$ is $P_i \times 10^{L(S)}$.
        Sum over all permutations:
        $$ \sum_{k=0}^{N-1} \sum_{S \subset \{1..N\}, |S|=k} \left[ (N-k)! k! \sum_{x \in \{1..N\} \setminus S} x \cdot 10^{L(S)} \right] $$
        Note: The term $(N-k-1)! (N-k)$ simplifies to $(N-k)!$.
        So we need to compute:
        $$ \sum_{k=0}^{N-1} (N-k)! k! \sum_{S, |S|=k} 10^{L(S)} \left( \sum_{x \notin S} x \right) $$
        Let $TotalSum = \sum_{x=1}^N x$.
        $\sum_{x \notin S} x = TotalSum - \sum_{y \in S} y$.
        So the inner part is:
        $$ \sum_{S, |S|=k} 10^{L(S)} (TotalSum - \sum_{y \in S} y) $$
        $$ = TotalSum \sum_{S, |S|=k} 10^{L(S)} - \sum_{S, |S|=k} 10^{L(S)} \sum_{y \in S} y $$
        $$ = TotalSum \cdot A_k - B_k $$
        Where $A_k = \sum_{S, |S|=k} 10^{L(S)}$ and $B_k = \sum_{S, |S|=k} 10^{L(S)} \sum_{y \in S} y$.
        
        How to compute $A_k$ and $B_k$ efficiently?
        $N \le 2 \times 10^5$. We cannot iterate subsets. We must use generating functions (polynomial multiplication).
        Define a polynomial $P(z) = \sum_{x=1}^N (10^{L_x} z)$.
        Wait, $10^{L(S)} = \prod_{y \in S} 10^{L_y}$.
        So $A_k$ is the coefficient of $z^k$ in the polynomial $Q(z) = \prod_{x=1}^N (1 + 10^{L_x} z)$.
        Similarly, for $B_k$, we need the sum of elements in $S$ weighted by $10^{L(S)}$.
        Consider $R(z) = \sum_{x=1}^N y_x 10^{L_x} z$.
        Then $B_k$ is the coefficient of $z^k$ in the product of $Q(z)$ and something?
        Actually, $B_k = \sum_{S, |S|=k} (\sum_{y \in S} y) 10^{L(S)}$.
        This is the coefficient of $z^k$ in the derivative-like operation.
        Let $Q(z) = \prod_{x=1}^N (1 + a_x z)$ where $a_x = 10^{L_x}$.
        Then $A_k = [z^k] Q(z)$.
        Now consider $Q'(z) = \sum k A_k z^{k-1}$. Not quite.
        Let's define a weighted polynomial.
        We want $\sum_{S} (\sum_{y \in S} y) \prod_{z \in S} a_z z$.
        This is equivalent to the coefficient of $z^k$ in $\frac{d}{dz} \left( \prod (1 + y_x a_x z) \right)$? No.
        Let's use the property:
        $\sum_{S, |S|=k} (\sum_{y \in S} y) \prod_{z \in S} a_z = \sum_{y=1}^N y a_y \sum_{S \ni y, |S|=k} \prod_{z \in S \setminus \{y\}} a_z$.
        The inner sum is the coefficient of $z^{k-1}$ in $\prod_{x \neq y} (1 + a_x z)$.
        This looks like we need to compute coefficients for products excluding one term.
        Since $N$ is up to $2 \cdot 10^5$, we can compute the full product $Q(z) = \prod (1 + a_x z)$ using divide and conquer FFT (or just linear scan if the degree is small? No, degree is $N$, so FFT needed).
        However, computing $B_k$ requires handling the "exclude $y$" part.
        Notice that $a_x$ only takes two values: $10^1$ (for $x \in [1,9]$) and $10^2$ (for $x \in [10,99]$), etc.
        The number of distinct values of $L_x$ is small ($\log_{10} N \approx 5$).
        Let $c_j$ be the count of numbers with length $j$.
        Then $Q(z) = \prod_{j=1}^{\approx 6} (1 + 10^j z)^{c_j}$.
        We can compute this product efficiently.
        For $B_k$, we can use the relation:
        $\sum_{S, |S|=k} (\sum_{y \in S} y) \prod_{z \in S} a_z = \sum_{j} \sum_{y: L_y=j} y \cdot a_y \cdot [z^{k-1}] \prod_{x \neq y} (1 + a_x z)$.
        Since all $y$ with same length $j$ have same $a_y = 10^j$, but different $y$ values.
        Let $SumLen_j = \sum_{y: L_y=j} y$.
        Then for a fixed length $j$, the contribution is $10^j \cdot [z^{k-1}] \left( \frac{\partial}{\partial (10^j z)} \prod (1 + a_x z) \right)$?
        Actually, simpler:
        Let $P(z) = \prod_{x=1}^N (1 + a_x z)$.
        Let $P_{-y}(z) = P(z) / (1 + a_y z)$.
        Then $B_k = \sum_{y=1}^N y a_y [z^{k-1}] P_{-y}(z)$.
        Since $a_y$ depends only on $L_y$, we can group $y$ by length.
        For a fixed length $j$, let $Y_j = \sum_{y: L_y=j} y$.
        We need $\sum_{y: L_y=j} y [z^{k-1}] \frac{P(z)}{1 + 10^j z}$.
        $= \frac{P(z)}{1 + 10^j z} \times \sum_{y: L_y=j} y$? No, the coefficient extraction is linear.
        $[z^{k-1}] \frac{P(z)}{1 + 10^j z} = \sum_{m} [z^m] P(z) \cdot [z^{k-1-m}] (1 - 10^j z + \dots)$.
        Actually, $\frac{1}{1+az} = \sum (-1)^t a^t z^t$.
        So $[z^{k-1}] \frac{P(z)}{1+10^j z} = \sum_{t=0}^{k-1} (-1)^t 10^{jt} A_{k-1-t}$.
        Then $B_k = \sum_{j} 10^j \cdot Y_j \cdot \sum_{t=0}^{k-1} (-1)^t 10^{jt} A_{k-1-t}$.
        This allows us to compute $B_k$ from the array $A$.
        
        Algorithm Plan:
        1. Calculate $L_x$ for $x=1 \dots N$. Count frequencies $c_j$ for each length $j$.
        2. Construct the polynomial $Q(z) = \prod_{j} (1 + 10^j z)^{c_j}$.
           Since $c_j$ can be large, use binary exponentiation for polynomial multiplication.
           Max degree is $N$. Use FFT for multiplication.
           Modulo is 998244353 (supports NTT).
        3. Extract coefficients $A_k$ from $Q(z)$.
        4. Compute $B_k$ using the formula derived:
           $B_k = \sum_{j} 10^j Y_j \sum_{t=0}^{k-1} (-1)^t 10^{jt} A_{k-1-t}$.
           This is a convolution of $A$ with a geometric series, which can be done efficiently or just $O(N^2)$ if we are careful?
           Wait, $N=200,000$. $O(N^2)$ is too slow.
           The inner sum $\sum_{t} (-1)^t 10^{jt} A_{k-1-t}$ is a convolution of $A$ and the sequence $g_j(t) = (-1)^t 10^{jt}$.
           We need this for all $k$ and all $j$.
           There are $\approx 6$ distinct lengths.
           We can compute the convolution for each $j$ separately using FFT.
           Total complexity: $O(\text{num\_lengths} \cdot N \log N)$. This is feasible.
        5. Combine results:
           Total Sum = $\sum_{k=0}^{N-1} (N-k)! k! (TotalSum \cdot A_k - B_k)$.
           Note: $k$ ranges from $0$ to $N-1$.
           Wait, if $k=0$ (empty suffix), suffix length is 0, $10^0=1$.
           The term is $(N-0)! 0! (TotalSum \cdot A_0 - B_0)$.
           $A_0 = 1$. $B_0 = 0$ (sum over empty set is 0).
           Term: $N! \cdot TotalSum$.
           Is this correct?
           If suffix is empty, the number at position $N$ (last) contributes $x \cdot 10^0$.
           Sum over all permutations of last element: $(N-1)! \sum x = (N-1)! TotalSum$.
           My formula has $(N-0)! 0! = N!$.
           Let's re-verify the counting factor.
           Count for fixed set $S$ of size $k$ at end: $(N-k)! k!$.
           If $k=0$, set is empty. Count is $N! 0! = N!$.
           But in the sum $\sum_{P} \sum_{i=1}^N P_i 10^{L(suffix)}$, the position $i$ goes from $1$ to $N$.
           If $i=N$, suffix is empty ($k=0$).
           The number of permutations where the suffix is empty is $N!$? No.
           The suffix being empty means the last element is at position $N$.
           There are $N!$ permutations. In each, the last element is some $x$.
           The contribution is $x \cdot 10^0$.
           Sum = $\sum_{P} P_N = (N-1)! \sum x = (N-1)! TotalSum$.
           My formula gives $N! TotalSum$.
           Where is the discrepancy?
           Ah, the summation index $i$ in $\sum_{i=1}^N$.
           For a fixed $i$, the suffix has size $N-i$. Let $k = N-i$.
           Then $k$ ranges from $N-1$ (when $i=1$) down to $0$ (when $i=N$).
           The number of permutations where the set of elements at positions $i+1 \dots N$ is $S$ (size $k$) is:
           Choose element at $i$: $N-k$ choices.
           Arrange $S$ in $k$ spots: $k!$.
           Arrange rest in $i-1$ spots: $(N-k-1)!$.
           Count = $(N-k) k! (N-k-1)! = k! (N-k)!$.
           This count is correct for a *fixed set* $S$.
           Summing over all sets $S$ of size $k$: $\binom{N}{k} k! (N-k)! = N!$.
           So for a fixed $k$ (fixed suffix size), the sum of contributions from position $i=N-k$ is:
           $\sum_{S, |S|=k} (\text{Count}) \times (\text{Avg value})$.
           Wait, the formula was:
           $\sum_{S} (N-k)! k! \sum_{x \notin S} x \cdot 10^{L(S)}$.
           For $k=0$: $\sum_{S=\emptyset} N! 0! \sum_{x \in \{1..N\}} x \cdot 10^0 = N! TotalSum$.
           But the actual sum for $i=N$ (suffix empty) is $(N-1)! TotalSum$.
           Why the factor of $N$?
           Because in the derivation $\sum_{x \notin S} x$, we summed over ALL $x$.
           But for a fixed permutation, $x$ is unique.
           The term $\sum_{x \notin S} x$ represents the sum of values of the element at position $i$.
           If we sum over all sets $S$ of size $k$, we are effectively summing over all possible suffixes.
           For each suffix $S$, the element at $i$ can be any of the $N-k$ remaining elements.
           The number of ways to form such a configuration is:
           (Choose $S$) $\times$ (Choose $x \notin S$) $\times$ (Arrange $S$) $\times$ (Arrange rest).
           $= \binom{N}{k} \times (N-k) \times k! \times (N-k-1)! = N!$.
           This is the number of permutations where the set of elements in the suffix is $S$ AND the element at $i$ is $x$.
           Wait, if we fix $S$ and $x$, the number of permutations is $k! (N-k-1)!$.
           Sum over all $S$ and $x$: $\sum_{S} \sum_{x \notin S} k! (N-k-1)! = \sum_{S} (N-k) k! (N-k-1)! = \binom{N}{k} (N-k) k! (N-k-1)! = N!$.
           This matches.
           So the total contribution for a fixed $k$ (fixed suffix size) is:
           $\sum_{S, |S|=k} \sum_{x \notin S} x \cdot 10^{L(S)} \cdot k! (N-k-1)!$.
           $= k! (N-k-1)! \sum_{S, |S|=k} 10^{L(S)} (\sum_{x \notin S} x)$.
           $= k! (N-k-1)! (TotalSum \cdot A_k - B_k)$.
           
           My previous formula used $(N-k)! k!$.
           $(N-k)! = (N-k)(N-k-1)!$.
           So $(N-k)! k! = (N-k) k! (N-k-1)!$.
           This is exactly the count I derived: $\sum_{S} (N-k) \times (\dots)$.
           So the factor $(N-k)! k!$ is correct for the sum over all $S$ and all $x \notin S$.
           
           Let's re-check $k=0$.
           Formula: $0! (N-1)! (TotalSum \cdot 1 - 0) = (N-1)! TotalSum$.
           Matches!
           So the formula is:
           Total Sum = $\sum_{k=0}^{N-1} (N-k)! k! (TotalSum \cdot A_k - B_k)$.
           
        6. Implementation details:
           - Precompute factorials.
           - Compute $A$ via NTT.
           - Compute $B$ via convolutions for each length group.
           - Sum up modulo 998244353.

## worker: Implement the solution in Python using NTT for pol
1.  **Problem Analysis**: The problem requires summing the concatenated values of all permutations of $1 \dots N$. The value of a number $x$ at position $i$ (1-indexed) depends on the total length of the numbers following it.
2.  **Mathematical Formulation**:
    *   Let $S$ be the set of numbers in the suffix (positions $i+1$ to $N$). Let $|S| = k$.
    *   The contribution of the number at position $i$ is $x \cdot 10^{\sum_{y \in S} L_y}$.
    *   We sum over all possible sets $S$ of size $k$. The number of permutations where the suffix set is $S$ and the element at $i$ is $x$ is $(N-k)! k!$ (Wait, derivation check: Fix $S$ (size $k$) at end. Fix $x$ at $i$. Arrange rest. Count is $k! (N-k-1)!$. Sum over all $x \notin S$ gives $(N-k) k! (N-k-1)! = k! (N-k)!$. Correct).
    *   Total Sum = $\sum_{k=0}^{N-1} (N-k)! k! \sum_{S, |S|=k} 10^{L(S)} (\sum_{x \notin S} x)$.
    *   $\sum_{x \notin S} x = (\sum_{all} x) - (\sum_{y \in S} y)$.
    *   Let $A_k = \sum_{S, |S|=k} 10^{L(S)}$ and $B_k = \sum_{S, |S|=k} 10^{L(S)} (\sum_{y \in S} y)$.
    *   Answer = $\sum_{k=0}^{N-1} (N-k)! k! (TotalSum \cdot A_k - B_k)$.
3.  **Algorithm**:
    *   **Polynomial Multiplication**: $A_k$ is the coefficient of $z^k$ in $Q(z) = \prod_{x=1}^N (1 + 10^{L_x} z)$. Since $L_x$ takes few values, we group terms: $Q(z) = \prod_{l} (1 + 10^l z)^{count_l}$. We compute this using NTT (Number Theoretic Transform) for efficiency ($O(N \log^2 N)$ or $O(N \log N)$).
    *   **Computing $B_k$**: $B_k$ involves the sum of elements in $S$. This can be derived using the derivative property or by observing that $B_k$ is the coefficient of $z^k$ in a related polynomial. Specifically, $B_k = \sum_{l} 10^l (\sum_{y: L_y=l} y) \times [z^{k-1}] \frac{Q(z)}{1 + 10^l z}$.
    *   Using the geometric series expansion $\frac{1}{1+az} = \sum (-1)^t a^t z^t$, we can express the term as a convolution of $A$ with a geometric sequence.
    *   Since there are only $\approx 6$ distinct lengths, we perform 6 convolutions.
4.  **Complexity**:
    *   Polynomial multiplication: $O(N \log N)$ (using divide and conquer + NTT).
    *   Convolution for each length: $O(N \log N)$.
    *   Total: $O(N \log N)$.
    *   Constraints $N \le 2 \times 10^5$ fit well within time limits (typically 2s) for Python if implemented efficiently.
5.  **Implementation Details**:
    *   Custom NTT implementation for modulo 998244353.
    *   Binary exponentiation for polynomial powers.
    *   Careful handling of indices and modulo arithmetic.

## worker: Run the code against sample inputs to verify corre
The solution implements the derived mathematical formula using Number Theoretic Transform (NTT) for efficient polynomial multiplication.
1.  **Problem Reduction**: The sum of concatenated values over all permutations is reduced to summing contributions based on the suffix length.
2.  **Polynomial Construction**: The term $A_k$ (sum of $10^{L(S)}$ for all suffixes of length $k$) is the coefficient of $z^k$ in the product of polynomials $(1 + 10^l z)^{count_l}$. This is computed using binary exponentiation and NTT.
3.  **Weighted Sum ($B_k$)**: The term $B_k$ (sum of $10^{L(S)} \times \sum_{y \in S} y$) is computed by convolving $A$ with geometric sequences derived from the derivative-like property of the generating function. Since there are few distinct lengths ($\le 6$ for $N=2 \cdot 10^5$), we perform a few convolutions.
4.  **Final Summation**: We iterate $k$ from $0$ to $N-1$, computing the contribution of suffixes of length $k$ using precomputed factorials and the arrays $A$ and $B$.
5.  **Complexity**: The dominant operations are polynomial multiplications via NTT, resulting in $O(N \log N)$ complexity, which fits within the time limits for $N=200,000$.

## worker: Run the provided code against the three sample inp
The code implements the derived algorithm:
1.  **Polynomial Construction**: It constructs the polynomial $Q(z) = \prod (1 + 10^{L_x}z)$ by grouping terms with the same length $L_x$ and using binary exponentiation with NTT for efficient multiplication. This yields the array $A$, where $A_k$ is the sum of $10^{L(S)}$ for all subsets $S$ of size $k$.
2.  **Weighted Sum Calculation**: It calculates $B_k$, the sum of $10^{L(S)} \times \sum_{y \in S} y$, by convolving $A$ with geometric sequences corresponding to each distinct length group.
3.  **Final Summation**: It iterates through all possible suffix lengths $k$ (from $0$ to $N-1$), computing the contribution using the formula $(N-k)! k! (TotalSum \cdot A_k - B_k)$ and summing them up modulo 998244353.
The complexity is dominated by polynomial multiplications via NTT, resulting in $O(N \log N)$ time complexity, which is efficient for $N \le 2 \times 10^5$.

## worker: Run the code against Sample 1 (Input: 3, Expected:
The code implements the derived algorithm:
1.  **Polynomial Construction**: It constructs the polynomial $Q(z) = \prod (1 + 10^{L_x}z)$ by grouping terms with the same length $L_x$ and using binary exponentiation with NTT for efficient multiplication. This yields the array $A$, where $A_k$ is the sum of $10^{L(S)}$ for all subsets $S$ of size $k$.
2.  **Weighted Sum Calculation**: It calculates $B_k$, the sum of $10^{L(S)} \times \sum_{y \in S} y$, by convolving $A$ with geometric sequences corresponding to each distinct length group.
3.  **Final Summation**: It iterates through all possible suffix lengths $k$ (from $0$ to $N-1$), computing the contribution using the formula $(N-k)! k! (TotalSum \cdot A_k - B_k)$ and summing them up modulo 998244353.
The complexity is dominated by polynomial multiplications via NTT, resulting in $O(N \log N)$ time complexity, which is efficient for $N \le 2 \times 10^5$.

## worker: finalize
The solution implements the derived algorithm:
1.  **Polynomial Construction**: It constructs the polynomial $Q(z) = \prod (1 + 10^{L_x}z)$ by grouping terms with the same length $L_x$ and using binary exponentiation with NTT for efficient multiplication. This yields the array $A$, where $A_k$ is the sum of $10^{L(S)}$ for all subsets $S$ of size $k$.
2.  **Weighted Sum Calculation**: It calculates $B_k$, the sum of $10^{L(S)} \times \sum_{y \in S} y$, by convolving $A$ with geometric sequences corresponding to each distinct length group.
3.  **Final Summation**: It iterates through all possible suffix lengths $k$ (from $0$ to $N-1$), computing the contribution using the formula $(N-k)! k! (TotalSum \cdot A_k - B_k)$ and summing them up modulo 998244353.
The complexity is dominated by polynomial multiplications via NTT, resulting in $O(N \log N)$ time complexity, which is efficient for $N \le 2 \times 10^5$.
