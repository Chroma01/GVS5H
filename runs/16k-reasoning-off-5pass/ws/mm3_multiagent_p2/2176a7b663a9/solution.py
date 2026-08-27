import sys
from sys import stdin

def main():
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(next(it))
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(next(it))
        R[i] = int(next(it))
    
    # Build interval graph H (overlap = edge) and its complement G
    # We need connected components of G = co-interval graph
    # G has edge (i,j) iff R[i] < L[j] or R[j] < L[i]
    
    # Approach: find components using sweep + DSU
    # Sort intervals by L, process in order
    # For each interval I, merge with all intervals J with R[J] < L[I]
    # Use a trick: maintain a "representative" array, and only merge distinct components
    
    # Sort intervals by L (and by R as tiebreak for determinism)
    order = list(range(1, N + 1))
    order.sort(key=lambda x: (L[x], R[x]))
    
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
    
    # For each interval I, we need to find all intervals J with R[J] < L[I]
    # that are in distinct DSU components, and merge them with I.
    # 
    # Key trick: process intervals in order of L. For each I, find the "rightmost"
    # interval J with R[J] < L[I] (i.e., the one with largest R[J] < L[I]).
    # Connect I to J. This handles the case where ended intervals are already
    # connected through earlier processing.
    #
    # But ended intervals might be in multiple components. We need to connect I
    # to all of them.
    #
    # Observation: if J_1 and J_2 both have R < L[I], and they're in different
    # components, then connecting I to one doesn't merge with the other.
    # We need to find the representative of each distinct component.
    #
    # Use a dict: for each component rep, store the "rightmost R" in that component.
    # When processing I, iterate over all J with R[J] < L[I], find their reps,
    # and merge I with each distinct rep.
    #
    # To make this efficient: maintain a "last processed" map. When we process
    # an interval J (add it to the "ended" set), we store it. When processing I,
    # we iterate over ended intervals in order of R, and skip those already
    # processed (via "last_rep" tracking).
    
    # Maintain a sorted list of "ended" intervals by R
    # Actually, maintain a list of intervals in order of R, and a pointer
    # to the "rightmost ended" position.
    
    # Simpler: sort all intervals by R. For each I (in order of L), find all
    # intervals with R < L[I] using a pointer into the R-sorted list.
    # These are "candidates". For each candidate, find its DSU rep.
    # If the rep is the same as the last one we processed, skip.
    # Otherwise, merge I with it.
    
    by_R = sorted(range(1, N + 1), key=lambda x: (R[x], L[x]))
    r_ptr = 0  # pointer into by_R
    last_rep = 0  # last DSU rep we merged with
    
    # For each I in order of L:
    for idx in order:
        # Advance r_ptr to include all intervals with R < L[idx]
        target = L[idx]
        while r_ptr < N and R[by_R[r_ptr]] < target:
            j = by_R[r_ptr]
            rep_j = find(j)
            if rep_j != last_rep and rep_j != idx:
                union(idx, rep_j)
                last_rep = find(idx)  # update after merge
            r_ptr += 1
        last_rep = 0  # reset for next I
    
    # Now also handle "right" connections: for each I, intervals with L > R[I]
    # Process in reverse order of R (or forward order of L from the other side)
    # Sort intervals by R descending
    by_R_desc = sorted(range(1, N + 1), key=lambda x: (-R[x], -L[x]))
    # For each I in order of decreasing R, find intervals with L > R[I]
    # Sort intervals by L ascending for the "future" set
    by_L = sorted(range(1, N + 1), key=lambda x: (L[x], R[x]))
    l_ptr = 0  # this won't work as is; need different structure
    
    # Actually, the left-to-right pass already handles all connections because:
    # If I connects to J (R[J] < L[I]), they're in the same component.
    # If J connects to K (R[K] < L[J]), they're in the same component.
    # So transitively, I, J, K are in the same component.
    # 
    # But what about J_1 and J_2 both with R < L[I], in different components?
    # If they're in different components of G, then there's no path between them
    # in G. But I connects to both (since R[J_1], R[J_2] < L[I]). So after
    # processing I, J_1, J_2, I are all in the same component (via I).
    # 
    # The left-to-right pass with the "last_rep" trick handles this:
    # When processing I, we iterate over all J with R[J] < L[I] (in order of R).
    # For each, we find its DSU rep. If it's a new rep (different from last),
    # we merge I with it. This ensures I is connected to all distinct components
    # among the ended intervals.
    # 
    # So the left-to-right pass should be sufficient! Let me verify.
    # 
    # Wait, but what about connections via "right" intervals?
    # E.g., I and J where R[I] < L[J]. In the left-to-right pass (sorted by L),
    # J is processed after I (since L[J] > L[I] usually, but not always).
    # When J is processed, we look at intervals with R < L[J]. I has R[I] < L[J],
    # so I is included. So J merges with I's component. Good.
    # 
    # But what if I is processed after J? Then when I is processed, we look at
    # intervals with R < L[I]. J has L[J] > R[I] (since R[I] < L[J]), so J's R
    # might be > L[I], so J is not in the "ended" set. So I doesn't merge with J.
    # But J was already processed and merged with I (or I's component).
    # Wait, if J is processed first and I is processed later:
    # - J is processed: looks at intervals with R < L[J]. I has R[I] < L[J] (given),
    #   so I is in the "ended" set when J is processed. J merges with I.
    # - So J and I are in the same component. Good.
    # 
    # So the left-to-right pass with the "last_rep" trick is sufficient!
    
    # Let me re-verify the last_rep logic:
    # When processing I, we iterate over intervals with R < L[I] in order of R.
    # For each such J, find rep. If rep != last_rep, merge I with rep.
    # This ensures I is merged with each distinct component exactly once.
    # 
    # But wait, after merging I with rep1, I's rep changes. Then we encounter
    # J_2 with rep2. If rep2 != new rep of I, we merge. But rep2 might equal
    # the old rep of I (before merge), which is the same as last_rep.
    # So we correctly skip it.
    # 
    # Actually, after union(idx, rep_j), I's new rep is the merged one.
    # We update last_rep = find(idx). Then next J with same rep_j is skipped.
    # Next J with different rep is merged.
    # 
    # This looks correct.
    
    # Now answer queries
    Q = int(next(it))
    out = []
    for _ in range(Q):
        s = int(next(it))
        t = int(next(it))
        if find(s) == find(t):
            # Same component - need to compute shortest path
            # For now, placeholder: use a simple approach
            # TODO: compute actual shortest path
            out.append(str(W[s] + W[t]))  # placeholder: direct edge weight
        else:
            out.append("-1")
    
    print("\n".join(out))

if __name__ == "__main__":
    main()