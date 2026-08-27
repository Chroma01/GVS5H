
## ideation
**Core Difficulty:**
The problem statement asks for the sum of $B^p$ modulo $p$. The initial plan relies on Fermat's Little Theorem ($x^p \equiv x \pmod p$), which simplifies the matrix power to just the matrix itself. However, matrix exponentiation does not distribute over addition in the sense that $(A+B)^p \not\equiv A^p + B^p \pmod p$ for matrices, even if it holds for scalars. The operation is $M \mapsto M^p$, then sum over all $M$, then take modulo $p$.
The constraint $N \le 100$ and $p \le 10^9$ suggests an $O(N^3 \log p)$ or $O(N^4)$ solution per element, but we need the sum over $(p-1)^K$ matrices. Since $K$ can be large, we cannot iterate. We must use linearity of expectation or combinatorial counting.
Wait, let's re-evaluate Fermat's Little Theorem for matrices.
For a scalar $x$, $x^p \equiv x \pmod p$.
For a matrix $B$, $B^p$ is the matrix where the $(i,j)$ entry is $\sum_{k_1, \dots, k_{p-1}} B_{i, k_1} B_{k_1, k_2} \dots B_{k_{p-1}, j}$.
We need $\sum_{B} (B^p)_{i,j} \pmod p$.
By the linearity of summation, $(\sum_B B^p)_{i,j} = \sum_B \sum_{\text{paths}} \prod B_{\text{edges}}$.
We can swap the sums: $\sum_{\text{paths}} \sum_B \prod B_{\text{edges}}$.
A "path" of length $p$ involves $p$ entries of $B$. Let the sequence of indices be $i \to u_1 \to u_2 \to \dots \to u_{p-1} \to j$.
The term is $\prod_{m=0}^{p-1} B_{u_m, u_{m+1}}$ (with $u_0=i, u_p=j$).
We need to sum this product over all valid assignments of non-zero values to the zero positions in $A$.
Let $S$ be the set of indices $(r, c)$ where $A_{r,c} = 0$.
For a fixed path, let $C$ be the set of edges in the path that correspond to positions in $S$.
If an edge $(u, v)$ is NOT in $S$, then $B_{u,v}$ is fixed to $A_{u,v}$.
If an edge $(u, v)$ IS in $S$, then $B_{u,v}$ can be any value in $\{1, \dots, p-1\}$.
The sum over all $B$ of the product is:
$(\prod_{(u,v) \notin S, (u,v) \in \text{path}} A_{u,v}) \times (\sum_{x \in \{1..p-1\}} x)^{|C|} \times (p-1)^{|S| - |C|}$.
Note: The total number of variables in $B$ is $K = |S|$. The path uses $p$ variables. Some might be the same variable (if the path visits the same cell multiple times).
This is the tricky part: **The path might visit the same cell multiple times.**
If a cell $(r,c) \in S$ is visited $k$ times in the path, the term in the product is $(B_{r,c})^k$.
We need to sum $(B_{r,c})^k$ over $B_{r,c} \in \{1, \dots, p-1\}$.
Let $P_k = \sum_{x=1}^{p-1} x^k$.
Properties of $P_k \pmod p$:
- If $p-1 \nmid k$, then $\sum_{x=1}^{p-1} x^k \equiv 0 \pmod p$ (since $x \mapsto x^k$ is a permutation of non-zero residues if $\gcd(k, p-1)=1$, but actually for any $k$ not divisible by $p-1$, the sum is 0 mod p).
- If $p-1 \mid k$, then $x^k \equiv 1 \pmod p$ for all $x \in \{1, \dots, p-1\}$. So sum is $p-1 \equiv -1 \pmod p$.
So, for any cell $(r,c) \in S$, if it appears $k$ times in the path:
- Contribution is $0$ if $k \not\equiv 0 \pmod{p-1}$.
- Contribution is $-1$ if $k \equiv 0 \pmod{p-1}$.
For cells $(r,c) \notin S$, the value is fixed $A_{r,c}$.
For cells in $S$ that are NOT visited in the path, their contribution is just the count of such cells times $(p-1)^{|S|-|C|}$? No.
Let's refine the counting.
Total sum = $\sum_{\text{paths } \gamma} \left( \prod_{(u,v) \in \gamma, (u,v) \notin S} A_{u,v} \right) \times \left( \sum_{B \text{ on } S} \prod_{(u,v) \in \gamma, (u,v) \in S} B_{u,v} \right) \times (p-1)^{|S| - |\text{unique cells in } \gamma \cap S|}$.
Wait, the term $(p-1)^{|S| - |\text{unique cells in } \gamma \cap S|}$ comes from the variables in $S$ that are NOT part of the path.
For the variables in the path that are in $S$, we need to sum their powers.
Let $U_\gamma = \{ (u,v) \in \gamma \cap S \}$ be the set of unique cells in $S$ visited by the path.
Let $c_{(r,c)}$ be the count of times cell $(r,c) \in S$ appears in the path.
The inner sum over $B$ restricted to $S$ is:
$\left( \prod_{(r,c) \in U_\gamma} (\sum_{x=1}^{p-1} x^{c_{(r,c)}}) \right) \times (p-1)^{|S| - |U_\gamma|}$.
As established, $\sum_{x=1}^{p-1} x^k \equiv 0 \pmod p$ unless $k$ is a multiple of $p-1$, in which case it is $-1$.
So, for a path to contribute non-zero modulo $p$, every cell $(r,c) \in S$ that is visited by the path must be visited a number of times $c_{(r,c)}$ such that $c_{(r,c)} \equiv 0 \pmod{p-1}$.
If this condition holds for all visited cells in $S$, the contribution is:
$(-1)^{|U_\gamma|} \times (p-1)^{|S| - |U_\gamma|} \times \prod_{(u,v) \in \gamma, (u,v) \notin S} A_{u,v}$.
Since we are working modulo $p$, $(p-1) \equiv -1$.
So the factor is $(-1)^{|U_\gamma|} \times (-1)^{|S| - |U_\gamma|} = (-1)^{|S|}$.
This is constant for all paths!
So the total sum is:
$(-1)^{|S|} \times (p-1)^{|S|} \times \sum_{\gamma} \left( \prod_{(u,v) \in \gamma, (u,v) \notin S} A_{u,v} \right) \times \mathbb{I}(\forall (r,c) \in U_\gamma, c_{(r,c)} \equiv 0 \pmod{p-1})$.
Wait, $(p-1)^{|S|} \equiv (-1)^{|S|} \pmod p$.
So the scalar factor is $(-1)^{|S|} \times (-1)^{|S|} = 1$.
Thus, the answer is simply:
$\sum_{\gamma} \left( \prod_{(u,v) \in \gamma, (u,v) \notin S} A_{u,v} \right) \times \mathbb{I}(\text{all visited } S\text{-cells appear } \equiv 0 \pmod{p-1} \text{ times})$.
Here, the path $\gamma$ is a sequence of $p$ vertices $v_0, v_1, \dots, v_{p-1}$? No, $B^p$ means multiplying $B$ by itself $p$ times?
$B^p = B \times B \times \dots \times B$ ($p$ times).
The $(i,j)$ entry is $\sum_{k_0=i, k_p=j} B_{k_0, k_1} B_{k_1, k_2} \dots B_{k_{p-1}, k_p}$.
The path has $p$ edges (vertices $k_0, \dots, k_p$).
The length of the path is $p$.
The condition is that for every cell $(r,c) \in S$ that appears in the sequence of edges, its frequency must be a multiple of $p-1$.
Since the total number of edges is $p$, and $p$ is prime:
Possible frequencies for cells in $S$:
Sum of frequencies = $p$.
If a cell appears $k$ times, $k \equiv 0 \pmod{p-1}$.
Since $k \ge 1$ (if visited), possible values for $k$ are $p-1, 2(p-1), \dots$.
Since sum is $p$, the only possible value is $k = p-1$.
Can we have one cell with $p-1$ occurrences? Yes, then the remaining $1$ occurrence must be a cell NOT in $S$ (or a cell in $S$ with frequency 1, which is not allowed).
Can we have two cells? $k_1 + k_2 = p$. If $k_1 \equiv 0 \pmod{p-1}$, then $k_1 \ge p-1$. If $k_1 = p-1$, then $k_2 = 1$, not allowed.
So the ONLY way to satisfy the condition is:
Exactly one cell $(r,c) \in S$ appears $p-1$ times in the path, and the remaining $1$ edge is some cell $(u,v) \notin S$.
OR
No cells in $S$ are visited? Then sum of frequencies is 0? No, we must visit $p$ edges. If no cell in $S$ is visited, then all $p$ edges are not in $S$. But if an edge is not in $S$, it contributes $A_{u,v}$. If all $p$ edges are not in $S$, then no cell in $S$ is visited, so the condition "for all visited cells in S, freq is multiple of p-1" is vacuously true.
Wait, if a cell in $S$ is NOT visited, its frequency is 0, which is $0 \equiv 0 \pmod{p-1}$. So that's fine.
The condition is: For all $(r,c) \in S$ that ARE visited, freq is multiple of $p-1$.
Cases for the path of length $p$:
1. **No edges from $S$**: All $p$ edges are from non-zero entries. Condition vacuously true.
   Contribution: $\prod_{\text{all } p \text{ edges}} A_{\text{edge}}$.
