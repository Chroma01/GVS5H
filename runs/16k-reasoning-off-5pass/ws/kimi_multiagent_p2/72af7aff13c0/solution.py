import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos+1]); pos += 2
    total = H * W
    A = [int(x) % MOD for x in data[pos:pos+total]]; pos += total
    Q = int(data[pos]); sh = int(data[pos+1]); sw = int(data[pos+2]); pos += 3
    queries = [(data[pos+2*i].decode(), int(data[pos+2*i+1]) % MOD) for i in range(Q)]

    # Orient so that the DP dimension (rows) is the small one.
    if H <= W:
        n = W; s = H
        col = [A[r*W + (j-1)] for j in range(1, W+1) for r in range(H)]
        dmap = {'L':'L','R':'R','U':'U','D':'D'}
        ch, cw = sh-1, sw
    else:
        n = H; s = W
        col = [A[(j-1)*W + r] for j in range(1, H+1) for r in range(W)]
        dmap = {'U':'L','D':'R','L':'U','R':'D'}
        ch, cw = sw-1, sh

    # Lpre[j]: prefix DP vector at column j (includes column j values), j = 0..n
    # Rrow[j]: suffix row vector such that answer = dot(Rrow[j+1], Lpre[j]), j = 1..n+1
    Lpre = [[0]*s for _ in range(n+1)]
    Lpre[0][0] = 1
    for j in range(1, n+1):
        base = (j-1)*s
        prev = Lpre[j-1]; cur = Lpre[j]
        run = 0
        for c in range(s):
            run = (col[base+c] * ((prev[c] + run) % MOD)) % MOD
            cur[c] = run
    Rrow = [[0]*s for _ in range(n+2)]
    Rrow[n+1][s-1] = 1
    for j in range(n, 0, -1):
        base = (j-1)*s
        nxt = Rrow[j+1]; cur = Rrow[j]
        run = 0
        for r in range(s-1, -1, -1):
            run = (col[base+r] * ((nxt[r] + run) % MOD)) % MOD
            cur[r] = run

    out = []
    j = cw
    for d, a in queries:
        dm = dmap[d]
        if dm == 'L':
            j -= 1
            # Rrow[j] became stale when column j was last updated; refresh it.
            base = (j-1)*s
            nxt = Rrow[j+1]; cur = Rrow[j]
            run = 0
            for r in range(s-1, -1, -1):
                run = (col[base+r] * ((nxt[r] + run) % MOD)) % MOD
                cur[r] = run
        elif dm == 'R':
            j += 1
        elif dm == 'U':
            ch -= 1
        else:
            ch += 1
        col[(j-1)*s + ch] = a
        # Recompute Lpre[j] from Lpre[j-1] (always valid).
        base = (j-1)*s
        prev = Lpre[j-1]; cur = Lpre[j]
        run = 0
        for c in range(s):
            run = (col[base+c] * ((prev[c] + run) % MOD)) % MOD
            cur[c] = run
        # Answer = dot(Rrow[j+1], Lpre[j]); Rrow[j+1] is always valid.
        rr = Rrow[j+1]
        ans = 0
        for r in range(s):
            ans = (ans + rr[r]*cur[r]) % MOD
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

main()