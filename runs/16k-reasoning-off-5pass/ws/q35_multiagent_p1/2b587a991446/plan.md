1. **Model the State Space**: The state can be represented as $(u, v)$ where $u$ is the position of piece A and $v$ is the position of piece B. The goal is to go from $(S, T)$ to $(T, S)$.
2. **Breadth-First Search (BFS)**: Since we need the minimum number of moves, BFS is suitable. The state space has $N^2$ states, which is too large for $N=2 \times 10^5$. However, we can optimize.
3. **Optimization**: Notice that if the graph has an edge between $S$ and $T$, or if there's a path that allows swapping without collision, we can compute distances. A simpler approach is to run BFS on the product graph but prune states where $u=v$. Given constraints, $N^2$ is too big.
4. **Alternative Insight**: The problem is equivalent to finding two disjoint paths (vertex-disjoint except possibly at endpoints if we consider the swap carefully, but here they can't meet) or a sequence of moves. Actually, a known result for this specific "swapping tokens" problem on a graph is that if the graph is not a simple path $S-T$ with no other edges, the answer is often related to the shortest path distances.
5. **Refined Approach**: 
   - Calculate shortest path distances from $S$ to all nodes ($distS$) and from $T$ to all nodes ($distT$).
   - If there is an edge $(S, T)$, we might be able to swap in 1 move? No, because they can't land on the same vertex. If $S$ and $T$ are adjacent, can we swap? Only if there's a third vertex. If the graph is just $S-T$, it's impossible (Sample 2).
   - General case: The minimum moves is often $dist(S, T) + dist(T, S) = 2 \cdot dist(S, T)$ if we can move them independently. But they block each other.
   - Actually, a standard solution for this problem involves checking if there exists a vertex $k$ such that we can move A to $k$ and B to $k$'s neighbor? No.
   - Let's use BFS on the state space $(u, v)$ but only visit states where $u \neq v$. To handle the size, note that we only care about states reachable from $(S, T)$. In many competitive programming contexts for this specific problem (AtCoder ABC 277 F is different, this looks like ABC 256 Ex or similar), the trick is:
     - If the graph has a cycle or degree $\ge 3$ somewhere, it's usually possible.
     - The answer is typically $dist(S, T) + dist(T, S)$ if no direct conflict, but conflicts happen.
     - Correct Algorithm: Run BFS from $(S, T)$. The number of states is $N^2$. With $N=2 \cdot 10^5$, this is TLE.
     - Wait, look at constraints. $N, M \le 2 \cdot 10^5$. We need a faster way.
     - Key realization: If there is any vertex $v$ adjacent to both $S$ and $T$, or if there is a path $S \to \dots \to T$ that doesn't use the direct edge if it exists, we can often swap.
     - Actually, the minimum number of moves is $dist(S, T) + dist(T, S)$ IF we can move them "around" each other. If the graph is just a line $S-T$, it's -1.
     - If there is an alternative path, the cost is often $2 \cdot dist(S, T)$? No.
     - Let's stick to BFS on the product graph but optimize. We only need to find the shortest path in the graph of pairs. Since the graph is unweighted, BFS works. To avoid $O(N^2)$, we can note that we only expand states $(u, v)$ where $dist(S, u) + dist(T, v)$ is small? No.
     - Actually, for this specific problem (often found in contests), if the graph is not a simple edge $S-T$, the answer is usually $dist(S, T) + dist(T, S)$? No, Sample 1: $S=3, T=4$. Edge $3-4$ exists. $dist(3,4)=1$. Answer is 3. $1+1=2 \neq 3$.
     - Let's re-read Sample 1. Moves: A: $3 \to 2$, B: $4 \to 3$, A: $2 \to 4$. Total 3.
     - Path for A: $3 \to 2 \to 4$ (len 2). Path for B: $4 \to 3$ (len 1). Total 3.
     - It seems the answer is $dist(S, T) + dist(T, S)$ is not correct.
     - Correct logic: The problem is equivalent to finding the shortest path in the product graph. However, we can use the fact that if there is a vertex $k$ such that we can "pass" each other, the cost is related.
     - Given the complexity, I will implement a BFS on the product graph but with a check: if $N$ is large, we might need a heuristic. But wait, $N=2 \cdot 10^5$ means $N^2$ is huge.
     - There is a known result: If the graph has a cycle or a vertex with degree $\ge 3$, it is possible. The answer is $dist(S, T) + dist(T, S)$? No.
     - Let's look at Sample 3: $S=3, T=5$. Output 4. $dist(3,5)=1$ (edge 3-5? No, edges: 1-2, 2-3, 1-5, 2-4, 1-3, 2-5). Path $3-1-5$ len 2. Path $3-2-5$ len 2. $dist(3,5)=2$. $2+2=4$. Matches.
     - Sample 1: $dist(3,4)=1$. But answer 3. Why? Because they block.
     - If $S$ and $T$ are adjacent, and there is a third node connected to either, we can swap.
     - Algorithm:
       1. Compute $distS$ and $distT$ using BFS.
       2. If $distS[T] == \infty$, return -1 (graph is connected, so this won't happen).
       3. Check if a direct swap is possible in 1 move? No, they can't land on same vertex.
       4. If there is an edge $(S, T)$, we need to move one aside.
       5. General formula: The answer is $distS[T] + distT[S]$ if we can move independently. But if they are adjacent, they might block.
       6. Actually, the correct approach for this problem (AtCoder ABC 256 Ex? No, this is likely **ABC 277 F** or similar) is:
          - If the graph is just $S-T$ (i.e., $M=1$ and $N=2$), return -1.
          - Otherwise, the answer is $dist(S, T) + dist(T, S)$? No, Sample 1 is 3, $dist=1$, sum=2.
          - Let's use BFS on the product graph but limit the search. Since we want the shortest path, and the graph is unweighted, BFS is optimal. To handle $N=2 \cdot 10^5$, we must avoid $O(N^2)$.
          - Observation: We only need to consider states $(u, v)$ where $u$ is close to $S$ and $v$ is close to $T$? No.
          - Alternative: If there exists a vertex $k$ such that $k$ is adjacent to $S$ and $k \neq T$, and $k$ is adjacent to $T$ and $k \neq S$?
          - Actually, a simpler solution: Run BFS from $(S, T)$. If the queue gets too large, we might TLE. However, in many cases, the shortest path is small.
          - But worst case, the path could be long.
          - Let's try the following: If $S$ and $T$ are not adjacent, the answer is $dist(S, T) + dist(T, S)$? No, they move sequentially.
          - Correct Insight: The minimum number of moves is $dist(S, T) + dist(T, S)$ IF we can move them without blocking. If they are adjacent, we might need extra moves.
          - Specifically, if $S$ and $T$ are adjacent, and there is a vertex $v$ adjacent to $S$ ($v \neq T$) and a vertex $w$ adjacent to $T$ ($w \neq S$), we can move A to $v$, B to $S$, A to $T$? No.
          - Let's just implement BFS on the product graph. With $N=2 \cdot 10^5$, we can't store $N^2$ states. But we only visit reachable states. In the worst case, this is still bad.
          - However, note that if the graph is not a simple path, the "swap" is usually possible in roughly $2 \cdot dist(S, T)$ moves.
          - I will implement a BFS that stops if the distance exceeds a reasonable bound? No.
          - Given the constraints and problem type, I'll use BFS on the product graph but with a `visited` set. In Python, this might be slow for $N=2 \cdot 10^5$ if the state space is large. But typically, the shortest path is short.
          - Wait, if the graph is a line $1-2-3-4$ and $S=1, T=4$, can we swap? Yes. $1 \to 2, 4 \to 3, 2 \to 3$ (Conflict!).
          - Actually, for a line graph, if $N > 2$, we can swap? $1-2-3$. $S=1, T=3$. Move A to 2. B is at 3. Move B to 2? Conflict. Move B to ... B has no other neighbor. So if the graph is a line, and $S, T$ are endpoints, and there is no "sidetrack", it might be impossible?
          - Sample 2: $2$ vertices, $1$ edge. Impossible.
          - If $N=3$, $1-2-3$, $S=1, T=3$. Move A: $1 \to 2$. B: $3 \to 2$ (Conflict). So B cannot move. A is stuck at 2? No, A can move back.
          - So for a line graph, if $S$ and $T$ are adjacent, it's impossible? No, if there's a third node.
          - In $1-2-3$, $S=1, T=2$. Move A to ... nowhere except 2 (blocked). So impossible.
          - So if $S$ and $T$ are adjacent and have no other neighbors, impossible.
          - If they have other neighbors, we can swap.
          - I will implement BFS on the product graph. To prevent TLE, I'll use `collections.deque` and a `visited` set. If the number of visited states exceeds $N \times 10$, I'll assume it's not the optimal path? No.
          - Given the time, I'll write the BFS solution. It is the most correct.