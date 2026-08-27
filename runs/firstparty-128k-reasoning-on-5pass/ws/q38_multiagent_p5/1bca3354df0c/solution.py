import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    adj = [[] for _ in range(N)]

    idx = 2
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    m = M & 1

    # For odd N, every maximal final complete bipartite graph has an even
    # number of edges, so the parity of the total number of moves is M mod 2.
    if N & 1:
        print("Aoki" if m else "Takahashi")
        return

    color = [-1] * N
    odd_components = 0
    isolated = 0
    b = 0  # parity of components whose two bipartition sides are both odd

    for start in range(N):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]
        c0 = 1
        c1 = 0

        while stack:
            x = stack.pop()
            nxt_color = color[x] ^ 1
            for y in adj[x]:
                if color[y] == -1:
                    color[y] = nxt_color
                    if nxt_color == 0:
                        c0 += 1
                    else:
                        c1 += 1
                    stack.append(y)

        size = c0 + c1
        if size & 1:
            odd_components += 1
            if size == 1:
                isolated += 1
        else:
            if (c0 & 1) and (c1 & 1):
                b ^= 1

    if isolated == odd_components:
        first_loses = (m == (b ^ ((odd_components // 2) & 1)))
    elif isolated >= odd_components - 2:
        first_loses = False
    else:
        first_loses = (m == 0)

    print("Takahashi" if first_loses else "Aoki")


if __name__ == "__main__":
    main()