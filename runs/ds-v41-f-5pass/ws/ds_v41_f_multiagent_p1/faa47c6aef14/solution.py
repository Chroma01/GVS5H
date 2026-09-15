import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    X = int(data[p]) - 1; p += 1
    A = [int(x) for x in data[p:p + N]]; p += N
    B = [int(x) for x in data[p:p + N]]; p += N
    P = [int(x) - 1 for x in data[p:p + N]]; p += N
    Q = [int(x) - 1 for x in data[p:p + N]]; p += N

    def build_cycle(perm, start):
        seq = []
        cur = start
        while True:
            seq.append(cur)
            cur = perm[cur]
            if cur == start:
                break
        return seq

    pc = build_cycle(P, X)          # [X, P_X, P^2_X, ...]
    qc = build_cycle(Q, X)
    pset = set(pc)
    qset = set(qc)

    # Feasibility: every red ball must lie on the P-cycle of X, every blue on Q-cycle of X.
    for i in range(N):
        if A[i] and i not in pset:
            sys.stdout.write("-1\n")
            return
        if B[i] and i not in qset:
            sys.stdout.write("-1\n")
            return

    def req(seq, arr):
        # seq[0] is X. Farthest ball = smallest index j>=1 with a ball.
        for j in range(1, len(seq)):
            if arr[seq[j]]:
                return seq[j:]        # operation order: farthest -> predecessor of X
        return []

    R = req(pc, A)
    Bs = req(qc, B)

    # Min ops = |R| + |Bs| - LCS(R, Bs). Elements distinct -> LCS via LIS.
    pos = {}
    for i, v in enumerate(R):
        pos[v] = i
    tails = []
    for v in Bs:
        if v in pos:
            x = pos[v]
            k = bisect_left(tails, x)
            if k == len(tails):
                tails.append(x)
            else:
                tails[k] = x

    sys.stdout.write(str(len(R) + len(Bs) - len(tails)) + "\n")


main()