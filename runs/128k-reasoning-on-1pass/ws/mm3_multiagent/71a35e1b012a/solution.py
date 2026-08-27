import sys
import bisect

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    intervals = []
    for i in range(M):
        L, R = map(int, input().split())
        intervals.append((L, R, i))
    
    # Sort intervals by L
    intervals.sort(key=lambda x: (x[0], x[1]))
    
    # Build distinct L values and top3 for each distinct L
    distinct_L = []
    top3 = []  # top3[i] is list of (R, idx) for top 3 intervals with L_i <= distinct_L[i]
    current_top3 = []  # list of (R, idx)
    i = 0
    while i < M:
        L = intervals[i][0]
        distinct_L.append(L)
        # add all intervals with this L
        j = i
        while j < M and intervals[j][0] == L:
            R, idx = intervals[j][1], intervals[j][2]
            # merge with current_top3
            # we want to keep top 3 by R
            new_list = current_top3 + [(R, idx)]
            new_list.sort(key=lambda x: -x[0])
            current_top3 = new_list[:3]
            j += 1
        i = j
        top3.append(current_top3[:])
    
    # Function to cover [a, b] using intervals not in exclude_set
    INF = float('inf')
    def cover(a, b, exclude_set):
        if a > b:
            return [], 0
        cur = a
        used = []
        count = 0
        # Safety limit to avoid infinite loops
        max_iters = 1000000
        iters = 0
        while cur < b:
            iters += 1
            if iters > max_iters:
                return None, INF
            # find largest L_i <= cur
            idx = bisect.bisect_right(distinct_L, cur) - 1
            if idx < 0:
                return None, INF
            # get top3 for distinct_L[idx]
            cand = top3[idx]  # list of (R, idx) sorted by descending R
            chosen = None
            for R, ii in cand:
                if ii not in exclude_set and R > cur:
                    chosen = (R, ii)
                    break
            if chosen is None:
                # maybe there is an interval with L_i < that L_i? but all such intervals are in top3[idx]
                # However, if all top3 are in exclude_set or have R <= cur, impossible
                return None, INF
            R, ii = chosen
            cur = R
            used.append(ii)
            count += 1
            # if cur not increased, break
            if cur == a and count > 0:
                return None, INF
        return used, count
    
    # Case T empty
    used0, cnt0 = cover(1, N, set())
    best_cost = INF
    best_T = set()
    best_S = set()
    
    if cnt0 != INF:
        best_cost = cnt0
        best_T = set()
        best_S = set(used0)
    
    # Check for two disjoint intervals (cost 2)
    # Sort intervals by L and check if any interval ends before next starts
    has_disjoint = False
    for i in range(M - 1):
        if intervals[i][1] < intervals[i+1][0]:
            has_disjoint = True
            break
    if has_disjoint:
        if 2 < best_cost:
            best_cost = 2
            # We will reconstruct later; for now we just note that cost 2 is achievable
            # But we need to know which intervals to use as type2.
            # We'll find any two disjoint intervals.
            for i in range(M - 1):
                if intervals[i][1] < intervals[i+1][0]:
                    best_T = {intervals[i][2], intervals[i+1][2]}
                    best_S = set()
                    break
    
    # Case T size 1
    for i in range(M):
        L_i, R_i, idx = intervals[i][0], intervals[i][1], intervals[i][2]
        used, cnt = cover(L_i, R_i, {idx})
        if cnt != INF:
            total = 1 + cnt
            if total < best_cost:
                best_cost = total
                best_T = {idx}
                best_S = set(used)
    
    # Find i_maxL and j_minR
    # i_maxL: index of interval with maximum L
    # j_minR: index of interval with minimum R
    i_maxL = 0
    maxL = intervals[0][0]
    for k in range(1, M):
        if intervals[k][0] > maxL:
            maxL = intervals[k][0]
            i_maxL = k
    j_minR = 0
    minR = intervals[0][1]
    for k in range(1, M):
        if intervals[k][1] < minR:
            minR = intervals[k][1]
            j_minR = k
    
    if i_maxL != j_minR:
        a = max(intervals[i_maxL][0], intervals[j_minR][0])
        b = min(intervals[i_maxL][1], intervals[j_minR][1])
        if a <= b:
            # overlapping, need to cover [a,b]
            used, cnt = cover(a, b, {intervals[i_maxL][2], intervals[j_minR][2]})
            if cnt != INF:
                total = 2 + cnt
                if total < best_cost:
                    best_cost = total
                    best_T = {intervals[i_maxL][2], intervals[j_minR][2]}
                    best_S = set(used)
        else:
            # disjoint, intersection empty, cost 2
            if 2 < best_cost:
                best_cost = 2
                best_T = {intervals[i_maxL][2], intervals[j_minR][2]}
                best_S = set()
    
    if best_cost == INF:
        print(-1)
        return
    
    # Reconstruct operations
    op = [0] * M
    for idx in best_T:
        op[idx] = 2
    for idx in best_S:
        op[idx] = 1
    print(best_cost)
    print(' '.join(map(str, op)))

if __name__ == "__main__":
    solve()