import sys
sys.setrecursionlimit(1000000)


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    parent = list(range(N + 1))
    color = [0] * (N + 1)  # color relative to component root

    def find(x):
        # returns (root, color of x relative to root)
        if parent[x] == x:
            return x, 0
        r, c = find(parent[x])
        c ^= color[x]
        parent[x] = r
        color[x] = c
        return r, c

    def union(x, y):
        rx, cx = find(x)
        ry, cy = find(y)
        if rx == ry:
            return
        # make color[y] = color[x] ^ 1
        parent[ry] = rx
        color[ry] = cx ^ cy ^ 1

    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        union(u, v)

    # gather color-class sizes per component
    # comp[root] = [count_color0, count_color1]
    comp = {}
    for v in range(1, N + 1):
        r, c = find(v)
        if r not in comp:
            comp[r] = [0, 0]
        comp[r][c] += 1

    C = len(comp)
    k = 0          # number of odd-sized components
    base = 0       # sum of a_i mod 2
    singles = 0    # isolated vertices
    for (a, b) in comp.values():
        if (a + b) % 2 == 1:
            k += 1
        base = (base + a) % 2
        if a + b == 1:
            singles += 1

    # Decide winner
    if N % 2 == 1:
        # T = A*B - M, A*B always even -> T parity = M parity
        aoki = (M % 2 == 1)
    else:
        if k == 0:
            # no decisive merge possible; A parity fixed = base
            aoki = ((base + M) % 2 == 1)
        elif k == 2:
            odd_sizes = [(a, b) for (a, b) in comp.values()
                         if (a + b) % 2 == 1]
            both_single = all(a + b == 1 for (a, b) in odd_sizes)
            if both_single and C == 2:
                # only two isolated vertices: A forced odd
                aoki = ((1 + M) % 2 == 1)
            else:
                # player to move makes the last decisive merge and
                # can set A to either parity
                aoki = True
        else:
            # k >= 4: first player seizes the decisive-merge race
            aoki = True

    print("Aoki" if aoki else "Takahashi")


main()