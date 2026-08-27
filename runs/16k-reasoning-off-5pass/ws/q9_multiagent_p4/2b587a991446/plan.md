The problem asks for the minimum moves to swap two pieces on a graph without occupying the same vertex. If the shortest path between S and T is unique, the pieces can simply follow this path in opposite directions without ever colliding, resulting in a cost of $2 \times \text{dist}(S, T)$. If there are multiple shortest paths, we might be able to "pass" each other by taking a slightly longer detour, but we must ensure the detour allows them to cross without occupying the same node at the same time or blocking each other indefinitely. The core logic involves calculating the shortest distance $D$ and checking if there exists a path of length $D+1$ that shares an edge or vertex with the shortest path in a way that allows swapping. Specifically, if the graph is a simple line (unique shortest path), output $-1$ (unless $N=2$ and they just swap, but the constraint "cannot be on same vertex" makes swapping on a single edge impossible if they start on endpoints? Wait, Sample 2 says -1 for N=2, M=1. So unique path always fails). If there is an alternative route, we calculate the cost based on the structure of the "bottleneck" where they meet. The strategy is: 1. BFS to find shortest distance $D$. 2. Identify if the shortest path is unique. 3. If not unique, find the minimum cost to swap, which usually involves one piece taking a detour of length $D+1$ or both taking detours. Actually, the standard solution for this specific problem (AtCoder ABC 212 F or similar logic) is: if unique shortest path, impossible (-1). If not unique, the answer is $D + 1$ if they can pass on a shared edge/vertex configuration, or $2D$ if they can just walk past each other on a multi-edge? No, simple graph. The correct logic is: Calculate $D = \text{dist}(S, T)$. If the number of shortest paths is 1, output -1. Otherwise, output $D+1$? Let's re-verify Sample 1: S=3, T=4. Edges: (2,4), (1,4), (3,4), (2,3). Shortest path 3->4 is length 1. Is it unique? Yes, direct edge (3,4). But output is 3. Wait, if direct edge exists, they can't swap directly because they would collide. They must move out. 3->2, 4->3, 2->4. Total 3 moves. Here $D=1$, answer=3. Sample 3: S=3, T=5. Edges... Shortest path 3->1->5 (len 2) or 3->2->5 (len 2). Two shortest paths. Answer 4. $D=2$, answer=4. It seems if multiple shortest paths exist, answer is $2D$? No, Sample 1 had unique shortest path but answer was $2D+1$? $2(1)+1=3$. Sample 2: unique, -1. So: If unique shortest path, check if $D=1$. If $D=1$, impossible (-1). If $D>1$, can we do it? On a line 1-2-3-4, S=1, T=4. Unique path. Can we swap? No, blocked. So unique path always -1. If multiple shortest paths, answer is $2D$? Sample 3: $D=2$, ans=4. Sample 1: Unique, ans=3. Wait, Sample 1 is unique. Why 3? Because they have to go around. Path 3->2->4->3? No. 3->2, 4->3, 2->4. Moves: A(3->2), B(4->3), A(2->4). Total 3. This is $2D+1$. Is it always $2D+1$ for unique? What if $D=2$ unique? 1-2-3-4, S=1, T=4. Unique. Can we swap? No. So unique -> -1.
Wait, Sample 1: 3-4 is an edge. But 3-2-4 is also a path of length 2. So shortest path is length 1 (3-4). Is it unique? Yes. But answer is 3. Why? Because they cannot use the edge (3,4) to swap directly. They must use a longer path. The "swap" requires them to effectively cross. If the shortest path is unique, they are stuck on a line segment. They can never cross. So unique shortest path -> -1.
BUT Sample 1 output is 3. This contradicts "unique -> -1". Let's re-read Sample 1 carefully.
Graph: 1-4, 2-4, 2-3, 3-4.
S=3, T=4.
Shortest path from 3 to 4: Edge (3,4). Length 1.
Is there another path of length 1? No.
So shortest path is unique.
Why is answer 3?
Sequence: A(3->2), B(4->3), A(2->4).
Final state: A at 4, B at 3.
Path taken by A: 3->2->4 (Length 2).
Path taken by B: 4->3 (Length 1).
Total moves: 2+1 = 3.
Ah, they don't both have to take shortest paths. One takes a detour.
So the condition "unique shortest path implies impossible" is FALSE if one piece can take a detour while the other moves.
However, if the graph is a simple line (tree where the path is the only way), they can never pass.
So the condition is: Is the path unique AND is it a "bridge" that blocks all other paths?
Actually, the condition for impossibility is when the graph is a simple path between S and T (i.e., removing the edges on the shortest path disconnects the graph or rather, there are no alternative paths that allow crossing).
More precisely: If the number of shortest paths is 1, we check if there is ANY path of length $D+1$ that shares an edge with the shortest path?
Let's look at the logic for "Passing".
To swap, they must effectively cross.
Case 1: There are two distinct shortest paths of length $D$. Then they can just walk along their respective paths. If they meet at a vertex, they can't be there at the same time. But since paths are distinct, they can coordinate. Actually, if there are two disjoint paths, they just swap. If they share edges, they might block. But usually, if there are $\ge 2$ shortest paths, answer is $2D$? Or $2D+1$?
In Sample 3: S=3, T=5. Paths: 3-1-5 (len 2), 3-2-5 (len 2). They share no edges? 3-1, 1-5 vs 3-2, 2-5. Disjoint. They can swap in 4 moves (2 each). Output 4.
In Sample 1: Shortest path 3-4 (len 1). No other shortest path. But there is a path of len 2 (3-2-4).
They use the len 2 path for A and len 1 for B. Total 3.
General Algorithm:
1. BFS from S to get distS[] and count shortest paths? Or just check if there are multiple shortest paths.
2. BFS from T to get distT[].
3. $D = \text{distS}[T]$.
4. Check if there are multiple shortest paths. If yes, answer is $2D$? Wait, what if they share an edge?
Actually, the standard solution for this problem (which is likely "Swap" from a contest) is:
- Calculate $D$.
- Check if the shortest path is unique.
- If unique:
    - Check if there exists a path of length $D+1$ that shares an edge with the shortest path?
    - Actually, if unique, we need to find a vertex $v$ on the shortest path such that we can go $S \to \dots \to v \to \dots \to T$ via a detour?
    - Let's reconsider Sample 1. Shortest path $P_1 = (3,4)$. Detour $P_2 = (3,2,4)$. They share vertex 3 and 4. They don't share an internal edge.
    - The operation is: A takes $P_2$ (len 2), B takes reverse of $P_1$ (len 1). Total 3.
    - Can we always do $2D+1$ if there is a path of length $D+1$?
    - What if the only alternative path is length $D+2$? Then cost is $2D+2$?
    - We want to minimize $L_A + L_B$ where $L_A + L_B$ is the total moves, and they don't collide.
    - If there are $\ge 2$ shortest paths, answer is $2D$ (they take different shortest paths).
    - If unique shortest path:
        - We need to find a path $P'$ for one piece such that $P'$ and the reverse of $P_{short}$ don't collide.
        - The best strategy is usually: One piece takes the shortest path (length $D$), the other takes a path of length $D+1$ that shares exactly one edge or vertex?
        - Actually, if the shortest path is unique, the graph looks like a "lollipop" or a line with a side branch.
        - If there is ANY path of length $D+1$, we can achieve $2D+1$?
        - Let's verify. If unique shortest path, can we always do $2D+1$ if a $D+1$ path exists?
        - In Sample 1, $D=1$, path len 2 exists. Ans=3 ($2*1+1$).
        - What if $D=2$, unique, and path len 3 exists? Ans=5?
        - Is it possible to do better? No, because one must take at least $D$, the other must take at least something to let the first pass. If the first takes $D$, the second must take at least $D+1$ to avoid collision on the unique bottleneck?
        - Wait, if the second takes $D$, they collide. So one must take $>D$. Minimum is $D+1$. Total $2D+1$.
        - So the algorithm:
            1. Find $D = \text{dist}(S, T)$.
            2. Count number of shortest paths. If $>1$, answer $2D$.
            3. If $1$:
                - Check if there is a path of length $D+1$. If yes, answer $2D+1$.
                - Else, answer -1.
        - Wait, is it possible that even with multiple shortest paths, the answer is not $2D$?
          - If two shortest paths share an edge, say $S \to u \to v \to T$ and $S \to x \to v \to T$. They meet at $v$. Can they swap?
          - A goes $S \to u \to v$, B goes $T \to v \to x$. At $v$, one arrives, the other leaves?
          - Time steps:
            - t=0: A@S, B@T
            - t=1: A@u, B@v (if B moves T->v) -> Collision? No, A@u, B@v.
            - t=2: A@v, B@x. OK.
            - Then A@v, B@x. Goal: A@T, B@S.
            - A needs to go v->T (1 step). B needs to go x->S (path length?).
            - If B takes $T \to v \to x \to \dots \to S$.
            - If paths are distinct, they can usually coordinate to $2D$.
            - The only case $2D$ fails is if they are forced to occupy the same vertex at the same time on the same edge? No, vertices.
            - If they share a vertex $v$ on the shortest path, they can pass sequentially.
            - So if count > 1, answer is $2D$.
        - Is it possible that count > 1 but we cannot do $2D$?
          - Only if the graph is a single edge? No, then count=1.
          - If there are two paths, they must diverge at some point and converge later. They can pass.
          - So logic holds.

