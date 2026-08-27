
## ideation
The core difficulty is efficiently counting triplets $(A, B, C)$ from a set $S$ such that $A, B, C \in S$, $A < B < C$, and $B - A = C - B$ (which implies $A + C = 2B$).

A naive $O(N^2)$ approach checking all pairs for each $B$ is too slow given $N \le 10^6$.
However, the values $S_i$ are bounded by $M = 10^6$. This allows us to use a frequency array (or boolean array) of size $M+1$.

The condition $A + C = 2B$ suggests using polynomial multiplication (convolution).
Let $P(x)$ be a polynomial where the coefficient of $x^k$ is 1 if $k \in S$, and 0 otherwise.
The product $Q(x) = P(x) \cdot P(x)$ will have coefficients $Q[k]$ representing the number of pairs $(A, C)$ such that $A + C = k$.
Specifically, $Q[2B]$ counts the number of pairs $(A, C)$ with $A, C \in S$ such that $A + C = 2B$.
Since $S$ contains distinct integers, $A$ and $C$ are distinct unless $A=C=B$.
The pair $(B, B)$ contributes 1 to $Q[2B]$ because $B+B=2B$.
Other pairs $(A, C)$ with $A \neq C$ appear twice in the convolution (once as $(A, C)$ and once as $(C, A)$).
We want to count triplets with $A < B < C$.
For a fixed $B$, any pair $(A, C)$ with $A+C=2B$ and $A \neq C$ satisfies either $A < B < C$ or $C < B < A$.
Since we require $A < B < C$, exactly half of the non-diagonal pairs satisfy this condition.
The diagonal pair $(B, B)$ corresponds to $A=B=C$, which is invalid since we need distinct elements and strict inequality.
Thus, for each $B \in S$, the number of valid pairs $(A, C)$ with $A < B < C$ is $(Q[2B] - 1) / 2$.
The total answer is $\sum_{B \in S} \frac{Q[2B] - 1}{2}$.

We need to compute the convolution of the binary array representing $S$ with itself.
The maximum value in $S$ is $10^6$, so the maximum sum $A+C$ is $2 \cdot 10^6$.
The polynomial degree is up to $2 \cdot 10^6$.
We can use FFT (Fast Fourier Transform) to compute this convolution in $O(M \log M)$ time, where $M = 10^6$.
The size of the FFT needs to be at least $2 \cdot 10^6 + 1$. The next power of 2 is $2^{21} = 2,097,152$.

Pitfalls:
1. Precision issues with standard `float` FFT. Using `numpy`'s FFT is generally safe for integer coefficients up to this magnitude, but we must round the results to nearest integers.
2. Memory usage: Arrays of size $2^{21}$ are manageable in Python with numpy.
3. The input $N$ is up to $10^6$, so reading input efficiently is important.

## worker: none
The problem asks us to count triplets $(A, B, C)$ from a set $S$ such that $A < B < C$ and $B - A = C - B$, which is equivalent to $A + C = 2B$.

1. **Polynomial Representation**: We represent the set $S$ as a binary polynomial $P(x)$ where the coefficient of $x^k$ is 1 if $k \in S$ and 0 otherwise.
2. **Convolution via FFT**: The product $Q(x) = P(x) \cdot P(x)$ has coefficients $Q[k]$ that count the number of pairs $(A, C)$ such that $A + C = k$. We use FFT to compute this convolution efficiently in $O(M \log M)$ time, where $M = \max(S) \le 10^6$.
3. **Counting Valid Triplets**: For each $B \in S$, we look at $Q[2B]$. This value counts all pairs $(A, C)$ with $A, C \in S$ and $A + C = 2B$.
   - The pair $(B, B)$ is always counted once (since $B \in S$).
   - Any other pair $(A, C)$ with $A \neq C$ is counted twice (once as $(A, C)$ and once as $(C, A)$).
   - We want pairs with $A < B < C$. Since $A + C = 2B$, if $A \neq C$, then either $A < B < C$ or $C < B < A$. Exactly half of the non-diagonal pairs satisfy $A < B < C$.
   - Therefore, for each $B$, the number of valid triplets is $(Q[2B] - 1) / 2$.
4. **Complexity**: The FFT size is $O(M)$, and each FFT operation is $O(M \log M)$. With $M = 10^6$, this is feasible. The final summation is $O(N)$.
