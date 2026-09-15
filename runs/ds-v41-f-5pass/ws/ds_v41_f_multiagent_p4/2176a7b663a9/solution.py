import sys

INF = 10**18

def build_seg(arr):
    n = len(arr)
    size = 1
    while size < n:
        size <<= 1
    tree = [INF] * (2 * size)
    for i in range(n):
        tree[size + i] = arr[i]
    for i in range(size - 1, 0, -1):
        left = tree[2 * i]
        right = tree[2 * i + 1]
        tree[i] = left if left < right else right
    return tree, size

def query_seg(tree, size, l, r):
    if l > r:
        return INF
    l += size
    r += size
    res = INF
    while l <= r:
        if l & 1:
            if tree[l] < res:
                res = tree[l]
            l += 1
        if not (r & 1):
            if tree[r] < res:
                res = tree[r]
            r -= 1
        l >>= 1
        r >>= 1
    return res

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    W = [next(it) for _ in range(N)]
    L = [0] * N
    R = [0] * N
    maxv = 2 * N + 2
    minL = [INF] * (maxv + 2)
    minR = [INF] * (maxv + 2)
    for i in range(N):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        w = W[i]
        if w < minL[l]:
            minL[l] = w
        if w < minR[r]:
            minR[r] = w

    Q = next(it)
    queries = []
    for _ in range(Q):
        s = next(it) - 1
        t = next(it) - 1
        queries.append((s, t))

    # prefR[x] = min W_i with R_i < x
    prefR = [INF] * (maxv + 2)
    for x in range(1, maxv + 2):
        v = prefR[x - 1]
        u = minR[x - 1]
        prefR[x] = v if v < u else u

    # suffL[x] = min W_i with L_i > x
    suffL = [INF] * (maxv + 2)
    for x in range(maxv, -1, -1):
        v = suffL[x + 1]
        u = minL[x + 1]
        suffL[x] = v if v < u else u

    treeL, sizeL = build_seg(minL)
    treeR, sizeR = build_seg(minR)

    out = []
    for s, t in queries:
        Ws = W[s]
        Wt = W[t]
        Ls = L[s]
        Rs = R[s]
        Lt = L[t]
        Rt = R[t]

        if Rs < Lt or Rt < Ls:
            ans = Ws + Wt
        else:
            X = Ls if Ls < Lt else Lt
            Y = Rs if Rs > Rt else Rt
            bl = prefR[X]
            br = suffL[Y]
            best2 = bl if bl < br else br
            len2 = Ws + Wt + best2 if best2 < INF else INF

            len3 = INF
            if Ls < Lt and Rs < Rt:
                minA = query_seg(treeL, sizeL, Rs + 1, Rt)
                minB = query_seg(treeR, sizeR, Ls, Lt - 1)
                if minA < INF and minB < INF:
                    len3 = Ws + Wt + minA + minB
            elif Lt < Ls and Rt < Rs:
                minA = query_seg(treeL, sizeL, Rt + 1, Rs)
                minB = query_seg(treeR, sizeR, Lt, Ls - 1)
                if minA < INF and minB < INF:
                    len3 = Ws + Wt + minA + minB

            ans = len2 if len2 < len3 else len3
            if ans >= INF:
                ans = -1
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()