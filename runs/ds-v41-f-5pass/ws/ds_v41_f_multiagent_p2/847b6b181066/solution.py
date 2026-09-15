import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3].decode()

    # displacement per wind direction (dr, dc)
    delta = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}

    # seen holds prefix-sum positions P_s for s processed so far; include P_0 = (0,0)
    seen = {(0, 0)}
    r = 0
    c = 0
    out = []
    for ch in S:
        dr, dc = delta[ch]
        r += dr
        c += dc
        # smoke from origin at time s+0.5 (s<t) reaches (R,C) iff P_s = P_t - (R,C)
        if (r - R, c - C) in seen:
            out.append('1')
        else:
            out.append('0')
        seen.add((r, c))

    sys.stdout.write(''.join(out) + '\n')

main()