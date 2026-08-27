import sys

def main():
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    def cross(X, Y):
        # sum over all (i, j) of f(X[i] + Y[j])
        if not X or not Y:
            return 0
        Xe, Xo, Ye, Yo = [], [], [], []
        for x in X:
            if x & 1:
                Xo.append(x)
            else:
                Xe.append(x)
        for y in Y:
            if y & 1:
                Yo.append(y)
            else:
                Ye.append(y)
        res = 0
        # mixed parity: sum is odd, f = x + y
        if Xe and Yo:
            res += len(Xe) * sum(Yo) + sum(Xe) * len(Yo)
        if Xo and Ye:
            res += len(Xo) * sum(Ye) + sum(Xo) * len(Ye)
        # both even: f(x+y) = f(x/2 + y/2)
        if Xe and Ye:
            res += cross([x >> 1 for x in Xe], [y >> 1 for y in Ye])
        # both odd: f(x+y) = f((x+1)/2 + (y-1)/2)
        if Xo and Yo:
            res += cross([(x + 1) >> 1 for x in Xo], [(y - 1) >> 1 for y in Yo])
        return res

    def self_solve(A):
        # sum over i <= j of f(A[i] + A[j])
        if not A:
            return 0
        E, O = [], []
        for a in A:
            if a & 1:
                O.append(a)
            else:
                E.append(a)
        res = 0
        # mixed parity pairs: f = e + o
        if E and O:
            res += len(E) * sum(O) + sum(E) * len(O)
        # even-even pairs
        if E:
            res += self_solve([e >> 1 for e in E])
        # odd-odd pairs: (B(U,V) + sum(O)) // 2
        if O:
            U = [(o + 1) >> 1 for o in O]
            V = [(o - 1) >> 1 for o in O]
            res += (cross(U, V) + sum(O)) // 2
        return res

    print(self_solve(A))

main()