import sys
from collections import defaultdict

def solve():
    # Increase recursion depth just in case, though we try to avoid deep recursion
    sys.setrecursionlimit(10**6)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 3:
        # Constraints say N >= 3, but handle gracefully
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)
    
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Identify leaves: degree 1
    is_leaf = [False] * (N + 1)
    for i in range(1, N + 1):
        if degree[i] == 1:
            is_leaf[i] = True

    # For each node, count leaf neighbors and identify non-leaf neighbors
    # We want to find nodes v that can be intermediate nodes.
    # An intermediate node v for center u with parameter y must satisfy:
    # 1. v has exactly y leaf neighbors.
    # 2. v has exactly 1 non-leaf neighbor, which is u.
    # 3. y >= 1.
    
    # Let's collect candidates: (center_node, y) -> count
    # We use a dictionary: center_node -> defaultdict(int) mapping y -> count
    center_y_counts = defaultdict(lambda: defaultdict(int))
    
    for v in range(1, N + 1):
        # Count leaf neighbors and find non-leaf neighbors
        leaf_neighbors = []
        non_leaf_neighbors = []
        
        for neighbor in adj[v]:
            if is_leaf[neighbor]:
                leaf_neighbors.append(neighbor)
            else:
                non_leaf_neighbors.append(neighbor)
        
        num_leaves = len(leaf_neighbors)
        num_non_leaves = len(non_leaf_neighbors)
        
        # An intermediate node must have exactly 1 non-leaf neighbor (the center)
        # and at least 1 leaf neighbor (since y >= 1).
        if num_non_leaves == 1 and num_leaves >= 1:
            center_node = non_leaf_neighbors[0]
            y = num_leaves
            # This node v can be an intermediate node for center_node with parameter y
            center_y_counts[center_node][y] += 1

    max_kept = 0
    
    # Iterate over all potential centers
    # A center must be a non-leaf node? 
    # If a node is a leaf, it has 0 non-leaf neighbors, so it won't appear as a key in center_y_counts
    # unless it has a non-leaf neighbor. But if it's a leaf, it has degree 1.
    # If its only neighbor is non-leaf, then it's a leaf. It can't be an intermediate node itself.
    # Can a leaf be a center? 
    # If center is a leaf, it has 1 neighbor. That neighbor must be an intermediate node.
    # But an intermediate node needs to connect to the center.
    # If the center is a leaf, the intermediate node's non-leaf neighbor is the center.
    # So yes, a leaf CAN be a center if it has a neighbor that is a valid intermediate node.
    # However, our logic above: v is intermediate, u is center.
    # If u is a leaf, it appears as a key in center_y_counts if some v points to it.
    # So we just iterate over all keys in center_y_counts.
    
    for center, y_map in center_y_counts.items():
        for y, x in y_map.items():
            # x is the number of intermediate nodes for this center and y
            # Kept nodes = 1 (center) + x * (1 + y)
            kept = 1 + x * (1 + y)
            if kept > max_kept:
                max_kept = kept

    # If max_kept is 0, it means no valid snowflake tree was found.
    # But the problem guarantees it's always possible.
    # The smallest snowflake is x=1, y=1 -> 3 nodes.
    # If N=3 and it's a line 1-2-3, then 2 is center, 1 and 3 are leaves.
    # Node 2: non-leaf neighbors? None (1 and 3 are leaves). So num_non_leaves=0.
    # Wait. In a line 1-2-3:
    # Node 1: leaf. Neighbor 2 (non-leaf).
    # Node 3: leaf. Neighbor 2 (non-leaf).
    # Node 2: neighbors 1, 3. Both are leaves.
    # So for Node 2: num_leaves=2, num_non_leaves=0.
    # It doesn't satisfy num_non_leaves==1.
    # So Node 2 is not considered an intermediate node.
    # Who is the center?
    # If we pick Node 2 as center:
    # Neighbors are 1 and 3.
    # Node 1: leaf. Can it be an intermediate node?
    # Node 1 has neighbor 2 (non-leaf). num_non_leaves=1. num_leaves=0.
    # y=0 is not allowed (y>=1).
    # So Node 1 cannot be an intermediate node.
    # This logic seems to fail for the line graph 1-2-3.
    
    # Let's re-read the definition.
    # "Prepare one vertex." (Center)
    # "Prepare x more vertices, and connect each of them to the vertex prepared in step 2." (Intermediates)
    # "For each of the x vertices prepared in step 3, attach y leaves to it."
    
    # In 1-2-3:
    # If Center=2, Intermediates={1,3}? No, 1 and 3 are leaves in the original tree.
    # But in the Snowflake Tree, 1 and 3 are leaves attached to intermediates.
    # Wait. The problem says "Consider deleting zero or more vertices... so that the remaining graph becomes a single Snowflake Tree."
    # The remaining graph IS the Snowflake Tree.
    # In the remaining graph, the nodes 1 and 3 are leaves.
    # The node 2 is the center.
    # Are there intermediate nodes?
    # If x=1, y=1: Center connected to 1 intermediate. Intermediate connected to 1 leaf.
    # Total nodes: 1+1+1=3.
    # Structure: Center -- Intermediate -- Leaf.
    # In 1-2-3, if we keep all nodes, is it a Snowflake Tree?
    # If Center=2, Intermediate=1, Leaf=3? No, 1 is connected to 2 and 3.
    # If Center=2, Intermediate=3, Leaf=1? Same.
    # If Center=1, Intermediate=2, Leaf=3?
    # Center 1 connected to Intermediate 2. Intermediate 2 connected to Leaf 3.
    # This works! x=1, y=1.
    # So Center=1, Intermediate=2, Leaf=3.
    # Let's check our logic for this case.
    # Node 2: Neighbors 1, 3.
    # Is 1 a leaf? In the ORIGINAL tree, yes (degree 1).
    # Is 3 a leaf? In the ORIGINAL tree, yes (degree 1).
    # So Node 2 has 2 leaf neighbors. num_leaves=2.
    # Non-leaf neighbors: None. num_non_leaves=0.
    # So Node 2 is NOT an intermediate node in our logic.
    
    # Why? Because we assumed the "non-leaf neighbor" is the center.
    # But in the original tree, the center might be a leaf!
    # If the center is a leaf in the original tree, then for an intermediate node v,
    # its neighbor u (the center) is a leaf in the original tree.
    # So u is NOT a non-leaf neighbor.
    # Our definition of "non-leaf neighbor" was based on the original tree's degrees.
    # This is a flaw.
    
    # Correction:
    # An intermediate node v in the Snowflake Tree has degree y+1 in the Snowflake Tree.
    # In the original tree, v must have at least y+1 neighbors? No, we delete nodes.
    # But we keep v and its y leaf children and its center parent.
    # So in the original tree, v must be connected to its center and its y leaves.
    # The key is: In the Snowflake Tree, the neighbors of v are:
    # 1. The center (1 node).
    # 2. y leaves.
    # All these nodes must exist in the original tree and be kept.
    # The center is NOT a leaf in the Snowflake Tree. But it might be a leaf in the original tree.
    # The y leaves are leaves in the Snowflake Tree. They MUST be leaves in the original tree?
    # Not necessarily. They could have other neighbors in the original tree that are deleted.
    # BUT, if a node is a leaf in the Snowflake Tree, it has degree 1 in the Snowflake Tree.
    # If it has degree > 1 in the original tree, we must delete all other neighbors.
    # This is allowed.
    # However, if we keep a node as a leaf in the Snowflake Tree, we keep it and its single edge to its parent (intermediate).
    # We delete all other edges incident to it.
    # This means any node in the original tree can potentially be a leaf in the Snowflake Tree,
    # provided we delete its other neighbors.
    # BUT, if we delete a neighbor, that neighbor is gone.
    # The constraint is that the remaining graph is connected and forms the Snowflake structure.
    
    # Let's rethink.
    # We keep a set of vertices S. The induced subgraph on S is a Snowflake Tree.
    # S consists of:
    # - 1 Center C.
    # - x Intermediates I_1 ... I_x.
    # - x*y Leaves L_1 ... L_{xy}.
    # Edges in S:
    # - (C, I_j) for all j.
    # - (I_j, L_{j,k}) for all j, k.
    # No other edges.
    
    # This implies:
    # 1. In the original tree, C must be connected to each I_j.
    # 2. In the original tree, each I_j must be connected to each L_{j,k}.
    # 3. There are no other edges between nodes in S in the original tree?
    #    No, the induced subgraph must NOT have other edges.
    #    So if there is an edge between C and L_{j,k} in the original tree, we cannot keep both C and L_{j,k} unless that edge is part of the Snowflake structure. But C is not connected to L in Snowflake. So we cannot keep both if they are adjacent in original tree?
    #    Actually, if we keep both, the edge exists in the induced subgraph.
    #    So, for the induced subgraph to be EXACTLY the Snowflake Tree, there must be NO extra edges.
    #    This means:
    #    - C cannot be adjacent to any L in the original tree.
    #    - I_j cannot be adjacent to I_k (j!=k) in the original tree.
    #    - I_j cannot be adjacent to L_{m,n} (m!=j) in the original tree.
    #    - L_{j,k} cannot be adjacent to L_{m,n} in the original tree.
    
    # This is a very strong condition.
    # However, we can delete vertices.
    # If we keep a set S, the induced subgraph must be the Snowflake Tree.
    
    # Let's go back to the candidate approach but fix the "leaf" definition.
    # In the Snowflake Tree, the leaves L have degree 1.
    # In the original tree, a node L can be a leaf in the Snowflake Tree if:
    # - It is connected to its parent I in the original tree.
    # - All other neighbors of L in the original tree are DELETED.
    # This is always possible if we delete those neighbors.
    # So ANY node can be a leaf in the Snowflake Tree, as long as we delete its other neighbors.
    # BUT, if we delete a neighbor, that neighbor is not in S.
    
    # The cost is the number of deleted vertices.
    # We want to maximize |S|.
    # |S| = 1 + x + x*y.
    
    # Let's fix the Center C and the parameter y.
    # We need to choose x intermediates I_1 ... I_x.
    # Each I_j must be a neighbor of C in the original tree.
    # Each I_j must have y neighbors in the original tree that will be its leaves L_{j,1} ... L_{j,y}.
    # These L nodes must be neighbors of I_j in the original tree.
    # Also, C, I_j, and L_{j,k} must not have any other edges between them in the original tree (except the ones in the Snowflake structure).
    # And we must ensure that no other nodes in S are connected to each other outside the Snowflake structure.
    
    # This seems complex. Let's look at the constraints and sample cases.
    # Sample 1: 8 nodes. Output 1.
    # Edges: 1-3, 2-3, 3-4, 4-5, 5-6, 5-7, 4-8.
    # Tree structure:
    # 3 is connected to 1, 2, 4.
    # 4 is connected to 3, 5, 8.
    # 5 is connected to 4, 6, 7.
    # Leaves: 1, 2, 6, 7, 8.
    # Delete 8. Remaining: 1,2,3,4,5,6,7.
    # Edges: 1-3, 2-3, 3-4, 4-5, 5-6, 5-7.
    # Is this a Snowflake Tree?
    # Center 3? Neighbors 1,2,4.
    # If Center=3, Intermediates={4}?
    # 4 is connected to 3.
    # 4 has neighbors 5. (1,2 are connected to 3, not 4).
    # So 4 has 1 leaf child? 5 is not a leaf in the remaining tree (connected to 6,7).
    # So this doesn't work with Center=3.
    
    # Sample output says: Snowflake Tree with x=2, y=2.
    # Total nodes = 1 + 2 + 4 = 7.
    # Deleted 1 node (8).
    # Structure: Center connected to 2 intermediates. Each intermediate connected to 2 leaves.
    # Let's try Center=5.
    # Neighbors of 5: 4, 6, 7.
    # If Intermediates are 4 and ...?
    # 4 is connected to 5.
    # 4's other neighbors in remaining tree: 3.
    # 3 is connected to 1, 2.
    # This looks like Center=5, Intermediate=4, and 4 has children 3 and ...?
    # No, 4 is connected to 3. 3 is connected to 1,2.
    # If 3 is a leaf, then 4 has 1 leaf child.
    # But we need y=2.
    
    # Let's try Center=4.
    # Neighbors of 4: 3, 5, 8(deleted).
    # So neighbors 3, 5.
    # If Intermediates are 3 and 5.
    # For Intermediate 3: Neighbors in remaining tree: 1, 2.
    # 1 and 2 are leaves. So 3 has 2 leaf children. y=2.
    # For Intermediate 5: Neighbors in remaining tree: 6, 7.
    # 6 and 7 are leaves. So 5 has 2 leaf children. y=2.
    # Center 4 is connected to 3 and 5.
    # This works! x=2, y=2.
    # Kept nodes: 4 (center) + 3,5 (intermediates) + 1,2,6,7 (leaves) = 7 nodes.
    # Deleted: 8.
    
    # So, in this case:
    # Center 4.
    # Intermediate 3: Neighbors 1,2 (leaves).
    # Intermediate 5: Neighbors 6,7 (leaves).
    # Note that 3 and 5 are NOT leaves in the original tree.
    # 1,2,6,7 ARE leaves in the original tree.
    
    # So my previous logic was:
    # "An intermediate node v must have exactly y leaf neighbors and exactly 1 non-leaf neighbor."
    # In this case:
    # Node 3: Neighbors 1,2,4.
    # 1,2 are leaves. 4 is non-leaf.
    # So Node 3 has 2 leaf neighbors and 1 non-leaf neighbor (4).
    # This fits the pattern! y=2, center=4.
    # Node 5: Neighbors 4,6,7.
    # 6,7 are leaves. 4 is non-leaf.
    # So Node 5 has 2 leaf neighbors and 1 non-leaf neighbor (4).
    # This fits the pattern! y=2, center=4.
    
    # So the logic holds IF we define "leaf" as "leaf in the original tree".
    # And "non-leaf" as "not a leaf in the original tree".
    # And the center is a non-leaf node.
    
    # What if the center is a leaf in the original tree?
    # Example: 1-2-3-4.
    # Can we make a Snowflake Tree?
    # Delete 1,4? Keep 2,3. No, need at least 3 nodes.
    # Delete 1? Keep 2,3,4.
    # 2-3-4.
    # Center 3, Intermediate 2, Leaf 1? No, 1 is deleted.
    # Center 3, Intermediate 4, Leaf ?
    # 4 has no other neighbors.
    # Center 2, Intermediate 3, Leaf 4.
    # x=1, y=1.
    # Kept: 2,3,4. Deleted: 1.
    # Is 2 a leaf in original tree? Yes.
    # Is 3 a non-leaf? Yes.
    # Is 4 a leaf? Yes.
    # So Center=2 (leaf in original).
    # Intermediate=3.
    # Node 3: Neighbors 2,4.
    # 2 is a leaf in original tree.
    # 4 is a leaf in original tree.
    # So Node 3 has 2 leaf neighbors.
    # Non-leaf neighbors: None.
    # So Node 3 does NOT fit the pattern "1 non-leaf neighbor".
    
    # But this IS a valid Snowflake Tree!
    # Center 2, Intermediate 3, Leaf 4.
    # The edge is 2-3 and 3-4.
    # In the original tree, 2 is a leaf.
    # So the "non-leaf neighbor" assumption is wrong.
    # The center can be a leaf in the original tree.
    # If the center is a leaf, then for an intermediate node v, its neighbor u (center) is a leaf.
    # So u is NOT a non-leaf neighbor.
    
    # Revised Logic:
    # An intermediate node v in the Snowflake Tree has:
    # - 1 parent (the center).
    # - y children (leaves).
    # In the original tree, v must be connected to its parent and its y children.
    # The parent can be ANY node (leaf or non-leaf).
    # The children must be leaves in the Snowflake Tree.
    # Do the children have to be leaves in the original tree?
    # If a child L has other neighbors in the original tree, we must delete them.
    # This is allowed.
    # So ANY node can be a leaf in the Snowflake Tree.
    # However, if we keep L as a leaf, we keep the edge (v, L).
    # We delete all other edges incident to L.
    # This means L can be any node.
    
    # But wait, if L is not a leaf in the original tree, say L has degree 3.
    # We keep L and its edge to v. We delete L's other 2 neighbors.
    # This is valid.
    # So, in the original tree, v must have at least y+1 neighbors?
    # No, v must have at least 1 neighbor that will be the center, and y neighbors that will be leaves.
    # These y+1 neighbors must be distinct.
    # So v must have degree at least y+1 in the original tree.
    # And we select 1 neighbor as center, y neighbors as leaves.
    # The remaining neighbors of v (if any) must be deleted.
    
    # Also, the center C must be connected to v.
    # And C must not be connected to any other intermediate or leaf in the Snowflake Tree (except its own intermediates).
    # And C's other neighbors (if any) must be deleted.
    
    # This suggests we should iterate over all possible centers C.
    # For a fixed center C, we look at its neighbors.
    # Each neighbor v can be:
    # 1. An intermediate node.
    # 2. Deleted.
    # If v is an intermediate node, it must have y leaf children.
    # This means v must have at least y neighbors other than C.
    # We choose y of them to be leaves.
    # The cost of keeping v as an intermediate with y leaves is:
    # We keep v, C, and y leaves.
    # We delete all other neighbors of v.
    # We also delete all other neighbors of C (except the chosen intermediates).
    
    # This is getting complicated because the choice of y affects the cost.
    # And y is global for the Snowflake Tree.
    
    # Let's go back to the sample 1 logic which worked.
    # The key was that the leaves in the Snowflake Tree WERE leaves in the original tree.
    # And the intermediates had exactly 1 non-leaf neighbor (the center).
    
    # What if we assume that the optimal solution always uses leaves from the original tree as leaves in the Snowflake Tree?
    # And intermediates have exactly 1 non-leaf neighbor?
    # This worked for Sample 1 and Sample 2.
    # Sample 2: 1-2-3.
    # Center 1 (leaf). Intermediate 2. Leaf 3.
    # Node 2: Neighbors 1,3. Both leaves.
    # Non-leaf neighbors: 0.
    # So it doesn't fit "1 non-leaf neighbor".
    
    # So the "1 non-leaf neighbor" rule is not universal.
    # It fails when the center is a leaf.
    
    # Let's handle the case where the center is a leaf separately?
    # Or, generalize:
    # An intermediate node v has 1 parent (center) and y children (leaves).
    # In the original tree, v has degree d_v.
    # It uses 1 edge to parent, y edges to children.
    # The remaining d_v - 1 - y edges must be deleted.
    # The parent C is a neighbor of v.
    # The children are y neighbors of v.
    # All these must be distinct.
    # So d_v >= y+1.
    
    # For a fixed center C and fixed y, we want to choose x intermediates.
    # Each intermediate v must be a neighbor of C.
    # And v must have at least y other neighbors (to be leaves).
    # If v has exactly y other neighbors, then all of them are leaves.
    # If v has more than y other neighbors, we must choose y of them to be leaves, and delete the rest.
    # But if we delete a neighbor of v, that neighbor is gone.
    # Can that neighbor be used as a leaf for another intermediate? No, it's deleted.
    # Can it be used as a leaf for C? No, C's leaves are not a thing.
    
    # To minimize deletions, we want to maximize kept nodes.
    # Kept nodes = 1 (C) + x (intermediates) + x*y (leaves).
    # For a fixed C and y, we should pick as many intermediates as possible.
    # An intermediate v is valid if it has at least y neighbors other than C.
    # If it has exactly y, cost to keep it is 0 (we keep all its neighbors).
    # If it has more than y, we must delete some.
    # But if we delete a neighbor of v, we lose that node.
    # Is it better to delete v entirely or keep it with some leaves?
    # If we keep v with y leaves, we keep 1+y nodes.
    # If we delete v, we delete 1 node (v) and all its other neighbors are either deleted or kept as something else?
    # No, if v is deleted, its neighbors are not affected unless they are also deleted.
    
    # This is a complex optimization problem.
    # Given the constraints and the nature of competitive programming, there might be a simpler observation.
    # Observation: The Snowflake Tree is a star of stars.
    # Center C.
    # x branches. Each branch is a star with center I_j and y leaves.
    # The I_j are connected to C.
    
    # Let's iterate over all possible centers C.
    # For each C, we want to find the best y and x.
    # For a fixed C and y, each neighbor v of C can be an intermediate node if:
    # - v has at least y neighbors other than C.
    # - We choose y of them to be leaves.
    # - The cost of keeping v is: we keep v and y leaves. We delete the other neighbors of v.
    # - The gain is 1+y nodes.
    # - The loss is (deg(v)-1-y) nodes (the other neighbors of v).
    # - But wait, if we delete a neighbor of v, that node is gone.
    # - We also delete all other neighbors of C (except the chosen intermediates).
    
    # Let S_C be the set of neighbors of C.
    # For each v in S_C, let k_v = deg(v) - 1 (number of neighbors other than C).
    # If we make v an intermediate with parameter y, we need k_v >= y.
    # The number of kept nodes in this branch is 1 (v) + y (leaves).
    # The number of deleted nodes in this branch is k_v - y (other neighbors of v).
    # If we don't make v an intermediate, we delete the entire branch at v.
    # The number of deleted nodes is k_v + 1 (v and all its other neighbors).
    # Wait, if we delete v, do we delete its other neighbors?
    # Yes, because they are only connected to v (and possibly others, but if they are only in this branch, they are deleted).
    # But if a neighbor of v is also a neighbor of C, it's not in this branch.
    # But in a tree, there are no cycles. So a neighbor of v cannot be a neighbor of C unless it is C itself.
    # So the branches at C are independent.
    
    # So for a fixed C and y, for each neighbor v:
    # Option 1: Keep v as intermediate. Valid if k_v >= y.
    #   Kept: 1+y. Deleted: k_v - y.
    # Option 2: Delete v.
    #   Kept: 0. Deleted: k_v + 1.
    
    # We must choose at least one intermediate (x >= 1).
    # We want to maximize total kept nodes.
    # Total kept = 1 (C) + sum over chosen intermediates of (1+y).
    # Total deleted = N - Total kept.
    
    # For a fixed C and y, we should choose all neighbors v with k_v >= y to be intermediates?
    # Yes, because keeping v gives 1+y kept nodes, and deleting it gives 0.
    # And there's no conflict between branches.
    # So x = number of neighbors v of C with k_v >= y.
    # If x == 0, this (C,y) is invalid.
    # Max kept for (C,y) = 1 + x * (1+y).
    
    # We iterate over all C and all y.
    # What are the possible y?
    # y can be from 1 to max(k_v).
    # max(k_v) is max degree - 1.
    
    # Algorithm:
    # 1. Compute degrees.
    # 2. For each node C, look at its neighbors.
    # 3. For each neighbor v, compute k_v = deg(v) - 1.
    # 4. We want to find y that maximizes 1 + x_y * (1+y), where x_y is the count of neighbors with k_v >= y.
    # 5. x_y is a non-increasing function of y.
    # 6. We can iterate y from 1 to max_k.
    # 7. But N is 3*10^5. Iterating all y for all C is O(N^2).
    # 8. We need a faster way.
    
    # For a fixed C, let the values of k_v for its neighbors be k_1, k_2, ..., k_d.
    # Sort them in descending order: k_(1) >= k_(2) >= ... >= k_(d).
    # For y <= k_(d), x_y = d.
    # For k_(d) < y <= k_(d-1), x_y = d-1.
    # ...
    # For k_(i) < y <= k_(i-1), x_y = i.
    # (With k_(0) = infinity).
    
    # We want to maximize 1 + i * (1+y) for y in (k_(i+1), k_(i)].
    # For a fixed i, the function f(y) = 1 + i*(1+y) is increasing in y.
    # So the maximum for a fixed i is at y = k_(i).
    # So we only need to check y = k_(i) for each i from 1 to d.
    # And also y=1 if k_(d) >= 1.
    
    # So for each C:
    # - Get k_v for all neighbors v.
    # - Sort k_v.
    # - For each unique value k in the sorted list, let i be the number of neighbors with k_v >= k.
    # - Calculate kept = 1 + i * (1+k).
    # - Update global max.
    
    # Complexity:
    # Sum of degrees is 2N.
    # Sorting the k_v for each C takes O(deg(C) log deg(C)).
    # Total time: Sum deg(C) log deg(C) <= N log N.
    # This is efficient.

    max_kept = 0
    
    for C in range(1, N + 1):
        # Get k_v for all neighbors
        k_vals = []
        for v in adj[C]:
            k_v = degree[v] - 1
            if k_v >= 1: # y >= 1, so we need at least 1 leaf
                k_vals.append(k_v)
        
        if not k_vals:
            continue
            
        k_vals.sort(reverse=True)
        
        # For each unique k, calculate kept
        # We can iterate through the sorted list
        # For the i-th element (0-indexed), the number of neighbors with k_v >= k_vals[i] is i+1.
        # But we should only consider y = k_vals[i].
        # And we should avoid duplicates.
        
        # Let's just iterate through the sorted list and consider y = k_vals[i]
        # The number of intermediates is i+1.
        
        for i, k in enumerate(k_vals):
            x = i + 1
            y = k
            kept = 1 + x * (1 + y)
            if kept > max_kept:
                max_kept = kept

    print(N - max_kept)

solve()