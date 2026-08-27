import sys

# Increase recursion depth just in case, though we will use iterative approach or sys.setrecursionlimit
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 3:
        # Constraints say N >= 3, but handle gracefully
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # We need to iterate over each node as the potential center.
    # For a fixed center c, we root the tree at c.
    # The neighbors of c are the roots of the subtrees.
    # For each neighbor v, we need to know the number of children v has in the tree rooted at c.
    # Let this be d_v. Then v can support any y in [1, d_v].
    # We want to maximize 1 + y * (count of neighbors v with d_v >= y).

    # To do this efficiently for all centers, we can use a rerooting technique or simply
    # iterate. Since N is up to 3*10^5, O(N^2) is too slow.
    # However, the sum of degrees is 2N. If we process each node's neighbors,
    # the total work is proportional to sum of degrees = 2N.
    # For each node c, we collect the list of d_v for all neighbors v.
    # Then we sort this list and compute the max value.
    # Sorting a list of size k takes O(k log k). Sum of k log k over all nodes
    # is bounded by O(N log N) in worst case (e.g. star graph, center has N-1 neighbors).
    # Actually, sum of k_i = 2N. The worst case for sum k_i log k_i is when one k_i is large.
    # Max k_i is N-1. So O(N log N) is acceptable.

    max_kept = 0

    # We can perform a DFS to compute subtree sizes and parent pointers if we fix a root,
    # but since we are iterating over ALL possible centers, we need the "children count"
    # relative to each center.
    # Note: For a center c, the "children" of a neighbor v are all neighbors of v except c.
    # So d_v = degree(v) - 1 if v is not the root of the whole tree? No.
    # When we root at c, the neighbors of c are the immediate children of c.
    # For a neighbor v, its children in the rooted tree are all its neighbors except c.
    # So d_v = len(adj[v]) - 1.
    # This holds for ALL neighbors v of c.
    # So for a fixed center c, the list of degrees is simply [len(adj[v]) - 1 for v in adj[c]].
    # We only consider v where len(adj[v]) - 1 >= 1, i.e., len(adj[v]) >= 2.
    # If len(adj[v]) == 1, then v is a leaf in the original tree, so d_v = 0, cannot be intermediate.

    for c in range(1, N + 1):
        # Get the degrees of neighbors relative to c
        # d_v = degree(v) - 1
        neighbor_degrees = []
        for v in adj[c]:
            deg_v = len(adj[v])
            if deg_v >= 2:
                neighbor_degrees.append(deg_v - 1)
        
        if not neighbor_degrees:
            # No neighbor can be an intermediate node
            continue
        
        # We want to maximize y * count(d_v >= y)
        # Sort the degrees in descending order to easily count how many are >= y
        neighbor_degrees.sort(reverse=True)
        
        # Iterate through possible y values.
        # The critical y values are the values present in neighbor_degrees.
        # For a given y, the count of neighbors with degree >= y is the number of elements in neighbor_degrees >= y.
        # Since neighbor_degrees is sorted descending, if we pick y = neighbor_degrees[i],
        # then the count is i + 1 (indices 0 to i).
        # However, we can also pick y smaller than neighbor_degrees[i] but larger than neighbor_degrees[i+1].
        # The function f(y) = y * count is maximized at one of the values in neighbor_degrees.
        # Why? Because count is a step function that only changes at values in neighbor_degrees.
        # Between two consecutive distinct values u < v, count is constant. f(y) = y * C is increasing in y.
        # So the maximum must occur at the largest y in that interval, which is v.
        
        current_max_for_c = 0
        
        # Iterate through the sorted degrees
        # neighbor_degrees[i] is the (i+1)-th largest degree.
        # There are i+1 neighbors with degree >= neighbor_degrees[i].
        # So for y = neighbor_degrees[i], the kept intermediate nodes count is i+1.
        # Kept vertices = 1 + (i+1) * neighbor_degrees[i]
        
        for i, d in enumerate(neighbor_degrees):
            # d is the degree of the (i+1)-th neighbor
            # Count of neighbors with degree >= d is at least i+1.
            # Note: There might be multiple neighbors with the same degree.
            # If we pick y = d, all neighbors with degree >= d are valid.
            # Since the list is sorted descending, all neighbors from index 0 to i have degree >= d.
            # Neighbors from i+1 onwards have degree <= d.
            # If neighbor_degrees[i+1] == d, then the count is actually larger.
            # But we will encounter that larger count when we process the later index with the same d.
            # So it's sufficient to just check y = d with count = i+1.
            # The true count for y=d is the number of elements >= d.
            # Let's find the last index with value >= d.
            # Actually, since we iterate i from 0, and d is non-increasing,
            # for a specific value v, the first time we see it, the count is minimal for that y.
            # The last time we see it, the count is maximal.
            # So we should just check the last occurrence of each distinct degree?
            # Or simply, since f(y) is increasing in y for fixed count, and count is non-increasing in y,
            # we just need to check y = d for each d.
            # The value calculated is 1 + (i+1)*d.
            # Is it possible that a smaller y gives a better result?
            # Suppose we have degrees [5, 2].
            # i=0, d=5: count=1, val = 1 + 1*5 = 6.
            # i=1, d=2: count=2, val = 1 + 2*2 = 5.
            # What if y=1? Count=2, val = 1 + 2*1 = 3.
            # What if y=3? Count=1 (only 5>=3), val = 1 + 1*3 = 4.
            # So checking y=d at each step covers the local maxima.
            
            kept = 1 + (i + 1) * d
            if kept > current_max_for_c:
                current_max_for_c = kept
        
        if current_max_for_c > max_kept:
            max_kept = current_max_for_c

    # The answer is the minimum deletions, which is N - max_kept
    print(N - max_kept)

solve()