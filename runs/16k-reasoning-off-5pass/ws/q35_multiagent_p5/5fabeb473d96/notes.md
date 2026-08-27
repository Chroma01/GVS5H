
## ideation
The problem asks for the sum of distances between $u$ and $v$ over all $(N-1)!$ possible random recursive trees defined by parent choices $P_i \in \{1, \dots, i-1\}$.
By linearity of expectation (or sum), the total distance is the sum over all edges $e_i$ (connecting $i$ to $P_i$ with weight $A_i$) of $A_i \times (\text{number of trees where } e_i \text{ is on the path between } u \text{ and } v)$.

Let $N_{total} = (N-1)!$.
For a fixed edge $i$ (node $i$'s parent edge), let $S_i$ be the random subtree rooted at $i$. The edge $i$ is on the path between $u$ and $v$ if and only if exactly one of $u, v$ is in $S_i$.
Assume $u < v$.
The condition $x \in S_i$ for $x > i$ is equivalent to $i$ being an ancestor of $x$.
It is a known property of random recursive trees that for $i < x$, $P(i \text{ is ancestor of } x) = \frac{1}{i}$.
Furthermore, for $i < u < v$, the events "$i$ is ancestor of $u$" and "$i$ is ancestor of $v$" are not independent, but we can compute the joint probability.
Actually, a more direct combinatorial approach is:
The number of trees where $i$ is an ancestor of $j$ ($i<j$) is $\frac{(N-1)!}{i}$.
The number of trees where $i$ is an ancestor of both $u$ and $v$ ($i < u < v$) is $\frac{(N-1)!}{i(i-1)}$? No.
Let's derive $P(i \text{ anc } u \text{ and } i \text{ anc } v)$ for $i < u < v$.
The path from $v$ to root must pass through $i$. The path from $u$ to root must pass through $i$.
Consider the set of nodes $\{1, \dots, v\}$. The structure of the tree on these nodes is a random recursive tree.
The probability that $i$ is an ancestor of $u$ is $1/i$.
Given $i$ is an ancestor of $u$, what is the probability $i$ is an ancestor of $v$?
This is equivalent to: in the random recursive tree on $\{1, \dots, v\}$, conditioned on $i$ being an ancestor of $u$, is $i$ an ancestor of $v$?
Actually, it is known that for $i < u < v$, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$?
Let's check $N=3, i=1, u=2, v=3$.
$P(1 \text{ anc } 2) = 1$. $P(1 \text{ anc } 3) = 1$. Joint = 1.
Formula $\frac{1}{1(0)}$ undefined.
For $i=2, u=3$? No, need $u < v$.
Let's check $N=4, i=1, u=2, v=3$.
$P(1 \text{ anc } 2 \text{ and } 1 \text{ anc } 3) = 1$.
$i=1, u=2, v=4$.
$P(1 \text{ anc } 2) = 1$. $P(1 \text{ anc } 4) = 1$. Joint = 1.
$i=2, u=3, v=4$.
$P(2 \text{ anc } 3) = 1/2$.
$P(2 \text{ anc } 4) = 1/2$.
$P(2 \text{ anc } 3 \text{ and } 2 \text{ anc } 4)$?
Trees on $\{1,2,3,4\}$: $3! = 6$.
P=(1,1,1): 2->1, 3->1, 4->1. 2 is not anc 3, not anc 4.
P=(1,1,2): 2->1, 3->1, 4->2. 2 is not anc 3, 2 is anc 4.
P=(1,1,3): 2->1, 3->1, 4->3. 2 is not anc 3, 2 is not anc 4 (path 4-3-1).
P=(1,2,1): 2->1, 3->2, 4->1. 2 is anc 3, 2 is not anc 4.
P=(1,2,2): 2->1, 3->2, 4->2. 2 is anc 3, 2 is anc 4.
P=(1,2,3): 2->1, 3->2, 4->3. 2 is anc 3, 2 is anc 4 (path 4-3-2-1).
So 2 is anc 3 in P=(1,2,1), (1,2,2), (1,2,3) -> 3 cases. Prob 3/6 = 1/2.
2 is anc 4 in P=(1,1,2), (1,2,2), (1,2,3) -> 3 cases. Prob 1/2.
Both in P=(1,2,2), (1,2,3) -> 2 cases. Prob 2/6 = 1/3.
Formula $\frac{1}{i(i-1)}$ for $i=2$ gives $1/2$. Incorrect.
Formula $\frac{1}{i(i+1)}$? $1/6$. Incorrect.
Formula $\frac{1}{i} \times \frac{1}{i}$? $1/4$. Incorrect.

Correct derivation:
$P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i} \times \frac{1}{i}$? No.
Actually, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$ is for specific cases?
Let's use the property: $P(i \text{ anc } u) = 1/i$.
$P(i \text{ anc } u \text{ and } i \text{ anc } v) = P(i \text{ anc } u) P(i \text{ anc } v | i \text{ anc } u)$.
Given $i$ is anc of $u$, the subtree of $i$ contains $u$. The probability that $v$ is in the subtree of $i$ is the same as the probability that $v$ is in the subtree of $i$ in a random recursive tree of size $v$ where $i$ is fixed as an ancestor of $u$?
Actually, it is known that $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$ is WRONG.
The correct probability is $\frac{1}{i(i-1)}$?
Let's check $i=2, u=3, v=4$. Prob = 1/3.
$\frac{1}{2(1)} = 1/2$. No.
$\frac{1}{2(2+1)} = 1/6$. No.
$\frac{1}{3} = \frac{1}{i(i-1)/2}$? No.