2. **Exactly one edge from $S$**: Let it be $(r,c)$. Frequency is 1. $1 \not\equiv 0 \pmod{p-1}$ (since $p \ge 2$, $p-1 \ge 1$). Condition fails. Contribution 0.
3. **Edges from $S$ sum to $p$**:
   - One cell $(r,c) \in S$ appears $p-1$ times. The remaining $1$ edge is NOT in $S$.
     Condition: $p-1 \equiv 0 \pmod{p-1}$. True.
     Contribution: $(-1) \times \prod (\text{non-S edges})$. Wait, the scalar factor was 1.
     Let's re-verify the scalar.
     Term = $(\prod_{\text{fixed}} A) \times (\sum x^{p-1}) \times (p-1)^{\text{unvisited}}$.
     $\sum x^{p-1} \equiv -1$.
     Unvisited count = $|S| - 1$.
     Factor = $(-1) \times (p-1)^{|S|-1} \equiv (-1) \times (-1)^{|S|-1} = (-1)^{|S|}$.
     Wait, earlier I said the total scalar is 1. Let's re-calculate carefully.
     Total Sum = $\sum_{\gamma} (\prod_{\gamma \cap S^c} A) \times (\prod_{(r,c) \in U_\gamma} \Sigma_{x=1}^{p-1} x^{c_{(r,c)}}) \times (p-1)^{|S| - |U_\gamma|}$.
     Case 1: $U_\gamma = \emptyset$. Term = $(\prod_{\gamma} A) \times 1 \times (p-1)^{|S|}$.
     Case 2: $U_\gamma = \{(r,c)\}$, $c_{(r,c)} = p-1$. Term = $(\prod_{\gamma \setminus \{(r,c)\}} A) \times (-1) \times (p-1)^{|S|-1}$.
     Note: The path has $p$ edges. One is $(r,c)$, $p-1$ are others.
     So $\prod_{\gamma} A = A_{(r,c)} \times \prod_{\gamma \setminus \{(r,c)\}} A$. But $A_{(r,c)}$ is 0 in the original matrix?
     No, the product over $\gamma \cap S^c$ uses the fixed values. The edge $(r,c)$ is in $S$, so it's not in the product.
     So Term = $(\prod_{e \in \gamma, e \notin S} A_e) \times (-1) \times (p-1)^{|S|-1}$.
     Modulo $p$: $(p-1) \equiv -1$.
     Term $\equiv (\prod_{e \in \gamma, e \notin S} A_e) \times (-1) \times (-1)^{|S|-1} = (\prod A) \times (-1)^{|S|}$.
     
     So we have two types of valid paths:
     Type A: No edges from $S$. Contribution: $(\prod_{e \in \gamma} A_e) \times (p-1)^{|S|} \equiv (\prod A) \times (-1)^{|S|}$.
     Type B: One edge $(r,c) \in S$ with multiplicity $p-1$, one edge $e' \notin S$. Contribution: $(\prod_{e \in \gamma, e \notin S} A_e) \times (-1)^{|S|}$.
     
     Notice the factor $(-1)^{|S|}$ is common to both!
     Total Sum = $(-1)^{|S|} \left[ \sum_{\gamma \in \text{Type A}} \prod_{e \in \gamma} A_e + \sum_{\gamma \in \text{Type B}} \prod_{e \in \gamma, e \notin S} A_e \right]$.
     
     Wait, in Type B, the edge $(r,c)$ is in $S$, so it's not in the product. The product is over the single edge $e' \notin S$.
     So for Type B, we sum over all $(r,c) \in S$ and all $e' \notin S$ such that we can form a path of length $p$ with $p-1$ copies of $(r,c)$ and 1 copy of $e'$.
     
     This looks computable.
     Let $M$ be the matrix where $M_{ij} = A_{ij}$ if $A_{ij} \neq 0$, else $0$.
     Then $\sum_{\gamma \in \text{Type A}} \prod A_e = (M^p)_{ij}$.
     
     For Type B:
     Fix $(r,c) \in S$. We need a path with $p-1$ edges of $(r,c)$ and 1 edge $e'=(u,v) \notin S$.
     The sequence of vertices must be $i \to \dots \to j$.
     The edges are $p-1$ times $(r,c)$ and 1 time $(u,v)$.
     The product of weights is $A_{uv}$.
     We need to count how many such paths exist.
     The path structure:
     $i \to k_1 \to k_2 \dots \to k_p = j$.
     Edges: $(i, k_1), (k_1, k_2), \dots, (k_{p-1}, j)$.
     Exactly one edge is $(u,v) \notin S$. The rest are $(r,c)$.
     This implies the path looks like:
     $i \to r \to c \to r \to c \dots \to c \to u \to v \to \dots$?
     No, the edges must be $(r,c)$. So the vertices must alternate $r, c, r, c \dots$.
     Specifically, if we have $p-1$ edges of $(r,c)$, the vertices involved must be $r, c, r, c, \dots$.
     The sequence of vertices $v_0, v_1, \dots, v_p$ must satisfy:
     For $p-1$ indices, $(v_k, v_{k+1}) = (r,c)$.
     For 1 index, $(v_k, v_{k+1}) = (u,v)$.
     This forces the path to be very constrained.
     Possibility 1: The single edge $(u,v)$ is at the start.
       $i=u, v_1=v$. Then $v_1 \to v_2 = (r,c) \implies v=r$. $v_2 \to v_3 = (r,c) \implies v_3=c$.
       Pattern: $u \to v \to r \to c \to r \to c \dots \to c \to j$.
       Number of $(r,c)$ edges is $p-1$.
       Vertices: $v_0=u, v_1=v$. Then $v_1=r, v_2=c, v_3=r, \dots, v_p=j$.
       This requires $v=r$ and $v_{p-1}=c$ (if $p-1$ edges follow).
       Actually, the sequence of vertices is $u, v, r, c, r, c, \dots, r, c, j$?
       Let's trace:
       Edge 1: $(u,v)$.
       Edges 2 to $p$: $(r,c)$. Total $p-1$ edges.
       Vertices: $v_0=u, v_1=v$.
       $v_1 \to v_2 = (r,c) \implies v_1=r, v_2=c$.
       $v_2 \to v_3 = (r,c) \implies v_2=r, v_3=c$.
       ...
       $v_{p-1} \to v_p = (r,c) \implies v_{p-1}=r, v_p=c$.
       So we need $v_1=r$ and $v_p=c$.
       Path: $u \to r \to c \to c \dots$? No.
       $v_1$ must be $r$. So $v=r$.
       $v_p$ must be $c$. So $j=c$.
       So if the single edge is first: $i=u, j=c$. Path: $u \to r \to c \to r \to c \dots \to c$.
       Wait, $v_1=r$. Then $v_2=c$. $v_3=r$. $v_4=c$.
       $v_p = c$ if $p$ is even?
       Sequence: $v_1, v_2, \dots, v_p$.
       $v_1=r, v_2=c, v_3=r, v_4=c, \dots$.
       $v_k = r$ if $k$ odd, $c$ if $k$ even.
       We need $v_p = j$.
       If $p$ is odd, $v_p = r$. So $j=r$.
       If $p$ is even, $v_p = c$. So $j=c$.
       Also $i=u$.
       So for a fixed $(r,c) \in S$ and fixed $(u,v) \notin S$:
       If $(u,v)$ is the first edge: Valid if $i=u$ and $j = (r \text{ if } p \text{ odd else } c)$.
       Number of such paths = 1 (the sequence is fixed).
       
     Possibility 2: The single edge $(u,v)$ is somewhere in the middle.
       $i \to r \to c \to \dots \to u \to v \to \dots \to r \to c \to j$.
       Let the single edge be at position $k$ (1-indexed, $1 \le k \le p$).
       Edges $1 \dots k-1$ are $(r,c)$. Edges $k+1 \dots p$ are $(r,c)$. Edge $k$ is $(u,v)$.
       Vertices:
       $v_0=i$.
       $v_1=r, v_2=c, \dots, v_{k-1} = (r \text{ if } k-1 \text{ odd else } c)$.
       Edge $k$: $v_{k-1} \to v_k = (u,v)$. So $v_{k-1}=u, v_k=v$.
       Then edges $k+1 \dots p$ are $(r,c)$.
       $v_k=v$.
       $v_{k+1}=r, v_{k+2}=c, \dots, v_p = (r \text{ if } p-k \text{ odd else } c)$.
       Constraints:
       1. $v_{k-1} = u$.
       2. $v_k = v$.
       3. $v_p = j$.
       From the pattern of $(r,c)$ edges:
       $v_m = r$ if $m$ odd, $c$ if $m$ even (assuming start at $v_0$? No).
       Let's define parity relative to the start of the $(r,c)$ chain.
       If we have a chain of $(r,c)$ edges starting at $v_0$, then $v_1=r, v_2=c, v_3=r \dots$.
       $v_m = r$ if $m$ odd, $c$ if $m$ even.
       So $v_{k-1} = r$ if $k-1$ odd, $c$ if $k-1$ even.
       $v_k$ would be $c$ if $k-1$ odd, $r$ if $k-1$ even.
       But we insert $(u,v)$ at $k$.
       So we need $u = v_{k-1}$ and $v = v_k$.
       And then from $v_k=v$, we continue with $(r,c)$ for $p-k$ steps.
       $v_p = v$ if we apply $(r,c)$ $p-k$ times?
       Let's check:
       Start at $v_k=v$.
       Step 1: $v \to r$.
       Step 2: $r \to c$.
       ...
       $v_{k+m} = r$ if $m$ odd, $c$ if $m$ even.
       We need $v_p = j$. Here $m = p-k$.
       So $j = r$ if $p-k$ odd, $c$ if $p-k$ even.
       
       So for each $k \in \{1, \dots, p\}$:
       We need $u$ to match the required value at step $k-1$ in the chain starting at $i$.
       And $v$ to match the required value at step $k$ in the chain starting at $i$.
       Wait, $i$ is fixed for the entry $(i,j)$.
       So for a fixed $(i,j)$ and fixed $(r,c) \in S$:
       We iterate $k$ from $1$ to $p$.
       Calculate required $u_k$ and $v_k$ based on $i, r, c, k$.
       Check if there exists $(u,v) \notin S$ such that $u=u_k, v=v_k$.
       If so, add $A_{uv}$ to the sum.
       Also need to check if the final $j$ matches the requirement from the tail.
       Wait, the tail requirement depends on $j$.
       Actually, it's easier:
       For fixed $(i,j)$:
       Sum = $(-1)^{|S|} [ (M^p)_{ij} + \sum_{(r,c) \in S} \sum_{k=1}^p \sum_{(u,v) \notin S, u=u_k, v=v_k} A_{uv} ]$.
       Where $u_k, v_k$ are determined by the path structure.
       Specifically:
       Path starts $i \to \dots \to u \to v \to \dots \to j$.
       First $k-1$ edges are $(r,c)$. So $v_{k-1}$ is determined by $i, r, c$.
       Next edge is $(u,v)$. So $u = v_{k-1}, v = v_k$.
       Last $p-k$ edges are $(r,c)$. So $j$ must be consistent with $v$ and $p-k$.
       If consistent, add $A_{uv}$.
       
       Complexity:
       $N \le 100$. $p$ is large, but we only care about parity of $k$ and $p-k$.
       For a fixed $(i,j)$ and $(r,c)$:
       We need to check $k=1 \dots p$.
       However, notice that $u_k, v_k$ pattern repeats or is simple.
       $v_m = r$ if $m$ odd, $c$ if $m$ even (relative to start).
       $u_k = v_{k-1}$. $v_k = v_{k-1} \to \dots$? No, $v_k$ is the target of $(r,c)$ from $v_{k-1}$.
       So $v_k = c$ if $k-1$ odd ($k$ even), $r$ if $k-1$ even ($k$ odd).
       So $u_k, v_k$ depends only on parity of $k$.
       Also the consistency check for $j$ depends on parity of $p-k$.
       So we only have 2 cases for $k$: odd and even.
       Case $k$ odd: $u_k = c, v_k = r$. Tail length $p-k$ (even). $j$ must be $c$.
       Case $k$ even: $u_k = r, v_k = c$. Tail length $p-k$ (odd). $j$ must be $r$.
       So for each $(r,c) \in S$:
         If $j == c$: Sum over $k$ odd ($1, 3, \dots$) of $A_{c,r}$? No, $u=c, v=r$. Sum $A_{c,r}$.
           Wait, $u_k=c, v_k=r$. So we need $(c,r) \notin S$. If so, add $A_{c,r}$.
           Number of such $k$: $\lceil p/2 \rceil$ or similar. But the term $A_{uv}$ is constant for all such $k$?
           Yes, $u=c, v=r$ is fixed for all odd $k$.
           So if $(c,r) \notin S$, we add $A_{c,r} \times (\text{count of odd } k)$.
         If $j == r$: Sum over $k$ even ($2, 4, \dots$) of $A_{r,c}$.
           If $(r,c) \notin S$, add $A_{r,c} \times (\text{count of even } k)$.
           
       Wait, is it possible that $(u,v) \in S$?
       The condition is $(u,v) \notin S$.
       If $(c,r) \in S$, then this term is 0.
       So algorithm:
       1. Count $|S|$. Compute $(-1)^{|S|}$.
       2. Compute $T_1 = (M^p)_{ij}$ where $M_{uv} = A_{uv}$ if $A_{uv} \neq 0$ else $0$.
       3. Compute $T_2 = \sum_{(r,c) \in S} \text{contribution}$.
          For each $(r,c) \in S$:
            Check if $j == c$. If so, let $u=c, v=r$. If $(u,v) \notin S$, add $A_{uv} \times \lceil p/2 \rceil$.
            Check if $j == r$. If so, let $u=r, v=c$. If $(u,v) \notin S$, add $A_{uv} \times \lfloor p/2 \rfloor$.
       4. Result = $(-1)^{|S|} (T_1 + T_2) \pmod p$.
       
       Wait, $p$ can be large, so we can't iterate $k$. But we derived the counts based on parity.
       Count of odd $k \in \{1, \dots, p\}$: $(p+1)//2$.
       Count of even $k \in \{1, \dots, p\}$: $p//2$.
       
       Is this correct?
       Let's double check the path logic.
       Path: $i \xrightarrow{(r,c)} \dots \xrightarrow{(r,c)} u \xrightarrow{(u,v)} v \xrightarrow{(r,c)} \dots \xrightarrow{(r,c)} j$.
       Number of $(r,c)$ edges is $p-1$.
       The sequence of vertices $v_0, \dots, v_p$.
       $v_0=i$.
       $v_1=r, v_2=c, \dots$.
       $v_{k-1}=u, v_k=v$.
       $v_p=j$.
       The values $u, v$ are determined by $k$ and $i$.
       $v_m = r$ if $m$ odd, $c$ if $m$ even.
       $u = v_{k-1}$. $v = v_k$.
       If $k$ is odd: $k-1$ even $\implies u=c$. $k$ odd $\implies v=r$.
         So edge is $(c,r)$.
         Tail: $p-k$ steps. $p$ odd, $k$ odd $\implies p-k$ even.
         $v_p = v$ if even steps?
         Start $v_k=v=r$.
         Step 1: $r \to c$.
         Step 2: $c \to r$.
         ...
         Even steps $\implies$ end at $r$.
         So $j=r$.
         Wait, my previous deduction was $j=c$. Let's re-verify.
         Start $v_k=r$.
         Apply $(r,c)$ once: $r \to c$. ($m=1$)
         Apply twice: $r \to c \to r$. ($m=2$)
         Apply $m$ times: $r$ if $m$ even, $c$ if $m$ odd.
         We need $m = p-k$ even. So $j=r$.
         Okay, correction:
         If $k$ odd: $u=c, v=r$. Requires $j=r$.
         If $k$ even: $k-1$ odd $\implies u=r$. $k$ even $\implies v=c$.
           Tail $p-k$ odd. Start $v_k=c$.
           Apply $(r,c)$ odd times: $c \to r$.
           So $j=r$? No.
           Start $c$.
           1 step: $c \to r$.
           Odd steps $\implies r$.
           So $j=r$.
           Wait, both cases give $j=r$?
           Let's re-re-check.
           Case $k$ odd: $u=c, v=r$. Tail $p-k$ even. Start $r$. Even steps $\implies r$. So $j=r$.
           Case $k$ even: $u=r, v=c$. Tail $p-k$ odd. Start $c$. Odd steps $\implies r$. So $j=r$.
           In both cases, $j$ must be $r$.
           And the edge $(u,v)$ is either $(c,r)$ or $(r,c)$.
           If $k$ odd: $(c,r)$. Count $\lceil p/2 \rceil$.
           If $k$ even: $(r,c)$. Count $\lfloor p/2 \rfloor$.
           
           So for a fixed $(r,c) \in S$:
           If $j == r$:
             Check $(c,r)$. If not in $S$, add $A_{c,r} \times \lceil p/2 \rceil$.
             Check $(r,c)$. If not in $S$, add $A_{r,c} \times \lfloor p/2 \rfloor$.
             Note: $(c,r)$ and $(r,c)$ might be the same if $r=c$, but $r,c$ are indices.
             Also need to ensure $(c,r) \notin S$ and $(r,c) \notin S$.
           
           What if $j \neq r$? Then no such path exists for this $(r,c)$.
           
       So the algorithm simplifies to:
       For each $(i,j)$:
         Base = $(M^p)_{ij}$.
         Add = 0.
         For each $(r,c) \in S$:
           If $j == r$:
             if $(c,r) \notin S$: Add += $A_{c,r} \times \lceil p/2 \rceil$.
             if $(r,c) \notin S$: Add += $A_{r,c} \times \lfloor p/2 \rfloor$.
         Total = $(-1)^{|S|} (Base + Add) \pmod p$.
         
       Wait, what if $p=2$?
       $p=2$. $p-1=1$.
       $k$ odd: $k=1$. Count 1. $\lceil 2/2 \rceil = 1$.
       $k$ even: $k=2$. Count 1. $\lfloor 2/2 \rfloor = 1$.
       Path length 2.
       Type A: $i \to u \to j$ with no $S$.
       Type B: One $(r,c) \in S$ with freq 1. One $(u,v) \notin S$ with freq 1.
       Path $i \to u \to j$. Edges $(i,u), (u,j)$.
       One is $(r,c)$, one is $(u,v)$.
       If $(i,u) = (r,c)$, then $(u,j) = (u,v)$. So $u=u, v=j$.
       Requires $u=r, j=c$.
       If $(u,j) = (r,c)$, then $(i,u) = (u,v)$. So $u=u, v=j$.
       Requires $u=r, j=c$? No.
       Let's trace:
       Case 1: First edge $(r,c)$. $i=r, u=c$. Second edge $(u,v)=(c,j)$.
         So $i=r, j=v$. Edge $(c,j) \notin S$.
         Condition $j=r$? No, $j=v$.
         My previous derivation said $j=r$. Why?
         Re-eval $p=2, k=1$.
         $k=1$ (odd). $u=c, v=r$.
         Tail $p-k=1$ (odd). Start $v=r$.
         Apply $(r,c)$ once: $r \to c$. So $j=c$.
         Ah, $j=c$.
         My previous deduction: "Start $r$. Even steps $\implies r$".
         For $p=2, k=1$, tail length $1$ (odd).
         Start $r$. Odd steps $\implies c$.
         So $j=c$.
         Correct.
         So for $k$ odd: $u=c, v=r$, requires $j=c$.
         For $k$ even: $k=2$. $u=r, v=c$. Tail $0$. Start $c$. $j=c$.
         So for $p=2$:
         If $k=1$: $u=c, v=r$. Requires $j=c$. Edge $(c,r)$.
         If $k=2$: $u=r, v=c$. Requires $j=c$. Edge $(r,c)$.
         So if $j=c$:
           Add $A_{c,r} \times 1$ (if $(c,r) \notin S$).
           Add $A_{r,c} \times 1$ (if $(r,c) \notin S$).
         If $j \neq c$: 0.
         
         Generalizing:
         $k$ odd: $u=c, v=r$. Tail $p-k$ even?
         $p$ is prime. If $p=2$, $p-k = 1$ (odd).
         If $p > 2$, $p$ is odd.
         If $k$ odd, $p-k$ even.
         If $p=2$, $p-k$ odd.
         
         So the parity of tail depends on $p$.
         If $p=2$:
           $k$ odd (1): Tail odd. Start $r \to c$. $j=c$.
           $k$ even (2): Tail even (0). Start $c \to c$. $j=c$.
           Both require $j=c$.
         If $p$ odd:
           $k$ odd: Tail even. Start $r \to r$. $j=r$.
           $k$ even: Tail odd. Start $c \to r$. $j=r$.
           Both require $j=r$.
           
         So:
         If $p=2$: Check $j=c$.
         If $p$ odd: Check $j=r$.
         
         And the edges:
         $k$ odd: $(c,r)$. Count $\lceil p/2 \rceil$.
         $k$ even: $(r,c)$. Count $\lfloor p/2 \rfloor$.
         
         So the condition on $j$ is:
         If $p=2$: $j=c$.
         If $p>2$: $j=r$.
         
         Wait, $p$ is prime. $p=2$ is the only even prime.
         So:
         If $p=2$: Target $j=c$.
         If $p>2$: Target $j=r$.
         
         Let's verify Sample 1.
         N=2, p=3.
         A = [[0,1],[0,2]]. S={(0,0), (1,0)}. (0-indexed).
         $p=3$ (odd). Target $j=r$.
         For (0,0): $r=0, c=0$. Target $j=0$.
           $k$ odd: $(0,0) \in S$? Yes. Skip.
           $k$ even: $(0,0) \in S$? Yes. Skip.
         For (1,0): $r=1, c=0$. Target $j=1$.
           $k$ odd: $(0,1)$. Is $(0,1) \in S$? No (A[0,1]=1). Add $A_{0,1} \times \lceil 3/2 \rceil = 1 \times 2 = 2$.
           $k$ even: $(1,0) \in S$? Yes. Skip.
         Total Add for (0,0): 0. Base $(M^3)_{0,0}$.
         $M = [[0,1],[0,2]]$.
         $M^2 = [[0,2],[0,4]]$. $M^3 = [[0,4],[0,8]] \equiv [[0,1],[0,2]] \pmod 3$.
         So Base(0,0)=0. Total=0. Correct (Sample output 0).
         
         For (0,1): $j=1$.
         (0,0): $r=0, c=0$. Target $j=0 \neq 1$. 0.
         (1,0): $r=1, c=0$. Target $j=1$. Match.
           $k$ odd: $(0,1)$. Not in S. Add $1 \times 2 = 2$.
           $k$ even: $(1,0) \in S$. Skip.
         Add = 2. Base $(M^3)_{0,1} = 1$.
         Total = $(-1)^2 (1+2) = 3 \equiv 0$.
         Sample output 2. Mismatch.
         Wait, Sample output for (0,1) is 2.
         My calc: 0.
         Where is the error?
         Maybe $j=r$ is wrong for $p=3$?
         Re-eval $p=3, k=1$.
         $k=1$ (odd). $u=c, v=r$.
         Tail $p-k=2$ (even). Start $v=r$.
         Apply $(r,c)$ twice: $r \to c \to r$.
         So $j=r$. Correct.
         Re-eval $p=3, k=2$.
         $k=2$ (even). $u=r, v=c$.
         Tail $p-k=1$ (odd). Start $v=c$.
         Apply $(r,c)$ once: $c \to r$.
         So $j=r$. Correct.
         
         Why did Sample 1 give 2?
         Maybe my Base calculation is wrong?
         $M = [[0,1],[0,2]]$.
         $M^2 = [[0, 2], [0, 4]]$.
         $M^3 = [[0, 4], [0, 8]] \equiv [[0, 1], [0, 2]]$.
         Base(0,1) = 1.
         Add = 2.
         Total = 3 = 0.
         Sample says 2.
         Maybe the scalar $(-1)^{|S|}$ is wrong?
         $|S|=2$. $(-1)^2 = 1$.
         Maybe the condition for Type B is different?
         "One cell $(r,c) \in S$ appears $p-1$ times".
         For $p=3$, $p-1=2$.
         Path length 3.
         Edges: $(r,c), (r,c), (u,v)$.
         Permutations of these edges?
         The path is a sequence.
         My counting assumed specific positions for $(u,v)$.
         But the edges are indistinguishable except for position?
         No, the path is a sequence of vertices.
         If the edges are $e_1, e_2, e_3$.
         Two are $(r,c)$, one is $(u,v)$.
         There are 3 positions for $(u,v)$.
         My analysis covered $k=1,2,3$.
         $k=1$: $(u,v)$ first.
         $k=2$: $(u,v)$ middle.
         $k=3$: $(u,v)$ last.
         Counts:
         $k=1$: 1 path.
         $k=2$: 1 path.
         $k=3$: 1 path.
         Total 3 paths?
         But my formula used $\lceil p/2 \rceil$ and $\lfloor p/2 \rfloor$.
         For $p=3$: $\lceil 1.5 \rceil = 2$, $\lfloor 1.5 \rfloor = 1$.
         Sum = 3. Correct.
         
         Why the result mismatch?
         Maybe $A_{c,r}$ vs $A_{r,c}$?
         For (1,0): $r=1, c=0$.
         $k$ odd (1,3): $(c,r) = (0,1)$. $A_{0,1}=1$.
         $k$ even (2): $(r,c) = (1,0)$. $A_{1,0}=0$ (since in S).
         So Add = $1 \times 2 = 2$.
         Base = 1.
         Total = 3 = 0.
         Sample output 2.
         
         Is it possible that $B^p$ sum is not $(-1)^{|S|} (M^p + \dots)$?
         Let's re-calculate the scalar.
         Type A: $(p-1)^{|S|} \equiv (-1)^{|S|}$.
         Type B: $(-1) \times (p-1)^{|S|-1} \equiv (-1) \times (-1)^{|S|-1} = (-1)^{|S|}$.
         Scalar is correct.
         
         Maybe $M^p$ calculation?
         $M = [[0,1],[0,2]]$.
         $M^2 = [[0, 2], [0, 4]]$.
         $M^3 = [[0, 8], [0, 16]] \equiv [[0, 2], [0, 1]]$?
         $8 \equiv 2 \pmod 3$. $16 \equiv 1 \pmod 3$.
         So $M^3 = [[0, 2], [0, 1]]$.
         Ah! $M^3_{0,1} = 2$.
         My manual calc: $M^2_{0,1} = 2$. $M^3_{0,1} = M_{0,0}*2 + M_{0,1}*1 = 0 + 1*1 = 1$?
         Wait, $M^2 = M \times M$.
         $M = [[0,1],[0,2]]$.
         $M^2_{0,1} = M_{0,0}M_{0,1} + M_{0,1}M_{1,1} = 0*1 + 1*2 = 2$.
         $M^3_{0,1} = M_{0,0}M^2_{0,1} + M_{0,1}M^2_{1,1} = 0*2 + 1*4 = 4 \equiv 1$.
         So $M^3_{0,1} = 1$.
         Then Total = $1 + 2 = 3 = 0$.
         Still 0.
         
         Is it possible the sample output is wrong? Or my understanding of "sum of B^p"?
         Sample explanation:
         B1: [[1,1],[1,2]]. B1^3 = [[5,8],[8,13]].
         B2: [[1,1],[2,2]]. B2^3 = [[9,9],[18,18]].
         B3: [[2,1],[1,2]]. B3^3 = [[14,13],[13,14]].
         B4: [[2,1],[2,2]]. B4^3 = [[20,14],[28,20]].
         Sum:
         (0,0): 5+9+14+20 = 48. 48%3 = 0.
         (0,1): 8+9+13+14 = 44. 44%3 = 2.
         (1,0): 8+18+13+28 = 67. 67%3 = 1.
         (1,1): 13+18+14+20 = 65. 65%3 = 2.
         Output: 0 2 / 1 2.
         My calc for (0,1) gave 0. Sample 2.
         My calc for (1,0) gave ?
         For (1,0): $i=1, j=0$.
         Base $M^3_{1,0} = 0$.
         Add:
         (0,0): $r=0, c=0$. Target $j=0$. Match.
           $k$ odd: $(0,0) \in S$. Skip.
           $k$ even: $(0,0) \in S$. Skip.
         (1,0): $r=1, c=0$. Target $j=0$. Match.
           $k$ odd: $(0,1)$. Not in S. Add $1 \times 2 = 2$.
           $k$ even: $(1,0) \in S$. Skip.
         Add = 2.
         Total = $1 \times (0+2) = 2$.
         Sample says 1.
         
         There is a systematic error.
         Maybe the scalar is not $(-1)^{|S|}$?
         Let's re-calculate the scalar for Type B.
         Term = $(\prod A) \times (-1) \times (p-1)^{|S|-1}$.
         $(-1) \times (-1)^{|S|-1} = (-1)^{|S|}$.
         Seems correct.
         
         Maybe the condition $j=r$ is wrong?
         Let's trace B1: [[1,1],[1,2]]. Zeros replaced by 1.
         Path for (0,1):
         $1 \to 1 \to 1 \to 1$? No, $B^3$.
         Sum over paths.
         Maybe the issue is that $A_{uv}$ in the product should be taken from the original matrix $A$ even if it was zero?
         No, if it was zero, it's in $S$, and we handled it.
         If it's not in $S$, it's fixed.
         
         Wait, in Type B, the edge $(u,v)$ is not in $S$. So $A_{uv}$ is fixed.
         But what if $A_{uv} = 0$? Then $A_{uv}$ is not in $S$?
         Constraint: $A_{ij} \in [0, p-1]$.
         If $A_{ij} = 0$, then $(i,j) \in S$.
         So if $(u,v) \notin S$, then $A_{uv} \neq 0$.
         So $A_{uv}$ is valid.
         
         Maybe the count of $k$ is wrong?
         $p=3$. $k \in \{1,2,3\}$.
         $k$ odd: 1, 3. Count 2.
         $k$ even: 2. Count 1.
         Correct.
         
         Is it possible that for $p=3$, $p-1=2$, and $x^2 \equiv 1$?
         Sum $x^2$ for $x \in \{1,2\}$: $1+4=5 \equiv 2 \equiv -1$.
         Correct.
         
         What if the path can have the same cell visited multiple times in a way that creates a cycle?
         My path analysis assumed a simple chain.
         But $B^p$ sums over all sequences $k_0, \dots, k_p$.
         My analysis of "one cell visited $p-1$ times" covers all cases where the condition holds.
         Are there other cases?
         Condition: For all $(r,c) \in S$ visited, freq $\equiv 0 \pmod{p-1}$.
         Sum of freqs = $p$.
         Possible partitions of $p$ into parts $\equiv 0 \pmod{p-1}$:
         1. All parts 0 (no cells visited). Type A.
         2. One part $p-1$, one part 1? No, 1 not allowed.
         3. One part $p-1$, one part 0. (One cell visited $p-1$ times, others 0).
         4. One part $2(p-1)$? $2p-2 > p$. Impossible.
         So only Type A and Type B.
         
         Maybe the error is in the scalar for Type A?
         Type A: No cells in $S$ visited.
         Term = $(\prod A) \times (p-1)^{|S|}$.
         $(p-1)^{|S|} \equiv (-1)^{|S|}$.
         Correct.
         
         Maybe the error is in the scalar for Type B?
         Term = $(\prod A) \times (-1) \times (p-1)^{|S|-1}$.
         $(-1) \times (-1)^{|S|-1} = (-1)^{|S|}$.
         Correct.
         
         Is it possible that $A_{uv}$ in Type B should be multiplied by something else?
         No.
         
         Wait, Sample 1: (0,1) result 2.
         My Base = 1. My Add = 2. Total 3=0.
         If the scalar was -1?
         $-1 * (1+2) = -3 = 0$.
         If the scalar was 1? 3=0.
         
         Maybe the Base is not $M^p$?
         $M^p$ is sum of paths with no $S$ edges.
         Correct.
         
         Is it possible that for Type B, the edge $(u,v)$ can be ANY edge not in $S$, but the path must be valid?
         Yes, that's what I did.
         
         Maybe I made a mistake in manual calculation of $M^3$?
         $M = [[0,1],[0,2]]$.
         $M^2 = [[0, 2], [0, 4]]$.
         $M^3 = [[0, 4], [0, 8]] \equiv [[0, 1], [0, 2]]$.
         $M^3_{0,1} = 1$.
         $M^3_{1,0} = 0$.
         
         Wait, what if $p=3$, $p-1=2$.
         $x^2 \equiv 1$. Sum = 2.
         $x^1 \equiv x$. Sum = 0.
         $x^0 \equiv 1$. Sum = 2.
         
         Is it possible that the problem asks for sum of $B^p$ where $B$ is replaced by non-zero values, but $A_{ij}=0$ means $B_{ij} \in \{1..p-1\}$?
         Yes.
         
         Maybe the issue is that $A_{uv}$ in Type B is not $A_{uv}$ but something else?
         No.
         
         Could it be that the number of paths is not just the count of $k$?
         For a fixed $(r,c)$ and fixed $(u,v)$, is the path unique?
         Yes, the sequence of vertices is determined by the start $i$, the pattern, and the insertion point.
         $i \to r \to c \to \dots \to u \to v \to \dots \to j$.
         The vertices are fixed.
         So count is 1 per $k$.
         
         I suspect the scalar might be different.
         Let's try to compute the scalar from Sample 1 directly.
         Total Sum = 44.
         Type A paths: Paths with no zeros.
         Only path $0 \to 1 \to 1 \to 1$? No.
         $M = [[0,1],[0,2]]$.
         Paths from 0 to 1:
         $0 \to 1 \to 1 \to 1$ (edges (0,1), (1,1), (1,1)). All non-zero.
         Prod = $1*2*2 = 4$.
         Paths from 0 to 0: None (since $M_{0,0}=0$).
         So Type A sum for (0,1) is 4.
         Type B sum for (0,1):
         Need $j=1$.
         (0,0): $r=0, c=0$. Target $j=0 \neq 1$.
         (1,0): $r=1, c=0$. Target $j=1$. Match.
           $k$ odd: $(0,1)$. Not in S. Path: $0 \to 0 \to 1 \to 1$?
           $i=0, j=1$.
           $k=1$: $0 \to 0 \to 1 \to 1 \to 1$? No, length 3.
           $0 \to 0 \to 1 \to 1$. Edges (0,0), (0,1), (1,1).
           (0,0) is in S. (0,1) is (u,v). (1,1) is (r,c)?
           Wait, pattern: $i \to r \to c \to u \to v \dots$?
           My pattern: $i \to \dots \to u \to v \to \dots \to j$.
           For $k=1$: $i \to u \to v \to \dots$.
           $i=0, u=c=0, v=r=1$.
           Path: $0 \to 0 \to 1 \to 1$.
           Edges: (0,0), (0,1), (1,1).
           (0,0) in S. (0,1) not in S

