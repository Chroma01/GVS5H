import sys

sys.setrecursionlimit(1_000_000)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    edges = [(data[i], data[i + 1]) for i in range(2, 2 + 2 * M, 2)]

    # Odd N: every terminal K_{A,B} has A+B odd, so AB is even.
    # Hence the number of moves is AB-M and its parity is just M mod 2.
    if N & 1:
        print("Aoki" if (M & 1) else "Takahashi")
        return

    parent = list(range(N + 1))
    diff = [0] * (N + 1)      # parity to parent: color[x] xor color[parent[x]]
    usz = [1] * (N + 1)

    def find(x):
        if parent[x] == x:
            return x
        r = find(parent[x])
        diff[x] ^= diff[parent[x]]
        parent[x] = r
        return r

    def union(u, v):
        ru, rv = find(u), find(v)
        if ru == rv:
            return
        du, dv = diff[u], diff[v]
        if usz[ru] < usz[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        diff[rv] = du ^ dv ^ 1   # force color[u] != color[v]
        usz[ru] += usz[rv]

    for u, v in edges:
        union(u, v)

    sz = [0] * (N + 1)
    c0 = [0] * (N + 1)
    ec = [0] * (N + 1)

    for v in range(1, N + 1):
        r = find(v)
        sz[r] += 1
        if diff[v] == 0:
            c0[r] += 1
    for u, _ in edges:
        ec[find(u)] += 1

    odd_components = 0       # k: connected components with odd vertex count
    flexible_odd = 0         # o: odd-sized components that are not isolated vertices
    fills_parity = 0         # sum over components of (a*b - edges_in_component), mod 2

    for r in range(1, N + 1):
        if sz[r] == 0:
            continue
        a = min(c0[r], sz[r] - c0[r])
        b = max(c0[r], sz[r] - c0[r])
        f = a * b - ec[r]
        fills_parity ^= (f & 1)
        if sz[r] & 1:
            odd_components += 1
            if a > 0:          # an isolated vertex has (a,b)=(0,1)
                flexible_odd += 1

    k = odd_components
    o = flexible_odd

    if o == 1 or o == 2:
        # The first player immediately makes the last free-choice merge
        # (O+I for o=1, O+O for o=2) and chooses the final color parity.
        win = True
    elif o == 0:
        # Only isolates are odd; they are forced to pair up.
        win = ((fills_parity + (k // 2)) & 1) == 1
    else:
        # o >= 3: touching a flexible odd component hands the win to the
        # opponent, so the game is decided by the parity of all ordinary
        # moves: initial edges plus the forced pairing of odd components.
        win = (((M & 1) + (k // 2)) & 1) == 1

    print("Aoki" if win else "Takahashi")


main()