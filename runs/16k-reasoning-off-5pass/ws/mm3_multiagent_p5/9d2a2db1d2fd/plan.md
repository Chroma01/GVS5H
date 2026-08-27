We need to answer many queries of the form: minimum stair moves to go from floor Y at (A,B) to floor Z at (C,D). Stair moves count vertical moves within a building; walkway moves are free (any number). A walkway can be taken from floor X in (i,j) to floor X in a cardinally adjacent building that has height ≥ X.

Observation: The cost is the sum of absolute vertical moves performed within each building visited. Since walkway moves don't change floor, we can think of the journey as a sequence of floor changes at certain cells. The total stair cost equals sum over visited cells of |floor_in - floor_out| (or 0 if we don't change floor there). We can change floor at any visited cell, possibly multiple times, but it's optimal to change at most once per cell (monotonic).

Key insight: The optimal strategy is to pick a floor X that is achievable (≤ min height along some path) and walk from start to a cell where we can descend/ascend to target floor. Actually, we can think of it as: we can walk at any floor X that is ≤ min height of all cells on the path. So we need to find a path from start to goal where we can choose intermediate floor(s) to minimize total vertical movement.

This is equivalent to: we can move freely on any floor X that is ≤ the minimum building height along the path. So we want to find a path that allows us to "bridge" the floor difference Y→Z with minimal stair usage.

Alternative view: Consider the graph where nodes are (cell, floor). Stair edges have weight 1 between consecutive floors in same cell. Walkway edges have weight 0 between same floor X in adjacent cells if both have height ≥ X. We need shortest path distances. But H,W up to 500, heights up to 1e6, Q up to 2e5 — too large for per-query Dijkstra.

Better approach: Precompute for each floor X, the connected components of cells with height ≥ X (via walkways). Then for a query, we need min over X of: cost to go from Y to X (stairs) + cost to go from X to Z (stairs), where the path between cells must stay within cells of height ≥ X.

Actually, we can change floor at any cell along the path. So we can go from Y down/up to some floor X at start cell (cost |Y-X|), walk via walkway at floor X to some cell near goal (must stay in cells with height ≥ X), then go from X to Z at goal cell (cost |X-Z|). But we could also change floor at intermediate cells. However, since walkway is free and we can change floor at any cell, the optimal is: pick a floor X, go from Y to X at start (|Y-X|), walk at floor X to goal cell (if connected), then X to Z (|X-Z|). But we might also walk to an intermediate cell, change floor there, etc. That would be like picking two floors X1, X2. But we can combine: it's equivalent to picking a single floor X that we walk at, because we can always consolidate floor changes.

Wait, consider: start at Y, walk at floor Y to some cell A (cost 0 if connected at Y), then stairs to floor X at A (cost |Y-X|), walk at X to goal (cost 0 if connected at X), then stairs to Z (cost |X-Z|). So total = |Y-X| + |X-Z|, provided there exists a path from A to goal at floor X, and a path from start to A at floor Y. But we can choose A = start cell, so we just need: start and goal are connected at floor X. Then cost = |Y-X| + |X-Z|. But we could also walk at Y to some cell, change to X, walk at X to goal. That requires connectivity at Y from start to some cell, and at X from that cell to goal. This is equivalent to: there exists a cell reachable from start at floor Y and from which goal is reachable at floor X. This is more flexible than requiring start and goal directly connected at X.

However, we can also change floor multiple times. The general problem: we have a sequence of floors f0=Y, f1, f2, ..., fk=Z. At each step i, we walk at floor fi from current cell to next cell (must be connected at fi), then stairs to fi+1 at that cell. Total stair cost = sum |fi - f_{i+1}|. We want to minimize this.

This is like: we can move in the "floor graph" where moving between cells at floor X is free if connected. We want to find a path in the combined state space.

Observation: The floor changes are independent of the path except for the connectivity constraint. The connectivity at floor X is determined by the set of cells with height ≥ X. As X decreases, the set grows (more cells included), so connectivity can only increase. So if two cells are connected at floor X, they are connected at any floor Y ≤ X.

Thus, for a query, we can consider: we want to find floors X and Y (with X ≤ min height on path from start to some pivot, Y ≤ min height on path from pivot to goal) such that... Actually, let's think differently.

Since we can walk at any floor as long as we stay in cells with height ≥ that floor, and we can change floor at any cell, the problem reduces to: we can traverse a path in the grid where at each cell we may change floor. The cost is the total variation in floor.

This is equivalent to: we have a graph where nodes are cells, and we can move between adjacent cells at cost 0 if we stay on the same floor, but we can also change floor at cost equal to the difference. Actually, we can model it as: we have a 3D grid (i,j,f) for f=1..F_{i,j}. Stairs: (i,j,f) <-> (i,j,f+1) cost 1. Walkway: (i,j,f) <-> (i',j',f) cost 0 if adjacent and both have height ≥ f.

We need shortest path between (A,B,Y) and (C,D,Z). This is a huge graph.

