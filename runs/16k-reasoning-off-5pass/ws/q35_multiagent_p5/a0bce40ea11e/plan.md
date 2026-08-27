1. **Key Insight**: By Fermat's Little Theorem, for any scalar $x$, $x^p \equiv x \pmod p$. However, this does not directly apply to matrices. But we can use the fact that in characteristic $p$, $(A+B)^p = A^p + B^p$ if $A$ and $B$ commute. More importantly, we need to sum $B^p$ over all completions of zeros.
2. **Linearity and Independence**: The zeros in the matrix are filled independently. Let $Z$ be the set of positions with zeros. For each position $(i,j) \in Z$, we sum over $v \in \{1, \dots, p-1\}$. For non-zero positions, the value is fixed.
3. **Matrix Power Expansion**: Computing $B^p$ directly is expensive. However, note that we are working modulo $p$. A crucial property in characteristic $p$ is that the map $X \mapsto X^p$ is related to the Frobenius endomorphism, but for matrices, it's not simply element-wise.
4. **Alternative Approach - Linearity of Expectation/Sum**: We can rewrite the sum. Let $B = A_{fixed} + A_{zero}$, where $A_{fixed}$ has zeros where $A$ has zeros and original values elsewhere, and $A_{zero}$ has the variable values at zero positions and 0 elsewhere. This decomposition doesn't make powers easy.
5. **Better Insight**: Consider the polynomial nature. The entry $(B^p)_{i,j}$ is a polynomial in the entries of $B$. Since we sum over all possible values for the zero entries, we can use the property that $\sum_{x=0}^{p-1} x^k \equiv 0 \pmod p$ if $p-1 \nmid k$, and $\equiv -1 \pmod p$ if $p-1 \mid k$ and $k>0$, and $\equiv p-1 \equiv -1$ for $k=0$? Actually, $\sum_{x=1}^{p-1} x^k \equiv -1 \pmod p$ if $p-1 \mid k$ and $k>0$, and $0$ otherwise. Wait, the sum is over $1 \dots p-1$.
   - $\sum_{x=1}^{p-1} 1 = p-1 \equiv -1 \pmod p$.
   - $\sum_{x=1}^{p-1} x^k \equiv 0 \pmod p$ if $p-1 \nmid k$.
   - $\sum_{x=1}^{p-1} x^k \equiv -1 \pmod p$ if $p-1 \mid k$ and $k > 0$.
