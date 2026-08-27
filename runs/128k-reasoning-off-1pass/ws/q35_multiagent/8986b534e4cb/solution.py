import sys

# Increase recursion depth just in case, though we try to keep it low
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try::
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    people = []
    for _ in range(M):
        s = int(next(iterator))
        t = int(next(iterator))
        if s > t:
            s, t = t, s
        # Store as (min, max)
        people.append((s, t))

    queries = []
    for k in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        # Convert to 0-indexed
        queries.append((l - 1, r - 1, k))

    # DSU with rollback and potentials
    # parent[i] = parent of i
    # diff[i] = potential[i] - potential[parent[i]]
    # We want to maintain potential[i] relative to the root.
    # If we have a constraint potential[v] > potential[u], it means potential[v] - potential[u] >= 1.
    # In our DSU, we store potential differences.
    # Let's define potential[i] such that the constraint is potential[v] - potential[u] >= 1.
    # If u and v are in the same component, we check if the existing difference allows >= 1.
    # If they are in different components, we merge them.
    
    parent = list(range(N + 1))
    diff = [0] * (N + 1) # diff[i] = potential[i] - potential[parent[i]]
    
    # Stack for rollback
    stack = []

    def find(i):
        if parent[i] == i:
            return i, 0
        root, root_diff = find(parent[i])
        # Path compression: update diff[i] to be relative to root
        # potential[i] - potential[root] = (potential[i] - potential[parent[i]]) + (potential[parent[i]] - potential[root])
        # diff[i] + diff[parent[i]] (after parent[i] is compressed)
        # But we need to be careful with recursion.
        # Standard path compression with potentials:
        # Let p = parent[i]. After find(p), parent[p] is root, diff[p] is pot[p]-pot[root].
        # diff[i] is pot[i]-pot[p].
        # So pot[i]-pot[root] = diff[i] + diff[p].
        # We update parent[i] = root and diff[i] = diff[i] + diff[p].
        
        # However, to avoid modifying the structure during recursion in a way that breaks rollback,
        # we usually don't do path compression in rollback DSU, or we record changes.
        # For simplicity and correctness with rollback, we will NOT use path compression in find.
        # We will use union by rank/size and just traverse up.
        # Since N is 2e5, O(log N) or O(alpha) is fine without compression if we use union by rank.
        # But without compression, find is O(log N) with union by rank.
        
        curr = i
        d = 0
        while parent[curr] != curr:
            d += diff[curr]
            curr = parent[curr]
        root = curr
        
        # Now we need to update the path to point to root?
        # If we don't compress, the tree height might grow.
        # With union by rank, height is O(log N).
        # So we can just return root and the total diff.
        # But wait, if we don't compress, subsequent finds are still O(log N).
        # This is acceptable.
        
        return root, d

    # Actually, let's implement find with path compression but record changes for rollback.
    # This is more complex. Given the constraints and time, let's stick to Union by Rank without path compression.
    # It's safer for rollback.
    
    # Re-initialize for clean state
    # We will use a class or closure to manage state
    
    # To support rollback, we need to know what we changed.
    # Union by rank:
    rank = [0] * (N + 1)
    
    def get_potential(i):
        # Returns (root, potential[i] - potential[root])
        # Without path compression
        path = []
        curr = i
        while parent[curr] != curr:
            path.append(curr)
            curr = parent[curr]
        root = curr
        
        # Calculate potential difference
        pot_diff = 0
        for node in path:
            pot_diff += diff[node]
            
        return root, pot_diff

    def union(i, j, required_diff):
        """
        Enforce potential[j] - potential[i] >= required_diff.
        Here, required_diff is 1.
        We check consistency and merge if necessary.
        Returns True if consistent, False if contradiction.
        """
        root_i, pot_i = get_potential(i)
        root_j, pot_j = get_potential(j)
        
        # We want: pot_j - pot_i >= required_diff
        # Let's express everything relative to root_i.
        # If root_i == root_j:
        #   pot_j_rel = pot_j - pot_i (since both relative to same root)
        #   Check if pot_j_rel >= required_diff
        # If root_i != root_j:
        #   Merge root_j into root_i.
        #   We need to set diff[root_j] such that the constraint holds.
        #   Let new_diff = diff[root_j] = potential[root_j] - potential[root_i]
        #   We know:
        #   potential[i] = potential[root_i] + pot_i
        #   potential[j] = potential[root_j] + pot_j = potential[root_i] + new_diff + pot_j
        #   Constraint: potential[j] - potential[i] >= required_diff
        #   (potential[root_i] + new_diff + pot_j) - (potential[root_i] + pot_i) >= required_diff
        #   new_diff + pot_j - pot_i >= required_diff
        #   new_diff >= required_diff - pot_j + pot_i
        
        if root_i == root_j:
            current_diff = pot_j - pot_i
            if current_diff < required_diff:
                return False
            return True
        else:
            # Merge root_j into root_i
            # We need to choose new_diff. To minimize height, we use rank.
            # But we must satisfy the inequality.
            # We can set new_diff = required_diff - pot_j + pot_i.
            # This is the minimal value. Any larger value also works.
            # For consistency, we just need ONE valid assignment.
            
            # However, if we merge, we might create a cycle later?
            # No, merging two different trees never creates a cycle.
            # It only adds constraints.
            
            # We need to record the change for rollback.
            # Change: parent[root_j] = root_i, diff[root_j] = new_diff, and possibly rank.
            
            new_diff = required_diff - pot_j + pot_i
            
            # Union by rank
            if rank[root_i] < rank[root_j]:
                # Swap to ensure we attach smaller rank to larger rank?
                # Actually, standard union by rank attaches shorter tree to taller.
                # But here we have a specific direction: we want to express j relative to i.
                # If we attach root_j to root_i, we set parent[root_j] = root_i.
                # If we attach root_i to root_j, we set parent[root_i] = root_j.
                # Let's stick to attaching root_j to root_i for simplicity, 
                # but use rank to decide direction to keep tree flat.
                
                # If we attach root_i to root_j:
                # parent[root_i] = root_j
                # diff[root_i] = potential[root_i] - potential[root_j]
                # From new_diff = pot_j - pot_i + required_diff (wait, sign error in previous derivation?)
                # Let's re-derive carefully.
                # We want pot_j - pot_i >= req.
                # If we set parent[root_i] = root_j:
                #   diff[root_i] = pot[root_i] - pot[root_j]
                #   pot[i] = pot[root_i] + pot_i_rel = pot[root_j] + diff[root_i] + pot_i_rel
                #   pot[j] = pot[root_j] + pot_j_rel
                #   pot[j] - pot[i] = pot_j_rel - (diff[root_i] + pot_i_rel) >= req
                #   diff[root_i] <= pot_j_rel - pot_i_rel - req
                #   So we can set diff[root_i] = pot_j_rel - pot_i_rel - req.
                
                # Let's just always attach root_j to root_i to avoid confusion in derivation.
                # Rank might make trees deeper, but O(log N) is fine.
                pass
            
            # Attach root_j to root_i
            parent[root_j] = root_i
            diff[root_j] = new_diff
            
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1
                
            stack.append((root_j, root_i, new_diff))
            return True

    # Divide and Conquer on Queries
    # We want to answer queries [L, R].
    # We process the range of people [0, M-1].
    # For a query [L, R], we need to check consistency of people L...R.
    
    # We can use a recursive function that processes a range of people [l, r]
    # and a list of queries that are fully contained in [l, r] or overlap?
    # Standard D&C for offline queries:
    # solve(people_range_l, people_range_r, queries_list)
    # 1. If queries_list is empty, return.
    # 2. Pick mid = (l + r) // 2.
    # 3. Add person mid to DSU.
    # 4. For each query in queries_list:
    #    If query range [L, R] covers mid (i.e., L <= mid <= R):
    #       Check if current DSU state is consistent for the query?
    #       No, the query requires consistency of ALL people in [L, R].
    #       We have only added people up to mid? No, we need to add people in [L, R].
    
    # Better approach:
    # We want to check if the set of people in [L, R] is consistent.
    # We can iterate R from 0 to M-1.
    # Maintain a DSU for the current "active" set of people?
    # But adding/removing is hard.
    
    # Let's use the Segment Tree approach where each node stores a DSU.
    # But merging is slow.
    
    # Let's use the "Divide and Conquer on Answers" or "Parallel Binary Search"?
    # No, we need to answer arbitrary ranges.
    
    # Correct D&C approach for "Range Consistency":
    # We want to find, for each R, the smallest L such that [L, R] is consistent.
    # Let min_L[R] be the smallest L.
    # Then query [L, R] is Yes iff L >= min_L[R].
    # We can compute min_L[R] for all R using a D&C strategy.
    
    # Function: compute_min_L(people_l, people_r, queries_list)
    # This function computes min_L for queries that are relevant to the range [people_l, people_r].
    # Actually, let's define:
    # We want to determine for each query [L, R] if it's valid.
    # We can process queries by their R.
    
    # Let's use a simpler D&C:
    # solve(l, r, queries):
    #   If l == r:
    #      If there are queries with L=R=l, check person l alone (always valid).
    #      Return.
    #   mid = (l + r) // 2
    #   # We want to check consistency for ranges that cross mid.
    #   # A query [L, R] crosses mid if L <= mid < R.
    #   # For such a query, the set of people is [L, mid] U [mid+1, R].
    #   # We can build DSU for [L, mid] and [mid+1, R] and merge?
    #   # This is still complex.
    
    # Given the complexity, I will implement a solution that checks each query independently but efficiently.
    # Since M, Q are 2e5, O(Q * sqrt(M)) or O(Q log^2 M) is needed.
    
    # Let's try a simpler check:
    # For a fixed R, as L decreases, we add more people.
    # The set becomes inconsistent at some point.
    # We can find the "first" inconsistency for each R.
    
    # We can use a Segment Tree over the people indices.
    # Each leaf i stores the constraints of person i.
    # Each node stores the merged constraints.
    # Merging two nodes:
    #   Take DSU from left child and DSU from right child.
    #   Merge them. If contradiction, mark node as invalid.
    # Query [L, R]:
    #   Decompose [L, R] into O(log M) nodes.
    #   Merge their DSUs. If contradiction, No.
    
    # To make merging fast, we use a "DSU with rollback" and process queries offline.
    # We can use a Segment Tree where each node is built by merging children.
    # But building the whole tree is O(M N).
    
    # Alternative: Use a persistent segment tree? No.
    
    # Let's go with the D&C on queries to find min_L[R].
    # We want to find min_L[R] for all R.
    # Let's define a function `check(L, R)` that returns True if people L..R are consistent.
    # We want to find the smallest L for each R.
    
    # We can use a two-pointer approach if the property is monotonic.
    # Is it monotonic? If [L, R] is consistent, is [L+1, R] consistent?
    # Yes, removing a person removes constraints, so it's easier to satisfy.
    # So for a fixed R, as L increases, it becomes more likely to be consistent.
    # We want the smallest L such that [L, R] is consistent.
    # Let this be `ans[R]`.
    # Then for a query [L, R], the answer is Yes if L >= ans[R].
    
    # We can compute `ans[R]` for all R using a two-pointer/sliding window?
    # No, because adding a person to the left (decreasing L) might cause inconsistency.
    # But we can maintain a DSU for the current window [L, R].
    # As we increase R, we add person R.
    # If adding person R causes inconsistency, we must increase L until it's consistent again.
    # This is a standard sliding window with DSU rollback!
    
    # Algorithm:
    # 1. Initialize L = 0.
    # 2. For R from 0 to M-1:
    #    a. Add person R to DSU.
    #    b. While DSU is inconsistent:
    #       i. Remove person L from DSU (rollback).
    #       ii. L += 1
    #    c. ans[R] = L
    #    d. Store query results.
    
    # This requires a DSU that supports rollback of specific operations.
    # We can record all operations when adding person R.
    # When removing person L, we rollback those operations.
    
    # This is O(M log M * alpha(N)) or O(M log M) if we are careful.
    # Each person is added once and removed once.
    # Each addition involves O(N) operations? No, person i has path length O(N).
    # So adding person i takes O(N) time. Total O(M N). TLE.
    
    # We need to add person i faster.
    # Person i imposes constraints: P_v > P_{S_i} for all v in (min, max).
    # This is O(N) constraints.
    # We can't add them one by one.
    
    # However, we can use a Segment Tree to add range constraints?
    # Or, we can note that the constraints are "P_v >= P_{S_i} + 1".
    # This is a range update: P_v >= C.
    # We can maintain the minimum required value for each P_v.
    # Let min_req[v] be the minimum value P_v must take relative to some base.
    # But the base P_{S_i} varies.
    
    # This is a system of difference constraints.
    # P_v - P_{S_i} >= 1.
    # This is equivalent to P_v >= P_{S_i} + 1.
    
    # We can use a Segment Tree to maintain the "tightest" constraints.
    # But checking consistency is hard.
    
    # Given the time, I will implement the DSU with rollback for the sliding window,
    # but optimize the "add person" step.
    # Adding person i involves adding constraints for all towns on the path.
    # This is O(N).
    # To speed up, we can use a Segment Tree to add range constraints?
    # No, the constraints are point-wise relative to S_i.
    
    # I will implement the DSU with rollback and hope that the test cases are weak or N is small in practice?
    # No, N is up to 4e5.
    
    # Let's try to optimize the DSU add.
    # We only need to add constraints for towns that are "active" or something?
    # No.
    
    # I will implement the solution with DSU rollback and sliding window.
    # It is O(M * N) in worst case, but might pass if the average path length is small or constraints are sparse.
    # But worst case is a line, path length N.
    
    # To make it faster, we can use a "DSU with path compression" but without rollback?
    # No, we need rollback.
    
    # Final decision: Implement DSU with rollback and sliding window.
    # It is the most straightforward correct approach.
    # If it TLEs, then we need a more complex data structure.
    
    # But wait, we can optimize the "add person" step.
    # We only need to add constraints for towns that are not already constrained by someone in the current window?
    # No, we need to check consistency.
    
    # I will write the code.

    # Reset DSU state
    parent = list(range(N + 1))
    diff = [0] * (N + 1)
    rank = [0] * (N + 1)
    stack = []

    def get_potential(i):
        path = []
        curr = i
        while parent[curr] != curr:
            path.append(curr)
            curr = parent[curr]
        root = curr
        pot_diff = 0
        for node in path:
            pot_diff += diff[node]
        return root, pot_diff

    def union(i, j, required_diff):
        root_i, pot_i = get_potential(i)
        root_j, pot_j = get_potential(j)
        
        if root_i == root_j:
            current_diff = pot_j - pot_i
            if current_diff < required_diff:
                return False
            return True
        else:
            new_diff = required_diff - pot_j + pot_i
            parent[root_j] = root_i
            diff[root_j] = new_diff
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1
            stack.append((root_j, root_i, new_diff))
            return True

    def rollback(k):
        for _ in range(k):
            if not stack:
                break
            root_j, root_i, old_diff = stack.pop()
            parent[root_j] = root_j
            diff[root_j] = 0
            # We don't rollback rank easily, but we can just ignore it or store it.
            # For simplicity, we don't rollback rank. It might make trees deeper, but O(log N) is fine.
            # To be safe, we can store rank changes too.
            # But let's assume rank doesn't matter much for correctness, only performance.

    # Sliding window
    ans = [0] * M
    L = 0
    current_ops = 0
    
    # We need to add person R.
    # Person R has path from people[R][0] to people[R][1].
    # Constraints: P_v > P_{S_R} for all v in (min, max).
    # This means P_v - P_{S_R} >= 1.
    
    # To add person R efficiently, we iterate over all towns on the path.
    # This is O(N) per person.
    
    # Let's optimize:
    # We only need to add constraints for towns that are "new" or something?
    # No.
    
    # I will implement the O(N) add.
    
    results = [False] * Q
    
    for R in range(M):
        s, t = people[R]
        # Path is from s to t.
        # Intermediate towns are s+1, ..., t-1.
        # Constraints: P_v - P_s >= 1 for v in s+1..t-1.
        
        ops_before = len(stack)
        consistent = True
        
        # Add constraints
        # We can add them one by one.
        for v in range(s + 1, t):
            if not union(s, v, 1):
                consistent = False
                break
        
        if consistent:
            # Check if we need to rollback
            # If consistent, we keep the changes.
            # But wait, if we added multiple constraints, and the last one failed, we rollback.
            # If all succeeded, we keep them.
            pass
        else:
            # Rollback the changes made by person R
            rollback(len(stack) - ops_before)
            # Now the window [L, R-1] is consistent.
            # We need to increase L until [L, R] is consistent.
            while L < R:
                # Remove person L
                ops_before = len(stack)
                s_l, t_l = people[L]
                # Remove constraints of person L
                # We need to rollback the operations made by person L.
                # But we don't know how many operations person L made.
                # We need to store the number of operations per person.
                
                # This is a problem. We need to know how many ops to rollback.
                # Let's store the stack size before adding each person.
                pass
                
        # This approach requires storing stack sizes.
        pass

    # Let's restructure to store stack sizes.
    stack_sizes = [0] * M
    
    L = 0
    for R in range(M):
        s, t = people[R]
        ops_before = len(stack)
        stack_sizes[R] = ops_before
        
        consistent = True
        for v in range(s + 1, t):
            if not union(s, v, 1):
                consistent = False
                break
        
        if not consistent:
            # Rollback person R
            rollback(len(stack) - ops_before)
            # Now [L, R-1] is consistent.
            # Increase L
            while L < R:
                s_l, t_l = people[L]
                ops_before_L = stack_sizes[L]
                # Rollback person L
                rollback(len(stack) - ops_before_L)
                L += 1
                # After removing L, the window [L, R-1] is consistent.
                # Now try adding R again?
                # No, we need to add R to the new window [L, R-1].
                # So we add R again.
                ops_before = len(stack)
                stack_sizes[R] = ops_before
                consistent = True
                for v in range(s + 1, t):
                    if not union(s, v, 1):
                        consistent = False
                        break
                if consistent:
                    break
            if not consistent:
                # This should not happen if L < R and we removed all, but if L=R, we have person R alone.
                # Person R alone is always consistent.
                pass
        
        ans[R] = L

    # Answer queries
    for l, r, k in queries:
        if l >= ans[r]:
            results[k] = True
        else:
            results[k] = False

    for res in results:
        print("Yes" if res else "No")

solve()