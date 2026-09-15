import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    lower = {}
    upper = {}

    idx = 2
    for _ in range(M):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3

        if c == b'B':
            if y > lower.get(x, 0):
                lower[x] = y
        else:
            u = y - 1
            if u < upper.get(x, N):
                upper[x] = u

    rows = set(lower.keys())
    rows.update(upper.keys())

    max_lower = 0

    for x in sorted(rows, reverse=True):
        l = lower.get(x, 0)
        if l > max_lower:
            max_lower = l

        u = upper.get(x, N)
        if max_lower > u:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()