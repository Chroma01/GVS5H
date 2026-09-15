import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    seen = {(0, 0)}
    r = 0
    c = 0
    ans = []

    for ch in S[:N]:
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:  # ch == 'E'
            c += 1

        qr = r - R
        qc = c - C

        if (qr, qc) in seen:
            ans.append('1')
        else:
            ans.append('0')

        seen.add((r, c))

    sys.stdout.write(''.join(ans))


if __name__ == "__main__":
    main()