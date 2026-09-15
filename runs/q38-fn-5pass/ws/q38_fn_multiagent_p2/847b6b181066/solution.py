import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    # Encode coordinates (x, y) with x, y in [-N, N] as a unique integer.
    off = N
    base = 2 * N + 1

    seen = set()
    seen.add(off * base + off)  # (0, 0)

    add = seen.add
    contains = seen.__contains__

    r = 0
    c = 0

    ans = []
    append = ans.append

    lower = -N
    upper = N

    for ch in S:
        if ch == 78:       # 'N'
            r -= 1
        elif ch == 83:     # 'S'
            r += 1
        elif ch == 87:     # 'W'
            c -= 1
        else:              # 'E'
            c += 1

        key_d = (r + off) * base + (c + off)

        # If the origin is empty after the wind, a new smoke is generated.
        # This happens exactly when the current cumulative displacement is new.
        if not contains(key_d):
            add(key_d)

        # Smoke generated at cumulative displacement g is at D - g now.
        # We need D - g == (R, C), i.e. g == D - (R, C).
        qr = r - R
        qc = c - C

        if lower <= qr <= upper and lower <= qc <= upper:
            key_q = (qr + off) * base + (qc + off)
            append('1' if contains(key_q) else '0')
        else:
            append('0')

    sys.stdout.write(''.join(ans))


if __name__ == "__main__":
    main()