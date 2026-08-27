import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); K = int(data[1])
    A = list(map(int, data[2:2+n]))
    B = list(map(int, data[2+n:2+2*n]))
    C = list(map(int, data[2+2*n:2+3*n]))
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    m = min(n, K)
    if m < n:
        A = A[:m]; B = B[:m]; C = C[:m]

    push = heapq.heappush
    pop = heapq.heappop

    a0 = A[0]; b0 = B[0]; c0 = C[0]
    heap = [(-(a0*b0 + b0*c0 + c0*a0), 0)]
    mm = m * m

    nv = 0
    for _ in range(K):
        nv, idx = pop(heap)
        i, r = divmod(idx, mm)
        j, k = divmod(r, m)
        ai = A[i]; bj = B[j]; ck = C[k]
        i1 = i + 1
        if i1 < m:
            a2 = A[i1]
            push(heap, (-(a2*bj + bj*ck + ck*a2), idx + mm))
        if i == 0:
            j1 = j + 1
            if j1 < m:
                b2 = B[j1]
                push(heap, (-(ai*b2 + b2*ck + ck*ai), idx + m))
            if j == 0:
                k1 = k + 1
                if k1 < m:
                    c2 = C[k1]
                    push(heap, (-(ai*bj + bj*c2 + c2*ai), idx + 1))

    sys.stdout.write(str(-nv) + "\n")

main()