import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # If N is odd, every terminal complete bipartite graph K_{A,B}
    # has A+B odd, hence A*B is even. The winner depends only on M.
    if N % 2 == 1:
        print("Aoki" if M % 2 == 1 else "Takahashi")
        return

    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N
    odd_components = 0
    missing_parity = 0

    for start in range(N):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]
        cnt0 = 1
        cnt1 = 0
        edge_twice = 0

        while stack:
            u = stack.pop()
            cu = color[u]

            for v in adj[u]:
                edge_twice += 1
                if color[v] == -1:
                    color[v] = cu ^ 1
                    if color[v] == 0:
                        cnt0 += 1
                    else:
                        cnt1 += 1
                    stack.append(v)

        m = edge_twice // 2
        size = cnt0 + cnt1

        if size & 1:
            odd_components += 1

        # Parity of missing internal edges in this component.
        missing_parity ^= ((cnt0 * cnt1 - m) & 1)

    if odd_components == 0:
        first_wins = (missing_parity == 1)
    elif odd_components == 2:
        first_wins = True
    else:
        first_wins = (M % 2 == 1)

    print("Aoki" if first_wins else "Takahashi")


if __name__ == "__main__":
    main()