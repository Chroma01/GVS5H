import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    # Encode (x, y) as (x + offset) * base + (y + offset).
    # Query coordinates can be in [-2N, 2N], so this offset/base is safe.
    offset = 2 * N + 5
    base = 4 * N + 11

    r = 0
    c = 0

    seen = {(offset) * base + offset}  # encodes (0, 0)
    ans = bytearray(N)

    contains = seen.__contains__
    add = seen.add

    for i, ch in enumerate(S):
        if ch == 78:       # 'N'
            r -= 1
        elif ch == 83:     # 'S'
            r += 1
        elif ch == 87:     # 'W'
            c -= 1
        else:              # 'E'
            c += 1

        key = (r - R + offset) * base + (c - C + offset)
        ans[i] = 49 if contains(key) else 48  # ord('1') / ord('0')

        add((r + offset) * base + (c + offset))

    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()