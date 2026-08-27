
## ideation
The problem asks for the sum of $f(P)$ over all permutations $P$ of $(1, \dots, N)$, where $f(P)$ is the integer formed by concatenating the elements of $P$.
The key insight is to calculate the contribution of each number $x \in \{1, \dots, N\}$ to the total sum.
For a fixed $x$, it appears in each position $k$ (1-indexed) of the permutation in exactly $(N-1)!$ permutations.
When $x$ is at position $k$, its value is multiplied by $10^{S_k}$, where $S_k$ is the total number of digits in the elements at positions $k+1, \dots, N$.
The set of elements at positions $k+1, \dots, N$ is a random subset of size $N-k$ from $\{1, \dots, N\} \setminus \{x\}$.
Let $L_y$ be the number of digits in $y$. The term contributed by $x$ at position $k$ is $x \cdot (N-1)! \cdot \mathbb{E}[10^{\sum_{y \in S} L_y}]$, where the expectation is over all subsets $S$ of size $N-k$ from $\{1, \dots, N\} \setminus \{x\}$.
The sum of $10^{\sum_{y \in S} L_y}$ over all such subsets $S$ is the coefficient of $z^{N-k}$ in the polynomial $Q_{L_x}(z) = \prod_{y \neq x} (1 + z \cdot 10^{L_y})$.
Since numbers with the same number of digits are symmetric, we can group them. Let $cnt_d$ be the count of numbers with $d$ digits.
The generating function for the full set is $P(z) = \prod_{d} (1 + z \cdot 10^d)^{cnt_d}$.
For a number $x$ with length $d$, the generating function for the set excluding $x$ is $Q_d(z) = P(z) / (1 + z \cdot 10^d)$.
We can precompute $P(z)$ using NTT (Number Theoretic Transform) since $N$ is up to $2 \times 10^5$.
Then, for each distinct length $d$, we compute $Q_d(z)$ by dividing $P(z)$ by $(1 + z \cdot 10^d)$. This division can be performed in $O(N \log N)$ or $O(N)$ time.
Finally, the total sum is $\sum_{d} (\sum_{x: L_x=d} x) \cdot (N-1)! \cdot \sum_{k=1}^N [z^{N-k}] Q_d(z)$.
The inner sum $\sum_{k=1}^N [z^{N-k}] Q_d(z)$ is simply the sum of all coefficients of $Q_d(z)$ (since the degree is at most $N-1$).
Wait, the degree of $Q_d(z)$ is $N-1$. The powers of $z$ range from $0$ to $N-1$. The term for position $k$ corresponds to $z^{N-k}$. As $k$ goes from $1$ to $N$, $N-k$ goes from $N-1$ to $0$. So we sum all coefficients of $Q_d(z)$.
The sum of coefficients of a polynomial $Q(z)$ is $Q(1)$.
So, $S_d = Q_d(1) = P(1) / (1 + 1 \cdot 10^d)$.
This simplifies the problem significantly! We don't need to compute the full polynomial coefficients if we only need the sum of coefficients.
Let's verify:
$Q_d(z) = \frac{P(z)}{1 + z \cdot 10^d}$.
Sum of coefficients of $Q_d(z)$ is $Q_d(1) = \frac{P(1)}{1 + 10^d}$.
$P(1) = \prod_{j=1}^N (1 + 10^{L_j})$.
So for each length $d$, the total multiplier for all numbers of length $d$ is $(N-1)! \cdot \frac{P(1)}{1 + 10^d}$.
The answer is $\sum_{d} (\sum_{x: L_x=d} x) \cdot (N-1)! \cdot \frac{P(1)}{1 + 10^d}$.
This is $O(N)$ to compute sums of numbers by length and $P(1)$.
Let's double check this logic.
The contribution of $x$ is $x \cdot (N-1)! \cdot \sum_{k=1}^N [z^{N-k}] Q_{L_x}(z)$.
$\sum_{k=1}^N [z^{N-k}] Q_{L_x}(z) = \sum_{j=0}^{N-1} [z^j] Q_{L_x}(z) = Q_{L_x}(1)$.
Yes, this is correct.
So the algorithm is:
1. Compute $cnt_d$ and sum of numbers $Sum_d$ for each length $d$.
2. Compute $P(1) = \prod_{j=1}^N (1 + 10^{L_j}) \pmod M$.
3. For each length $d$, compute $Term_d = Sum_d \cdot (N-1)! \cdot P(1) \cdot (1 + 10^d)^{-1} \pmod M$.
4. Sum $Term_d$ for all $d$.

Pitfalls:
- Modular inverse of $(1 + 10^d)$ must exist. Since $M = 998244353$ is prime and $1 + 10^d < M$ for $d \le 6$, it's fine.
- $N$ up to $2 \times 10^5$, so $O(N)$ is required.
- Be careful with 1-indexing and 0-indexing if using arrays, but here we just iterate.

## worker: (None)
The problem asks for the sum of $f(P)$ over all permutations $P$ of $(1, \dots, N)$, where $f(P)$ is the integer formed by concatenating the elements.
We derived that the total sum can be computed by considering the contribution of each number $x$.
For a fixed $x$, it appears in each position $k$ in $(N-1)!$ permutations. When at position $k$, it is multiplied by $10^{S_k}$ where $S_k$ is the total number of digits in the suffix.
The sum of $10^{S_k}$ over all permutations where $x$ is at position $k$ is related to the coefficient of $z^{N-k}$ in the generating function $Q_{L_x}(z) = \prod_{y \neq x} (1 + z \cdot 10^{L_y})$.
The total contribution of $x$ is $x \cdot (N-1)! \cdot \sum_{k=1}^N [z^{N-k}] Q_{L_x}(z)$.
The sum of coefficients of $Q_{L_x}(z)$ is $Q_{L_x}(1) = \frac{P(1)}{1 + 10^{L_x}}$, where $P(1) = \prod_{y=1}^N (1 + 10^{L_y})$.
Thus, the total answer is $\sum_{d} (\sum_{x: L_x=d} x) \cdot (N-1)! \cdot \frac{P(1)}{1 + 10^d}$.
This approach is $O(N)$ time and space, which fits within the constraints.