But note: walkway edges have weight 0 and connect all cells with height ≥ f at floor f. So at each floor f, the cells with height ≥ f form a connected component (or multiple). Within a component, we can move freely at cost 0. Between floors, we have stairs.

This suggests we can compress: for each floor f, compute connected components of cells with height ≥ f. Then the state is (component_id, floor). But component_id changes with f.

Alternative: Think of the problem as: we want to go from Y to Z. We can decrease floor (go down) at cost 1 per floor, walk horizontally at that lower floor (if possible), then increase floor (go up) at cost 1 per floor. So the optimal is to find a floor X such that we can walk from start to goal at floor X, and the cost is |Y-X| + |X-Z|. But we might also walk at Y to some cell, then go down to X, walk at X to goal. That requires that start and some cell are connected at Y, and that cell and goal are connected at X. This is equivalent to: there exists a floor X such that start and goal are in the same connected component at floor X, OR there exists a sequence of floors.

Actually, consider the following: we can walk at floor Y from start to some cell A (if connected at Y). Then we go down to floor X at A (cost Y-X). Then walk at X from A to goal (if connected at X). Total cost = (Y-X) + (X-Z) = Y-Z if X is between Y and Z? Wait, if Y > X and X > Z, then cost = (Y-X)+(X-Z)=Y-Z. But if Y=10, Z=6, and we pick X=6, cost = 4+0=4. But we need connectivity at X=6 from A to goal. If we pick A=start, we need start and goal connected at floor 6. In sample 1, start (1,1) height 12, goal (3,1) height 7. At floor 6, are they connected? Let's see: (1,1) has height 12 ≥6, (1,2) height 10 ≥6, (1,3) height 6 ≥6, (2,3) height 8 ≥6, (3,3) height 7 ≥6, (3,2) height 6 ≥6, (3,1) height 7 ≥6. So yes, they are connected at floor 6. Then cost = |10-6| + |6-6| = 4. But sample answer is 10. So my model is wrong.

Why? Because we cannot necessarily walk at floor 6 from start to goal directly? Wait, in the sample, the path described uses floor 10, then down to 6, then down to 3, then up to 6. They go down to 3 because at floor 6, maybe the path is not connected? Let's check: at floor 6, (1,1) to (1,2) to (1,3) to (2,3) to (3,3) to (3,2) to (3,1). All have height ≥6? (1,3) has height 6, yes. (2,3) has height 8, yes. (3,3) has height 7, yes. (3,2) has height 6, yes. (3,1) has height 7, yes. So they are connected at floor 6. Then why is the answer 10, not 4?

Because to go from floor 10 to floor 6 at start costs 4 stairs. Then walk at floor 6 to goal costs 0. Then from floor 6 to floor 6 at goal costs 0. Total 4. But sample says 10. So there must be a constraint I'm missing.

Re-read problem: "Choose a building with at least X floors in a cardinally adjacent block, and move to the X-th floor of that building using a (sky) walkway." So walkway moves you to the X-th floor of the adjacent building. That means if you are at floor X in building (i,j), you can move to floor X in adjacent building only if that building has height ≥ X. So at floor 6, you can move from (1,1) to (1,2) because (1,2) has height 10 ≥6. From (1,2) to (1,3) because (1,3) has height 6 ≥6. From (1,3) to (2,3) because (2,3) has height 8 ≥6. From (2,3) to (3,3) because (3,3) has height 7 ≥6. From (3,3) to (3,2) because (3,2) has height 6 ≥6. From (3,2) to (3,1) because (3,1) has height 7 ≥6. So yes, connected.

Then why is the answer 10? Let's check the sample input:
H=3, W=3
F:
12 10 6
1 1 3
8 6 7
Query 1: from (1,1) floor 10 to (3,1) floor 6.
My proposed path: at start, go down 4 floors to floor 6 (cost 4). Then walk via walkway at floor 6 to (3,1). Then we are at floor 6 at goal. Cost 4. But sample says 10. So either my path is invalid or I misread heights.

Wait: (2,1) has height 1. (2,2) has height 1. (2,3) has height 3. So at floor 6, (2,1) and (2,2) are not included. But my path doesn't go through (2,1) or (2,2). It goes (1,1)->(1,2)->(1,3)->(2,3)->(3,3)->(3,2)->(3,1). All these have height ≥6? (1,3) has height 6, yes. (2,3) has height 3? Wait, F_{2,3} = 3? Let's check input:
Row 1: 12 10 6
Row 2: 1 1 3
Row 3: 8 6 7
So (2,3) has height 3. At floor 6, (2,3) has height 3 < 6, so cannot be used! So the path I proposed is invalid because (2,3) cannot support floor 6.

So connectivity at floor 6: cells with height ≥6 are:
(1,1):12, (1,2):10, (1,3):6, (3,1):7, (3,2):6, (3,3):7.
(2,1):1, (2,2):1, (2,3):3 are excluded.
So the component containing (1,1) at floor 6 is: (1,1)-(1,2)-(1,3). That's it. (3,1) is in a separate component: (3,1)-(3,2)-(3,3). So they are not connected at floor 6.

