import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); M = int(data[ptr + 1]); Q = int(data[ptr + 2]); ptr += 3
    a = [0] * (M + 1); b = [0] * (M + 1); sg = [0] * (M + 1)
    for i in range(1, M + 1):
        S = int(data[ptr]); Tv = int(data[ptr + 1]); ptr += 2
        if S < Tv:
            a[i] = S; b[i] = Tv; sg[i] = 1
        else:
            a[i] = Tv; b[i] = S; sg[i] = -1

    prev = [0] * (M + 1)
    # same left endpoint
    last = [0] * (N + 1)
    for j in range(1, M + 1):
        x = a[j]
        if last[x] > prev[j]:
            prev[j] = last[x]
        last[x] = j
    # same right endpoint
    last = [0] * (N + 1)
    for j in range(1, M + 1):
        y = b[j]
        if last[y] > prev[j]:
            prev[j] = last[y]
        last[y] = j

    size = 1
    while size < N + 1:
        size <<= 1
    TT = [0] * (2 * size)
    VV = [0] * (2 * size)
    ver_box = [0]

    def sweepA(L, R, ca, cb):
        ver = ver_box[0] + 1; ver_box[0] = ver
        tt = TT; vv = VV; pv = prev; sz = size
        p_ = 0; nL = len(L)
        for j in R:
            aj = ca[j]
            while p_ < nL:
                i = L[p_]
                if ca[i] >= aj:
                    break
                q = cb[i] + sz
                if vv[q] != ver:
                    vv[q] = ver; tt[q] = 0
                if tt[q] < i:
                    tt[q] = i
                    q >>= 1
                    while q:
                        lc = q << 1; rc = lc | 1
                        vl = tt[lc] if vv[lc] == ver else 0
                        vr = tt[rc] if vv[rc] == ver else 0
                        nv = vl if vl > vr else vr
                        if vv[q] != ver:
                            vv[q] = ver; tt[q] = 0
                        if tt[q] >= nv:
                            break
                        tt[q] = nv
                        q >>= 1
                p_ += 1
            l = aj + 1 + sz
            r = cb[j] - 1 + sz + 1
            res = 0
            while l < r:
                if l & 1:
                    if vv[l] == ver and tt[l] > res:
                        res = tt[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if vv[r] == ver and tt[r] > res:
                        res = tt[r]
                l >>= 1; r >>= 1
            if res > pv[j]:
                pv[j] = res

    def merge_run(X, Y, ca):
        if not X: return Y
        if not Y: return X
        res = []; ap = res.append
        i = 0; j = 0; nx = len(X); ny = len(Y)
        while i < nx and j < ny:
            if ca[X[i]] <= ca[Y[j]]:
                ap(X[i]); i += 1
            else:
                ap(Y[j]); j += 1
        if i < nx: res.extend(X[i:])
        if j < ny: res.extend(Y[j:])
        return res

    def run(ca, cb):
        nodes = []
        for i in range(1, M + 1):
            if sg[i] == 1:
                nodes.append(([i], []))
            else:
                nodes.append(([], [i]))
        while len(nodes) > 1:
            nn = []
            i = 0; n = len(nodes)
            while i + 1 < n:
                LP, LM = nodes[i]
                RP, RM = nodes[i + 1]
                if LP and RP:
                    sweepA(LP, RP, ca, cb)
                if LM and RM:
                    sweepA(LM, RM, ca, cb)
                nn.append((merge_run(LP, RP, ca), merge_run(LM, RM, ca)))
                i += 2
            if i < n:
                nn.append(nodes[i])
            nodes = nn

    # pattern A: a_i < a_j < b_i < b_j
    run(a, b)
    # pattern B via mirror: a'=N+1-b, b'=N+1-a
    ma = [0] * (M + 1); mb = [0] * (M + 1)
    for i in range(1, M + 1):
        ma[i] = N + 1 - b[i]
        mb[i] = N + 1 - a[i]
    run(ma, mb)

    pref = [0] * (M + 1)
    cur = 0
    for j in range(1, M + 1):
        pj = prev[j]
        if pj > cur:
            cur = pj
        pref[j] = cur

    out = []
    for _ in range(Q):
        L = int(data[ptr]); R = int(data[ptr + 1]); ptr += 2
        out.append("No" if pref[R] >= L else "Yes")
    sys.stdout.write("\n".join(out))

main()