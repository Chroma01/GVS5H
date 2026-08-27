import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]

    f = [-1] * 26
    # set(zip(S,T)) has at most 676 elements; building it is O(N)
    for a, b in set(zip(S, T)):
        x = a - 97
        y = b - 97
        if f[x] == -1:
            f[x] = y
        elif f[x] != y:
            sys.stdout.write("-1\n")
            return

    dom = [c for c in range(26) if f[c] != -1]
    changed = sum(1 for c in dom if f[c] != c)

    if changed == 0:
        sys.stdout.write("0\n")
        return

    indeg = Counter(f[c] for c in dom)

    if len(dom) == 26 and len(set(f[c] for c in dom)) == 26:
        # f is a permutation of all 26 letters, and it's not the identity:
        # the number of distinct letters can only decrease, so impossible.
        sys.stdout.write("-1\n")
        return

    color = [0] * 26  # 0 = unvisited, 1 = on current path, 2 = finished
    extra = 0
    for s in range(26):
        if color[s] != 0:
            continue
        path = []
        v = s
        while True:
            if color[v] == 0:
                color[v] = 1
                path.append(v)
                if f[v] == -1:
                    break
                v = f[v]
            elif color[v] == 1:
                i = path.index(v)
                cyc = path[i:]
                if len(cyc) >= 2 and all(indeg[u] == 1 for u in cyc):
                    extra += 1
                break
            else:
                break
        for u in path:
            color[u] = 2

    sys.stdout.write(str(changed + extra) + "\n")

main()