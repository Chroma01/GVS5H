
## ideation
The problem asks us to find a sequence $A$ of length $N$ such that for $M$ given pairs $(X_i, Y_i)$, the condition $A_{X_i} \oplus A_{Y_i} = Z_i$ holds. We need to minimize $\sum A_i$.

1.  **Graph Representation**: The indices $1 \dots N$ are nodes. Each constraint $(X_i, Y_i)$ with value $Z_i$ is an edge between $X_i$ and $Y_i$ with weight $Z_i$.
2.  **Connected Components**: The graph decomposes into connected components. Constraints within a component must be consistent with each other. Constraints between different components are independent.
3.  **Consistency Check (Cycle Detection)**:
    *   For any component, pick an arbitrary root node $r$ and set $A_r = 0$ (arbitrarily).
    *   Perform a traversal (BFS or DFS) to determine the value of every other node $u$ in the component relative to $r$. Let $val[u]$ be the value such that $A_u = A_r \oplus val[u]$. Since we set $A_r=0$, $A_u = val[u]$.
    *   If we encounter an edge $(u, v)$ with weight $w$ where $v$ has already been visited, we must check if $A_u \oplus A_v = w$. Substituting the derived values: $(A_r \oplus val[u]) \oplus (A_r \oplus val[v]) = val[u] \oplus val[v]$. This must equal $w$. If $val[u] \oplus val[v] \neq w$, the system is inconsistent, and no solution exists. Output -1.
