import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = sorted(map(int, data[2:2 + n]), reverse=True)
    B = sorted(map(int, data[2 + n:2 + 2 * n]), reverse=True)
    C = sorted(map(int, data[2 + 2 * n:2 + 3 * n]), reverse=True)

    SHIFT = 53
    MASK = (1 << SHIFT) - 1
    nn = n * n

    v0 = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    heap = [((-v0) << SHIFT)]
    push = heappush
    pop = heappop

    ans = 0
    for _ in range(K):
        key = pop(heap)
        v = -(key >> SHIFT)
        code = key & MASK
        ij, k = divmod(code, n)
        i, j = divmod(ij, n)
        ans = v

        ni = i + 1
        if ni < n:
            bj = B[j]; ck = C[k]; ai = A[ni]
            nv = ai * bj + bj * ck + ck * ai
            push(heap, ((-nv) << SHIFT) | (ni * nn + j * n + k))
        if i == 0:
            nj = j + 1
            if nj < n:
                a0 = A[0]; bj = B[nj]; ck = C[k]
                nv = a0 * bj + bj * ck + ck * a0
                push(heap, ((-nv) << SHIFT) | (nj * n + k))
            if j == 0:
                nk = k + 1
                if nk < n:
                    a0 = A[0]; b0 = B[0]; ck = C[nk]
                    nv = a0 * b0 + b0 * ck + ck * a0
                    push(heap, ((-nv) << SHIFT) | nk)

    sys.stdout.write(str(ans))

main()