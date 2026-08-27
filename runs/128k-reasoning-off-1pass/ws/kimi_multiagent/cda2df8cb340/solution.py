import sys

def main():
    sys.setrecursionlimit(1 << 20)
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    def f0(vals):
        # sum over i<=j of oddpart(v_i + v_j)
        if not vals:
            return 0
        E = []
        O = []
        for v in vals:
            if v & 1:
                O.append(v)
            else:
                E.append(v)
        total = 0
        nE = len(E)
        nO = len(O)
        if nE and nO:
            # even + odd = odd -> f is identity
            total += nO * sum(E) + nE * sum(O)
        if nE:
            # f(2x + 2y) = f(x + y)
            total += f0([v >> 1 for v in E])
        if nO:
            # f((2u+1)+(2w+1)) = f(u + w + 1)
            total += f1([(v - 1) >> 1 for v in O])
        return total

    def f1(vals):
        # sum over i<=j of oddpart(v_i + v_j + 1)
        if not vals:
            return 0
        E = []
        O = []
        for v in vals:
            if v & 1:
                O.append(v)
            else:
                E.append(v)
        total = 0
        nE = len(E)
        nO = len(O)
        if nE:
            # same parity: sum+1 is odd -> direct
            sE = sum(E)
            total += (nE + 1) * sE + nE * (nE + 1) // 2
        if nO:
            sO = sum(O)
            total += (nO + 1) * sO + nO * (nO + 1) // 2
        if nE and nO:
            # mixed: (2u) + (2w+1) + 1 = 2(u + w + 1)
            total += h1([v >> 1 for v in E], [(v - 1) >> 1 for v in O])
        return total

    def h1(X, Y):
        # sum over all x in X, y in Y of oddpart(x + y + 1)
        if not X or not Y:
            return 0
        XE = []
        XO = []
        for v in X:
            if v & 1:
                XO.append(v)
            else:
                XE.append(v)
        YE = []
        YO = []
        for v in Y:
            if v & 1:
                YO.append(v)
            else:
                YE.append(v)
        total = 0
        nXE = len(XE)
        nXO = len(XO)
        nYE = len(YE)
        nYO = len(YO)
        if nXE and nYE:
            # even+even+1 odd -> direct
            total += nYE * sum(XE) + nXE * sum(YE) + nXE * nYE
        if nXO and nYO:
            # odd+odd+1 odd -> direct
            total += nYO * sum(XO) + nXO * sum(YO) + nXO * nYO
        if nXE and nYO:
            total += h1([v >> 1 for v in XE], [(v - 1) >> 1 for v in YO])
        if nXO and nYE:
            total += h1([(v - 1) >> 1 for v in XO], [v >> 1 for v in YE])
        return total

    sys.stdout.write(str(f0(A)) + "\n")

main()