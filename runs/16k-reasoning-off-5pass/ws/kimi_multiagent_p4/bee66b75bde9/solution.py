import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = {}
    U = {}
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if c == b'B':
            if x in L:
                if y > L[x]:
                    L[x] = y
            else:
                L[x] = y
        else:  # W
            v = y - 1
            if x in U:
                if v < U[x]:
                    U[x] = v
            else:
                U[x] = v

    rows = sorted(set(L) | set(U))
    hi = N
    for x in rows:
        l = L.get(x, 0)
        u = U.get(x, N)
        if l > u or l > hi:
            sys.stdout.write("No\n")
            return
        if u < hi:
            hi = u
    sys.stdout.write("Yes\n")

main()