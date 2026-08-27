import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    L = {}
    U = {}
    idx = 2
    for _ in range(m):
        x = int(data[idx]); y = int(data[idx+1]); c = data[idx+2]
        idx += 3
        if c == b'B':
            if x in L:
                if y > L[x]:
                    L[x] = y
            else:
                L[x] = y
        else:
            v = y - 1
            if x in U:
                if v < U[x]:
                    U[x] = v
            else:
                U[x] = v
    rows = set(L.keys())
    rows.update(U.keys())
    run = 0
    ok = True
    for x in sorted(rows, reverse=True):
        lv = L.get(x, 0)
        if lv > run:
            run = lv
        uv = U.get(x, n)
        if run > uv:
            ok = False
            break
    sys.stdout.write("Yes\n" if ok else "No\n")

main()