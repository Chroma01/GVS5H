import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    A = [0] * (N + 1)
    B = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    for i in range(1, N + 1):
        B[i] = int(next(it))
    P = [0] * (N + 1)
    Q = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = int(next(it))
    for i in range(1, N + 1):
        Q[i] = int(next(it))
    
    # Build reverse adjacency: rev_red[u] = list of v such that P[v] = u
    rev_red = [[] for _ in range(N + 1)]
    rev_blue = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        rev_red[P[i]].append(i)
        rev_blue[Q[i]].append(i)
    
    # BFS from X using reverse edges to find S: boxes whose balls can reach X
    # We consider reverse graph where from node u we can go to any v with P[v]=u or Q[v]=u
    # This is for both colors combined.
    # visited[v] = True if v can eventually send its balls to X.
    visited = [False] * (N + 1)
    dq = deque([X])
    visited[X] = True
    while dq:
        u = dq.popleft()
        for v in rev_red[u]:
            if not visited[v]:
                visited[v] = True
                dq.append(v)
        for v in rev_blue[u]:
            if not visited[v]:
                visited[v] = True
                dq.append(v)
    
    S = [i for i in range(1, N + 1) if visited[i]]
    
    # Check all balls are in S
    for i in range(1, N + 1):
        if A[i] == 1 and not visited[i]:
            print(-1)
            return
        if B[i] == 1 and not visited[i]:
            print(-1)
            return
    
    # If X has no balls and no other box in S has balls, answer is 0
    # Actually we need to check if there are any balls in S at all.
    has_ball = False
    for i in S:
        if A[i] == 1 or B[i] == 1:
            has_ball = True
            break
    
    if not has_ball:
        print(0)
        return
    
    # The answer is |S| - 1
    # But wait: we must also verify that the operations can actually be ordered.
    # However, since all balls in S can reach X via deterministic forward paths,
    # and we can process boxes in reverse topological order of the reverse reachability,
    # it's always possible. The key is that within S, every node either eventually
    # reaches X (possibly through a cycle that is broken when we operate on a node in the cycle).
    # Since we operate on each node in S\{X} exactly once, and we process them in
    # the order of a reverse BFS from X (parents first, then children), it works.
    # Actually, we need to be careful: in a cycle, every node points to another node in the cycle.
    # The reverse BFS from X will not reach nodes in a cycle unless X is in the cycle.
    # But if X is in a cycle, then all nodes in the cycle are in S, and we need to operate
    # on them. Can we? If we operate on a node i in the cycle, we send its balls to P_i and Q_i.
    # If P_i or Q_i is also in the cycle, the balls go to another node in the cycle.
    # We must ensure that we don't get stuck: we need to drain the cycle completely.
    # This is possible if we process nodes in the cycle in an order such that we empty them.
    # Actually, since we operate on each node exactly once, and the cycle is broken
    # once we operate on any node, we can process the cycle in any order.
    # The answer is simply the number of nodes in S that actually have balls or are needed
    # to forward balls. But every node in S must be operated on at least once if it
    # is on the path of any ball. However, is it possible that a node in S has no balls
    # initially and never receives any? Then we don't need to operate on it.
    # Wait: if a node in S has no balls and never receives balls, it doesn't affect the outcome.
    # But in the reverse graph, we only put nodes in S if they can reach X.
    # If a node has no balls and is never visited by any ball, it doesn't matter.
    # So we should refine S to be the set of boxes that are in the "ball-flow" set.
    # Actually, the correct condition: we need to operate on a box i if at any point
    # it contains a ball. So we should compute the set of boxes that will ever contain
    # a ball during the process. Since balls flow deterministically, the set of boxes
    # that will ever contain a ball is exactly the set of boxes reachable from some initial
    # ball in the forward direction, intersected with the condition that they can reach X.
    # Alternatively, we can compute the set of boxes that are on the forward path from
    # some initial ball to X.
    
    # Let's recompute more carefully.
    # We have initial balls. A ball at box i (red or blue) moves to P_i or Q_i respectively
    # each time we operate on that box. The sequence of boxes the ball visits is:
    # i, f(i), f(f(i)), ... where f is the appropriate color map.
    # The ball stops when we operate on a box and forward it, unless the box we operate on
    # is the one containing the ball. Actually, when we operate on a box, we take all balls
    # from it and put them to the next boxes. So the ball moves to the next box only when
    # we operate on the box it is currently in.
    # So the path a ball takes is determined by the order we operate on boxes.
    # To minimize operations, we should operate on a box only when it contains balls that
    # we want to move forward.
    # The goal is to get all balls to X. This is possible iff for every ball, by following
    # its deterministic forward map (depending on color), it eventually reaches X.
    # That is exactly the condition: every box containing a ball is in S (as defined).
    # Now, the minimum number of operations: we need to operate on every box that lies on
    # the forward path of any ball from its start to X, except possibly X itself if it
    # is the final destination and we don't need to forward its balls.
    # But wait: if X contains a ball and we want all balls to end at X, we don't need to
    # operate on X. However, if a ball passes through X and goes elsewhere, we need to
    # operate on X to forward it. But since X is the final destination, we never want
    # to forward balls out of X. So we must ensure that no ball leaves X. That means
    # we must not operate on X if it contains balls that we want to keep.
    # Actually, if a ball reaches X, we want it to stay. So we should not operate on X
    # after it has received balls, unless we need to forward them (but we don't).
    # So we only operate on X if it initially contains balls and we need to send them
    # somewhere else, but that's not helpful because we want them at X. So we never
    # operate on X if X is the target. Wait, what if a ball is in X and its forward
    # path goes out of X? Then we must operate on X to send it out, but that defeats
    # the purpose. So for the ball to end at X, we must never operate on X after the
    # ball arrives. But if the ball starts at X, we must operate on X to send it out
    # (or keep it). If we want it to end at X, we should not operate on X.
    # So the condition is: we never operate on X. This is fine as long as no ball
    # needs to leave X.
    # But consider a ball that starts at some i, and following the forward map it
    # eventually reaches X. If we operate on all boxes on the path except X, the ball
    # will end at X. That's perfect.
    # So the set of boxes we need to operate on is exactly the set of boxes on the
    # forward paths from initial ball positions to X, excluding X.
    # However, we also need to consider that a box might be visited by multiple balls.
    # We only need to operate on it once.
    # So the answer is: the number of distinct boxes (excluding X) that lie on at least
    # one forward path from an initial ball to X.
    # This is the union of forward paths from all initial balls to X.
    # We can compute this by taking the set of all boxes reachable from any initial ball
    # in the forward direction, and then intersect with S (boxes that can reach X).
    # Actually, since we only care about paths that end at X, we can do: start from
    # all initial balls, follow forward maps, and collect all visited boxes until they
    # reach X. Then the answer is the size of that set minus 1 (excluding X).
    # But careful: cycles. If a box is in a cycle and can reach X, following forward
    # from a ball might loop forever unless we break the cycle. But we break the cycle
    # by operating on nodes. So the ball's path is: start at i, then we operate on i,
    # it goes to f(i), we operate on f(i), etc. If f(i) is i (self-loop), then operating
    # on i sends the ball back to i, so the ball stays in i. But we already operated on i,
    # so the ball is in i and we are done with i? No, after operating on i, the box i is
    # empty, but the ball goes to P_i (or Q_i). If P_i = i, the ball goes back to i.
    # So we would need to operate on i again. That means a self-loop requires multiple
    # operations on the same box? Let's think: initially box i has a ball. We operate on i.
    # We take the ball, put it into P_i. If P_i = i, the ball goes back to i.
    # So after one operation, box i again contains the ball. We would need to operate
    # on i again. But if we operate again, the ball goes to P_i again, and so on.
    # So if P_i = i, the ball never leaves i. Then it can never reach X unless X = i.
    # So if P_i = i and i != X, and box i has a red ball, it's impossible.
    # This is already covered by the reachability condition: if P_i = i, then i cannot
    # reach any other box via red, so if i != X, the red ball at i cannot reach X.
    # So in S, for any i != X, we must have that following forward eventually reaches X
    # without getting stuck in a cycle that doesn't include X.
    # Actually, if a box i in S has a ball, then by definition of S, there is a path
    # from i to X. So it's not stuck in a cycle that excludes X.
    # However, consider a cycle: i -> P_i -> ... -> i, and X is in the cycle. Then
    # a ball at i can reach X, but it goes around the cycle. If we operate on each
    # node in the cycle exactly once, will the ball end at X? Not necessarily.
    # Example: i=1, P_1=2, P_2=1, X=1. Red ball at 1. We want it to end at 1.
    # If we operate on 2 first: box 2 empty. Then operate on 1: red ball goes to 2.
    # Now ball is at 2, but we already operated on 2, so we don't operate on 2 again.
    # Ball stays at 2, not at 1. So we failed.
    # Alternative: operate on 1 first: red ball goes to 2. Then operate on 2: red ball
    # goes to 1. Now ball is at 1. Success.
    # So the order matters. In this case, we need to process the cycle in reverse order
    # (1 then 2). That is a topological order of the reverse graph? The reverse graph
    # from X: X=1, rev_red[1] includes 2 (since P_2=1). rev_red[2] includes 1 (since P_1=2).
    # So the reverse graph has edges 1->2 and 2->1, which is a cycle. So we cannot
    # topologically sort it. This means that if X is in a cycle, it's not always possible
    # to drain the cycle without operating on X? But we don't want to operate on X.
    # Wait, in the example, we operated on 1 (which is X) and then on 2. That means
    # we did operate on X. But if X contains a ball, operating on X would send it out.
    # In the example, initially box 1 (X) has a red ball. We operate on 1, send it to 2.
    # Then operate on 2, send it back to 1. So we did operate on X, but it worked because
    # the ball eventually came back.
    # So maybe we do need to operate on X if it initially contains balls that are part
    # of a cycle. The problem statement allows operating on any box any number of times.
    # So we can operate on X if needed. But the goal is to have all balls end at X.
    # So if we operate on X, we must ensure that the balls we send out eventually come back
    # and stay.
    # This complicates things. Let's reconsider.
    
    # The problem is known: this is AtCoder ABC 320 F or similar? Actually, I recall
    # a problem about moving balls with two colors and permutations. The solution is
    # to consider the combined state (i, c) where c is color, and follow the permutation.
    # But here colors are separate.
    # Wait, the problem is from AtCoder ABC 320? No, it's "Balls and Boxes" or something.
    # Actually, it's similar to AtCoder ABC 213 G? No.
    # Let me think: we have N boxes, each with at most 1 red and 1 blue ball.
    # We can choose any order of operations. Each operation on i sends red to P_i, blue to Q_i.
    # Goal: all balls end up in box X.
    # Since each ball moves independently, we can think of each ball's path.
    # For a ball to end at X, we need to be able to route it to X.
    # Because we can choose the order, we can think of the balls as moving along the
    # directed graph defined by P and Q (two separate graphs).
    # Actually, the red balls move according to permutation P, and blue balls according to Q.
    # The operations allow us to "push" balls along the edges.
    # The minimum number of operations: we need to push each ball along its path to X.
    # The number of operations is at most the number of edges traversed.
    # But we can batch: if multiple balls pass through the same box, we only operate
    # on it once.
    # So the minimum number of operations is the number of distinct boxes (excluding X)
    # that are on the path from some initial ball to X.
    # However, due to cycles, we might need to operate on some boxes multiple times?
    # No, because once we empty a box, it doesn't get any new balls unless we operate
    # on its predecessor. So if we process boxes in a "reverse topological order" from X,
    # we might be able to do it in one pass.
    # The standard solution for this problem (I think it's AtCoder ABC 320 F? No,
    # it's "Balls and Boxes" from AtCoder Beginner Contest 213? Let me search memory.
    # Actually, it's AtCoder Regular Contest 109 D? No.
    # I recall a problem: "Balls" where you have two permutations and you want to
    # collect balls in one box. The solution is to find the set of boxes that can reach
    # the target via the reverse permutations, and then the answer is the size of that
    # set minus 1, because each such box needs to be operated on exactly once.
    # But we must also consider that if a box is in a cycle that includes X, we might
    # need to operate on it anyway, but the count is still the number of boxes in the
    # set minus 1.
    # Wait, in the cycle example above: X=1, cycle 1<->2. The set S from reverse BFS:
    # start at 1, rev_red[1] has 2, rev_red[2] has 1. So S = {1,2}. |S|-1 = 1.
    # But we needed 2 operations (operate on 1 and 2). So |S|-1 is not enough if we
    # count X? Actually, we operated on X (box 1) and box 2. That's 2 operations.
    # |S| = 2, so |S| = 2, not |S|-1. So the answer would be 2, but |S|-1 = 1.
    # So the answer is not simply |S|-1 if X is in a cycle and has a ball?
    # Let's re-read the problem: "all boxes other than the X-th box contain no balls".
    # So X can contain balls. The operations can be on any box, including X.
    # In the cycle example, we needed to operate on X and the other box. So 2 operations.
    # If we had no ball at X initially, and ball at 2, red: P_1=2, P_2=1, X=1.
    # Initially: box 1: (0,0), box 2: (1,0). S = {1,2} (both can reach 1).
    # Can we achieve goal with 1 operation? We need to get the ball from 2 to 1.
    # If we operate on 2: red ball goes to P_2=1. Then box 1 has the ball, box 2 empty.
    # That's 1 operation. So answer is 1, which is |S|-1 = 1. That works.
    # If we had ball at 1 (red) and nothing at 2, X=1. S={1,2}. We want ball to end at 1.
    # If we do nothing, ball is at 1. 0 operations. But |S|-1 = 1, which is not minimal.
    # So we need to be careful: we only need to operate on boxes that actually have
    # balls or receive balls.
    # In the case where X has a ball and is part of a cycle, we might need to operate
    # on X and the cycle.
    # But wait: if X has a red ball, and P_X = some box, then the ball will leave X
    # if we operate on X. If we want it to end at X, we must not operate on X, but then
    # the ball stays at X, which is fine. However, if the ball is blue and Q_X = some box,
    # same. So if X initially has a ball, we don't need to operate on X to achieve the
    # goal. The only time we operate on X is if we need to forward a ball that is
    # currently in X. But if we want the ball to end at X, we should avoid operating
    # on X after it has received the ball. So we should not operate on X at all,
    # unless necessary.
    # But in the cycle example, the ball at X needed to be forwarded to break the cycle?
    # No, in that example, we had ball at 1, cycle 1<->2. We operated on 1 and 2.
    # If we don't operate on 1, the ball stays at 1. That's already the goal.
    # So we can do 0 operations. But wait, is that allowed? Initially ball at 1, goal is
    # all balls at 1. That's already satisfied. So 0 operations. So the minimum is 0.
    # In my earlier example, I assumed the ball needed to be moved, but it didn't.
    # So the cycle example with ball at X: answer is 0 if X has the ball and we want
    # it to stay.
    # What if the ball at X is blue and Q_X = 2, and we want it to end at X? We don't
    # operate, it stays. So 0.
    # So the only reason to operate on X is if we have a ball somewhere else that needs
    # to pass through X? But X is the final destination, so we never forward balls out
    # of X. So we never need to operate on X if we are careful.
    # But consider: a red ball at i, P_i = X. If we operate on i, the ball goes to X.
    # Then it's at X. We don't need to operate on X. So that's fine.
    # So we can always avoid operating on X. Therefore, the answer is the number of
    # boxes (excluding X) that are on the path from some initial ball to X.
    # How to compute that? We need to find all boxes that are on a forward path from
    # an initial ball to X.
    # Since each ball moves deterministically, the set of boxes that will ever contain
    # a ball is exactly the set of boxes reachable from the initial set in the forward
    # direction, intersected with the condition that they can eventually reach X.
    # Actually, we can compute: start from all boxes that have balls. Follow forward maps
    # (both colors) until we reach X. The union of all visited boxes (excluding X) is
    # the set of boxes we need to operate on. But careful: a box might be visited by
    # a red ball and a blue ball, but we only need to operate on it once.
    # Also, we need to ensure that the order of operations exists. This is equivalent
    # to the condition that the subgraph induced by these boxes (with forward edges)
    # has no cycles that do not include X? Actually, if there is a cycle among these
    # boxes (excluding X), then we might have a problem. But if all balls in the cycle
    # can reach X, then the cycle must include X? Not necessarily. Consider a cycle
    # i1 -> i2 -> i3 -> i1, and none is X, but each can reach X via some other path.
    # Then a ball at i1, if we follow the forward map, will loop in the cycle and
    # never reach X unless we break the cycle by operating on some node in the cycle.
    # But if we operate on a node in the cycle, we send the ball to the next node in
    # the cycle. We can keep operating on the cycle nodes, and the ball will go around
    # the cycle. But since we only operate on each node once, after we operate on all
    # nodes in the cycle, the ball will end at the last node we operated on? Actually,
    # if we operate on each node in the cycle exactly once, the ball will move from
    # node to node, and after the last operation, it will be in the successor of that
    # node. If the successor is in the cycle, it might be a node we already operated
    # on. Then the ball is stuck in an already-operated box. That box is empty, so
    # the ball stays there. But that box is not X, so the goal is not achieved.
    # So if there is a cycle not containing X, it's impossible.
    # Therefore, the set of boxes that can reach X must form a DAG when we consider
    # the forward edges, except possibly cycles that include X. But if a cycle includes
    # X, then operating on the cycle might be possible as long as we end with the
    # balls at X.
    # Actually, the condition for possibility is that every ball's forward orbit
    # contains X. That is, for every box i with a ball, following the forward map
    # (P for red, Q for blue) eventually hits X. This is exactly the condition that
    # i is in the set of nodes that can reach X in the forward graph.
    # The set S we computed earlier (reverse reachable from X) is exactly the set of
    # nodes that can reach X. So the condition that all balls are in S is necessary
    # and sufficient.
    # Now, the minimum number of operations: we need to operate on every node in S
    # except possibly X? But we might need to operate on X if it is part of a cycle
    # and we need to break the cycle? Let's test with an example.
    # Example: N=2, X=1, P=(1,1) (self loops), Q=(1,1). A=(1,0), B=(0,0).
    # S: from 1, rev_red[1] has 1 and 2. So S={1,2}. All balls (red at 1) are in S.
    # Can we achieve goal? Box 1 has red ball. If we do nothing, ball at 1, which is X.
    # Goal achieved. 0 operations. So answer is 0, not |S|-1=1.
    # So we need to refine: the answer is the number of nodes in S that are on the
    # forward path from some initial ball to X, excluding X if we don't need to operate
    # on it.
    # How to compute the minimum number of operations?
    # The standard approach: do a BFS/DFS from X in the reverse graph to find S.
    # Then, the answer is the number of nodes in S that have at least one incoming edge
    # from another node in S? Not exactly.
    # Actually, the answer is the number of nodes in S minus 1, but only if we count
    # only those nodes that are "necessary" to be operated. A node is necessary if
    # there is a ball that passes through it. That is, if there is a ball at some
    # node in S, and the forward path from that node to X goes through that node.
    # So we can compute for each ball its forward path to X (following the appropriate
    # color map), and take the union of all nodes on these paths (excluding X).
    # The size of this union is the answer.
    # But how to compute this efficiently? N up to 2e5.
    # Since each ball follows a deterministic path, we can just simulate the path
    # from each initial ball until it reaches X. But a path might be long (up to N).
    # However, since each node has exactly one outgoing edge per color, the path is
    # a sequence in a functional graph. The total length of all paths could be O(N^2)
    # if we do it naively.
    # But we can use the fact that the reverse graph from X is a tree (if we ignore
    # multiple incoming edges) or a DAG? Actually, the reverse graph is a directed
    # graph where each node can have multiple incoming edges (since P and Q are
    # permutations, each node has exactly one incoming red edge and one incoming blue
    # edge? No: P is a permutation, so each node has exactly one incoming red edge
    # (from the node i such that P_i = that node). Similarly for Q. So in the reverse
    # graph (considering both colors), each node has at most 2 incoming edges.
    # The subgraph induced by S (nodes that can reach X) might have cycles.
    # But we can compute the set of nodes that are on some path from an initial ball
    # to X. This is the set of nodes that are reachable from the initial balls in the
    # forward direction, intersected with S.
    # We can do a BFS/DFS from the initial balls in the forward direction, but stop
    # when we reach X. However, we need to avoid infinite loops. Since we only follow
    # forward edges from nodes that can reach X, and we stop when we reach X, we can
    # just follow the path until we reach X, and mark all visited nodes.
    # But a node might be visited by multiple balls. We need to visit each node at most
    # once. We can do a DFS with memoization? Since each node has out-degree 1 for
    # each color, we can compute for each node the path to X for red and blue.
    # Actually, we can precompute for each node and each color, the sequence of nodes
    # until X, but that's too much memory.
    # Alternatively, we can perform a BFS from X in the reverse graph to find S,
    # and then the answer is simply the number of nodes in S that are not X and are
    # reachable from some initial ball in the forward direction within S.
    # But we can do a multi-source BFS from the initial balls in the forward direction,
    # but only within S, and stop at X. However, we need to ensure we don't get stuck
    # in cycles. Since we only care about paths that end at X, and all nodes in S
    # can reach X, we can just follow the forward edges until we reach X, and mark
    # the nodes. But we need to do this efficiently.
    # Since the graph is functional for each color, we can compute for each node its
    # "distance" to X along the forward edge, but there might be cycles.
    # Actually, we can use the fact that the set S is exactly the set of nodes that
    # can reach X. In the forward direction, from any node in S, following the forward
    # edge will eventually reach X (possibly after traversing a cycle that includes X).
    # So we can compute for each node in S the set of nodes on the path to X.
    # We can do a DFS from each initial ball, but we need to avoid repeated work.
    # We can use a stack and a visited set for the DFS from initial balls. When we
    # visit a node, if we haven't computed its path to X yet, we compute it recursively.
    # But this could still be O(N^2) in the worst case (e.g., a long chain).
    # However, since each node has out-degree 1, the total number of edges traversed
    # across all DFS calls is O(N) if we memoize the result. We can compute for each
    # node a boolean: "is this node on the path from some initial ball to X?".
    # Actually, we want the set of nodes that are on at least one path from an
    # initial ball to X. We can compute this by starting from initial balls and
    # following forward edges until we reach X, marking all nodes we visit. But if
    # we do this naively for each ball, we might revisit nodes. So we should do a
    # single pass that marks nodes as we visit them.
    # Since the graph is deterministic, we can do a DFS from each unvisited initial
    # ball, following the forward edge of the appropriate color, and we stop when we
    # reach a node that is already marked (either as visited or as not leading to X?).
    # But we need to handle cycles. If we encounter a cycle, we need to know that
    # it can reach X. Since we only start from nodes in S (we should only start from
    # nodes that have balls and are in S), and all nodes in S can reach X, any cycle
    # we encounter is entirely within S. We can break the cycle by marking all nodes
    # in the cycle as "on the path" if they are reachable from an initial ball.
    # This is getting complicated.
    # Let's look at the problem constraints: A_i, B_i are 0 or 1. So there are at
    # most 2N balls. But N is 2e5.
    # I recall the solution to this problem (it's from AtCoder ABC 320 F? No, it's
    # "Balls and Boxes" from AtCoder Beginner Contest 213? Actually, it's "Balls" from
    # AtCoder Regular Contest 109? Let me think.
    # I think it's AtCoder ABC 320 F? No, ABC 320 F is "Fuel Round Trip".
    # Maybe it's from AtCoder Grand Contest? 
    # Wait, I remember a problem: "Balls and Boxes" where you have two permutations
    # and you want to collect balls in one box. The answer is the size of the set of
    # nodes that can reach the target via the reverse permutations, minus 1, but only
    # if there is at least one ball. Actually, in the sample 1, answer is 4. Let's
    # compute S for sample 1.
    # Sample 1: N=5, X=3.
    # A = [0,1,0,1,0]
    # B = [0,0,1,0,1]
    # P = [4,1,2,3,5]
    # Q = [3,4,5,2,1]
    # Reverse edges:
    # P: 1->4, 2->1, 3->2, 4->3, 5->5.
    # So rev_red: 1:[2], 2:[3], 3:[4], 4:[1], 5:[5].
    # Q: 1->3, 2->4, 3->5, 4->2, 5->1.
    # So rev_blue: 1:[5], 2:[4], 3:[1], 4:[2], 5:[3].
    # BFS from X=3:
    # visited: 3.
    # from 3: rev_red: 4 -> visited 4; rev_blue: 1 -> visited 1.
    # from 4: rev_red: 1 (already); rev_blue: 2 -> visited 2.
    # from 1: rev_red: 2 (already); rev_blue: 5 -> visited 5.
    # from 2: rev_red: 3 (already); rev_blue: 4 (already).
    # from 5: rev_red: 5 (already); rev_blue: 3 (already).
    # So S = {1,2,3,4,5}. All boxes. |S|-1 = 4. That matches the answer.
    # So in this case, |S|-1 works.
    # In sample 2, no balls, S from X=3? Let's compute: BFS from 3, same S = {1,2,3,4,5}.
    # But answer is 0. So we need to check if there are any balls. If no balls, answer 0.
    # In sample 3: N=2, X=2. A=[1,1], B=[1,1]. P=[1,2], Q=[1,2].
    # Reverse: rev_red: 1:[1], 2:[2]. rev_blue: same.
    # BFS from 2: visited 2. from 2: rev_red:2 (already), rev_blue:2 (already). So S={2}.
    # Boxes with balls: 1 has balls, but 1 not in S. So impossible. Answer -1.
    # That matches.
    # In sample 4: answer 8. Let's check if |S|-1 is 8.
    # We need to compute S. Probably |S|=9 or 8+1=9. So likely |S|-1 works when there are balls.
    # So the pattern is: if no balls, answer 0. Else, answer |S|-1, provided all balls are in S.
    # But wait, in the cycle example where X has a ball and we want 0 operations, |S|-1 would give 1, which is wrong. So there must be an additional condition: we only count boxes that are "necessary". In that example, S includes X and another box. The other box is in S, but it has no balls and we don't need to operate on it. So we should not count it.
    # How to distinguish? The other box is in S because it can reach X (via the cycle). But it doesn't have any balls and we never need to forward any balls through it. So we should not include it in the count.
    # In the BFS from X, we include all nodes that can reach X. But some of these nodes might not be on the path of any ball. We only want to count nodes that are on the forward path from some initial ball to X.
    # So we need to compute the set T = { nodes that are on a forward path from some initial ball to X }.
    # Then the answer is |T| - 1 (excluding X if X is in T, but we don't operate on X).
    # But wait: if X is in T, we don't operate on it, so the number of operations is the number of nodes in T other than X. So answer = |T| - 1 if X in T, else |T|. But since X is the target, we can assume X is in T if there are balls? Not necessarily: if all balls are already at X, then T = {X}, answer 0.
    # So algorithm:
    # 1. Find S = set of nodes that can reach X via reverse BFS.
    # 2. Check that all boxes with balls are in S. If not, print -1.
    # 3. If no balls, print 0.
    # 4. Otherwise, we need to find the set T of nodes that are on the forward path from some initial ball to X. But we can just compute the size of T minus 1.
    # How to compute T efficiently? We can start from all boxes that have balls, and follow forward edges (appropriate color) until we reach X. We mark all visited nodes. Since we only follow edges within S (because we already checked all balls are in S, and following forward from a node in S stays in S? Not necessarily: following forward from a node in S might go to a node not in S? Actually, if a node is in S, it can reach X. Following forward from it, the next node might not be in S? That would mean the next node cannot reach X, which is impossible because the path from the current node to X goes through the next node. So the next node is also in S. So forward edges from S stay in S.
    # So we can do a DFS from each initial ball, following the forward edge of the correct color, and we will eventually reach X. We can use a visited set to avoid revisiting nodes. Since the graph is functional, each node has at most one outgoing edge per color. We can precompute for each node and each color the next node.
    # We can do a simple iterative process: for each box i with a ball (say red), we start at i, then while i != X: mark i as needed, i = P[i]. Then mark X? No, we don't operate on X. So we mark all nodes except X.
    # But we need to do this for both colors. We can maintain a set needed = set(). For each initial ball (i, color), we traverse: cur = i; while cur != X: needed.add(cur); cur = next[cur] (using P for red, Q for blue). This will mark all nodes on the path from i to X. However, we might traverse the same path multiple times. To avoid O(N^2), we can use memoization: once we have computed the set of nodes on the path from a node to X, we can store it. But storing a set for each node is too much.
    # Instead, we can note that if we traverse from i, we will visit a sequence of nodes. If we encounter a node that we have already processed, we can skip. We can use a "visited" array for the traversal: when we start from i, we follow forward until we hit a node that is already marked as "processed" (i.e., we have already determined the path from it to X). But we need to know which nodes are on the path from that processed node to X. That would require storing the path or a boolean.
    # Actually, we can use a DFS with recursion and memoization of the "needed" status. But we can also do a topological order: the graph of forward edges restricted to S is a functional graph. Since every node in S can reach X, the graph consists of cycles that include X, and trees feeding into them. We can process nodes in reverse topological order: start from X, go backwards in the reverse graph, and count how many nodes have balls in their subtree? Not exactly.
    # Another approach: we can compute the number of operations as the number of edges in the minimal set of operations. Actually, the minimum number of operations is exactly the number of boxes that are operated on. Each operation is on a box that currently has balls. The set of boxes that are operated on is exactly the set of boxes that are on the path from some initial ball to X, excluding X. So we just need the size of that set.
    # We can compute this by doing a BFS from X in the reverse graph, but only following edges that are "activated" by balls. Alternatively, we can do a multi-source BFS from all initial balls in the forward direction, but we stop when we reach X or when we reach a node that is already visited. However, we need to be careful: if a node is visited by multiple paths, we should only count it once.
    # Since the forward graph is a permutation for each color, the set of nodes reachable from a set of sources in the forward direction (ignoring color) is not simply a tree because each node has two possible forward edges (one for red, one for blue). But a specific ball only follows one edge.
    # We can treat red and blue separately. For red balls, we have a set of sources R (boxes with red balls). We want to find the set of nodes that are on a path from some source in R to X, following P. This is the set of nodes that are reachable from R in the forward graph, intersected with S. Since P is a permutation, the forward graph is a collection of cycles. The set of nodes that can reach X via P is exactly the set of nodes in the same cycle as X (in the permutation P) that are "before" X in the cycle? Actually, in a permutation, every node can reach every other node in the same cycle. So the set of nodes that can reach X via P is exactly the cycle containing X in the permutation P. Similarly for Q.
    # So the set S is the union of the cycle containing X in P and the cycle containing X in Q. But wait, we also have boxes that are not in those cycles? No, because P and Q are permutations, so every node is in some cycle. The reverse BFS from X will visit all nodes in the cycle of X in P and all nodes in the cycle of X in Q, and also nodes that are in cycles that can reach X? But in a permutation, you can only reach nodes in the same cycle. So if a node is not in the same cycle as X in P, it cannot reach X via P alone. But we have both P and Q. So a node can reach X if it is in the cycle of X in P or in the cycle of X in Q, or if it is in a node that can reach such a cycle? But since P and Q are permutations, from any node, following P or Q will eventually cycle. So a node can reach X if and only if it is in the same cycle as X in P or in the same cycle as X in Q. Because if it's in a different cycle in P, following P will never reach X. So S is exactly the union of the cycle containing X in P and the cycle containing X in Q. But is that true? Let's check sample 1: P permutation: (1->4, 4->3, 3->2, 2->1) and 5->5. So cycle containing 3: 3->2->1->4->3. That's 4 nodes. Q permutation: 1->3, 3->5, 5->1, and 2->4, 4->2. So cycle containing 3: 3->5->1->3. That's 3 nodes. Union: {1,2,3,4,5} = all nodes. That matches S.
    # In sample 2, same P and Q, S is all nodes, but no balls, so answer 0.
    # So S is simply the union of the cycles containing X in P and Q. That is much simpler! Since P and Q are permutations, the reverse BFS from X will exactly visit all nodes in the cycle of X in P (because in the reverse graph of a cycle, you can reach all nodes in the cycle) and all nodes in the cycle of X in Q. There are no other nodes because from any node, following P or Q will stay in its cycle, and if it's not in the cycle of X, it can never reach X.
    # So we can compute the cycle containing X in P: start from X, follow P until we return to X, mark all visited. Similarly for Q. Then S is the union.
    # Now, the set of boxes that need to be operated on: we need to find the set of boxes that are on the forward path from some initial ball to X. Since the forward path is just following P or Q, and we know that any ball starting in S will eventually reach X by following its color's permutation. The path is just the sequence of nodes in the cycle until hitting X.
    # So for a red ball at node i, its path to X is: starting from i, follow P until you reach X. This path is unique and is a subset of the cycle of X in P. The nodes on this path are exactly the nodes in the cycle of X in P that are "between" i and X (including i, excluding X if we don't operate on X).
    # So the set of nodes that need to be operated on for red balls is the union of the paths from all red ball sources to X in the cycle of X in P. Similarly for blue in the cycle of X in Q.
    # Then the answer is the size of the union of these two sets (excluding X, but X is in both cycles, so we don't count it).
    # We need to compute this efficiently. For a cycle, if we have multiple sources, the union of paths to a target X is simply the set of nodes that are "before" X in the cycle order? Actually, if we have a cycle and a target X, the path from any node i to X is the sequence of nodes from i to X following the cycle direction. The union of all such paths from a set of sources is the set of nodes that are on the path from the "farthest" source to X? More precisely, if we have a cycle with a target X, and a set of sources S_red, then the union of paths from S_red to X is the set of nodes that are on the path from the "last" source in the cycle order to X. But we need to define the order. In a cycle, we can define the distance from each node to X: the number of steps following P to reach X. For nodes in the cycle, the distance is well-defined. The path from i to X consists of all nodes j such that dist(j) <= dist(i) and j is on the path from i to X? Actually, if we start at i and follow P, we visit nodes with decreasing distance to X (until distance 0 at X). So the path is the set of nodes with distance in [0, dist(i)] that are on the same "arc" from i to X. But since it's a cycle, there is only one path from i to X (if we don't go the other way around). Actually, in a cycle, there are two paths from i to X: one going forward (following P) and one going backward (following P^{-1}). But since P is a permutation, the forward map is defined. The operation sends red to P_i. So the ball must follow P. So it will go in the direction of P. So the path is uniquely determined: it follows the cycle in the direction of P until it hits X.
    # So for each node i in the cycle of X in P, we can compute the distance d(i) = number of steps to reach X following P. Then the path from i to X is the set of nodes j such that d(j) is in [0, d(i)] and j is on the forward orbit from i. But actually, since it's a cycle, if we start at i and follow P, we will visit a sequence of nodes. The distances to X along the way are d(i), d(P(i)), d(P^2(i)), ... until we hit 0. So the path is exactly the set of nodes with distance d(i), d(i)-1, ..., 0. But are these nodes distinct? Yes, until we hit X. So the path from i to X is the set of nodes on the "ray" from i to X.
    # Now, if we have a set of sources S_red, the union of their paths to X is the set of all nodes j such that there exists a source i with d(i) >= d(j) and j is on the path from i to X. This is equivalent to: the union is the set of nodes j with d(j) <= max_{i in S_red} d(i)? Not exactly, because the path from i to X might not include all nodes with smaller distance. For example, if the cycle is 1->2->3->4->1, and X=1. Then distances: d(1)=0, d(2)=1, d(3)=2, d(4)=3. Paths:
    # from 2: {2,1}
    # from 3: {3,2,1}
    # from 4: {4,3,2,1}
    # Union of {2,3} = {3,2,1}. So it includes all nodes with distance <= 2? Yes.
    # What if sources are {3,4}? Union is {4,3,2,1} which is all.
    # What if sources are {2,4}? Union is {4,3,2,1}.
    # Actually, in a cycle, if we have multiple sources, the union of paths to X is exactly the set of nodes that are on the path from the "farthest" source to X. But is that always true? Consider a cycle of length 5: 1->2->3->4->5->1, X=1. Distances: d(1)=0, d(2)=1, d(3)=2, d(4)=3, d(5)=4. Suppose sources are {3,5}. Path from 3: {3,2,1}. Path from 5: {5,4,3,2,1}. Union = {5,4,3,2,1} which is the path from 5. So yes, it's the path from the source with the maximum distance. But is the maximum distance always well-defined? Yes, since distances are non-negative integers.
    # So for red balls, the set of nodes that need to be operated on (excluding X) is the set of nodes on the path from the red source with the maximum distance to X in the cycle of X in P. If there are no red balls, this set is empty.
    # Similarly for blue balls in the cycle of X in Q.
    # Then the answer is the size of the union of these two sets.
    # But wait, is it possible that a node appears in both cycles? Yes, if a node is in both the cycle of X in P and the cycle of X in Q. Then we don't need to operate on it twice. So we take the union of the two sets.
    # So the algorithm:
    # 1. Find the cycle containing X in P. Compute the distance from each node in that cycle to X (following P).
    # 2. Find the cycle containing X in Q. Compute the distance from each node in that cycle to X (following Q).
    # 3. For red balls: find the maximum distance among nodes that have a red ball. Let max_red = that max distance. Then the set of nodes to operate on for red is all nodes in the P-cycle with distance <= max_red, excluding X. But careful: is it all nodes with distance <= max_red? Yes, because if max_red is the maximum distance, then for any node j with distance d(j) <= max_red, there is a source i with d(i) >= d(j), but is j on the path from i to X? Not necessarily. For example, consider a cycle where the sources are not contiguous. But in a cycle, the path from i to X is contiguous in the cycle order. If we have two sources with distances d1 and d2, the union of their paths is the path from the one with larger distance. Because the path from the larger distance includes the path from the smaller distance. So indeed, the union is the set of all nodes on the path from the "farthest" source to X. And that path is exactly the set of nodes with distance from that source down to 0. So it is {nodes with distance in [0, max_red]}. But wait, is it all nodes with distance <= max_red? Yes, because as you go from the farthest source to X, you pass through all distances from max_red down to 0. So the set is exactly the set of nodes j in the cycle such that d(j) <= max_red. But note that there might be nodes in the cycle with distance > max_red that are not on the path from the farthest source? Actually, if the farthest source has distance max_red, then all nodes with distance > max_red are not on the path from that source, because the path goes from max_red down to 0. So the set is exactly the nodes with distance <= max_red.
    # So for red, the set is { i in P-cycle : d_P(i) <= max_red_dist } \ {X}.
    # Similarly for blue: { i in Q-cycle : d_Q(i) <= max_blue_dist } \ {X}.
    # Then the answer is the size of the union of these two sets.
    # But we must also consider that we might not need to operate on a node if it is in the set but has no balls and is not on the path of any ball? Actually, by this construction, if a node has distance <= max_red_dist, it is on the path from the farthest red source. So it is on the path of some red ball. So it will receive a ball and need to be operated on. So it's necessary.
    # However, is it possible that a node is in the set but we don't need to operate on it because the ball that would pass through it actually doesn't? No, because the ball from the farthest source will definitely pass through all nodes with smaller distance. So they will receive balls.
    # So this seems correct.
    # Let's test with the cycle example where X has a ball: N=2, X=1, P: 1->2, 2->1. Q: 1->2, 2->1. A: 1 at 1, B: 0. So red ball at 1. P-cycle: {1,2}. d(1)=0, d(2)=1. max_red_dist = 0 (since ball at 1 has distance 0). So set_red = nodes with d<=0 minus X = empty. So answer 0. That matches.
    # If red ball at 2: d=1, max_red=1, set_red = {2} (d<=1 minus X). Answer 1. That matches earlier.
    # So the algorithm is:
    # 1. Find cycle of X in P: traverse P starting from X until back to X. Record nodes and distances (0 for X, 1 for P(X), etc.).
    # 2. Find cycle of X in Q: similarly.
    # 3. For red: if any box i has A_i=1, find the maximum distance among those i that are in the P-cycle. If a red ball is in a box not in the P-cycle, then it's impossible (but we already checked all balls are in S, and S is union of cycles, so it must be in the cycle). So max_red = max(d_P(i) for i with A_i=1 and i in P-cycle). If no red balls, max_red = -1.
    # 4. For blue: similarly.
    # 5. Then the set of nodes to operate on is: {i in P-cycle: d_P(i) <= max_red} union {i in Q-cycle: d_Q(i) <= max_blue}, minus X.
    # But careful: if max_red is -1, the set is empty. Similarly for blue.
    # The answer is the size of this union.
    # Complexity: O(N) to find cycles and compute distances.
    # Let's test on sample 1.
    # P-cycle: start at 3. P(3)=2, P(2)=1, P(1)=4, P(4)=3. So cycle: 3,2,1,4. Distances: d(3)=0, d(2)=1, d(1)=2, d(4)=3.
    # Red balls: A: box2=1, box4=1. So red sources: 2 (d=1), 4 (d=3). max_red = 3.
    # Set_red: nodes with d<=3: all nodes in cycle: {3,2,1,4}. Exclude X=3: {2,1,4}. Size 3.
    # Q-cycle: start at 3. Q(3)=5, Q(5)=1, Q(1)=3. So cycle: 3,5,1. Distances: d(3)=0, d(5)=1, d(1)=2.
    # Blue balls: B: box3=1, box5=1. So blue sources: 3 (d=0), 5 (d=1). max_blue = 1.
    # Set_blue: nodes with d<=1: {3,5}. Exclude X=3: {5}. Size 1.
    # Union: {2,1,4} U {5} = {1,2,4,5}. Size 4. That's the answer.
    # So this works!
    # Now, we must also consider that we might not need to operate on some nodes in the set if they are not on the path? But the set is defined as all nodes with distance <= max_dist, which are exactly the nodes on the path from the farthest source. So they are all on the path. So we need to operate on all of them.
    # But wait: what if a node is in the set but it is not on the path from the farthest source because the cycle order is not contiguous? In a cycle, the path from a source to X is contiguous along the cycle direction. The set of nodes with distance <= max_dist is exactly the set of nodes that are "before" the farthest source in the cycle order? Actually, if you start at the farthest source and follow P, you will visit nodes with decreasing distance. So you will visit all nodes with distance from max_dist down to 0. So yes, the set is exactly that.
    # So the answer is the number of nodes in the union of these two sets (excluding X).
    # Implementation details:
    # We need to map each node to its distance in the P-cycle. We can do this by traversing the P-cycle once and storing distances in a dictionary or array of size N+1, initialized to -1.
    # Similarly for Q.
    # Then compute max_red and max_blue.
    # Then count: for i in 1..N, if i != X, and ((distP[i] != -1 and distP[i] <= max_red) or (distQ[i] != -1 and distQ[i] <= max_blue)), then count.
    # But careful: what if max_red is -1? Then distP[i] <= -1 is false. So no contribution.
    # What if max_red is 0? Then only nodes with distance 0, which is X. Exclude X, so no nodes. So that matches.
    # So the condition is: (max_red != -1 and distP[i] != -1 and distP[i] <= max_red) or (max_blue != -1 and distQ[i] != -1 and distQ[i] <= max_blue).
    # And i != X.
    # Let's test with the impossible case: sample 3. N=2, X=2. P: 1->1, 2->2. Q: 1->1, 2->2.
    # P-cycle from X=2: just {2}. distP[2]=0, others -1.
    # Q-cycle from X=2: just {2}. distQ[2]=0.
    # Red balls: A: 1,1. Both in P-cycle? No, only 2 is in P-cycle. So red ball at 1 is not in S. So we will check all balls in S? Our algorithm: we need to check that every box with a ball is in the P-cycle or Q-cycle? Actually, S is the union of the two cycles. So we can check: if A[i]=1 and i not in P-cycle, then impossible. Similarly for B and Q-cycle. That is exactly the condition that all balls are in S. So we can do that check first.
    # So algorithm:
    # - Compute distP for P-cycle starting at X: traverse P until we return to X, assign increasing distances.
    # - Compute distQ for Q-cycle starting at X: similarly.
    # - Check for each i: if A[i]=1 and distP[i]==-1, print -1 and return.
    #   if B[i]=1 and distQ[i]==-1, print -1 and return.
    # - If no balls (sum A and B all zero), print 0 and return.
    # - Compute max_red = max(distP[i] for i in 1..N if A[i]==1 and distP[i]!=-1). Default -1.
    # - Compute max_blue = max(distQ[i] for i in 1..N if B[i]==1 and distQ[i]!=-1). Default -1.
    # - Count = number of i such that i != X and ( (max_red != -1 and distP[i]!=-1 and distP[i] <= max_red) or (max_blue != -1 and distQ[i]!=-1 and distQ[i] <= max_blue) ).
    # - Print count.
    # This should be O(N).
    # Let's test on sample 4: answer 8. We can trust it.
    # Edge case: what if X is not in a cycle with itself? But P and Q are permutations, so X is in some cycle. The cycle containing X is what we traverse.
    # What if the cycle is just {X}? Then distP[X]=0, others -1. That's fine.
    # This is a beautiful solution.
    # Let's implement.
    
    # Build distP
    distP = [-1] * (N + 1)
    cur = X
    d = 0
    while distP[cur] == -1:
        distP[cur] = d
        d += 1
        cur = P[cur]
    
    # Build distQ
    distQ = [-1] * (N + 1)
    cur = X
    d = 0
    while distQ[cur] == -1:
        distQ[cur] = d
        d += 1
        cur = Q[cur]
    
    # Check all balls are in S
    for i in range(1, N + 1):
        if A[i] == 1 and distP[i] == -1:
            print(-1)
            return
        if B[i] == 1 and distQ[i] == -1:
            print(-1)
            return
    
    # Check if no balls
    total_balls = sum(A) + sum(B)
    if total_balls == 0:
        print(0)
        return
    
    max_red = -1
    for i in range(1, N + 1):
        if A[i] == 1:
            # distP[i] is guaranteed != -1 by check above
            if distP[i] > max_red:
                max_red = distP[i]
    
    max_blue = -1
    for i in range(1, N + 1):
        if B[i] == 1:
            if distQ[i] > max_blue:
                max_blue = distQ[i]
    
    count = 0
    for i in range(1, N + 1):
        if i == X:
            continue
        if max_red != -1 and distP[i] != -1 and distP[i] <= max_red:
            count += 1
        elif max_blue != -1 and distQ[i] != -1 and distQ[i] <= max_blue:
            count += 1
    
    print(count)

if __name__ == "__main__":
    solve()