import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    ops = []
    for i in range(M):
        L, R = map(int, input().split())
        ops.append((L, R, i))
    
    INF = 10**9
    
    # Build furthest and op_for_furthest for type 1 using sweep with max-heap
    sorted_ops = sorted(ops, key=lambda x: x[0])  # sort by L
    furthest = [-1] * (N + 2)
    op_for_furthest = [-1] * (N + 2)
    heap = []  # max-heap with negative R
    ptr = 0
    for p in range(1, N + 1):
        while ptr < M and sorted_ops[ptr][0] == p:
            L, R, idx = sorted_ops[ptr]
            heapq.heappush(heap, (-R, idx))
            ptr += 1
        while heap and -heap[0][0] < p:
            heapq.heappop(heap)
        if heap:
            furthest[p] = -heap[0][0]
            op_for_furthest[p] = heap[0][1]
        else:
            furthest[p] = -1
            op_for_furthest[p] = -1
    
    # Build next_pos
    next_pos = [-1] * (N + 2)
    for p in range(1, N + 1):
        if furthest[p] != -1:
            next_pos[p] = furthest[p] + 1
    next_pos[N + 1] = -1
    
    # Build binary lifting table for next_pos
    max_log = (M).bit_length() + 1
    nxt = []
    nxt.append(next_pos[:])  # nxt[0]
    for k in range(1, max_log + 1):
        prev = nxt[k-1]
        cur = [-1] * (N + 2)
        for p in range(1, N + 2):
            if prev[p] != -1:
                cur[p] = prev[prev[p]]
        nxt.append(cur)
    
    def compute_f(l, r):
        if l > r:
            return INF
        pos = l
        steps = 0
        for i in range(max_log, -1, -1):
            if nxt[i][pos] != -1 and nxt[i][pos] <= r:
                pos = nxt[i][pos]
                steps += (1 << i)
        if next_pos[pos] != -1 and next_pos[pos] > r:
            return steps + 1
        else:
            return INF
    
    # Precompute for type 2: maxR_at_L and minL_at_R
    maxR_at_L = [-1] * (N + 1)  # index 0 unused
    minL_at_R = [N + 1] * (N + 1)
    for L, R, idx in ops:
        if maxR_at_L[L] < R:
            maxR_at_L[L] = R
        if minL_at_R[R] > L:
            minL_at_R[R] = L
    
    # Build segment tree for minL_at_R to find first R in [L, U] with minL_at_R[R] <= L
    size = 1
    while size < N + 1:
        size <<= 1
    tree = [N + 1] * (2 * size)
    for i in range(1, N + 1):
        tree[size + i] = minL_at_R[i]
    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2*i], tree[2*i+1])
    
    sys.setrecursionlimit(1 << 25)
    def find_first(node, node_l, node_r, ql, qr, L):
        if node_r < ql or node_l > qr or tree[node] > L:
            return -1
        if node_l == node_r:
            if node_l <= N:
                return node_l
            else:
                return -1
        mid = (node_l + node_r) // 2
        res = find_first(2*node, node_l, mid, ql, qr, L)
        if res != -1:
            return res
        return find_first(2*node+1, mid+1, node_r, ql, qr, L)
    
    # Collect candidate l values
    candidate_l_set = set()
    candidate_l_set.add(1)  # for cost0 candidate
    L_set = set()
    for L in range(1, N+1):
        if maxR_at_L[L] != -1:
            L_set.add(L)
            candidate_l_set.add(L)
    
    # Generate candidates
    candidates = []  # each: (l, r, cost2)
    
    # Cost0 candidate: (1, N)
    candidates.append((1, N, 0))
    
    # Cost1 candidates from each op
    for L, R, idx in ops:
        candidates.append((L, R, 1))
        candidate_l_set.add(L)
    
    # Cost2 candidates: for each L in L_set
    for L in L_set:
        U = maxR_at_L[L]
        if U < L:
            continue
        R2 = find_first(1, 1, size, L, U, L)
        if R2 != -1:
            candidates.append((L, R2, 2))
            candidate_l_set.add(L)
    
    # Precompute chains for each l in candidate_l_set
    chains = {}  # l -> list of op indices in order
    for l in candidate_l_set:
        chain_ops = []
        pos = l
        while pos <= N and furthest[pos] != -1:
            idx = op_for_furthest[pos]
            chain_ops.append(idx)
            pos = furthest[pos] + 1
        chains[l] = chain_ops
    
    # For each candidate, compute f and lower bound
    cand_data = []  # (lower_bound, l, r, cost2)
    for l, r, cost2 in candidates:
        if l > r:
            continue
        f = compute_f(l, r)
        if f == INF:
            continue
        lower = cost2 + f
        cand_data.append((lower, l, r, cost2))
    
    # Sort by lower bound
    cand_data.sort()
    
    # Precompute for type 2 op selection
    type2_by_LR = {}
    type2_by_L = {}
    type2_by_R = {}
    for L, R, idx in ops:
        type2_by_LR.setdefault((L, R), []).append(idx)
        type2_by_L.setdefault(L, []).append((R, idx))
        type2_by_R.setdefault(R, []).append((L, idx))
    
    best_cost = INF
    best_info = None  # (l, r, cost2, type1_ops, type2_ops)
    
    for lower, l, r, cost2 in cand_data:
        # Get type1 ops from chain
        type1_ops = chains[l]
        # Find number of type1 ops needed to cover r
        needed = 0
        pos = l
        covered = False
        for idx in type1_ops:
            needed += 1
            if furthest[pos] >= r:
                covered = True
                break
            pos = furthest[pos] + 1
            if pos > r:
                covered = True
                break
        if not covered:
            continue
        type1_set = set(type1_ops[:needed])
        
        # Check feasibility for type2 ops
        if cost2 == 0:
            feasible = True
            type2_ops = []
        elif cost2 == 1:
            candidates2 = type2_by_LR.get((l, r), [])
            feasible = False
            for idx in candidates2:
                if idx not in type1_set:
                    type2_ops = [idx]
                    feasible = True
                    break
        elif cost2 == 2:
            ops1 = [idx for (R2, idx) in type2_by_L.get(l, []) if R2 >= r and idx not in type1_set]
            ops2 = [idx for (L2, idx) in type2_by_R.get(r, []) if L2 <= l and idx not in type1_set]
            feasible = False
            for i1 in ops1:
                for i2 in ops2:
                    if i1 != i2:
                        type2_ops = [i1, i2]
                        feasible = True
                        break
                if feasible:
                    break
        else:
            feasible = False
            type2_ops = []
        
        if feasible:
            best_cost = lower
            best_info = (l, r, cost2, type1_ops[:needed], type2_ops)
            break
    
    if best_info is None:
        print(-1)
        return
    
    l, r, cost2, type1_ops, type2_ops = best_info
    result = [0] * M
    for idx in type1_ops:
        result[idx] = 1
    for idx in type2_ops:
        result[idx] = 2
    print(best_cost)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()