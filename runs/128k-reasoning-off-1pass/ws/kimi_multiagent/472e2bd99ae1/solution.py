import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); K = int(data[1])
    A = [int(x) for x in data[2:2+n]]
    B = [int(x) for x in data[2+n:2+2*n]]
    C = [int(x) for x in data[2+2*n:2+3*n]]

    # Any top-K triple must have each index within the top-min(N,K) of its array
    # (value is strictly increasing in each of A_i, B_j, C_k when others fixed).
    M = n if n < K else K
    A.sort(reverse=True); A = A[:M]
    B.sort(reverse=True); B = B[:M]
    C.sort(reverse=True); C = C[:M]

    a = A; b = B; c = C
    m = M
    m2 = m * m

    # Best-first search over the monotone 3D grid (arrays sorted descending =>
    # value nonincreasing in each index). Tree-push rule: each cell (i,j,k) has
    # exactly one parent: (i-1,j,k) if i>0, else (0,j-1,k) if j>0, else (0,0,k-1).
    # Push children on pop => no visited set needed, descending enumeration.
    v0 = a[0]*b[0] + b[0]*c[0] + c[0]*a[0]
    heap = [(-v0, 0)]
    push = heapq.heappush
    pop = heapq.heappop
    ans = v0
    for _ in range(K):
        negv, code = pop(heap)
        ans = -negv
        i, rem = divmod(code, m2)
        j, k = divmod(rem, m)
        ai = a[i]; bj = b[j]; ck = c[k]
        # child 1: (i+1, j, k)
        if i + 1 < m:
            ai1 = a[i+1]
            v = ai1*bj + bj*ck + ck*ai1
            push(heap, (-v, code + m2))
        # child 2: (i, j+1, k), only when i == 0
        if i == 0 and j + 1 < m:
            bj1 = b[j+1]
            v = ai*bj1 + bj1*ck + ck*ai
            push(heap, (-v, code + m))
        # child 3: (i, j, k+1), only when i == 0 and j == 0
        if i == 0 and j == 0 and k + 1 < m:
            ck1 = c[k+1]
            v = ai*bj + bj*ck1 + ck1*ai
            push(heap, (-v, code + 1))
    sys.stdout.write(str(ans) + "\n")

main()