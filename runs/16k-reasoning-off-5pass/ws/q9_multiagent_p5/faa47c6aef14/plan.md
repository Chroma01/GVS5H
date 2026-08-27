The problem asks for the minimum operations to consolidate all balls into box $X$. Since each box $i$ sends its red balls to $P_i$ and blue balls to $Q_i$, the flow of balls is deterministic. We can model this as a graph where edges go $i \to P_i$ (red) and $i \to Q_i$ (blue). To move balls from a box $i$ to $X$, there must be a path of operations leading to $X$. Specifically, if we operate on $i$, balls move to $P_i$ and $Q_i$. To eventually get them to $X$, $P_i$ or $Q_i$ must eventually lead to $X$. This suggests a reverse graph approach: start from $X$ and find all boxes that can feed into $X$ (directly or indirectly) via the operation rules. However, the operation rule is "take from $i$, put to $P_i, Q_i$". So if we want to empty $i$, we must operate on $i$, sending its contents to $P_i$ and $Q_i$. Then we must empty $P_i$ and $Q_i$ (if they are not $X$) by operating on them, and so on. This looks like finding the set of all nodes that can reach $X$ in the "reverse" dependency graph where an edge $u \to v$ exists if operating on $u$ sends balls to $v$. Actually, it's simpler: we need to empty every box $i \neq X$. To empty $i$, we operate on it, sending balls to $P_i$ and $Q_i$. Now $P_i$ and $Q_i$ have extra balls. We must eventually operate on $P_i$ and $Q_i$ to move those balls further towards $X$. This implies we need to process nodes in an order such that when we operate on $u$, its targets $P_u$ and $Q_u$ are either $X$ or already processed (emptied). Wait, if we operate on $u$, balls go to $P_u$ and $Q_u$. If $P_u$ is not $X$, we must later operate on $P_u$ to move those balls further. So the dependency is: to clear $u$, we need to be able to clear $P_u$ and $Q_u$ *after* moving balls there? No, the operation on $u$ happens, then we operate on $P_u$. So the sequence is $u \to P_u \to \dots \to X$. Thus, we need a path from $u$ to $X$ in the graph where edges are $i \to P_i$ and $i \to Q_i$. If such a path exists for all $i \neq X$, we can clear them. The minimum operations is simply the number of nodes $i \neq X$ that have a path to $X$? Not exactly. If a node $u$ has a path to $X$, we operate on $u$, then the balls go to neighbors. We must operate on those neighbors too. Essentially, every node $i \neq X$ that can reach $X$ must be operated on exactly once. If a node cannot reach $X$, we can never empty it (unless it's already empty), so output -1. If all non-empty nodes can reach $X$, the answer is the count of such nodes? Let's re-read carefully. "Take all balls from $i$... put red to $P_i$, blue to $Q_i$". If we operate on $i$, it becomes empty. The balls appear at $P_i$ and $Q_i$. We must then operate on $P_i$ and $Q_i$ to move them further. So yes, every node that receives balls and is not $X$ must be operated on. The set of nodes that must be operated on is the set of all nodes $i$ such that there is a path from $i$ to $X$ in the graph defined by edges $i \to P_i$ and $i \to Q_i$. Wait, if $i$ is initially empty, do we need to operate on it? Only if balls are sent *to* it from some other node $j$. If $i$ is initially empty and no balls ever come to it, we don't operate on it. So the algorithm is:
1. Construct a graph with edges $i \to P_i$ and $i \to Q_i$.
2. Find all nodes $v$ that can reach $X$ in this graph.
3. Check if all initially non-empty boxes are in this set. If not, impossible (-1).
4. The answer is the number of nodes in this set that are initially non-empty? No. Consider Sample 1. Balls at 2, 4, 5. Paths to 3?
   Edges: $1\to4, 1\to3$; $2\to1, 2\to4$; $3\to2, 3\to5$; $4\to3, 4\to2$; $5\to4, 5\to1$.
   Target $X=3$.
   Can 5 reach 3? $5\to4\to3$. Yes.
   Can 4 reach 3? $4\to3$. Yes.
   Can 2 reach 3? $2\to1\to3$ or $2\to4\to3$. Yes.
   Can 1 reach 3? $1\to3$. Yes.
   Initially non-empty: 2, 4, 5. All can reach 3.
   Do we operate on 1? Initially empty. But balls from 2 go to 1. So 1 receives balls. Must operate on 1.
   So the set of operations is the set of all nodes $v$ (including initially empty ones) that can reach $X$ AND receive balls (either initially or from someone who can reach $X$).
   Actually, it's simpler: The set of nodes that must be operated on is exactly the set of all nodes $v$ such that there is a path from $v$ to $X$. Why? Because if $v$ can reach $X$, balls starting at $v$ (or coming from someone who can reach $v$) will eventually arrive at $X$ only if we operate on every node on the path. If we skip a node $u$ on the path $v \to \dots \to u \to \dots \to X$, the balls get stuck at $u$ (or its children) and never reach $X$. Since we want *all* other boxes empty, we must clear every node that has balls. Any node $v$ that can reach $X$ will eventually receive balls from the "source" set (initially non-empty nodes) if the graph structure allows flow. Specifically, if there is a path from an initially non-empty node $S$ to $v$, and $v$ can reach $X$, then $v$ must be operated on.
   Is it possible that a node can reach $X$ but never receives balls? Yes, if no initially non-empty node can reach it. In that case, we don't need to operate on it.
   So the algorithm is:
   1. Build graph $G$ with edges $i \to P_i, i \to Q_i$.
   2. Run BFS/DFS from $X$ in the *reverse* graph ($u \to v$ if $v \to u$ in $G$) to find all nodes $R$ that can reach $X$.
   3. Identify the set of "active" nodes: Start with initially non-empty nodes. Propagate reachability: if $u$ is active and $u \to v$ in $G$, then $v$ becomes active (because balls from $u$ go to $v$).
   4. Check if all active nodes are in $R$. If not, return -1.
   5. The answer is the size of the set $R \cap \text{ActiveNodes}$. Wait, is it just the count of nodes in $R$ that are part of the connected component of initially non-empty nodes leading to $X$?
   Let's trace Sample 1 again.
   Initially non-empty: {2, 4, 5}.
   Reverse reachability to 3: {1, 2, 3, 4, 5}. (All nodes can reach 3).
   Propagate active:
   Start {2, 4, 5}.
   From 2: goes to 1, 4. Add 1. Active: {1, 2, 4, 5}.
   From 4: goes to 3, 2. 3 is target (stop?), 2 is already active.
   From 5: goes to 4, 1. Already active.
   From 1: goes to 4, 3.
   From 3: target.
   Active set: {1, 2, 4, 5}.
   Intersection with ReverseReachable {1, 2, 3, 4, 5}: {1, 2, 4, 5}. Size 4. Correct.
   
   Sample 3:
   N=2, X=2.
   A=[1,1], B=[1,1]. Non-empty: {1, 2}.
   P=[1, 2], Q=[1, 2].
   Edges: $1\to1, 1\to1$; $2\to2, 2\to2$.
   Reverse reachability to 2: Only {2}. (1 cannot reach 2).
   Active propagation: Start {1, 2}.
   From 1: goes to 1. No new.
   Active: {1, 2}.
   Check: Is 1 in ReverseReachable? No. Return -1. Correct.

   So the logic holds:
   1. Build reverse graph $G_{rev}$ where edge $v \to u$ exists if $u \to P_u$ or $u \to Q_u$ in original.
   2. Find set $S_{reach}$ of all nodes that can reach $X$ in original graph (BFS from $X$ in $G_{rev}$).
   3. Find set $S_{active}$ of all nodes that will contain balls. Start with initially non-empty nodes. Perform BFS/DFS in original graph $G$ starting from $S_{active}$ to find all reachable nodes.
   4. If $S_{active} \not\subseteq S_{reach}$, output -1.
   5. Else, output $|S_{active} \cap S_{reach}|$. Note that since $S_{active} \subseteq S_{reach}$ is required, the answer is just $|S_{active}|$. Wait, is it possible for a node to be in $S_{active}$ but not $S_{reach}$? That's the failure case. If we pass the check, then $S_{active} \subseteq S_{reach}$, so answer is $|S_{active}|$.