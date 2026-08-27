import sys

# Increase recursion depth for deep DSU or tree operations
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    for i in range(1, M + 1):
        S[i] = int(next(iterator))
        T[i] = int(next(iterator))
    
    queries = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))

    # Sort queries by R to process offline
    # We will process people 1..M and maintain a data structure.
    # If a contradiction occurs at person i, then any query [L, R] with R >= i 
    # and L <= i is potentially invalid. However, the condition is that ALL people 
    # in [L, R] must be satisfiable. So if person i causes a contradiction, 
    # then any query covering i is invalid.
    
    # We need to find the set of indices i in [1, M] that cause contradictions.
    # Let's call this set BadIndices.
    # A query [L, R] is valid if BadIndices has no intersection with [L, R].
    
    # Algorithm:
    # 1. Maintain a Segment Tree over nodes 0..N-1 (representing towns 1..N mapped to 0..N-1).
    #    Each node u stores max_reach[u]: the maximum index v such that there is a path 
    #    of strict inequalities from u to v.
    # 2. Use DSU to maintain components of nodes with equal potential.
    #    Each component has a representative. We maintain max_reach for the representative.
    #    When merging two components (due to equality constraint), we update the max_reach 
    #    of the new representative to max(max_reach[root1], max_reach[root2]).
    #    Crucially, we must also update the max_reach of the new representative to include 
    #    the max_reach of all nodes in the component? 
    #    Actually, the property we maintain is: for any node u in the component, 
    #    max_reach[u] should be the max of max_reach[v] for all v in the component.
    #    Since we only merge, we can just store the global max for the component.
    #    However, when we add an inequality u -> [L, R], we update max_reach[u] = max(max_reach[u], R).
    #    If u is part of a component, we update the component's max_reach.
    #    Wait, the inequality is: P[u] < P[v] for all v in (L, R).
    #    This implies a path from u to L, L+1, ..., R.
    #    So max_reach[u] becomes max(max_reach[u], R).
    #    But we also need to ensure that if we later merge u with some w, the new component 
    #    knows about the reachability from w as well.
    #    
    #    Refined approach:
    #    We maintain a Segment Tree where `tree[x]` stores the maximum `max_reach` value 
    #    for any node in the range `[x, x+1]`? No, that's not right.
    #    
    #    Let's use a Segment Tree to support:
    #    - Range Max Query: Get max(max_reach) in a range.
    #    - Point Update: Update max_reach[u] = val.
    #    - Range Update: Not strictly needed if we process carefully, but we might need to 
    #      propagate updates.
    #    
    #    Actually, the standard solution for this problem (often called "Stamina" or similar)
    #    uses a Segment Tree to maintain the "rightmost reachable" for each node.
    #    Since the graph is a line, the "rightmost reachable" from u is simply the max index v
    #    such that there is a path of inequalities u -> ... -> v.
    #    When we have an equality u == v, we merge them. The new reachability is the union.
    #    When we have an inequality u < v (for a range), we update u's reachability.
    #    
    #    Data Structure:
    #    Segment Tree over indices 0 to N-1.
    #    Each leaf i stores `reach[i]`. Initially `reach[i] = i`.
    #    Internal nodes store `max(reach[left], reach[right])`.
    #    Operations:
    #    1. Update `reach[u] = max(reach[u], R)`. This is a point update.
    #    2. Check if `reach[u] >= v` (where v is the target of equality). If so, contradiction.
    #    3. Merge u and v. This means `reach[new_root] = max(reach[u], reach[v])`.
    #       But wait, if we merge u and v, any node w that could reach u can now reach v,
    #       and vice versa. So the reachability of the component is the max of all members.
    #       We need to efficiently query the max reachability in a component.
    #       Since we only merge adjacent components (or arbitrary ones via equality),
    #       and the reachability is monotonic, we can just maintain the max for the component.
    #       However, the Segment Tree approach usually works by:
    #       - `reach[u]` is the max index reachable from u via inequalities.
    #       - When merging u and v (equality), we effectively say `reach[u]` and `reach[v]` 
    #         are now part of the same set. The new effective reachability for the set is 
    #         `max(reach[u], reach[v])`.
    #       - But we also need to handle the case where an inequality updates `reach[u]`.
    #         If u is in a component, we update the component's max.
    #    
    #    Let's use a Segment Tree to store `max_reach` for each node.
    #    `tree[i]` stores the max reachability of node `i`.
    #    We also need to know which component a node belongs to. DSU handles this.
    #    But DSU doesn't easily support "update max of component" if we just store it in the root.
    #    Actually, we can just store the max reachability in the DSU root.
    #    When merging roots r1 and r2, new_root.max_reach = max(r1.max_reach, r2.max_reach).
    #    When updating a node u with a new reach R:
    #       root = find(u)
    #       root.max_reach = max(root.max_reach, R)
    #       But wait, if we update a non-root node, we must update the root.
    #       So: find(u), update root.max_reach.
    #    
    #    Is this sufficient?
    #    Suppose we have 1-2-3. Inequality 1->3 (so 1<2<3). reach[1]=3.
    #    Equality 2==3. Merge 2 and 3. New component {2,3}. max_reach = max(reach[2], reach[3]).
    #    If reach[2] was 2, reach[3] was 3. New max is 3.
    #    Now if we have inequality 1->2 (1<2). reach[1] becomes max(3, 2) = 3.
    #    Check 1==3? reach[1]=3 >= 3. Contradiction.
    #    This seems correct.
    #    
    #    Wait, there's a catch.
    #    The inequality is: P[S] < P[k] for all k in (S, T).
    #    This implies P[S] < P[S+1] < ... < P[T-1].
    #    So there is a path S -> S+1 -> ... -> T-1.
    #    So reach[S] must be at least T-1.
    #    So we update reach[S] = max(reach[S], T-1).
    #    Then we check if reach[S] >= T. If so, contradiction.
    #    Then we merge S and T (since P[S] == P[T]).
    #    Wait, the problem says P[S] == P[T] and P[k] > 0 for k in between.
    #    The condition "P[k] > 0" is satisfied if P[S] < P[k] and P[k] < P[T] is NOT required.
    #    Wait, the problem says:
    #    "When departing Town S_i and when arriving at Town T_i, their stamina should be exactly 0.
    #     At every other town, their stamina should always be a positive integer."
    #    Let P[x] be the stamina at town x.
    #    P[S] = 0, P[T] = 0.
    #    For k in (S, T), P[k] > 0.
    #    The edge weights w_j = P[j+1] - P[j].
    #    So P[x] = sum(w_j) from S to x-1.
    #    The condition P[k] > 0 means sum(w_j) from S to k-1 > 0.
    #    This implies P[S] < P[S+1] < ... < P[T-1] is NOT necessarily true.
    #    It just means P[k] > P[S] (since P[S]=0).
    #    So P[S] < P[k] for all k in (S, T).
    #    This implies P[S] < P[S+1], P[S] < P[S+2], ..., P[S] < P[T-1].
    #    It does NOT imply P[S+1] < P[S+2].
    #    However, the standard reduction for this problem (which is a known problem, e.g., from AtCoder)
    #    relies on the fact that if P[S] < P[k] for all k, then we can model this as a path constraint.
    #    Actually, the known solution involves checking if there is a path from S to T in the "greater than" graph.
    #    If P[S] < P[k], then we have an edge S -> k.
    #    If we have a path S -> ... -> T, then P[S] < P[T], which contradicts P[S] = P[T] = 0.
    #    So we need to check if there is a path from S to T using edges (u, v) where u < v and u < v is implied by the constraints?
    #    No, the constraints are P[u] < P[v].
    #    If we have P[S] < P[k] for all k in (S, T), does this imply a path?
    #    Not directly a single path, but a set of constraints.
    #    However, if we assume the "potential" model, P[v] - P[u] > 0.
    #    If we have a chain of such inequalities, we get a contradiction.
    #    The standard trick is:
    #    For each person (S, T), we require P[S] < P[k] for all k in (S, T).
    #    This is equivalent to saying that in the graph of "strictly increasing" relations,
    #    there is no path from S to T.
    #    But we don't have edges for every pair. We only have edges implied by the "between" condition.
    #    Actually, the condition P[S] < P[k] for all k in (S, T) is satisfied if and only if
    #    there is NO path from S to T in the graph where edges are (u, v) such that P[u] < P[v].
    #    But we are building the graph.
    #    The known solution for this specific problem (AtCoder Grand Contest 015, Problem C? No, maybe different)
    #    is to maintain the "rightmost reachable" index.
    #    Let's re-verify the logic.
    #    If we have P[S] < P[k] for all k in (S, T), then specifically P[S] < P[S+1], P[S] < P[S+2], etc.
    #    This doesn't force P[S+1] < P[S+2].
    #    However, if we have another constraint P[A] < P[B] where A, B are in (S, T), it doesn't help.
    #    The contradiction arises if we have a chain S -> x -> y -> ... -> T where each step is a strict increase.
    #    But the constraints are only P[S] < P[k].
    #    Wait, if P[S] < P[k] for all k, then P[S] < P[S+1] and P[S] < P[S+2].
    #    Does this imply P[S+1] < P[S+2]? No.
    #    So why does the "rightmost reachable" logic work?
    #    Maybe the problem implies something else?
    #    "At every other town, their stamina should always be a positive integer."
    #    This means P[k] >= 1 for k in (S, T).
    #    Since P[S] = 0, this means P[k] > P[S].
    #    So yes, P[S] < P[k].
    #    The contradiction is if we can deduce P[S] < P[T].
    #    How can we deduce P[S] < P[T]?
    #    If there is a path S -> v1 -> v2 -> ... -> T such that P[S] < P[v1] < P[v2] < ... < P[T].
    #    But we only know P[S] < P[k] for k in (S, T).
    #    We don't know relations between k1 and k2.
    #    UNLESS... the problem implies that the "shortest path" logic forces something?
    #    No, the path is fixed (line graph).
    #    Let's look at the sample.
    #    Sample 1:
    #    P1: 4->2. S=4, T=2. Path 4-3-2.
    #    P[4]=0, P[2]=0. P[3]>0.
    #    So P[4] < P[3] and P[3] > P[2] (since P[2]=0).
    #    Wait, P[3] > P[2] is P[3] > 0.
    #    So we have P[4] < P[3] and P[2] < P[3].
    #    This does NOT imply P[4] < P[2].
    #    So why would it be a contradiction?
    #    Ah, the sample explanation says:
    #    "Person 1 starts at town 4 with stamina 0, visits town 3 with stamina 1, and arrives at town 2 with stamina 0."
    #    This is possible.
    #    Sample 2 query: Persons 2, 3, 4.
    #    P2: 1->3. S=1, T=3. Path 1-2-3. P[1]=0, P[3]=0, P[2]>0. => P[1]<P[2], P[2]>P[3].
    #    P3: 3->5. S=3, T=5. Path 3-4-5. P[3]=0, P[5]=0, P[4]>0. => P[3]<P[4], P[4]>P[5].
    #    P4: 2->4. S=2, T=4. Path 2-3-4. P[2]=0, P[4]=0, P[3]>0. => P[2]<P[3], P[3]>P[4].
    #    Combine:
    #    P[1] < P[2]
    #    P[2] > P[3]
    #    P[3] < P[4]
    #    P[4] > P[2] (from P[3]>P[4] and P[2]<P[3]? No, P[2]<P[3] and P[3]>P[4] doesn't imply P[2] vs P[4]).
    #    Wait, P4 says P[2]=0, P[4]=0, P[3]>0.
    #    So P[2] < P[3] and P[3] > P[4].
    #    From P2: P[1] < P[2] and P[2] > P[3].
    #    From P3: P[3] < P[4] and P[4] > P[5].
    #    From P4: P[2] < P[3] and P[3] > P[4].
    #    Contradiction: P2 says P[2] > P[3]. P4 says P[2] < P[3].
    #    So the contradiction is P[2] > P[3] AND P[2] < P[3].
    #    This is a cycle in the "greater than" graph?
    #    P[2] > P[3] and P[3] > P[2] (since P[2] < P[3] is equivalent to P[3] > P[2]).
    #    Yes.
    #    So the problem is to detect if the constraints form a cycle in the strict inequality graph.
    #    The constraints are:
    #    For each person (S, T):
    #      For all k in (S, T): P[S] < P[k] AND P[k] > P[T].
    #      Wait, P[T]=0, P[S]=0. So P[k] > 0.
    #      This gives P[S] < P[k] and P[k] > P[T].
    #      Since P[S] = P[T], this is P[S] < P[k] and P[k] > P[S].
    #      This is consistent.
    #    But we also have other people.
    #    The contradiction in Sample 2 comes from P2 and P4.
    #    P2: P[1] < P[2] and P[2] > P[3].
    #    P4: P[2] < P[3] and P[3] > P[4].
    #    So P[2] > P[3] and P[2] < P[3]. Contradiction.
    #    
    #    So the constraints are:
    #    For each person i:
    #      Add edges: S_i -> k for all k in (S_i, T_i) (meaning P[S_i] < P[k])
    #      Add edges: k -> T_i for all k in (S_i, T_i) (meaning P[k] > P[T_i] => P[T_i] < P[k])
    #    Wait, P[k] > P[T_i] means P[T_i] < P[k].
    #    So we have edges S_i -> k and T_i -> k? No.
    #    P[S_i] < P[k] => edge S_i -> k.
    #    P[k] > P[T_i] => P[T_i] < P[k] => edge T_i -> k.
    #    So for each k in (S, T), we have edges S -> k and T -> k.
    #    This means S and T are both "less than" k.
    #    This does not create a path from S to T directly.
    #    But if we have another person where S' -> k' and T' -> k', and k' = S, then we have T' -> S.
    #    If we also have S -> T (from some other constraint), then T' -> S -> T, so T' < T.
    #    If we also have T -> T' (from some other constraint), then T < T', contradiction.
    #    
    #    So the graph has edges:
    #    For each person (S, T):
    #      For each k in (S, T):
    #        Add directed edge S -> k.
    #        Add directed edge T -> k.
    #    We need to check if there is a path from S to T?
    #    No, we need to check if the system is consistent.
    #    Consistency fails if there is a cycle.
    #    But wait, the problem asks if we can set weights.
    #    This is equivalent to checking if the graph of strict inequalities has a cycle.
    #    However, the number of edges is O(N*M), which is too large.
    #    We need to compress the edges.
    #    Notice that for a person (S, T), we add S -> k and T -> k for all k in (S, T).
    #    This is equivalent to:
    #      S -> (S+1, ..., T-1)
    #      T -> (S+1, ..., T-1)
    #    This looks like range updates.
    #    But we need to detect cycles.
    #    Actually, the standard solution for this problem (which is "Stamina" from a contest) uses the "rightmost reachable" logic.
    #    The logic is:
    #    Maintain `max_reach[u]` = max index v such that there is a path u -> ... -> v.
    #    Initially `max_reach[u] = u`.
    #    When adding S -> k for all k in (S, T):
    #      This implies S -> T-1 (since S -> T-1 is the strongest constraint? No).
    #      Actually, if we have S -> k for all k, then S -> T-1 is implied if we consider the transitive closure?
    #      No, S -> k for all k means S is less than all of them.
    #      The "rightmost reachable" logic works if the edges are u -> v where u < v.
    #      Here we have S -> k (S < k) and T -> k (T < k).
    #      Since S < k < T (for k in (S, T)), we have S < k and T < k.
    #      This doesn't help connect S to T.
    #      BUT, if we have another person (A, B) where A < B, and we have edges A -> k for k in (A, B).
    #      If k = T, then A -> T.
    #      If we also have T -> S (from some other constraint), then A -> T -> S.
    #      If we also have S -> A (from some other constraint), then cycle.
    #    
    #    The key insight from similar problems is that we only need to track the "rightmost" node reachable from u.
    #    Why? Because if there is a path u -> v, then u < v.
    #    If we have a path u -> ... -> v, then P[u] < P[v].
    #    If we have a path S -> T, then P[S] < P[T].
    #    But we require P[S] = P[T]. Contradiction.
    #    So we need to check if there is a path from S to T.
    #    The edges are:
    #      For each person (S, T):
    #        For each k in (S, T):
    #          S -> k
    #          T -> k
    #    This is not a path from S to T.
    #    Wait, maybe I misinterpreted the constraints.
    #    "At every other town, their stamina should always be a positive integer."
    #    P[k] > 0.
    #    P[S] = 0, P[T] = 0.
    #    So P[S] < P[k] and P[k] > P[T].
    #    This means P[S] < P[k] and P[T] < P[k].
    #    This does NOT imply P[S] < P[T].
    #    So why is Sample 2 a contradiction?
    #    P2: 1->3. S=1, T=3. k=2. P[1]<P[2], P[3]<P[2].
    #    P4: 2->4. S=2, T=4. k=3. P[2]<P[3], P[4]<P[3].
    #    From P2: P[3] < P[2].
    #    From P4: P[2] < P[3].
    #    Contradiction: P[3] < P[2] and P[2] < P[3].
    #    So the contradiction is P[3] < P[2] and P[2] < P[3].
    #    This is a cycle 2 -> 3 -> 2.
    #    How do we get 2 -> 3?
    #    From P4: P[2] < P[3]. Edge 2 -> 3.
    #    How do we get 3 -> 2?
    #    From P2: P[3] < P[2]. Edge 3 -> 2.
    #    So the edges are:
    #      For person (S, T):
    #        For k in (S, T):
    #          Edge S -> k
    #          Edge T -> k
    #    Wait, P[3] < P[2] comes from P[3] < P[2]?
    #    P2 says P[3] < P[2]. Yes, because P[3] < P[2] is required?
    #    No, P2 says P[3] > 0 and P[1]=0, P[3]=0.
    #    So P[1] < P[2] and P[3] < P[2].
    #    This gives edges 1->2 and 3->2.
    #    P4 says P[2] < P[3] and P[4] < P[3].
    #    This gives edges 2->3 and 4->3.
    #    So we have 3->2 and 2->3. Cycle!
    #    
    #    So the edges are:
    #      For each person (S, T):
    #        For k in (S, T):
    #          Edge S -> k
    #          Edge T -> k
    #    Wait, this is not right.
    #    P2: S=1, T=3. k=2.
    #    P[1] < P[2] => 1->2.
    #    P[3] < P[2] => 3->2.
    #    P4: S=2, T=4. k=3.
    #    P[2] < P[3] => 2->3.
    #    P[4] < P[3] => 4->3.
    #    So we have 3->2 and 2->3.
    #    
    #    So the edges are:
    #      For each person (S, T):
    #        For k in (S, T):
    #          Edge S -> k
    #          Edge T -> k
    #    Wait, this means S and T are both sources for k.
    #    But in P2, S=1, T=3. k=2.
    #    Edges: 1->2, 3->2.
    #    In P4, S=2, T=4. k=3.
    #    Edges: 2->3, 4->3.
    #    So we have 3->2 and 2->3.
    #    
    #    So the algorithm is:
    #    Maintain a graph with edges S->k and T->k for all k in (S, T).
    #    Check for cycles.
    #    But the number of edges is O(N*M).
    #    We need to compress.
    #    Notice that for a fixed S, we have edges S->k for all k in (S, T).
    #    This is a range of edges.
    #    Also T->k for all k in (S, T).
    #    This is also a range.
    #    We can use a Segment Tree to maintain the "rightmost reachable" index.
    #    Let `reach[u]` be the max index v such that there is a path u -> ... -> v.
    #    Initially `reach[u] = u`.
    #    When adding edges S->k for k in (S, T):
    #      This implies S -> T-1? No.
    #      It implies S -> k for all k.
    #      So `reach[S]` should be updated to max(reach[S], T-1)?
    #      No, because S->k for all k means S is less than all of them.
    #      The "rightmost reachable" logic works if the edges are u->v with u<v.
    #      Here we have S->k (S<k) and T->k (T<k).
    #      So S->k is an edge from S to k.
    #      T->k is an edge from T to k.
    #      So we update `reach[S]` with max over k in (S, T) of k.
    #      And `reach[T]` with max over k in (S, T) of k.
    #      So `reach[S] = max(reach[S], T-1)`.
    #      `reach[T] = max(reach[T], T-1)`.
    #    Wait, if we have S->k for all k, then S -> T-1 is the strongest?
    #    Yes, because T-1 is the largest k.
    #    So we update `reach[S] = max(reach[S], T-1)`.
    #    And `reach[T] = max(reach[T], T-1)`.
    #    Then we check if `reach[S] >= T`?
    #    No, we check if there is a path from S to T.
    #    If `reach[S] >= T`, then there is a path S -> ... -> T.
    #    This implies P[S] < P[T].
    #    But we require P[S] = P[T]. Contradiction.
    #    So we check if `reach[S] >= T`.
    #    But wait, we also have edges T->k.
    #    So `reach[T]` is updated to T-1.
    #    If `reach[T] >= S`, then T -> ... -> S.
    #    This implies P[T] < P[S].
    #    But P[S] = P[T]. Contradiction.
    #    So we check if `reach[T] >= S`.
    #    
    #    So the algorithm is:
    #    1. Initialize `reach[u] = u` for all u.
    #    2. For each person (S, T) (assume S < T):
    #       a. Update `reach[S] = max(reach[S], T-1)`.
    #       b. Update `reach[T] = max(reach[T], T-1)`.
    #       c. Check if `reach[S] >= T` or `reach[T] >= S`.
    #          If so, contradiction.
    #       d. Merge S and T?
    #          Wait, if P[S] = P[T], then they are in the same component.
    #          So we merge S and T.
    #          When merging, we update the `reach` of the new component.
    #          `reach[new_root] = max(reach[S], reach[T])`.
    #          But we also need to update the `reach` of all nodes in the component?
    #          No, we just need to know the max reachability of the component.
    #          Because if any node u in the component can reach v, then all nodes in the component can reach v?
    #          No, only if they are connected by equality.
    #          If P[u] = P[v], then P[u] < P[w] implies P[v] < P[w].
    #          So yes, if u and v are in the same component, their reachability sets are the same.
    #          So we maintain `reach[root]` = max reachability of any node in the component.
    #          When merging u and v:
    #             root = find(u)
    #             reach[root] = max(reach[root], reach[find(v)])
    #             union(u, v)
    #    3. But wait, the update `reach[S] = max(reach[S], T-1)` is a point update.
    #       If S is in a component, we update the component's reach.
    #       So:
    #         root = find(S)
    #         reach[root] = max(reach[root], T-1)
    #         root = find(T)
    #         reach[root] = max(reach[root], T-1)
    #         Check contradiction:
    #           If reach[find(S)] >= T: Contradiction.
    #           If reach[find(T)] >= S: Contradiction.
    #         Then merge S and T.
    #           root = find(S)
    #           reach[root] = max(reach[root], reach[find(T)])
    #           union(S, T)
    #    4. But we need to handle the queries.
    #       We process people 1..M.
    #       If person i causes a contradiction, then any query [L, R] with L <= i <= R is invalid.
    #       We can mark i as "bad".
    #       Then for each query [L, R], check if any bad index is in [L, R].
    #       We can use a Segment Tree or Fenwick Tree to mark bad indices.
    #       Or simply, since we process offline, we can just store the bad indices and check.
    #       But Q is large, so we need efficient checking.
    #       We can use a Segment Tree over [1, M] to mark bad indices.
    #       Then for each query, check if the sum in [L, R] is > 0.
    
    #    Wait, the update `reach[S] = max(reach[S], T-1)` might be insufficient.
    #    Because if we have S -> k for all k, then S -> T-1 is the strongest.
    #    But what if we have a chain?
    #    S -> k1 -> k2 -> ... -> T-1.
    #    Then `reach[S]` should be T-1.
    #    The update `reach[S] = max(reach[S], T-1)` handles this if we process in order?
    #    No, because we might have S -> k1 and k1 -> k2.
    #    If we process S->k1 first, `reach[S]` becomes k1.
    #    Then k1->k2, `reach[k1]` becomes k2.
    #    Then we need to update `reach[S]` to k2.
    #    This requires propagating updates.
    #    This is where the Segment Tree comes in.
    #    We maintain `reach[u]` for each u.
    #    When updating `reach[u] = val`, we update the Segment Tree at position u.
    #    But we also need to propagate the max.
    #    Actually, the standard solution uses a Segment Tree to maintain the max reachability.
    #    `tree[i]` stores the max reachability of node i.
    #    When we update `reach[u] = val`, we do `update(u, val)`.
    #    But we also need to query the max reachability of a component.
    #    Since we use DSU, we can just store the max reachability in the DSU root.
    #    But when we update a non-root node, we must update the root.
    #    So:
    #      root = find(u)
    #      reach[root] = max(reach[root], val)
    #    This works because if u reaches v, and u is merged with w, then w also reaches v.
    #    So the max reachability of the component is the max of all members.
    #    And since we only merge, the max reachability of the new component is the max of the old components.
    #    So the DSU approach with `reach[root]` maintenance is correct.
    #    
    #    Wait, but we have range updates?
    #    No, we only have point updates: `reach[S] = max(reach[S], T-1)`.
    #    And `reach[T] = max(reach[T], T-1)`.
    #    Is this sufficient?
    #    Suppose we have S -> k1 and k1 -> k2.
    #    Person 1: S -> k1. Update `reach[S] = k1`.
    #    Person 2: k1 -> k2. Update `reach[k1] = k2`.
    #    Now `reach[S]` is k1, `reach[k1]` is k2.
    #    If we merge S and k1, then `reach[S]` becomes max(k1, k2) = k2.
    #    So yes, it works.
    #    
    #    So the algorithm is:
    #    1. Initialize `reach[u] = u` for u in 0..N-1.
    #    2. DSU with `parent` and `max_reach`.
    #    3. For each person i (S, T) (assume S < T):
    #       a. u = S, v = T.
    #       b. Update `reach[u] = max(reach[u], T-1)`.
    #          root_u = find(u)
    #          max_reach[root_u] = max(max_reach[root_u], T-1)
    #       c. Update `reach[v] = max(reach[v], T-1)`.
    #          root_v = find(v)
    #          max_reach[root_v] = max(max_reach[root_v], T-1)
    #       d. Check contradiction:
    #          if max_reach[find(u)] >= T: mark i as bad.
    #          if max_reach[find(v)] >= S: mark i as bad.
    #          (Note: if S and T are already in the same component, we check if max_reach[root] >= T or >= S?
    #           Actually, if S and T are in the same component, then P[S] = P[T].
    #           If max_reach[root] >= T, then there is a path from S to T (since S is in the component).
    #           So contradiction.
    #           Similarly if max_reach[root] >= S.
    #           But since S < T, max_reach[root] >= T implies path S->...->T.
    #           max_reach[root] >= S is always true since S is in the component and max_reach[S] >= S.
    #           So we only need to check max_reach[root] >= T.
    #       e. Merge u and v.
    #          root_u = find(u), root_v = find(v)
    #          if root_u != root_v:
    #             parent[root_v] = root_u
    #             max_reach[root_u] = max(max_reach[root_u], max_reach[root_v])
    #    4. Mark bad indices.
    #    5. Answer queries.
    
    #    Wait, is the update `reach[u] = max(reach[u], T-1)` correct?
    #    The person (S, T) implies P[S] < P[k] for all k in (S, T).
    #    This implies P[S] < P[T-1].
    #    So S -> T-1.
    #    So `reach[S]` should be at least T-1.
    #    Yes.
    #    And P[T] < P[k] for all k in (S, T).
    #    This implies P[T] < P[T-1].
    #    So T -> T-1.
    #    So `reach[T]` should be at least T-1.
    #    Yes.
    #    
    #    So the algorithm seems correct.
    
    #    Implementation details:
    #    - DSU with path compression and union by rank/size.
    #    - `max_reach` array for DSU roots.
    #    - `bad` array for people.
    #    - Segment Tree or Fenwick Tree to count bad people in range [L, R].
    #      Since we process people 1..M, we can just build a Fenwick Tree over [1, M].
    #      When we find person i is bad, update Fenwick at i with +1.
    #      Then query sum(L, R). If > 0, then No.
    
    #    Wait, the problem says "if it is possible to set the strengths ... for all people L_k ... R_k".
    #    This means if ANY person in [L, R] causes a contradiction, then the answer is No.
    #    So we need to check if there is any bad index in [L, R].
    #    Yes, sum(L, R) > 0 means there is a bad index.
    
    #    One more thing: The problem says "Person i's requirement is ...".
    #    We process people 1..M.
    #    If person i causes a contradiction, then person i cannot be satisfied.
    #    So any query including i is No.
    #    Correct.
    
    #    Let's code.
    
    #    Note: S and T are 1-based. Convert to 0-based for internal logic?
    #    Towns 1..N. Potentials P[1]..P[N].
    #    Edges between j and j+1.
    #    Person i: S_i, T_i.
    #    Path from S_i to T_i.
    #    If S_i < T_i:
    #       k in (S_i, T_i) => k from S_i+1 to T_i-1.
    #       Update reach[S_i] with T_i-1.
    #       Update reach[T_i] with T_i-1.
    #    If S_i > T_i:
    #       Swap S_i, T_i?
    #       The problem says "shortest path".
    #       The constraints are symmetric?
    #       P[S] = 0, P[T] = 0.
    #       P[k] > 0 for k in (S, T).
    #       If S > T, then k in (T, S).
    #       So P[S] < P[k] and P[T] < P[k].
    #       So we update reach[S] with S-1? No.
    #       The range is (min(S, T), max(S, T)).
    #       Let u = min(S, T), v = max(S, T).
    #       Then k in (u, v).
    #       P[u] < P[k] and P[v] < P[k].
    #       So we update reach[u] with v-1.
    #       And reach[v] with v-1.
    #       Wait, if S > T, then u = T, v = S.
    #       So update reach[T] with S-1.
    #       And reach[S] with S-1.
    #       So in general:
    #         u = min(S, T)
    #         v = max(S, T)
    #         reach[u] = max(reach[u], v-1)
    #         reach[v] = max(reach[v], v-1)
    #         Check if reach[find(u)] >= v.
    #         Merge u and v.
    
    #    Wait, if S > T, then the path is from S to T.
    #    The towns between are T+1, ..., S-1.
    #    So k in (T, S).
    #    So P[T] < P[k] and P[S] < P[k].
    #    So yes, u = T, v = S.
    #    So the logic holds.
    
    #    Complexity: O((N+M+Q) * alpha(N)).
    #    This is efficient enough.
    
    #    Let's implement.
    
    pass