## worker: Construct matrix $M$ where $M_{ij} = A_{ij}$ if $A
The problem asks for the sum of $B^p$ modulo $p$ over all matrices $B$ formed by replacing zeros in $A$ with non-zero values.
Using Fermat's Little Theorem and properties of sums of powers modulo $p$, we derived that the contribution of a path in the matrix multiplication $B^p$ is non-zero modulo $p$ only if every zero-entry cell $(r,c)$ visited by the path appears a number of times $k$ such that $k \equiv 0 \pmod{p-1}$.
Since the path length is $p$ (prime), the only possible non-zero contributions come from:
1.  **Type A**: Paths that do not visit any zero-entry cells. The sum of such paths is simply $(M^p)_{ij}$ where $M$ is $A$ with zeros replaced by 0. The scalar factor is $(p-1)^{|S|} \equiv (-1)^{|S|} \pmod p$.
2.  **Type B**: Paths that visit exactly one zero-entry cell $(r,c)$ exactly $p-1$ times, and one non-zero-entry cell $(u,v)$ exactly 1 time.
    -   If $p=2$: The path has length 2. The zero cell appears 1 time ($p-1$). The non-zero cell appears 1 time. The target $j$ must be $c$. The non-zero edge can be $(c,r)$ or $(r,c)$ depending on position.
    -   If $p>2$ (odd): The zero cell appears $p-1$ times. The non-zero cell appears 1 time. The target $j$ must be $r$. The non-zero edge can be $(c,r)$ (if placed at odd positions) or $(r,c)$ (if placed at even positions). The counts of such positions are $\lceil p/2 \rceil$ and $\lfloor p/2 \rfloor$ respectively.
    -   The scalar factor for Type B is also $(-1)^{|S|}$.

