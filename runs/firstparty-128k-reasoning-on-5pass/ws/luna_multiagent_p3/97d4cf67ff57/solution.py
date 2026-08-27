import sys


def solve() -> None:
    input = sys.stdin.buffer.readline
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n
    parent[0] = n
    order = [0]

    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    branch = [0] * n
    good = [-10**18] * n
    answer = -1

    for u in reversed(order):
        best = []
        best_good_child = -10**18

        for v in graph[u]:
            if v == parent[u]:
                continue

            x = branch[v]
            if len(best) < 4:
                best.append(x)
                best.sort(reverse=True)
            elif x > best[-1]:
                best[-1] = x
                best.sort(reverse=True)

            if good[v] > best_good_child:
                best_good_child = good[v]

        branch[u] = 1
        if len(best) >= 3:
            degree_four_branch = 1 + best[0] + best[1] + best[2]
            branch[u] = max(branch[u], degree_four_branch)
            good[u] = degree_four_branch

        if len(best) >= 4:
            answer = max(answer, 1 + best[0] + best[1] + best[2] + best[3])

        if best_good_child > 0:
            answer = max(answer, 1 + best_good_child)

    print(answer)


if __name__ == "__main__":
    solve()