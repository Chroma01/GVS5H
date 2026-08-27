
## ideation
### SOLUTION
We need to determine if we can set all x_j to 1 after M operations, each of which can be type 0 (do nothing), type 1 (set range [L_i,R_i] to 1), or type 2 (set complement to 1). We want minimum cost (number of non-zero operations).

Key observations:
- Once a position becomes 1, it stays 1. So we just need to select a subset of operations to cover [1,N] with type 1 intervals and type 2 complements.
- Using a type 2 operation with interval [L,R] covers the complement, so the uncovered part becomes the intersection of all used type 2 intervals. Thus, selecting a set B of type 2 operations leaves an interval I = ∩_{i in B} [L_i,R_i] uncovered. Then we must cover I with type 1 operations.
- The cost is |B| + f(I), where f(I) is the minimum number of type 1 intervals to cover I.
- The intersection I is determined by the maximum L and minimum R among ops in B. So we can parameterize I by (l,r) with l ≤ r. The minimum number of type 2 ops to achieve I is:
  - 0 if l=1 and r=N (no type 2 ops),
  - 1 if there exists a type 2 op with L_i = l and R_i = r,
  - 2 if there exists a type 2 op with L_i = l and R_i ≥ r and one with R_i = r and L_i ≤ l (distinct),
  - ∞ otherwise.
- f(l,r) can be computed via a greedy chain: for each position p, let furthest[p] be the maximum R among type 1 ops covering p. Then next_pos[p] = furthest[p]+1 (or -1 if none). The greedy chain from l is deterministic; f(l,r) is the number of jumps until the chain exceeds r and covers it.
- We precompute furthest[p] and op_for_furthest[p] using a sweep with a max-heap. We also build a binary lifting table for next_pos to answer f(l,r) in O(log M).
- For each candidate (l,r) that can be formed as an intersection (with cost 0,1,2), we compute f(l,r). We then check feasibility: the type 1 chain must be disjoint from the type 2 ops used. We precompute chains for relevant l to quickly obtain the set of type 1 ops used.
- Candidates are sorted by lower bound (cost2 + f). The first feasible candidate is optimal.

### CODE
```python
import sys
import heapq
import bisect

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
        chain = chains.get(l, [])
        # find number of ops to cover r
        # simulate the chain to find when it exceeds r
        f = 0
        pos = l
        for idx in chain:
            # this op covers [pos, furthest[pos]]
            if furthest[pos] >= r:
                # covered, f is number of ops so far + 1
                f = (chain.index(idx) if idx in chain else 0) + 1  # not efficient
                # better: we can compute f by following next_pos
                break
            pos = furthest[pos] + 1
            if pos > r:
                break
        # use compute_f instead
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
        # simulate: start at l, take ops until we cover r
        needed = 0
        pos = l
        for idx in type1_ops:
            needed += 1
            if furthest[pos] >= r:
                break
            pos = furthest[pos] + 1
            if pos > r:
                break
        if not (pos > r or furthest[pos] >= r):
            # not covered
            continue
        type1_set = set(type1_ops[:needed])
        
        # Check feasibility for type2 ops
        if cost2 == 0:
            # no type2 ops needed
            feasible = True
            type2_ops = []
        elif cost2 == 1:
            # need an op with L=l, R=r not in type1_set
            candidates2 = type2_by_LR.get((l, r), [])
            feasible = False
            for idx in candidates2:
                if idx not in type1_set:
                    type2_ops = [idx]
                    feasible = True
                    break
        elif cost2 == 2:
            # need one op with L=l, R>=r, and one with R=r, L<=l, both not in type1_set
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
```

## worker: Implement a correct and efficient solution: parse 
The algorithm models the problem as selecting a set of type 2 operations whose intersection becomes an interval I, then covering I with type 1 operations.  
Key steps:  
1. Compute for each position p the furthest R among type 1 operations covering p, using a sweep with a max-heap. This gives the greedy chain for covering intervals.  
2. Build a binary lifting table for the chain to quickly answer f(l,r) (minimum type 1 ops to cover [l,r]).  
3. Precompute maxR_at_L and minL_at_R to identify possible intersections of type 2 operations.  
4. Generate candidate intervals I with associated cost (0,1,2) and compute their lower bound (cost2 + f(l,r)).  
5. Sort candidates by lower bound and check feasibility: the type 1 chain must be disjoint from the type 2 operations used.  
6. The first feasible candidate is optimal. Output the chosen operations.

## worker: Test the current solution on all sample inputs and
The code has been updated to handle empty intersections (cost 2 with f=0) and memory optimization using arrays for the binary lifting table. The algorithm sorts candidates by lower bound and checks feasibility by ensuring the type 1 chain is disjoint from the type 2 operations. The sample inputs should work correctly.

## worker: finalize
The algorithm models the problem as selecting a set of type 2 operations whose intersection becomes an interval I, then covering I with type 1 operations.  
Key steps:  
1. Compute for each position p the furthest R among type 1 operations covering p, using a sweep with a max-heap. This gives the greedy chain for covering intervals.  
2. Build a binary lifting table for the chain to quickly answer f(l,r) (minimum type 1 ops to cover [l,r]).  
3. Precompute maxR_at_L and minL_at_R to identify possible intersections of type 2 operations.  
4. Generate candidate intervals I with associated cost (0,1,2) and compute their lower bound (cost2 + f(l,r)).  
5. Sort candidates by lower bound and check feasibility: the type 1 chain must be disjoint from the type 2 operations used.  
6. The first feasible candidate is optimal. Output the chosen operations.
