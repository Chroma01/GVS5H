import sys


def candidate_from_adj(N, adj, M):
    # Odd N: every terminal complete bipartite graph has an even number of edges.
    if N & 1:
        return 'Aoki' if (M & 1) else 'Takahashi'

    color = [-1] * N
    o = 0          # total number of odd-size components (including isolated vertices)
    i = 0          # number of isolated vertices
    b = 0          # number of even components with both color classes odd (E1)

    for s in range(N):
        if color[s] != -1:
            continue

        color[s] = 0
        stack = [s]
        c0 = 1
        c1 = 0

        while stack:
            v = stack.pop()
            cv = color[v]
            for to in adj[v]:
                if color[to] == -1:
                    color[to] = cv ^ 1
                    if color[to] == 0:
                        c0 += 1
                    else:
                        c1 += 1
                    stack.append(to)

        size = c0 + c1
        if size & 1:
            o += 1
            if size == 1:
                i += 1
        else:
            if (c0 & 1) and (c1 & 1):
                b += 1

    # P = parity of the number of currently missing internal edges.
    # For a component, a*b is odd iff it is of type E1.
    P = (b & 1) ^ (M & 1)

    # Corrected even-N classification:
    # H (always Aoki): i == o-2 or i == o-1
    # i == o: Aoki iff P ^ ((o//2)&1) == 1
    # i < o-2: Aoki iff P ^ (b&1) == 1  (equivalently, M is odd)
    if i == o - 2 or i == o - 1:
        return 'Aoki'

    if i == o:
        return 'Aoki' if ((P ^ ((o // 2) & 1)) == 1) else 'Takahashi'

    return 'Aoki' if ((P ^ (b & 1)) == 1) else 'Takahashi'


def _edge_index(N):
    mat = [[-1] * N for _ in range(N)]
    idx = 0
    for a in range(N):
        for c in range(a + 1, N):
            mat[a][c] = mat[c][a] = idx
            idx += 1
    return mat


def _incident(N, mat):
    inc = [[] for _ in range(N)]
    for a in range(N):
        for c in range(a + 1, N):
            bit = mat[a][c]
            inc[a].append((c, bit))
            inc[c].append((a, bit))
    return inc


def _is_bipartite_mask(mask, N, inc):
    color = [-1] * N
    for s in range(N):
        if color[s] != -1:
            continue

        color[s] = 0
        stack = [s]

        while stack:
            v = stack.pop()
            cv = color[v]
            for u, bit in inc[v]:
                if (mask >> bit) & 1:
                    if color[u] == -1:
                        color[u] = cv ^ 1
                        stack.append(u)
                    elif color[u] == cv:
                        return False
    return True


def _adj_from_mask(N, mask, mat):
    adj = [[] for _ in range(N)]
    for a in range(N):
        for c in range(a + 1, N):
            if (mask >> mat[a][c]) & 1:
                adj[a].append(c)
                adj[c].append(a)
    return adj


def run_validation():
    mismatches = []

    for N in range(1, 7):
        E = N * (N - 1) // 2
        mat = _edge_index(N)
        inc = _incident(N, mat)
        size = 1 << E

        bip = [False] * size
        for mask in range(size):
            bip[mask] = _is_bipartite_mask(mask, N, inc)

        win = [False] * size
        for mask in range(size - 1, -1, -1):
            if not bip[mask]:
                continue

            for bit in range(E):
                if (mask >> bit) & 1:
                    continue
                nm = mask | (1 << bit)
                if bip[nm] and not win[nm]:
                    win[mask] = True
                    break

        for mask in range(size):
            if not bip[mask]:
                continue

            adj = _adj_from_mask(N, mask, mat)
            cand = candidate_from_adj(N, adj, mask.bit_count())
            brute = 'Aoki' if win[mask] else 'Takahashi'

            if cand != brute:
                mismatches.append((N, mask, cand, brute))
                if len(mismatches) >= 20:
                    break

        if len(mismatches) >= 20:
            break

    if not mismatches:
        print("no mismatches for N<=6")
    else:
        print(f"{len(mismatches)} mismatches")
        for N, mask, cand, brute in mismatches:
            print(f"N={N} mask={mask} candidate={cand} brute={brute}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--validate':
        run_validation()
        return

    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    adj = [[] for _ in range(N)]
    idx = 2
    for _ in range(M):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    print(candidate_from_adj(N, adj, M))


if __name__ == '__main__':
    main()