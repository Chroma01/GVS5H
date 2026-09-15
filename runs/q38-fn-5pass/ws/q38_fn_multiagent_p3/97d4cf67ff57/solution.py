import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Minimum alkane size is 5: if x >= 1 vertices have degree 4,
    # then total vertices = 3*x + 2.
    if n < 5:
        print(-1)
        return

    adj = [[] for _ in range(n)]
    idx = 1
    for _ in range(n - 1):
        a = data[idx] - 1
        b = data[idx + 1] - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)

    del data

    # Root the tree at 0 and get an order where parents appear before children.
    parent = [-1] * n
    parent[0] = -2
    order = [0]
    i = 0
    while i < len(order):
        v = order[i]
        i += 1
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            order.append(to)

    NEG = -10**18

    # present1[v]:
    #   Maximum size of a valid connected subgraph inside subtree(v),
    #   including v and the edge to its parent, and containing at least
    #   one degree-4 vertex.
    #
    # absent1[v]:
    #   Maximum size of a valid connected subgraph inside subtree(v),
    #   including v, NOT including the edge to its parent, and containing
    #   at least one degree-4 vertex.
    present1 = [NEG] * n
    absent1 = [NEG] * n

    for v in reversed(order):
        # Four largest branch values among children.
        top0 = top1 = top2 = top3 = 0
        child_count = 0

        # Maximum present1[child] among children.
        max_child_present1 = NEG

        for to in adj[v]:
            if parent[to] != v:
                continue

            p1 = present1[to]
            if p1 > max_child_present1:
                max_child_present1 = p1

            # If the edge v-to is selected, the best branch from 'to' is:
            #   - size 1 if we make 'to' a degree-1 leaf, or
            #   - present1[to] if we make 'to' degree-4 and include its subtree.
            if p1 > 1:
                val = p1
            else:
                val = 1

            # Maintain top four values.
            if val > top0:
                top3 = top2
                top2 = top1
                top1 = top0
                top0 = val
            elif val > top1:
                top3 = top2
                top2 = top1
                top1 = val
            elif val > top2:
                top3 = top2
                top2 = val
            elif val > top3:
                top3 = val

            child_count += 1

        # Parent edge present:
        # To contain a degree-4 vertex, v itself must be degree-4,
        # so it must select exactly 3 child branches.
        if child_count >= 3:
            present1[v] = 1 + top0 + top1 + top2

        # Parent edge absent:
        # v is the highest vertex of the chosen alkane.
        best = NEG

        # Case 1: v has degree 1. Then the selected child branch must
        # already contain a degree-4 vertex.
        if max_child_present1 != NEG:
            best = 1 + max_child_present1

        # Case 2: v has degree 4. Then v itself supplies the degree-4 flag,
        # and we choose the best 4 child branches.
        if child_count >= 4:
            cand = 1 + top0 + top1 + top2 + top3
            if cand > best:
                best = cand

        absent1[v] = best

    ans = max(absent1)
    print(-1 if ans < 0 else ans)


if __name__ == "__main__":
    solve()