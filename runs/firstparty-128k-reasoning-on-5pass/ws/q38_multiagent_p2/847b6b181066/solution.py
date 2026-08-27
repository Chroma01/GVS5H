import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    target_r = int(data[1])
    target_c = int(data[2])
    s = data[3]

    # All prefix coordinates are in [-n, n] on each axis.
    # Query points (prefix - target) are in [-2n, 2n] on each axis.
    # This base makes (x, y) -> x * base + y injective for all used points.
    base = 4 * n + 5

    visited = set()
    visited.add(0)  # P_0 = (0, 0)

    r = 0
    c = 0
    ans = bytearray()
    append = ans.append

    for ch in s:
        if ch == 78:      # 'N'
            r -= 1
        elif ch == 87:    # 'W'
            c -= 1
        elif ch == 83:    # 'S'
            r += 1
        else:             # 'E'
            c += 1

        # Insert current prefix position P_t.
        visited.add(r * base + c)

        # Smoke exists at (target_r, target_c) iff P_t - target is visited.
        query = (r - target_r) * base + (c - target_c)
        append(49 if query in visited else 48)

    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()