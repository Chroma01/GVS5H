
## ideation
The core difficulty lies in efficiently computing the sum of $B^p$ over all possible matrices $B$ obtained by replacing zeros in $A$ with values from $1$ to $p-1$, modulo $p$. A naive approach of iterating over all $(p-1)^K$ matrices is infeasible due to the large number of possibilities.

Key insights:
1. **Matrix Expansion**: The $(i,j)$-th entry of $B^p$ is the sum over all paths of length $p$ from $i$ to $j$ of the product of the entries along the path.
2. **Summation over $B$**: The total sum $S_{i,j}$ is the sum over all paths of the sum over all $B$ of the product of entries along the path. This factors into a product of sums for each entry in the path.
3. **Sum of Powers**: For a zero entry $(r,c)$ that appears $k$ times in a path, the sum over $x \in \{1, \dots, p-1\}$ of $x^k$ is $-1 \pmod{p}$ if $p-1 \mid k$ and $k>0$, and $0$ otherwise. For a non-zero entry, the value is fixed. If a zero entry does not appear in the path, the sum over its possible values is $\sum_{x=1}^{p-1} 1 = p-1 \equiv -1 \pmod{p}$.
4. **Valid Paths**: A path contributes non-trivially only if for every zero entry $(r,c)$ in the path, the count $k_{r,c}$ is either $0$ or a multiple of $p-1$. The contribution is $(-1)^{|Z|} \times \prod_{(r,c) \notin Z} A_{r,c}^{k_{r,c}}$, where $|Z|$ is the number of zero positions in $A$.
5. **Special Cases**:
   - For $p=2$, $p-1=1$, so all paths are valid. The sum is $(-1)^{|Z|}$ times the sum over all paths of the product of entries. However, since $B$ is uniquely determined (zeros become 1), we can directly compute $B^2$.
   - For $p>2$, the only paths that can have a zero entry with count multiple of $p-1$ are those where the zero entry is a self-loop and appears $p-1$ times, with one other edge appearing once (to make the total length $p$). This leads to additional contributions from self-loop zeros.

The solution handles $p=2$ separately by directly computing $B^2$ where $B$ has zeros replaced by 1. For $p>2$, it computes $M^p$ where $M$ is $A$ with zeros replaced by 0, and adds corrections for self-loop zeros.

## worker: Implement the solution as described, handling $p=2
The solution handles two cases separately:
1. For $p=2$: Since each zero can only be replaced by 1, there's only one possible matrix $B$. We compute $B^2 \pmod{2}$ directly.
2. For $p>2$: We use the path sum approach where:
   - The main contribution comes from paths using only non-zero entries, computed as $M^p \pmod{p}$ where $M$ is $A$ with zeros replaced by 0.
   - Additional contributions come from self-loop zeros, where a path can have $p-1$ copies of the self-loop edge and 1 copy of an adjacent non-zero edge.
   - The sign factor $(-1)^{|Z|}$ accounts for the sum over all zero positions (whether used or not).

The matrix multiplication is optimized to skip zero entries for efficiency.