Thus, to go from (1,1) to (3,1), we need to go through a floor where the two components are connected. The only way is to go down to floor 3? At floor 3, cells with height ≥3: (1,1):12, (1,2):10, (1,3):6, (2,3):3, (3,1):7, (3,2):6, (3,3):7. (2,1):1, (2,2):1 excluded. So at floor 3, (1,1) component: (1,1)-(1,2)-(1,3)-(2,3). (3,1) component: (3,1)-(3,2)-(3,3). Still disconnected because (2,3) is not adjacent to (3,3)? Actually (2,3) is adjacent to (3,3) (down). So (2,3) and (3,3) are adjacent. So at floor 3, (2,3) has height 3, so it can connect to (3,3) which has height 7. So the whole thing is connected: (1,1)-(1,2)-(1,3)-(2,3)-(3,3)-(3,2)-(3,1). So at floor 3, they are connected.

So we can go from floor 10 down to floor 3 at start (cost 7), walk at floor 3 to goal (cost 0), then up from floor 3 to floor 6 at goal (cost 3). Total 10. That matches sample.

So the problem is: we need to find a floor X such that start and goal are connected at floor X, and the cost is |Y-X| + |Z-X|. But we can also change floor at intermediate cells. However, if we can find a floor X where they are connected, we can just go from Y to X at start, walk to goal at X, then X to Z. That gives cost |Y-X|+|Z-X|. But we might do better by using two different floors: e.g., walk at Y to some cell A, then down to X, walk at X to goal. That requires connectivity at Y from start to A, and at X from A to goal. This is equivalent to: there exists a cell A such that start and A are connected at floor Y, and A and goal are connected at floor X. Since connectivity is monotone decreasing with floor, if start and A are connected at Y, they are connected at any floor ≤ Y. Similarly, if A and goal are connected at X, they are connected at any floor ≤ X. So if we pick X ≤ Y, then we need A such that start-A connected at Y (implies connected at X) and A-goal connected at X. That means start and goal are connected at X via A. So it's equivalent to start and goal connected at X. Similarly if X ≥ Y, we need A such that start-A connected at Y and A-goal connected at X. Since X ≥ Y, connectivity at X is a subset of connectivity at Y. So we need A in the intersection of the Y-component of start and the X-component of goal. This is more restrictive.

But we can also change floor multiple times. However, the optimal solution can be found by considering: we can walk at floor Y from start to some cell in the Y-component of start. Then we can change floor to any X ≤ Y (cost Y-X). Then walk at X to some cell in the X-component of goal. Then change to Z (cost |X-Z|). So we need to find X ≤ Y and a cell A such that A is in Y-component of start and X-component of goal. Then cost = (Y-X) + |X-Z|. Similarly, we could walk at floor Z from goal backwards? Actually, we can also go up first: walk at Y to A, then up to X ≥ Y, then walk at X to goal. But if X ≥ Y, the X-component of goal is smaller, so we need A in Y-component of start and X-component of goal. Since X ≥ Y, the X-component of goal is a subset of the Y-component of goal. So we need A in the intersection of Y-component(start) and X-component(goal). This is possible only if the two components overlap.

But we can also walk at floor Z from goal to some cell, then change floor, etc. By symmetry, we can consider walking at Y from start, or walking at Z from goal.

Actually, the general optimal strategy: we can walk at floor Y from start to some cell A (in the Y-component of start). Then we change floor to some X (cost |Y-X|). Then walk at X from A to some cell B (in the X-component of A). Then change to Z (cost |X-Z|). But we can combine the last walk: we want B to be the goal cell, so we need A and goal to be connected at X. So we need X such that there exists A in Y-component(start) with A connected to goal at X. That is: the Y-component of start and the X-component of goal intersect.

Similarly, we could walk at Z from goal to some cell B, then change to X, then walk to start. That requires X-component(start) and Z-component(goal) intersect.

Since we can choose to walk at Y or at Z first, the problem reduces to: find X such that either:
- Y-component(start) and X-component(goal) intersect, cost = (Y-X) + |X-Z| (if X ≤ Y) or (X-Y) + (X-Z) if X ≥ Y? Wait, if we walk at Y to A, then change to X. If X > Y, we go up, cost X-Y. Then walk at X to goal, cost 0 if connected. Then change to Z, cost |X-Z|. Total = (X-Y) + |X-Z|. But we need A in Y-component(start) and goal in X-component(A). Since X > Y, X-component is smaller. So we need A in Y-component(start) and also in X-component(goal). That is, Y-component(start) and X-component(goal) intersect.

If X < Y, we go down, cost Y-X. Then walk at X to goal. Need A in Y-component(start) and goal in X-component(A). Since X < Y, X-component is larger. So if goal is in X-component of A, then A and goal are connected at X. But we also need A in Y-component(start). So we need a cell A that is in Y-component(start) and also connected to goal at X. This is equivalent to: there is a path from start to A at Y, and from A to goal at X. This is possible if the Y-component of start intersects the X-component of goal. Because if they intersect at A, then A is in both.

So in both cases (X > Y or X < Y), the condition is: Y-component(start) and X-component(goal) intersect. And the cost is |Y-X| + |X-Z|.

