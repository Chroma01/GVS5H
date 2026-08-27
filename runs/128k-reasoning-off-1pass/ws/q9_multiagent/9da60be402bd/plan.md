We will model the problem using a shortest path algorithm on a graph where nodes represent states of a palindrome being built. Since we need the shortest palindrome path between all pairs, we can run a multi-source BFS (or Dijkstra, since edge weights are 1) from all possible "center" states. A palindrome can be viewed as expanding outwards from a center: either a single character (odd length) or a gap between characters (even length). We will construct a state graph where a state is defined by `(u, v, len, side)`, representing that we have matched a prefix of length `len` starting from `u` going forward and `v` going backward (or vice versa depending on perspective), but a more efficient approach for "all pairs" is to reverse the problem: for every possible center (a vertex for odd length, or an edge for even length), run a BFS to find the shortest path to all other vertices that forms a palindrome. However, given $N \le 100$, an $O(N^4)$ or $O(N^5)$ approach is acceptable. A robust method is to consider all possible centers: for each vertex $i$, treat it as the center of an odd-length palindrome and run BFS; for each edge $(i, j)$, treat it as the center of an even-length palindrome and run BFS. In the BFS, we maintain the current "head" and "tail" vertices and the current length. We transition by moving the head forward with character $c$ and the tail backward with character $c$. Since we need the shortest path for *all* pairs, we can initialize the BFS queue with all possible centers simultaneously and track the distance to reach state $(start, end)$. Actually, a simpler unified approach: Create a state $(u, v)$ representing that we are currently at vertex $u$ looking for the next character to match the character we will eventually pick at vertex $v$ (conceptually, we are building the palindrome from both ends inwards, but since we need the path from $i$ to $j$, let's flip the logic).
Correct Logic: We want path $i \to \dots \to j$ with label $S$ where $S$ is a palindrome. Let $S = c_1 c_2 \dots c_k$. Then $c_1 = c_k, c_2 = c_{k-1}$, etc. We can run a BFS where the state is $(u, v)$, representing that the current unmatched prefix starts at $u$ and the current unmatched suffix ends at $v$. Initially, for a specific target pair $(i, j)$, this is hard. Instead, we iterate over all possible "centers".
1. **Odd Length Palindromes**: Center is a vertex $x$. The path starts at $x$ (length 0) and expands. State: $(u, v)$ means we have matched a path from $x$ to $u$ (forward) and from $x$ to $v$ (backward? No).
Let's refine: We want to find shortest path $i \to j$ with palindrome label.
Let the palindrome be $P$. $P = p_1 p_2 \dots p_L$. $p_1$ is the edge leaving $i$, $p_L$ is the edge entering $j$. $p_1 = p_L, p_2 = p_{L-1}$, etc.
We can run a BFS where the state is $(u, v)$, representing that we have successfully matched a palindrome prefix of length $k$ starting at $i$ and ending at some intermediate node, and a palindrome suffix of length $k$ ending at $j$ and starting at some intermediate node? No.
Standard technique for "shortest palindrome path":
Run a BFS on the state space $(u, v)$ where $u$ is the current vertex in the forward direction and $v$ is the current vertex in the backward direction.
Wait, the start and end points $i$ and $j$ are fixed for the query, but we need all pairs.
Alternative: Since $N$ is small, we can iterate over all possible centers.
Case 1: Odd length palindrome. Center is a vertex $c$. The path goes $i \to \dots \to c \to \dots \to j$. The part $i \to c$ and $c \to j$ must be reverse of each other in terms of labels.
Case 2: Even length palindrome. Center is an edge $(c_1, c_2)$. The path goes $i \to \dots \to c_1 \to c_2 \to \dots \to j$. The part $i \to c_1$ and $c_2 \to j$ must be reverse.
Algorithm:
Initialize `dist[i][j] = infinity`.
For each vertex $c$ (potential center for odd length):
  Run BFS starting with state $(c, c)$ and distance 0.
  State $(u, v)$ means we have a path from $c$ to $u$ with label $S$ and a path from $c$ to $v$ with label $S^R$ (reverse of $S$). Wait, this doesn't directly give $i \to j$.
Let's try the "expand from both ends" approach for all pairs simultaneously.
State: $(u, v)$ represents that we have matched a palindrome of length $L$ such that the forward path starts at some $i$ and ends at $u$, and the backward path starts at $v$ and ends at some $j$? No, $i$ and $j$ are variables.
Let's fix the definition: We want to find the shortest path from $i$ to $j$ with palindrome label.
Let's consider the palindrome $P$. $P = x_1 x_2 \dots x_k$.
$x_1$ is the label of edge $i \to u_1$.
$x_k$ is the label of edge $u_{k-1} \to j$.
$x_1 = x_k$.
$x_2$ is label $u_1 \to u_2$.
$x_{k-1}$ is label $u_2 \to j$? No, $x_{k-1}$ is label $u_{k-2} \to u_{k-1}$.
This implies we are matching edges from the start and end inwards.
State: $(u, v)$ where $u$ is the current vertex reached from the start $i$, and $v$ is the current vertex reached from the end $j$ (traversing backwards).
But $i$ and $j$ vary.
Idea: Run BFS from all possible "centers" simultaneously.
1. **Odd Centers**: For each vertex $c$, initialize a BFS with state $(c, c)$ and length 0. This represents a palindrome of length 0 centered at $c$.
   Transitions: From state $(u, v)$ with length $L$, we can move to $(next(u, char), prev(v, char))$ if there is an edge $u \to next$ with label $char$ and an edge $prev \to v$ with label $char$.
   Wait, the direction matters.
   If we are at $(u, v)$, it means we have a path $c \to \dots \to u$ with label $S$ and a path $v \to \dots \to c$ with label $S^R$.
   To extend, we need an edge $u \to u'$ with label $c$ and an edge $v' \to v$ with label $c$.
   Then we have path $c \to \dots \to u \to u'$ (label $S+c$) and $u' \to \dots \to v \to v'$? No.
   Let's re-orient.
   We want path $i \to j$.
   Let's define state $(u, v)$ as: we have matched a palindrome prefix $P$ starting at $i$ ending at $u$, and a palindrome suffix $P^R$ ending at $j$ starting at $v$.
   This requires knowing $i$ and $j$.
   
   Better approach:
   Since we need the answer for ALL pairs $(i, j)$, we can iterate over all possible "centers" of the palindrome.
   A palindrome has a center which is either a vertex (odd length) or an edge (even length).
   **Odd Length**: Center is vertex $k$. The path is $i \to \dots \to k \to \dots \to j$. The segment $i \to k$ has label $S$, and $k \to j$ has label $S^R$.
   **Even Length**: Center is edge $(k, l)$. The path is $i \to \dots \to k \to l \to \dots \to j$. The segment $i \to k$ has label $S$, and $l \to j$ has label $S^R$.
   
   Algorithm:
   Initialize `ans[N][N]` with infinity.
   **Step 1 (Odd)**: For each vertex $k$ from 1 to $N$:
     Run BFS starting with state $(k, k)$ and length 0.
     State $(u, v)$ means: we have a path from $k$ to $u$ with label $S$, and a path from $v$ to $k$ with label $S^R$.
     Wait, if we have path $k \to u$ ($S$) and $v \to k$ ($S^R$), then the combined path $u \to \dots \to k \to \dots \to v$ is a palindrome $S + S^R$? No.
     Path $k \to u$ is $S$. Path $v \to k$ is $S^R$.
     If we reverse the second path, it becomes $k \to v$ with label $S$.
     So we have two paths from $k$: to $u$ (label $S$) and to $v$ (label $S$).
     This doesn't help form $i \to j$.
     
     Let's flip the state definition for the BFS originating from center $k$:
     State $(u, v)$: Path $k \to u$ has label $S$, Path $v \to k$ has label $S^R$.
     Actually, we want to connect $i \to k$ and $k \to j$.
     Let's define state $(u, v)$ as: Path $u \to k$ has label $S$, Path $k \to v$ has label $S^R$.
     Initial state: $(k, k)$, length 0.
     Transitions: From $(u, v)$, we want to extend the palindrome.
     We need to add a character $c$ to the beginning of $S$ (so $u \to u'$ with $c$) and to the end of $S^R$ (so $v \to v'$ with $c$).
     Wait, $S^R$ is the label of $k \to v$. If we add $c$ to the end of $S^R$, the new path is $k \to v \to v'$ with label $S^R + c$.
     The new prefix is $u' \to u \to k$ with label $c + S$.
     For the whole thing to be a palindrome, we need the new total string to be a palindrome.
     Current total string from $u'$ to $v'$ via $k$ is $(c+S) + (S^R+c) = c + S + S^R + c$.
     This is a palindrome if $S + S^R$ is a palindrome (which it is) and the outer chars match ($c=c$).
     So, transition: If there is edge $u' \to u$ with label $c$ and edge $v \to v'$ with label $c$, then from state $(u, v)$ we go to $(u', v')$ with length $L+2$.
     Wait, the edges are directed.
     We need path $u' \to u$ (label $c$) and path $v \to v'$ (label $c$).
     Then the path $u' \to \dots \to k \to \dots \to v'$ has label $c + S + S^R + c$.
     The start node is $u'$, end node is $v'$.
     So `ans[u'][v'] = min(ans[u'][v'], L+2)`.
     Also, we need to consider the case where the palindrome is just the single character $c$ (length 1).
     This corresponds to $u=k, v=k$, and we find edge $k \to k$ with label $c$? No, that's a self loop.
     Or $u=k, v=k$ and we take edge $k \to x$ with $c$ and edge $x \to k$ with $c$? That's length 2.
     What about length 1? Path $i \to j$ with label $c$. Center is the edge $(i, j)$.
     
     **Step 2 (Even)**: For each edge $(u, v)$ with label $c$:
       This edge forms the center of an even length palindrome.
       The path is $i \to \dots \to u \to v \to \dots \to j$.
       Label: $S + c + S^R$.
       We need path $u \to \dots \to i$ with label $S^R$ (so $i \to \dots \to u$ is $S$) and path $v \to \dots \to j$ with label $S^R$ (so $j \to \dots \to v$ is $S$).
       Wait, if path $i \to u$ is $S$, and path $v \to j$ is $S^R$, then total is $S + c + S^R$.
       For this to be a palindrome, $S$ must be the reverse of $S^R$, which is always true.
       So we need path $i \to u$ with label $S$ and path $v \to j$ with label $S^R$.
       This is symmetric to the odd case.
       We can run a BFS from the "center edge" $(u, v)$.
       State $(x, y)$: Path $x \to u$ has label $S$, Path $v \to y$ has label $S^R$.
       Initial state: $(u, v)$, length 0 (just the edge $u \to v$).
       Transitions: Find $x' \to x$ with $c$ and $y \to y'$ with $c$.
       New state $(x', y')$, length $L+2$.
       Update `ans[x'][y']`.
       
     **Step 3 (Single Edge)**:
     For every edge $u \to v$ with label $c$, the path of length 1 is valid.
     `ans[u][v] = min(ans[u][v], 1)`.
     
     **Step 4 (Single Vertex)**:
     Path of length 0 from $i$ to $i$ is valid.
     `ans[i][i] = 0`.
     
     **Refining the BFS**:
     We have $N$ vertices and $N^2$ potential edges.
     Total centers: $N$ (odd) + $N^2$ (even).
     For each center, we run a BFS.
     State space size: $N \times N$.
     Transitions: Iterate over incoming edges to $u$ and outgoing from $v$?
     Actually, from state $(u, v)$, we need to find $u'$ such that $u' \to u$ exists, and $v'$ such that $v \to v'$ exists, with same label.
     We can precompute adjacency lists `adj[u][char]` and `rev_adj[v][char]` (incoming edges).
     For each center, BFS:
       Queue $Q$.
       While $Q$ not empty:
         Pop $(u, v, dist)$.
         For each char $c$ in 'a'-'z':
           Find $u'$ such that $u' \to u$ has label $c$.
           Find $v'$ such that $v \to v'$ has label $c$.
           If both exist and $(u', v')$ not visited:
             Push $(u', v', dist+2)$.
             Update `ans[u'][v']`.
             
     Complexity:
     Centers: $O(N^2)$.
     BFS per center: $O(N^2 \cdot \Sigma)$ where $\Sigma=26$.
     Total: $O(N^4 \cdot \Sigma)$. With $N=100$, $10^8 \cdot 26 \approx 2.6 \cdot 10^9$, which is too slow for 2 seconds.
     We need a more efficient way.