Refined Algorithm:
1. BFS from S to get `distS`. $D = \text{distS}[T]$.
2. BFS from T to get `distT`.
3. Count shortest paths? Or just check existence of alternative.
   - To check if shortest path is unique:
     - We can count the number of shortest paths modulo a large prime, or use DP.
     - Or simpler: Check if there exists a path of length $D$ other than the one we found?
     - Actually, we need to know if there are $\ge 2$ shortest paths.
     - Let's count number of shortest paths from S to T. If $>1$, ans = $2D$.
     - If $=1$:
       - Check if there exists a path of length $D+1$.
       - How to check efficiently?
       - A path of length $D+1$ exists if there is a vertex $v$ such that $\text{distS}[v] + \text{distT}[v] = D+1$? No, that's for any path.
       - We need a path of length $D+1$.
       - Actually, if the shortest path is unique, the graph structure is a line with some branches.
       - The condition for "path of length $D+1$ exists" is equivalent to: Is there any vertex $v$ such that $\text{distS}[v] + \text{distT}[v] = D+1$?
         - If such a $v$ exists, then $S \to \dots \to v \to \dots \to T$ has length $D+1$.
         - Does this guarantee we can swap?
         - In Sample 1: $D=1$. Vertices: 1,2,3,4.
           - distS (from 3): 3:0, 2:1, 4:1, 1:2.
           - distT (from 4): 4:0, 3:1, 2:1, 1:2.
           - Check $v=2$: distS[2]=1, distT[2]=1. Sum=2 = $D+1$. Yes.
           - Check $v=1$: distS[1]=2, distT[1]=2. Sum=4.
           - So $v=2$ works. Ans $2D+1 = 3$.
         - What if $D=2$, unique, and we have a path of length 3?
           - Then ans $2D+1 = 5$.
         - Is it possible to have a path of length $D+1$ but still impossible?
           - Only if the "detour" doesn't allow passing?
           - If there is a vertex $v$ with $\text{distS}[v] + \text{distT}[v] = D+1$, then $S \to v$ is shortest, $v \to T$ is shortest.
           - The path $S \to v \to T$ has length $D+1$.
           - The shortest path $P_{short}$ goes through some vertices.
           - Since shortest path is unique, $v$ is not on $P_{short}$?
             - If $v$ is on $P_{short}$, then $\text{distS}[v] + \text{distT}[v] = D$.
             - So if sum is $D+1$, $v$ is NOT on the shortest path.
           - So we have a "side branch" at some point?
           - Wait, if $v$ is not on the shortest path, then the path $S \to v \to T$ must leave the shortest path and come back?
           - But if the shortest path is unique, any deviation must increase length.
           - If we go $S \to \dots \to u \to v \to \dots \to T$, and $u$ is on shortest path, then length is $\text{distS}[u] + 1 + \text{distT}[v]$.
           - We need total $D+1$.
           - So $\text{distS}[u] + 1 + \text{distT}[v] = D+1 \implies \text{distS}[u] + \text{distT}[v] = D$.
           - Since $\text{distS}[u] + \text{distT}[u] = D$ (u on shortest path), this implies $\text{distT}[v] = \text{distT}[u]$.
           - And edge $(u,v)$ exists.
           - So there is an edge from the shortest path to a vertex $v$ which is at the same distance from T as $u$.
           - This forms a "parallel" edge effectively?
           - In this case, can we swap?
           - A takes $S \to \dots \to u \to v \to \dots \to T$ (len $D+1$).
           - B takes $T \to \dots \to u \to S$ (len $D$).
           - They meet at $u$?
           - A arrives at $u$ at time $k$. B arrives at $u$ at time $D-k$?
           - We need to schedule them so they don't collide.
           - Since A takes a longer path, A can wait? No, we want minimum moves.
           - If A takes $D+1$ and B takes $D$, total $2D+1$.
           - Can we always schedule?
           - Yes, A moves first, then B, etc.
           - The only constraint is they can't be on same vertex.
           - If they meet at $u$, one must leave before the other arrives.
           - Since lengths differ by 1, we can offset.
           - So yes, if such a $v$ exists, answer is $2D+1$.
           - If no such $v$ exists (i.e., no path of length $D+1$), then impossible (-1).

