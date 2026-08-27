1. **Analyze the Graph Structure**: The graph $G$ consists of a cycle $0-1-\dots-(N-1)-0$ and a "hub" vertex $N$ connected to vertex $i$ if $s_i=1$. Let $K$ be the number of 1s in $s$. The total number of edges is $N + K$.
2. **In-Degree Constraints**: In any orientation, the sum of in-degrees is $N+K$. For vertex $i < N$, its degree in $G$ is $2 + s_i$ (two cycle neighbors + hub if $s_i=1$). For vertex $N$, its degree is $K$.
3. **Decompose the Problem**: The orientation of cycle edges and hub edges are somewhat independent but linked by the in-degree counts. Specifically, for each $i$, let $x_i$ be the direction of the cycle edge between $i$ and $(i+1)\bmod N$ (say $x_i=1$ if $i \to i+1$, $0$ if $i+1 \to i$). Let $y_i$ be the direction of the edge between $i$ and $N$ (say $y_i=1$ if $i \to N$, $0$ if $N \to i$).
4. **Formulate In-Degrees**:
   - $d_i = (1-x_{i-1}) + x_i + (1-y_i)$ if $s_i=1$ (incoming from prev cycle, outgoing to next cycle, incoming from hub? No: $x_{i-1}=1 \implies i-1 \to i$, so $1-x_{i-1}$ is 0. Wait. Let's define carefully.
   - Let $c_i \in \{0,1\}$ be orientation of edge $(i, i+1)$. $c_i=1 \iff i \to i+1$. Then $i \to i+1$ contributes 1 to $d_{i+1}$ and 0 to $d_i$. Edge $(i-1, i)$ contributes $c_{i-1}$ to $d_i$ if $c_{i-1}=1$ ($i-1 \to i$) and $1-c_{i-1}$ to $d_i$ if $c_{i-1}=0$ ($i \to i-1$). So cycle contribution to $d_i$ is $c_{i-1} + (1-c_{i-1})$? No.
     - If $c_{i-1}=1$ ($i-1 \to i$), $i$ gets 1.
     - If $c_{i-1}=0$ ($i \to i-1$), $i$ gets 0.
     - If $c_i=1$ ($i \to i+1$), $i$ gets 0.
     - If $c_i=0$ ($i+1 \to i$), $i$ gets 1.
     - So cycle in-degree for $i$ is $c_{i-1} + (1-c_i)$.
   - Hub contribution: If $s_i=1$, edge $(i,N)$. Let $h_i=1$ if $i \to N$, $0$ if $N \to i$.
     - If $h_i=1$, $i$ gets 0.
     - If $h_i=0$, $i$ gets 1.
     - So hub in-degree for $i$ is $1-h_i$ (if $s_i=1$), else 0.
   - Thus $d_i = c_{i-1} + 1 - c_i + (1-h_i)s_i$.
   - For $d_N$: It receives from $i$ if $h_i=1$. So $d_N = \sum_{i: s_i=1} h_i$.
5. **Counting Valid Sequences**: We need to count distinct vectors $(d_0, \dots, d_N)$.
   - Note that $d_i$ depends on $c_{i-1}, c_i, h_i$.
   - The sequence $c_0, \dots, c_{N-1}$ determines the "cycle flow". There are $2^N$ such sequences.
   - The sequence $h_i$ (for $s_i=1$) determines hub connections. There are $2^K$ such sequences.
   - Total orientations $2^{N+K}$. However, different orientations might yield the same in-degree sequence.
   - Key Insight: The map from orientations to in-degree sequences is not necessarily injective. However, notice that $d_i$ for $i<N$ is determined locally by $c_{i-1}, c_i, h_i$. $d_N$ is determined globally by all $h_i$.
   - Actually, we can iterate over all possible cycle orientations ($2^N$ is too big). We need a smarter way.
   - Observe that $d_i - d_{i+1}$ might simplify?
   - Alternative approach: Dynamic Programming.
   - Let's fix the cycle orientation pattern. The values $c_i$ form a binary string.
   - For a fixed $c$, the term $A_i = c_{i-1} + 1 - c_i$ is fixed for each $i$. $A_i \in \{0, 1, 2\}$.
     - $c_{i-1}=0, c_i=0 \implies A_i = 0 + 1 - 0 = 1$.
     - $c_{i-1}=0, c_i=1 \implies A_i = 0 + 1 - 1 = 0$.
     - $c_{i-1}=1, c_i=0 \implies A_i = 1 + 1 - 0 = 2$.
     - $c_{i-1}=1, c_i=1 \implies A_i = 1 + 1 - 1 = 1$.
   - So $A_i \in \{0, 1, 2\}$. Specifically, $A_i=0$ iff $c_{i-1}=0, c_i=1$. $A_i=2$ iff $c_{i-1}=1, c_i=0$. $A_i=1$ otherwise.
   - If $s_i=1$, $d_i = A_i + (1-h_i)$. Since $h_i \in \{0,1\}$, $d_i$ can be $A_i$ or $A_i+1$.
   - If $s_i=0$, $d_i = A_i$.
   - $d_N = \sum_{i: s_i=1} h_i$. Let $H = d_N$. Then $\sum_{i: s_i=1} h_i = H$.
   - For a fixed cycle orientation $c$, the possible values of $d_i$ for $s_i=1$ are coupled with $H$.
   - Specifically, for each $i$ with $s_i=1$, we choose $h_i$. This determines $d_i$ and contributes to $H$.
   - The sequence $d$ is determined by $c$ and the choices of $h_i$.
   - Two different pairs $(c, h)$ and $(c', h')$ might produce the same $d$.
   - However, note that $A_i$ is determined by $c$. If $c \neq c'$, can they produce the same $d$?
     - If $s_i=0$, $d_i = A_i$. So if $c$ and $c'$ differ at a position where $s_{i-1}=0$ or $s_i=0$? No, $A_i$ depends on $c_{i-1}, c_i$.
     - If there is any $i$ with $s_i=0$, then $d_i = A_i$. If $c \neq c'$, it's possible $A_i = A'_i$ for all $i$.
     - Example: $c = 00, c' = 11$. $A_0(c) = c_{N-1} + 1 - c_0$. $A_0(c') = c'_{N-1} + 1 - c'_0$.
     - If $N=3$, $c=000 \implies A=(1,1,1)$. $c=111 \implies A=(1,1,1)$.
     - So $c=000$ and $c=111$ produce the same $A$ vector. In fact, any $c$ and its bitwise negation $\bar{c}$ produce the same $A$?
       - $A_i(c) = c_{i-1} + 1 - c_i$.
       - $A_i(\bar{c}) = (1-c_{i-1}) + 1 - (1-c_i) = 1 - c_{i-1} + c_i = 2 - (c_{i-1} + 1 - c_i) = 2 - A_i(c)$.
       - So $A_i(\bar{c}) = 2 - A_i(c)$. They are NOT the same unless $A_i=1$.
     - So $c$ and $\bar{c}$ generally produce different $A$.
     - However, $c$ and $c$ shifted? No.
   - Crucial Observation: The mapping from $(c, h)$ to $d$ is injective?
     - Given $d$, can we recover $c$ and $h$?
     - For $s_i=0$, $d_i = A_i$. This fixes $A_i$.
     - For $s_i=1$, $d_i \in \{A_i, A_i+1\}$. This gives $h_i = 1 - (d_i - A_i)$.
     - So if we know $A$, we know $h$. And $H = \sum h_i$ must match $d_N$.
     - So for a fixed $c$, the $h$ is uniquely determined by $d_{0\dots N-1}$. And $d_N$ is then fixed.
     - Thus, different $c$ might produce the same $d$ if they produce the same $A$ and compatible $h$.
     - But we established $A$ determines $c$ up to some symmetries?
     - Actually, $A_i$ determines the transitions. $A_i=0 \iff 0 \to 1$. $A_i=2 \iff 1 \to 0$. $A_i=1 \iff 0 \to 0$ or $1 \to 1$.
     - The sequence $A$ does not uniquely determine $c$. For example, if all $A_i=1$, $c$ could be all 0s or all 1s.
     - If $c=00\dots0$, $h$ is determined by $d_i \in \{1, 2\}$.
     - If $c=11\dots1$, $A_i=1$. $h$ is determined by $d_i \in \{1, 2\}$.
     - The resulting $d$ sequence is identical for $c=00\dots0$ and $c=11\dots1$ IF the same $h$ is chosen?
       - For $c=00\dots0$, $d_i = 1 + (1-h_i)$.
       - For $c=11\dots1$, $d_i = 1 + (1-h_i)$.
       - Yes! So $c=0^N$ and $c=1^N$ produce the same set of $d$ vectors for the same $h$.
     - Are there other collisions?
       - Generally, $A_i$ determines $c_{i-1} \oplus c_i$? No.
       - $A_i=0 \implies c_{i-1}=0, c_i=1$.
       - $A_i=2 \implies c_{i-1}=1, c_i=0$.
       - $A_i=1 \implies c_{i-1}=c_i$.
       - So $A$ determines the "edges" where $c$ flips. The values of $c$ are determined up to a global flip (0 vs 1) if the graph of flips is connected?
       - If there is at least one $A_i \in \{0,2\}$, the relative values of $c$ are fixed. Then $c$ is determined up to global flip.
       - If all $A_i=1$, then $c$ can be all 0 or all 1.
     - Case 1: $s$ has at least one 0. Then there is some $i$ with $s_i=0$. $d_i = A_i$.
       - If the pattern of $A$ forces a unique $c$ or pair $\{c, \bar{c}\}$, we handle it.
     - Case 2: All $s_i=1$. Then $d_i$ never directly reveals $A_i$.
       - Here, $d_i = A_i + 1 - h_i$.
       - $d_N = \sum h_i$.
       - We need to count distinct $d$.

   - Simplified Strategy:
     1. Identify that $c$ and $\bar{c}$ often produce same $A$-related structures? No, $A(\bar{c}) = 2-A(c)$.
     2. If $c \neq \bar{c}$, the $A$ vectors are different.
     3. The only collision is when $c = \bar{c}$? Impossible for $N \ge 1$.
     4. Wait, $c=00\dots0$ gives $A=(1,1,\dots,1)$. $c=11\dots1$ gives $A=(1,1,\dots,1)$.
        - Here $c \neq \bar{c}$ (unless $N=0$), but $A(c) = A(\bar{c})$.
        - This happens iff $c$ is constant.
        - Are there other $c$ with $A(c) = A(c')$?
        - $A_i(c) = A_i(c') \implies c_{i-1} - c_i = c'_{i-1} - c'_i$.
        - This implies $c_i - c'_i = c_{i-1} - c'_{i-1}$.
        - So $c_i - c'_i$ is constant for all $i$.
        - Since $c, c' \in \{0,1\}$, the difference is in $\{-1, 0, 1\}$.
        - If constant is 0, $c=c'$.
        - If constant is 1, $c_i = c'_i + 1$. Since values are 0/1, this means $c'_i=0, c_i=1$ for all $i$. So $c=1^N, c'=0^N$.
        - If constant is -1, $c_i = c'_i - 1$. So $c=0^N, c'=1^N$.
        - Conclusion: $A(c) = A(c')$ if and only if $c=c'$ or $\{c,c'\} = \{0^N, 1^N\}$.
     
     - So, all $c$ except $0^N$ and $1^N$ produce unique $A$ vectors.
     - $0^N$ and $1^N$ produce the same $A$ vector (all 1s).
     
     - Algorithm:
       1. Calculate the number of distinct $d$ vectors generated by $c \notin \{0^N, 1^N\}$.
          - For each such $c$, $A$ is unique.
          - For a fixed $A$, we vary $h$ (for $s_i=1$).
          - $d_i = A_i + (1-h_i)$ for $s_i=1$, $d_i=A_i$ for $s_i=0$.
          - $d_N = \sum_{s_i=1} h_i$.
          - The vector $d$ is determined by $A$ and $h$.
          - Since $A$ is unique to $c$ (except the pair), and $h$ varies, do different $c$ produce overlapping $d$?
          - If $A(c) \neq A(c')$, can they produce same $d$?
            - If there is any $i$ with $s_i=0$, $d_i = A_i$. So if $A(c) \neq A(c')$, $d$ differs at $i$.
            - If all $s_i=1$, then $d_i = A_i + 1 - h_i$.
            - We need $A_i + 1 - h_i = A'_i + 1 - h'_i \implies h_i - h'_i = A_i - A'_i$.
            - Also $d_N = \sum h_i = \sum h'_i$.
            - This is a system of equations. It's possible for different $(A, h)$ and $(A', h')$ to collide.
            
     - Given complexity, let's use DP.
     - State: DP index $i$, current "phase" of cycle orientation relative to start?
     - Since $N$ is up to $10^6$, we need $O(N)$ or $O(N \log N)$.
     
     - Let's count total valid $d$ sequences.
     - Total orientations $2^{N+K}$.
     - Map $(c, h) \to d$.
     - We know $c=0^N$ and $c=1^N$ map to same $A$.
     - For any other $c$, $A$ is unique.
     - Let $S$ be the set of all $d$ vectors.
     - $S = S_{special} \cup S_{others}$.
     - $S_{special}$: $d$ vectors from $c=0^N$ and $c=1^N$.
       - $A_i=1$ for all $i$.
       - $d_i = 1 + 1 - h_i = 2 - h_i$ for $s_i=1$.
       - $d_i = 1$ for $s_i=0$.
       - $d_N = \sum_{s_i=1} h_i$.
       - $h_i \in \{0,1\}$.
       - $d_i \in \{1,2\}$ for $s_i=1$.
       - Let $k = \sum h_i$. Then $d_N = k$.
       - The number of 2s in $d_{0\dots N-1}$ (at positions with $s_i=1$) is $k$.
       - So $d$ is determined by $k$ and the positions of $h_i=0$ (which give $d_i=2$).
       - Actually, $d$ is determined by the vector $h$.
       - Distinct $d$ from special $c$:
         - $d_i$ for $s_i=0$ is fixed to 1.
         - $d_i$ for $s_i=1$ is $2-h_i$.
         - $d_N = \sum h_i$.
         - Two different $h, h'$ produce same $d$ iff $h=h'$?
           - If $h \neq h'$, there is some $i$ with $s_i=1$ where $h_i \neq h'_i$. Then $d_i \neq d'_i$.
           - So all $2^K$ choices of $h$ produce distinct $d$ vectors?
           - Yes, because $h_i$ is directly recoverable from $d_i$ for $s_i=1$.
           - So $|S_{special}| = 2^K$.
           
     - $S_{others}$: $c \notin \{0^N, 1^N\}$.
       - For each such $c$, $A$ is unique.
       - Does $S_{special}$ overlap with $S_{others}$?
         - If $d \in S_{special}$, then for all $s_i=0$, $d_i=1$.
         - If $d \in S_{others}$, it comes from some $c \notin \{0^N, 1^N\}$.
         - If there is any $s_i=0$, then $d_i = A_i(c)$.
         - If $A_i(c) \neq 1$, then $d \notin S_{special}$.
         - If $A_i(c) = 1$ for all $s_i=0$, it's possible $d \in S_{special}$?
         - If all $s_i=1$, then $S_{special}$ has $d_i \in \{1,2\}$.
         - $S_{others}$ has $d_i = A_i + 1 - h_i$. $A_i \in \{0,1,2\}$.
         - Collision analysis is complex.
         
     - Given time, I'll implement a DP that counts distinct $d$ by iterating $c$? No, $2^N$.
     - DP on cycle:
       - State: $i$, $c_i$, and current partial sum for $d_N$? No, $d_N$ is global.
       - We need to count distinct vectors.
       
     - Alternative: The number of distinct in-degree sequences is equal to the number of valid $(c, h)$ pairs divided by collision factor?
     - Collision only between $0^N$ and $1^N$.
     - For $c \notin \{0^N, 1^N\}$, the map $h \to d$ is injective?
       - Yes, because $A$ is unique to $c$ (and $\bar{c}$ produces different $A$).
       - Wait, $A(c)$ and $A(\bar{c})$ are different.
       - So each $c \notin \{0^N, 1^N\}$ generates a set of $2^K$ vectors.
       - Do these sets overlap with each other or $S_{special}$?
       - If $s$ has a 0, $d_i=A_i$ fixes $A$. So sets for different $A$ are disjoint.
       - If all $s_i=1$, sets might overlap.
       
     - I will write a solution that handles the general case by DP.
     - DP state: `dp[i][last_c][current_d_N_partial]`? No.
     
     - Let's just output the code for the DP approach.