6. **Polynomial Degree**: The entry $(B^p)_{i,j}$ is a homogeneous polynomial of degree $p$ in the entries of $B$. Each term is a product of $p$ entries. When we sum over the choices for a specific zero entry $B_{r,c}$, we look at the exponent of $B_{r,c}$ in each monomial. If the total exponent of $B_{r,c}$ across all factors in a monomial is $e$, then the sum over $B_{r,c} \in \{1,\dots,p-1\}$ is non-zero (specifically $-1$) only if $p-1 \mid e$. Since the total degree is $p$, and $p < 2(p-1)$ for $p>2$, the exponent $e$ can only be $0$ or $p-1$ (if $p=2$, $p-1=1$, so any $e \ge 1$ works? No, for $p=2$, sum over $x=1$ is just $1$. The condition $p-1 \mid e$ means $1 \mid e$, which is always true. So for $p=2$, the sum is just the value itself).
7. **Special Case p=2**: Sum over $x=1$ is trivial.
8. **General p**: For a monomial to survive the summation over a specific zero variable $B_{r,c}$, the variable must appear with exponent $p-1$ or $0$. Since the total degree is $p$, if a variable appears with exponent $p-1$, the remaining $p-(p-1)=1$ factor must come from other variables. This implies that for the sum to be non-zero, each zero variable that appears in a surviving term must appear with exponent exactly $p-1$.
9. **Structure of Surviving Terms**: A term in the expansion of $(B^p)_{i,j}$ corresponds to a path of length $p$ from $i$ to $j$ in the graph defined by non-zero entries of $B$. Specifically, $(B^p)_{i,j} = \sum_{k_1, \dots, k_{p-1}} B_{i,k_1} B_{k_1,k_2} \dots B_{k_{p-1},j}$.
   We sum this over all assignments of zeros.
   For a fixed path, let $c_{r,c}$ be the count of how many times edge $(r,c)$ appears in the path.
   The contribution of this path to the total sum is:
   $\left( \prod_{(r,c) \notin Z} B_{r,c}^{c_{r,c}} \right) \times \left( \prod_{(r,c) \in Z} \left( \sum_{v=1}^{p-1} v^{c_{r,c}} \right) \right)$.
   The inner sum is $-1$ if $p-1 \mid c_{r,c}$ and $c_{r,c} > 0$, and $0$ if $p-1 \nmid c_{r,c}$. Note if $c_{r,c}=0$, the sum is over an empty product (value 1), effectively the variable doesn't appear.
   So, a path contributes to the final sum if and only if for every zero-edge $(r,c)$ used in the path, the count $c_{r,c}$ is a multiple of $p-1$.
   Since the total length is $p$, and $p$ is prime, the only multiples of $p-1$ that can appear are $0$ and $p-1$ (since $2(p-1) > p$ for $p>2$).
   Thus, for $p>2$, a path contributes if and only if:
   - Every zero-edge used in the path appears exactly $p-1$ times.
   - The remaining $p - (p-1) = 1$ step is a non-zero edge (or a zero-edge with count 0, i.e., not used).
   - Actually, if a zero-edge is used, it must be used $p-1$ times. The remaining 1 step must be an edge that is NOT a zero-edge (because if it were a zero-edge, its count would be $p-1+1=p$, which is not divisible by $p-1$? Wait. $p \equiv 1 \pmod{p-1}$. So if a zero-edge is used $p$ times, the sum is $\sum v^p = \sum v \equiv 0 \pmod p$? No. $\sum_{v=1}^{p-1} v = \frac{(p-1)p}{2}$. If $p=2$, sum=1. If $p>2$, sum=0. Generally $\sum v^k$. If $k=p$, $v^p \equiv v$. So $\sum v \equiv 0$. So yes, count $p$ gives 0.
   - So, effectively, for $p>2$, the only non-zero contributions come from paths where exactly one edge is a "non-zero-fixed" edge (or a zero-edge that is effectively treated as non-zero? No, zeros are variables) and the other $p-1$ edges are the SAME zero-edge?
   - Let's re-evaluate. The path has $p$ edges. Let $S_Z$ be the set of zero-edges used. For each $e \in S_Z$, let $c_e$ be its count. We need $p-1 \mid c_e$. Since $\sum c_e = p$, and $c_e \ge 1$, the only solution is one edge has count $p-1$ and one edge has count $1$.
   - Case 1: The edge with count 1 is a non-zero fixed edge. The edge with count $p-1$ is a zero edge.
   - Case 2: The edge with count 1 is a zero edge? Then count is 1. $p-1 \mid 1 \implies p=2$.
   - So for $p>2$, we only have Case 1. The path consists of $p-1$ traversals of a single zero-edge $(u,v)$ and 1 traversal of a fixed non-zero edge $(x,y)$.
   - The structure of the path must be a cycle of length $p-1$ on edge $(u,v)$? No, a path of length $p$.
   - The $p-1$ edges are $(u,v)$. This implies the path goes $u \to v \to u \to v \dots$. This requires $u=v$? No. $B_{u,v}$ is used. The path is a sequence of vertices $v_0, v_1, \dots, v_p$.
   - If $p-1$ edges are $(u,v)$, then the path looks like: start at some node, take some steps, then traverse $(u,v)$ repeatedly?
   - Actually, the edges are ordered. The term is $B_{v_0,v_1} B_{v_1,v_2} \dots B_{v_{p-1},v_p}$.
   - If $p-1$ of these are $(u,v)$, then the path must visit $u$ and $v$ appropriately.
   - Specifically, the single non-zero edge $(x,y)$ must connect the "components" of the zero-edge traversals.
   - Since the zero edges are all $(u,v)$, the path essentially bounces between $u$ and $v$ for $p-1$ steps, and takes one step $(x,y)$.
   - For the path to be valid, the sequence of vertices must be consistent.
   - This implies that the non-zero edge $(x,y)$ must be either $(u,v)$ or $(v,u)$ or connect to $u/v$?
   - Actually, if the path uses $(u,v)$ $p-1$ times, the vertices involved are only $u$ and $v$. So the non-zero edge must also be between $u$ and $v$.
   - So, for each pair of indices $(u,v)$ such that $A_{u,v}=0$, we consider paths that use $(u,v)$ exactly $p-1$ times and one other edge $(x,y)$ which is non-zero.
   - The non-zero edge must be $(u,v)$? No, $A_{u,v}$ is zero. So the non-zero edge must be $(v,u)$? Or $(u,u)$?
   - The path is a sequence. The single non-zero edge $(x,y)$ must fit into the sequence.
   - If the non-zero edge is $(u,v)$, it's a zero edge, contradiction.
   - So the non-zero edge must be $(v,u)$ or $(u,u)$ or $(v,v)$?
   - Let's check the vertex sequence.
   - If we have $p-1$ edges of $(u,v)$, the path alternates $u \to v \to u \to v \dots$.
   - If we insert one edge $(x,y)$, it must replace one $(u,v)$ or be adjacent?
   - Actually, the path is fixed length $p$.
   - If the non-zero edge is $(v,u)$, we can have a path like $u \xrightarrow{(v,u)?} $ No.
   - Let's just iterate over all possible "special" zero-edges $(u,v)$ and all possible "single" non-zero edges $(x,y)$.
   - For a fixed pair of edges $E_1=(u,v)$ (zero) and $E_2=(x,y)$ (non-zero), how many paths of length $p$ use $E_1$ exactly $p-1$ times and $E_2$ exactly 1 time?
   - The path is a sequence of $p$ edges. The position of $E_2$ can be any of the $p$ positions.
   - However, the vertices must match.
   - If $E_2$ is at position $k$ (1-indexed), then:
     - Edges $1 \dots k-1$ are $E_1$.
     - Edge $k$ is $E_2$.
     - Edges $k+1 \dots p$ are $E_1$.
   - This requires:
     - Start at $v_0$. $v_1 = v_0 + (u,v)$.
     - ...
     - $v_{k-1}$ must be $u$ (start of $E_2$).
     - $v_k = y$ (end of $E_2$).
     - $v_{k+1} = v_k + (u,v) = y + (u,v)$. This requires $y=u$ for $E_1$ to start? No, $E_1$ is $(u,v)$. So we need start of $E_1$ to be $y$. So $y=u$.
     - Then $v_{k+1} = v$.
     - Then $v_{k+2} = u$, etc.
     - Finally, $v_p$ must be the end of the last $E_1$.
   - So, we need $y=u$. The non-zero edge is $(x,u)$.
   - Also, the prefix of $k-1$ edges of $(u,v)$ must end at $u$.
     - $v_0 \xrightarrow{(u,v)} v_1 \dots \xrightarrow{(u,v)} v_{k-1}=u$.
     - If $k-1$ is even, $v_0=u \implies v_{k-1}=u$. If $k-1$ is odd, $v_0=v \implies v_{k-1}=u$.
     - So $v_0$ is determined by parity of $k-1$.
   - Similarly, the suffix of $p-k$ edges of $(u,v)$ starts at $u$ (since $v_k=u$) and ends at $v_p$.
     - $v_k=u \xrightarrow{(u,v)} v_{k+1}=v \dots \xrightarrow{(u,v)} v_p$.
     - $v_p$ is determined by parity of $p-k$.
   - We sum over all $k=1 \dots p$.
   - The value contributed is $A_{x,u} \times (-1)^{1}$ (from the sum over the zero edge) $= -A_{x,u}$.
   - Wait, the sum over the zero edge variable is $-1$. The fixed edge is $A_{x,u}$.
   - So contribution is $-A_{x,u}$.
   - We sum this over all valid $k$ and all pairs $(u,v)$ (zero) and $(x,u)$ (non-zero).
   - Note: $x$ can be anything such that $A_{x,u} \neq 0$.
   - Also, we must ensure the path is valid (vertices match).
   - This logic holds for $p>2$. For $p=2$, we handle separately.