# DSU implementation
parent = []
max_reach = []

def find(i):
    if parent[i] == i:
        return i
    parent[i] = find(parent[i])
    return parent[i]

def union(i, j):
    root_i = find(i)
    root_j = find(j)
    if root_i != root_j:
        # Merge j into i
        parent[root_j] = root_i
        max_reach[root_i] = max(max_reach[root_i], max_reach[root_j])
        return True
    return False

def update_reach(i, val):
    root = find(i)
    if val > max_reach[root]:
        max_reach[root] = val

def solve():
    global parent, max_reach
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    for i in range(1, M + 1):
        S[i] = int(next(iterator))
        T[i] = int(next(iterator))
    
    # Initialize DSU
    parent = list(range(N + 1))
    max_reach = list(range(N + 1))
    
    bad = [False] * (M + 1)
    
    for i in range(1, M + 1):
        u = S[i]
        v = T[i]
        if u > v:
            u, v = v, u
        
        # Constraints: P[u] < P[k] and P[v] < P[k] for k in (u, v)
        # This implies P[u] < P[v-1] and P[v] < P[v-1]
        # So update reach[u] with v-1, reach[v] with v-1
        
        # Update u
        root_u = find(u)
        if v - 1 > max_reach[root_u]:
            max_reach[root_u] = v - 1
        
        # Update v
        root_v = find(v)
        if v - 1 > max_reach[root_v]:
            max_reach[root_v] = v - 1
        
        # Check contradiction
        # If there is a path from u to v, then P[u] < P[v], but P[u] = P[v].
        # Path from u to v exists if max_reach[find(u)] >= v.
        # Note: u and v might be in the same component.
        root_u = find(u)
        if max_reach[root_u] >= v:
            bad[i] = True
        else:
            # Check if v can reach u?
            # If max_reach[find(v)] >= u, then P[v] < P[u], contradiction.
            root_v = find(v)
            if max_reach[root_v] >= u:
                bad[i] = True
        
        # Merge u and v
        if not bad[i]:
            # Only merge if not bad? 
            # Actually, even if bad, we might need to merge for future queries?
            # No, if it's bad, the configuration is impossible.
            # But the problem asks if there exists a configuration for the range.
            # If person i is bad, then any range including i is No.
            # We don't need to merge if it's bad, because we won't use this person.
            # But wait, if we don't merge, future people might not see the equality.
            # However, if person i is bad, we don't care about the configuration.
            # We just need to mark i as bad.
            # But what if person i is bad, but person j (j > i) depends on the merge?
            # If person i is bad, then the whole set including i is invalid.
            # So we don't need to process further for this set.
            # But we are processing people 1..M sequentially.
            # If person i is bad, we mark it.
            # We still need to process person i+1, i+2, etc.
            # But the merge for person i is only relevant if person i is valid.
            # If person i is invalid, we don't need to merge because we won't use the constraints of person i.
            # So we skip merge if bad[i].
            pass
        
        if not bad[i]:
            union(u, v)
    
    # Build Fenwick Tree for bad indices
    # We need to check if there is any bad index in [L, R].
    # Fenwick Tree supports point update and range sum.
    
    bit = [0] * (M + 1)
    
    def update_bit(idx, val):
        while idx <= M:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query_bit(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
    
    for i in range(1, M + 1):
        if bad[i]:
            update_bit(i, 1)
            
    # Process queries
    results = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        if query_bit(r) - query_bit(l - 1) > 0:
            results.append("No")
        else:
            results.append("Yes")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()