4.  **Minimization Strategy**:
    *   Within a connected component, once the relative values ($val[u]$) are fixed by the traversal, the actual values are $A_u = K \oplus val[u]$ for some constant $K$ (where $K = A_r$).
    *   Changing $K$ flips the bits of all $A_u$ in that component according to the bits of $K$. Specifically, if we choose $K=0$, $A_u = val[u]$. If we choose $K = val[r]$ (effectively swapping the roles of 0 and the initial root value in the relative system, or simply trying the other "phase"), the new value is $val[u] \oplus val[r]$.
    *   Actually, a simpler view: Once relative values are fixed, the entire component's values are determined up to a global XOR constant $C$. The two distinct possibilities for the set of values in the component are:
        1.  Set $A_r = 0 \implies A_u = val[u]$. Sum $S_1 = \sum_{u \in Comp} val[u]$.
        2.  Set $A_r = val[r]$ (which is the value derived if we assumed the root was 1 in a binary sense, but here it's just the flip). Wait, if $A_r = C$, then $A_u = C \oplus val[u]$.
        *   Are there only 2 choices? Yes, because if we pick any $C$, the sum is $\sum (C \oplus val[u])$. However, note that $C$ is a single integer. We cannot pick $C$ bit-by-bit independently for different bits if we want to maintain the XOR difference property?
        *   Correction: The constraint is $A_u \oplus A_v = Z$. If we have a valid assignment $A^{(0)}$ where $A^{(0)}_r = 0$, then any other valid assignment must satisfy $A^{(1)}_u = A^{(0)}_u \oplus C$ for some constant $C$. Why? Because $(A^{(1)}_u \oplus C) \oplus (A^{(1)}_v \oplus C) = A^{(1)}_u \oplus A^{(1)}_v = Z = A^{(0)}_u \oplus A^{(0)}_v$. So $A^{(1)}_u = A^{(0)}_u \oplus C$.
        *   To minimize $\sum (A^{(0)}_u \oplus C)$, we need to find the optimal $C$.
        *   However, observe the structure: $A^{(0)}_u$ is fixed relative to the root. If we change the root's value from 0 to $X$, all values in the component become $A^{(0)}_u \oplus X$.
        *   Is it sufficient to check only $C=0$ and $C=val[root]$?
            *   Consider the component. We have values $v_1, v_2, \dots, v_k$. We want to minimize $\sum (v_i \oplus C)$.
            *   This is a known problem: finding $C$ to minimize sum of XORs. However, in this specific graph problem, the "degrees of freedom" are often limited.
            *   Let's re-read the logic. If the graph is bipartite (which it must be for a solution to exist if we view it as 2-coloring with weights), does that restrict $C$?
            *   Actually, the standard approach for this specific problem (often seen in competitive programming contexts like AtCoder) is:
                For each component, fix one node to 0. Propagate. Check consistency.
                Then, for that component, we have two candidate assignments for the whole component:
                Option 1: Keep the derived values ($A_r = 0$).
                Option 2: Flip all bits? No, that's not quite right.
                Let's look at the degrees of freedom again. $A_u \oplus A_v = Z$. This is a linear system over GF(2) for each bit.
                For a connected component, the solution space for a specific bit is either:
                - Unique (if the component has odd cycles? No, XOR graphs don't have "odd/even" cycles in the same way. Cycles imply $Z_{cycle} = 0$).
                - Two solutions: $x$ and $x \oplus 1$ (for that bit).
                Since the constraints link bits only via the values $Z_i$, the choices for different bits are independent *within* the component structure?
                Actually, the constraint $A_u \oplus A_v = Z_i$ couples all bits of $A_u$ and $A_v$ simultaneously. You cannot choose the LSB independently of the MSB.
                Therefore, the entire vector $A$ for a component is determined up to a global XOR constant $C$.
                So we need to find $C$ that minimizes $\sum_{u \in Comp} (val[u] \oplus C)$.
                Is it true that we only need to check $C=0$ and $C=val[root]$?
                Let's test. Suppose component has values $\{0, 4\}$.
                $C=0 \implies \{0, 4\}$, sum=4.
                $C=4 \implies \{4, 0\}$, sum=4.
                $C=1 \implies \{1, 5\}$, sum=6.
                $C=2 \implies \{2, 6\}$, sum=8.
                It seems checking $C=0$ and $C=val[root]$ (which corresponds to flipping the "root assumption") is sufficient?
                Wait, if $val[root] = 0$, then $C=0$ and $C=0$ are the same.
                If $val[root] \neq 0$, say $val[root]=K$.
                If we set $A_{root} = 0$, values are $V = \{v_1, \dots\}$.
                If we set $A_{root} = K$, values are $V' = \{v_1 \oplus K, \dots\}$.
                Are there other $C$?
                Suppose we have a component with 2 nodes, $u, v$, edge $Z=5$.
                $val[u]=0, val[v]=5$.
                Try $C=0 \implies \{0, 5\}$, sum=5.
                Try $C=5 \implies \{5, 0\}$, sum=5.
                Try $C=1 \implies \{1, 4\}$, sum=5.
                Try $C=2 \implies \{2, 7\}$, sum=9.
                Try $C=4 \implies \{4, 1\}$, sum=5.
                It seems the minimum is achieved when $C$ is either $0$ or $val[root]$?
                Actually, in many similar problems, the "flip" operation is defined as $A_u \leftarrow A_u \oplus val[root]$. This corresponds to setting the root to $val[root]$ instead of 0.
                Why would $C$ be restricted to these two?
                Because the system of equations $A_u \oplus A_v = Z$ defines a subspace. The dimension of the solution space for a connected component is 1 (one degree of freedom). The basis vector for this degree of freedom is the vector $B$ where $B_u = val[u]$ (assuming root is 0). Any solution is $A = A_{particular} \oplus (k \cdot B)$? No, over integers, it's $A_u = val[u] \oplus C$.
                The question is: does the optimal $C$ have to be $0$ or $val[root]$?
                Let's reconsider the sample cases or logic.
                Actually, the standard solution for this specific problem (which appears to be from a contest like AtCoder ABC or ARC) relies on the fact that for each component, you can either keep the current assignment or "invert" the assignment relative to the root.
                Wait, if I have $val[u]$ and $val[v]$, and I choose $C$, the cost is $\sum (val[u] \oplus C)$.
                Is it possible that a different $C$ yields a lower sum?
                Example: $val = \{0, 1, 2, 3\}$.
                $C=0 \to 0+1+2+3 = 6$.
                $C=1 \to 1+0+3+2 = 6$.
                $C=2 \to 2+3+0+1 = 6$.
                $C=3 \to 3+2+1+0 = 6$.
                $C=4 \to 4+5+6+7 = 22$.
                It seems for small numbers, $0$ and $val[root]$ (if $val[root]$ is part of the set) might not be the only candidates, but usually $val[root]$ is the "flip" of the root.
                However, note that $val[root]$ is the value of the root relative to itself? No, $val[root]=0$ by definition.
                Ah, if we set $A_{root} = 0$, then $val[root]=0$.
                If we set $A_{root} = X$, then the new values are $val[u] \oplus X$.
                The "flip" usually refers to the fact that if the graph is bipartite, we can swap the two partitions. But here the weights $Z$ are arbitrary.
                Let's look at the constraints again. $A_u \oplus A_v = Z$.
                This is equivalent to $A_u + A_v = Z$ in GF(2) vector space.
                The solution space is $A = A_0 \oplus C \cdot \mathbf{1}$? No.
                If $A$ is a solution, then $A' = A \oplus C$ is a solution ONLY IF $C \oplus C = 0$, which is always true for the edge constraint $(A_u \oplus C) \oplus (A_v \oplus C) = A_u \oplus A_v = Z$.
                So yes, the entire solution space for a component is $\{ A_0 \oplus C \mid C \in \mathbb{Z}_{\ge 0} \}$.
                We need to find $C$ minimizing $\sum (A_{0,u} \oplus C)$.
                Is it true that checking $C=0$ and $C=A_{0,root}$ is sufficient?
                Note that $A_{0,root} = 0$. So checking $C=0$ and $C=0$ is the same.
                This implies my previous deduction about "two choices" was based on a misunderstanding of the "flip".
                Let's re-evaluate.
                If I fix $A_{root}=0$, I get a specific vector $V$.
                If I fix $A_{root}=K$, I get vector $V \oplus K$.
                Are there any other degrees of freedom?
                No. The component is connected. Once $A_{root}$ is fixed, all other $A_u$ are fixed.
                So the only variable is $A_{root}$.
                But $A_{root}$ can be ANY integer?
                Yes.
                So we need to find $K$ to minimize $\sum_{u \in Comp} (val[u] \oplus K)$.
                Wait, if $K$ can be anything, why did the sample explanation say "Other good sequences include... but A=(0,3,4) has the smallest sum"?
                In Sample 1:
                Edges: (1,3,4), (1,2,3).
                Component {1,2,3}.
                Set $A_1 = 0$.
                $A_3 = 0 \oplus 4 = 4$.
                $A_2 = 0 \oplus 3 = 3$.
                Vector: $(0, 3, 4)$. Sum = 7.
                Try $A_1 = 1$.
                $A_3 = 1 \oplus 4 = 5$.
                $A_2 = 1 \oplus 3 = 2$.
                Vector: $(1, 2, 5)$. Sum = 8.
                Try $A_1 = 7$.
                $A_3 = 7 \oplus 4 = 3$.
                $A_2 = 7 \oplus 3 = 4$.
                Vector: $(7, 4, 3)$. Sum = 14.
                Try $A_1 = 2$.
                $A_3 = 6, A_2 = 1$. Sum = 9.
                It seems $K=0$ is optimal here.
                
                Is it possible that for some $K$, the sum is smaller?
                Consider $val = \{0, 1\}$.
                $K=0 \to 1$.
                $K=1 \to 1$.
                $K=2 \to 3$.
                Consider $val = \{0, 3\}$.
                $K=0 \to 3$.
                $K=3 \to 3$.
                $K=1 \to 1+2=3$.
                $K=2 \to 2+1=3$.
                Consider $val = \{0, 1, 2\}$.
                $K=0 \to 3$.
                $K=1 \to 1+0+3=4$.
                $K=2 \to 2+3+0=5$.
                $K=3 \to 3+2+1=6$.
                
                Hypothesis: The optimal $K$ is always either $0$ or $val[root]$?
                Wait, $val[root]$ is always 0 in our derivation.
                Maybe the "two choices" logic in competitive programming literature for this problem assumes that the component is bipartite and we can swap the two sets of nodes?
                No, the weights $Z$ break the simple bipartite structure unless $Z=0$ for edges within the same partition? No.
                Let's rethink the "degree of freedom".
                The system is $A_u \oplus A_v = Z_{uv}$.
                This is a system of linear equations over GF(2) if we consider bits independently.
                But the variables are integers.
                However, the constraint $A_u \oplus A_v = Z$ means $A_u$ and $A_v$ differ by $Z$ in XOR.
                If we change $A_u$ to $A_u \oplus \delta$, then $A_v$ must become $A_v \oplus \delta$ to maintain the XOR difference.
                So yes, the only degree of freedom is a global XOR constant $C$ for the component.
                So we must minimize $f(C) = \sum_{u \in Comp} (val[u] \oplus C)$.
                Is it true that the minimum of this function occurs at $C=0$ or $C=val[root]$?
                Wait, if $val[root]=0$, then $C=0$ is the only candidate from that pair.
                Maybe the "flip" is not about $C$, but about the fact that we can choose the root to be 0 or 1?
                No, the root can be any integer.
                
                Let's look at the constraints and typical solutions for this problem (it looks like AtCoder ABC 232 F? No. Maybe ABC 240 E? No. It's likely **AtCoder Grand Contest** or similar).
                Actually, this is **AtCoder Beginner Contest 232, Problem F**? No.
                It is **AtCoder Beginner Contest 257, Problem D**? No.
                It is **AtCoder Beginner Contest 287, Problem D**? No.
                It matches **AtCoder Beginner Contest 232, Problem C**? No.
                Wait, the problem is **AtCoder Beginner Contest 232, Problem F** is different.
                Let's search for "minimize sum of elements XOR constraints".
                This is **AtCoder Beginner Contest 240, Problem E**? No.
                It is **AtCoder Beginner Contest 232, Problem F** is "XOR Pyramid".
                Ah, this is **AtCoder Beginner Contest 232, Problem F** is not it.
                It is **AtCoder Beginner Contest 232, Problem D**? No.
                Okay, let's ignore the source and solve logically.
                
                Function $f(C) = \sum (val[u] \oplus C)$.
                This function is convex?
                For a single bit $k$, let $c_k$ be the $k$-th bit of $C$. Let $x_{u,k}$ be the $k$-th bit of $val[u]$.
                Contribution of bit $k$ to the sum is $c_k \cdot 2^k \cdot (\text{count of } u \text{ where } x_{u,k}=1) + (1-c_k) \cdot 2^k \cdot (\text{count of } u \text{ where } x_{u,k}=0)$.
                Wait, $a \oplus b$ sum is not separable like that because the bits are weighted by $2^k$.
                However, the choice of $c_k$ for bit $k$ is independent of $c_j$ for bit $j$ in terms of the sum?
                Yes! $\sum (val[u] \oplus C) = \sum_u \sum_k ( (val[u]_k \oplus C_k) \cdot 2^k ) = \sum_k 2^k \sum_u (val[u]_k \oplus C_k)$.
                So we can optimize each bit of $C$ independently!
                For each bit position $k$:
                Count how many $val[u]$ have bit $k$ set ($cnt_1$) and how many have bit $k$ unset ($cnt_0$).
                If we choose $C_k = 0$, cost is $cnt_1 \cdot 2^k$.
                If we choose $C_k = 1$, cost is $cnt_0 \cdot 2^k$.
                We choose $C_k = 0$ if $cnt_1 < cnt_0$, else $C_k = 1$.
                So the optimal $C$ is constructed by setting the $k$-th bit to 1 if the majority of $val[u]$ have 0 at that bit, else 0.
                
                Wait, does this mean we can just construct the optimal $C$ bit by bit?
                Yes.
                BUT, is there a constraint that $C$ must be one of the values in the component?
                No, $C$ is just a constant we XOR with everything.
                So the algorithm is:
                1. Build graph.
                2. Find connected components.
                3. For each component:
                   a. Pick root, set $val[root]=0$. BFS/DFS to compute $val[u]$ for all $u$.
                   b. Check consistency on edges. If fail, return -1.
                   c. For each bit $k$ from 0 to ~30:
                      Count $cnt_1$ (nodes with $k$-th bit 1) and $cnt_0$ (nodes with $k$-th bit 0).
                      If $cnt_0 > cnt_1$, set $k$-th bit of $C$ to 1. Else 0.
                   d. Compute final values $A_u = val[u] \oplus C$.
                   e. Add to total sum and store results.
                4. Print result.
                
                Let's verify with Sample 1.
                $val = \{0, 3, 4\}$. Binary: $000, 011, 100$.
                Bit 0: $val$ bits: $0, 1, 0$. $cnt_1=1, cnt_0=2$. Choose $C_0=1$.
                Bit 1: $val$ bits: $0, 1, 0$. $cnt_1=1, cnt_0=2$. Choose $C_1=1$.
                Bit 2: $val$ bits: $0, 0, 1$. $cnt_1=1, cnt_0=2$. Choose $C_2=1$.
                $C = 111_2 = 7$.
                $A_1 = 0 \oplus 7 = 7$.
                $A_2 = 3 \oplus 7 = 4$.
                $A_3 = 4 \oplus 7 = 3$.
                Sum = $7+4+3 = 14$.
                BUT Sample output says sum is $0+3+4=7$.
                My calculation gave 14.
                Why?
                Ah, because $C$ is not independent per bit?
                Wait, $\sum (A \oplus B) = \sum \sum (a_i \oplus b_i) 2^i = \sum 2^i \sum (a_i \oplus b_i)$.
                The sum is linear in the bits. The choice of $b_i$ (bit of C) does not affect other bits.
                So why did the sample output prefer $C=0$?
                Let's re-calculate the cost for $C=0$ and $C=7$.
                $C=0$: Sum = $0+3+4 = 7$.
                $C=7$: Sum = $7+4+3 = 14$.
                My bit logic:
                Bit 0: $val$ bits $\{0, 1, 0\}$. $cnt_1=1, cnt_0=2$. Optimal $C_0=1$. Cost contribution: $2 \times 1 = 2$.
                Bit 1: $val$ bits $\{0, 1, 0\}$. $cnt_1=1, cnt_0=2$. Optimal $C_1=1$. Cost contribution: $2 \times 2 = 4$.
                Bit 2: $val$ bits $\{0, 0, 1\}$. $cnt_1=1, cnt_0=2$. Optimal $C_2=1$. Cost contribution: $2 \times 4 = 8$.
                Total cost = $2+4+8 = 14$.
                Wait, if $C=0$, cost is $0+3+4=7$.
                Bits of $C=0$: $0,0,0$.
                Bit 0 cost: $1 \times 1 = 1$.
                Bit 1 cost: $1 \times 2 = 2$.
                Bit 2 cost: $1 \times 4 = 4$.
                Total = 7.
                So $C=0$ is better.
                Why did my bit logic suggest $C_0=1$?
                Because $cnt_0=2, cnt_1=1$. If I choose $C_0=1$, cost is $cnt_0 \times 1 = 2$. If I choose $C_0=0$, cost is $cnt_1 \times 1 = 1$.
                So $C_0=0$ is better!
                My logic: "If $cnt_0 > cnt_1$, set $C_k=1$".
                If $C_k=1$, cost is $cnt_0 \times 2^k$.
                If $C_k=0$, cost is $cnt_1 \times 2^k$.
                We want to minimize cost. So if $cnt_0 < cnt_1$, we choose $C_k=1$ (cost $cnt_0$). If $cnt_0 > cnt_1$, we choose $C_k=0$ (cost $cnt_1$).
                Correct logic: Choose $C_k=1$ if $cnt_0 < cnt_1$. Else $C_k=0$.
                In Sample 1:
                Bit 0: $cnt_0=2, cnt_1=1$. $2 > 1 \implies C_0=0$.
                Bit 1: $cnt_0=2, cnt_1=1 \implies C_1=0$.
                Bit 2: $cnt_0=2, cnt_1=1 \implies C_2=0$.
                So $C=0$. Correct.
                
                So the algorithm is:
                1. Build graph.
                2. Iterate components.
                3. BFS/DFS to get relative values $val[u]$. Check consistency.
                4. For each bit $k$, count $cnt_1$ and $cnt_0$ in the component.
                5. Set $C_k = 1$ if $cnt_0 < cnt_1$, else $0$.
                6. $A_u = val[u] \oplus C$.
                7. Accumulate sum.
                
                This seems robust. $N, M \le 2 \times 10^5$. $Z_i \le 10^9$ (so ~30 bits).
                Complexity: $O(N + M + 30 \times N)$. Feasible.

## worker: Implement the solution in Python.
1.  **Graph Modeling**: The problem is modeled as a graph where indices $1 \dots N$ are nodes and constraints $(X_i, Y_i, Z_i)$ are edges with weight $Z_i$.
2.  **Connected Components**: The graph is decomposed into connected components. Constraints within a component must be consistent.
3.  **Consistency Check**: For each component, we arbitrarily set the value of a root node to 0 and propagate the XOR constraints using BFS. If an edge connects two already visited nodes, we verify if the derived values satisfy the edge constraint ($A_u \oplus A_v = Z$). If not, no solution exists.
4.  **Minimization**: Once relative values $val[u]$ are fixed for a component (where $A_u = val[u] \oplus C$), we need to find a constant $C$ that minimizes $\sum (val[u] \oplus C)$. Since the sum of XORs is separable by bit positions, we can optimize each bit of $C$ independently. For each bit position $k$, we count how many nodes in the component have the $k$-th bit set ($cnt_1$) and unset ($cnt_0$). We set the $k$-th bit of $C$ to 1 if $cnt_0 < cnt_1$ (to minimize the number of set bits in the result for that position), otherwise 0.
5.  **Complexity**: The algorithm runs in $O(N + M + 30N)$ time, which fits well within the limits ($N, M \le 2 \times 10^5$).

## worker: Run the code against the provided sample inputs to
The solution models the problem as a graph where indices are nodes and constraints are weighted edges.
1.  **Graph Traversal**: We iterate through each node. If unvisited, we start a BFS to traverse the connected component.
2.  **Consistency Check**: During BFS, we assign values relative to the root (root=0). When encountering an already visited node, we verify if the existing relative values satisfy the edge constraint ($A_u \oplus A_v = Z$). If not, the system is inconsistent, and we output -1.
3.  **Optimization**: For a consistent component, the values are determined up to a global XOR constant $C$ ($A_u = val[u] \oplus C$). To minimize the sum $\sum A_u$, we determine the optimal $C$ bit by bit. For each bit position $k$, we count how many nodes in the component have the $k$-th bit set ($cnt_1$) and unset ($cnt_0$). We set the $k$-th bit of $C$ to 1 if $cnt_0 < cnt_1$ (to minimize the number of set bits in the result for that position), otherwise 0.
4.  **Complexity**: The algorithm runs in $O(N + M + 30N)$ time, which is efficient for $N, M \le 2 \times 10^5$.

## worker: Run the provided code against Sample 1, Sample 2, 
The code implements the logic derived:
1.  **Graph Construction**: Reads $N, M$ and builds an adjacency list where edges represent XOR constraints.
2.  **Component Processing**: Iterates through nodes $1 \dots N$. For unvisited nodes, it initiates a BFS to traverse the connected component.
3.  **Consistency Check**: During BFS, it assigns relative values ($val[u]$) starting from 0 for the root. When an edge to an already visited node is encountered, it checks if $val[u] \oplus val[v] == w$. If not, it sets `possible = False`.
4.  **Optimization**: For each consistent component, it counts the number of set bits ($cnt_1$) and unset bits ($cnt_0$) for each bit position $k$ across all nodes in the component. It constructs an optimal constant $C$ such that the $k$-th bit of $C$ is 1 if $cnt_0 < cnt_1$ (to minimize the sum of XORs for that bit position), otherwise 0.
5.  **Result Calculation**: The final value for each node is $val[u] \oplus C$.
6.  **Output**: Prints -1 if inconsistent, otherwise prints the sequence.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the logic derived:
1.  **Graph Construction**: Reads $N, M$ and builds an adjacency list where edges represent XOR constraints.
2.  **Component Processing**: Iterates through nodes $1 \dots N$. For unvisited nodes, it initiates a BFS to traverse the connected component.
3.  **Consistency Check**: During BFS, it assigns relative values ($val[u]$) starting from 0 for the root. When an edge to an already visited node is encountered, it checks if $val[u] \oplus val[v] == w$. If not, it sets `possible = False`.
4.  **Optimization**: For each consistent component, it counts the number of set bits ($cnt_1$) and unset bits ($cnt_0$) for each bit position $k$ across all nodes in the component. It constructs an optimal constant $C$ such that the $k$-th bit of $C$ is 1 if $cnt_0 < cnt_1$ (to minimize the sum of XORs for that bit position), otherwise 0.
5.  **Result Calculation**: The final value for each node is $val[u] \oplus C$.
6.  **Output**: Prints -1 if inconsistent, otherwise prints the sequence.

## worker: finalize
The solution models the problem as a graph where indices $1 \dots N$ are nodes and constraints $(X_i, Y_i, Z_i)$ are weighted edges.
1.  **Graph Traversal**: We iterate through each node. If unvisited, we start a BFS to traverse the connected component.
2.  **Consistency Check**: During BFS, we assign values relative to the root (root=0). When encountering an edge to an already visited node, we verify if the derived values satisfy the edge constraint ($A_u \oplus A_v = Z$). If not, the system is inconsistent, and we output -1.
3.  **Optimization**: For a consistent component, the values are determined up to a global XOR constant $C$ ($A_u = val[u] \oplus C$). To minimize the sum $\sum A_u$, we determine the optimal $C$ bit by bit. For each bit position $k$, we count how many nodes in the component have the $k$-th bit set ($cnt_1$) and unset ($cnt_0$). We set the $k$-th bit of $C$ to 1 if $cnt_0 < cnt_1$ (to minimize the number of set bits in the result for that position), otherwise 0.
4.  **Complexity**: The algorithm runs in $O(N + M + 30N)$ time, which is efficient for $N, M \le 2 \times 10^5$.
