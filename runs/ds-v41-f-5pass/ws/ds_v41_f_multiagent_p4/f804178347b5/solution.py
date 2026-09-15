import sys

def main():
    data = sys.stdin.buffer.read().split()
    A = data[1]  # bytes object of '0'/'1'
    # original value per leaf: 0/1 ; flip cost per leaf = 1
    o = [c & 1 for c in A]
    g = [1] * len(o)

    while len(o) > 1:
        o0 = o[0::3]; o1 = o[1::3]; o2 = o[2::3]
        g0 = g[0::3]; g1 = g[1::3]; g2 = g[2::3]
        no = []
        ng = []
        ao = no.append
        ag = ng.append
        for a, b, c, da, db, dc in zip(o0, o1, o2, g0, g1, g2):
            # node original value = majority
            oo = 1 if (a + b + c) >= 2 else 0
            # cost to turn each child into (1 - oo): 0 if already 1-oo, else its flip cost
            e1 = da if a == oo else 0
            e2 = db if b == oo else 0
            e3 = dc if c == oo else 0
            tot = e1 + e2 + e3
            mx = e1
            if e2 > mx: mx = e2
            if e3 > mx: mx = e3
            ao(oo)
            ag(tot - mx)   # sum of the two smallest = total - max
        o = no
        g = ng

    sys.stdout.write(str(g[0]) + "\n")

main()