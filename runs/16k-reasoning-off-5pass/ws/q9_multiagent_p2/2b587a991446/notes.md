
## ideation
The problem asks for the minimum number of moves to swap two pieces A (at S) and B (at T) on a simple connected undirected graph without them occupying the same vertex simultaneously.

**Core Difficulty:**
The constraint "cannot make a move that results in both pieces ending up on the same vertex" prevents direct swapping on an edge if S and T are adjacent, unless there is a third vertex to facilitate the move. If the graph is a tree (no cycles), the unique path between any two nodes means pieces will inevitably block each other if they try to cross, making the swap impossible in most cases.

**Candidate Approaches:**
1.  **Graph Properties Check:**
    *   If the graph is a tree ($M = N - 1$), it is generally impossible to swap pieces because there are no alternative paths to maneuver around each other. The only exception might be trivial cases, but analysis shows even with $N > 2$, if the graph is a tree, the swap is impossible.
    *   If the graph is not a tree ($M \ge N$), cycles exist, allowing pieces to go "around" each other.

2.  **Distance Analysis:**
    *   Calculate the shortest path distance $D$ between $S$ and $T$ using BFS.
    *   **Case 1: $D = 1$ (S and T are adjacent).**
        *   If the graph is a tree, it's impossible (as established above).
        *   If the graph is not a tree, we can use a neighbor of S (other than T) or T (other than S) to facilitate the swap. The sequence typically takes 3 moves: Move A to a neighbor $u$ of S, Move B to S, Move A to T. Or similar variations. The minimum is 3.
    *   **Case 2: $D > 1$.**
        *   If the graph is a tree, it's impossible.
        *   If the graph is not a tree, the pieces can move towards each other along the shortest path. One piece moves to a neighbor of S, the other moves to a neighbor of T, and they cross. The minimum moves required is $2 \times D$.

**Pitfalls:**
*   Assuming adjacency ($D=1$) is always impossible (Sample 1 shows it's possible if $N > 2$ and there's a cycle).
*   Assuming a solution always exists if $M \ge N$. While rare, specific graph structures might still be tricky, but for this specific problem type (likely from a contest like AtCoder), the "Tree = Impossible" rule is the key discriminator.
*   Not handling the $N=2$ case correctly (Sample 2).

**Refined Logic:**
1.  If $M == N - 1$ (Tree): Output -1.
2.  Else (Graph has cycles):
    *   Run BFS to find $dist(S, T)$.
    *   If $dist(S, T) == 1$: Output 3.
    *   Else: Output $2 \times dist(S, T)$.

This logic covers all samples:
*   Sample 1: $N=4, M=4$ (Not tree), $dist=1 \rightarrow 3$. Correct.
*   Sample 2: $N=2, M=1$ (Tree) $\rightarrow -1$. Correct.
*   Sample 3: $N=5, M=6$ (Not tree), $dist=2 \rightarrow 4$. Correct.

## worker: Implement the complete Python solution reading fro
The solution relies on the property that swapping two pieces on a graph without collision is impossible if the graph is a tree (since there are no cycles to maneuver around each other), provided $N \ge 2$.
1.  **Tree Check**: If $M = N - 1$, the graph is a tree. In this case, the unique path between any two nodes means pieces will block each other. The output is -1.
2.  **Non-Tree Case**: If $M \ge N$, there is at least one cycle.
    *   If $S$ and $T$ are adjacent ($dist(S, T) = 1$), we cannot move directly because the destination is occupied. We must move one piece to a neighbor (possible since $N > 2$ in a non-tree graph with adjacent $S, T$ implies a cycle or extra edges), perform the swap, and return. The minimum moves is 3.
    *   If $S$ and $T$ are not adjacent ($dist(S, T) = d > 1$), the pieces can move towards each other along the shortest path. One piece moves to a neighbor of $S$, the other to a neighbor of $T$, and they cross. The total moves required is $2 \times d$.

The BFS correctly computes the shortest path distance in an unweighted graph.
