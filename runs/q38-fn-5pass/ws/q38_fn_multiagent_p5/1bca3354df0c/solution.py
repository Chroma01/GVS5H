import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    # For odd N, every terminal complete bipartite graph has an even number
    # of edges, so the parity of the whole play is fixed by M.
    if n & 1:
        print("Aoki" if (m & 1) else "Takahashi")
        return

    adj = [[] for _ in range(n)]
    idx = 2
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * n

    odd_components = 0       # K
    isolated_vertices = 0    # z
    sum_ab_parity = 0        # XOR of (a*b mod 2) over components

    for s in range(n):
        if color[s] != -1:
            continue

        color[s] = 0
        stack = [s]
        a = 0
        b = 0

        while stack:
            u = stack.pop()
            if color[u] == 0:
                a += 1
            else:
                b += 1

            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = cu ^ 1
                    stack.append(v)

        size = a + b

        if size == 1:
            isolated_vertices += 1
        if size & 1:
            odd_components += 1

        # a*b is odd iff both color classes have odd size.
        sum_ab_parity ^= (a & 1) & (b & 1)

    # D = total number of currently missing internal legal edges, modulo 2.
    # D = (sum a_i b_i - M) mod 2.
    d_parity = sum_ab_parity ^ (m & 1)

    # y = number of non-isolated odd components.
    y = odd_components - isolated_vertices

    if y == 0:
        # Only isolated vertices are odd components.
        # The second player wins iff (z/2 + D) is even.
        first_wins = ((isolated_vertices // 2) + d_parity) & 1
    elif y <= 2:
        # With one or two non-isolated odd components, the player to move
        # can make the last "choice" merge and force a win.
        first_wins = 1
    else:
        # With at least three non-isolated odd components, the outcome is
        # exactly the parity of M.
        first_wins = m & 1

    print("Aoki" if first_wins else "Takahashi")


if __name__ == "__main__":
    solve()