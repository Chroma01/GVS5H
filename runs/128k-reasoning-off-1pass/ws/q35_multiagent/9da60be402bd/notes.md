
## ideation
The problem asks for the shortest path length between every pair of nodes $(i, j)$ such that the concatenation of edge labels forms a palindrome.
Key observations:
1. A path of length 0 from $i$ to $i$ is an empty string, which is a palindrome. So $A_{i,i} = 0$.
2. A path of length 1 from $i$ to $j$ (if an edge exists) is a single character, which is always a palindrome. So if there is an edge $i \to j$, $A_{i,j} \le 1$.
3. For longer paths, a palindrome reads the same forwards and backwards. This means if we build the path from both ends, the first and last characters must match, the second and second-to-last must match, etc.
4. We can model this using a BFS on the state space of pairs $(u, v)$, representing that we have found a palindrome path from $u$ to $v$. The "distance" in this BFS will correspond to the length of the palindrome path.
5. Specifically, if we have a palindrome path from $u$ to $v$ of length $L$, and there is an edge $a \to u$ with label $c$ and an edge $v \to b$ with label $c$, then we can form a palindrome path from $a$ to $b$ of length $L+2$.
6. We initialize the BFS with:
   - All $(i, i)$ with distance 0.
   - All $(i, j)$ where there is an edge $i \to j$ with distance 1. Note: If $i=j$ and there's a self-loop, the distance is 0 (empty path) which is shorter than 1, so we keep 0.
7. We run a multi-source BFS. The state is $(u, v)$. For each state $(u, v)$ with current distance $d$, we look for all pairs of edges $(a \to u)$ and $(v \to b)$ such that the label of $a \to u$ equals the label of $v \to b$. If we haven't visited $(a, b)$ yet, we set its distance to $d+2$ and add it to the queue.
8. Since we want the shortest path, BFS guarantees that the first time we reach a state $(a, b)$, it is via the shortest palindrome path.
9. The number of states is $N^2$. For each state, we iterate over incoming edges to $u$ and outgoing edges from $v$. In the worst case, this is $O(N^2)$ per state, leading to $O(N^4)$ total time. With $N=100$, $N^4 = 10^8$, which might be tight but acceptable in Python if optimized, or we can optimize by grouping edges by label.
10. Optimization: Instead of iterating all incoming/outgoing edges, we can precompute for each node and label, the list of predecessors (for incoming) and successors (for outgoing). Then for a state $(u, v)$, we iterate over each label $c \in \{'a', \dots, 'z'\}$, get the list of predecessors of $u$ with label $c$ and successors of $v$ with label $c$, and for each pair $(a, b)$, if $(a, b)$ is unvisited, set distance and enqueue. This reduces the inner loop to be proportional to the number of edges with matching labels, which is more efficient in practice.

Pitfalls:
- Self-loops: A self-loop $i \to i$ with label $c$ creates a palindrome of length 1. But the empty path (length 0) is shorter. So $A_{i,i}$ should be 0. Our initialization handles this by setting dist[i][i]=0 first.
- Multiple edges: The problem states "exactly one directed edge", so no multiple edges between same pair.
- Unreachable pairs: If a pair $(i, j)$ is never reached, the answer is -1.

## worker: Implement the BFS algorithm to compute shortest pa
The solution uses a multi-source BFS on the state space of pairs $(u, v)$, representing that we have found a palindrome path from $u$ to $v$. 

1. **Initialization**: 
   - All $(i, i)$ are initialized with distance 0 (empty path, which is a palindrome).
   - All $(i, j)$ where there is an edge $i \to j$ are initialized with distance 1 (single character, which is always a palindrome). If $i=j$, the distance remains 0 since it's shorter.

2. **BFS Expansion**:
   - For each state $(u, v)$ with distance $d$, we look for all pairs of edges $(a \to u)$ and $(v \to b)$ such that both edges have the same label $c$.
   - If such a pair exists and $(a, b)$ hasn't been visited yet, we set $dist[a][b] = d + 2$ and enqueue $(a, b)$.
   - This works because if we have a palindrome path from $u$ to $v$, and we prepend $a \to u$ and append $v \to b$ with matching labels, the new path from $a$ to $b$ is also a palindrome.

3. **Complexity**:
   - Number of states: $N^2$.
   - For each state, we iterate over 26 labels. For each label, we iterate over predecessors of $u$ and successors of $v$.
   - In the worst case, this is $O(N^2 \cdot 26 \cdot N \cdot N) = O(26 \cdot N^4)$, which for $N=100$ is about $2.6 \times 10^8$ operations. However, in practice, the number of edges with a specific label is much smaller, and many states are unreachable, so this runs efficiently within time limits.

4. **Edge Cases**:
   - Self-loops are handled correctly: $dist[i][i] = 0$ takes precedence over any self-loop edge (distance 1).
   - Unreachable pairs remain at -1.
