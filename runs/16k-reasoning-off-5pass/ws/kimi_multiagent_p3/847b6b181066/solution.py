import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3]

    # Encode 2D coordinate (r, c) as a single integer key.
    # Inserted points P(g) have coords in [-N, N]; queried points
    # P(t) - (R, C) have coords in [-2N, 2N]. With OFF = 2N+2 and
    # stride W = 4N+5, both r+OFF and c+OFF lie in [2, 4N+2] ⊂ [0, W),
    # so the encoding is provably injective over all used points.
    OFF = 2 * N + 2
    W = 4 * N + 5

    def key(r, c):
        return (r + OFF) * W + (c + OFF)

    seen = set()
    seen.add(key(0, 0))  # initial smoke puff at origin, generation time g=0

    cr = cc = 0  # current prefix displacement P(t)
    out = []
    for t in range(N):
        ch = S[t]
        if ch == 'N':
            cr -= 1
        elif ch == 'S':
            cr += 1
        elif ch == 'W':
            cc -= 1
        else:  # 'E'
            cc += 1

        # Smoke at (R, C) at time t+0.5 iff some puff g has P(g) = P(t) - (R, C)
        if key(cr - R, cc - C) in seen:
            out.append('1')
        else:
            out.append('0')

        # Generate new puff at origin if origin is empty, i.e. P(t) not in seen
        k = key(cr, cc)
        if k not in seen:
            seen.add(k)

    sys.stdout.write(''.join(out) + '\n')

main()