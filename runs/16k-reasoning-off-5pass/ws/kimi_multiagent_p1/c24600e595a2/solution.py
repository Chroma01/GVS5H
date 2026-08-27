import sys


class BIT:
    __slots__ = ('n', 't')

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i, v):
        i += 1
        while i <= self.n:
            self.t[i] += v
            i += i & -i

    def sum(self, i):  # prefix sum over [0, i]
        i += 1
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


def solve_fast(N, A, B, C):
    W0 = 0
    S1 = []  # A=1,B=0 : flip off
    S0 = []  # A=0,B=1 : flip on
    D = []   # A=1,B=1 : candidates to park
    for j in range(N):
        if A[j] == 1:
            W0 += C[j]
        if A[j] == 1 and B[j] == 0:
            S1.append(C[j])
        elif A[j] == 0 and B[j] == 1:
            S0.append(C[j])
        elif A[j] == 1 and B[j] == 1:
            D.append(C[j])

    # coordinate compression
    allc = sorted(set(S1) | set(S0) | set(D)) if (S1 or S0 or D) else []
    comp = {v: i for i, v in enumerate(allc)}
    M = len(allc)

    O = sorted(S1, reverse=True)   # offs, decreasing
    U = sorted(S0)                 # ons, increasing
    Wbase = W0 - sum(S1)

    # base cost K=0
    cost = 0
    W = W0
    for c in O:
        W -= c
        cost += W
    W = Wbase
    for c in U:
        W += c
        cost += W
    ans = cost

    # BITs over O and U (count + sum)
    oc = BIT(M); osm = BIT(M)
    uc = BIT(M); usm = BIT(M)
    for c in O:
        oc.add(comp[c], 1); osm.add(comp[c], c)
    for c in U:
        uc.add(comp[c], 1); usm.add(comp[c], c)

    D.sort(reverse=True)  # park in decreasing C order
    for c in D:
        i = comp[c]
        # O elements with C <= c : count/sum  (indices 0..i since comp ascending)
        cntO_le = oc.sum(i)
        sumO_le = osm.sum(i)
        # U elements with C < c : indices 0..i-1
        cntU_lt = uc.sum(i - 1) if i > 0 else 0
        sumU_lt = usm.sum(i - 1) if i > 0 else 0
        # Delta = 2*Wbase + SufO + PreU - c*(cntO_le + cntU_lt + 1)
        delta = 2 * Wbase + sumO_le + sumU_lt - c * (cntO_le + cntU_lt + 1)
        cost += delta
        Wbase -= c
        oc.add(i, 1); osm.add(i, c)
        uc.add(i, 1); usm.add(i, c)
        if cost < ans:
            ans = cost
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos + N]]; pos += N
    B = [int(x) for x in data[pos:pos + N]]; pos += N
    C = [int(x) for x in data[pos:pos + N]]; pos += N
    print(solve_fast(N, A, B, C))


main()