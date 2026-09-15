import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]
    C = data[1 + 2 * n:1 + 3 * n]

    one = b'1'
    F = []  # A=1, B=0 : forced off
    T = []  # A=0, B=1 : forced on
    M = []  # A=1, B=1 : optional toggle
    for i in range(n):
        ai = A[i]
        bi = B[i]
        c = int(C[i])
        if ai == one:
            if bi == one:
                M.append(c)
            else:
                F.append(c)
        else:
            if bi == one:
                T.append(c)
            # else 0,0 : ignored

    f = len(F)
    t = len(T)
    K = f + t
    CM = sum(M)
    CT = sum(T)

    F.sort()
    T.sort()

    prefF = [0] * (f + 1)
    for i in range(f):
        prefF[i + 1] = prefF[i] + F[i]
    prefT = [0] * (t + 1)
    for i in range(t):
        prefT[i + 1] = prefT[i] + T[i]

    # sum of min over unordered pairs
    PFF = 0
    for i in range(f):
        PFF += F[i] * (f - 1 - i)
    PTT = 0
    for i in range(t):
        PTT += T[i] * (t - 1 - i)

    # cost with no optional positions toggled
    base = K * CM + PFF + CT + PTT
    ans = base
    cur = base
    P = 0  # weight of already chosen optional positions (all >= current)

    M.sort(reverse=True)
    for c in M:
        j = bisect_left(F, c)
        SF = prefF[j] + c * (f - j)      # sum_F min(c, C)
        k = bisect_left(T, c)
        ST = prefT[k] + c * (t - k)      # sum_T min(c, C)
        # marginal of adding c to current prefix (all chosen weights >= c)
        delta = 2 * (CM - P) - (K + 1) * c + SF + ST
        cur += delta
        P += c
        if cur < ans:
            ans = cur

    sys.stdout.write(str(ans) + "\n")


main()