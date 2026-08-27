import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]
    
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    # We use a priority queue to generate the top K values in descending order.
    # Because the expression is strictly increasing in each of A_i, B_j, C_k (all positive),
    # sorting descending makes the 3D grid monotone. A best-first search from (0,0,0)
    # expanding by incrementing one index at a time yields the correct order.
    # To reduce heap size, we group by (i,j) pairs: each heap entry contains (i,j,k).
    # When (i,j,k) is popped, we push (i,j,k+1) if possible, plus (i+1,j,0) and (i,j+1,0) if not seen.
    # A visited set on (i,j) prevents duplicate pairs.
    
    MASK = (1 << 18) - 1  # N <= 2e5 < 2^18 = 262144
    def pack(i, j, k):
        return (i << 36) | (j << 18) | k
    def pack_ij(i, j):
        return (i << 18) | j
    
    v0 = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    heap = [(-v0, pack(0, 0, 0))]
    visited_ij = {pack_ij(0, 0)}
    k_map = {pack_ij(0, 0): 0}  # current k pointer for each active (i,j) pair
    
    count = 0
    a, b, c = A, B, C
    n = N
    push = heapq.heappush
    pop = heapq.heappop
    add_visited = visited_ij.add
    contains_visited = visited_ij.__contains__
    
    while count < K:
        neg_v, p = pop(heap)
        count += 1
        if count == K:
            print(-neg_v)
            return
        
        i = p >> 36
        j = (p >> 18) & MASK
        k = p & MASK
        ai, bj, ck = a[i], b[j], c[k]
        pk = pack_ij(i, j)
        
        # Advance k for the same (i,j) pair
        nk = k + 1
        if nk < n:
            k_map[pk] = nk
            val = ai * bj + bj * c[nk] + c[nk] * ai
            push(heap, (-val, pack(i, j, nk)))
        else:
            k_map.pop(pk, None)
        
        # Neighbor (i+1, j) with k=0
        ni = i + 1
        if ni < n:
            nij = pack_ij(ni, j)
            if not contains_visited(nij):
                add_visited(nij)
                val = a[ni] * bj + bj * c[0] + c[0] * a[ni]
                k_map[nij] = 0
                push(heap, (-val, pack(ni, j, 0)))
        
        # Neighbor (i, j+1) with k=0
        nj = j + 1
        if nj < n:
            nij = pack_ij(i, nj)
            if not contains_visited(nij):
                add_visited(nij)
                val = ai * b[nj] + b[nj] * c[0] + c[0] * ai
                k_map[nij] = 0
                push(heap, (-val, pack(i, nj, 0)))

if __name__ == "__main__":
    solve()