import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    s = data[1] if len(data) > 1 else b""
    # in case the string was given with spaces separating characters
    if len(data) > 2:
        s = b"".join(data[1:])
    vals = [x - 48 for x in s]
    L = 3 ** N
    if len(vals) != L:
        vals = vals[:L]
    costs = [1] * len(vals)

    for _ in range(N):
        v0 = vals[0::3]; v1 = vals[1::3]; v2 = vals[2::3]
        c0 = costs[0::3]; c1 = costs[1::3]; c2 = costs[2::3]
        nv = []
        nc = []
        av = nv.append
        ac = nc.append
        for a, b, c, ca, cb, cc in zip(v0, v1, v2, c0, c1, c2):
            t = a + b + c
            if t == 0:
                av(0)
                m = ca
                if cb > m: m = cb
                if cc > m: m = cc
                ac(ca + cb + cc - m)
            elif t == 3:
                av(1)
                m = ca
                if cb > m: m = cb
                if cc > m: m = cc
                ac(ca + cb + cc - m)
            elif t == 2:
                av(1)
                # children with value 1: flip the cheapest one
                if a == 0:
                    m = cb if cb < cc else cc
                elif b == 0:
                    m = ca if ca < cc else cc
                else:
                    m = ca if ca < cb else cb
                ac(m)
            else:
                av(0)
                # children with value 0: flip the cheapest one
                if a == 1:
                    m = cb if cb < cc else cc
                elif b == 1:
                    m = ca if ca < cc else cc
                else:
                    m = ca if ca < cb else cb
                ac(m)
        vals = nv
        costs = nc

    sys.stdout.write(str(costs[0]) + "\n")

main()