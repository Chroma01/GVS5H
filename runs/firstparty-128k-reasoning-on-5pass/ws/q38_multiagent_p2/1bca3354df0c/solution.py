import sys


def build_table():
    # type indices: 0 = I, 1 = M, 2 = O, 3 = E
    trans = [[None] * 4 for _ in range(4)]
    trans[0][0] = [(2, 0)]                 # I + I -> O, d = 0
    trans[0][1] = [(2, 0), (3, 1)]         # I + M -> O d0 or E d1
    trans[0][2] = [(1, 0)]                 # I + O -> M, d = 0
    trans[0][3] = [(1, 1)]                 # I + E -> M, d = 1
    trans[1][1] = [(2, 0), (3, 1)]         # M + M -> O d0 or E d1
    trans[1][2] = [(1, 0)]                 # M + O -> M, d = 0
    trans[1][3] = [(1, 1)]                 # M + E -> M, d = 1
    trans[2][2] = [(3, 1)]                 # O + O -> E, d = 1
    trans[2][3] = [(2, 1)]                 # O + E -> O, d = 1
    trans[3][3] = [(3, 1)]                 # E + E -> E, d = 1

    win = [False] * 512
    states = []
    for i in range(4):
        for m in range(4):
            for o in range(4):
                for e in range(4):
                    s = i + m + o + e
                    states.append((s, 0, i, m, o, e))
                    states.append((s, 1, i, m, o, e))

    # Merges strictly decrease the sum of residues.
    # For the same sum, p = 0 must be computed before p = 1.
    states.sort(key=lambda x: (x[0], x[1]))

    def idx(i, m, o, e, p):
        return (((i * 4 + m) * 4 + o) * 4 + e) * 2 + p

    for s, p, i, m, o, e in states:
        cnt = [i, m, o, e]
        w = False

        # p = 1 means an odd positive number of internal waiting moves.
        # An even positive number is equivalent to zero, so p = 0 has no internal move.
        if p == 1 and not win[idx(i, m, o, e, 0)]:
            w = True

        if not w:
            for a in range(4):
                if cnt[a] == 0:
                    continue
                for b in range(a, 4):
                    if a == b:
                        if cnt[a] < 2:
                            continue
                    else:
                        if cnt[b] == 0:
                            continue

                    for r, d in trans[a][b]:
                        nc = cnt[:]
                        nc[a] -= 1
                        nc[b] -= 1
                        nc[r] = (nc[r] + 1) % 4
                        if not win[idx(nc[0], nc[1], nc[2], nc[3], p ^ d)]:
                            w = True
                            break
                    if w:
                        break
                if w:
                    break

        win[idx(i, m, o, e, p)] = w

    return win


WIN = build_table()


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    edge_count = data[1]

    # If N is odd, every terminal complete bipartite graph has an even number of edges.
    if N % 2 == 1:
        print("Aoki" if (edge_count & 1) else "Takahashi")
        return

    adj = [[] for _ in range(N)]
    pos = 2
    for _ in range(edge_count):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N
    cnt = [0, 0, 0, 0]  # I, M, O, E

    for s in range(N):
        if color[s] != -1:
            continue

        color[s] = 0
        size = [1, 0]
        stack = [s]

        while stack:
            v = stack.pop()
            cv = color[v]
            for to in adj[v]:
                if color[to] == -1:
                    color[to] = cv ^ 1
                    size[color[to]] += 1
                    stack.append(to)

        a, b = size
        if a + b == 1:
            cnt[0] += 1  # isolated vertex
        elif (a & 1) == 0 and (b & 1) == 0:
            cnt[3] += 1  # even-even
        elif (a & 1) == 1 and (b & 1) == 1:
            cnt[2] += 1  # odd-odd
        else:
            cnt[1] += 1  # mixed non-isolated

    i = cnt[0] % 4
    m = cnt[1] % 4
    o = cnt[2] % 4
    e = cnt[3] % 4

    # Parity of missing internal edges:
    # a*b is odd exactly for odd-odd components.
    p = (cnt[2] & 1) ^ (edge_count & 1)

    state = (((i * 4 + m) * 4 + o) * 4 + e) * 2 + p
    print("Aoki" if WIN[state] else "Takahashi")


if __name__ == "__main__":
    solve()