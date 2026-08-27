import sys

def solve():
    data = sys.stdin.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3]

    # Encode (r, c) as a single integer; offset keeps it non-negative.
    # |r|, |c| <= N, so use base = 2N+5.
    base = 2 * N + 5
    off = N + 2

    def enc(r, c):
        return (r + off) * base + (c + off)

    births = set()
    births.add(enc(0, 0))  # initial smoke at time 0

    pr = 0
    pc = 0
    out = []
    for ch in S:
        if ch == 'N':
            pr -= 1
        elif ch == 'S':
            pr += 1
        elif ch == 'W':
            pc -= 1
        else:  # 'E'
            pc += 1

        # Smoke at (R,C) at time t+0.5 iff some birth prefix P[k] = P[t] - (R,C)
        if enc(pr - R, pc - C) in births:
            out.append('1')
        else:
            out.append('0')

        # If origin empty at time t+0.5, new smoke is born there (birth prefix P[t])
        cur = enc(pr, pc)
        if cur not in births:
            births.add(cur)

    sys.stdout.write(''.join(out) + '\n')

solve()