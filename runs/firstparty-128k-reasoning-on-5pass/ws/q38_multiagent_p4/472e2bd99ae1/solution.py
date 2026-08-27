import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    A = data[2:2 + N]
    B = data[2 + N:2 + 2 * N]
    C = data[2 + 2 * N:2 + 3 * N]
    del data

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    M = K if K < N else N
    if M < N:
        del A[M:]
        del B[M:]
        del C[M:]

    b = (M - 1).bit_length()
    if b == 0:
        b = 1
    two_b = b << 1
    shift = b * 3
    mask = (1 << b) - 1
    code_mask = (1 << shift) - 1

    A0 = A[0]
    B0 = B[0]
    C0 = C[0]
    A0B0 = A0 + B0
    LIMIT = A0 * B0 + C0 * A0B0

    if M > 1:
        Adrop = [A[i] - A[i + 1] for i in range(M - 1)]
        Bdrop = [B[i] - B[i + 1] for i in range(M - 1)]
        Cdrop = [C[i] - C[i + 1] for i in range(M - 1)]
    else:
        Adrop = Bdrop = Cdrop = []

    # key = ((LIMIT - value) << shift) + code
    heap = [0]
    hpop = heapq.heappop
    hpush = heapq.heappush

    for _ in range(K - 1):
        key = hpop(heap)
        d = key >> shift  # d = LIMIT - current value
        code = key & code_mask

        k = code & mask
        i = (code >> b) & mask
        j = code >> two_b

        ck = C[k]

        ni = i + 1
        if ni < M:
            high = d + Adrop[i] * (B[j] + ck)
            hpush(heap, (high << shift) + (j << two_b) + (ni << b) + k)

        if i == 0:
            nj = j + 1
            if nj < M:
                high = d + Bdrop[j] * (A0 + ck)
                hpush(heap, (high << shift) + (nj << two_b) + k)

            if j == 0:
                nk = k + 1
                if nk < M:
                    high = d + Cdrop[k] * A0B0
                    hpush(heap, (high << shift) + nk)

    key = hpop(heap)
    val = LIMIT - (key >> shift)
    sys.stdout.write(str(val) + "\n")


if __name__ == "__main__":
    solve()