Let's look at the counts directly.
Number of trees where $i$ is anc of $u$: $N_{anc}(i, u) = \frac{(N-1)!}{i}$.
Number of trees where $i$ is anc of $u$ and $v$: $N_{anc}(i, u, v)$.
For $i < u < v$, $N_{anc}(i, u, v) = \frac{(N-1)!}{i(i-1)}$?
For $N=4, i=2, u=3, v=4$, $(N-1)! = 6$. $6 / (2 \cdot 1) = 3$. But we found 2.
So $N_{anc}(i, u, v) = \frac{(N-1)!}{i(i-1)}$ is wrong.
It is $\frac{(N-1)!}{i(i-1)} \times \dots$?
Actually, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$?
Wait, $2/6 = 1/3$.
$\frac{1}{i(i-1)} = 1/2$.
$\frac{1}{i(i+1)} = 1/6$.
$\frac{1}{i^2} = 1/4$.
$\frac{1}{i(i-1)/2}$? No.

Let's use the formula:
$P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$ is for $u, v$ being specific nodes?
Actually, the probability that $i$ is an ancestor of $u$ is $1/i$.
The probability that $i$ is an ancestor of $v$ given $i$ is an ancestor of $u$ is $1/(i)$? No.
It is $1/(i)$?
If $i$ is anc of $u$, then $u$ is in $T_i$. The probability that $v$ is in $T_i$ is the same as the probability that $v$ chooses a parent in $T_i$ eventually?
Actually, for $i < u < v$, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$?
Let's try $N=5, i=2, u=3, v=4$.
$(N-1)! = 24$.
$P(2 \text{ anc } 3) = 1/2$. Count = 12.
$P(2 \text{ anc } 4) = 1/2$. Count = 12.
$P(2 \text{ anc } 3 \text{ and } 2 \text{ anc } 4)$?
Count = ?
If we assume the pattern $1/3$ for $N=4$, maybe it's $1/3$ generally?
No, it depends on $N$? No, the probability that $i$ is anc of $u$ and $v$ depends only on $i, u, v$?
Actually, the event depends on the relative ordering.
For $i < u < v$, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$?
Let's check $i=1$. $P(1 \text{ anc } u \text{ and } 1 \text{ anc } v) = 1$.
Formula $\frac{1}{1(0)}$ undefined.
For $i=2$, $P(2 \text{ anc } 3 \text{ and } 2 \text{ anc } 4) = 1/3$.
Formula $\frac{1}{2(1)} = 1/2$.
Formula $\frac{1}{2(2)} = 1/4$.
Formula $\frac{1}{3} = \frac{1}{i(i-1)/2}$? No.

Correct Formula from literature:
$P(i \text{ is ancestor of } j) = 1/i$.
$P(i \text{ is ancestor of } j \text{ and } i \text{ is ancestor of } k) = \frac{1}{i(i-1)}$ for $i < j < k$?
No, for $i=2, j=3, k=4$, it is $1/3$.
$\frac{1}{2(1)} = 1/2$.
$\frac{1}{2(2)} = 1/4$.
$\frac{1}{3} = \frac{1}{i(i-1)/2}$? No.
$\frac{1}{3} = \frac{1}{i(i-1)} \times \dots$?

Actually, $P(i \text{ anc } u \text{ and } i \text{ anc } v) = \frac{1}{i(i-1)}$ is WRONG.
The correct probability is $\frac{1}{i(i-1)}$?
Let's just use the code to compute the exact counts for small N and find the pattern.

## worker: finalize
The problem asks for the sum of distances between $u$ and $v$ over all $(N-1)!$ random recursive trees. By linearity of expectation, this is the sum over all edges $e_i$ (connecting $i$ to $P_i$ with weight $A_i$) of $A_i \times (\text{number of trees where } e_i \text{ is on the path between } u \text{ and } v)$.

The edge $e_i$ is on the path between $u$ and $v$ if and only if exactly one of $u, v$ is in the subtree rooted at $i$ ($T_i$).
Assuming $u < v$:
1. If $i < u$: Both $u$ and $v$ can be in $T_i$. The probability that $i$ is an ancestor of $j$ ($i < j$) is $1/i$. The joint probability $P(i \text{ anc } u \text{ and } i \text{ anc } v)$ is $2/(i(i+1))$. Thus, $P(\text{exactly one}) = 2/i - 4/(i(i+1)) = 2(i-1)/(i(i+1))$.
2. If $i = u$: $u$ is always in $T_u$. $v$ is in $T_u$ with probability $1/u$. $P(\text{exactly one}) = 1 - 1/u = (u-1)/u$.
3. If $u < i < v$: $u$ is never in $T_i$. $v$ is in $T_i$ with probability $1/i$. $P(\text{exactly one}) = 1/i$.
4. If $i = v$: $v$ is always in $T_v$. $u$ is never in $T_v$. $P(\text{exactly one}) = 1$.
5. If $i > v$: Neither is in $T_i$. $P(\text{exactly one}) = 0$.

We precompute prefix sums of $A[i] \times \text{coeff}_i$ for the ranges $i < u$ and $u < i < v$ to answer each query in $O(1)$ time. The final answer is multiplied by $(N-1)!$.
