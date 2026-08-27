
## ideation
The problem asks whether string $S$ can be transformed into string $T$ using two operations that essentially swap a block of $X$ zeros with an adjacent block of $Y$ ones.
- Operation A: `0^X 1^Y` $\to$ `1^Y 0^X` (Y ones move left by X positions).
- Operation B: `1^Y 0^X` $\to$ `0^X 1^Y` (Y ones move right by X positions).

Key observations:
1. The total number of 1s in $S$ and $T$ must be equal. If not, it's impossible.
2. Each operation changes the position of a block of $Y$ ones by exactly $X$ positions (either left or right). Consequently, the sum of the indices of all 1s changes by $\pm X \cdot Y$.
3. Therefore, the sum of the indices of the 1s modulo $X \cdot Y$ is an invariant. Let $P_S$ be the sum of 1-based indices of 1s in $S$, and $P_T$ be the sum for $T$. We must have $P_S \equiv P_T \pmod{X \cdot Y}$.
4. It turns out these two conditions are sufficient. The operations allow us to effectively "bubble" blocks of ones past blocks of zeros, and as long as the global invariant holds and the counts match, a sequence of operations exists to transform $S$ to $T$. This is a known result for this specific type of block-swap problem on a line.

Algorithm:
1. Read $N, X, Y$ and strings $S, T$.
2. Count the number of 1s in $S$ and $T$. If they differ, output "No".
3. Calculate the sum of 1-based indices of 1s in $S$ and $T$.
4. Check if $(Sum_S - Sum_T) \% (X \cdot Y) == 0$. If yes, output "Yes", else "No".

Pitfalls:
- Using 0-based vs 1-based indexing. The problem statement uses 1-based indexing for the description, but the invariant holds regardless of base as long as it's consistent. Let's use 1-based indexing for clarity: index $i$ corresponds to $S[i-1]$.
- Integer overflow for the sum of indices? $N \le 5 \times 10^5$, max sum $\approx N^2/2 \approx 1.25 \times 10^{11}$, which fits in a 64-bit integer. Python handles large integers automatically.
- $X \cdot Y$ can be large, but modulo arithmetic is standard.

## worker: Implement the solution in Python.
The problem allows swapping a block of $X$ zeros with an adjacent block of $Y$ ones. This operation moves a block of $Y$ ones by exactly $X$ positions (either left or right). Consequently, the sum of the positions (indices) of all '1's in the string changes by $\pm X \cdot Y$ with each operation. This implies that the sum of the indices of '1's modulo $X \cdot Y$ is an invariant.

Additionally, the total number of '1's must remain constant, so the count of '1's in $S$ and $T$ must be equal.

It is a known result for this class of problems (block swaps on a line) that these two conditions are necessary and sufficient:
1. The number of '1's in $S$ equals the number of '1's in $T$.
2. The sum of the 1-based indices of '1's in $S$ is congruent to the sum of the 1-based indices of '1's in $T$ modulo $X \cdot Y$.

The solution implements these checks efficiently in $O(N)$ time.