Wait, if X > Y, cost = (X-Y) + |X-Z|. If X < Y, cost = (Y-X) + |X-Z|. So in both cases, cost = |Y-X| + |X-Z|. So the formula is the same.

But is it sufficient? What if we walk at Z from goal first? Then we need Z-component(goal) and X-component(start) intersect. Cost = |Z-X| + |X-Y|. Same.

So the problem reduces to: find a floor X such that the component containing start at floor Y and the component containing goal at floor X intersect. Then cost = |Y-X| + |X-Z|. But wait, we also need that the intersection cell A is reachable from start at Y and from goal at X. If the components intersect, then there is a cell A in both. Then we can walk from start to A at Y (since A is in Y-component of start), then change to X at A (cost |Y-X|), then walk from A to goal at X (since A is in X-component of goal), then change to Z (cost |X-Z|). So yes.

But is it necessary that the components intersect? Could we do better by changing floor at multiple cells? For example, walk at Y to A, down to X1, walk at X1 to B, down to X2, walk at X2 to goal. That would be cost (Y-X1) + (X1-X2) + |X2-Z|. But since X2 ≤ X1 ≤ Y, this is Y-X2 + |X2-Z| ≥ |Y-X2| + |X2-Z|. And the condition is that there is a path from A to B at X1 and B to goal at X2. This is more restrictive than just having a path from A to goal at X2. So it's not better.

What about going up? Walk at Y to A, up to X > Y, walk at X to B, down to Z? That would be (X-Y) + (X-Z) if X ≥ Z, or (X-Y)+(Z-X) if X < Z. But if we go up to X, then down to Z, we are effectively passing through X. The cost is |Y-X| + |X-Z|. And we need connectivity at X from A to B, and at Z from B to goal. But if we can go from A to B at X, and B to goal at Z, then since Z ≤ X, the Z-component of goal contains B? Actually, if B is connected to goal at Z, then B is in Z-component(goal). And A is in Y-component(start). We need A and B connected at X. This is equivalent to: there is a path from start to A at Y, from A to B at X, from B to goal at Z. This is possible if Y-component(start) contains A, X-component contains A and B, and Z-component(goal) contains B. This is equivalent to: there exists a cell A in Y-component(start) and a cell B in Z-component(goal) such that A and B are connected at X. This is more general than requiring Y-component(start) and X-component(goal) intersect. Because here we have A in Y-component(start), B in Z-component(goal), and A-B connected at X. Note that B is in Z-component(goal), so B is connected to goal at Z. But we need A-B connected at X. Since X ≥ Z, X-component is smaller. So we need A and B in the same X-component. This is a stronger condition than just Y-component(start) and X-component(goal) intersecting? Let's compare.

Case 1: Y-component(start) and X-component(goal) intersect at A. Then A is in Y-component(start) and X-component(goal). Since X-component(goal) is connected to goal at X, A is connected to goal at X. So we can set B = goal. Then A and B are connected at X (since A is in X-component(goal)). So this is a special case of the more general condition where B = goal.

Case 2: We pick A in Y-component(start) and B in Z-component(goal) such that A and B are connected at X. Then we can walk start->A at Y, A->B at X, B->goal at Z. Cost = |Y-X| + |X-Z|. This is the same cost. But is it always possible to achieve this cost? We need to find X such that there exists A in Y-comp(start) and B in Z-comp(goal) with A and B in the same X-component.

Note that if we take X = min(Y, Z), then we might have connectivity. But we can also take X larger than both.

So the problem is: find X that minimizes |Y-X| + |X-Z| subject to the existence of a path from start to goal that uses floors: Y at start, then X at some intermediate segment, then Z at goal. More precisely, we need a sequence of cells: start = v0, v1, ..., vk = goal, and floors f0=Y, f1, ..., fk=Z such that for each i, vi and vi+1 are adjacent and both have height ≥ fi, and |fi - f_{i+1}| is the stair cost. We want to minimize sum |fi - f_{i+1}|.

This is equivalent to: we can move in the grid at floor Y from start to some cell A (if connected), then change to X, move at X to some cell B, then change to Z, move at Z to goal. The cost is |Y-X| + |X-Z|. And we need that there is a path from start to A at Y, from A to B at X, and from B to goal at Z.

Since we can choose A and B arbitrarily, the condition is: there exists a cell A reachable from start at Y, and a cell B reachable from goal at Z, such that A and B are connected at X. This is equivalent to: the Y-component of start and the Z-component of goal are connected at floor X (i.e., there is a path between them using only cells with height ≥ X). Because if there is a path from A to B at X, then A and B are in the same X-component. And A is in Y-component(start), B is in Z-component(goal). So the Y-component of start and the Z-component of goal are in the same X-component.