So Final Logic:
1. BFS from S -> `distS`.
2. BFS from T -> `distT`.
3. $D = \text{distS}[T]$.
4. Check if shortest path is unique.
   - How? Count number of shortest paths.
   - If count > 1, return $2D$.
   - If count == 1:
     - Check if there exists any vertex $v$ such that $\text{distS}[v] + \text{distT}[v] == D+1$.
     - If yes, return $2D+1$.
     - Else, return -1.

Wait, is "count > 1" sufficient for $2D$?
Yes, if there are two shortest paths, they can be chosen to be disjoint in terms of timing or just pass each other.
Actually, if they share an edge, say $u-v$, then one goes $S \to u \to v \to T$, other $S \to x \to v \to T$.
They both use $v$.
Can they pass?
A: $S \to u \to v \to T$.
B: $S \to x \to v \to T$.
They both need to go through $v$.
One arrives at $v$, leaves. The other arrives later.
Since they start at same time, they can't both be at $v$ at same time.
Can they swap?
Goal: A at T, B at S.
A takes path 1. B takes path 2.
Path 1: $S \to \dots \to v \to \dots \to T$.
Path 2: $S \to \dots \to v \to \dots \to T$.
Wait, if both take shortest paths, they both end at T. But B needs to end at S.
So B must take the reverse of a shortest path from T to S.
So B takes $T \to \dots \to v \to \dots \to S$.
A takes $S \to \dots \to v \to \dots \to T$.
They meet at $v$.
If the two shortest paths are distinct, they diverge before $v$ and converge after $v$? Or diverge and converge at $v$?
If they converge at $v$, then one comes from left, one from right? No, both come from S and T.
Path A: $S \to \dots \to v \to \dots \to T$.
Path B: $T \to \dots \to v \to \dots \to S$.
They meet at $v$.
If the paths are distinct, does that mean they don't overlap completely?
Yes.
Can they pass?
Yes, one passes through $v$ at time $t$, the other at time $t'$.
Since total length is $2D$, and they move simultaneously, we need to ensure no collision.
With two distinct shortest paths, there is always a way to order moves to avoid collision (e.g., one waits at start, or they pass at different times).
Actually, the standard result is: if multiple shortest paths, ans = $2D$.
If unique, check for $D+1$ path.