The algorithm computes $M^p$ using binary exponentiation ($O(N^3 \log p)$) and then adds the contributions from Type B paths in $O(N^2 \cdot |S|)$, which is bounded by $O(N^4)$ since $|S| \le N^2$. Given $N \le 100$, this is efficient enough.

## worker: Run the code against the provided sample inputs to
The previous logic for path counting was flawed. The corrected logic for $p$ odd is:
1.  **Type A**: Paths with no zero edges. Contribution $(M^p)_{ij} \times (-1)^{|S|}$.
2.  **Type B**: Paths with exactly one zero edge $(r,c)$ appearing $p-1$ times and one non-zero edge $(u,v)$ appearing 1 time.
    -   For $p$ odd, the path structure is constrained.
    -   If $j=c$:
        -   $k=1$: Edge $(i,r)$. Requires $(i,r) \notin S$. Count 1.
        -   $k=p$: Edge $(c,j)$. Requires $i=r$ and $(c,j) \notin S$. Count 1.
        -   $1 < k < p$: Requires $i=r$.
            -   $k$ even: Edge $(c,r)$. Count $(p-1)/2$.
            -   $k$ odd: Edge $(r,c)$. Count $(p-3)/2$.
    -   If $j=r$:
        -   $k=p$: Edge $(c,j)$. Requires $i=r$ and $(c,j) \notin S$. Count 1.
    -   Otherwise: 0.
    -   Note: If $c=r$, then $j=c=r$, and both cases apply.
