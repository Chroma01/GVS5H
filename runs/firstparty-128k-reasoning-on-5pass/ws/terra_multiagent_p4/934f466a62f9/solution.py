import sys


def solve_case(n, k, cakes):
    m = 2 * k

    best_value = [0] * n
    base_label = [0] * n
    for i, (x, y, z) in enumerate(cakes):
        if x >= y and x >= z:
            best_value[i] = x
            base_label[i] = 0
        elif y >= z:
            best_value[i] = y
            base_label[i] = 1
        else:
            best_value[i] = z
            base_label[i] = 2

    order = sorted(range(n), key=lambda i: best_value[i], reverse=True)

    selected = [False] * n
    selected_groups = [[] for _ in range(3)]
    base_sum = 0

    for i in order[:m]:
        selected[i] = True
        selected_groups[base_label[i]].append(i)
        base_sum += best_value[i]

    unselected = [i for i in range(n) if not selected[i]]

    odd = [p for p in range(3) if len(selected_groups[p]) & 1]
    if not odd:
        return base_sum

    a, b = odd
    c = 3 - a - b

    # For every baseline source label, retain cakes cheapest to remove.
    # Three are more than sufficient: at most one cake can be forbidden
    # by compatibility with the other retained operation.
    source_best = [
        sorted(selected_groups[p], key=lambda i: best_value[i])[:3]
        for p in range(3)
    ]

    # For every destination label, retain cakes most valuable to insert.
    destination_best = [
        sorted(unselected, key=lambda i, q=q: cakes[i][q], reverse=True)[:3]
        for q in range(3)
    ]

    # For each directed relabel transition, retain the cheapest relabels.
    relabel_best = [[None] * 3 for _ in range(3)]
    for p in range(3):
        for q in range(3):
            if p == q:
                relabel_best[p][q] = []
            else:
                relabel_best[p][q] = sorted(
                    selected_groups[p],
                    key=lambda i, q=q: best_value[i] - cakes[i][q]
                )[:3]

    edge_cache = {}

    def edge_operations(p, q):
        """
        Return retained operations whose parity effect toggles labels p and q.

        Tuple format: (loss, selected_source_id, inserted_unselected_id).
        For relabels, inserted_unselected_id is -1.
        """
        key = (p, q) if p < q else (q, p)
        if key in edge_cache:
            return edge_cache[key]

        ops = []
        for src, dst in ((p, q), (q, p)):
            for i in relabel_best[src][dst]:
                ops.append((best_value[i] - cakes[i][dst], i, -1))

            for i in source_best[src]:
                for j in destination_best[dst]:
                    ops.append((best_value[i] - cakes[j][dst], i, j))

        edge_cache[key] = ops
        return ops

    # A one-edge correction directly joins the two odd labels.
    correction = min(loss for loss, _, _ in edge_operations(a, b))

    # The only other simple path over three labels is a-c-b.
    left_ops = edge_operations(a, c)
    right_ops = edge_operations(c, b)

    for loss1, s1, u1 in left_ops:
        for loss2, s2, u2 in right_ops:
            if s1 == s2:
                continue
            if u1 != -1 and u1 == u2:
                continue
            correction = min(correction, loss1 + loss2)

    return base_sum - correction


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    ans = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = [(next(it), next(it), next(it)) for _ in range(n)]
        ans.append(str(solve_case(n, k, cakes)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()