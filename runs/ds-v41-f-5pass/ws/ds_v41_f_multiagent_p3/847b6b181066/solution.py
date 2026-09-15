import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].decode()

    seen = {(0, 0)}  # all prefix positions P_0 .. P_{t-1}
    r = c = 0
    out = []

    for ch in S:
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:  # 'E'
            c += 1

        # Particle born at time k sits at P_t - P_k at time t+0.5.
        # Target (R, C) occupied iff some earlier P_k == P_t - (R, C).
        if (r - R, c - C) in seen:
            out.append('1')
        else:
            out.append('0')

        seen.add((r, c))

    sys.stdout.write(''.join(out) + '\n')


main()