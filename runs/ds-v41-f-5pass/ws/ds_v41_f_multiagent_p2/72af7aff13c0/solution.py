import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    H = int(data[0]); W = int(data[1])
    HW = H * W
    Qn = int(data[2 + HW])
    sh = int(data[3 + HW]); sw = int(data[4 + HW])
    pos = 5 + HW
    
    # Count vertical moves to choose orientation minimizing vertical work
    cu = 0; cl = 0
    q = pos
    for _ in range(Qn):
        d = data[q]
        if d == b'U' or d == b'D':
            cu += 1
        else:
            cl += 1
        q += 2
    
    if cu * W <= cl * H:
        transposed = False
        L = H; K = W
        A = []
        for i in range(H):
            A.append([int(x) for x in data[2 + i*W : 2 + (i+1)*W]])
        r = sh - 1; c = sw - 1
    else:
        transposed = True
        L = W; K = H
        A = []
        for i in range(W):
            row = [int(data[2 + j*W + i]) for j in range(H)]
            A.append(row)
        r = sw - 1; c = sh - 1
    
    # Inclusive prefix DP per row
    e0 = [0]*K; e0[0] = 1
    pre0 = [None]*L
    prev = e0
    for i in range(L):
        rowA = A[i]
        cur = [0]*K
        s = 0
        for j in range(K):
            s += prev[j]
            if s >= MOD: s -= MOD
            v = rowA[j] * s % MOD
            cur[j] = v
            s = v
        pre0[i] = cur
        prev = cur
    
    # Inclusive suffix DP per row
    S0 = [None]*(L+1)
    bas = [0]*K; bas[K-1] = 1
    S0[L] = bas
    for i in range(L-1, -1, -1):
        rowA = A[i]
        nxt = S0[i+1]
        cur = [0]*K
        s = 0
        for j in range(K-1, -1, -1):
            s += nxt[j]
            if s >= MOD: s -= MOD
            v = rowA[j] * s % MOD
            cur[j] = v
            s = v
        S0[i] = cur
    
    ans = pre0[L-1][K-1]
    P = pre0[r-1] if r > 0 else e0
    Q = S0[r+1]
    rowA = A[r]
    
    # Exclusive prefix (pes) and suffix (vs) for the current row
    pref = [0]
    s = 0
    for j in range(c):
        s += P[j]
        if s >= MOD: s -= MOD
        v = rowA[j] * s % MOD
        pref.append(v)
        s = v
    
    suff_rev = []
    s = Q[K-1]
    suff_rev.append(s)
    for j in range(K-2, c-1, -1):
        s = (Q[j] + rowA[j+1] * s) % MOD
        suff_rev.append(s)
    
    pstack = []
    sstack = []
    out = []
    q = pos
    for _ in range(Qn):
        d = data[q]; a = int(data[q+1]); q += 2
        if transposed:
            if d == b'U': d = b'L'
            elif d == b'D': d = b'R'
            elif d == b'L': d = b'U'
            else: d = b'D'
        
        if d == b'R':
            rowA = A[r]
            v = pref[c] + P[c]
            if v >= MOD: v -= MOD
            pref.append(rowA[c] * v % MOD)
            suff_rev.pop()
            c += 1
        elif d == b'L':
            pref.pop()
            rowA = A[r]
            suff_rev.append((Q[c-1] + rowA[c] * suff_rev[-1]) % MOD)
            c -= 1
        elif d == b'D':
            pstack.append(P)
            rowA = A[r]
            newP = pref[1:]
            if len(newP) < K:
                newP.extend([0] * (K - c))
            s = pref[-1]
            for j in range(c, K):
                s += P[j]
                if s >= MOD: s -= MOD
                v = rowA[j] * s % MOD
                newP[j] = v
                s = v
            P = newP
            if sstack:
                Q = sstack.pop()
            else:
                Q = S0[r+2]
            r += 1
            rowA = A[r]
            pref = [0]
            s = 0
            for j in range(c):
                s += P[j]
                if s >= MOD: s -= MOD
                v = rowA[j] * s % MOD
                pref.append(v)
                s = v
            suff_rev = []
            s = Q[K-1]
            suff_rev.append(s)
            for j in range(K-2, c-1, -1):
                s = (Q[j] + rowA[j+1] * s) % MOD
                suff_rev.append(s)
        else:  # U
            rowA = A[r]
            newQ = [0]*K
            s = 0
            for j in range(K-1, -1, -1):
                s += Q[j]
                if s >= MOD: s -= MOD
                v = rowA[j] * s % MOD
                newQ[j] = v
                s = v
            sstack.append(Q)
            Q = newQ
            if pstack:
                P = pstack.pop()
            elif r >= 2:
                P = pre0[r-2]
            else:
                P = e0
            r -= 1
            rowA = A[r]
            pref = [0]
            s = 0
            for j in range(c):
                s += P[j]
                if s >= MOD: s -= MOD
                v = rowA[j] * s % MOD
                pref.append(v)
                s = v
            suff_rev = []
            s = Q[K-1]
            suff_rev.append(s)
            for j in range(K-2, c-1, -1):
                s = (Q[j] + rowA[j+1] * s) % MOD
                suff_rev.append(s)
        
        rowA = A[r]
        old = rowA[c]
        if a != old:
            delta = a - old
            if delta < 0:
                delta += MOD
            pe = pref[c] + P[c]
            if pe >= MOD: pe -= MOD
            ve = suff_rev[-1]
            ans = (ans + delta * pe % MOD * ve) % MOD
            rowA[c] = a
        out.append(ans)
    
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

if __name__ == '__main__':
    solve()