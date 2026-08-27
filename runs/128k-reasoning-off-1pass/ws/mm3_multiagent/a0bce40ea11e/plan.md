Let $K$ be the number of zero entries in $A$. Each zero can be replaced by any of the $p-1$ nonzero values in $\mathbb{F}_p$, so we sum $B^p$ over all such $B$. For a fixed zero $z$, summing a polynomial $f(z)$ over all nonzero $z \in \mathbb{F}_p$ equals $-(p-1)f(0) + \sum_{x\in\mathbb{F}_p} f(x)$ by inclusion-exclusion. Since $p$ is prime, $\sum_{x\in\mathbb{F}_p} x^k = 0$ for $0<k<p$ and $= -1$ for $p\mid k$. We apply this entrywise to $B^p$, expand it, and simplify using the fact that each zero appears in many monomials. After simplification, the sum over all $B$ of $B^p$ equals $-(p-1)^K \cdot A^p + (p-1)^K \cdot (p \text{ divides power}) \cdot \text{(something)}$.

Actually, let's verify: For each zero position, in $B^p$ entries, we need sums of monomials of degree $p$ where some variables are zeros. The trick: $\sum_{B} B^p = (p-1)^K \cdot A^p$ if we simply replace each zero by the average? No, we need exact.

Let $Z$ be the set of zero positions. For any polynomial $f(x_1,\ldots,x_K)$ homogeneous of degree $p$ in the zero-variables, the sum over all nonzero assignments is:
$$S(f) = \sum_{x_i \in \mathbb{F}_p^*} f(x) = \sum_{x \in \mathbb{F}_p^K} f(x) - \sum_{S \neq \emptyset} (-1)^{|S|+1} \sum_{x_i=0, i\in S} f(x)$$
This is complex. But note: $B^p$ is a matrix of monomials, each monomial has degree $p$ total. The sum of $B^p$ over all $B$ can be computed by a known technique: replace each zero with a formal variable, compute, then for each variable sum over $\mathbb{F}_p^*$ using the trick. But the answer is:

**Key insight**: $\sum_{x \in \mathbb{F}_p^*} x^k = -1$ if $(p-1) | k$ and $k>0$, else $0$ (for $0<k$). Wait: $x \in \mathbb{F}_p^*$ has order $p-1$. $\sum_{x \in \mathbb{F}_p^*} x^k = 0$ unless $(p-1) | k$, in which case it equals $p-1$. So sum over $\mathbb{F}_p^*$ of $x^k$ is $p-1$ if $(p-1)|k, k>0$, else $0$.

Hmm, but we also have $-x^k$ adjustment? Let's recompute: Let $S^* f = \sum_{x_i \in \mathbb{F}_p^*} f(x)$. We can write this as $\sum_{x \in \mathbb{F}_p^K} f(x) - \sum_{\text{some } x_i=0} \cdots$, which involves inclusion-exclusion. This becomes complicated.

Let me think differently. We want $\sum_B B^p$. Consider $B = A + E$ where $E$ has the zero positions as free variables and others zero. So $B = A + E$, $E_{ij} \in \{0, 1, \ldots, p-1\}$ if $A_{ij}=0$ (actually $E_{ij} \in \mathbb{F}_p$, representing the choice), and $E_{ij}=0$ if $A_{ij}\neq 0$. Then $\sum_B B^p = \sum_{E} (A+E)^p$.

Expand: $(A+E)^p = \sum_{k=0}^p \binom{p}{k} A^{p-k} E^k$ over the matrix product? No, $A$ and $E$ are matrices, they don't commute in general. But $A$ and $E$ do commute since $E$ is a diagonal-like matrix (only zeros and free vars)? No, $E$ is not diagonal.

Actually, $A$ and $E$ don't necessarily commute. So this approach is messy.

**Better approach**: Think entrywise. $B^p_{ij} = \sum_{i_1,\ldots,i_{p-1}} B_{i,i_1} B_{i_1,i_2} \cdots B_{i_{p-1},j}$. Each term is a product of $p$ entries of $B$. We sum over all choices of $B$. For a monomial $m = \prod_{t} B_{r_t, c_t}$ (with repetition allowed), the sum over $B$ is $\prod_{(r,c): A_{rc}=0} (\sum_{x \in \mathbb{F}_p^*} x^{\deg_{rc}(m)})$ since for nonzero $A_{rc}$, the entry is fixed. Here $\deg_{rc}(m)$ is the number of times $(r,c)$ appears in the monomial.

Now $\sum_{x \in \mathbb{F}_p^*} x^d$ is $p-1$ if $(p-1) | d$ and $d > 0$, else $0$. So the sum is nonzero only if for every zero position $(r,c)$, the count of times it appears is a multiple of $p-1$. Since total degree is $p$, and $p$ is prime, either $p-1$ divides this count, or it equals $0$.

Case 1: $p=1$. But $p$ is prime and $1\le p$, so $p \ge 2$? Constraint says $1 \le p \le 10^9$, prime. Primes are $\ge 2$. So $p \ge 2$.

If $p=2$, then $p-1=1$, so every count satisfies $(p-1)|d$, and the sum is always $(p-1)^K = 1$ times the product of entries. So the answer is $\sum_B B^2$ where each zero entry is summed over $\mathbb{F}_2^*=\{1\}$. So $B$ is fixed, and the answer is just $B^2$ for that single $B$. That matches sample 2: identity matrix, $B^2 = $ all ones matrix, sum mod 2 = 1.

For $p \ge 3$: $p-1 \ge 2$. Each zero position must appear a multiple of $p-1$ times. The total degree is $p$. So if a zero position appears $0$ times, it contributes nothing. If it appears $p-1$ times, then the other factor must have total degree $1$, meaning it's a single entry from $A$ (nonzero). So the monomial has $p-1$ copies of one zero position and $1$ copy of one nonzero $A$ position. Or, if the count is $0$ mod $p-1$ and positive, it could be $p-1$ (since $2(p-1) > p$ for $p \ge 3$).

So the sum reduces to: for each monomial which is a path of length $p$ (in the matrix-product sense: $p$ entries multiplied), such that exactly one zero position is used $p-1$ times and one nonzero position is used $1$ time, contribute $(p-1)^K$ times $1$ (the value of the nonzero $A$ entry). All other monomials contribute $0$.

So the sum is $(p-1)^K \cdot \sum_{(i,j): A_{ij} \neq 0} A_{ij} \cdot C^{(i,j)}$ where $C^{(i,j)}$ is the count of length-$p$ paths where zero position $z$ appears $p-1$ times and position $(i,j)$ appears once, for some fixed zero $z$. Wait, we need to sum over all zero positions $z$, and for each $z$, count the number of ways to form a length-$p$ monomial (in the matrix-power sense) where $z$ is used $p-1$ times and some nonzero position is used once. Then multiply by $A_{ij}$ for that nonzero position.

But wait, the monomial for $B^p_{ab}$ is $\sum_{i_1,\ldots,i_{p-1}} B_{a,i_1} B_{i_1,i_2} \cdots B_{i_{p-1},b}$. This is a sum over sequences $(a=i_0, i_1, \ldots, i_{p-1}, i_p=b)$ of products. Each product is a specific multiset of matrix entries. We need the count of sequences such that the multiset has one nonzero position appearing once and one zero position appearing $p-1$ times.

So the total sum is $(p-1)^K \cdot \sum_{z \in Z} \sum_{e: A_e \neq 0} A_e \cdot N^{(z,e)}$ where $N^{(z,e)}$ is the number of paths $(a=i_0, i_1, \ldots, i_p=b)$ such that the edge multiset consists of $p-1$ copies of $z$ and one copy of $e$, and we're computing the $(a,b)$ entry.

We can precompute: For each zero position $z=(r,c)$, and for each path length $p$ with $p-1$ copies of $z$ and $1$ copy of $e$, the path is determined by the position of $e$ in the sequence. The path has $p+1$ vertices $i_0, i_1, \ldots, i_p$ and $p$ edges (each edge is the pair $(i_{t-1}, i_t)$). We need $p-1$ edges to be $z$ and $1$ edge to be $e$. 

If $e=(i_{k-1}, i_k)$ for some $k$, then the other edges are $z$. The path alternates: if $z=(r,c)$, the path is forced: starting from some vertex, we follow $z$ repeatedly. The sequence of vertices is determined by the start and the position of $e$. Let's say the path is $v_0, v_1, \ldots, v_p$. The edge $v_{t-1} \to v_t$ is $z$ for $p-1$ of the $t$'s, and $e$ for one $t$. If the $e$ edge is at position $k$ (meaning $v_{k-1} \to v_k$ is $e$), then $v_0, v_1, \ldots, v_{k-1}$ is a sequence where each step is $z$, and $v_k, v_{k+1}, \ldots, v_p$ is also a sequence where each step is $z$. So $v_{k-1} = ?$ Let's compute: starting from $v_0$, applying $z$ means $v_t = $ row of $z$ if $t$ is such that the step is $z$? Wait, $z=(r,c)$ means the edge is $r \to c$. So $v_{t} = c$ if the step from $v_{t-1}$ to $v_t$ is $z$ and $v_{t-1}=r$. So all $v_t$ for $t \ge 1$ that are reached by a $z$-step from $r$ will be $c$. Specifically, if $v_{t-1}=r$ and step is $z$, then $v_t=c$. Otherwise, we need to trace.

Actually, if $p-1$ steps are $z=(r,c)$ and the path has vertices $v_0, v_1, \ldots, v_p$:
- For $t$ such that step $t$ (from $v_{t-1}$ to $v_t$) is $z$, we have $v_{t-1}=r$ and $v_t=c$.
- For the step that is $e=(i,j)$, we have $v_{k-1}=i$ and $v_k=j$.

Since only one step is not $z$, the path is almost entirely forced. Let's see: if $k=1$, then $v_0 \to v_1$ is $e$, so $v_0=i, v_1=j$. Then steps 2 through $p$ are $z$. So $v_1 \to v_2$ is $z$, requiring $v_1=r$ and $v_2=c$. But $v_1=j$, so we need $j=r$. Then $v_2=c$, $v_3=c$ (if step 3 is $z$ and $v_2=r$? No, step 3 is $v_2 \to v_3$ is $z$, requiring $v_2=r$ and $v_3=c$. But $v_2=c$, so we need $c=r$. Then $v_3=c=r$, $v_4=c$... this continues. So the path is $i, j=r, c, c, \ldots, c$ with $v_p = c$. This requires $j=r$.

