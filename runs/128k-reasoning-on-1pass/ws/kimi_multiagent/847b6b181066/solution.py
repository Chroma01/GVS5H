import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].decode()

    # Prefix positions P[t] lie in [-N, N]^2; query points P[t]-(R,C) lie in
    # [-2N, 2N]^2, so use offset 2N and width 4N+1 for an injective int key.
    off = 2 * N
    W = 4 * N + 1

    first = {}  # key -> earliest time this prefix position occurred
    rs = [0] * (N + 1)
    cs = [0] * (N + 1)

    r = c = 0
    first[(r + off) * W + (c + off)] = 0  # initial smoke = creation at time 0

    for t in range(1, N + 1):
        ch = S[t - 1]
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:  # 'E'
            c += 1
        rs[t] = r
        cs[t] = c
        k = (r + off) * W + (c + off)
        if k not in first:
            first[k] = t  # smoke generated exactly at first-occurrence times

    out = []
    get = first.get
    for t in range(1, N + 1):
        # Smoke at (R,C) at time t iff P[t]-(R,C) is a prefix position
        # whose first occurrence time is <= t.
        yk = (rs[t] - R + off) * W + (cs[t] - C + off)
        f = get(yk)
        out.append('1' if (f is not None and f <= t) else '0')

    sys.stdout.write(''.join(out))

main()