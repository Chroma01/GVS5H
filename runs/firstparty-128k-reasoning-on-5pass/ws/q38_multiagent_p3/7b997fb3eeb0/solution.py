import sys
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    p = 0
    N = data[p]
    p += 1
    A = data[p:p + N]
    p += N
    Q = data[p]
    p += 1
    queries = data[p:]
    del data

    nxt = [0] * N
    gap = [0] * N
    j = 0
    for i in range(N):
        if j <= i:
            j = i + 1
        lim = A[i] * 2
        while j < N and A[j] < lim:
            j += 1
        nxt[i] = j
        gap[i] = j - i

    size = 1 << (N - 1).bit_length()
    seg = [0] * (2 * size)
    seg[size:size + N] = gap
    for i in range(size - 1, 0, -1):
        left = seg[i << 1]
        right = seg[(i << 1) | 1]
        seg[i] = left if left >= right else right

    del A, gap

    out = [''] * Q
    br = bisect_right
    p = 0
    for qi in range(Q):
        l = queries[p] - 1
        r = queries[p + 1] - 1
        p += 2
        C = r - l + 1
        s = br(nxt, r + 1)
        M = 0
        if s - 1 >= l:
            rr = s - 1
            if rr > r:
                rr = r
            left = l + size
            right = rr + size
            res = 0
            while left <= right:
                if left & 1:
                    v = seg[left]
                    if v > res:
                        res = v
                    left += 1
                if not (right & 1):
                    v = seg[right]
                    if v > res:
                        res = v
                    right -= 1
                left >>= 1
                right >>= 1
            M = res
        if s <= r:
            v = r + 1 - (l if l >= s else s)
            if v > M:
                M = v
        ans = C - M
        half = C >> 1
        if ans > half:
            ans = half
        out[qi] = str(ans)

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()