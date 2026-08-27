import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = data[p]; R[i] = data[p + 1]; p += 2
    Q = data[p]; p += 1
    Xs = data[p:p + Q]

    V = max(Xs) if Xs else 1
    n = V + 2  # fenwick size; index b+1 can be V+1
    bit = [0] * (n + 1)

    # highest power of two <= n
    hb = 1
    while (hb << 1) <= n:
        hb <<= 1

    for i in range(N):
        Li = L[i]
        Ri = R[i]
        # posL = max pos in [0..V] with value(pos) < Li  (value(0) treated as -inf)
        pos = 0
        acc = 0
        k = hb
        while k:
            nxt = pos + k
            if nxt <= V:
                # value(nxt) = nxt + prefixA(nxt); prefixA(nxt) = acc + bit[nxt]
                if nxt + acc + bit[nxt] < Li:
                    pos = nxt
                    acc += bit[nxt]
            k >>= 1
        a = pos + 1
        # posR = max pos in [0..V] with value(pos) <= Ri
        pos = 0
        acc = 0
        k = hb
        while k:
            nxt = pos + k
            if nxt <= V:
                if nxt + acc + bit[nxt] <= Ri:
                    pos = nxt
                    acc += bit[nxt]
            k >>= 1
        b = pos
        if a <= b:
            # range add +1 on [a, b]: point updates at a (+1) and b+1 (-1)
            j = a
            while j <= n:
                bit[j] += 1
                j += j & (-j)
            e = b + 1
            j = e
            while j <= n:
                bit[j] -= 1
                j += j & (-j)

    out = []
    for X in Xs:
        s = 0
        j = X
        while j > 0:
            s += bit[j]
            j -= j & (-j)
        out.append(str(X + s))
    sys.stdout.write("\n".join(out) + "\n")

main()