Conversely, if the Y-component of start and the Z-component of goal are in the same X-component, then there exists A in Y-comp(start) and B in Z-comp(goal) with A and B connected at X. So the condition is: there exists a path from start to goal that goes through floors Y, X, Z in that order, with the middle segment at floor X. But we can also have more segments. However, any such path can be reduced to at most two floor changes: from Y to X at some cell, then from X to Z at some cell. Because we can always consolidate: if we have Y -> X1 -> X2 -> Z, we can think of it as Y -> min(X1,X2) -> max(X1,X2) -> Z, but the cost is the same. Actually, if we go down then up, we might waste. But the optimal is to have at most one intermediate floor X. Because the cost is |Y-X| + |X-Z|, which is convex in X. So we can restrict to one intermediate floor.

Thus, the problem is: find X such that the Y-component of start and the Z-component of goal are connected at floor X (i.e., there is a path between them using cells with height ≥ X). Then cost = |Y-X| + |X-Z|.

But wait: is it necessary that the Y-component of start and Z-component of goal are connected at X? What if we walk at Y from start to A, then down to X, then walk at X to goal? That requires A in Y-comp(start) and goal in X-comp(A). That means Y-comp(start) and X-comp(goal) intersect. This is a special case of the above where B = goal. Similarly, walking at Z from goal to B, then up to X, then walk at X to start requires Z-comp(goal) and X-comp(start) intersect. This is the other special case.

But the general case allows A and B to be different. However, if Y-comp(start) and Z-comp(goal) are connected at X, then there is a path from some A in Y-comp(start) to some B in Z-comp(goal) at X. Then we can walk start->A at Y, A->B at X, B->goal at Z. So the condition is exactly that the two sets are connected at X.

So the problem reduces to: for each query, we need to find the minimum over X of |Y-X| + |X-Z| such that the Y-component of start and the Z-component of goal are connected at floor X.

Now, note that the connectivity condition is monotone: if they are connected at X, they are connected at any X' ≤ X. Because lowering the floor only adds more cells. So the set of X for which they are connected is a downward-closed set: if X works, any smaller floor works.

Thus, we want to minimize f(X) = |Y-X| + |X-Z| over X in some set S that is downward-closed. f(X) is a convex function: it decreases as X approaches the interval [min(Y,Z), max(Y,Z)], and increases outside. Specifically, if Y ≤ Z, f(X) = (Z-Y) for X in [Y,Z], and f(X) = Z-X for X < Y, and X-Y + X-Z = 2X - (Y+Z) for X > Z. So the minimum is achieved at the largest X ≤ Y that is in S, or the smallest X ≥ Z that is in S, or any X in [Y,Z] ∩ S.

Since S is downward-closed, if there is any X in [Y,Z] that is in S, then the minimum is Z-Y (just pick any X in [Y,Z] ∩ S). If not, then we need to go below Y or above Z. Since S is downward-closed, if we go below Y, we can pick the largest X ≤ Y in S. If we go above Z, we need X ≥ Z in S, but S is downward-closed, so if X ≥ Z is in S, then all smaller floors are in S, so in particular Y is in S (if Y ≤ X). But if Y > Z, then going above Z might not help because S is downward-closed: if X ≥ Z is in S, then Z is in S, but we need X ≥ Z. Actually, if X ≥ Z is in S, then since S is downward-closed, any floor ≤ X is in S. So if X ≥ Z, then Z is in S. But we need X ≥ Z. So we can pick X = Z if Z is in S. But Z is in S if the two components are connected at floor Z. If not, we might need X > Z. But if X > Z is in S, then since S is downward-closed, Z is also in S? No, downward-closed means if X is in S, then all floors ≤ X are in S. So if X > Z is in S, then Z is in S. So if there is any X > Z in S, then Z is in S. So we only need to consider X ≤ Z. Similarly, if there is X < Y in S, then all floors ≤ X are in S, but that doesn't imply Y is in S. So the relevant candidates are: the largest X ≤ Y in S, and the smallest X ≥ Z in S (but if Z is in S, we can pick X=Z). Actually, since S is downward-closed, the set of X in S is of the form [0, M] for some M? Not necessarily, because connectivity might not be monotone in that way? Wait, connectivity at floor X: as X decreases, more cells are included, so connectivity increases. So if two components are connected at X, they are connected at any X' < X. So the set of X where they are connected is indeed downward-closed: if X is in S, then any X' < X is in S. So S = {X | X ≤ T} for some T? Not necessarily, because there might be a gap: they are connected at high floors, then disconnected at some lower floor? No, as floor decreases, cells are added, so connectivity can only increase. So if they are connected at X, they are connected at all lower floors. So S is an interval [0, M] where M is the maximum floor at which they are connected. Actually, they are always connected at floor 1? At floor 1, all cells with height ≥1 are included, which is all cells. So at floor 1, the whole grid is connected. So S always contains 1. So S = [1, M] for some M ≥ 1. M is the maximum floor such that start and goal are connected at floor M. Since at floor M, they are connected, and at any floor > M, they might not be connected. So S = [1, M].

Thus, for a query, we need to find M = the maximum floor such that start and goal are connected at floor M. Then the feasible X are 1 ≤ X ≤ M. We want to minimize |Y-X| + |X-Z| over X in [1, M].

