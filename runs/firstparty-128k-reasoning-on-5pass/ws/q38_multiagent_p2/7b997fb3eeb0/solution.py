import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    ptr = 0
    N = data[ptr]
    ptr += 1
    A = data[ptr:ptr + N]
    ptr += N
    Q = data[ptr]
    ptr += 1

    p = [0] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        target = A[i] * 2
        while j < N and A[j] < target:
            j += 1
        p[i] = j

    w = [i - p[i] for i in range(N)]

    size = 1
    while size < N:
        size <<= 1
    INF = 10 ** 18
    seg = [INF] * (2 * size)
    seg[size:size + N] = w
    for i in range(size - 1, 0, -1):
        a = seg[i << 1]
        b = seg[(i << 1) | 1]
        seg[i] = a if a < b else b

    y_arr = [-1] * N
    idx = 0
    for r in range(N):
        while idx < N and p[idx] <= r:
            idx += 1
        y_arr[r] = idx - 1

    del A, p, w

    out = []
    append = out.append
    seg_local = seg
    size_local = size
    INF_local = INF
    y_local = y_arr

    for _ in range(Q):
        L = data[ptr]
        R = data[ptr + 1]
        ptr += 2
        l = L - 1
        r = R - 1
        M = r - l + 1
        ans = M >> 1
        Smax = l + ans - 1
        y = y_local[r]
        m = Smax if Smax < y else y

        if m >= l:
            left = l + size_local
            right = m + 1 + size_local
            res = INF_local
            while left < right:
                if left & 1:
                    v = seg_local[left]
                    if v < res:
                        res = v
                    left += 1
                if right & 1:
                    right -= 1
                    v = seg_local[right]
                    if v < res:
                        res = v
                left >>= 1
                right >>= 1
            cand = M + res
            if cand < ans:
                ans = cand

        cand = y + 1 - l
        if cand < ans:
            ans = cand
        if ans < 0:
            ans = 0
        append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()