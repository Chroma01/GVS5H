The problem asks for the minimum moves to swap two pieces on a graph without occupying the same vertex. Since the graph is connected and undirected, we can model this as a shortest path problem on a state space where a state is defined by `(pos_A, pos_B)`. However, the state space is too large ($O(N^2)$). Instead, we can observe that the pieces must traverse a path between $S$ and $T$. If the shortest path between $S$ and $T$ has length $L$, the pieces can simply swap positions if they can pass each other. They can pass each other if there exists a vertex adjacent to the path that allows one piece to wait while the other moves around, or if the path itself allows a "detour" without collision. Specifically, if the shortest path is unique and has no alternative adjacent vertices to maneuver, they might get stuck (like in Sample 2). A more robust approach is to consider the distance $d(u, v)$. The total moves will be roughly $2 \times \text{dist}(S, T)$ plus potential detours. Actually, the optimal strategy usually involves one piece moving to a neighbor of the other's path to let the other pass, or simply moving along the shortest path if no collision occurs. The key insight is that we need to find the shortest path from $(S, T)$ to $(T, S)$ in the state graph, but we can optimize by noting that the pieces effectively just need to traverse the edges of the graph. If the shortest path between $S$ and $T$ is $L$, the answer is often $2L$ unless they block each other. If they block, one must take a detour. The minimum detour involves finding a vertex $v$ adjacent to the shortest path such that moving to $v$ and back adds minimal cost. Alternatively, we can run a BFS on the state space $(u, v)$ but prune states where $u=v$. Given constraints $N, M \le 2 \cdot 10^5$, a full BFS is too slow. We must use the property that the optimal path for the pair is related to the shortest path in the original graph. The answer is $2 \times \text{dist}(S, T)$ if they don't collide. If they do collide (which happens if the shortest path is a bridge and the graph is a simple line or tree structure where no side branches exist near the path), we need to find the shortest path that avoids the collision. Actually, the condition for impossibility is when the graph is a simple path between $S$ and $T$ (a line) and there are no other edges. In that case, they can never pass. Otherwise, if there is any vertex $v$ adjacent to the shortest path (or reachable via a short detour), they can swap. The minimum moves is $2 \times \text{dist}(S, T)$ if they can pass directly. If not, they must use a longer path. The correct logic: Calculate $d = \text{dist}(S, T)$. If the graph is just a line $S \dots T$, output -1. Otherwise, the answer is $2d$ if they can pass. Wait, Sample 1: $S=3, T=4$. Path $3-4$ length 1. Moves: $3 \to 2$ (A), $4 \to 3$ (B), $2 \to 4$ (A). Total 3. $2 \times 1 = 2 \neq 3$. So the formula isn't simply $2d$.
Let's re-evaluate. The state is $(u, v)$. Start $(S, T)$, End $(T, S)$.
Transitions: $(u, v) \to (w, v)$ if $(u, w) \in E, w \neq v$. Cost 1.
$(u, v) \to (u, w)$ if $(v, w) \in E, w \neq u$. Cost 1.
This is a BFS on $N^2$ states. Too big.
However, notice that in the optimal solution, the pieces generally move along the shortest path between $S$ and $T$. Let the shortest path be $P$. If $|P| = 1$ (edge $S-T$), they are adjacent. To swap, one must move to a neighbor of $S$ or $T$. If no such neighbor exists (degree 1), impossible. If exists, say $S \to x$, then $A: S \to x$, $B: T \to S$, $A: x \to T$. Cost $1+1+1=3$.
If the shortest path is longer, say $S \to \dots \to T$. They can move towards each other. The bottleneck is when they meet. They can pass if there is a vertex adjacent to the meeting point that allows one to wait.
Actually, the standard solution for this problem (AtCoder ABC 233 F? No, similar to "Two Pieces" problems) is:
1. Find shortest path distance $D = \text{dist}(S, T)$.
2. If $D=1$ (adjacent): Check if there is any vertex adjacent to $S$ or $T$ other than each other. If yes, answer is 3. If no (both degree 1), answer -1.
3. If $D > 1$: They can always pass? Not necessarily. Consider a line $S-A-B-T$. $S \to A$, $B \to T$? No.
Let's trace Sample 1 again. $3-4$ is an edge. $D=1$. Neighbors of 3: 2, 4. Neighbors of 4: 1, 2, 3. Common neighbors? 2. So they can use 2.
General Algorithm:
Run BFS from $S$ to get distances $distS[]$.
Run BFS from $T$ to get distances $distT[]$.
The minimum moves is the shortest path in the state graph.
Since the state graph is bipartite (parity of $u+v$ changes every step), and we want min steps.
Key observation: The pieces will effectively traverse the edges of the graph. The total distance traveled by A plus total distance traveled by B is the answer.
Let the path of A be $S \to \dots \to T$ and B be $T \to \dots \to S$.
They cannot be on the same vertex.
This is equivalent to finding a path for A from $S$ to $T$ and B from $T$ to $S$ such that they don't collide and sum of lengths is minimized.
Since the graph is unweighted, we can think of this as:
Case 1: They move along the shortest path $P$ of length $D$.
If $D=1$: They are adjacent. They must detour. Cost = $1 (\text{A moves away}) + 1 (\text{B moves to S}) + 1 (\text{A moves to T}) = 3$. Condition: $\exists v$ adjacent to $S$ or $T$ such that $v \neq \text{other}$.
If $D > 1$: They can move towards each other. They will meet at some edge or vertex.
Actually, if $D > 1$, is it always possible? Yes, unless the graph is a simple path and they are blocked? No, if $D>1$, there is at least one intermediate node.
Wait, Sample 2: $1-2$. $S=1, T=2$. $D=1$. No other neighbors. Output -1.
What if $S=1, T=3$ in $1-2-3$? $D=2$.
Moves: $A: 1 \to 2$. $B: 3 \to 2$? Collision.
$A: 1 \to 2$. $B$ waits? No, B must move. $B: 3 \to 2$ collides with A at 2.
So $A$ must go $1 \to 2$, then $B$ must go $3 \to 2$? No.
Sequence:
1. $A: 1 \to 2$. State $(2, 3)$.
2. $B: 3 \to 2$? Collision.
Can $B$ go somewhere else? No, 3 only connected to 2.
So $B$ is stuck?
Wait, if $B$ cannot move, we can't proceed.
So in $1-2-3$, can we solve?
Start $(1, 3)$.
Possible moves:
- $A \to 2$: $(2, 3)$. Now $B$ at 3, only neighbor 2 (occupied). $B$ stuck.
- $B \to 2$: $(1, 2)$. Now $A$ at 1, only neighbor 2 (occupied). $A$ stuck.
So for $1-2-3$, it seems impossible?
But wait, the problem says "connected graph". $1-2-3$ is connected.
Is it impossible?
Let's re-read carefully. "Choose either piece... move... cannot make a move that results in both pieces ending up on the same vertex."
In $1-2-3$, from $(1, 3)$:
Move A to 2 -> $(2, 3)$. Valid.
From $(2, 3)$:
Move A? Neighbors of 2 are 1, 3. 3 is occupied. So A can go to 1. Back to start.
Move B? Neighbors of 3 is 2. 2 is occupied. B cannot move.
So yes, $1-2-3$ is impossible.
So the condition is: Is there a vertex $v$ adjacent to the shortest path that allows passing?
Actually, the general solution is:
Calculate $D = \text{dist}(S, T)$.
If $D=1$:
  Check if there is any vertex $v$ adjacent to $S$ or $T$ (excluding the other endpoint).
  If yes, ans = 3.
  If no, ans = -1.
