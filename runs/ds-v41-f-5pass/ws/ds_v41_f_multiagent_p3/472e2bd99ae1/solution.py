import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = sorted(map(int, data[2:2 + n]), reverse=True)
    B = sorted(map(int, data[2 + n:2 + 2 * n]), reverse=True)
    C = sorted(map(int, data[2 + 2 * n:2 + 3 * n]), reverse=True)

    # differences (<= 0 because arrays are sorted descending)
    da = [A[i + 1] - A[i] for i in range(n - 1)]
    db = [B[i + 1] - B[i] for i in range(n - 1)]
    dc = [C[i + 1] - C[i] for i in range(n - 1)]

    push = heapq.heappush
    pop = heapq.heappop
    heap = []

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]

    v0 = a0 * b0 + b0 * c0 + c0 * a0
    push(heap, (-v0, 0))          # negated value, packed index (i,j,k)

    SH = 18
    MASK = (1 << SH) - 1
    D1 = 1
    D2 = 1 << SH
    D3 = 1 << (2 * SH)

    ans = 0
    for _ in range(K):
        nv, p = pop(heap)
        v = -nv
        ans = v

        k = p & MASK
        t = p >> SH
        j = t & MASK
        i = t >> SH

        if i == 0:
            ck = C[k]
            bj = B[j]
            if j == 0:
                if i + 1 < n:
                    push(heap, (-(v + da[0] * (b0 + ck)), p + D3))
                if j + 1 < n:
                    push(heap, (-(v + db[0] * (a0 + ck)), p + D2))
                if k + 1 < n:
                    # FIX: difference uses dc[k], valid for all k (node here is (0,0,k))
                    push(heap, (-(v + dc[k] * (a0 + b0)), p + D1))
            else:
                if i + 1 < n:
                    push(heap, (-(v + da[0] * (bj + ck)), p + D3))
                if j + 1 < n:
                    push(heap, (-(v + db[j] * (a0 + ck)), p + D2))
        else:
            if i + 1 < n:
                push(heap, (-(v + da[i] * (B[j] + C[k])), p + D3))

    sys.stdout.write(str(ans))


main()