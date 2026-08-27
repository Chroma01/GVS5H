import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # ---- forward pass: pre[i] = distinct(A_1..A_i), prev_occ[j] = last index < j with same value (0 if none)
    pre = [0] * (n + 2)
    prev_occ = [0] * (n + 2)
    last = [0] * (n + 2)
    c = 0
    for j in range(1, n + 1):
        a = A[j - 1]
        lo = last[a]
        prev_occ[j] = lo
        if lo == 0:
            c += 1
        last[a] = j
        pre[j] = c

    # ---- backward pass: suf[k] = distinct(A_k..A_N)
    suf = [0] * (n + 3)
    seen = bytearray(n + 2)
    c = 0
    for k in range(n, 0, -1):
        a = A[k - 1]
        if not seen[a]:
            seen[a] = 1
            c += 1
        suf[k] = c
    # suf[n+1] = 0 already

    # ---- record stack over active positions 1..j-1
    # records = strict suffix maxima of f_j(i) = pre[i] + distinct(A_{i+1..j})
    # values strictly decrease left->right; d[q] = f[q] - f[nxt[q]] (>=1); L = f[head]
    d = [0] * (n + 2)
    nxt = [0] * (n + 2)
    prv = [0] * (n + 2)
    par = list(range(n + 2))   # DSU: largest alive record position <= x

    head = 1
    tail = 1
    nxt[1] = 0
    prv[1] = 0
    L = pre[1]                 # f[1] = pre[1] (before the +1 applied at step j=2)
    ans = 0

    for j in range(2, n):
        if j >= 3:
            # append position j-1 with value pre[j-1]; current tail is j-2 with value pre[j-2]+1
            tv = pre[j - 2] + 1
            v = pre[j - 1]
            t = tail
            nj = j - 1
            if v >= tv:
                # tail loses strictness -> delete it; d[prv[t]] stays numerically the same
                q = prv[t]
                par[t] = t - 1
                if q:
                    nxt[q] = nj
                    prv[nj] = q
                else:
                    head = nj
                    prv[nj] = 0
                    # L unchanged (new head has same value)
                tail = nj
            else:
                d[t] = tv - v
                nxt[t] = nj
                prv[nj] = t
                tail = nj
            nxt[nj] = 0

        # suffix add +1 on [p, j-1]
        p = prev_occ[j]
        if p < 1:
            p = 1
        if head >= p:
            L += 1
        else:
            x = p - 1
            while par[x] != x:
                x = par[x]
            r = x
            x = p - 1
            while par[x] != r:
                par[x], x = r, par[x]
            q = r
            dq = d[q] - 1
            d[q] = dq
            if dq == 0:
                nx = nxt[q]
                pq = prv[q]
                par[q] = q - 1
                if pq:
                    nxt[pq] = nx
                    prv[nx] = pq
                else:
                    head = nx
                    prv[nx] = 0

        t3 = L + suf[j + 1]
        if t3 > ans:
            ans = t3

    sys.stdout.write(str(ans))

main()