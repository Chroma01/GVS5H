import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2+N]))
    B = list(map(int, data[2+N:2+2*N]))
    C = list(map(int, data[2+2*N:2+3*N]))
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    if N == 1:
        ans = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
        sys.stdout.write(str(ans))
        return

    push = heapq.heappush
    pop = heapq.heappop
    heap = []

    a0, b0, c0 = A[0], B[0], C[0]
    v0 = a0*b0 + b0*c0 + c0*a0
    push(heap, (-v0, 0))

    SHIFT = 20
    MASK = (1 << SHIFT) - 1
    ADD_J = 1 << SHIFT
    ADD_I = 1 << 40

    for _ in range(K - 1):
        neg_v, packed = pop(heap)
        i = packed >> 40
        j = (packed >> SHIFT) & MASK
        k = packed & MASK
        ai = A[i]
        bj = B[j]

        nk = k + 1
        if nk < N:
            ck = C[nk]
            nv = ai*bj + bj*ck + ck*ai
            push(heap, (-nv, packed + 1))

        if k == 0:
            nj = j + 1
            if nj < N:
                bj2 = B[nj]
                ck = C[0]
                nv = ai*bj2 + bj2*ck + ck*ai
                push(heap, (-nv, packed + ADD_J))
            if j == 0:
                ni = i + 1
                if ni < N:
                    ai2 = A[ni]
                    bj0 = B[0]
                    ck0 = C[0]
                    nv = ai2*bj0 + bj0*ck0 + ck0*ai2
                    push(heap, (-nv, packed + ADD_I))

    neg_v, _ = pop(heap)
    ans = -neg_v
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()