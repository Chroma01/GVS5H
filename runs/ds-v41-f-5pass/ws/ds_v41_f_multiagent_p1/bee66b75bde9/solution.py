import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])

    # L[x] = max black y in row x, default 0
    # R[x] = min white y - 1 in row x, default N
    L = {}
    R = {}
    idx = 2
    for _ in range(M):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3
        if c == b'B':
            if x in L:
                if y > L[x]:
                    L[x] = y
            else:
                L[x] = y
        else:
            r = y - 1
            if x in R:
                if r < R[x]:
                    R[x] = r
            else:
                R[x] = r

    rows = set(L) | set(R)

    # same-row consistency
    for x in rows:
        lx = L.get(x, 0)
        rx = R.get(x, N)
        if lx > rx:
            sys.stdout.write("No\n")
            return

    # global monotonicity check
    sorted_rows = sorted(rows)
    min_r = N
    for x in sorted_rows:
        lx = L.get(x, 0)
        rx = R.get(x, N)
        if rx < min_r:
            min_r = rx
        if lx > min_r:
            sys.stdout.write("No\n")
            return

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    solve()