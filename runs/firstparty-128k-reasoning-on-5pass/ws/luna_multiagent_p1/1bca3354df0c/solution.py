import sys


def solve() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * n
    components = []

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]
        cnt0 = cnt1 = 0

        while stack:
            v = stack.pop()
            if color[v] == 0:
                cnt0 += 1
            else:
                cnt1 += 1

            for to in adj[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    stack.append(to)

        components.append((cnt0, cnt1))

    c = len(components)
    has_odd_component = any((a + b) % 2 == 1 for a, b in components)

    # If there are at least three components and the final parity can vary
    # with the orientations, minimax reduces to the parity of the current
    # number of edges.
    if c >= 3 and n % 2 == 0 and has_odd_component:
        print("Aoki" if m % 2 == 1 else "Takahashi")
        return

    # With exactly two components, the player who merges them can choose
    # either relative orientation. Aoki wins iff one orientation leaves an
    # odd number of moves.
    if c == 2:
        a, b = components[0]
        x, y = components[1]

        terminal1 = (a + x) * (b + y)
        terminal2 = (a + y) * (b + x)

        if (terminal1 - m) % 2 == 1 or (terminal2 - m) % 2 == 1:
            print("Aoki")
        else:
            print("Takahashi")
        return

    # In all remaining cases, every maximal play has the same parity.
    side = sum(a for a, _ in components)
    terminal_edges = side * (n - side)
    print("Aoki" if (terminal_edges - m) % 2 == 1 else "Takahashi")


if __name__ == "__main__":
    solve()