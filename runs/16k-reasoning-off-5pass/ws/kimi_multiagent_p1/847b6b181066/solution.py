import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3]

    # Encode (r, c) as a single integer. Coordinates stay within [-N, N].
    BASE = 2 * N + 5
    OFF = N + 2
    def enc(r, c):
        return (r + OFF) * BASE + (c + OFF)

    births = set()
    births.add(enc(0, 0))  # initial smoke at time 0

    pr = 0  # prefix displacement row
    pc = 0  # prefix displacement col
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

        # Smoke at (R, C) at t+0.5 iff some birth k has P_k = P_t - (R, C).
        out.append('1' if enc(pr - R, pc - C) in births else '0')

        # Generate new smoke at (0,0) if empty: (0,0) occupied iff P_t in births.
        key = enc(pr, pc)
        if key not in births:
            births.add(key)

    sys.stdout.write(''.join(out) + '\n')

main()