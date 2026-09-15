import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    offset = 2 * N + 5
    M = 4 * N + 10

    # Prefix position P[0] = (0, 0)
    seen = set()
    seen.add((0 + offset) * M + (0 + offset))

    r = 0
    c = 0
    ans = []

    for ch in S:
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:  # ch == 'E'
            c += 1

        # Need P[b] = P[t] - (R, C)
        qr = r - R
        qc = c - C
        qkey = (qr + offset) * M + (qc + offset)

        if qkey in seen:
            ans.append('1')
        else:
            ans.append('0')

        # Insert current prefix position P[t]
        curkey = (r + offset) * M + (c + offset)
        seen.add(curkey)

    sys.stdout.write(''.join(ans))

if __name__ == "__main__":
    main()