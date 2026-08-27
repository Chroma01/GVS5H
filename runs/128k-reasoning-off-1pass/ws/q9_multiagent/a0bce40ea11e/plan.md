The problem requires calculating the sum of $B^p$ modulo $p$ over all valid matrices $B$. By Fermat's Little Theorem, for any non-zero element $x$, $x^p \equiv x \pmod p$, and $0^p = 0$. Thus, the sum of $B^p$ is equivalent to the sum of $B$ itself where every zero in $A$ is replaced by a sum of $x^p$ (which is $x$) over all possible choices. However, since we are summing over all $(p-1)^K$ matrices, we can treat the contribution of each cell independently. For a cell $(i, j)$ in $B$, if $A_{i,j} \neq 0$, its value is fixed. If $A_{i,j} = 0$, it takes values $1 \dots p-1$ uniformly. The term $(B^p)_{i,j}$ is a sum of products of entries. Due to the linearity of expectation (or sum) and the specific property that $\sum_{x=1}^{p-1} x^k \equiv 0 \pmod p$ for $0 < k < p-1$ and $\equiv -1 \pmod p$ for $k=p-1$ (and $1$ for $k=0$), we can derive that only terms where the total exponent of a variable $x$ in a product is a multiple of $p-1$ survive or simplify. Specifically, for the sum of $B^p$, the contribution of a zero at $(i,j)$ is non-zero only if the path/product structure forces the exponent of that variable to be $0 \pmod{p-1}$. Actually, a simpler approach using linearity: The sum of $B^p$ is the sum over all paths in the matrix multiplication definition. A term in $(B^p)_{i,j}$ is $\sum_{k_1, \dots, k_{p-1}} B_{i, k_1} B_{k_1, k_2} \dots B_{k_{p-1}, j}$. We sum this over all assignments of zeros. If a variable $B_{u,v}$ appears $c$ times in a product, its contribution to the sum over its domain $\{1, \dots, p-1\}$ is $\sum_{x=1}^{p-1} x^c$. This sum is $0 \pmod p$ if $c$ is not a multiple of $p-1$, and $-1 \pmod p$ if $c$ is a multiple of $p-1$ (and $c>0$), or $p-1 \equiv -1$ if $c=0$ (but $c \ge 1$ here). Wait, $\sum_{x=1}^{p-1} x^c \equiv 0 \pmod p$ for $1 \le c < p-1$, and $\equiv -1 \pmod p$ for $c \ge 1$ and $c \equiv 0 \pmod{p-1}$. If $c=0$, the sum is $p-1 \equiv -1$. But in matrix multiplication, exponents are counts of edges. Since $p$ is large, we only care if $c \equiv 0 \pmod{p-1}$. Given $N \le 100$, the max path length is $N$. If $p-1 > N$, then $c$ can never be a multiple of $p-1$ unless $c=0$ (impossible) or we consider the case where the variable doesn't appear? No, if a variable appears, $c \ge 1$. If $p-1 > N$, then $c < p-1$, so the sum is always 0. Thus, if $p-1 > N$, any zero in the matrix makes the entire sum 0? Let's re-evaluate.
Actually, the question asks for the sum of $B^p$.
$(B^p)_{i,j} = \sum_{k_1, \dots, k_{p-1}} B_{i, k_1} B_{k_1, k_2} \dots B_{k_{p-1}, j}$.
We sum this over all $B$. By linearity, we sum each term. A term is a product of $p$ entries. If any entry is a zero in $A$, say $B_{u,v}$, and it appears $c$ times in the product, the sum over its possible values is $\sum_{x=1}^{p-1} x^c$.
If $c \not\equiv 0 \pmod{p-1}$, the sum is $0 \pmod p$.
If $c \equiv 0 \pmod{p-1}$, the sum is $-1 \pmod p$.
Since the maximum number of times an entry can appear in a product of length $p$ is $p$, and the path length is $p-1$ (so $p$ entries total), the count $c$ can be up to $p$.
However, note that if $p-1 > N$, then any path of length $p-1$ (visiting $p$ vertices with repetition allowed) might repeat vertices. But the constraint is $N \le 100$. If $p$ is large (e.g., $p > N+1$), then $p-1 > N$. The maximum multiplicity of any edge in a walk of length $p-1$ is $p-1$. It is possible for an edge to appear $p-1$ times.
Wait, if $p-1 > N$, then $c$ can be $p-1$. In that case, the sum is $-1$.
But usually in these problems, if $p$ is large, the answer is 0 unless the structure forces specific counts.
Let's reconsider the logic. The sum is over all $B$.
If $A_{u,v} \neq 0$, $B_{u,v}$ is fixed.
If $A_{u,v} = 0$, $B_{u,v}$ varies.
For a specific term in the expansion of $(B^p)_{i,j}$, which is a product of $p$ variables $B_{x_1, y_1} \dots B_{x_p, y_p}$ (where $y_k = x_{k+1}$), we sum over all assignments.
The sum is non-zero modulo $p$ if and only if for every variable $B_{u,v}$ that is originally $0$ in $A$, the exponent of $B_{u,v}$ in the product is a multiple of $p-1$.
Since the product has length $p$, the exponents sum to $p$.
If $p-1 > N$, can we have an exponent equal to $p-1$? Yes, if the walk goes $u \to v \to u \to v \dots$ ($p-1$ times).
However, if $p-1 > N$, the only way to have an exponent divisible by $p-1$ (and $>0$) is if the exponent is exactly $p-1$ (since max exponent is $p$).
If $p-1 \le N$, then multiples of $p-1$ can be $p-1$ or $2(p-1)$ etc.
Actually, there is a known result for this specific problem (AtCoder ABC 244 F? No, this looks like a specific contest problem).
Let's simplify:
Sum of $x^c$ for $x \in \{1, \dots, p-1\}$ is $0 \pmod p$ if $c \not\equiv 0 \pmod{p-1}$.
It is $-1 \pmod p$ if $c \equiv 0 \pmod{p-1}$ and $c > 0$.
If $c=0$, sum is $p-1 \equiv -1$. But $c$ is count of occurrences, so $c \ge 1$ if the variable is present.
So, a term contributes $(-1)^k$ where $k$ is the number of distinct zero-entries whose exponent is a multiple of $p-1$.
Wait, if multiple zeros have exponents divisible by $p-1$, the product of their sums is $(-1) \times (-1) \dots$.
So, $(B^p)_{i,j}$ sum = $\sum_{\text{walks } W} \prod_{(u,v) \in W, A_{u,v}=0} (\sum_{x=1}^{p-1} x^{count_W(u,v)})$.
This is non-zero only if for all $(u,v)$ with $A_{u,v}=0$, $count_W(u,v) \equiv 0 \pmod{p-1}$.
If $p-1 > N$, then $count_W(u,v)$ can only be $0$ or $p-1$ (since max count is $p-1$). Since $count \ge 1$ for present edges, it must be $p-1$.
This implies the walk must traverse the edge $(u,v)$ exactly $p-1$ times.
Given $N \le 100$, if $p$ is large ($p-1 > N$), the only way to satisfy this for a zero is if the walk is entirely composed of that edge? Or rather, if a zero appears, the walk must be very specific.
Actually, if $p-1 > N$, then for any zero $(u,v)$, the only way $count \equiv 0 \pmod{p-1}$ is if $count = p-1$.
This means the walk must consist of $p-1$ steps, all being the edge $(u,v)$. This is only possible if $u=v$ (self loop) or if the walk oscillates $u \to v \to u \dots$. But the edge is $(u,v)$. The sequence of edges must be $(u,v), (v, \dots), \dots$. If the edge is $(u,v)$, the next edge must start at $v$. So the sequence must be $(u,v), (v, \dots)$. For the count of $(u,v)$ to be $p-1$, the walk must be $u \to v \to u \to v \dots$? No, the edge is directed. The edge $(u,v)$ goes from $u$ to $v$. The next edge must start at $v$. If the next edge is also $(u,v)$, it must be that $v=u$.
So if $p-1 > N$, a zero at $(u,v)$ with $u \neq v$ can never have count $p-1$ because you can't traverse $(u,v)$ then immediately $(u,v)$ again unless $u=v$.
Thus, if $p-1 > N$ and there is any zero at $(u,v)$ with $u \neq v$, the answer is 0.
If $u=v$ (diagonal zero), count can be $p-1$.
If $p-1 \le N$, we can have more complex walks.
However, given the constraints and typical CP patterns, if $p-1 > N$, the answer is likely 0 everywhere unless $A$ has no zeros or specific diagonal zeros.
But let's look at the sample cases.
Sample 1: N=2, p=3. $p-1=2 \le N$. Zeros at (1,1), (2,1).
Sample 2: N=3, p=2. $p-1=1 \le N$.
Sample 3: N=4, p=13. $p-1=12 > N$.
Output for Sample 3 is not all zeros.
Wait, Sample 3 output:
8 0 6 5
...
It's not zero.
Why?
Ah, the sum is over $B^p$.
Maybe my condition "count must be multiple of p-1" is correct, but I missed something.
Is it possible that $count = 0$? No, if the edge is in the walk, count $\ge 1$.
Is it possible that $count = p-1$ for $u \neq v$?
Walk: $u \to v \to u \to v \dots$
Edges: $(u,v), (v,u), (u,v), (v,u) \dots$
Count of $(u,v)$ is roughly $p/2$.
For $p=13$, $p-1=12$. We need count 12.
Walk length 12 (13 vertices).
If we have edge $(u,v)$, next is $(v, ?)$. To get another $(u,v)$, we need $?=u$. So $(v,u)$.
Then $(u,v)$ again.
Sequence: $(u,v), (v,u), (u,v), (v,u) \dots$
Length 12.
If we start at $u$, end at $u$?
$u \xrightarrow{(u,v)} v \xrightarrow{(v,u)} u \dots$
After 12 steps, we are at $u$ if 12 is even?
$u \to v$ (1), $v \to u$ (2), ... $u \to v$ (11), $v \to u$ (12). End at $u$.
Edges: 6 of $(u,v)$, 6 of $(v,u)$.
Count of $(u,v)$ is 6. Not 12.
So for $u \neq v$, count cannot be $p-1$ if $p-1$ is even?
Wait, if $p-1$ is odd?
If $p=3$, $p-1=2$. $u \to v \to u$. Edges: $(u,v), (v,u)$. Count $(u,v)=1$. Not 2.
So for $u \neq v$, count of $(u,v)$ is at most $(p-1)/2$?
Unless the walk is $u \to v \to v \to v \dots$? No, edges must match.
So if $u \neq v$, the count of $(u,v)$ is at most $\lceil (p-1)/2 \rceil$.
If $p-1 > 2 \lceil (p-1)/2 \rceil$, which is impossible.
Wait, if $p-1 > N$, and we need count $\equiv 0 \pmod{p-1}$.
Since max count for $u \neq v$ is $(p-1)/2$ (approx), and $p-1 > (p-1)/2$, the only multiple is 0. But count $\ge 1$.
So for $u \neq v$, if $p-1 > N$, the contribution is 0.
What about $u=v$?
Walk $u \to u \to u \dots$ (self loops).
Edges: $(u,u), (u,u), \dots$
Count of $(u,u)$ is $p-1$.
So if $A_{u,u} = 0$, and we have a walk of length $p-1$ staying at $u$, the count is $p-1$.
This contributes $-1$.
So for Sample 3 ($p=13, N=4$), $p-1=12 > 4$.
Zeros are at (1,1), (1,4), (2,3), (3,1), (3,3), (4,3), (4,4).
Diagonal zeros: (1,1), (3,3), (4,4).
Off-diagonal zeros: (1,4), (2,3), (3,1), (4,3).
For off-diagonal zeros, count cannot be 12. So they contribute 0.
For diagonal zeros, count can be 12.
So the sum is non-zero only for terms where the walk is a self-loop on a diagonal zero?
But the walk must start at $i$ and end at $j$.
If $i=j=u$, and $A_{u,u}=0$, we can have a walk $u \to u \dots \to u$ (12 steps).
This gives a term $(-1)$.
Are there other walks?
If $i \neq j$, can we have a walk with all zeros having count $\equiv 0 \pmod{p-1}$?
If there are any off-diagonal zeros in the walk, their count must be 0 (impossible) or $p-1$ (impossible for $u \neq v$).
So if the walk contains any off-diagonal zero, the term is 0.
Thus, the only non-zero terms are walks that use ONLY diagonal zeros (and non-zero entries).
And for those diagonal zeros, the count must be $p-1$.
This implies the walk must be entirely within a single vertex $u$ where $A_{u,u}=0$?
Or can it mix?
If the walk visits $u$ and $v$ ($u \neq v$), and $A_{u,u}=0, A_{v,v}=0$.
To have count of $(u,u)$ be $p-1$, the walk must be entirely at $u$.
So the walk cannot visit $v$.
Thus, for a fixed $i, j$, the sum is non-zero only if $i=j=u$ and $A_{u,u}=0$.
In that case, the only valid walk is the self-loop $u \to u \dots \to u$ ($p-1$ times).
The contribution is $(-1) \times (\text{product of non-zero entries?})$.
Wait, if $A_{u,u}=0$, the term is $\sum_{x=1}^{p-1} x^{p-1} = -1$.
The other entries in the walk are $A_{u,u}$ (which is the zero we are summing over).
So the term is just $-1$.
But what if $A_{u,u} \neq 0$? Then it's fixed.
So if $p-1 > N$:
If $i=j$ and $A_{i,i} = 0$, the answer is $-1 \pmod p$.
If $i=j$ and $A_{i,i} \neq 0$, the answer is $A_{i,i}^p \equiv A_{i,i} \pmod p$.
If $i \neq j$, the answer is 0?
Let's check Sample 3.
$p=13, N=4$. $p-1=12 > 4$.
Diagonal:
(1,1): 0 -> -1 = 12. Output says 8. Mismatch.
(2,2): 4 -> 4. Output says 1. Mismatch.
(3,3): 0 -> 12. Output says 4. Mismatch.
(4,4): 0 -> 12. Output says 9. Mismatch.
My hypothesis is wrong.
Re-read the problem carefully.
"Sum of $B^p$".
Maybe I should compute the sum of $B$ first?
No, $B^p$.
Is it possible that $p$ is small in general? No, $p \le 10^9$.
Wait, the sample 3 output is not 0 or -1.
Let's reconsider the condition.
$\sum_{x=1}^{p-1} x^c \equiv 0 \pmod p$ if $c \not\equiv 0 \pmod{p-1}$.
$\equiv -1 \pmod p$ if $c \equiv 0 \pmod{p-1}$.
This is correct.
Why did Sample 3 fail?
Maybe the walk doesn't have to be length $p-1$?
$B^p$ means $B \times B \times \dots \times B$ ($p$ times).
The indices are $i, k_1, k_2, \dots, k_{p-1}, j$.
Number of edges is $p$.
Wait, $B^p$ has $p$ factors.
$(B^2)_{ij} = \sum_k B_{ik} B_{kj}$. (2 factors, 2 edges? No, 2 matrices multiplied).
$(B^p)_{ij} = \sum_{k_1, \dots, k_{p-1}} B_{i, k_1} B_{k_1, k_2} \dots B_{k_{p-1}, j}$.
Number of terms in product is $p$.
Number of edges is $p$.
My previous count was $p-1$ steps?
$i \to k_1$ (1), $k_1 \to k_2$ (2), ..., $k_{p-1} \to j$ (p).
Total $p$ edges.
So the length of the walk is $p$.
The condition is $count \equiv 0 \pmod{p-1}$.
Max count is $p$.
Possible counts: $p-1, p$.
If count $= p$, then all edges are $(u,v)$. This requires $u=v$ (since $v \to u$ must be $(u,v)$).
If count $= p-1$, then one edge is different?
If $u \neq v$, can we have count $p-1$?
Walk: $u \to v \to u \to v \dots$
Edges: $(u,v), (v,u), (u,v), \dots$
Count of $(u,v)$ is roughly $p/2$.
If $p$ is large, $p/2 < p-1$.
So for $u \neq v$, count cannot be $p-1$ or $p$.
So only $u=v$ allows count $p-1$ or $p$.
If $u=v$, count can be $p$ (all self loops) or $p-1$ (one different edge? No, if one edge is different, say $(u, w)$, then we leave $u$. To get back, we need $(w, u)$. Then we are at $u$.
Sequence: $(u,u) \dots (u,u), (u,w), (w,u), (u,u) \dots$
Count of $(u,u)$ is $p-2$. Not divisible by $p-1$.
So for $u=v$, the only way to have count divisible by $p-1$ is count $= p-1$ or $p$.
If count $= p$, all edges are $(u,u)$.
If count $= p-1$, we need one edge not $(u,u)$. But then we must leave $u$ and come back.
If we leave $u$ via $(u,w)$, we must return via $(w,u)$.
Then we have 2 non-$(u,u)$ edges.
So count of $(u,u)$ is $p-2$.
Unless $p-2$ is a multiple of $p-1$? Impossible for $p>2$.
So only count $= p$ works for $u=v$.
This implies the walk must be entirely self-loops on $u$.
This leads back to the same contradiction with Sample 3.

Alternative idea:
Maybe the sum is not over $B^p$ but something else? No, "sum of B^p".
Maybe I should just implement the matrix exponentiation with the sum logic?
But $p$ is $10^9$, cannot iterate.
Wait, if $p-1 > N$, then for any zero $(u,v)$ with $u \neq v$, the count is never $0 \pmod{p-1}$.
So any walk containing an off-diagonal zero contributes 0.
So we only consider walks that use only diagonal zeros and non-zero entries.
And for diagonal zeros, the count must be $p-1$ or $p$.
As argued, only count $= p$ (all self loops) works.
So if $A_{i,i} = 0$, the only valid walk is $i \to i \dots \to i$ ($p$ times).
Contribution: $(-1) \times (\text{product of other edges?})$.
But there are no other edges.
So contribution is $-1$.
But Sample 3 output for (1,1) is 8. $p=13$. $-1 \equiv 12$.
Why 8?
Maybe my assumption about $\sum x^c$ is wrong?
$\sum_{x=1}^{p-1} x^c \pmod p$.
If $c=0$, sum is $p-1 \equiv -1$.
If $c \equiv 0 \pmod{p-1}$ and $c>0$, sum is $-1$.
If $c \not\equiv 0$, sum is 0.
This is standard.
Is it possible that $p$ is small in Sample 3? $p=13$.
Maybe the "zero" in $A$ is not the only thing?
"replacing each zero in A with an integer between 1 and p-1".
Yes.
Is it possible that the walk can use edges that are NOT zeros?
Yes. If $A_{u,v} \neq 0$, $B_{u,v}$ is fixed to $A_{u,v}$.
So the term is $A_{u,v}^{count}$.
If $A_{u,v} = 0$, it is $\sum x^{count}$.
So for Sample 3, (1,1) is 0.
Walk $1 \to 1 \dots \to 1$.
Edges: $(1,1)$ 12 times? No, $p=13$, so 13 edges.
Count of $(1,1)$ is 13.
$13 \equiv 1 \pmod{12}$. Not 0.
So sum is 0?
But output is 8.
This implies my condition "count must be multiple of p-1" is wrong.
Why?
Ah! $B^p$.
Fermat's Little Theorem: $x^p \equiv x \pmod p$.
So $B^p \equiv B \pmod p$.
Wait, is this true for matrices?
$(B^p)_{ij} = \sum \dots$.
If we replace $B_{uv}^p$ with $B_{uv}$, does it hold?
No, $(B^p)_{ij}$ is not $\sum B_{ij}$.
But $x^p \equiv x$ for scalars.
So if the matrix entries are in $\mathbb{Z}_p$, then $B^p = B$?
No, matrix exponentiation is not the same as element-wise.
However, if $B$ is a matrix over $\mathbb{Z}_p$, then $B^p \equiv B$ is NOT generally true.
But maybe the sum simplifies?
Let's check Sample 1.
$p=3$. $B^3$.
Sample output:
0 2
1 2
If $B^3 \equiv B$, then sum of $B$ over all $B$.
Zeros at (1,1), (2,1).
(1,1): sum of $1,2$ is $1+2=3 \equiv 0$.
(2,1): sum of $1,2$ is $0$.
(1,2): fixed 1.
(2,2): fixed 2.
Sum of $B$:
(1,1): 0.
(1,2): 1.
(2,1): 0.
(2,2): 2.
Matrix:
0 1
0 2
Mod 3:
0 1
0 2
Sample output:
0 2
1 2
Mismatch. (1,2) is 2 in output, 1 in sum-B.
So $B^3 \neq B$ in sum.
Okay, back to the counting.
Maybe the number of zeros $K$ matters?
Total sum = $\sum_B \sum_{\text{walks}} \prod B_{edges}$.
Swap sums: $\sum_{\text{walks}} \sum_B \prod B_{edges}$.
For a fixed walk, let $S$ be the set of edges in the walk.
For $e \in S$, if $A_e \neq 0$, value is $A_e$.
If $A_e = 0$, value is $\sum_{x=1}^{p-1} x^{count(e)}$.
Let $c_e$ be the count of edge $e$ in the walk.
Term is $\prod_{e \in S, A_e \neq 0} A_e^{c_e} \times \prod_{e \in S, A_e = 0} (\sum_{x=1}^{p-1} x^{c_e})$.
The sum over $x$ is $0$ if $c_e \not\equiv 0 \pmod{p-1}$.
It is $-1$ if $c_e \equiv 0 \pmod{p-1}$ and $c_e > 0$.
So for the term to be non-zero, for every zero edge $e$ in the walk, $c_e \equiv 0 \pmod{p-1}$.
In Sample 3, $p=13, p-1=12$.
Walk length 13.
If a zero edge has count 12, it works.
If count 13, $13 \equiv 1 \pmod{12}$, fails.
So we need count 12.
Walk length 13.
If an edge appears 12 times, the other edge appears 1 time.
Let the edge with count 12 be $e_1=(u,v)$.
The other edge $e_2$ must connect $v$ to $u$ to close the loop?
Walk: $u \xrightarrow{e_1} v \xrightarrow{e_2} u \dots$
If $e_1$ appears 12 times, and $e_2$ appears 1 time.
Sequence: $e_1, e_2, e_1, e_1, \dots$?
Start at $i$.
$i \xrightarrow{e_1} v \xrightarrow{e_2} u \xrightarrow{e_1} v \dots$
If $e_1=(u,v)$, then after $e_2$ (which must be $(v,u)$), we are at $u$.
Then we can do $e_1$ again.
So we can have 12 $e_1$ and 1 $e_2$.
Total 13 edges.
Start at $i$. End at $j$.
If $e_1=(u,v)$ and $e_2=(v,u)$.
Walk: $u \to v \to u \to v \dots$
If we start at $u$, do $e_1$ (to $v$), then $e_2$ (to $u$), then 11 $e_1$?
No, we need 12 $e_1$.
Path: $u \xrightarrow{e_1} v \xrightarrow{e_2} u \xrightarrow{e_1} v \dots$
If we alternate, counts are equal.
To get 12 $e_1$ and 1 $e_2$:
Start at $u$.
$u \xrightarrow{e_1} v \xrightarrow{e_2} u \xrightarrow{e_1} v \dots$
We need 12 $e_1$.
Sequence: $e_1, e_2, e_1, e_1, \dots$?
No, edges must match.
$u \xrightarrow{e_1} v$. Next must start at $v$.
If next is $e_2=(v,u)$, then next must start at $u$.
If next is $e_1=(u,v)$, ok.
So we can have $e_1, e_2, e_1, e_1, \dots$?
No, after $e_2$ we are at $u$. We can do $e_1$.
After $e_1$ we are at $v$. We can do $e_2$ or $e_1$?
If we do $e_1$, we need $v=u$, impossible.
So after $e_1$, we MUST do $e_2$ (if $e_2$ is the only option from $v$).
But we can have other edges.
If the walk uses only $e_1$ and $e_2$, and $e_1=(u,v), e_2=(v,u)$.
Then the sequence must be alternating $e_1, e_2, e_1, e_2 \dots$.
Counts are equal.
So we cannot have 12 and 1.
Unless there is a self loop?
If $e_1=(u,u)$. Then we can do $e_1$ 12 times, and one other edge?
If $e_1=(u,u)$, we are at $u$.
We can do $e_1$ 12 times. Then one more edge $e_2=(u, j)$.
Then we end at $j$.
So if $A_{u,u}=0$, and there is an edge $(u,j)$ (which can be zero or non-zero), we can have a walk with 12 $(u,u)$ and 1 $(u,j)$.
Condition: $A_{u,u}=0$.
The term for $(u,u)$ is $-1$.
The term for $(u,j)$ is $A_{u,j}$ (if non-zero) or sum (if zero).
If $A_{u,j} \neq 0$, term is $A_{u,j}$.
So contribution is $-1 \times A_{u,j}$.
This matches the structure of Sample 3?
Sample 3: (1,1) is 0.
Possible $j$: 1, 2, 3, 4.
If $j=1$, edge $(1,1)$. Count 13. Fails.
If $j=2$, edge $(1,2)=1$. Count 1.
Walk: 12 times $(1,1)$, then $(1,2)$.
Start 1, end 2.
Contribution: $-1 \times 1 = -1 \equiv 12$.
But output is 8.
Maybe there are multiple such walks?
Or maybe $A_{1,2}$ is not the only option.
Wait, if $A_{1,2}=1$, fixed.
What if $A_{1,3}=2$?
Walk: 12 $(1,1)$, then $(1,3)$.
Contribution: $-1 \times 2 = -2 \equiv 11$.
Sum: $12 + 11 + \dots$?
This seems plausible.
So the algorithm is:
For each $i, j$:
Sum over all $u$ such that $A_{u,u}=0$.
If $i=u$ and $j=u$, count 13 (fails).
If $i=u$ and $j \neq u$, we need a walk with 12 $(u,u)$ and 1 $(u,j)$.
This is valid if $A_{u,u}=0$.
The term is $-1 \times A_{u,j}$ (if $A_{u,j} \neq 0$) or sum over $x$ (if $A_{u,j}=0$).
If $A_{u,j}=0$, sum is $-1$ (since count 1, not div by 12).
So if $A_{u,j}=0$, term is $-1 \times (-1) = 1$.
So for each $u$ with $A_{u,u}=0$:
If $i=u$:
  For each $j$:
    If $j=u$: 0 (count 13).
    If $j \neq u$:
      If $A_{u,j} \neq 0$: add $-A_{u,j}$.
      If $A_{u,j} = 0$: add $1$.
If $i \neq u$:
  Can we start at $i$?
  We need 12 $(u,u)$.
  Path: $i \to \dots \to u \xrightarrow{12} u \xrightarrow{1} j$.
  But we need to get to $u$ and leave $u$.
  If we enter $u$ via some edge, we must leave.
  If we do 12 $(u,u)$, we are at $u$.
  Then we do 1 edge to $j$.
  So the walk is $i \to \dots \to u \to u \dots \to u \to j$.
  The segment $u \to \dots \to u$ must be valid.
  But we only have 12 $(u,u)$ and 1 $(u,j)$.
  So the only edges are $(u,u)$ and $(u,j)$.
  To get from $i$ to $u$, we need edges.
  If $i \neq u$, we need at least one edge not $(u,u)$ or $(u,j)$.
  But we only have 13 edges total.
  If we use any other edge, its count must be multiple of 12.
  Impossible (max 13).
  So no other edges allowed.
  Thus, we cannot reach $u$ from $i$ if $i \neq u$.
  So only $i=u$ works.
  And we need $j$ such that we can leave $u$.
  So for each $u$ with $A_{u,u}=0$:
    For $j \neq u$:
      If $A_{u,j} \neq 0$: add $-A_{u,j}$.
      If $A_{u,j} = 0$: add $1$.
  Also, what if $i \neq u$ but $A_{i,i} \neq 0$?
  Then we can't use the zero logic.
  So the answer is sum over $u$ with $A_{u,u}=0$ of the above.
  Plus, if $A_{i,i} \neq 0$, is there any contribution?
  If $A_{i,i} \neq 0$, then no zero at $i$.
  So no term with $-1$.
  So answer is 0?
  But Sample 3 (2,2) is 1. $A_{2,2}=4 \neq 0$.
  So my logic is incomplete.
  Maybe there are walks with no zeros?
  If no zeros, term is $\prod A_e^{c_e}$.
  Sum over walks.
  This is just $(A^p)_{ij} \pmod p$.
  But we sum over $B$. If no zeros, $B=A$.
  So sum is $A^p$.
  If there are zeros, we add the contributions from walks with zeros.
  So:
  Total = $(A^p)_{ij} + \sum_{u: A_{u,u}=0} \text{contribution from walks with } u \text{ as the zero hub}$.
  Wait, if $A_{u,u}=0$, then $A^p$ uses $0^p=0$.
  So the term in $A^p$ is 0.
  The actual sum includes the walks where $B_{u,u}$ is replaced by $x$.
  So we add the sum of those walks.
  My derived contribution for $u$ with $A_{u,u}=0$ and $i=u, j \neq u$ is $-A_{u,j}$ (if $A_{u,j} \neq 0$) or $1$ (if $A_{u,j}=0$).
  What about $i \neq u$?
  If $i \neq u$, can we have a walk with 12 $(u,u)$?
  Only if we can reach $u$ and leave $u$ with no other edges.
  Impossible if $i \neq u$.
  So only $i=u$ contributes.
  So for each $u$ with $A_{u,u}=0$:
    For $j \neq u$:
      If $A_{u,j} \neq 0$: add $-A_{u,j}$.
      If $A_{u,j} = 0$: add $1$.
  And for $j=u$: 0.
  Also, we must add the term from $A^p$ where $B=A$.
  But $A^p$ has 0 at $(u,u)$?
  No, $A^p$ is computed with $A_{u,u}=0$.
  So $(A^p)_{ij}$ is the sum of walks with fixed values.
  If a walk uses $(u,u)$, it contributes 0.
  So $(A^p)_{ij}$ only counts walks that do NOT use $(u,u)$?
  No, it counts walks, but the value of $(u,u)$ is 0, so any walk using $(u,u)$ has product 0.
  So $(A^p)_{ij}$ is sum of walks that avoid all zeros?
  No, walks can use zeros, but their value is 0.
  So $(A^p)_{ij}$ is sum of walks that use ONLY non-zero entries.
  Then we add the contributions from walks that use zeros.
  The only non-zero contributions come from walks with exactly one zero at $(u,u)$ with count 12, and one non-zero (or zero) at $(u,j)$.
  So:
  Result = $(A^p)_{ij} + \sum_{u: A_{u,u}=0, i=u, j \neq u} (\text{if } A_{u,j} \neq 0 \text{ then } -A_{u,j} \text{ else } 1)$.
  Let's test Sample 3.
  $A^p \pmod{13}$.
  Compute $A^p$. Since $p=13$, $A^{13} \equiv A \pmod{13}$?
  No, matrix.
  But if $A$ has zeros, $A^{13}$ might be 0.
  Let's assume $A^p$ is computed normally.
  Then add corrections.
  This seems to be the solution.