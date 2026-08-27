import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    A = data[idx:idx+n]; idx += n
    B = data[idx:idx+n]; idx += n
    P = data[idx:idx+n]; idx += n
    Q = data[idx:idx+n]; idx += n

    A = [int(v) for v in A]
    B = [int(v) for v in B]
    P = [int(v) for v in P]
    Q = [int(v) for v in Q]

    # 1-indexed arrays
    invP = [0]*(n+1)
    invQ = [0]*(n+1)
    for i in range(1, n+1):
        invP[P[i-1]] = i
        invQ[Q[i-1]] = i

    NEG = -1
    distP = [NEG]*(n+1)
    distQ = [NEG]*(n+1)
    nodeAtDistP = [0]*(n+1)
    nodeAtDistQ = [0]*(n+1)

    distP[x] = 0
    nodeAtDistP[0] = x
    cur = x
    d = 0
    while True:
        cur = invP[cur]
        d += 1
        if cur == x:
            break
        distP[cur] = d
        nodeAtDistP[d] = cur

    distQ[x] = 0
    nodeAtDistQ[0] = x
    cur = x
    d = 0
    while True:
        cur = invQ[cur]
        d += 1
        if cur == x:
            break
        distQ[cur] = d
        nodeAtDistQ[d] = cur

    Dr = 0
    Db = 0
    for i in range(1, n+1):
        if A[i-1] == 1:
            dp = distP[i]
            if dp < 0:
                sys.stdout.write("-1\n")
                return
            if dp > Dr:
                Dr = dp
        if B[i-1] == 1:
            dq = distQ[i]
            if dq < 0:
                sys.stdout.write("-1\n")
                return
            if dq > Db:
                Db = dq

    if Dr == 0 and Db == 0:
        sys.stdout.write("0\n")
        return

    # posB[v] = position in Bchain (0-based) if v is in Bchain
    posB = [-1]*(n+1)
    for dd in range(1, Db+1):
        v = nodeAtDistQ[dd]
        posB[v] = Db - dd

    # LIS (strictly increasing) over posB values in Rchain order
    tails = []
    for dd in range(Dr, 0, -1):
        v = nodeAtDistP[dd]
        p = posB[v]
        if p < 0:
            continue
        j = bisect_left(tails, p)
        if j == len(tails):
            tails.append(p)
        else:
            tails[j] = p
    L = len(tails)

    sys.stdout.write(str(Dr + Db - L) + "\n")

main()