Similarly for other $k$. In general, the path is: starting from $v_0$, we have $z$-steps except at position $k$. The $z$-steps force vertices to be $r$ or $c$. Specifically, a $z$-step from $r$ goes to $c$, and from $c$ goes to $c$ (if $c$ is the row index of $z$? No, $z$ is the edge $r \to c$, so the row is $r$. If the current vertex is $c$, a $z$-step would require the row to be $r$, but current vertex is $c$. So if current vertex $\neq r$, the step cannot be $z$. 

Wait, I confused. A $z$-step is the edge $(r,c)$. This means the previous vertex is $r$ and the next is $c$. So a $z$-step can only occur if the current vertex is $r$. If the current vertex is not $r$, the step is not $z$.

So in the path, every $z$-step requires the current vertex to be $r$ and the next is $c$. So if we have a run of $z$-steps, the first one goes $r \to c$, but then the next $z$-step would need the current vertex to be $r$, but it's $c$. So a run of consecutive $z$-steps is impossible unless... wait, $v_{t-1}=r$ and $v_t=c$ for a $z$-step. Then for the next step to be $z$, we need $v_t=r$, but $v_t=c$. So only isolated $z$-steps are possible, separated by other steps. 

Hmm, but we have $p-1$ copies of $z$ and 1 copy of $e$, total $p$ steps. The steps are ordered. The $z$-steps can be interleaved with the $e$-step. Since only one $e$-step, the path is: some $z$-steps, then $e$, then some $z$-steps. But a $z$-step requires the current vertex to be $r$. Let's trace: start at $v_0$. If step 1 is $z$, then $v_0=r$, $v_1=c$. Step 2 is $z$ requires $v_1=r$, but $v_1=c$, contradiction unless $c=r$. If $c=r$ (diagonal zero), then $v_0=r, v_1=r$, and we can have a run of $z$-steps all staying at $r$. 

If $z$ is not on the diagonal, then $c \neq r$. A $z$-step goes $r \to c$. The next step, if also $z$, would need to start at $r$, but we are at $c \neq r$. So $z$-steps cannot be adjacent. The only way to have $p-1$ copies of $z$ and $1$ of $e$ in $p$ steps, with $z$-steps non-adjacent (unless $r=c$), is: the $e$-step separates groups of $z$-steps. The maximum number of $z$-steps in $p$ steps with at most one group? If $e$-step is at position $k$, then steps $1,\ldots,k-1$ are $z$ and steps $k+1,\ldots,p$ are $z$. For steps $1$ to $k-1$ to all be $z$, we need $v_0=r, v_1=c, v_2=c$? But $v_1=c$, so step 2 requires $v_1=r$, contradiction. So actually, if $r \neq c$, we cannot have two consecutive $z$-steps. So the $z$-steps must be isolated. The maximum number of isolated $z$-steps in $p$ steps with one $e$-step is: place the $e$-step, then $z$-steps can only be at positions where the current vertex is $r$. This is very restrictive.

Let's reconsider. The condition is: the multiset of edges used is $\{z, z, \ldots, z, e\}$ with $p-1$ copies of $z$. The path is a sequence of vertices $v_0, v_1, \ldots, v_p$ with edges $(v_{t-1}, v_t)$. Each edge is either $z$ or $e$.

Let $T = \{t : (v_{t-1}, v_t) = z\}$ and $k$ be the unique element not in $T$. So $|T| = p-1$.

For $t \in T$: $v_{t-1} = r$ and $v_t = c$.
For $t = k$: $v_{k-1} = i$ and $v_k = j$ where $e=(i,j)$.

Now, for $t \in T$ and $t+1 \in T$ (consecutive), we have $v_t = c$ and $v_{t+1} = c$ (from the $t+1$ condition: $v_t = r$? No, the condition for step $t+1$ being $z$ is $v_t = r$ and $v_{t+1}=c$. So if steps $t$ and $t+1$ are both $z$, then $v_t = c$ (from step $t$) and $v_t = r$ (from step $t+1$). So $c=r$.

So: if $r \neq c$, then no two consecutive steps can be $z$. Since there is only one non-$z$ step, the $z$-steps are all consecutive except for one interruption. But if $r \neq c$, the $z$-steps form a contiguous block. The block can have length at most 1? Let's see: if we have a block of $z$-steps of length $L \ge 2$, then the first step goes $r \to c$, but the second step needs to start at $r$, contradiction. So if $r \neq c$, the block length is at most 1. But we need $p-1$ copies of $z$, so we need $p-1$ blocks, which is impossible since there's only one non-$z$ step creating two blocks. So if $r \neq c$, we cannot have $p-1$ copies of $z$ unless $p-1 \le 1$, i.e., $p \le 2$. Since $p$ is prime $\ge 2$, for $p=2$, $p-1=1$, which is fine.

For $p \ge 3$ and $r \neq c$: no contribution from this $z$.

If $r = c$ (diagonal zero), then $z = (r,r)$. A $z$-step goes $r \to r$. So any step from $r$ can be $z$ (going to $r$). Then we can have a run of $z$-steps: the path is $r, r, r, \ldots, r$ with one $e$-step. The $e$-step $(i,j)$ requires $i$ to be the vertex before it. So the path is: start at some vertex, go to $r$ somehow? No, the path is continuous. Let's say the $e$-step is at position $k$. The path: $v_0, v_1, \ldots, v_{k-1}, v_k, v_{k+1}, \ldots, v_p$ with $v_{k-1} \to v_k$ being $e=(i,j)$. The other steps are $z=(r,r)$. For step $t$ to be $z$, we need $v_{t-1}=r$ and $v_t=r$. So all vertices except possibly $v_{k-1}$ and $v_k$ that are adjacent to $e$-steps must be $r$. Specifically:
- For $t < k$: $v_{t-1}=r, v_t=r$. So $v_0=r, v_1=r, \ldots, v_{k-1}=r$.
- For $t > k$: $v_{t-1}=r, v_t=r$. So $v_k=r, v_{k+1}=r, \ldots, v_p=r$.
- The $e$-step: $v_{k-1}=i, v_k=j$.
But from the $z$ conditions, $v_{k-1}=r$ and $v_k=r$. So $i=r$ and $j=r$. But $e=(i,j)$ is a nonzero position, and $A_{ij} \neq 0$, so $e$ could be anything. However, the conditions force $i=j=r$. So $e$ must be $(r,r)$, i.e., on the diagonal at row $r$. 

Wait, but $e$ is a nonzero position, meaning $A_{ij} \neq 0$. It could be on the diagonal. So if $z=(r,r)$ is a zero, then for a monomial to survive, the one nonzero position used must be on the same diagonal position $(r,r)$. And the path is all $r$'s: $v_0=v_1=\cdots=v_p=r$. Then the $e$-step is also $(r,r)$, but that's the same as $z$! Contradiction, because $e$ is a nonzero position and $z$ is a zero position, they are different. Unless... $e=(r,r)$ is a different entry from $z=(r,r)$? But they are the same matrix position. Since $A_{rr}$ is either zero or nonzero, it can't be both. So if $z=(r,r)$ is a zero, then $(r,r)$ is not a nonzero position, so no such $e$ exists. 

Therefore, for $p \ge 3$, there are NO surviving monomials! The sum should be the zero matrix.

But sample 1 has $p=3$, and the answer is not zero. Sample 1: $A = \begin{pmatrix} 0 & 1 \\ 0 & 2 \end{pmatrix}$, zeros at $(1,1)$ and $(2,1)$. According to my analysis, sum should be zero. But sample output is $\begin{pmatrix} 0 & 2 \\ 1 & 2 \end{pmatrix}$. So my analysis is wrong.

Let me re-examine. I claimed that for a monomial to survive, each zero position must appear a multiple of $p-1$ times. But I used the sum over $\mathbb{F}_p^*$. Wait, I need to recheck: the sum over $B$ of $B^p_{ij}$ is $\sum_{B} \sum_{paths} \prod B_{entry}$. For a fixed monomial $m$ (a product of entries), $\sum_B m = \prod_{z \in Z} (\sum_{x_z \in \mathbb{F}_p^*} x_z^{\deg_z(m)})$. Yes, because the $B$ choices are independent across zero positions. So the sum is $\prod_z S(\deg_z(m))$ where $S(d) = \sum_{x \in \mathbb{F}_p^*} x^d$.

Now $S(d) = \sum_{x=1}^{p-1} x^d \pmod p$. 
- If $d=0$: $S(0) = p-1 \equiv -1 \pmod p$.
- If $d > 0$ and $(p-1) \nmid d$: $S(d) = 0 \pmod p$.
- If $d > 0$ and $(p-1) | d$: $S(d) = p-1 \equiv -1 \pmod p$.

So $S(d) \equiv -1 \pmod p$ iff $d$ is a multiple of $p-1$ (including 0), and $0$ otherwise.

So for the product to be nonzero mod $p$, we need for each zero $z$, $\deg_z(m) \equiv 0 \pmod{p-1}$.

This is what I had. Then for $p=3$, $p-1=2$. Each zero must appear 0 or 2 times. Total degree is 3. So possibilities: one zero appears 2 times, and the remaining 1 is a nonzero position. Or, a zero appears 0 times (meaning all 3 are nonzero), but then the product is over nonzero positions only, which is fixed, and we have no zero variables, so the factor is 1 (empty product). Wait, if a zero appears 0 times, then $\deg_z(m)=0$, and $S(0) = -1$ for that zero. So we have a factor of $-1$ for each zero not used. 

So the full condition: for each zero $z$, $\deg_z(m) \in \{0, 2\}$ (since $2 \le 3$). And total $\sum \deg = 3$.

Cases:
- One zero $z_0$ has $\deg=2$, all others have $\deg=0$, and the remaining one factor is a nonzero position $e$ with $\deg_e(m)=1$.
- Three nonzero positions (no zero used), so all zeros have $\deg=0$.

So the surviving monomials are of two types:
Type 1: Three distinct (or with repetition) nonzero positions multiplied together.
Type 2: One zero position $z$ used twice, one nonzero position $e$ used once.

In both cases, the contribution to the sum mod $p$ is a factor of $(-1)^K$ from all the zeros with $\deg=0$ (i.e., $S(0)=-1$ for each). 

Type 1 monomials: no zero used, so each zero contributes $S(0)=-1$. Product = $(-1)^K$. The value is $\prod_{e} A_e^{\deg_e(m)}$. Sum over all such monomials = $(-1)^K \cdot (A^p)$? Wait, $A^p$ is the sum over all paths of length $p$ of the product of $A$ entries. That's exactly the sum over monomials using only nonzero positions, but in $A^p$ the entries are from $A$, which has zeros. We need to be careful: $A^p_{ij} = \sum_{paths} \prod A_{v_{t-1},v_t}$. For a monomial to be "Type 1", all factors must be nonzero positions, meaning the path only uses nonzero entries of $A$. So it's a sub-sum of $A^p$.

Type 2 monomials: one zero $z$ used twice, one nonzero $e$ used once. Factor from zeros: $(-1)^K$ (since all zeros have $\deg=0$ except $z$ which has $\deg=2$, $S(2)=p-1=-1$ as well! So $S(2) \equiv -1 \pmod 3$ since $p-1=2$ divides 2). Wait, for $p=3$, $S(2) = 1^2 + 2^2 = 1+4=5 \equiv 2 \equiv -1 \pmod 3$. Yes. So both $\deg=0$ and $\deg=2$ give $S(d)=-1$. So the product is $(-1)^K$ for both types! 

In general, $S(d) \equiv -1 \pmod p$ iff $(p-1)|d$ (including $d=0$). And $(p-1)|d$ and $d>0$ means $d \ge p-1$. Since total degree is $p$, and $p-1 \le p$, the only positive multiple of $p-1$ that is $\le p$ is $p-1$ itself (since $2(p-1) > p$ for $p \ge 3$). For $p=2$, $p-1=1$, so all degrees work.

So for $p \ge 3$: each zero in the monomial either appears 0 times or $p-1$ times. Total degree $p$, so exactly one zero appears $p-1$ times and the rest 0 times, or all zeros appear 0 times. In both cases, the sum factor is $(-1)^K$.

Therefore, the total sum mod $p$ is $(-1)^K \cdot [ \text{sum over paths of length } p \text{ using only nonzero positions} \times \text{something} ]$? Let's be precise.

Let $S = \sum_B B^p$. We have $S_{ij} = \sum_{paths P: v_0=i, v_p=j} \sum_{B} \prod_{t=1}^p B_{v_{t-1},v_t}$.

For a fixed path $P$, the monomial is $m_P = \prod_{t=1}^p B_{v_{t-1},v_t}$. The sum over $B$ is $\prod_{z \in Z} S(\deg_z(P))$ where $\deg_z(P)$ is the number of times the edge $z$ appears in $P$.

As argued, for $p \ge 3$, this is nonzero mod $p$ only if every zero appears 0 or $p-1$ times in $P$.

Case A: All zeros appear 0 times in $P$ (i.e., the path uses only nonzero positions). Then the product is $\prod_{(r,c) \in P} A_{r,c}$, and the factor is $\prod_z S(0) = (p-1)^K \equiv (-1)^K \pmod p$.

Case B: Exactly one zero $z_0$ appears $p-1$ times, and one nonzero position $e$ appears 1 time (the rest of the path is $z_0$). The factor is again $(p-1)^K \equiv (-1)^K$ since $S(p-1) = p-1 \equiv -1$.

In both cases, the factor is $(-1)^K \pmod p$.

So $S_{ij} \equiv (-1)^K \cdot [ \sum_{P \text{ using only nonzero}} \prod A + \sum_{z_0 \in Z} \sum_{P: \text{ uses } z_0 \text{ } p-1 \text{ times and one } e} \prod A ] \pmod p$.

The first sum is exactly $(A')^p_{ij}$ where $A'$ is $A$ with zeros replaced by 1? No, it's the sum over paths avoiding zeros of the product of $A$ values. That's like $(A \odot \text{mask})^p$ but with the mask... actually, let $M$ be the matrix with $M_{ij} = A_{ij}$ if $A_{ij} \neq 0$ and $0$ if $A_{ij}=0$. Then the first sum is $(M^p)_{ij}$.

The second sum: for each zero $z_0 = (r_0, c_0)$, and for each nonzero $e = (i_e, j_e)$ with $A_{e} \neq 0$, count the number of paths $P$ from $i$ to $j$ of length $p$ such that the multiset of edges is $\{z_0, z_0, \ldots, z_0, e\}$ ($p-1$ times $z_0$). Then multiply by $A_e$.

This is still complex. But note: the path has $p$ edges. $p-1$ of them are $z_0$, one is $e$. The path is a sequence. Let's count the number of such paths for fixed $i,j,z_0,e$.

Let $z_0 = (r,c)$ and $e = (u,v)$. The path is $v_0=i, v_1, \ldots, v_p=j$. The edges are $e_1, e_2, \ldots, e_p$ where $e_t = (v_{t-1}, v_t)$. We need $e_t = z_0$ for all $t \neq k$ and $e_k = e$ for some $k \in \{1,\ldots,p\}$.

For $t \neq k$: $v_{t-1} = r$ and $v_t = c$.
For $t = k$: $v_{k-1} = u$ and $v_k = v$.

Now, for $t < k$ and $t \neq k$: $v_{t-1}=r, v_t=c$. This means:
- If $k > 1$, then for $t=1,\ldots,k-1$, we have $v_0=r, v_1=c, v_2=c, \ldots$? Let's compute:
  - $t=1$: $v_0=r, v_1=c$.
  - $t=2$: $v_1=r, v_2=c$. But $v_1=c$, so $c=r$. 
  So if $k-1 \ge 2$ (i.e., $k \ge 3$), we need $c=r$ to have $t=2$ work.
  
  More carefully, for $t \in \{1,\ldots,k-1\}$, we have $v_{t-1}=r$ and $v_t=c$. 
  - $t=1$: $v_0=r, v_1=c$.
  - $t=2$: requires $v_1=r$ and $v_2=c$. Since $v_1=c$, need $c=r$ and $v_2=c$.
  - If $c=r$, then $v_1=c=r$, $v_2=c=r$, etc. So all $v_t = r$ for $t < k$.
  If $c \neq r$, then $k-1$ can be at most 1, so $k \le 2$.

Similarly for $t > k$: $v_{t-1}=r, v_t=c$ for $t=k+1,\ldots,p$.
  - $t=k+1$: $v_k=r, v_{k+1}=c$.
  - $t=k+2$: $v_{k+1}=r, v_{k+2}=c$, so need $v_{k+1}=r$, but $v_{k+1}=c$, so need $c=r$.
  
So in general, the $z_0$-steps force the vertices to be $r$ (except possibly at the boundaries near the $e$-step). The path looks like: 
- From $v_0$ to $v_{k-1}$: sequence of $z_0$-steps.
- Step $k$ is $e$.
- From $v_k$ to $v_p$: sequence of $z_0$-steps.

For the first part: if there are $k-1$ steps, all $z_0$, then:
  - $v_0 \to v_1$ is $z_0$: need $v_0=r$ and $v_1=c$.
  - $v_1 \to v_2$ is $z_0$: need $v_1=r$ and $v_2=c$. So if $k-1 \ge 2$, need $v_1=r$, but $v_1=c$, so $c=r$ and then $v_2=c=r$.
  So if $c=r$, then all $z_0$-steps are $(r,r)$, and the path stays at $r$: $v_0=v_1=\cdots=r$ for all vertices before $v_k$? Let's see: if $z_0=(r,r)$, then a step from $r$ goes to $r$. So yes, the path can be at $r$ arbitrarily. Specifically, for the first $k$ vertices $v_0,\ldots,v_{k-1}$, they are all $r$ if we only take $z_0$-steps? Wait, if all steps are $z_0=(r,r)$, then yes, $v_0=r$ implies $v_1=r$, etc. But we also have the $e$-step at position $k$: $v_{k-1} \to v_k$ is $e=(u,v)$, so $v_{k-1}=u$ and $v_k=v$. But from the $z_0$ sequence, $v_{k-1}=r$. So $u=r$. Similarly, for $t>k$, $v_k=r$ (from $z_0$ step at $k+1$: $v_k=r, v_{k+1}=c=r$). So $v=v_k=r$. Thus $e=(r,r)$. But $e$ is a nonzero position, and $z_0=(r,r)$ is a zero position, so they are the same position, contradiction. 

Therefore, there are NO surviving monomials of Type B for any $p$! Unless... wait, in Type B, $z_0$ is a zero and $e$ is a nonzero position, so they are different. Thus the case $c=r$ leads to contradiction. For $c \neq r$, the $z_0$-steps are isolated, but we need $p-1$ of them in $p$ steps with only one interruption. Let's check the constraint carefully.

Suppose $c \neq r$. For $t < k$ and $t \neq k$, step $t$ is $z_0$, so $v_{t-1}=r, v_t=c$. 
If $k-1 \ge 2$, then steps 1 and 2 are both $z_0$. Step 1: $v_0=r, v_1=c$. Step 2: $v_1=r, v_2=c$. But $v_1=c \neq r$, contradiction. So $k-1 \le 1$, i.e., $k \in \{1,2\}$.

Similarly, for $t > k$, step $t$ is $z_0$, so $v_{t-1}=r, v_t=c$. If there are $\ge 2$ steps after $k$, i.e., $p-k \ge 2$, then steps $k+1$ and $k+2$ are $z_0$. Step $k+1$: $v_k=r, v_{k+1}=c$. Step $k+2$: $v_{k+1}=r, v_{k+2}=c$. But $v_{k+1}=c \neq r$, contradiction. So $p-k \le 1$, i.e., $k \ge p-1$.

Combining: $k \in \{1,2\}$ and $k \ge p-1$. For $p \ge 3$, $p-1 \ge 2$, so $k=2$ and $p-1 \le 2$, so $p \le 3$. 
- If $p=2$, then $p-1=1$, $k \ge 1$, $k \le 2$ (since $k \in \{1,2\}$ and $k \ge p-1=1$). So $k \in \{1,2\}$.
- If $p=3$, then $p-1=2$, $k \ge 2$ and $k \le 2$, so $k=2$.

For $p=3$, $k=2$. Let's check $p=3, k=2, c \neq r$.
Path: $v_0, v_1, v_2, v_3$ with $v_0=i, v_3=j$.
Step 1: $z_0=(r,c)$, so $v_0=r, v_1=c$.
Step 2: $e=(u,v)$, so $v_1=u, v_2=v$.
Step 3: $z_0=(r,c)$, so $v_2=r, v_3=c$.

From step 1: $v_0=r, v_1=c$.
From step 2: $v_1=u, v_2=v$.
From step 3: $v_2=r, v_3=c$.

So $v_0=r$, $v_1=c=u$, $v_2=v=r$, $v_3=c$.
Thus $i = r$, $j = c$.
And $e = (u,v) = (c, r)$.
So $e$ must be $(c, r)$, and $A_{c,r} \neq 0$ (nonzero).
And $i=r, j=c$.

This is a valid path! For sample 1: $p=3$, zeros at $(1,1)$ and $(2,1)$. 
For $z_0=(1,1)$: $r=1,c=1$, but $c=r$, so this case doesn't apply (we assumed $c \neq r$).
For $z_0=(2,1)$: $r=2,c=1$, $c \neq r$. Then $i=2, j=1$. And $e=(c,r)=(1,2)$. $A_{1,2}=1 \neq 0$. Good. So there is one path: $v_0=2, v_1=1, v_2=2, v_3=1$. Check: step 1: $(2,1)=z_0$? $z_0=(2,1)$, yes. Step 2: $(1,2)=e$, yes. Step 3: $(2,1)=z_0$, yes. So the path exists. The product is $B_{2,1} B_{1,2} B_{2,1} = z_0^2 \cdot e$. Sum over $B$: $S(2) \cdot S(1) \cdot \prod_{other} S(0) = (-1) \cdot (-1) \cdot (-1)^{K-1}$? Let's see: $K=2$ zeros. For $z_0$, $\deg=2$, $S(2)=-1$. For other zero $(1,1)$, $\deg=0$, $S(0)=-1$. So product $= (-1)^2 = 1$. Value: $1 \cdot A_{1,2}^1 = 1 \cdot 1 = 1$. So contribution to $(2,1)$ entry is 1.

Similarly for $z_0=(1,1)$? $r=c=1$. We need to check the $r=c$ case separately. Earlier I argued no contribution, but let's recheck. If $r=c$, then $z_0=(r,r)$. Step is $r \to r$. For $k=2$ (only possibility for $p=3$ with $p-1=2$ and $k \ge p-1$, $k \le 2$):
Path: $v_0, v_1, v_2, v_3$. Steps: 1: $z_0$, 2: $e$, 3: $z_0$.
Step 1: $v_0=r, v_1=r$.
Step 2: $v_1=u, v_2=v$.
Step 3: $v_2=r, v_3=r$.
So $v_0=r, v_1=r=u, v_2=v=r, v_3=r$.
Thus $i=r, j=r$, and $e=(r,r)$. But $z_0=(r,r)$ is a zero, so $(r,r)$ is zero, contradicting $e$ nonzero. So no path.

Therefore, for sample 1, the only Type B path is for $z_0=(2,1)$, $e=(1,2)$, contributing to $(i,j)=(2,1)$. Value 1.

Now Type A: paths using only nonzero positions. Nonzero positions: $(1,2)$ with value 1, $(2,2)$ with value 2. 
All paths of length 3 from $i$ to $j$ using only these edges. The graph has edges $1\to2$ and $2\to2$. 
Possible paths:
- $1 \to 2 \to 2 \to 2$: uses $(1,2), (2,2), (2,2)$. Product $1 \cdot 2 \cdot 2 = 4 \equiv 1 \pmod 3$. End: $j=2$. Start $i=1$. So $(1,2)$ entry gets $1$.
- $2 \to 2 \to 2 \to 2$: uses $(2,2)^3 = 8 \equiv 2 \pmod 3$. Start $i=2$, end $j=2$. So $(2,2)$ gets $2$.

Type A contribution to $(1,2)$: $1$. To $(2,2)$: $2$. To $(2,1)$: 0. To $(1,1)$: 0.

Total with factor $(-1)^K = (-1)^2 = 1$:
$(1,1)$: 0
$(1,2)$: $0 + 1 = 1$? But sample output has $(1,2)=2$. And $(2,1)=1$, $(2,2)=2$.

Wait, I missed something. Type A is paths avoiding zeros. But for $p=3$, $A^p$ using only nonzero positions is computed. But we also have to consider that in the expansion, we have $(-1)^K$ factor. Here $K=2$, so $(-1)^2=1$.

But $(1,2)$ should be 2. Let me compute manually from sample. The sample says sum of $B^3$ over all $B$ is $\begin{pmatrix} 48 & 44 \\ 67 & 65 \end{pmatrix} \equiv \begin{pmatrix} 0 & 2 \\ 1 & 2 \end{pmatrix} \pmod 3$.

Compute Type A for $(1,2)$: path $1\to2\to2\to2$: product $1 \cdot 2 \cdot 2 = 4 \equiv 1$. That's the only path. So 1.

Type B for $(1,2)$: need $i=1, j=2$. From the analysis, for $z_0=(r,c)$ with $c \neq r$, $i=r, j=c$. So we need $r=1, c=2$, but there is no zero at $(1,2)$. For $z_0=(2,1)$, $i=2, j=1$. Not $(1,2)$. So no Type B for $(1,2)$.

But sample has 2. What's wrong?

Oh! I see. In the sum over $B$, for Type A (no zero used), the factor is $\prod_z S(0) = (p-1)^K$. For $p=3, K=2$, $(p-1)^K = 2^2 = 4 \equiv 1 \pmod 3$. Good.

For Type B, with one zero used $p-1=2$ times, factor is $S(2) \cdot \prod_{z \neq z_0} S(0) = (p-1) \cdot (p-1)^{K-1} = (p-1)^K \equiv 1 \pmod 3$.

So factor is 1. But the value is not matching.

Wait, let me recalculate Type A for $(1,2)$. The monomial is $B_{1,2} B_{2,2} B_{2,2}$. Sum over $B$ of this is $A_{1,2} \cdot A_{2,2} \cdot A_{2,2} \cdot \prod_z S(0) = 1 \cdot 2 \cdot 2 \cdot 1 = 4 \equiv 1$. But sample has 2.

Maybe I need to sum over all paths, not just one. The path $1\to2\to2\to2$ is the only one. But perhaps there are more. What about $1\to2$ then what? Only $2\to2$ is possible. So only one path.

Let me list all $B$ for sample 1 and compute $B^3 \pmod 3$.
$A = \begin{pmatrix} 0 & 1 \\ 0 & 2 \end{pmatrix}$. Zeros at $(1,1)$ and $(2,1)$. So $B = \begin{pmatrix} x & 1 \\ y & 2 \end{pmatrix}$ with $x,y \in \{1,2\}$.

$B^2 = \begin{pmatrix} x & 1 \\ y & 2 \end{pmatrix} \begin{pmatrix} x & 1 \\ y & 2 \end{pmatrix} = \begin{pmatrix} x^2 + y & x + 2 \\ xy + 2y & y + 4 \end{pmatrix} = \begin{pmatrix} x^2+y & x+2 \\ y(x+2) & y+4 \end{pmatrix}$.

$B^3 = B^2 \cdot B = \begin{pmatrix} x^2+y & x+2 \\ y(x+2) & y+4 \end{pmatrix} \begin{pmatrix} x & 1 \\ y & 2 \end{pmatrix}$.

Compute $(1,1)$: $(x^2+y)x + (x+2)y = x^3 + xy + xy + 2y = x^3 + 2xy + 2y$.
$(1,2)$: $(x^2+y)\cdot 1 + (x+2)\cdot 2 = x^2+y + 2x+4 = x^2+2x+y+4$.
$(2,1)$: $y(x+2)x + (y+4)y = xy(x+2) + y^2+4y = x^2y+2xy + y^2+4y$.
$(2,2)$: $y(x+2)\cdot 1 + (y+4)\cdot 2 = yx+2y + 2y+8 = xy + 4y + 8$.

Now sum over $x,y \in \{1,2\}$.

For $(1,1)$: $x^3 + 2xy + 2y$.
$x=1,y=1$: $1 + 2 + 2 = 5 \equiv 2$.
$x=1,y=2$: $1 + 4 + 4 = 9 \equiv 0$.
$x=2,y=1$: $8 + 4 + 2 = 14 \equiv 2$.
$x=2,y=2$: $8 + 8 + 4 = 20 \equiv 2$.
Sum: $2+0+2+2 = 6 \equiv 0 \pmod 3$. Good.

For $(1,2)$: $x^2+2x+y+4$.
$x=1,y=1$: $1+2+1+4=8 \equiv 2$.
$x=1,y=2$: $1+2+2+4=9 \equiv 0$.
$x=2,y=1$: $4+4+1+4=13 \equiv 1$.
$x=2,y=2$: $4+4+2+4=14 \equiv 2$.
Sum: $2+0+1+2=5 \equiv 2$. Good.

For $(2,1)$: $x^2y+2xy+y^2+4y$.
$x=1,y=1$: $1+2+1+4=8 \equiv 2$.
$x=1,y=2$: $2+4+4+8=18 \equiv 0$.
$x=2,y=1$: $4+4+1+4=13 \equiv 1$.
$x=2,y=2$: $8+8+4+8=28 \equiv 1$.
Sum: $2+0+1+1=4 \equiv 1$. Good.

For $(2,2)$: $xy+4y+8$.
$x=1,y=1$: $1+4+8=13 \equiv 1$.
$x=1,y=2$: $2+8+8=18 \equiv 0$.
$x=2,y=1$: $2+4+8=14 \equiv 2$.
$x=2,y=2$: $4+8+8=20 \equiv 2$.
Sum: $1+0+2+2=5 \equiv 2$. Good.

Now, my calculation gave for $(1,2)$: Type A (path $1\to2\to2\to2$) value 1, plus Type B: none. Total 1. But actual is 2. So I'm missing something.

Let's expand $B^3$ symbolically. $B = A + E$ where $E_{11}=x, E_{21}=y$, others 0. $B^3 = A^3 + A^2 E + A E A + E A^2 + A E^2 + E A E + E^2 A + E^3$.

We sum over $x,y$. Note that $E$ is a matrix with only two nonzero entries: $E_{11}=x, E_{21}=y$. So $E^2$: $(E^2)_{ij} = \sum_k E_{ik}E_{kj}$. $E$ has nonzero only at $(1,1)$ and $(2,1)$. So $E_{ik}$ is nonzero only for $(i,k)=(1,1)$ or $(2,1)$. $E_{kj}$ nonzero for $(k,j)=(1,1)$ or $(2,1)$. So for $E^2_{ij}$, need $E_{ik}$ and $E_{kj}$ nonzero. $k$ must be 1. Then $E_{i1}$ nonzero means $i=1$ or $i=2$. $E_{1j}$ nonzero means $j=1$. So $E^2$ has nonzero only at $(1,1)$: $E^2_{11} = E_{11}E_{11} = x^2$. And $(2,1)$: $E^2_{21} = E_{21}E_{11} = yx$. So $E^2 = \begin{pmatrix} x^2 & 0 \\ xy & 0 \end{pmatrix}$.

$E^3 = E^2 E = \begin{pmatrix} x^2 & 0 \\ xy & 0 \end{pmatrix} \begin{pmatrix} x & 0 \\ y & 0 \end{pmatrix} = \begin{pmatrix} x^3 & 0 \\ x^2 y & 0 \end{pmatrix}$. Wait, $E = \begin{pmatrix} x & 0 \\ y & 0 \end{pmatrix}$. Yes.

Now $A = \begin{pmatrix} 0 & 1 \\ 0 & 2 \end{pmatrix}$.

Compute each term in the sum $\sum_{x,y} B^3$.

But perhaps it's easier to note that my monomial expansion was for a specific path. The sum over $B$ of $B^3_{ij}$ is $\sum_{paths P} \sum_B m_P$. I claimed that only paths where each zero appears 0 or $p-1=2$ times survive. For $(1,2)$ entry, paths from 1 to 2 of length 3. Let's list all paths (sequences of vertices $v_0=1, v_1, v_2, v_3=2$):
- $1,1,1,2$: edges $(1,1), (1,1), (1,2)$. Zeros: $(1,1)$ appears twice. Nonzero: $(1,2)$ once. This is the Type B path I found! $i=1,j=2$. Here $z_0=(1,1)$ is used twice. But earlier I said for $z_0=(1,1)$, $r=c=1$, no path. But here it is! $e=(1,2)$. Let's check the conditions: $v_0=1, v_1=1, v_2=1, v_3=2$. Steps: 1: $(1,1)$, 2: $(1,1)$, 3: $(1,2)$. So $k=3$ (the $e$-step is step 3). 
But earlier for $p=3$, I had $k=2$ as the only possibility for $c \neq r$. For $r=c=1$, I had $k=2$ and got contradiction. But here $k=3$. 
For $r=c$, the path is: $v_0, \ldots, v_p$. Steps $t \neq k$ are $z_0=(r,r)$, step $k$ is $e$. 
If $k=3$, steps 1,2 are $z_0$, step 3 is $e$. 
Step 1: $v_0=r, v_1=r$. $v_0=1=r$, good. $v_1=1=r$.
Step 2: $v_1=r, v_2=r$. $v_2=1=r$.
Step 3: $v_2=u, v_3=v$. $v_2=1$, so $u=1$. $v_3=2$, so $v=2$. $e=(1,2)$. Good! 
But earlier I said for $t > k$ with $p-k \ge 2$, contradiction. Here $k=3, p=3$, so $p-k=0$, no steps after $k$. And for $t < k$, $k-1=2 \ge 2$, but since $r=c$, the step 2 is $v_1=r, v_2=r$, which is fine because $v_1=c=r$ and we need $v_1=r$, which is true. So my earlier analysis for $r=c$ was wrong when $k=p$. Let's re-analyze for $r=c$.

For $r=c$ and general $k$:
- For $t < k$: $v_{t-1}=r, v_t=r$. This is consistent as long as $v_0=r$. Then $v_1=r, v_2=r, \ldots, v_{k-1}=r$.
- For $t > k$: $v_{t-1}=r, v_t=r$. Consistent as long as $v_k=r$.
- Step $k$: $v_{k-1}=u, v_k=v$. But from above, $v_{k-1}=r$ and $v_k=r$. So $u=v=r$. Thus $e=(r,r)$. 

But in our example, $e=(1,2)$, not $(1,1)$. Contradiction! Let's check the path: $1,1,1,2$. Edges: $(1,1), (1,1), (1,2)$. The third edge is $(1,2)$, so $v_2=1, v_3=2$. For this to be a $z_0$-step? No, step 3 is $e=(1,2)$. $v_2=1=u$, $v_3=2=v$. Good. Now for the $z_0$-steps: steps 1 and 2. Step 1: $(v_0,v_1)=(1,1)$, which is $z_0=(1,1)$, so $v_0=1=r, v_1=1=c=r$. Step 2: $(v_1,v_2)=(1,1)$, which is $z_0$, so $v_1=1=r, v_2=1=c=r$. But $v_2=1$, good. Now, for step 2 to be $z_0$, we need $v_1=r$ and $v_2=c$. Here $r=c=1$, so $v_1=1=r$ and $v_2=1=c$. Good. But then $v_2=1$. For step 3 to be $e$, we need $v_2=u$ and $v_3=v$. Here $v_2=1$, so $u=1$. $v_3=2$, so $v=2$. $e=(1,2)$. Good.

But earlier I said for $t > k$, $v_k=r$. Here $k=3$, so no $t>k$. For $t<k$, $v_{k-1}=r$. Here $k=3$, $v_2=r=1$. Yes. And the step $k$: $v_{k-1}=v_2=1=u$, $v_k=v_3=2=v$. But I also said $v_{k-1}=r$ from the $z_0$ sequence. Here $r=1$, and $v_2=1$, so $u=r=1$, good. And $v_k=v_3=2$. But I claimed $v_k=r$ from the $z_0$ sequence for $t>k$, but there are no $t>k$. However, for the consistency of the path, $v_k$ is determined by the $e$-step. The condition $v_k=r$ only comes from step $k+1$ being $z_0$. Since $k=p$, there is no step $k+1$. So $v_k$ does not need to be $r$! 

Ah! So for $k=p$, the condition $v_k=r$ is not required because there's no next step. Similarly, for $k=1$, $v_0$ is not required to be $r$ from the left? Let's see: for $t < k$, i.e., $t<1$, none, so $v_0$ is free? But step 1 is $z_0$, which requires $v_0=r$. So $v_0=r$ is required. For $k=p$, the last step is $e$, so $v_{p-1}$ is determined by the $e$-step: $v_{p-1}=u$. And from the $z_0$ steps $t=p$, none, so $v_p$ is free? But the path ends at $v_p=j$, which is given. So for $k=p$:
- Steps $1$ to $p-1$ are $z_0$: requires $v_0=r$, and $v_1=r, \ldots, v_{p-1}=r$ (since $r=c$, the steps keep us at $r$).
- Step $p$ is $e$: $v_{p-1}=u, v_p=v$.
From $z_0$ steps, $v_{p-1}=r$. So $u=r$.
And $v_p=j=v$.
So the path is: $v_0=r, v_1=r, \ldots, v_{p-1}=r, v_p=v$.
Thus $i=v_0=r$, and $j=v_p=v$.
And $e=(r, v)$ where $v$ is such that $A_{r,v} \neq 0$.
This is a valid path! For sample 1: $z_0=(1,1)$, $r=1$. Then $i=1$, $j=v$ where $e=(1,j)$ is a nonzero position. $A_{1,2}=1 \neq 0$, so $e=(1,2)$, $j=2$. The path is $1,1,1,2$ with edges $(1,1),(1,1),(1,2)$. Yes! 

Similarly for $k=1$:
- Step 1 is $e$: $v_0=i=u, v_1=v$.
- Steps 2 to $p$ are $z_0$: requires $v_1=r$, so $v=r$. And $v_2=r, \ldots, v_p=r$ (since $r=c$).
So $i=u$, $j=v_p=r$. And $e=(u,r)$ with $A_{u,r} \neq 0$.

For $k$ in between (and $r=c$), the $z_0$ steps on both sides force $v_{k-1}=r$ and $v_k=r$, so $u=v=r$, but $e=(r,r)$ is a zero, contradiction. So only $k=1$ and $k=p$ work for $r=c$.

For $r \neq c$, we had $k \in \{1,2\}$ and $k \ge p-1$. For $p=3$, $k=2$ or $k=1,3$? $k \ge 2$ and $k \le 2$, so $k=2$. But we also have the $k=3$ case from above? No, for $r \neq c$, the $z_0$ steps cannot be adjacent. For $k=3$ in $p=3$, steps 1,2 are $z_0$, which are adjacent, so $r=c$ required. So for $r \neq c$, $k=2$ is the only case.

So the surviving paths are:
For each zero $z_0=(r,c)$:
- If $r \neq c$ and $p=3$: the path with $k=2$, giving $i=r, j=c, e=(c,r)$.
- If $r = c$ and $p=3$: paths with $k=1$ and $k=p=3$.
  - $k=1$: $i=u, j=r$, with $e=(u,r)$ nonzero, so $A_{u,r} \neq 0$.
  - $k=3$: $i=r, j=v$, with $e=(r,v)$ nonzero, so $A_{r,v} \neq 0$.

Plus the Type A paths (all nonzero).

For sample 1: zeros at $(1,1)$ and $(2,1)$.
$z_0=(1,1)$: $r=c=1$. $k=1$: $e=(u,1)$ with $A_{u,1} \neq 0$. But $A_{11}=0$, $A_{21}=0$. So no such $e$. $k=3$: $e=(1,v)$ with $A_{1,v} \neq 0$. $A_{12}=1 \neq 0$, so $e=(1,2)$, $i=1, j=2$. One path.
$z_0=(2,1)$: $r=2,c=1 \neq r$. $k=2$: $e=(1,2)$ with $A_{1,2} \neq 0$, yes. $i=2, j=1$. One path.

Type A: as before, path $1\to2\to2\to2$ for $(1,2)$, and $2\to2\to2\to2$ for $(2,2)$.

Now contributions:
- $(1,1)$: Type A: none. Type B: from $z_0=(1,1)$ $k=1$: need $j=1$, but $j=r=1$, and $e=(u,1)$, but no such $e$. $k=3$: $j=v=1$? But $A_{1,1}=0$. From $z_0=(2,1)$: $i=2,j=1$, not $(1,1)$. So total 0.
- $(1,2)$: Type A: 1. Type B: from $z_0=(1,1)$ $k=3$: $i=1,j=2$, $e=(1,2)$, value $A_{1,2}=1$. From $z_0=(2,1)$: $i=2,j=1$, not $(1,2)$. So Type B gives 1. Total $1+1=2$. Good!
- $(2,1)$: Type A: 0. Type B: from $z_0=(1,1)$: $k=1$ gives $j=1$, not 1. $k=3$ gives $i=1$, not 2. From $z_0=(2,1)$: $i=2,j=1$, $e=(1,2)=1$. Value 1. Total 1.
- $(2,2)$: Type A: $2 \equiv -1 \pmod 3$? $2^3=8 \equiv 2$. So 2. Type B: from $z_0=(1,1)$: $k=1$ gives $i=u, j=1$, not 2. $k=3$ gives $i=1$, not 2. From $z_0=(2,1)$: $i=2,j=1$, not 2. So 0. Total 2.

With factor $(-1)^K = 1$, this matches! 

So the algorithm is clear: compute the sum as $(-1)^K \times (\text{Type A} + \text{Type B}) \pmod p$.

Type A: sum over all paths of length $p$ using only nonzero positions, of the product of $A$ values. This is $(M^p)$ where $M_{ij} = A_{ij}$ if $A_{ij} \neq 0$ and 0 otherwise. Wait, but we need the product, and if the path uses a position where $A=0$, the product is 0, which is automatically excluded. So yes, it's $(M^p)_{ij}$ with $M$ being $A$ with zeros kept as zero.

Type B: for each zero $z_0=(r,c)$:
- If $r \neq c$: only possible for $p=3$ (and $p=2$). For general $p$, the condition $k \ge p-1$ and $k \le 2$ (from non-adjacency) gives $p-1 \le 2$, so $p \le 3$. For $p=2$, $p-1=1$, and $k$ can be 1 or 2. For $p=3$, $k=2$. For $p>3$, no contribution from $r \neq c$.
- If $r = c$ (diagonal zero): $z_0=(d,d)$. Then paths with $k=1$ and $k=p$ survive (for $p \ge 2$). 
  - $k=1$: path $u, d, d, \ldots, d$ with $u$ free? Let's derive: step 1 is $e=(u,d)$, steps 2..p are $z_0=(d,d)$. So $v_0=u, v_1=d, v_2=d, \ldots, v_p=d$. The path ends at $j=d$. So $i=u, j=d$. The edge $e=(u,d)$ must be nonzero, so $A_{u,d} \neq 0$. The product is $A_{u,d} \cdot 1^{p-1} = A_{u,d}$ (since $A_{d,d}=0$ but we don't use it as a value; the $z_0$ positions are free variables, but in the product we have $A$ for nonzero and the variable for zero. But wait! In the monomial, the $z_0$ positions are variables $x$, and we sum over $x \in \mathbb{F}_p^*$. The value of the monomial is $x^{p-1} \cdot A_{u,d}$. The sum is $S(p-1) \cdot S(0)^{K-1} = (p-1)^K$. Mod $p$, this is $(-1)^K$. So the contribution is $(-1)^K \cdot A_{u,d}$ for each $u$ with $A_{u,d} \neq 0$. And it contributes to $(i,j) = (u, d)$.
  - $k=p$: similarly, $i=d, j=v$ with $e=(d,v)$ nonzero, $A_{d,v} \neq 0$. Contributes to $(d,v)$.

So for diagonal zero $z_0=(d,d)$, the Type B contribution to the sum matrix $S$ is: add $(-1)^K \cdot A_{u,d}$ to $S_{u,d}$ for all $u$ with $A_{u,d} \neq 0$, and add $(-1)^K \cdot A_{d,v}$ to $S_{d,v}$ for all $v$ with $A_{d,v} \neq 0$.

For off-diagonal zero $z_0=(r,c)$ with $r \neq c$, only for $p=3$ (and $p=2$): 
- $p=3$: $k=2$, path $r, c, r, c$? Let's see: $v_0=r, v_1=c, v_2=r, v_3=c$. Steps: $(r,c), (c,r), (r,c)$. $z_0=(r,c)$ used twice, $e=(c,r)$ used once. So $e$ must be $(c,r)$, requiring $A_{c,r} \neq 0$. Contributes to $(i,j)=(r,c)$ with value $(-1)^K \cdot A_{c,r}$.
- $p=2$: $p-1=1$. $k \in \{1,2\}$.
  - $k=1$: step 1 is $e=(u,v)$, step 2 is $z_0=(r,c)$. So $v_0=u, v_1=v, v_2=c$. And step 2 requires $v_1=r$ and $v_2=c$. So $v=r$, $u$ is free? $v_0=i=u$. So $i=u, j=c$. $e=(u,r)$ must be nonzero. And the path has $i=u, j=c$. For $p=2$, $B^2_{ij}$ is the sum of paths of length 2. This might need separate handling, but for $p=2$ it's easy to brute force or note that $B^2$ is just computed.
  Actually for $p=2$, we can compute directly since the sum is small? But $p$ can be up to $10^9$, so we need the general formula. But for $p=2$, the condition $(p-1)|d$ is always true since $p-1=1$, so every monomial survives! The sum is $\sum_B B^2 = (p-1)^K \sum_B \prod ... $? Actually for $p=2$, $S(d) = \sum_{x \in \{1\}} x^d = 1$ for all $d \ge 0$ (with $0^0=1$). So the sum over $B$ of a monomial is simply the product of $A$ values for the nonzero positions (since the zero positions are fixed to 1). So the sum is $\sum_{B} B^2 = (A')^2$ where $A'$ is $A$ with zeros replaced by 1. And $(p-1)^K = 1^K = 1$. So the answer is $(A')^2 \pmod 2$. But the formula above with $(-1)^K$ etc. should also work. For $p=2$, the Type A and Type B are all merged. But the general expression $(-1)^K \cdot ( \text{Type A} + \text{Type B} )$ might need adjustment for $p=2$. However, the sample 2 has $p=2$ and it worked out to all ones. Let's check: $A=I$ with zeros elsewhere. $A' = J$ (all ones). $J^2 = 3J \equiv J \pmod 2$. So all ones. The formula: Type A is $(M^2)$ with $M$ having ones on diagonal. $M=I$, $M^2=I$. Type B for off-diagonal zero $(r,c)$: $k=1$ gives $i=u, j=c$ with $e=(u,r)$. Here $r \neq c$. $A_{u,r}$ is 1 if $u=r$, 0 otherwise. So contributes to $(r,c)$: $A_{r,r} \cdot (-1)^K$? $K=6$ (zeros at off-diagonal). $(-1)^6=1$. So $S_{r,c}$ gets $1$ from this. Similarly $k=2$: $i=r, j=v$ with $e=(r,v)$, $A_{r,v}=1$ if $v=r$, so contributes to $(r,r)$: 1. So total $S_{r,r} = 1$ (Type A) + 1 (Type B $k=2$ for some $z_0$? Wait, for a fixed $z_0=(r,c)$, it contributes to $(r,r)$ via $k=2$ with $v=r$, but $e=(r,r)$ is diagonal, which is not a zero. But for $p=2$, the formula is different. Anyway, for $p=2$ we can just compute directly, or use the fact that the sum is just $A'^2$ with $A'$ having ones at zero positions. But note: in sample 2, the answer is all ones, and $A'^2$ where $A'$ is all ones gives all $N \pmod 2 = 1$ (since $N=3$). So yes.

To unify: the sum is $(-1)^K \cdot ( \text{sum over } (i,j) \text{ as described} )$, but for $p=2$, $(-1)^K = 1$ and the formula might still hold if we consider all monomials. Actually, for $p=2$, every monomial has degree 2, and each zero appears 0 or 1 times. The condition $(p-1)|d$ is $1|d$, always true. So the factor is $(p-1)^K = 1$ for each zero. The sum is exactly the sum over all paths of the product, which is $(A')^2$ with $A'$ having ones at zeros. And $(A')^2$ can be computed. The formula $(-1)^K (M^p + \text{Type B})$ might be off by a factor of $(p-1)^K$ vs $(-1)^K$, but since $p=2$, $(p-1)^K = 1 = (-1)^K$, so it's fine. And for $p>2$, the surviving monomials are exactly the Type A and Type B described, and the factor is $(p-1)^K \equiv (-1)^K \pmod p$. So the general formula is:

Let $K$ be the number of zeros.
Let $M$ be the matrix with $M_{ij} = A_{ij}$ if $A_{ij} \neq 0$ and $0$ otherwise. Compute $P = M^p \pmod p$ using fast exponentiation.
Let $D$ be the sum of Type B contributions:
- For each zero $(r,c)$:
  - If $r = c$: add to the result matrix $R$: for each $u$ with $A_{u,r} \neq 0$, $R_{u,r} += A_{u,r}$; for each $v$ with $A_{r,v} \neq 0$, $R_{r,v} += A_{r,v}$.
  - If $r \neq c$ and $p=3$: if $A_{c,r} \neq 0$, then $R_{r,c} += A_{c,r}$. (Because the path is $r,c,r,c$ with $e=(c,r)$).
- For $p=2$, the formula is different. Actually, for $p=2$, we can just compute $(A')^2$ where $A'$ is $A$ with zeros replaced by 1. But note that for $p=2$, the sum is over $B$ with zeros replaced by 1 (only one choice), so it's just $(A')^2$. And $A' = M + J$ where $J$ has 1 at zero positions. But $(M+J)^2 = M^2 + MJ + JM + J^2$. This is not simply $M^2 + \text{something}$. So for $p=2$, better to handle separately. Since $p=2$ is small, we can compute $A'$ and square it.

But wait, for $p>2$, the formula $R = (-1)^K \cdot (P + D) \pmod p$ should work.

Let's verify with sample 3: $p=13$, $N=4$. Compute $K$ and check.

Sample 3:
$A = \begin{pmatrix} 0 & 1 & 2 & 0 \\ 3 & 4 & 0 & 5 \\ 0 & 6 & 0 & 7 \\ 8 & 9 & 0 & 0 \end{pmatrix}$.
Zeros: $(1,1), (1,4), (2,3), (3,1), (3,3), (4,3), (4,4)$. $K=7$.
$M$ is $A$ with zeros.
Compute $M^{13} \pmod{13}$.
Type B: 
Zeros:
(1,1): $r=c=1$. Add $A_{u,1}$ for $u$ with $A_{u1}\neq 0$: $A_{21}=3$, $A_{41}=8$. So $R_{2,1} += 3$, $R_{4,1} += 8$. Also add $A_{1,v}$ for $v$ with $A_{1v}\neq 0$: $A_{12}=1, A_{13}=2$. So $R_{1,2} += 1, R_{1,3} += 2$.
(1,4): $r=c=4$? $r=1,c=4 \neq$. So off-diagonal. $p=13 >3$, so no contribution.
(2,3): $r=2,c=3 \neq$. No.
(3,1): $r=3,c=1 \neq$. No.
(3,3): $r=c=3$. Add $A_{u,3}$: $A_{13}=2, A_{23}=0$? $A_{23}=0$, $A_{43}=0$. So only $A_{13}=2$. $R_{1,3} += 2$. Add $A_{3,v}$: $A_{32}=6, A_{34}=7$. $R_{3,2} += 6, R_{3,4} += 7$.
(4,3): $r=4,c=3 \neq$. No.
(4,4): $r=c=4$. Add $A_{u,4}$: $A_{14}=0, A_{24}=5, A_{34}=7$. $R_{2,4} += 5, R_{3,4} += 7$. Add $A_{4,v}$: $A_{41}=8, A_{42}=9$. $R_{4,1} += 8, R_{4,2} += 9$.

So $D$ has:
$R_{2,1} = 3$
$R_{4,1} = 8 + 8 = 16 \equiv 3$
$R_{1,2} = 1$
$R_{1,3} = 2 + 2 = 4$
$R_{3,2} = 6$
$R_{3,4} = 7 + 7 = 14 \equiv 1$
$R_{2,4} = 5$
$R_{4,2} = 9$

Now $P = M^{13} \pmod{13}$.
$M = \begin{pmatrix} 0 & 1 & 2 & 0 \\ 3 & 4 & 0 & 5 \\ 0 & 6 & 0 & 7 \\ 8 & 9 & 0 & 0 \end{pmatrix}$.

This is tedious to compute by hand, but the sample output is:
$\begin{pmatrix} 8 & 0 & 6 & 5 \\ 11 & 1 & 8 & 5 \\ 8 & 0 & 4 & 12 \\ 8 & 0 & 1 & 9 \end{pmatrix}$.

And $(-1)^7 = -1 \equiv 12 \pmod{13}$.
So $12 \cdot (P + D) \equiv \text{output}$.

Compute $D$:
$D = \begin{pmatrix} 0 & 1 & 4 & 0 \\ 3 & 0 & 0 & 5 \\ 0 & 6 & 0 & 1 \\ 3 & 9 & 0 & 0 \end{pmatrix}$.

Now we need $P$. Let's compute $M^2, M^4, M^8, M^{13} = M^8 \cdot M^4 \cdot M$.

$M = \begin{pmatrix} 0 & 1 & 2 & 0 \\ 3 & 4 & 0 & 5 \\ 0 & 6 & 0 & 7 \\ 8 & 9 & 0 & 0 \end{pmatrix}$.

Compute $M^2 \pmod{13}$:
Row1: 
c1: 0*0+1*3+2*0+0*8 = 3
c2: 0*1+1*4+2*6+0*9 = 4+12=16≡3
c3: 0*2+1*0+2*0+0*0 = 0
c4: 0*0+1*5+2*7+0*0 = 5+14=19≡6
Row2:
c1: 3*0+4*3+0*0+5*8 = 12+40=52≡0
c2: 3*1+4*4+0*6+5*9 = 3+16+45=64≡12
c3: 3*2+4*0+0*0+5*0 = 6
c4: 3*0+4*5+0*7+5*0 = 20≡7
Row3:
c1: 0*0+6*3+0*0+7*8 = 18+56=74≡9
c2: 0*1+6*4+0*6+7*9 = 24+63=87≡9
c3: 0*2+6*0+0*0+7*0 = 0
c4: 0*0+6*5+0*7+7*0 = 30≡4
Row4:
c1: 8*0+9*3+0*0+0*8 = 27≡1
c2: 8*1+9*4+0*6+0*9 = 8+36=44≡5
c3: 8*2+9*0+0*0+0*0 = 16≡3
c4: 8*0+9*5+0*7+0*0 = 45≡6

So $M^2 = \begin{pmatrix} 3 & 3 & 0 & 6 \\ 0 & 12 & 6 & 7 \\ 9 & 9 & 0 & 4 \\ 1 & 5 & 3 & 6 \end{pmatrix}$.

Now $M^4 = (M^2)^2$.
Let $B = M^2$.
B = 
3 3 0 6
0 12 6 7
9 9 0 4
1 5 3 6

Compute B^2:
Row1:
c1: 3*3+3*0+0*9+6*1 = 9+0+0+6=15≡2
c2: 3*3+3*12+0*9+6*5 = 9+36+0+30=75≡10
c3: 3*0+3*6+0*0+6*3 = 0+18+0+18=36≡10
c4: 3*6+3*7+0*4+6*6 = 18+21+0+36=75≡10
Row2:
c1: 0*3+12*0+6*9+7*1 = 0+0+54+7=61≡9
c2: 0*3+12*12+6*9+7*5 = 0+144+54+35=233≡12? 13*17=221, 233-221=12. Yes 12.
c3: 0*0+12*6+6*0+7*3 = 0+72+0+21=93≡2 (13*7=91)
c4: 0*6+12*7+6*4+7*6 = 0+84+24+42=150≡7 (13*11=143, 150-143=7)
Row3:
c1: 9*3+9*0+0*9+4*1 = 27+0+0+4=31≡5
c2: 9*3+9*12+0*9+4*5 = 27+108+0+20=155≡12 (13*11=143, 155-143=12)
c3: 9*0+9*6+0*0+4*3 = 0+54+0+12=66≡1
c4: 9*6+9*7+0*4+4*6 = 54+63+0+24=141≡11 (13*10=130, 141-130=11)
Row4:
c1: 1*3+5*0+3*9+6*1 = 3+0+27+6=36≡10
c2: 1*3+5*12+3*9+6*5 = 3+60+27+30=120≡3 (13*9=117)
c3: 1*0+5*6+3*0+6*3 = 0+30+0+18=48≡9
c4: 1*6+5*7+3*4+6*6 = 6+35+12+36=89≡11 (13*6=78, 89-78=11)

So $M^4 = \begin{pmatrix} 2 & 10 & 10 & 10 \\ 9 & 12 & 2 & 7 \\ 5 & 12 & 1 & 11 \\ 10 & 3 & 9 & 11 \end{pmatrix}$.

Now $M^8 = (M^4)^2$.
Let C = M^4.
C = 
2 10 10 10
9 12 2 7
5 12 1 11
10 3 9 11

Compute C^2:
Row1:
c1: 2*2+10*9+10*5+10*10 = 4+90+50+100=244≡10 (13*18=234, 244-234=10)
c2: 2*10+10*12+10*12+10*3 = 20+120+120+30=290≡4 (13*22=286)
c3: 2*10+10*2+10*1+10*9 = 20+20+10+90=140≡10 (13*10=130)
c4: 2*10+10*7+10*11+10*11 = 20+70+110+110=310≡11 (13*23=299, 310-299=11)
Row2:
c1: 9*2+12*9+2*5+7*10 = 18+108+10+70=206≡11 (13*15=195)
c2: 9*10+12*12+2*12+7*3 = 90+144+24+21=279≡6 (13*21=273)
c3: 9*10+12*2+2*1+7*9 = 90+24+2+63=179≡10 (13*13=169, 179-169=10)
c4: 9*10+12*7+2*11+7*11 = 90+84+22+77=273≡0
Row3:
c1: 5*2+12*9+1*5+11*10 = 10+108+5+110=233≡12 (13*17=221)
c2: 5*10+12*12+1*12+11*3 = 50+144+12+33=239≡5 (13*18=234)
c3: 5*10+12*2+1*1+11*9 = 50+24+1+99=174≡5 (13*13=169)
c4: 5*10+12*7+1*11+11*11 = 50+84+11+121=266≡6 (13*20=260)
Row4:
c1: 10*2+3*9+9*5+11*10 = 20+27+45+110=202≡7 (13*15=195)
c2: 10*10+3*12+9*12+11*3 = 100+36+108+33=277≡4 (13*21=273)
c3: 10*10+3*2+9*1+11*9 = 100+6+9+99=214≡6 (13*16=208)
c4: 10*10+3*7+9*11+11*11 = 100+21+99+121=341≡3 (13*26=338)

So $M^8 = \begin{pmatrix} 10 & 4 & 10 & 11 \\ 11 & 6 & 10 & 0 \\ 12 & 5 & 5 & 6 \\ 7 & 4 & 6 & 3 \end{pmatrix}$.

Now $M^{13} = M^8 \cdot M^4 \cdot M$.
First $M^8 \cdot M^4$:
M8 = 
10 4 10 11
11 6 10 0
12 5 5 6
7 4 6 3
M4 = 
2 10 10 10
9 12 2 7
5 12 1 11
10 3 9 11

Compute product P1 = M8 * M4:
Row1:
c1: 10*2+4*9+10*5+11*10 = 20+36+50+110=216≡8 (13*16=208)
c2: 10*10+4*12+10*12+11*3 = 100+48+120+33=301≡2 (13*23=299)
c3: 10*10+4*2+10*1+11*9 = 100+8+10+99=217≡9 (13*16=208)
c4: 10*10+4*7+10*11+11*11 = 100+28+110+121=359≡8 (13*27=351)
Row2:
c1: 11*2+6*9+10*5+0*10 = 22+54+50=126≡9 (13*9=117)
c2: 11*10+6*12+10*12+0*3 = 110+72+120=302≡3 (13*23=299)
c3: 11*10+6*2+10*1+0*9 = 110+12+10=132≡2 (13*10=130)
c4: 11*10+6*7+10*11+0*11 = 110+42+110=262≡2 (13*20=260)
Row3:
c1: 12*2+5*9+5*5+6*10 = 24+45+25+60=154≡11 (13*11=143)
c2: 12*10+5*12+5*12+6*3 = 120+60+60+18=258≡11 (13*19=247, 258-247=11)
c3: 12*10+5*2+5*1+6*9 = 120+10+5+54=189≡7 (13*14=182)
c4: 12*10+5*7+5*11+6*11 = 120+35+55+66=276≡3 (13*21=273)
Row4:
c1: 7*2+4*9+6*5+3*10 = 14+36+30+30=110≡6 (13*8=104)
c2: 7*10+4*12+6*12+3*3 = 70+48+72+9=199≡4 (13*15=195)
c3: 7*10+4*2+6*1+3*9 = 70+8+6+27=111≡7 (13*8=104)
c4: 7*10+4*7+6*11+3*11 = 70+28+66+33=197≡2 (13*15=195)

So P1 = 
8 2 9 8
9 3 2 2
11 11 7 3
6 4 7 2

Now multiply by M:
M = 
0 1 2 0
3 4 0 5
0 6 0 7
8 9 0 0

P = P1 * M:
Row1:
c1: 8*0+2*3+9*0+8*8 = 0+6+0+64=70≡5 (13*5=65)
c2: 8*1+2*4+9*6+8*9 = 8+8+54+72=142≡12 (13*10=130)
c3: 8*2+2*0+9*0+8*0 = 16≡3
c4: 8*0+2*5+9*7+8*0 = 0+10+63=73≡8 (13*5=65)
Row2:
c1: 9*0+3*3+2*0+2*8 = 0+9+0+16=25≡12
c2: 9*1+3*4+2*6+2*9 = 9+12+12+18=51≡12 (13*3=39)
c3: 9*2+3*0+2*0+2*0 = 18≡5
c4: 9*0+3*5+2*7+2*0 = 0+15+14=29≡3
Row3:
c1: 11*0+11*3+7*0+3*8 = 0+33+0+24=57≡5 (13*4=52)
c2: 11*1+11*4+7*6+3*9 = 11+44+42+27=124≡7 (13*9=117)
c3: 11*2+11*0+7*0+3*0 = 22≡9
c4: 11*0+11*5+7*7+3*0 = 0+55+49=104≡0
Row4:
c1: 6*0+4*3+7*0+2*8 = 0+12+0+16=28≡2
c2: 6*1+4*4+7*6+2*9 = 6+16+42+18=82≡4 (13*6=78)
c3: 6*2+4*0+7*0+2*0 = 12≡12
c4: 6*0+4*5+7*7+2*0 = 0+20+49=69≡4 (13*5=65)

So P = 
5 12 3 8
12 12 5 3
5 7 9 0
2 4 12 4

Now D = 
0 1 4 0
3 0 0 5
0 6 0 1
3 9 0 0

P + D = 
5 0 7 8
15≡2 12 5 8
5 13≡0 9 1
5 13≡0 12 4

= 
5 0 7 8
2 12 5 8
5 0 9 1
5 0 12 4

Now multiply by $(-1)^K = -1 \equiv 12 \pmod{13}$:
12 * (5,0,7,8) = (60,0,84,96) ≡ (8,0,6,5) since 60=13*4+8, 84=13*6+6, 96=13*7+5.
12 * (2,12,5,8) = (24,144,60,96) ≡ (11,1,8,5) since 24=13+11, 144=13*11+1, 60=8, 96=5.
12 * (5,0,9,1) = (60,0,108,12) ≡ (8,0,4,12) since 108=13*8+4.
12 * (5,0,12,4) = (60,0,144,48) ≡ (8,0,1,9) since 144=1, 48=9.

This matches the sample output! Great.

So the algorithm is:
1. Read N, p, and matrix A.
2. Count K = number of zeros in A.
3. Construct matrix M: M[i][j] = A[i][j] if A[i][j] != 0 else 0.
4. Compute P = M^p mod p using fast matrix exponentiation (O(N^3 log p)).
5. Compute D matrix (initialized to 0):
   For each zero position (r,c) in A (1-indexed):
     if r == c:
       for u in 1..N:
         if A[u][r] != 0: D[u][r] = (D[u][r] + A[u][r]) % p
       for v in 1..N:
         if A[r][v] != 0: D[r][v] = (D[r][v] + A[r][v]) % p
     else if p == 3:
       if A[c][r] != 0: D[r][c] = (D[r][c] + A[c][r]) % p
     (For p=2, handle separately? Or the general formula might need adjustment. Let's check p=2.)
6. Compute sign = 1 if K is even else -1. Mod p, sign = 1 if K%2==0 else p-1.
7. Result = sign * (P + D) mod p.
8. Output Result.

Now for p=2: 
- p=2, then p-1=1. The condition for survival is that each zero appears 0 or 1 times (since 1 divides everything). Actually, for p=2, the sum over x in F_p^* of x^d is 1 for all d>=0. So every monomial contributes 1. The sum is simply the sum over all B of the monomial, which is the product of A values for the fixed (nonzero) positions, and 1 for the zero positions (since they are fixed to 1). So the total sum is exactly the (i,j) entry of (A')^2 where A' is A with zeros replaced by 1. 
But the formula with (-1)^K (P + D) might not work for p=2. Let's test with sample 2: p=2, A is identity with zeros elsewhere. K=6. (-1)^6=1. 
M is A with zeros: M=I. P = I^2 = I.
D: for zero (r,c) with r!=c: since p=2, not 3, so no D from off-diagonal. For r=c: but there are no diagonal zeros in sample 2 (diagonal is 1). So D=0.
Result = I. But sample output is all ones. So the formula gives I (identity), which has 1 on diagonal and 0 elsewhere. But sample output is all 1s. So the formula is wrong for p=2.

We need to handle p=2 separately. For p=2, the answer is (A')^2 mod 2, where A' has 1 at zero positions. But note that A' is exactly M + Z, where Z is the matrix with 1 at zero positions. And (M+Z)^2 = M^2 + MZ + ZM + Z^2. This is not simply M^2. So for p=2, we should compute A' = A with zeros replaced by 1, then compute (A')^2 mod 2.

But wait, in sample 2, A is identity, so A' is all ones. (A')^2 = N * J ≡ J mod 2 (since N=3 is odd). So all ones. Correct.

For p>2, the formula works. For p=2, compute directly.

Edge case: p=2, and we need to compute matrix power. p is prime, 1 <= p <= 1e9, so p=2 is small enough that we can compute (A')^2 directly, but A' has entries 0 or 1, and we need to do it mod 2. Since N <= 100, it's fine.

Now, what about p=1? But p is prime, so p>=2. So only p=2 needs special handling.

Thus the algorithm:
- If p == 2:
  - Construct A' where A'[i][j] = 1 if A[i][j] == 0 else A[i][j] (which is 1 since A[i][j] in {0,1} for p=2).
  - Compute (A')^2 mod 2.
- Else:
  - Construct M, compute P = M^p mod p.
  - Compute D as above.
  - sign = (-1)^K mod p = 1 if K even else p-1.
  - Result = sign * (P + D) mod p.
  - Ensure positive mod p.

Now, we need to implement matrix multiplication mod p for N up to 100. p up to 1e9, so multiplication of two numbers up to p-1 can be up to ~1e18, which fits in 64-bit (Python int is arbitrary precision, so fine). The complexity is O(N^3 log p) = 100^3 * 30 = 3e7, which is acceptable in Python with some optimization? 3e7 operations might be slow in pure Python. We need to be careful. 100^3 = 1,000,000. log2(1e9) ~ 30. So 30 million multiplications. In Python, this is about 0.3 seconds per million? Actually, Python is slower, maybe 10-20 million operations per second? 30 million might take a few seconds, but might be okay for 2 seconds limit? We need to optimize.

We can use numpy? But we are to write pure Python probably. The problem says N up to 100, p up to 1e9. We can use list of lists and do matrix multiplication with loops. Or we can use the fact that for p large, but we can't avoid O(N^3). 

Maybe we can optimize by using the fact that M is sparse? But not necessarily. However, the number of zeros K can be large, so M might be sparse. But in the worst case, M is dense. So we need a general solution.

In Python, we can write the matrix multiplication with a triple loop, and use local variables. 30 million iterations of the innermost loop is about 30 million * (a few operations). It might be borderline but probably okay for 2 seconds? Let's estimate: each iteration: 2 multiplications, 2 additions, 2 array accesses, mod. Maybe 5-10 operations. So 300 million operations. Python does about 20-30 million simple operations per second. So maybe 10-15 seconds. Too slow.

We need to optimize. Perhaps we can use the built-in `pow` with matrix exponentiation using exponentiation by squaring, but the inner loop is still O(N^3). 

Alternative: use the fact that we only need M^p, and p can be up to 1e9. We can use repeated squaring. Each multiplication is O(N^3). 

We can try to use `numba`? Not allowed. Use `pypy`? The problem might expect PyPy. With PyPy, 30 million might be okay.

Or we can use the fact that N is only 100, and we can use a faster matrix multiplication algorithm? No.

Maybe we can note that for the sum, we don't need the full M^p. We have the expression $(-1)^K (M^p + D)$. But D is a simple sum. So we need M^p.

We can compute M^p mod p using the fact that we are working mod p, and p is prime. But that doesn't help with the matrix multiplication.

Another thought: the sum is $(-1)^K$ times something. But is there a simpler expression? The result is essentially the sum over B of B^p. Could it be that the result is simply $(-1)^K (A^p)$? No, because of the D term.

Wait, from the derivation, the sum is exactly $(-1)^K$ times the sum over certain monomials. But maybe the sum can be written as $(-1)^K$ times $A^p$ with some correction? Not really.

Given the time, perhaps we can accept the O(N^3 log p) solution and hope it's fast enough in PyPy. Or we can try to use the `array` module or `numpy` if allowed. The problem says "write a python program", and "read from stdin", so we can use any Python features. Using numpy would be easy but might not be allowed in some judges. However, the prompt says "Enclose your code within delimiters", and doesn't specify no numpy. But competitive programming judges often have numpy. Let's see: N=100, matrices of size 100x100. numpy dot product is fast. We can use numpy.

But if we use numpy, we need to handle mod p, and the matrices are small. However, p can be up to 1e9, so int64 is fine. numpy can do matrix multiplication efficiently. But repeated squaring requires many multiplications. We can do `np.dot(A, B) % p` each time. This will be much faster.

But we need to be careful: numpy's default int is int64, which can hold up to 9e18, and p^2 is up to 1e18, so safe. And mod p each time.

So I'll write the solution with numpy for the matrix exponentiation, and pure Python for the D part (which is O(N^2)). If numpy is not available, we fallback to pure Python with optimizations.

But to be safe, I can write a pure Python version with some optimizations: use list comprehensions, local variables, and maybe `map` for inner products? But the inner product is the bottleneck.

Actually, we can use the fact that we are multiplying mod p, and we can reduce mod p at the end of each row? Not much.

Given the time, I'll write the numpy version, and if numpy is not available, the judge might have it. Many judges now have numpy.

Let's outline the code:
```python
import sys
import numpy as np

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = []
    for _ in range(N):
        A.append(list(map(int, input().split())))
    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)
    if p == 2:
        A2 = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        # compute A2^2 mod 2
        # can use numpy or loops
        M = np.array(A2, dtype=np.int64)
        P = np.dot(M, M) % 2
        for row in P:
            print(' '.join(map(str, row)))
        return
    M = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] != 0:
                M[i][j] = A[i][j]
    M_np = np.array(M, dtype=np.int64)
    # compute M^p mod p
    P = np.eye(N, dtype=np.int64)
    base = M_np
    exp = p
    while exp > 0:
        if exp & 1:
            P = np.dot(P, base) % p
        base = np.dot(base, base) % p
        exp >>= 1
    # compute D
    D = np.zeros((N,N), dtype=np.int64)
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                if r == c:
                    # for u with A[u][r] != 0
                    for u in range(N):
                        if A[u][r] != 0:
                            D[u][r] = (D[u][r] + A[u][r]) % p
                    for v in range(N):
                        if A[r][v] != 0:
                            D[r][v] = (D[r][v] + A[r][v]) % p
                elif p == 3:
                    if A[c][r] != 0:
                        D[r][c] = (D[r][c] + A[c][r]) % p