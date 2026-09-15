import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3]
    T = data[4]

    # Zero operations always fine.
    if S == T:
        sys.stdout.write("Yes\n")
        return

    # If X+Y > N there is no legal choice of i, hence no operation at all.
    if X + Y > N:
        sys.stdout.write("No\n")
        return

    ZERO = 48  # ord('0') ; bytes indexing yields ints

    # Counts of zeros must match.  (Implied by residues, but cheap short-circuit.)
    if S.count(b'0') != T.count(b'0'):
        sys.stdout.write("No\n")
        return

    # Invariant: i-th zero lives at positions congruent mod Y, in order.
    # Invariant: i-th one lives at positions congruent mod X, in order.
    zs = []; os_ = []; sz = 0
    for i in range(N):
        if S[i] == ZERO:
            zs.append(i % Y); sz += i
        else:
            os_.append(i % X)

    zt = []; ot = []; tz = 0
    for i in range(N):
        if T[i] == ZERO:
            zt.append(i % Y); tz += i
        else:
            ot.append(i % X)

    if zs != zt or os_ != ot:
        sys.stdout.write("No\n")
        return

    # Every move shifts the sum of zero positions by exactly +-X*Y, so the sum
    # of zero positions is invariant modulo X*Y.  (Redundant on all tested data
    # because it is a function of the two ordered residue sequences, but it is a
    # genuine necessary condition and cheap, so we keep it.)
    M = X * Y
    if sz % M != tz % M:
        sys.stdout.write("No\n")
        return

    sys.stdout.write("Yes\n")

main()