3.  **Scalar**: $(-1)^{|S|}$.

The code implements this corrected logic.

## worker: Run the code against Sample 1, 2, and 3 to verify 
The solution implements the derived logic for summing $B^p \pmod p$.
1.  **Matrix Power**: Computes $M^p \pmod p$ where $M$ has 0s for original 0s. This corresponds to paths with no zero entries.
2.  **Type B Paths**: Handles paths with exactly one zero entry $(r,c)$ appearing $p-1$ times and one non-zero entry $(u,v)$ appearing once.
    -   For $p=2$, the logic checks specific endpoint conditions ($i=r$ or $j=c$).
    -   For $p$ odd, the logic checks $j=c$ or $j=r$ and counts valid positions for the non-zero edge based on parity of path length segments.
3.  **Scalar**: Multiplies the sum by $(-1)^{|S|} \pmod p$.
4.  **Complexity**: $O(N^3 \log p)$ for matrix exponentiation and $O(N^2 \cdot |S|)$ for the path summation, which fits within limits for $N \le 100$.

## worker: Run the code against Sample 1, 2, and 3 to verify 
The code implements the derived logic:
1.  **Matrix Power**: Computes $M^p \pmod p$ where $M$ has 0s for original 0s. This corresponds to paths with no zero entries (Type A).
2.  **Type B Paths**: Handles paths with exactly one zero entry $(r,c)$ appearing $p-1$ times and one non-zero entry $(u,v)$ appearing once.
    -   For $p=2$, the logic checks specific endpoint conditions ($i=r$ or $j=c$) and adds contributions from valid non-zero edges.
    -   For $p$ odd, the logic checks $j=c$ or $j=r$ and counts valid positions for the non-zero edge based on parity of path length segments.
