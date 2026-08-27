import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # Let r[x] be the black-prefix length of row x.
    # Column conditions are equivalent to r[1] >= r[2] >= ... >= r[N].
    # B at (x, y): r[x] >= y.  W at (x, y): r[x] <= y - 1.
    L = {}
    U = {}
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if x not in L:
            L[x] = 0
            U[x] = N
        if c == b'B':
            if y > L[x]:
                L[x] = y
        else:
            v = y - 1
            if v < U[x]:
                U[x] = v

    # Scan constrained rows upward. The largest feasible value for the current
    # row is min(all U so far); it must still reach this row's lower bound L.
    min_u = N
    for x in sorted(L):
        if U[x] < min_u:
            min_u = U[x]
        if L[x] > min_u:
            sys.stdout.write("No\n")
            return
    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    main()