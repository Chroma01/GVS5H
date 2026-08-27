
## ideation
The problem asks us to count the number of arithmetic progressions of length 3 in a given set $S$.
This is equivalent to finding triplets $(A, B, C)$ in $S$ such that $A + C = 2B$.
We can model the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$.
The coefficient of $x^k$ in $P(x)^2$ gives the number of pairs $(A, C)$ in $S$ such that $A + C = k$.
For each $B \in S$, we look at the coefficient of $x^{2B}$ in $P(x)^2$.
Let this count be $C_{2B}$. This count includes the pair $(B, B)$ and pairs $(A, C)$ with $A \neq C$.
Since $S$ has distinct elements, the pair $(B, B)$ contributes 1.
The remaining $C_{2B} - 1$ pairs are distinct and come in symmetric pairs $(A, C)$ and $(C, A)$.
We want to count triplets with $A < B < C$, which corresponds to pairs $(A, C)$ with $A < C$.
The number of such pairs is $(C_{2B} - 1) / 2$.
We sum this quantity over all $B \in S$.
To compute the coefficients of $P(x)^2$ efficiently, we use Fast Fourier Transform (FFT).
The maximum value in $S$ is $10^6$, so the polynomial degree is up to $10^6$.
The convolution size will be up to $2 \cdot 10^6$.
We use `numpy.fft` for efficient computation.
The time complexity will be $O(M \log M)$ where $M = 2^{21} \approx 2 \cdot 10^6$.
Space complexity is $O(M)$.

## worker: Implement the solution using FFT with numpy.
The problem asks for the number of arithmetic progressions of length 3 in a set $S$. This is equivalent to counting triplets $(A, B, C)$ such that $A, B, C \in S$, $A < B < C$, and $A + C = 2B$.
We can model the set $S$ as a polynomial $P(x) = \sum_{s \in S} x^s$. The coefficient of $x^k$ in $P(x)^2$ gives the number of pairs $(A, C)$ in $S$ such that $A + C = k$.
Using Fast Fourier Transform (FFT), we can compute the coefficients of $P(x)^2$ efficiently in $O(M \log M)$ time, where $M = \max(S)$.
For each $B \in S$, we look at the coefficient of $x^{2B}$ in $P(x)^2$, denoted as $cnt$. This count includes the pair $(B, B)$ exactly once. All other pairs $(A, C)$ with $A + C = 2B$ satisfy $A \neq C$ and come in symmetric pairs $(A, C)$ and $(C, A)$. The number of pairs with $A < C$ is therefore $(cnt - 1) / 2$.
Summing this quantity over all $B \in S$ gives the total number of fine triplets.
The maximum value of $S_i$ is $10^6$, so the FFT size is chosen as the next power of 2 greater than $2 \times 10^6$, which is $2^{21}$. This fits well within memory and time limits. Floating-point precision is handled by rounding to the nearest integer, which is safe given the maximum coefficient value ($10^6$) is well within double-precision limits.