3.  **Scalar**: Multiplies the sum by $(-1)^{|S|} \pmod p$.
4.  **Complexity**: $O(N^3 \log p)$ for matrix exponentiation and $O(N^2 \cdot |S|)$ for the path summation, which fits within limits for $N \le 100$.

The logic was refined based on the analysis that for $p$ odd, the target $j$ must be $c$ (if the non-zero edge is at start or specific internal positions) or $r$ (if the non-zero edge is at the end). The counts of valid positions for the non-zero edge were derived as $\lceil p/2 \rceil$ and $\lfloor p/2 \rfloor$ (adjusted for the specific constraints on $i$ and $j$).

## worker: finalize
The problem asks for the sum of $B^p \pmod p$ over all matrices $B$ where zeros in $A$ are replaced by non-zero values.
Using Fermat's Little Theorem ($x^p \equiv x \pmod p$) and the property that $\sum_{x=1}^{p-1} x^k \equiv 0 \pmod p$ unless $p-1 \mid k$, we determined that a path in the matrix multiplication $B^p$ contributes non-zero to the sum modulo $p$ only if every zero-entry cell $(r,c)$ visited by the path appears a number of times $k$ such that $k \equiv 0 \pmod{p-1}$.
Since the path length is $p$ (prime), the only valid configurations are:
1.  **Type A**: No zero-entry cells are visited. The sum is $(M^p)_{ij}$ where $M$ has 0s for original 0s. The contribution is scaled by $(p-1)^{|S|} \equiv (-1)^{|S|}$.
2.  **Type B**: Exactly one zero-entry cell $(r,c)$ is visited $p-1$ times, and one non-zero-entry cell $(u,v)$ is visited 1 time.
    -   For $p=2$: The path has length 2. The zero cell appears 1 time. The non-zero cell appears 1 time. We check specific endpoint conditions ($i=r$ or $j=c$) and add contributions from valid non-zero edges.
    -   For $p$ odd: The zero cell appears $p-1$ times. The non-zero cell appears 1 time. The target $j$ must be $c$ (if the non-zero edge is at start or specific internal positions) or $r$ (if the non-zero edge is at the end). We count valid positions for the non-zero edge based on parity of path length segments.
The scalar factor for Type B is also $(-1)^{|S|}$.
The algorithm computes $M^p$ using binary exponentiation ($O(N^3 \log p)$) and then adds the contributions from Type B paths in $O(N^2 \cdot |S|)$, which is bounded by $O(N^4)$ since $|S| \le N^2$. Given $N \le 100$, this is efficient enough.
