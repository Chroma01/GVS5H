import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3].decode()

    seen = {(0, 0)}   # prefix positions P(0), P(1), ... ; generation times
    r = c = 0         # current cumulative wind displacement P(t)
    res = []

    for ch in S:
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:  # 'E'
            c += 1

        # smoke at (R,C) at time t iff some generation g<=t has P(g)=P(t)-D
        if (r - R, c - C) in seen:
            res.append('1')
        else:
            res.append('0')

        seen.add((r, c))

    sys.stdout.write(''.join(res) + '\n')

main()