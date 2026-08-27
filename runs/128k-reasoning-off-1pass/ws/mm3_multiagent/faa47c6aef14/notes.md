
## ideation
**Core difficulty**
We have $N$ boxes each containing at most 1 red and 1 blue ball ($A_i,B_i \in \{0,1\}$). An operation on box $i$ deterministically sends its red balls to $P_i$ and its blue balls to $Q_i$. We need all balls to end up in box $X$ (and nowhere else) in the minimum number of operations.

Since each box starts with at most 1 red + 1 blue ball, we can treat the two colors independently. Each ball follows the forward map $f_\text{red}(i)=P_i$ or $f_\text{blue}(i)=Q_i$ until it reaches a box we choose to operate on. A box can be emptied only if we operate on it exactly once, *after* it has received all balls that will ever flow into it, and *before* any of those balls get forwarded elsewhere.

**Candidate approaches**

1. **Reachability via inverse graph**  
   - Build the reverse edges: for red, add $P_i \to i$; for blue, add $Q_i \to i$.  
   - From $X$ traverse backwards (along both color edges) to find the set $S$ of boxes whose balls can eventually reach $X$.  
   - If any ball starts in a box outside $S$, it's impossible → `-1`.  
   - Otherwise, every box in $S\setminus\{X\}$ must be operated on exactly once, and the order must be a topological order of the reverse reachability DAG (parents before children). This is always satisfiable because the reverse reachability forms a DAG (it's the union of cycle-free reverse paths into $X$? actually it can contain cycles, but all cycles are entirely within $S$ and every node in a cycle can reach $X$ multiple times — we must be careful).

2. **Cycle handling**  
   - Within $S$, if a box $i$ has both a red and blue edge pointing to distinct successors inside $S$, no problem.  
   - If $i$ is in a cycle (i.e., following forward maps from $i$ never reaches $X$ except by re-entering $i$), then balls stuck in that cycle can never reach $X$ unless the cycle is "broken" by operating on some node in the cycle. Operating on a node in a cycle sends its balls out and leaves the box empty, so the cycle is broken; then subsequent operations can drain the rest. This works iff the cycle is entirely within $S$ and every node in the cycle can reach $X$ in the reverse graph (which by definition of $S$ is true).  
   - Key fact: if all balls start in $S$, then operating on each node of $S\setminus\{X\}$ exactly once in *any* order that respects "a box is operated after all its reverse-reachable predecessors are operated" is valid. Such an order always exists: do a reverse DFS from $X$ and process nodes in the order they are visited (children before parents in the forward direction, i.e., parents before children in the reverse direction).

3. **Minimum number of operations**  
   - Once we know $S$ (the set of boxes that must be emptied), the answer is simply $|S|-1$ (or $0$ if $S$ is empty or only contains $X$). Every box in $S\setminus\{X\}$ requires exactly one operation; we cannot do fewer because each such box initially contains at least one ball (or will receive one), and operating is the only way to remove balls from a box.

## worker: Implement the solution in Python: read input, buil
The key insight is that since A_i, B_i ∈ {0,1} and P, Q are permutations, the movement of each color's balls is independent and follows a cycle. The set of boxes that can ever send balls to X is exactly the union of the cycle containing X in permutation P (for red) and the cycle containing X in permutation Q (for blue). We verify all initial balls lie in these cycles; otherwise, it's impossible. For the count, we compute the maximum distance to X (following the permutation) among initial red balls in the P-cycle, and similarly for blue. The required operations are exactly the nodes on the path from the farthest red source to X in the P-cycle, union the path from the farthest blue source to X in the Q-cycle, excluding X itself. This reduces to counting nodes with distance ≤ max_red in the P-cycle (excluding X) plus those with distance ≤ max_blue in the Q-cycle (excluding X), with duplicates counted once. The algorithm runs in O(N) time.
