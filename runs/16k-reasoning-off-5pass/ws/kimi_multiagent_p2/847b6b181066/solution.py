import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].decode()

    # Direction deltas
    # N: (-1, 0), S: (1, 0), W: (0, -1), E: (0, 1)
    dr = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
    dc = {'N': 0, 'S': 0, 'W': -1, 'E': 1}

    births = set()
    births.add((0, 0))  # initial smoke born at time 0, P[0] = (0,0)

    pr = 0
    pc = 0
    out = []
    for t in range(n):
        ch = S[t]
        pr += dr[ch]
        pc += dc[ch]
        # Generation check: smoke at (0,0) at time t+0.5 (before generation)
        # iff some existing birth b has P[b] == P[t].
        if (pr, pc) not in births:
            births.add((pr, pc))  # new birth at time t, P[t] = (pr, pc)
        # Query: smoke at (R,C) iff some birth b (<= t) has P[b] = P[t] - (R,C)
        if (pr - R, pc - C) in births:
            out.append('1')
        else:
            out.append('0')

    sys.stdout.write(''.join(out) + '\n')

main()