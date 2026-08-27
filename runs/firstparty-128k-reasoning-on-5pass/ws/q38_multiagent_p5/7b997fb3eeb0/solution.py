import sys

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

    g = [0] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        target = A[i] << 1
        while j < N and A[j] < target:
            j += 1
        if j < N:
            g[i] = j - i
        else:
            g[i] = N - i

    size = 1
    while size < N:
        size <<= 1

    seg = [0] * (size << 1)
    seg_len = [0] * (size << 1)
    base = size

    for i, val in enumerate(g):
        seg[base + i] = val
        seg_len[base + i] = 1

    for i in range(base - 1, 0, -1):
        left = i << 1
        right = left | 1
        lv = seg[left]
        rv = seg[right]
        seg[i] = lv if lv >= rv else rv
        seg_len[i] = seg_len[left] + seg_len[right]

    def max_right(l, M, seg=seg, seg_len=seg_len, size=size, N=N):
        if l == N:
            return N

        l += size
        sm_mx = 0
        sm_len = 0

        while True:
            while (l & 1) == 0:
                l >>= 1

            mx = seg[l]
            ln = seg_len[l]
            cmx = sm_mx if sm_mx >= mx else mx

            if cmx + sm_len + ln <= M:
                if mx > sm_mx:
                    sm_mx = mx
                sm_len += ln
                l += 1
            else:
                while l < size:
                    l <<= 1
                    mx = seg[l]
                    ln = seg_len[l]
                    cmx = sm_mx if sm_mx >= mx else mx
                    if cmx + sm_len + ln <= M:
                        if mx > sm_mx:
                            sm_mx = mx
                        sm_len += ln
                        l += 1

                res = l - size
                if res > N:
                    res = N
                return res

            if (l & -l) == l:
                break

        return N

    del A, g

    out = [None] * Q
    mr = max_right

    for qi in range(Q):
        l = data[p] - 1
        r = data[p + 1] - 1
        p += 2

        M = r - l + 1
        k = mr(l, M) - l
        half = M >> 1
        if k > half:
            k = half

        out[qi] = str(k)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()