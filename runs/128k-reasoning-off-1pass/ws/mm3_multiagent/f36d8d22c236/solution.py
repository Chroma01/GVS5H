import sys
from collections import defaultdict

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    
    # mapping from source char to target char
    # because operation replaces ALL occurrences of x with y,
    # a source letter must map to a unique target letter.
    src_to_target = {}
    for i in range(N):
        a, b = S[i], T[i]
        if a == b:
            continue
        if a in src_to_target:
            if src_to_target[a] != b:
                print(-1)
                return
        else:
            src_to_target[a] = b
    
    # find all letters that appear in S or T and have any mapping
    # nodes involved are sources and targets
    nodes = set(src_to_target.keys())
    for t in src_to_target.values():
        nodes.add(t)
    
    if not nodes:
        # no differences, already identical
        print(0)
        return
    
    # check for impossible case: a target letter that has outgoing edge
    # but no incoming edge (cannot be produced because it never appears as S[i])
    # Actually, if a letter is a target but also a source, it has incoming edge from somewhere
    # Wait: the condition is: any letter that appears in T (and has at least one outgoing edge)
    # must have at least one incoming edge? Let's think carefully.
    # If letter 'c' is a target (i.e., appears in T) and also a source (has outgoing edge),
    # then it has an incoming edge because it's a target.
    # If letter 'c' is a target but NOT a source, it must have at least one incoming edge
    # (i.e., some S[i] = c) to be producible. But S[i] can be c only if c appears in S.
    # Since it's a target from src_to_target, there exists some S[i] = src, T[i] = c,
    # so c has an incoming edge.
    # What if c appears in T but is not a target of any source, and also not a source?
    # Then c only appears in T in positions where S[i] != c. For S to become T,
    # we need c to be produced. The only way is if some source maps to c.
    # So such a c would be impossible. But we only care about letters that appear in T
    # in positions where S[i] != T[i] (i.e., targets). And if c is not a target,
    # it means S[i] = c whenever T[i] = c (so no change needed), or c never appears in T.
    # Actually, targets are exactly the set of values in src_to_target.values().
    # So we only need to check: for each target c, is there some source that maps to it?
    # Yes, by definition it is the value of some mapping, so it has at least one incoming edge.
    # So the "target with no incoming edge" case cannot happen if we only consider
    # the differences.
    # 
    # Wait, there's a subtler case: what if a letter appears in T in a position
    # where S[i] = c, but c is not in src_to_target? That means S[i] = T[i] = c,
    # so no change needed. That's fine.
    # 
    # The standard impossibility condition for this problem (Codeforces 1220C? No, 1295D? No...)
    # is: check that the graph has no cycle, and also that no node has out-degree 1
    # and in-degree 0 simultaneously. But with functional graph, if there's a node
    # with in-degree 0, it means no source maps to it. But can it still be produced?
    # Only if it appears in S in some position. But if it appears in S, and S[i] != T[i],
    # it would be a source. If S[i] = T[i], no change needed. So a node with in-degree 0
    # either doesn't appear in S (impossible to produce if it appears in T) or appears
    # only in S positions where S[i] = T[i] (no change needed).
    # 
    # Let's reconsider: nodes with in-degree 0 that appear in T (as a character where S[i] != T[i])
    # would be impossible. But if c is a target in src_to_target, it has in-degree >= 1.
    # If c appears in T but not as a target, then for all i with T[i]=c, we have S[i]=c,
    # so no change needed. So no problem.
    # 
    # Therefore, the only impossibility is a cycle in the graph.
    # Let's verify with the standard solution logic.
    
    # Actually, there's one more case: a letter that appears in S (as source) but maps to itself?
    # No, we skip S[i] == T[i], so no self-loops.
    # 
    # Let's check the official solution: the answer is the number of distinct source letters
    # minus the number of source letters that are already correct (self-loop).
    # Since we exclude S[i]==T[i], no source has self-loop, so answer = number of source letters.
    # 
    # But wait, the problem says minimum number of operations. The known solution is:
    # count = 0
    # for each source letter, if its target is not "fixed" (i.e., not a source itself or
    # appears in S in a position where it doesn't change), we need an operation.
    # Actually, the simple formula is: number of unique source letters that map to a different
    # target, and that target is not a source itself? No...
    # 
    # Let's re-derive: The operation merges x into y. This is like contracting edge x->y.
    # The graph is a set of directed trees pointing towards roots, possibly with some
    # extra nodes. Actually, since out-degree <= 1, it's a forest of arborescences
    # (each component has exactly one cycle or is a tree, but since out-degree <=1,
    # each weakly connected component is either a tree (pointing to a root) or a cycle
    # with trees attached? No, with out-degree <=1, the structure is: each component
    # has exactly one directed cycle (possibly of length 0? i.e., tree with root),
    # or is a single node.
    # 
    # The operation sequence: we can process the graph in reverse topological order
    # (from leaves to root). For each source node x with target y, we perform the operation
    # "replace x with y". This costs 1 operation per source node. However, if the target y
    # is also a source node that will later be replaced, we might be able to combine?
    # No, because the operations are global and sequential. But we can choose the order
    # to minimize operations. Actually, each source node requires exactly one operation,
    # and the operations are independent if the targets are not sources. If a target is
    # also a source, we need to replace it later, but the first operation still needed.
    # So the answer is exactly the number of source nodes (distinct letters in S that
    # have at least one differing position).
    # 
    # But wait, sample 1: S = afbfda, T = bkckbb
    # Pairs where S[i]!=T[i]: (a,b), (f,k), (b,c), (d,b)
    # Source letters: a, f, b, d -> 4. Answer is 4. Matches.
    # 
    # Sample 4: S = abac, T = bcba
    # Pairs: (a,b), (b,c), (a,c)? Let's see:
    # i=0: a->b
    # i=1: b->c
    # i=2: a->c? S[2]=a, T[2]=b, wait T[2]=b? T = bcba, so T[2]=b, S[2]=a -> a->b (consistent with i=0)
    # i=3: c->a? S[3]=c, T[3]=a -> c->a
    # So sources: a, b, c -> 3 distinct sources. But answer is 4.
    # Hmm, that doesn't match. Let me re-read sample 4.
    # Sample 4: N=4, S=abac, T=bcba
    # Positions:
    # 0: a -> b
    # 1: b -> c
    # 2: a -> b
    # 3: c -> a
    # So mappings: a->b, b->c, c->a. This forms a cycle a->b->c->a.
    # So it's impossible? But answer is 4, not -1. So cycle is not impossible?
    # Wait, let me check the problem statement again. Sample 4 output is 4.
    # 
    # Oh! I made a mistake. The operation is: choose x, y and replace every x in S with y.
    # This is not just "map S[i] to T[i]". We can use intermediate letters.
    # For example, a->b->c->a cycle: we can break the cycle by using a temporary letter.
    # Steps for cycle a->b, b->c, c->a:
    # 1. Replace a with x (temp) -> S becomes xbxc
    # 2. Replace b with a -> S becomes xaxc? Wait no.
    # Let's trace:
    # Initial: abac
    # Need to get: bcba
    # 
    # Actually, with cycle, we need n+1 operations for a cycle of n nodes.
    # For a->b, b->c, c->a (3 nodes), we need 4 operations.
    # That matches sample 4 answer 4.
    # 
    # So the formula is: for each weakly connected component, if it's a tree (m = n-1),
    # cost = n-1 = m. If it has a cycle (m = n, since functional graph with one cycle per component),
    # cost = m + 1 = n.
    # Total cost = total edges + number of cycles.
    # 
    # Now, how to detect cycles? In a functional graph (out-degree <= 1), each component
    # has at most one cycle. We can find cycles via DFS or union-find.
    # 
    # Alternative simpler formula: count number of source nodes (letters that appear as S[i]
    # with S[i] != T[i]), and subtract the number of source nodes that are not "leaves"
    # or something? Actually, the known solution is:
    # ans = 0
    # For each source letter x, if x appears in S and has a target y, and y does not appear
    # in S (i.e., y is a pure target), then we can do the operation x->y and it "fixes" x.
    # If y also appears in S, we need to fix y first, so we might not need an operation for x?
    # Wait, the standard solution from Codeforces problem "Make it Equal" or similar:
    # 
    # The minimum number of operations equals:
    # (number of distinct source letters) - (number of source letters that are "good",
    # i.e., their target appears in S in a position where it doesn't change, or they
    # form a cycle).
    # 
    # Actually, let's use the connected component approach. It's robust and clear.
    
    # Build adjacency list
    adj = defaultdict(list)
    nodes_set = set()
    for src, tgt in src_to_target.items():
        adj[src].append(tgt)
        nodes_set.add(src)
        nodes_set.add(tgt)
    
    # Check for cycles using DFS on 26 nodes
    # Since out-degree <= 1, we can also use a simple visited/stack array
    # But we need to consider only nodes in nodes_set
    # Actually, we can just run DFS on all 26 letters, but ignore those not in nodes_set
    # or with no edges.
    
    # The graph might have nodes that are not in nodes_set (letters not in S or T).
    # We only care about nodes in nodes_set.
    # 
    # To detect cycles: we can do a DFS with colors: 0=unvisited, 1=visiting, 2=done.
    # But since out-degree <= 1, we can also just follow the chain and detect repeats.
    # However, a node might have in-degree > 1, so a chain might visit a node twice
    # from different paths. We need standard cycle detection.
    
    # Let's use the component approach.
    # Find weakly connected components (treating edges as undirected).
    # For each component, count nodes and edges.
    # If edges == nodes, it's a cycle (plus possibly trees attached? No, with out-degree <=1,
    # the component is exactly a cycle with trees feeding into it, but the trees contribute
    # extra nodes and edges equally. Wait: in a functional graph, the number of edges equals
    # the number of nodes that have an outgoing edge, which is the number of source nodes.
    # In a component, the sum of out-degrees = number of edges. But each node has out-degree <=1.
    # A component is a cycle (k nodes) with trees rooted at the cycle nodes.
    # Total nodes = k + (trees). Total edges = (trees) + k (each tree node points to parent,
    # cycle nodes point to next cycle node). So edges = nodes. So every component has
    # edges == nodes! This is a property of functional graphs: sum of out-degrees = number
    # of edges, and every node has out-degree 0 or 1, so edges = number of non-root nodes
    # in the forest. But in a functional graph, there are no roots with in-degree 0 necessarily.
    # Actually, in a functional graph, each component has exactly one cycle. The total
    # number of edges equals the total number of nodes (because it's a permutation on the
    # cycle and trees attached, but trees have edges = nodes, and cycle has edges = nodes too).
    # Wait, that's not right. A tree with k nodes has k-1 edges. A cycle with k nodes has k edges.
    # If we attach trees to cycle nodes, the trees add nodes and edges equally. So total
    # edges = total nodes - (number of trees attached? No).
    # Let's be precise: Consider a component with cycle of length c, and t tree nodes
    # (nodes not in cycle). Each tree node has out-degree 1 (to its parent), and no in-degree
    # from within the tree except the root which has in-degree from the cycle or another tree.
    # Total edges = c (cycle edges) + t (tree edges) = c + t.
    # Total nodes = c + t.
    # So edges = nodes always! This is because every node except the cycle nodes has
    # in-degree 1 from its parent, but also has out-degree 1. The cycle nodes have
    # in-degree >= 1 (from cycle and possibly trees) and out-degree 1 (to next cycle).
    # So indeed, in any weakly connected component of a functional graph, edges = nodes.
    # 
    # Therefore, the number of operations needed for a component is: edges + (is_cycle ? 1 : 0).
    # But since edges = nodes, this is nodes + (is_cycle ? 1 : 0) - (number of nodes that are
    # already correct? No).
    # 
    # Actually, the formula is: cost = number of source nodes in the component that
    # map to a different target. But all source nodes map to a different target (we excluded
    # S[i]==T[i]). So cost per component = number of source nodes in component.
    # But in a component, the number of source nodes is exactly the number of edges.
    # So cost = edges for tree components, edges + 1 for cycle components.
    # Since edges = nodes, cost = nodes (for tree) or nodes+1 (for cycle).
    # 
    # But wait, a "tree" component (no cycle) in a functional graph? That would be a
    # component with a node of in-degree 0 that has no cycle. Yes, a chain ending in a
    # node with out-degree 0 (a "sink"). In that case, edges = nodes - 1.
    # Let's check: chain a->b->c. Nodes: a,b,c. Edges: a->b, b->c. 2 edges, 3 nodes.
    # edges = nodes - 1.
    # Chain a->b. Nodes: a,b. Edges: 1. nodes-1=1.
    # Single node a with no edge: not a component we care about (no differing positions).
    # 
    # So the general formula:
    # - If component has a cycle: cost = number of nodes in component.
    # - If component has no cycle: cost = number of edges in component = number of nodes - 1.
    # 
    # Sum over components.
    
    # Let's implement: find connected components (undirected), check if they contain a cycle.
    # Actually, we can just find cycles in the directed graph.
    # 
    # Simpler: use the fact that in the undirected sense, the component is connected.
    # For each component, count nodes and edges. If it's a directed cycle (each node has
    # in-degree 1 and out-degree 1 in the directed subgraph), then cost = nodes + 1.
    # Else cost = edges = nodes - 1 (since it's a tree in the directed sense? Wait,
    # a tree in the directed sense (arborescence) has nodes-1 edges and a unique root
    # with in-degree 0, but in our case, a node could have in-degree > 1 if multiple
    # nodes point to it. That's still a tree in the undirected sense, but in the directed
    # sense it's a forest of trees pointing to the same root? Actually, if two nodes point
    # to the same node, and that node has out-degree 0, it's still a tree in the undirected
    # sense. Example: a->c, b->c. Nodes: a,b,c. Edges: 2. It's a tree (no cycle).
    # Directed: a and b point to c. c points to nothing. This is a tree.
    # So cost = 2 (number of edges) = nodes - 1 = 3-1=2.
    # Operations: replace a with c, replace b with c. That's 2 operations.
    # Can we do better? If we replace a with b first: a->b, then b->c. That's 2 operations.
    # So 2 is correct.
    # 
    # Now, how to detect if a component has a directed cycle? We can run DFS on the
    # directed graph. But since we only need the total cost, and we know the structure,
    # we can use a standard algorithm.
    # 
    # Actually, the simplest correct approach: 
    # ans = 0
    # For each source letter x, if x has a target y:
    #   if y does not appear in S (i.e., y is not a key in src_to_target and y != x? 
    #     wait, y could be a key or not), then we need an operation.
    #   if y appears in S, then y will be replaced later, so we might not need an operation for x?
    #   This is the greedy approach: only do operations for sources whose target is not a source.
    #   But we also need to handle cycles.
    # 
    # Let's use the union-find / DFS cycle detection approach. It's straightforward.
    
    # Build graph
    graph = {node: [] for node in nodes_set}
    for src, tgt in src_to_target.items():
        graph[src].append(tgt)
        if tgt not in graph:
            graph[tgt] = []
    
    # Find cycles
    # state: 0=unvisited, 1=visiting, 2=done
    state = {node: 0 for node in graph}
    
    def has_cycle(node):
        state[node] = 1
        for nxt in graph[node]:
            if nxt not in state:
                continue
            if state[nxt] == 1:
                return True
            if state[nxt] == 0:
                if has_cycle(nxt):
                    return True
        state[node] = 2
        return False
    
    cycle_found = False
    for node in graph:
        if state[node] == 0:
            if has_cycle(node):
                cycle_found = True
                break
    
    if cycle_found:
        print(-1)
        return
    
    # No cycles. Now find connected components (undirected) and compute cost.
    # Actually, with no cycles, each component is a tree.
    # Cost per component = number of edges in component.
    # Total cost = total number of edges = number of source letters.
    # Wait, is that right?
    # If no cycles, then every component is a tree (in the undirected sense).
    # In a tree, number of edges = number of nodes - 1.
    # But the cost to merge a tree where edges are directed from sources to targets:
    # We process leaves (nodes with in-degree 0? or out-degree 0?).
    # Actually, the known result: minimum number of operations = number of distinct
    # source letters - number of source letters that are "already in the right place"
    # (i.e., target is not a source and not part of a cycle? No).
    # 
    # Let's think: with no cycles, we can perform operations in any order.
    # If we have a->b, b->c, c->d (chain). Sources: a, b, c. Total 3.
    # Can we do it in 3? Yes: c->d, b->c, a->b. Or b->c, c->d, a->b.
    # Can we do it in 2? If we replace a with d directly? No, operation only changes
    # all a to d, but b and c are still there. So we need to fix all.
    # So 3 is correct.
    # 
    # What if target is not a source? a->d, b->d, c->d. Sources: a, b, c.
    # Operations: 3 (replace a with d, b with d, c with d). Can we do 2? No.
    # So answer = number of source letters when no cycles.
    # 
    # When there are cycles, we need extra operations. Specifically, for a cycle of length k,
    # we need k+1 operations instead of k.
    # 
    # So the formula is: answer = number of source letters + number of cycles.
    # Where cycles are counted in the functional graph (each weakly connected component
    # with a directed cycle counts as 1 cycle, or is it each directed cycle? In a
    # functional graph, each component has at most one directed cycle. So number of cycles
    # = number of components that contain a directed cycle.
    # 
    # But wait, what if a component has a cycle but also has trees attached?
    # Example: a->b, c->b, b->d. Sources: a, c, b. (3 sources)
    # b->d is an edge, so b is a source. c->b, a->b. This is a tree (no cycle).
    # Cost: 3.
    # 
    # Example with cycle: a->b, b->a, c->a. Sources: a, b, c. (3 sources)
    # Cycle: a<->b. Component has cycle.
    # Cost: we need to break the cycle. Steps:
    # 1. Replace c with x (temp) -> S has x's and a,b
    # 2. Replace a with c -> now we have c's and b
    # 3. Replace b with a -> now we have c's and a's? Wait, this is getting messy.
    # Let's trace with actual letters: S has some a's, b's, c's. T has a's, b's, c's
    # but mapped.
    # For a->b, b->a, c->a:
    # We need a's to become b's, b's to become a's, c's to become a's.
    # Since a and b swap, we need a temp.
    # 1. Replace a with x: all a's become x. Now we have x's, b's, c's.
    # 2. Replace b with a: b's become a's. Now we have x's, a's, c's.
    # 3. Replace x with b: x's become b's. Now we have a's, b's, c's.
    # 4. Replace c with a: c's become a's. Now we have a's, b's. Wait, T has a's, b's, c's?
    # No, T has only a's and b's if c->a. Actually, if c->a, then c in S becomes a in T.
    # So T has no c's. So final S should have no c's.
    # After step 4: c's become a's. Now we have a's and b's. Matches T.
    # Total operations: 4. Sources: 3. So 3 + 1 = 4. Correct.
    # 
    # So formula: ans = number_of_source_letters + number_of_cycles_in_graph.
    # But we must be careful: a cycle of length 1 (self-loop) is impossible because we
    # exclude S[i]==T[i]. So cycles are length >= 2.
    # 
    # How to count cycles? In a functional graph, we can find them via DFS.
    # Or we can use the fact that after we remove all nodes that are not part of any cycle,
    # the remaining graph is a set of cycles.
    # 
    # Simpler: use the standard cycle detection that also counts cycles.
    # When we find a back edge to a node in the current stack, we found a cycle.
    # But we need to count the number of cycle components, not the number of back edges.
    # Actually, each cycle corresponds to exactly one back edge in the DFS if we start
    # from appropriate roots? Not exactly, but we can count components with cycles.
    # 
    # Alternatively, after detecting that there is a cycle, we can just say it's impossible?
    # But sample 4 has a cycle and answer is 4, not -1. So cycles are not impossible!
    # 
    # Wait, sample 3: abac -> abrc. Pairs: (a,a) skip, (b,b) skip, (a,r) -> a->r, (c,c) skip.
    # Actually i=2: S[2]=a, T[2]=r. So a->r. Also b is already correct.
    # So source: a. Target: r. r does not appear in S. So we can replace a with r.
    # But wait, T has 'r' at position 2. S[2]='a'. So a->r. That's one operation.
    # But answer is -1. Why? Because r appears in T but not in S. But we can produce r
    # by replacing a with r. So why -1?
    # Let me re-read sample 3:
    # N=4, S=abac, T=abrc
    # Positions:
    # 0: a->a (same)
    # 1: b->b (same)
    # 2: a->r (different)
    # 3: c->c (same)
    # So only one difference: a->r.
    # Operation: replace a with r. S becomes rbrc? No, S[0] is a, so becomes r.
    # S becomes rbrc. T is abrc. Not equal! Because S[1] was b, stays b, but T[1] is b.
    # Wait, T[1] is 'b'? T = abrc, so T[1] = b. S[1] = b. So S[1] stays b. T[0] = a, but S[0] becomes r. So mismatch.
    # So we cannot change a to r globally because it would affect S[0] which should stay a.
    # This is the consistency check: a appears in S at positions 0 and 2. At pos 0, S[0]=a, T[0]=a (no change). At pos 2, S[2]=a, T[2]=r (change to r). So a needs to stay a in one place and become r in another. This is impossible.
    # My initial check (src_to_target consistency) would catch this: when processing a, we see a->a (from pos 0? No, pos 0 is a==a, skipped). Then pos 2: a->r, so src_to_target[a] = r. No conflict. So my check misses it!
    # 
    # The real consistency check is: for each source letter x, all occurrences of x in S
    # must map to the same target letter y. But this is not just about positions where
    # S[i] != T[i]; it's about ALL positions. If x appears at position i where S[i]=x,
    # then T[i] must be the target for x. If T[i] is different, then x cannot be both
    # kept and changed.
    # 
    # So the mapping should be: for each x in S, the set of T[i] for all i with S[i]=x
    # must be a singleton {y}. Then x must become y.
    # 
    # Let's verify with sample 3: x=a. Positions with a: 0 and 2. T[0]=a, T[2]=r. Set = {a,r}. Not singleton -> impossible.
    # 
    # So the correct check is:
    # For each letter c (0-25), let S_set = {i | S[i]=c}, T_vals = {T[i] | i in S_set}.
    # If len(T_vals) > 1, impossible.
    # If len(T_vals) == 1, let y = the only element. Then we have a constraint c -> y.
    # If c == y, no operation needed for c (but c might still be a target of others).
    # 
    # This handles all cases. Let's verify sample 1: S=afbfda, T=bkckbb
    # a: positions 0,5. T[0]=b, T[5]=b. -> a->b
    # f: pos 1. T[1]=k. -> f->k
    # b: pos 2. T[2]=c. -> b->c
    # d: pos 4. T[4]=b. -> d->b
    # f again: pos 3? S[3]=b, T[3]=c. b->c (already).
    # So constraints: a->b, f->k, b->c, d->b. All consistent. No cycles.
    # Sources (c != y): a,b,d,f. Count = 4. Answer = 4.
    # 
    # Sample 4: S=abac, T=bcba
    # a: pos 0,2. T[0]=b, T[2]=b. -> a->b
    # b: pos 1. T[1]=c. -> b->c
    # c: pos 3. T[3]=a. -> c->a
    # Constraints: a->b, b->c, c->a. Cycle! a,b,c all different.
    # Number of source letters: 3. Cycle exists. Cost = 3 + 1 = 4. Matches.
    # 
    # Sample 2: S=abac, T=abac. All same. No constraints with c!=y. Answer 0.
    # 
    # So the algorithm is:
    # 1. For each letter c, find the set of target characters it must become.
    #    If the set has size > 1, print -1.
    #    If size 1 and c != target, add edge c -> target.
    #    (We don't need to add self-loops).
    # 2. Build the graph with these edges.
    # 3. If the graph has a cycle (in the directed sense), then for each cycle of length k,
    #    the cost contribution is k+1 instead of k. Since each node in a cycle is a source,
    #    and the total number of sources is sum of sizes of cycles and trees.
    #    Total cost = number_of_edges + number_of_cycles.
    #    (Since number_of_edges = number of source letters).
    # 4. Count the number of cycles in the graph. In a functional graph, each weakly
    #    connected component has at most one cycle. We can count components with cycles
    #    by checking if any node in the component is part of a cycle.
    # 
    # Implementation details:
    # - We have 26 letters.
    # - Build a list of constraints: for each c, if c must become y (y != c), add edge c->y.
    # - Check for cycle: use DFS or union-find. Since we need to count cycles, and each
    #   component can have at most one cycle, we can do:
    #   - Find all nodes involved in cycles.
    #   - Count the number of cycle components.
    # 
    # Simpler way to count cycles: 
    # After building the graph, do a topological sort. Nodes with in-degree 0 are not in cycles.
    # Remove them iteratively. The remaining nodes are all in cycles. The number of cycles
    # is the number of connected components in the remaining graph? Or just the number of
    # remaining nodes divided by their cycle length? Since each component has exactly one
    # cycle, the number of cycles equals the number of weakly connected components in the
    # remaining graph.
    # 
    # Or even simpler: use DFS to detect cycles. When we find a back edge, we know there's
    # a cycle. But to count how many cycles (i.e., how many components have cycles), we
    # can do a full DFS and count the number of times we find a cycle? Actually, in a
    # functional graph, a component has either 0 or 1 cycle. We can determine if a component
    # has a cycle by trying to find a cycle starting from any node in it.
    # 
    # Given the constraints (N up to 2e5, 26 letters), we can do this easily.
    # 
    # Algorithm:
    # 1. Initialize an array target[26] = None.
    # 2. For i in 0..N-1:
    #    c = S[i], d = T[i]
    #    if target[c] is None: set to d
    #    elif target[c] != d: print -1 and return.
    # 3. After loop, for c in 0..25:
    #    if target[c] is not None and target[c] != c:
    #       add edge c -> target[c]
    # 4. Count the number of edges: E.
    # 5. Detect cycles in the graph.
    #    If a cycle exists, count the number of connected components that contain a cycle.
    #    Let C be that count.
    #    Answer = E + C.
    # 
    # How to count C?
    # Method 1: Find all nodes that are in cycles. The number of cycles is the number of
    # weakly connected components formed by these nodes.
    # Method 2: Use the fact that after removing all nodes not in cycles, each component
    # is exactly a cycle. So the number of cycles is the number of components in the
    # subgraph induced by cycle nodes.
    # 
    # We can find cycle nodes by:
    # - Compute in-degree for each node (considering only edges).
    # - Initialize queue with nodes having in-degree 0.
    # - Remove them (decrement in-degree of their target).
    # - Repeat until no more nodes can be removed.
    # - Remaining nodes are in cycles.
    # Then, among remaining nodes, count connected components (undirected). That number is C.
    # 
    # Let's implement this.
    
    # Step 2: Build target mapping with consistency check
    target = [None] * 26
    for i in range(N):
        c = ord(S[i]) - ord('a')
        d = ord(T[i]) - ord('a')
        if target[c] is None:
            target[c] = d
        elif target[c] != d:
            print(-1)
            return
    
    # Build edges
    edges = []
    in_deg = [0] * 26
    nodes = [False] * 26
    for c in range(26):
        if target[c] is not None and target[c] != c:
            edges.append((c, target[c]))
            in_deg[target[c]] += 1
            nodes[c] = True
            nodes[target[c]] = True
    
    if not edges:
        print(0)
        return
    
    # Find nodes in cycles using topological removal
    from collections import deque
    in_deg_copy = in_deg[:]
    q = deque()
    for c in range(26):
        if nodes[c] and in_deg_copy[c] == 0:
            q.append(c)
    
    removed = [False] * 26
    while q:
        u = q.popleft()
        removed[u] = True
        v = target[u]
        if v is not None and v != u and not removed[v]:
            in_deg_copy[v] -= 1
            if in_deg_copy[v] == 0:
                q.append(v)
    
    # Remaining nodes (nodes[c] and not removed[c]) are in cycles
    # Count connected components among them (undirected)
    # Build undirected graph of remaining nodes
    adj_undirected = [[] for _ in range(26)]
    for c in range(26):
        if nodes[c] and not removed[c]:
            # find its target
            t = target[c]
            if t is not None and t != c and not removed[t]:
                adj_undirected[c].append(t)
                adj_undirected[t].append(c)
    
    visited = [False] * 26
    C = 0
    for c in range(26):
        if nodes[c] and not removed[c] and not visited[c]:
            # BFS/DFS to find component
            stack = [c]
            visited[c] = True
            while stack:
                u = stack.pop()
                for v in adj_undirected[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append(v)
            C += 1
    
    # Total answer: number of edges + C
    E = len(edges)
    print(E + C)

solve()