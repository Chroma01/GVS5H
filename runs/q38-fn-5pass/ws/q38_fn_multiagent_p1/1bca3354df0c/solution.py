import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N

    # K: number of connected components whose total vertex count is odd.
    # G: XOR/parity of even-sized components whose two bipartition sides are both odd.
    odd_components = 0
    g = 0

    for start in range(N):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]
        cnt0 = 1
        cnt1 = 0

        while stack:
            v = stack.pop()
            cv = color[v]
            for to in adj[v]:
                if color[to] == -1:
                    nc = cv ^ 1
                    color[to] = nc
                    if nc == 0:
                        cnt0 += 1
                    else:
                        cnt1 += 1
                    stack.append(to)

        size = cnt0 + cnt1
        if size & 1:
            odd_components += 1
        else:
            if (cnt0 & 1) and (cnt1 & 1):
                g ^= 1

    if N & 1:
        first_wins = (M & 1) == 1
    else:
        if odd_components == 0:
            first_wins = ((M & 1) ^ g) == 1
        elif odd_components == 2:
            first_wins = True
        else:
            first_wins = (M & 1) == 1

    sys.stdout.write("Aoki\n" if first_wins else "Takahashi\n")


if __name__ == "__main__":
    main()