This is a simple optimization: f(X) = |Y-X| + |X-Z|. The minimum over X in [1, M] is:
- If M ≥ max(Y,Z), then we can pick X in [Y,Z] (if Y≤Z) or [Z,Y] (if Z≤Y), so cost = |Y-Z|.
- If M < min(Y,Z), then we must pick X ≤ M. The best is X = M (since f is decreasing as X approaches the interval). Cost = |Y-M| + |Z-M| = (Y-M)+(Z-M) = Y+Z-2M.
- If Y ≤ M < Z, then we can pick X in [Y, M] (since M < Z, we cannot reach Z). The best is X = M (since f is decreasing as X increases towards Z). Cost = (M-Y) + (Z-M) = Z-Y.
- If Z ≤ M < Y, then best X = M, cost = (Y-M)+(M-Z) = Y-Z.

So the answer is:
If M ≥ max(Y,Z): |Y-Z|
Else if M ≥ min(Y,Z): |Y-Z| (since we can pick X between min and max, but M is less than max, so we can pick X = min(Y,Z) if min(Y,Z) ≤ M? Wait, if M ≥ min(Y,Z), then min(Y,Z) is in [1,M]. So we can pick X = min(Y,Z). Then cost = |Y-min| + |Z-min|. If Y ≤ Z, min=Y, cost = 0 + (Z-Y) = Z-Y. If Z ≤ Y, min=Z, cost = (Y-Z)+0 = Y-Z. So cost = |Y-Z|.
If M < min(Y,Z): cost = Y+Z-2M.

So the answer depends only on M, Y, Z. Specifically:
If M ≥ max(Y,Z): answer = |Y-Z|
Else if M ≥ min(Y,Z): answer = |Y-Z|
Else: answer = Y+Z-2M.

Wait, the second case: if M ≥ min(Y,Z), then min(Y,Z) ≤ M. But we also need that max(Y,Z) might be > M. In that case, we can pick X = min(Y,Z). Then cost = |Y-min| + |Z-min| = |Y-Z|. So indeed, if M ≥ min(Y,Z), answer = |Y-Z|.
If M < min(Y,Z), answer = Y+Z-2M.

So the answer is:
If M ≥ min(Y,Z): |Y-Z|
Else: Y+Z-2M.

But is that correct? Let's test with sample 1, query 1: start (1,1) Y=10, goal (3,1) Z=6. We need M = max floor such that (1,1) and (3,1) are connected. As we saw, at floor 6, they are not connected because (2,3) is too short. At floor 5, (2,3) has height 3 <5, so not included. At floor 4, same. At floor 3, (2,3) has height 3, so included. And (2,3) connects (1,3) and (3,3). So at floor 3, they are connected. At floor 4, (2,3) is not included, so (1,3) and (3,3) are not connected. So M=3. min(Y,Z)=6. M < min, so answer = 10+6-2*3 = 16-6=10. Correct.

Query 2: start (1,1) Y=6, goal (1,2) Z=4. M = max floor such that (1,1) and (1,2) are connected. They are adjacent, so they are connected at any floor ≤ min(height(1,1), height(1,2)) = min(12,10)=10. So M=10. min(Y,Z)=4. M ≥ min, so answer = |6-4|=2. Correct.

So the problem reduces to: for each query, we need to compute M = the maximum floor X such that the cell (A,B) and cell (C,D) are connected in the graph where edges exist between adjacent cells if both have height ≥ X. This is equivalent to: M = min over all paths from (A,B) to (C,D) of the minimum height along the path. Because if we take the minimum height along a path, then at that floor, all cells on the path have height ≥ that floor, so they are connected. And if they are connected at floor X, there is a path where all cells have height ≥ X, so the minimum height along that path is ≥ X. So M = max over paths of min height along path. This is the "maximin" path problem, also known as the widest path or maximum capacity path. We need to find the maximum possible value of the minimum edge weight (or node weight) along a path from start to goal. Here, the weight of a node is its height. The path weight is the minimum node height along the path. We want the maximum such weight.

This is a classic problem: we can sort cells by height descending, and use Union-Find (DSU) to connect cells. As we lower the threshold, we add cells. For each query, we need to know the maximum floor at which start and goal are connected. This is equivalent to: if we process cells in decreasing order of height, and union adjacent cells, then the answer M is the height of the cell when start and goal become connected in the DSU. But we have many queries (up to 2e5), and H,W up to 500 (so 250k cells). We can preprocess: sort all cells by height descending. Then for each cell, when we add it, we union with adjacent cells that are already added (i.e., have height ≥ current height). Then we can record for each pair? No, we need to answer queries online or offline.

We can process queries offline: sort queries by the answer M descending? But we don't know M. Alternatively, we can binary search on M for each query, but that would be too slow (2e5 * log(1e6) * DSU check). Better: we can compute for each cell the "time" (height) when it becomes connected to others. But we need pairwise connectivity.

Observation: The DSU process gives us a spanning forest. The maximum M for a pair is the minimum edge weight along the path in the DSU tree? Actually, if we build the DSU by adding cells in decreasing height order, the DSU forms a maximum spanning forest if we consider edges between adjacent cells with weight = min(height of two cells)? Wait, we are adding nodes, not edges. But we can think of edges between adjacent cells with weight = min(height of the two cells). Then the maximum M for a pair is the maximum weight of a path using these edges, which is the minimum edge weight along the path maximized. This is exactly the maximum spanning tree (or forest) problem. If we build a maximum spanning forest on the grid graph where edge weight = min(height(u), height(v)), then for any two cells, the maximum M is the minimum edge weight along the path in the maximum spanning forest. This is a known property: in a maximum spanning tree, the path between two nodes maximizes the minimum edge weight.

So we can build a maximum spanning forest of the grid graph with edge weights = min(F[u], F[v]). Then for each query, we need to find the minimum edge weight on the path between (A,B) and (C,D) in this forest. This is a standard problem: we can preprocess with binary lifting (LCA) to answer min edge weight on path queries in O(log N) per query.

N = H*W ≤ 250,000. Building the maximum spanning forest: we have edges between adjacent cells. Number of edges: about 2*H*W. We can sort edges by weight descending and use Kruskal's algorithm. Edge weight = min(F[u], F[v]). Since F values are up to 1e6, sorting edges is O(E log E) = O(HW log(HW)). That's fine.

Then we have a forest (actually a spanning forest if grid is disconnected, but it's connected because at floor 1 all cells are included, so the graph is connected, so it's a spanning tree). Wait, is the grid graph connected? Yes, all cells are adjacent in the grid, so the graph is connected. So the maximum spanning forest is a spanning tree.

Then we need to answer queries: for each query, find the minimum edge weight on the path between two nodes in this tree. We can preprocess parent and min-edge-to-parent for each node, and binary lifting to find LCA and min on path.

Complexities: O(HW log(HW)) for sorting edges, O(HW) for DSU, O(HW log(HW)) for binary lifting preprocessing, O(Q log(HW)) for queries. With H,W ≤ 500, HW ≤ 250k, Q ≤ 200k, this is fine.

Let's verify with sample: Build max spanning tree with edge weight = min(height). For query 1: path from (1,1) to (3,1). The min edge weight on that path should be 3. Let's see: possible path: (1,1)-(1,2)-(1,3)-(2,3)-(3,3)-(3,2)-(3,1). Edge weights: min(12,10)=10, min(10,6)=6, min(6,3)=3, min(3,7)=3, min(7,6)=6, min(6,7)=6. Min on path = 3. So M=3. Answer = 10+6-2*3=10. Correct.

Query 2: (1,1) to (1,2). Edge weight = min(12,10)=10. M=10. Answer = |6-4|=2. Correct.

So the algorithm is:
1. Read grid F.
2. Create list of edges: for each adjacent pair (u,v), weight = min(F[u], F[v]).
3. Sort edges by weight descending.
4. Run Kruskal's algorithm to build maximum spanning forest (tree). Keep track of parent and the edge weight used to connect each node to its parent.
5. Preprocess binary lifting: up[k][v] = 2^k-th ancestor, min_edge[k][v] = minimum edge weight on the path from v to up[k][v].
6. For each query (A,B,Y,C,D,Z):
   - Convert (A,B) to node id = (A-1)*W + (B-1).
   - Find M = minimum edge weight on path between the two nodes in the tree.
   - Compute answer: if M >= min(Y,Z): ans = abs(Y-Z); else ans = Y+Z-2*M.
   - Print ans.

Edge cases: The tree might not be rooted. We can root it arbitrarily, say at node 0. Then binary lifting works.

We need to be careful with indexing: 0-indexed or 1-indexed. Use 0-indexed for internal.

Let's code this in Python.

Steps:
- Read H, W.
- Read F as list of lists.
- N = H*W.
- Create edges: for i in range(H): for j in range(W): if i+1<H: edge between (i,j) and (i+1,j) weight = min(F[i][j], F[i+1][j]). Similarly for j+1<W.
- Sort edges by weight descending.
- DSU: parent array, size.
- For each edge in sorted order: if find(u) != find(v): union(u,v), and set parent of the root? Actually, we need to build a tree. We can store the tree edges: for the node that is attached, store its parent and the edge weight. In Kruskal, when we union, we can set the parent of one root to the other. But we need to ensure the tree is rooted. We can do: when union(u,v), we attach the root of u to root of v (or vice versa). But we need to know which node is the parent in the tree. We can store an array tree_parent and tree_weight. Initially, tree_parent[i] = -1 (or itself). When we union, we set tree_parent[root_u] = root_v, and tree_weight[root_u] = edge_weight. But we need to be careful with DSU union by size. We can store the tree edges separately: after DSU, we have a forest. We can then do a DFS to set parents. But it's easier: during Kruskal, we can maintain a separate array for the tree. Since we are building a spanning tree, we can just record the edge as part of the tree. We can do: when union(u,v), we set parent_in_tree[u] = v, weight_in_tree[u] = edge_weight. But we need to know which one is the child. We can decide based on DSU root. Let's do: we have DSU parent array. When we union, we have roots ru and rv. We can set tree_parent[ru] = rv, tree_weight[ru] = edge_weight. Then later, we need to root the tree. We can pick an arbitrary root, say node 0. Then we need to orient the tree edges. The tree_parent array we built might not be consistent with root 0. We can just build the tree using adjacency list: for each edge added in Kruskal, add an undirected edge between u and v with weight. Then we have a tree. Then we can run DFS/BFS from root 0 to set parent and depth and edge weight to parent.

So:
- edges_added = [] list of (u,v,weight) for edges that were added.
- After Kruskal, we have a spanning tree (since graph is connected). Build adjacency list: for each (u,v,w) in edges_added, adj[u].append((v,w)), adj[v].append((u,w)).
- Then DFS from root 0: parent[0] = -1, depth[0] = 0, min_edge_to_parent[0] = inf (or large). For each neighbor, set parent, depth, min_edge_to_parent = w.
- Then binary lifting: up[0][v] = parent[v], min_up[0][v] = min_edge_to_parent[v]. For k>0: up[k][v] = up[k-1][ up[k-1][v] ], min_up[k][v] = min( min_up[k-1][v], min_up[k-1][ up[k-1][v] ] ).

Then for query (u,v):
- Find LCA of u and v.
- Compute min edge on path from u to LCA and v to LCA.
- M = min of those two mins.

Complexities: O(N log N) for binary lifting, O(Q log N) for queries.

N ≤ 250k, log N ≈ 18. Q ≤ 200k. Total operations: about 250k*18 + 200k*18 = 4.5M + 3.6M = 8M, fine.

Memory: adjacency list: 2*(H*(W-1) + (H-1)*W) ≈ 2*500*500 = 500k edges. Each edge stored twice. Fine.

Let's code.

Potential issues: recursion depth for DFS might be up to N=250k, which is fine for Python if we use iterative stack or set recursionlimit. We'll use iterative DFS.

Also, need to handle the case where the graph is not connected? But grid is connected, so it's a tree.

Now, let's double-check the formula for answer.

We derived: M = max floor such that start and goal are connected. Then:
If M >= min(Y,Z): ans = |Y-Z|
Else: ans = Y+Z-2*M.

But wait, is it always true that if M >= min(Y,Z), then ans = |Y-Z|? Let's test: Y=10, Z=6, M=6. min=6, M>=min. Then ans = |10-6|=4. But earlier we saw that for sample query 1, M=3, so not this case. But if M=6, is it possible? That would mean they are connected at floor 6. But in sample, they are not connected at floor 6. So if they were connected at floor 6, answer would be 4. Is that correct? Let's think: if connected at floor 6, we can go from 10 down to 6 at start (cost 4), walk at 6 to goal (cost 0), then 6 to 6 (cost 0). Total 4. Yes.

What if Y=6, Z=10, M=6? Then min=6, ans=4. Same.

What if Y=5, Z=10, M=5? min=5, ans=5. Walk from 5 to 5 at start, walk at 5 to goal, then up to 10. Cost 5. Correct.

What if Y=5, Z=10, M=4? min=5, M<min. ans = 5+10-2*4=15-8=7. Is that achievable? We need to go down to 4 at start (cost 1), walk at 4 to goal (cost 0), then up from 4 to 10 (cost 6). Total 7. Could we do better? What if we walk at 5 from start to some cell, then down to 4, walk at 4 to goal, then up to 10? That would be cost 1+6=7. What if we walk at 5 to some cell, then up to 10? But we need to connect to goal. If we go up to 10, we need connectivity at 10. But M=4 means not connected at 5? Actually M=4 means connected at 4 but not at 5. So at floor 5, they are not connected. So we cannot walk at 5 from start to goal. So we must go down to at most 4. So 7 is optimal.

So formula seems correct.

Now, we need to compute M efficiently. The maximum spanning tree approach gives the minimum edge weight on the path, which is exactly the maximum M. Because in the maximum spanning tree, the path between two nodes maximizes the minimum edge weight. This is a standard property: for any two nodes, the path in the maximum spanning tree has the maximum possible bottleneck (minimum edge weight) among all paths. So M = min edge weight on path in max spanning tree.

Thus, we can compute M using LCA and binary lifting.

Let's implement.

One more thing: the grid is up to 500x500, so N=250,000. The number of edges is about 2*500*499 = 499,000. Sorting 500k edges is fine.

We need to be careful with memory for binary lifting: up to log2(250k) ≈ 18. So up to 19 levels. up[19][250000] is about 19*250k = 4.75M integers, which is fine. min_up similarly.

Now, code structure:

```python
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    H, W = map(int, input().split())
    F = [list(map(int, input().split())) for _ in range(H)]
    N = H * W
    # node id: i*W + j
    edges = []
    for i in range(H):
        for j in range(W):
            u = i * W + j
            if i + 1 < H:
                v = (i+1) * W + j
                w = min(F[i][j], F[i+1][j])
                edges.append((w, u, v))
            if j + 1 < W:
                v = i * W + (j+1)
                w = min(F[i][j], F[i][j+1])
                edges.append((w, u, v))
    edges.sort(reverse=True)  # descending by weight