import sys

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    # Root the original tree arbitrarily at vertex 0.
    parent = [-2] * n
    parent[0] = -1
    order = [0]

    for v in order:
        for to in graph[v]:
            if to != parent[v]:
                parent[to] = v
                order.append(to)

    neg_inf = -10**9

    # dp0[v]: maximum size of a valid selected subtree containing v,
    #          using the edge to parent[v], with no degree-4 vertex.
    # dp1[v]: same, but with at least one degree-4 vertex.
    #
    # Since v already uses its parent edge, it must select either
    # zero children (degree 1) or exactly three children (degree 4).
    dp0 = [neg_inf] * n
    dp1 = [neg_inf] * n

    answer = -1

    for v in reversed(order):
        # knap[k][f] = maximum total size of selected child branches
        # using exactly k children, with degree-4 flag f.
        knap = [[neg_inf, neg_inf] for _ in range(5)]
        knap[0][0] = 0

        for to in graph[v]:
            if to == parent[v]:
                continue

            ndp = [row[:] for row in knap]  # Do not select this child.
            for used in range(4):
                for flag in range(2):
                    if knap[used][flag] == neg_inf:
                        continue

                    if dp0[to] != neg_inf:
                        val = knap[used][flag] + dp0[to]
                        if val > ndp[used + 1][flag]:
                            ndp[used + 1][flag] = val

                    if dp1[to] != neg_inf:
                        val = knap[used][flag] + dp1[to]
                        if val > ndp[used + 1][1]:
                            ndp[used + 1][1] = val

            knap = ndp

        # Treat v as the highest selected vertex, so it has no selected
        # parent. It must have degree 1 or 4.
        # Degree 1: exactly one selected child, and that branch must already
        # contain a degree-4 vertex.
        if knap[1][1] != neg_inf:
            answer = max(answer, 1 + knap[1][1])

        # Degree 4: exactly four selected children; v itself supplies the
        # required degree-4 vertex.
        best_four = max(knap[4][0], knap[4][1])
        if best_four != neg_inf:
            answer = max(answer, 1 + best_four)

        # For a subtree attached through v's parent edge:
        # zero selected children gives a leaf and no degree-4 vertex.
        dp0[v] = 1

        # Exactly three selected children gives v degree 4.
        best_three = max(knap[3][0], knap[3][1])
        if best_three != neg_inf:
            dp1[v] = 1 + best_three

    print(answer)

if __name__ == "__main__":
    solve()