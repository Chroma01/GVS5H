import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]) - 1; idx += 1
    A = [1 if t == b'1' else 0 for t in data[idx:idx + N]]; idx += N
    B = [1 if t == b'1' else 0 for t in data[idx:idx + N]]; idx += N
    P = [int(t) - 1 for t in data[idx:idx + N]]; idx += N
    Q = [int(t) - 1 for t in data[idx:idx + N]]; idx += N

    def inverse(perm):
        inv = [0] * N
        for i in range(N):
            inv[perm[i]] = i
        return inv

    Pinv = inverse(P)
    Qinv = inverse(Q)

    def build_chain(balls, inv):
        # cycle[0] = X, cycle[k] = inv^k(X); a ball at cycle[k] needs k ops
        cycle = [X]
        cur = X
        while True:
            nxt = inv[cur]
            if nxt == X:
                break
            cycle.append(nxt)
            cur = nxt

        # every ball of this colour must lie on the cycle containing X
        oncycle = bytearray(N)
        for c in cycle:
            oncycle[c] = 1
        for i in range(N):
            if balls[i] and not oncycle[i]:
                return None

        # farthest occupied box (outside X) forces the operation chain
        d = 0
        for k in range(len(cycle) - 1, -1, -1):
            if balls[cycle[k]]:
                d = k
                break
        return cycle[d:0:-1]

    R = build_chain(A, Pinv)
    if R is None:
        sys.stdout.write("-1\n")
        return
    Bc = build_chain(B, Qinv)
    if Bc is None:
        sys.stdout.write("-1\n")
        return

    # joint minimum = shortest common supersequence of the two chains
    # = |R| + |B| - LCS(R, B); chains have distinct elements -> LCS via LIS
    posR = {v: i for i, v in enumerate(R)}
    seq = [posR[b] for b in Bc if b in posR]
    tails = []
    for v in seq:
        k = bisect_left(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v

    sys.stdout.write(str(len(R) + len(Bc) - len(tails)) + "\n")


main()