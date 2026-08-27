import sys

def solve():
    # Increase recursion depth just in case, though we use iterative approaches
    sys.setrecursionlimit(1000000)
    
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
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
        
    # Normalize intervals so that S < T for all people
    # The problem states |S_i - T_i| > 1, so they are never adjacent.
    # We can swap if S > T to maintain a consistent direction (left to right).
    # This simplifies the "interleaving" check to S_i < S_j < T_i < T_j.
    for i in range(1, M + 1):
        if S[i] > T[i]:
            S[i], T[i] = T[i], S[i]
            
    queries = []
    for k in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        queries.append((L, R))
        
    # We need to check if there exists any pair (i, j) in [L, R] such that
    # S_i < S_j < T_i < T_j.
    # This is equivalent to checking if the set of intervals {[S_i, T_i]} has any "crossing"
    # where one starts before another and ends after it.
    #
    # Algorithm:
    # 1. Sort the people by their start point S_i.
    # 2. For a query range [L, R], we consider the subset of people in this range.
    #    Let this subset be P. We want to know if there exist i, j in P such that
    #    S_i < S_j < T_i < T_j.
    #    Since we sort by S, if we pick i and j from the sorted list with i < j (so S_i <= S_j),
    #    the condition becomes S_i < S_j < T_i < T_j.
    #    Note: If S_i == S_j, they cannot satisfy S_i < S_j, so strict inequality handles distinct starts.
    #    However, the problem guarantees (S_i, T_i) != (S_j, T_j). It does not guarantee distinct S.
    #    But if S_i == S_j, then S_i < S_j is false, so no crossing possible between them.
    #    So we only care about pairs with distinct S.
    #
    #    Condition: S_i < S_j < T_i < T_j.
    #    This implies T_i > S_j. Also T_j > T_i.
    #    So for a fixed j (with larger S), we need to find an i (with smaller S) such that:
    #    S_i < S_j AND T_i > S_j AND T_i < T_j.
    #    Wait, the condition is T_i < T_j.
    #    So we need an i such that S_i < S_j < T_i < T_j.
    #    This means T_i must be in the range (S_j, T_j).
    #
    #    Let's rephrase:
    #    We have a set of intervals. We want to know if any two intervals cross strictly.
    #    Interval i: [S_i, T_i]. Interval j: [S_j, T_j].
    #    Crossing: S_i < S_j < T_i < T_j.
    #
    #    Approach using Segment Tree / Fenwick Tree:
    #    We can process queries offline. Sort queries by R (or L).
    #    Let's sort queries by R. We iterate R from 1 to M.
    #    When we are at R, we add person R to our data structure.
    #    The query asks about range [L, R].
    #    We need to check if there is any pair (i, j) with L <= i < j <= R such that S_i < S_j < T_i < T_j.
    #    Since we process by R, j is the current element being added.
    #    We need to check if there exists an i in [L, j-1] such that S_i < S_j < T_i < T_j.
    #    This breaks down to:
    #    1. S_i < S_j
    #    2. T_i > S_j
    #    3. T_i < T_j
    #
    #    So for a fixed j, we need to query the set of active i's (where L <= i < j) to see if
    #    there is any i satisfying: S_i < S_j AND T_i in (S_j, T_j).
    #
    #    Data Structure:
    #    We need to store pairs (S_i, T_i) for i in the current range [L, j-1].
    #    We need to query: count of i such that S_i < S_j and S_j < T_i < T_j.
    #    If count > 0, then Yes.
    #
    #    Since we process queries offline, we can use a 2D range sum query or a persistent segment tree.
    #    However, N and M are up to 4e5 and 2e5. A 2D structure might be heavy.
    #    Let's use a Fenwick Tree (BIT) over the S coordinates.
    #    But the condition on T_i is also a range.
    #    We can use a Segment Tree where each node stores a sorted list of T values? No, that's too slow.
    #    Better: Use a Segment Tree over the S-coordinates. Each leaf corresponds to an S value.
    #    But multiple people can have the same S.
    #    Actually, we can map the problem to:
    #    We have points (S_i, T_i). We want to check if there is a point (S_i, T_i) in the rectangle
    #    (-inf, S_j) x (S_j, T_j).
    #    Since we process j from 1 to M, we insert (S_j, T_j) into the structure.
    #    For a query [L, R], we consider j in [L, R]. We need to check if any previous i (in [L, j-1])
    #    satisfies the condition.
    #    This is equivalent to: Is there any point in the set { (S_k, T_k) | L <= k < j } that lies in
    #    the region S < S_j and S_j < T < T_j?
    #
    #    We can use a Segment Tree over the S-coordinates (1 to N).
    #    Each node in the segment tree will maintain a data structure to query the T values.
    #    Specifically, we want to know if there is a T value in (S_j, T_j) among the points with S < S_j.
    #    This looks like a 2D range query: count points in x < S_j and y in (S_j, T_j).
    #    Since the queries are offline and we add points one by one, we can use a Fenwick Tree over the S-axis?
    #    No, because the T constraint is dynamic.
    #
    #    Alternative: Divide and Conquer (CDQ Divide and Conquer) or simply a Segment Tree with Merge Sort Tree logic.
    #    Given the constraints and the nature of the query (offline), we can use a Segment Tree over the S-coordinates.
    #    In each node of the segment tree (covering a range of S values), we store a sorted list of T values
    #    for all people whose S falls in that range.
    #    Wait, if we build this structure statically for all M people, then for a query [L, R], we need to
    #    consider only people with index in [L, R].
    #    This suggests we need to handle the index constraint [L, R] as well.
    #
    #    Let's refine the offline approach:
    #    We have points (S_i, T_i) with an associated index i.
    #    Query: Given L, R, is there a pair (i, j) with L <= i < j <= R such that S_i < S_j < T_i < T_j?
    #    This is equivalent to: Does the set of points { (S_k, T_k) | L <= k <= R } contain a crossing pair?
    #    Note that if we just check the whole set, we might pick i < L or j > R.
    #    But the condition "L <= i < j <= R" is crucial.
    #
    #    Let's try a different perspective.
    #    Sort all people by S. Let the sorted order be p_1, p_2, ..., p_M.
    #    The condition S_i < S_j < T_i < T_j implies that in the sorted order, i comes before j (unless S_i = S_j, which is impossible for strict inequality).
    #    So we are looking for a pair (i, j) in the original index range [L, R] such that in the S-sorted order, i appears before j, and the crossing condition holds.
    #    This seems complicated because the "before" relation depends on S, not the original index.
    #
    #    Let's go back to the standard 2D range query idea.
    #    We want to detect if there exists a pair (i, j) in [L, R] with S_i < S_j < T_i < T_j.
    #    This is equivalent to: Is there a pair (i, j) in [L, R] such that S_i < S_j and T_i > S_j and T_i < T_j?
    #    Let's fix j. We need an i in [L, j-1] (in original indices) such that S_i < S_j and S_j < T_i < T_j.
    #    If we process j from 1 to M, we can maintain a data structure of all i < j.
    #    But we have the constraint i >= L.
    #    This is a 3D range query problem:
    #    Points: (i, S_i, T_i).
    #    Query: Count points in box [L, j-1] x (-inf, S_j) x (S_j, T_j).
    #    If count > 0, then Yes.
    #    We need to answer Q queries.
    #    We can solve this with CDQ Divide and Conquer or a 3D data structure.
    #    Given N, M, Q <= 4e5, O((M+Q) log^2 M) or O((M+Q) log M) is needed.
    #    CDQ D&C is suitable for 3D range counting.
    #
    #    CDQ D&C Plan:
    #    1. Sort points by the first dimension (index i).
    #    2. Recursively solve.
    #    3. When merging left and right halves, we consider pairs where i is in left and j is in right.
    #       Condition: i < j is satisfied by the split.
    #       We need to check if there exists a pair (i, j) with i in Left, j in Right such that:
    #       S_i < S_j AND T_i > S_j AND T_i < T_j.
    #       Rearranging: S_i < S_j AND S_j < T_i < T_j.
    #       For a fixed j (in Right), we need an i (in Left) such that S_i < S_j and T_i in (S_j, T_j).
    #    4. To do this efficiently:
    #       Sort Left and Right halves by S.
    #       Iterate j in Right (sorted by S). Maintain a pointer for Left.
    #       As S_j increases, we add i's from Left with S_i < S_j into a data structure.
    #       The data structure needs to support: "Is there any value T_i in (S_j, T_j)?"
    #       This is a range query on T values.
    #       We can use a Fenwick Tree (BIT) over the T coordinates (1 to N).
    #       For each i added, update BIT at position T_i with +1.
    #       Query BIT for sum in range (S_j + 1, T_j - 1). If > 0, then we found a crossing.
    #    5. After processing, we must revert the BIT updates (or use rollback) to keep it clean for other queries.
    #       Since we only add, we can just rollback the changes.
    #
    #    Complexity: T(N) = 2T(N/2) + O(N log N) -> O(N log^2 N).
    #    This fits within the time limit (approx 2-3 seconds for 4e5).
    
    # Implementation Details:
    # - Points: (index, S, T)
    # - Queries: (L, R, query_id)
    # - We need to check if ANY pair exists. So if count > 0, mark query as Yes.
    # - We can combine points and queries into a single list and sort by index.
    # - Actually, CDQ D&C is usually done on the array of points.
    # - Let's create a list of events:
    #   Type 0: Point i (index, S_i, T_i)
    #   Type 1: Query k (L, R, id) -> effectively asking about range [L, R].
    #   But standard CDQ handles points. How to handle range queries?
    #   We can split the query [L, R] into two parts? No.
    #   The condition is "exists pair in [L, R]".
    #   We can treat the query as: "Does the set of points with index in [L, R] contain a crossing pair?"
    #   This is not a standard 3D range sum.
    #   However, we can rephrase:
    #   We want to know if there is a pair (i, j) such that L <= i < j <= R and conditions hold.
    #   This is equivalent to:
    #   (Exists pair in [1, R] satisfying conditions) AND (Not (Exists pair in [1, L-1] satisfying conditions) ... wait, no).
    #   The pair must be entirely within [L, R].
    #   This is a "subarray" query.
    #   We can use the CDQ approach on the array of people sorted by index.
    #   In the merge step, we consider pairs (i, j) where i is in Left half and j is in Right half.
    #   This covers all pairs where i < j.
    #   But we need to restrict to i >= L and j <= R.
    #   This suggests we should process queries by their R, and maintain a data structure for L?
    #   Or, we can use the CDQ D&C to solve the 3D problem:
    #   Points: (i, S_i, T_i).
    #   Query: Count pairs (i, j) such that L <= i < j <= R and S_i < S_j < T_i < T_j.
    #   Wait, counting pairs is hard. We just need existence.
    #   But existence is equivalent to count > 0.
    #   However, the query is "exists pair in [L, R]".
    #   This is not a simple 3D range sum because the condition involves two points.
    #   Let's reconsider the "offline by R" approach with a Segment Tree.
    #   We iterate R from 1 to M.
    #   We add person R to the data structure.
    #   We need to answer queries ending at R: [L, R].
    #   The query asks: Is there a pair (i, j) with L <= i < j <= R such that S_i < S_j < T_i < T_j?
    #   Since we are at R, j can be any index in [L, R].
    #   But if we fix j, we need an i in [L, j-1].
    #   This is still tricky because L varies.
    #
    #   Let's try the CDQ D&C on the array of people (sorted by index).
    #   We want to check if there is a crossing pair in the subarray [L, R].
    #   This is a classic problem: "Given an array of intervals, for each query [L, R], is there a crossing pair?"
    #   Actually, we can transform the condition.
    #   A pair (i, j) crosses if S_i < S_j < T_i < T_j.
    #   This implies T_i > S_j.
    #   Let's define a new value for each person: maybe related to T?
    #   Consider the condition S_i < S_j < T_i < T_j.
    #   This is equivalent to: S_i < S_j AND T_i > S_j AND T_i < T_j.
    #   Let's sort people by S.
    #   If we sort by S, then for any pair i, j with i < j (in sorted order), we have S_i <= S_j.
    #   If S_i < S_j, then we check T_i > S_j and T_i < T_j.
    #   So the problem becomes: In the subarray [L, R] of the original indices, does there exist a pair (i, j) such that
    #   (in S-sorted order, i comes before j) AND S_i < S_j AND T_i > S_j AND T_i < T_j.
    #   This is getting complicated due to the mix of original index and S-sorted order.
    #
    #   Let's go back to the 3D range query formulation.
    #   We want to find if there exists a pair (i, j) such that:
    #   1. L <= i < j <= R
    #   2. S_i < S_j
    #   3. S_j < T_i
    #   4. T_i < T_j
    #   This is NOT a standard 3D range query because it involves two points.
    #   However, we can iterate over j. For a fixed j, we need an i such that:
    #   L <= i < j <= R
    #   S_i < S_j
    #   S_j < T_i < T_j
    #   This is a 3D range query for i:
    #   i in [L, j-1]
    #   S_i in (-inf, S_j)
    #   T_i in (S_j, T_j)
    #   If we can answer this efficiently for all j in [L, R], we are done.
    #   But we have Q queries.
    #   We can process queries offline.
    #   Sort queries by R.
    #   Iterate R from 1 to M.
    #   Add person R to the data structure.
    #   For all queries ending at R (i.e., R_k == R), we need to check if there exists ANY j in [L, R] such that the condition holds.
    #   Wait, if we just check for j=R, we might miss a pair where j < R.
    #   So we need to maintain the state of "is there a crossing pair in [L, R]?"
    #   Let's maintain a value `ans[L]` for each L.
    #   When we move from R-1 to R, we add person R.
    #   Person R can form a crossing pair with any i < R.
    #   If such an i exists with i >= L, then the query [L, R] is satisfied.
    #   So, for the current R, we check if there is any i in [L, R-1] satisfying the condition.
    #   If yes, then for all queries [L, R], the answer is Yes.
    #   We can maintain an array `possible[L]` which is True if there exists a crossing pair in [L, R-1].
    #   When we add R, we check for each L if there is an i in [L, R-1] satisfying the condition.
    #   If so, we set `possible[L] = True`.
    #   Then for all queries [L, R], if `possible[L]` is True, output Yes.
    #   But updating `possible[L]` for all L is O(N). Total O(N*M) -> TLE.
    #
    #   Optimization:
    #   We need to check if there exists i in [L, R-1] such that S_i < S_R and S_R < T_i < T_R.
    #   Let's denote the condition for i as: S_i < S_R and T_i in (S_R, T_R).
    #   We want to know if there is such an i with index >= L.
    #   This is equivalent to: Let min_index = min { i | i < R and S_i < S_R and T_i in (S_R, T_R) }.
    #   If min_index >= L, then Yes.
    #   So we need to query the minimum index i satisfying the 2D condition.
    #   Data Structure:
    #   We have points (S_i, T_i) with index i.
    #   Query: Min index i such that S_i < X and Y < T_i < Z.
    #   This is a 2D range query (on S and T) returning min index.
    #   We can use a Segment Tree over S coordinates.
    #   Each node stores a sorted list of T values? No, we need min index.
    #   We can use a Segment Tree over S. Each leaf corresponds to an S value.
    #   But multiple people have same S.
    #   Actually, we can use a Fenwick Tree over S? No, T is also a dimension.
    #   We can use a Segment Tree over S, and in each node, maintain a data structure for T.
    #   Since we process R from 1 to M, we add points one by one.
    #   We can use a Segment Tree over S (1..N).
    #   Each node in the segment tree will store a list of (T, index) pairs.
    #   But we need to query min index in a range of T.
    #   We can use a Segment Tree over T as well? That's 2D.
    #   Or, since we only add points, we can use a Fenwick Tree over T?
    #   Wait, the condition is S_i < S_R.
    #   So we only care about points with S < S_R.
    #   We can maintain a data structure that stores all points added so far.
    #   Query: Min index i such that S_i < S_R and T_i in (S_R, T_R).
    #   This is a 2D range query.
    #   We can solve this with a Segment Tree over S.
    #   In each node of the S-segment tree, we store a sorted list of T values?
    #   No, we need min index.
    #   Let's use a Segment Tree over S. Each node maintains a Fenwick Tree over T? Too heavy.
    #   Alternative: Use a Segment Tree over T.
    #   Query: Min index i such that S_i < S_R and T_i in (S_R, T_R).
    #   We can use a Segment Tree over T (1..N).
    #   Each node in the T-segment tree stores a list of S values?
    #   No, we need min index.
    #   Let's use a Segment Tree over T. Each node stores a list of (S, index) pairs.
    #   When we add a point (S_i, T_i, i), we update the path in the T-segment tree.
    #   But we need to query S_i < S_R.
    #   This is a 2D range query.
    #   We can use a Fenwick Tree over T, where each node stores a sorted list of S?
    #   No, we need min index.
    #   Let's use a Segment Tree over T. Each node stores a list of S values.
    #   But we need min index.
    #   Actually, we can use a Segment Tree over T, and each node stores a list of S values.
    #   Then we can binary search? No.
    #
    #   Let's try the CDQ D&C approach again. It is robust for 3D range queries.
    #   We want to find if there exists a pair (i, j) with L <= i < j <= R and S_i < S_j < T_i < T_j.
    #   This is equivalent to:
    #   Exists j in [L, R] such that there exists i in [L, j-1] with S_i < S_j and T_i in (S_j, T_j).
    #   Let's define a query for each j: "Does there exist i in [L, j-1] with S_i < S_j and T_i in (S_j, T_j)?"
    #   This is a 3D range query: i in [L, j-1], S_i < S_j, T_i in (S_j, T_j).
    #   We can solve this for all j and all queries.
    #   We can use CDQ D&C on the array of people (sorted by index).
    #   In the merge step, we consider pairs (i, j) with i in Left, j in Right.
    #   We need to check if there is a pair (i, j) such that L <= i < j <= R.
    #   Since i is in Left and j is in Right, i < j is satisfied.
    #   We need to check if there is a pair (i, j) with L <= i and j <= R.
    #   This means we need to check if there is a pair (i, j) in the merge step such that i >= L and j <= R.
    #   This is a 2D range query on the pairs (i, j) generated in the merge step?
    #   No, we generate pairs on the fly.
    #   We can treat the query as: "Is there a pair (i, j) in the current merge step such that L <= i and j <= R?"
    #   And we also need S_i < S_j and T_i in (S_j, T_j).
    #   This is getting complex.
    #
    #   Simpler approach:
    #   We can use the fact that we only need existence.
    #   Let's use a Segment Tree over the S-coordinates.
    #   We process queries offline.
    #   Sort queries by R.
    #   Iterate R from 1 to M.
    #   Add person R to the Segment Tree.
    #   The Segment Tree will store information about the "best" i for each S range.
    #   Specifically, for a given S_j, we want to know if there is an i < R (and i >= L) such that S_i < S_j and T_i in (S_j, T_j).
    #   We can maintain a Segment Tree over S (1..N).
    #   Each node in the Segment Tree will store the minimum index i such that T_i is in some range?
    #   No.
    #   Let's use a Segment Tree over S.
    #   Each leaf s stores a list of T values for people with S_i = s.
    #   But we need to query min index.
    #   Let's use a Segment Tree over S.
    #   Each node stores a Fenwick Tree over T? No.
    #   Let's use a Segment Tree over S.
    #   Each node stores a list of (T, index) pairs.
    #   We want to query: min index i such that S_i < S_j and T_i in (S_j, T_j).
    #   This is a 2D range query.
    #   We can use a Segment Tree over S.
    #   In each node, we store a sorted list of T values.
    #   But we need min index.
    #   We can store a Segment Tree over T in each node of the S-segment tree? Too heavy.
    #
    #   Let's try a different approach:
    #   We can use a Segment Tree over T (1..N).
    #   Each node in the T-segment tree stores a list of S values.
    #   When we add a person (S_i, T_i, i), we update the path in the T-segment tree.
    #   For each node covering a range of T, we add (S_i, i) to the list.
    #   Then for a query (S_j, T_j), we query the range (S_j, T_j) in the T-segment tree.
    #   We want min index i such that S_i < S_j.
    #   So in each node of the T-segment tree, we store a list of (S, index) pairs.
    #   We sort these lists by S.
    #   Then we can binary search for S < S_j and find the min index.
    #   But we need to combine results from multiple nodes.
    #   This is a standard technique: Merge Sort Tree.
    #   We build a Merge Sort Tree over T.
    #   Each node stores a sorted list of (S, index) pairs.
    #   Query: Range (S_j, T_j) in T. Find min index i such that S_i < S_j.
    #   We decompose the range (S_j, T_j) into O(log N) nodes.
    #   In each node, we binary search for S < S_j and find the min index.
    #   Then we take the global min.
    #   But we also need the constraint i >= L.
    #   This is the problem. The Merge Sort Tree stores all points added so far.
    #   We need to filter by i >= L.
    #   This suggests we need to handle the L constraint.
    #   We can use the offline processing by L?
    #   Sort queries by L descending.
    #   Iterate L from M down to 1.
    #   Add person L to the data structure.
    #   For queries starting at L, we check if there is a pair (i, j) with i >= L and j <= R.
    #   Since we add L, we have all points with index >= L.
    #   We need to check if there is a pair (i, j) with i >= L, j <= R, and crossing condition.
    #   This is still hard because j <= R is a constraint on the second point.
    #
    #   Let's go back to the CDQ D&C on the array of people.
    #   We want to check if there is a pair (i, j) in [L, R] with crossing condition.
    #   This is equivalent to:
    #   (Exists pair in [1, R] with crossing) AND (Not (Exists pair in [1, L-1] with crossing) ... no).
    #   Actually, we can use the property that if there is a crossing pair in [L, R], then there is a crossing pair in [1, R] that is "compatible" with L?
    #   No.
    #
    #   Let's try the "offline by R" with a Segment Tree over S, but storing min index.
    #   We process R from 1 to M.
    #   We add person R.
    #   We want to answer queries [L, R].
    #   Query: Is there a pair (i, j) with L <= i < j <= R and crossing?
    #   Since we are at R, j can be R or any previous j.
    #   But if we maintain the state "is there a crossing pair in [L, R]?", we can update it.
    #   Let `ans[L]` be a boolean: is there a crossing pair in [L, R]?
    #   When we move from R-1 to R:
    #   1. Check if person R forms a crossing pair with any i in [L, R-1].
    #      If yes, then `ans[L] = True` for all L such that i >= L.
    #      So for each i that forms a crossing pair with R, we set `ans[L] = True` for L in [1, i].
    #   2. Also, if `ans[L]` was already True, it remains True.
    #   So we need to support:
    #      - Update: Set `ans[L] = True` for L in [1, i].
    #      - Query: Is `ans[L]` True?
    #   This is a range update, point query.
    #   We can use a Segment Tree or Fenwick Tree for this.
    #   But we need to find all i that form a crossing pair with R.
    #   For a fixed R, we need to find all i < R such that S_i < S_R and T_i in (S_R, T_R).
    #   This is a 2D range query: count i in [1, R-1] with S_i < S_R and T_i in (S_R, T_R).
    #   If count > 0, then there exists such an i.
    #   But we need to know the specific i to update the range [1, i].
    #   Actually, if there are multiple such i, we need to update [1, min_i] where min_i is the minimum index among them.
    #   Because if there is an i, then for any L <= i, the pair (i, R) is in [L, R].
    #   So we need min_i = min { i | i < R, S_i < S_R, T_i in (S_R, T_R) }.
    #   If min_i exists, we update `ans[L] = True` for L in [1, min_i].
    #   So the algorithm is:
    #   1. Iterate R from 1 to M.
    #   2. Query min_i = min { i | i < R, S_i < S_R, T_i in (S_R, T_R) }.
    #   3. If min_i exists, update `ans[L] = True` for L in [1, min_i].
    #   4. Answer queries ending at R.
    #
    #   Step 2 is a 2D range query: min index in rectangle (-inf, S_R) x (S_R, T_R).
    #   We can use a Segment Tree over S.
    #   Each node stores a list of (T, index) pairs.
    #   But we need min index.
    #   We can use a Segment Tree over S.
    #   Each node stores a Fenwick Tree over T? No.
    #   We can use a Segment Tree over S.
    #   Each node stores a sorted list of T values.
    #   But we need min index.
    #   We can store a Segment Tree over T in each node of the S-segment tree? No.
    #   We can use a Segment Tree over S.
    #   Each node stores a list of (T, index) pairs.
    #   We want to query min index for T in (S_R, T_R).
    #   We can use a Segment Tree over S.
    #   Each node stores a list of (T, index) pairs.
    #   We sort the list by T.
    #   Then we can binary search for T in (S_R, T_R) and find the min index.
    #   But we need to combine results from multiple nodes.
    #   This is a standard technique: Merge Sort Tree.
    #   We build a Merge Sort Tree over S.
    #   Each node stores a sorted list of (T, index) pairs.
    #   Query: Range (-inf, S_R) in S. Find min index for T in (S_R, T_R).
    #   We decompose (-inf, S_R) into O(log N) nodes.
    #   In each node, we binary search for T in (S_R, T_R) and find the min index.
    #   Then we take the global min.
    #   This is O(log^2 N) per query.
    #   Total complexity: O(M log^2 N + Q log N).
    #   This fits.
    
    # Implementation:
    # - Build a Merge Sort Tree over S (1..N).
    #   - Each leaf s stores a list of (T, index) for people with S_i = s.
    #   - Each internal node merges the lists of children, sorted by T.
    # - For each R from 1 to M:
    #   - Query the tree for min index i in range [1, S_R - 1] with T_i in (S_R, T_R).
    #   - If found, update a Segment Tree (or Fenwick) for `ans` array: range update [1, min_i] to True.
    #   - Answer queries ending at R.
    # - The `ans` array can be maintained using a Fenwick Tree that supports range update, point query?
    #   - We want to know if `ans[L]` is True.
    #   - Update: Set `ans[L] = True` for L in [1, min_i].
    #   - Query: Is `ans[L]` True?
    #   - We can use a Fenwick Tree where we add 1 at min_i.
    #   - Then `ans[L]` is True if sum(L) > 0? No.
    #   - If we update [1, min_i], then for any L <= min_i, the sum at L should be > 0.
    #   - We can use a Fenwick Tree where we add 1 at min_i.
    #   - Then query(L) = sum(L). If sum(L) > 0, then there was an update covering L.
    #   - Yes, because updates are always [1, x]. So if x >= L, then sum(L) > 0.
    #   - So we just need a Fenwick Tree that supports point update (add 1 at x) and prefix sum.
    #   - Wait, if we have multiple updates, sum(L) will be the count of updates with x >= L.
    #   - If count > 0, then Yes.
    #   - So yes, a Fenwick Tree works.
    
    # Steps:
    # 1. Build Merge Sort Tree over S.
    # 2. Initialize Fenwick Tree for `ans`.
    # 3. Iterate R from 1 to M:
    #    a. Query MST for min_i in S < S_R and T in (S_R, T_R).
    #    b. If min_i exists, update Fenwick at min_i with +1.
    #    c. For each query ending at R, check if Fenwick.query(L) > 0.
    
    # Complexity:
    # - Build MST: O(M log N).
    # - Query MST: O(log^2 N).
    # - Update Fenwick: O(log N).
    # - Total: O(M log^2 N + Q log N).
    # - With N=4e5, M=2e5, Q=2e5, this is acceptable.
    
    # Note: S and T are 1-indexed.
    # MST size: 4*N.
    # Each node stores a list.
    
    # Edge cases: S_R - 1 might be 0.
    # T_i in (S_R, T_R) means S_R < T_i < T_R.
    
    # Let's implement.
    
    # Data structures:
    # - people: list of (S, T, index)
    # - queries: list of (L, R, id)
    # - mst: list of lists
    # - bit: Fenwick Tree
    
    # Precompute MST:
    # - Sort people by S.
    # - Build MST over S coordinates.
    # - Actually, we can just build the MST by sorting people by S and then building the tree.
    # - But we need to handle multiple people with same S.
    # - We can just use the S values as indices.
    # - People are 1..M.
    # - We can create an array `pos` where pos[s] = list of (T, index) for people with S=s.
    # - Then build the MST.
    
    # Wait, the MST is over S coordinates (1..N).
    # We can build it by:
    # - Create an array `tree` of size 4*N.
    # - Function build(node, start, end):
    #   - If start == end:
    #     - tree[node] = sorted list of (T, index) for people with S = start.
    #   - Else:
    #     - mid = (start + end) // 2
    #     - build(2*node, start, mid)
    #     - build(2*node+1, mid+1, end)
    #     - tree[node] = merge(tree[2*node], tree[2*node+1])
    
    # Query function:
    # - query(node, start, end, l, r, min_T, max_T):
    #   - If range [start, end] is outside [l, r], return infinity.
    #   - If range [start, end] is inside [l, r]:
    #     - Binary search in tree[node] for T in (min_T, max_T).
    #     - Find min index among those.
    #   - Else:
    #     - return min(query(left), query(right))
    
    # This is O(log^2 N).
    
    # Let's code.
    
    pass

# Re-implementing the logic in the final code block.