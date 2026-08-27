1.  **Model the State Space**: The state is defined by the positions of piece A $(u)$ and piece B $(v)$. Since $A$ and $B$ cannot occupy the same vertex, valid states are pairs $(u, v)$ with $u \neq v$. The goal state is $(T, S)$.
2.  **Breadth-First Search (BFS)**: We need the minimum number of operations, so BFS is appropriate. The initial state is $(S, T)$.
3.  **Transitions**: From state $(u, v)$, we can move A to any neighbor $u'$ of $u$ (provided $u' \neq v$) resulting in state $(u', v)$, or move B to any neighbor $v'$ of $v$ (provided $v' \neq u$) resulting in state $(u, v')$.
4.  **Complexity**: The number of states is $O(N^2)$, which is too large for $N=2 \cdot 10^5$. However, notice that in each step, only one piece moves. The total distance is roughly $dist(S, T) + dist(T, S) = 2 \cdot dist(S, T)$ if they could swap directly. But they block each other.
5.  **Optimization**: Instead of full $N^2$ BFS, observe that the problem is equivalent to finding a path for A from S to T and a path for B from T to S such that they don't collide. A simpler approach often used in competitive programming for this specific "two tokens" problem is to run BFS on the product graph but prune aggressively or use the fact that the graph is unweighted. However, $N^2$ is definitely too big.
6.  **Re-evaluation**: Wait, standard BFS on $N^2$ states is $O(N^2)$ which TLEs. We need a better approach.
    *   Actually, let's look at the constraints again. $N, M \le 2 \cdot 10^5$.
    *   Is there a simpler condition? If the graph is a simple path $S - \dots - T$, and there are no other edges, they might get stuck (Sample 2).
    *   Key Insight: The pieces can swap if there is an alternative path. Specifically, if there exists a vertex $k$ such that $dist(S, k) + dist(k, T) > dist(S, T)$ is not the right metric.
    *   Let's consider the BFS on the product graph but limit the search. Actually, many similar problems can be solved by checking if there is a "detour".
    *   Alternative Idea: The minimum moves is $2 \cdot dist(S, T)$ if they can just pass each other. When can they pass? If there is a vertex $w$ adjacent to the edge $(u, v)$ on the shortest path? No.
    *   Correct Approach for Large N: The state space is indeed large, but we only care about the shortest path.
    *   Let $d_S[u]$ be the shortest distance from $S$ to $u$, and $d_T[u]$ be the shortest distance from $T$ to $u$.
    *   If there is a path for A and a path for B that don't intersect at the same time step, we are good.
    *   Actually, a known result for this problem (ABC 256 F or similar) is that if the graph has a cycle or sufficient connectivity, the answer is $2 \cdot dist(S, T)$. If the graph is a simple line (tree) and S and T are endpoints of a bridge-like structure, it might be impossible.
    *   Let's stick to BFS but optimize. We can use 0-1 BFS or just standard BFS. But $N^2$ is too big.
    *   Wait, is it possible that the answer is always $2 \cdot dist(S, T)$ unless it's impossible?
    *   Sample 2: 1-2. Dist(1,2)=1. Answer -1.
    *   Sample 1: 3-4. Edges: (2,4), (1,4), (3,4), (2,3). Dist(3,4)=1. Answer 3. $2 \cdot 1 = 2 \neq 3$.
    *   So it's not always $2 \cdot dist$.
    *   Let's look at Sample 1 again. A:3->2, B:4->3, A:2->4. Total 3.
    *   Path for A: 3->2->4. Path for B: 4->3.
    *   They swapped.
    *   If we can't swap directly, we need a detour.
    *   Algorithm: Run BFS from S to get $d_S[\cdot]$ and from T to get $d_T[\cdot]$.
    *   The answer is likely related to $d_S[T]$.
    *   If there exists a vertex $v$ such that $d_S[v] + d_T[v] == d_S[T]$ and $v$ has a neighbor $w$ with $w \neq v$ such that $d_S[w] + d_T[w] == d_S[T]$? No.
    *   Let's use the property: If there is an edge $(u, v)$ on *some* shortest path from S to T, and there is another path that allows "passing", the cost is low.
    *   Actually, the most robust solution for $N=2 \cdot 10^5$ is to realize that if the graph is not a simple path between S and T (i.e., there is a cycle involving the path or an alternative route), the pieces can maneuver.
    *   Specific Logic:
        1. Compute $d_S[u]$ and $d_T[u]$ for all $u$.
        2. Let $D = d_S[T]$.
        3. If there is no path, return -1 (graph is connected, so path exists).
        4. Check if it's impossible. It is impossible if and only if $N=2$ and $M=1$ (Sample 2). Or more generally, if the only path is a simple edge and they block each other.
        5. Actually, Sample 2 is impossible because they are on adjacent vertices and the only move for A is to T (occupied) and B is to S (occupied).
        6. In general, if $d_S[T] == 1$ (adjacent), they need to swap. If they are adjacent, A wants to go to T (occupied) and B wants to go to S (occupied). One must move away. If there is a neighbor $u$ of S ($u \neq T$) and a neighbor $v$ of T ($v \neq S$), they can move out and swap.
        7. General Formula: The answer is $2 \cdot D$ if there is a "detour" available. If not, it might be $2 \cdot D + 2$ or impossible.
        8. Let's implement a BFS on the product graph but with a twist: We only expand states that are "close" to the shortest path? No, that's risky.
        9. Given the constraints and problem type, a full BFS on $N^2$ is TLE. However, note that we only care about the shortest path.
        10. There is a known solution:
            - Calculate $d_S$ and $d_T$.
            - If $d_S[T]$ is the shortest distance.
            - If there exists a vertex $v$ such that $d_S[v] + d_T[v] == d_S[T]$ and $v$ has a neighbor $w$ such that $d_S[w] + d_T[w] == d_S[T]$ and $w \neq v$? This checks for parallel edges on the shortest path DAG.
            - Actually, if there is *any* cycle in the graph that intersects the shortest path, or if there are multiple shortest paths, the answer is $2 \cdot d_S[T]$.
            - If the shortest path is unique and is a simple path with no alternative edges (i.e., the graph is a tree along the path), then we might need extra steps.
            - Let's try a different angle: BFS from $(S, T)$. To avoid $O(N^2)$, we can use the fact that the optimal path will likely stay close to the shortest path between S and T.
            - However, a simpler observation: If $N > 2$ or $M > N-1$, is it always possible? Sample 2 is $N=2, M=1$.
            - If $N=2, M=1$, output -1.
            - Otherwise, is the answer always $2 \cdot d_S[T]$?
            - Sample 1: $d_S[T] = 1$. Answer 3. $2 \cdot 1 = 2 \neq 3$. So no.
            - Why 3? A:3->2, B:4->3, A:2->4.
            - Distances: $d_3[2]=1, d_3[3]=0, d_3[4]=1$. $d_4[2]=1, d_4[3]=1, d_4[4]=0$.
            - The "detour" cost adds 1 move for each piece?
            
    Let's write a BFS that is optimized. We can use a `visited` set for pairs. But we must limit the depth. The maximum shortest path is $N$. The BFS depth won't exceed $2N$. The number of reachable states might still be large.
    
    Actually, there is a specific condition for impossibility: If the graph is a simple path $S-T$ and they are adjacent, they block. If they are not adjacent, they can move towards each other?
    
    Let's use the following robust strategy:
    1. Run BFS from S to get $d_S$.
    2. Run BFS from T to get $d_T$.
    3. If $d_S[T]$ is infinity, return -1.
    4. Check if it is impossible. It is impossible if and only if $S$ and $T$ are connected by a single edge and there are no other vertices? No, Sample 2 is the only case with -1 in small examples.
    5. Actually, if $N=2$ and $M=1$, return -1.
    6. For all other cases, is the answer $2 \cdot d_S[T]$?
       - Sample 1: $d_S[T]=1$. Ans=3.
       - Sample 3: $N=5, M=6, S=3, T=5$.
         Edges: 1-2, 2-3, 1-5, 2-4, 1-3, 2-5.
         $d_3$: 3->2 (1), 3->1 (1). 2->4 (2), 2->5 (2), 1->5 (2).
         $d_3[5] = 2$ (via 3-1-5 or 3-2-5).
         Ans=4. $2 \cdot 2 = 4$. Matches.
       
    Why is Sample 1 different?
    In Sample 1, $S=3, T=4$. Edge 3-4 exists.
    $d_3[4]=1$.
    If we try to do it in 2 moves:
    Move A: 3->4 (Blocked by B).
    Move B: 4->3 (Blocked by A).
    So they can't swap directly.
    One must move aside.
    A: 3->2. B: 4->3. A: 2->4. (3 moves).
    
    Hypothesis:
    - If $d_S[T] == 1$:
      - If there is a neighbor of S ($u \neq T$) and a neighbor of T ($v \neq S$) such that we can move A to $u$ and B to $v$?
      - Actually, if $S$ and $T$ are adjacent, we need to check if there is an alternative path.
      - If $deg(S) > 1$ or $deg(T) > 1$, we can likely do it in $2 \cdot d_S[T] + 1$? No, Sample 1 is 3. $2(1)+1=3$.
      - If $deg(S)==1$ and $deg(T)==1$ and $N=2$, impossible.
    - If $d_S[T] > 1$:
      - The pieces can move towards each other without blocking because they are not adjacent initially?
      - If they are not adjacent, A moves S->... and B moves T->...
      - They might meet in the middle. If the shortest path is unique and is a simple line, they might block at the last step.
      - However, if $d_S[T] > 1$, usually the answer is $2 \cdot d_S[T]$.
      
    Let's refine:
    1. Compute $d_S$ and $d_T$.
    2. If $d_S[T]$ is inf, return -1.
    3. If $S$ and $T$ are adjacent ($d_S[T] == 1$):
       - If $N=2$ and $M=1$, return -1.
       - Else, return $2 \cdot d_S[T] + 1$? i.e., 3?
       - Let's check if there's a case where it's 2? No, because they block.
       - Is it always 3 if possible?
       - What if $S$ and $T$ are adjacent, but there is a triangle? S-T, S-U, T-U.
         A:S, B:T.
         A:S->U. B:T->U (Blocked).
         A:S->U. B:T->S (Blocked).
         A:S->U. B:T->? If T has other neighbors.
         If T only connects to S and U, and S only connects to T and U.
         A:S->U. B:T->U (Blocked).
         So A must go to U. B must go to... if B goes to S, blocked.
         So B must go to a neighbor other than S. If T only has S and U, B is stuck?
         Wait, if B goes to U, it's blocked by A.
         So if the graph is just a triangle S-T-U-S, and A=S, B=T.
         1. A moves to U. State (U, T).
         2. B moves to U? Blocked. B moves to S? Blocked.
         So B is stuck?
         No, B can move to U if A is not there. But A is at U.
         So in a triangle, if A=S, B=T, and they are adjacent, can they swap?
         A:S->U. Now A=U, B=T.
         B needs to go to S. Path T->S is blocked. T->U->S?
         B:T->U? Blocked by A.
         So B cannot move to U.
         So B is stuck?
         Then A must move. A:U->T? Blocked by B. A:U->S? Blocked? No, S is empty.
         A:U->S. Back to start.
         So in a triangle, they cannot swap?
         Let's trace:
         Start: A=S, B=T.
         Move 1: A->U. State (U, T).
         Move 2: B cannot move to S (adjacent to T? Yes, edge T-S exists). But is S adjacent to T? Yes.
         Wait, B is at T. Neighbors of T are S and U.
         S is empty? Yes.
         U is occupied by A.
         So B can move to S!
         State (U, S).
         Move 3: A is at U. Neighbors S, T.
         S is occupied by B.
         T is empty.
         A moves to T. State (T, S).
         Goal reached in 3 moves.
         So even in a triangle, it's 3 moves.
         
    So, if $d_S[T] == 1$:
    - If impossible (N=2, M=1), return -1.
    - Else, return 3.
    
    If $d_S[T] > 1$:
    - Is it always $2 \cdot d_S[T]$?
    - Consider a line 1-2-3-4. S=1, T=4. Dist=3.
    - A:1, B:4.
    - 1. A:1->2. (2,4)
    - 2. B:4->3. (2,3)
    - 3. A:2->3? Blocked. A:2->1? Back.
    - B:3->2? Blocked. B:3->4? Back.
    - Stuck?
    - Wait, in step 2, if A moves to 2, B is at 4.
    - Can B move to 3? Yes. State (2,3).
    - Now A is at 2, B is at 3. They are adjacent.
    - A wants to go to 4. B wants to go to 1.
    - They are blocked.
    - So they need to detour. But there is no detour (Line graph).
    - So it is impossible?
    - If the graph is a simple path and they are at ends, they block in the middle.
    - So if the graph is a tree (specifically a path) and the shortest path is unique, it might be impossible.
    
    Condition for impossibility:
    - If the shortest path between S and T is unique and is a simple path, and there are no "side" edges to detour, they will block.
    - Specifically, if $d_S[T] == k$, and there is only one path, they meet at $k/2$.
    - If $k$ is odd, they end up on adjacent vertices blocking each other.
    - If $k$ is even, they end up on the same vertex? No, they move alternately.
    
    Actually, the condition is:
    - If there is ANY cycle or alternative path, answer is $2 \cdot d_S[T]$.
    - If the shortest path is unique and is a simple path (no other edges connect vertices on the path to each other or off the path in a way that allows bypassing), then it is IMPOSSIBLE if $d_S[T]$ is odd? Or always impossible if it's a simple line?
    
    Let's check Sample 2: 1-2. Dist=1. Odd. Impossible.
    Line 1-2-3-4. S=1, T=4. Dist=3. Odd.
    Can they swap?
    A:1->2, B:4->3. State (2,3). Blocked.
    If A goes back, no progress.
    So Impossible.
    
    Line 1-2-3. S=1, T=3. Dist=2. Even.
    A:1, B:3.
    1. A:1->2. State (2,3).
    2. B:3->2? Blocked.
    3. A:2->3? Blocked.
    Stuck.
    So even in even distance, if it's a simple line, they block.
    
    So, if the graph is a simple path between S and T (i.e., the shortest path is unique and there are no other edges that provide a detour), it is IMPOSSIBLE.
    
    How to check if there is a detour?
    - If there is an edge $(u, v)$ such that $d_S[u] + 1 + d_T[v] == d_S[T]$ and $d_S[v] + 1 + d_T[u] == d_S[T]$? This indicates a "parallel" edge on the shortest path DAG.
    - Or if there is a vertex $w$ not on the shortest path that connects two vertices on the shortest path?
    
    Simplified Logic:
    1. Compute $d_S$ and $d_T$.
    2. If $d_S[T]$ is inf, -1.
    3. If $N=2$ and $M=1$, -1.
    4. Check if there is a "detour". A detour exists if there is an edge $(u, v)$ such that $d_S[u] + 1 + d_T[v] == d_S[T]$ is NOT the only way, or rather, if there is a vertex on the shortest path that has a neighbor not on the shortest path, or two vertices on the shortest path are connected by an edge not in the path?
    
    Actually, a simpler check:
    If there exists a vertex $v$ such that $d_S[v] + d_T[v] == d_S[T]$ and $v$ has a neighbor $w$ such that $d_S[w] + d_T[w] == d_S[T]$ and $w \neq v$? No.
    
    Let's just use BFS on the product graph but prune.
    Since we want min moves, and max answer is likely small ($2N$), we can run BFS.
    To avoid $O(N^2)$, we note that we only visit states $(u, v)$ where $d_S[u] + d_T[v] \approx d_S[T]$? No.
    
    Given the complexity, I will implement the BFS with a `visited` set. For $N=2 \cdot 10^5$, if the graph is dense, BFS might be slow. But if the graph is sparse, the number of reachable states in the "shortest path corridor" is small.
    
    However, to be safe and correct, I'll use the following heuristic which is known to work for this problem (AtCoder ABC 256 F is different, but this is a classic):
    
    If $d_S[T] == 1$:
       If $N==2$ and $M==1$: return -1
       Else: return 3
    Else:
       If there is a detour: return $2 * d_S[T]$
       Else: return -1
       
    How to check detour?
    Detour exists if there is an edge $(u, v)$ such that $d_S[u] + 1 + d_T[v] == d_S[T]$ AND $d_S[v] + 1 + d_T[u] == d_S[T]$? No, that's for parallel edges.
    
    Detour exists if there is a vertex $x$ on the shortest path (i.e., $d_S[x] + d_T[x] == d_S[T]$) that has a neighbor $y$ such that $d_S[y] + d_T[y] == d_S[T]$? No.
    
    Detour exists if there is an edge $(u, v)$ such that $|d_S[u] - d_S[v]| == 1$ is not the only constraint?
    
    Actually, if there is ANY edge $(u, v)$ such that $d_S[u] + 1 + d_T[v] == d_S[T]$ and $d_S[v] + 1 + d_T[u] == d_S[T]$ is false?
    
    Let's just run BFS. If it TLEs, we optimize. But Python might be slow.
    
    I will write a BFS solution.