Implementation details:
- N, M up to 2e5.
- BFS is O(N+M).
- Counting shortest paths: Use DP with modulo arithmetic to avoid overflow? Or just check if count > 1.
- Since we only care if count > 1, we can cap the count at 2.
- `ways[u]` = number of shortest paths from S to u.
- `ways[T]` > 1 -> multiple.
- If `ways[T]` == 1:
  - Iterate all $v$. If `distS[v] + distT[v] == D+1`, then possible.

Corner case: $D=1$.
If unique, check $D+1=2$.
If exists path len 2, ans 3.
Else -1.
Matches Sample 1.

Corner case: $N=2, M=1$.
$D=1$. Unique. Check $D+1=2$. No path len 2. Ans -1.
Matches Sample 2.

Corner case: Sample 3.
$D=2$. Multiple shortest paths?
Paths: 3-1-5, 3-2-5.
Yes, multiple. Ans $2D = 4$.
Matches Sample 3.

One edge case: What if the two shortest paths share an edge but are otherwise distinct?
Does it matter? No, as long as they are distinct sequences of vertices, they can be scheduled.
Wait, what if the graph is a triangle? S=1, T=2. Edges (1,2), (1,3), (2,3).
Shortest path 1-2 (len 1). Unique? No, 1-3-2 is len 2.
Shortest is 1-2. Unique.
Check $D+1=2$. Path 1-3-2 exists. Ans $2(1)+1=3$.
Moves: A(1->3), B(2->1), A(3->2). Total 3. Correct.

What if graph is square? 1-2-3-4-1. S=1, T=3.
Shortest paths: 1-2-3, 1-4-3. Both len 2.
Multiple. Ans $2*2=4$.
Moves: A(1->2->3), B(3->4->1).
t=0: 1,3
t=1: 2,4
t=2: 3,1. Done. 4 moves. Correct.

Seems robust.