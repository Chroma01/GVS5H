import sys
from bisect import bisect_right


def main():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        N = next(it)
    except StopIteration:
        return

    A = [next(it) for _ in range(N)]
    Q = next(it)

    # f[i] = first index j with A[j] >= 2*A[i], or N if it does not exist.
    # f is nondecreasing.
    f = [N] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        need = A[i] * 2
        while j < N and A[j] < need:
            j += 1
        f[i] = j

    del A

    # Iterative segment tree for range maximum of h[i] = f[i] - i.
    size = 1
    while size < N:
        size <<= 1

    seg = [0] * (size << 1)
    base = size
    for i in range(N):
        seg[base + i] = f[i] - i

    for i in range(base - 1, 0, -1):
        left = seg[i << 1]
        right = seg[(i << 1) | 1]
        seg[i] = left if left >= right else right

    out = []
    append = out.append
    br = bisect_right
    seg_local = seg
    size_local = size
    f_local = f

    for _ in range(Q):
        L = next(it) - 1
        R = next(it) - 1
        M = R - L + 1
        end = R + 1

        # First index in [L, R] with f[index] > end, or end if none.
        jj = br(f_local, end, L, end)

        p_extra = 0

        # Range maximum over h[L .. jj-1], i.e. half-open [L, jj).
        if jj > L:
            l = L + size_local
            r = jj + size_local
            res = 0
            while l < r:
                if l & 1:
                    v = seg_local[l]
                    if v > res:
                        res = v
                    l += 1
                if r & 1:
                    r -= 1
                    v = seg_local[r]
                    if v > res:
                        res = v
                l >>= 1
                r >>= 1
            p_extra = res

        # If jj <= R, indices jj..R cannot be used as tops unless p >= end - jj.
        v = end - jj
        if v > p_extra:
            p_extra = v

        p = (M + 1) >> 1
        if p_extra > p:
            p = p_extra

        append(str(M - p))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()