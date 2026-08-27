The problem can be modeled as a shortest path problem on a state graph where each state is defined by the positions of pieces A and B `(u, v)`. The initial state is `(S, T)` and the target state is `(T, S)`. A move consists of moving one piece to an adjacent vertex, provided the new positions are distinct. Since edge weights are uniform (1 operation per move), we can use Breadth-First Search (BFS) to find the minimum number of operations. The state space size is up to $N^2$, which is too large for $N=2 \times 10^5$. However, we can optimize by noting that we only care about distances. Alternatively, we can run a multi-source BFS or use the property that the minimum swaps is related to the shortest path in the original graph. A more direct approach for competitive programming constraints is to realize that if there is an alternative path or a cycle, we can "swap" pieces. Specifically, if the shortest path distance $d(S, T)$ is $D$, the answer is often $2D - 1$ or similar, but collisions matter. The robust solution is BFS on the state graph $(u, v)$ with $u \neq v$. To handle the large state space, we note that we only need to explore states reachable within a reasonable distance. However, $N^2$ is too big. Let's reconsider. The problem is equivalent to finding the shortest path in the product graph $G \times G$ excluding the diagonal. Since $N$ is up to $2 \cdot 10^5$, we cannot build the full product graph. But notice that the number of operations is small? No.
Actually, a key insight is that if the graph has a cycle or multiple paths, we can bypass collisions. If the graph is a simple path (tree), swapping is impossible if $S$ and $T$ are endpoints and the path is unique. In general, we can use BFS. But wait, $N=200,000$ means $N^2$ states is $4 \cdot 10^{10}$, which is impossible.
Let's look at the structure. We want to swap A and B. This is possible if and only if there is a path from $S$ to $T$ and a path from $T$ to $S$ that don't "block" each other permanently. In an undirected graph, this is always possible unless the graph is a simple path and $S, T$ are the only nodes? No, Sample 2 shows a single edge $1-2$ with $S=1, T=2$ fails. This is because they must cross. If there is any other vertex $C$ adjacent to the path, they can swap.
Actually, the minimum number of moves is related to the shortest path distance $D = dist(S, T)$. If there exists a vertex $C$ such that we can move one piece out of the way, the cost is $2D - 1$ or $2D + 1$?
Let's use BFS on the state space but prune aggressively? No.
Correct approach: The problem is small enough for BFS if we consider that we only need to find the shortest path in the state graph. But we can't store all states.
Wait, look at constraints again. $N, M \le 2 \cdot 10^5$.
Is there a simpler formula?
If $dist(S, T) = D$.
If there is a vertex $v$ not on the shortest path, or a cycle, we can swap.
Actually, the standard solution for this problem (AtCoder ABC 277 F? No, similar to "Swap" problems) is:
1. Calculate shortest path distances from $S$ to all nodes ($distS$) and from $T$ to all nodes ($distT$).
2. The minimum moves is $2 \cdot dist(S, T) - 1$ if there is an "escape" vertex?
Let's trace Sample 1: $S=3, T=4$. Edges: (2,4), (1,4), (3,4), (2,3).
$dist(3,4)=1$. Answer 3. $2(1)-1 = 1 \neq 3$.
Sample 3: $S=3, T=5$. Edges: (1,2), (2,3), (1,5), (2,4), (1,3), (2,5).
$dist(3,5)$: $3-2-5$ is 2. $3-1-5$ is 2. Answer 4. $2(2)=4$.
Sample 2: $S=1, T=2$. $dist=1$. Answer -1.

Hypothesis:
If the graph is a simple path (tree) and the only path between S and T is unique, and there are no other branches, it's impossible.
Generally, if there is any vertex $C$ such that we can move A to $C$ and B to $C$? No, they can't be on the same vertex.
The condition for possibility: The graph must not be a simple path where S and T are the endpoints of the unique path and there are no other nodes? No, Sample 2 is a single edge.
Actually, if $dist(S, T) = D$, the answer is $2D - 1$ if we can "swap" via a neighbor?
In Sample 1, $D=1$. Answer 3. Path: $3 \to 2$, $4 \to 3$, $3 \to 4$ (A moves to 4).
State sequence: $(3,4) \to (2,4) \to (2,3) \to (4,3)$.
Moves: 3.
Note that $2 \cdot dist(3,4) + 1 = 3$.
In Sample 3, $D=2$. Answer 4. $2 \cdot 2 = 4$.