If $D > 1$:
  We need to check if there is a "side path".
  Actually, if $D > 1$, we can try to move one piece to a neighbor of the shortest path to let the other pass.
  The minimum cost is usually $2 \times D$ if they can pass directly? No, in $1-2-3$, $D=2$, impossible.
  In $1-2-3-4$, $S=1, T=4$. $D=3$.
  Path $1-2-3-4$.
  $A: 1 \to 2$. $(2, 4)$.
  $B: 4 \to 3$. $(2, 3)$.
  $A: 2 \to 3$? Collision with B at 3.
  $B: 3 \to 2$? Collision with A at 2.
  Stuck?
  Wait, from $(2, 3)$, can we move?
  $A$ at 2 (neighbors 1, 3). 3 occupied. Go to 1? Back.
  $B$ at 3 (neighbors 2, 4). 2 occupied. Go to 4? Back.
  So $1-2-3-4$ is also impossible?
  This implies if the graph is a simple path, it's impossible.
  But what if there is a branch?
  $1-2-3-4$ and $2-5$.
  $S=1, T=4$.
  $A: 1 \to 2$. $(2, 4)$.
  $B: 4 \to 3$. $(2, 3)$.
  $A: 2 \to 5$. $(5, 3)$.
  $B: 3 \to 2$. $(5, 2)$.
  $A: 5 \to 2$. $(2, 2)$ Collision!
  $B: 2 \to 1$. $(5, 1)$.
  $A: 2 \to 3$. $(3, 1)$.
  $B: 1 \to 2$. $(3, 2)$.
  $A: 3 \to 4$. $(4, 2)$.
  $B: 2 \to 3$. $(4, 3)$.
  $A: 4 \to 5$? No, need to get to 4.
  Wait, goal is $A$ at $T(4)$, $B$ at $S(1)$.
  Current $(4, 3)$.
  $B: 3 \to 2$. $(4, 2)$.
  $B: 2 \to 1$. $(4, 1)$. Done.
  Moves:
  1. A: 1->2
  2. B: 4->3
  3. A: 2->5
  4. B: 3->2
  5. B: 2->1 (Wait, A is at 5, B goes 2->1. OK)
  6. A: 5->2
  7. A: 2->3
  8. B: 1->2? No, B is at 1. A is at 3.
  Let's re-simulate carefully.
  Start: A=1, B=4.
  1. A->2. (A=2, B=4).
  2. B->3. (A=2, B=3).
  3. A->5. (A=5, B=3).
  4. B->2. (A=5, B=2).
  5. B->1. (A=5, B=1). Goal for B reached? No, B needs to be at 1. Yes B is at 1. But A is at 5. Need A at 4.
  6. A->2. (A=2, B=1).
  7. A->3. (A=3, B=1).
  8. A->4. (A=4, B=1). Done.
  Total moves: 8.
  Shortest path length $D=3$. $2D = 6$. We added 2 moves for detour.
  So the logic is:
  If the graph is a simple path between S and T, impossible.
  Otherwise, possible.
  How to detect "simple path"? If the number of edges in the component containing S and T is exactly $D$, then it's a simple path.
  But wait, Sample 3: 5 vertices, 6 edges. Not a simple path.
  So algorithm:
  1. Compute $D = \text{dist}(S, T)$.
  2. Check if the subgraph induced by the shortest path is the entire component? No, just check if there is any edge not on the shortest path that connects to the shortest path vertices?
  Actually, simpler:
  Run BFS from S to get $distS$.
  Run BFS from T to get $distT$.
  The answer is the shortest path in the state graph.
  Since $N$ is large, we can't run full BFS.
  However, we know the answer is either $2D$ (if they can pass without extra moves? No, even then they might need 1 extra move to swap parity? No, parity works out).
  Wait, in Sample 1 ($D=1$), ans=3. $2D+1 = 3$.
  In Sample 3 ($S=3, T=5$).
  Edges: (1,2), (2,3), (1,5), (2,4), (1,3), (2,5).
  Path 3-1-5 (len 2). Path 3-2-5 (len 2).
  $D=2$.
  Can we do it in $2D=4$?
  Sample output says 4.
  So if $D>1$, ans = $2D$?
  Let's check $1-2-3-4$ with branch at 2.
  $D=3$. Ans was 8? $2D=6$.
  My simulation gave 8. Maybe there is a faster way?
  1. A: 1->2. (2, 4)
  2. B: 4->3. (2, 3)
  3. A: 2->5. (5, 3)
  4. B: 3->2. (5, 2)
  5. A: 5->2? No, 2 occupied.
  5. B: 2->1. (5, 1).
  6. A: 5->2. (2, 1).
  7. A: 2->3. (3, 1).
  8. A: 3->4. (4, 1).
  Total 8.
  Is 6 possible?
  To do 6, A and B must each move 3 steps.
  A: 1->2->3->4.
  B: 4->3->2->1.
  Collisions at 2 and 3.
  They must swap order.
  If A goes 1->2, B must go 4->3.
  Then A at 2, B at 3.
  Next, A must go to 3 (blocked) or back. B must go to 2 (blocked) or back.
  So they MUST detour.
  So if $D > 1$, and the graph is a simple path, impossible.
  If there is a branch, they can detour.
  The cost of detour: One piece moves to a neighbor, waits, then comes back.
  This adds 2 moves to the total count?
  In the example above, we added 2 moves (A went 2->5->2). Total 8.
  Is it always $2D + 2$?
  Or maybe $2D$ if they can pass?
  When can they pass without detour?
  Only if the graph has a cycle that allows them to bypass?
  Actually, the condition for impossibility is: The graph is a simple path between S and T.
  If not a simple path, then possible.
  What is the minimum moves?
  If $D=1$:
    If possible (has branch), ans = 3.
    Else -1.
  If $D > 1$:
    If possible (has branch), ans = $2D$? Or $2D+2$?
    In Sample 3, $D=2$, ans=4 ($2D$).
    In my $1-2-3-4$ example with branch at 2, $D=3$, ans=8 ($2D+2$).
    Why the difference?
    Sample 3: $3-1-5$ and $3-2-5$. Two disjoint paths of length 2.
    A: 3->1->5. B: 5->2->3? No, B starts at 5.
    Let's trace Sample 3 for 4 moves.
    Start (3, 5).
    1. A: 3->1. (1, 5).
    2. B: 5->2. (1, 2).
    3. A: 1->5? No, 5 is start of B, but B moved. 5 is free? Yes.
       Wait, B is at 2. 5 is free.
       A: 1->5. (5, 2).
    4. B: 2->3. (5, 3).
    5. A: 5->? Need to get to 5. A is at 5. Goal A at 5.
       Wait, goal is A at T(5), B at S(3).
       Current (5, 3). Done?
       Moves: 4.
       Sequence:
       1. A 3->1
       2. B 5->2
       3. A 1->5 (A reaches T)
       4. B 2->3 (B reaches S)
       Yes! They used two different paths.
       So if there are two disjoint paths of length $D$, ans = $2D$.
       If only one path of length $D$ exists (and branches are further away), they must detour.
       So the algorithm is:
       1. Find all shortest paths from S to T.
       2. If there are at least 2 vertex-disjoint shortest paths, ans = $2D$.
       3. If there is only 1 shortest path, check if there is a vertex on this path that has a neighbor NOT on the path (a branch).
          If yes, they can detour. Cost = $2D + 2$?
          Wait, in Sample 1 ($D=1$), ans=3. $2(1)+1 = 3$.
          In my $1-2-3-4$ example ($D=3$), ans=8. $2(3)+2 = 8$.
          So if single path, ans = $2D + 2$?
          But wait, for $D=1$, $2D+2 = 4 \neq 3$.
          Special case $D=1$: ans = 3.
          For $D > 1$:
            If multiple disjoint shortest paths: $2D$.
            If single shortest path but with branches: $2D + 2$.
            If single shortest path and no branches (simple path): -1.
       
       How to check "multiple disjoint shortest paths"?
       We can count the number of shortest paths. If count > 1, then there are at least 2?
       Not necessarily vertex disjoint. E.g., $1-2-3$ and $1-4-3$ share no vertices.
       $1-2-3$ and $1-2-4-3$? No, must be shortest.
       If there are two shortest paths, do they share vertices?
       If they share a vertex $v$, then the path is $S \to v \to T$ and $S \to v \to T$. Same path.
       So if there are $\ge 2$ shortest paths, they must be vertex disjoint (except S and T)?
       Yes, because if they shared an internal vertex, they would be the same path (since shortest paths are unique segments).
       So: Count number of shortest paths. If $>1$, ans = $2D$.
       If $=1$, check for branches.
       To check branches:
       Identify the unique shortest path $P$.
       Check if any vertex $v \in P$ has a neighbor $u \notin P$.
       If yes, ans = $2D + 2$.
       If no, ans = -1.
       Exception: $D=1$.
       If $D=1$:
         Check if $S$ or $T$ has a neighbor other than each other.
         If yes, ans = 3.
         Else -1.
       
       Let's verify Sample 1: $D=1$. Neighbors of 3: 2, 4. 4 is T. 2 is other. Yes. Ans 3. Correct.
       Sample 2: $D=1$. Neighbors of 1: 2. Neighbors of 2: 1. No other. Ans -1. Correct.
       Sample 3: $D=2$. Paths: 3-1-5, 3-2-5. Two paths. Ans $2*2=4$. Correct.
       My $1-2-3-4$ with branch at 2:
       Shortest path: 1-2-3-4. Unique.
       Vertex 2 has neighbor 5 (not on path).
       So ans = $2*3 + 2 = 8$. Correct.
       
       Algorithm refined:
       1. BFS from S to get $distS$.
       2. BFS from T to get $distT$.
       3. $D = distS[T]$.
       4. If $D == -1$: return -1 (should not happen as connected).
       5. If $D == 1$:
            Check if degree(S) > 1 or degree(T) > 1.
            If yes, return 3.
            Else return -1.
       6. If $D > 1$:
            Count number of shortest paths.
            We can do this by DP or BFS counting.
            Since $N$ is large, we need to be careful with modulo? No, we just need to know if $>1$.
            We can run a BFS from S and count paths, but if count exceeds 1, stop.
            Actually, we need to know if there is more than one path.
            We can compute the number of shortest paths modulo a large prime? Or just boolean flag.
            Let `cnt[u]` be number of shortest paths from S to u.
            `cnt[S] = 1`.
            Iterate in BFS order. For each edge $(u, v)$ where $distS[u] + 1 == distS[v]$, `cnt[v] += cnt[u]`.
            If `cnt[v] > 1`, mark as multiple.
            After computing for all nodes, check `cnt[T]`.
            If `cnt[T] > 1`: return $2*D$.
            Else (unique path):
               Reconstruct the unique shortest path.
               Check if any vertex on this path has a neighbor not on the path.
               If yes: return $2*D + 2$.
               Else: return -1.
               
       Wait, is it possible that `cnt[T] > 1` but all paths share a vertex?
       As argued, shortest paths from S to T cannot share an internal vertex and be distinct.
       Proof: If they share $v$, then $S \to v$ is a prefix. The suffix $v \to T$ must be the same for both to be shortest?
       Suppose $P1 = S \to \dots \to v \to \dots \to T$ and $P2 = S \to \dots \to v \to \dots \to T$.
       If the segments after $v$ differ, then $dist(v, T)$ would be different? No, $dist(v, T)$ is fixed.
       But the path from $v$ to $T$ must be a shortest path.
       If there are multiple shortest paths from $v$ to $T$, then `cnt[T]` will be $>1$.
       But do they share vertices?
       Example: $v$ connected to $x$ and $y$, both connected to $T$.
       $v-x-T$ and $v-y-T$.
       These are disjoint after $v$.
       So yes, if `cnt[T] > 1`, there are at least two vertex-disjoint paths (except possibly S and T).
       So the logic holds.

       Implementation details:
       - BFS for distances.
       - BFS/DP for counting paths (capped at 2).
       - If unique, reconstruct path using parent pointers.
       - Check neighbors of path nodes.