Let's use BFS on the state graph $(u, v)$ but only visit states where $dist(u, v)$ is small? No.
Actually, we can run a BFS from $(S, T)$ to $(T, S)$. To make it efficient, we note that we only care about the shortest path. The number of states visited in BFS for shortest path in product graph is bounded by $O(M \cdot N)$ in worst case? No.
However, for this specific problem, it is known that if the graph is not a simple path (or rather, if there is a cycle or a branch), the answer is finite.
If the graph is a tree, it's impossible unless... actually, in a tree, if there is a node with degree $\ge 3$ on the path or nearby, it's possible.
Given the constraints and problem type, a BFS on the state space $(u, v)$ is the most robust, but we must optimize.
Wait, $N=200,000$. We cannot do $O(N^2)$.
But notice that we only move pieces along shortest paths? Not necessarily.
However, we can limit the BFS depth. The answer is at most $2N$?
Actually, there is a known result: The answer is $2 \cdot dist(S, T) - 1$ if there exists a vertex $C$ adjacent to the shortest path?
Let's just implement BFS on the state graph. To avoid TLE/MLE, we use a `visited` set or array. But $N^2$ array is too big. We can use a `set` or hash map for visited states, but that might be slow.
Alternatively, we can observe that we only need to explore states $(u, v)$ where $u$ is close to $S$'s target and $v$ is close to $T$'s target.
Actually, the maximum answer is not huge.
Let's try BFS with a queue. We store `(u, v)`. We use a `set` for visited.
Given the time limit (usually 2s), and $N=2 \cdot 10^5$, this might TLE if the state space is large.
But wait! If the graph is large, the diameter is small? No.
Let's look at the constraints again. $M \le 2 \cdot 10^5$.
Is there a simpler solution?
Yes. If the graph has a cycle, or a node with degree $\ge 3$, we can swap.
If the graph is a simple path, we can only swap if $S$ and $T$ are not the endpoints? No, if they are internal, we can't swap because they block each other.
Actually, if the graph is a tree, it is impossible to swap S and T if the path between them is unique and there are no "side paths" to bypass.
Specifically, if the graph is a simple path (line graph), and S and T are distinct, it is impossible if the path between them contains all nodes? No, Sample 2 is impossible.
If there is any vertex $C$ not on the shortest path between S and T, or adjacent to it, we can use it to swap.
Algorithm:
1. Compute $dist(S, T)$.
2. Check if there is a vertex $C$ such that we can "detour".
   Specifically, if there is a vertex $v$ with degree $\ge 3$ that is on the shortest path, or adjacent to the shortest path, we can swap.
   Actually, the condition for impossibility is that the graph is a simple path and S and T are the only nodes? No.
   The condition for impossibility is that the graph is a "path-like" structure where S and T are blocked.
   
   Let's stick to BFS. To optimize, we can use the fact that we only need to find the shortest path. We can use a `visited` array of size $N \times N$? No, memory error.
   We can use a `set<pair<int, int>>` for visited.
   Given the constraints and typical test cases, the number of reachable states in the shortest path BFS is often small.
   
   However, there is a better way:
   The answer is $2 \cdot dist(S, T) - 1$ if there is a "swap" opportunity.
   If no swap opportunity, -1.
   What is a swap opportunity?
   If there exists a vertex $C$ such that $C$ is adjacent to some vertex $U$ on the shortest path from $S$ to $T$, and $C$ is not on the shortest path?
   Or simply, if the graph is not a simple path?
   
   Let's implement BFS with `set` for visited. If it TLEs, we optimize. But for Python, `set` might be slow.
   
   Alternative:
   If $dist(S, T) = D$.
   If there is any vertex $v$ such that $dist(S, v) + dist(v, T) > D$? No.
   
   Let's try the BFS approach. It is the most correct.