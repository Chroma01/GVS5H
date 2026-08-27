import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    answers = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        length = 2 * k

        values = []
        best = []
        arg = []

        for i in range(n):
            x = next(it)
            y = next(it)
            z = next(it)
            v = (x, y, z)

            c = 0
            if y > v[c]:
                c = 1
            if z > v[c]:
                c = 2

            values.append(v)
            best.append(v[c])
            arg.append(c)

        order = sorted(range(n), key=lambda i: best[i], reverse=True)
        selected = [False] * n
        for i in order[:length]:
            selected[i] = True

        boundary = order[length - 1]
        base_sum = sum(best[i] for i in order[:length])

        parity = 0
        for i in order[:length]:
            parity ^= 1 << arg[i]

        selected_lists = [[], [], []]
        unselected_lists = [[], [], []]

        for i in range(n):
            c = arg[i]
            if selected[i]:
                selected_lists[c].append((best[i], i))
            else:
                unselected_lists[c].append((best[i], i))

        for c in range(3):
            selected_lists[c].sort()
            unselected_lists[c].sort(reverse=True)

        if parity == 0:
            answer = base_sum
        else:
            answer = -1

            odd = [c for c in range(3) if (parity >> c) & 1]
            r, s = odd

            # No reassignment: exchange one selected cake and one
            # unselected cake between the two odd coordinate classes.
            for from_c, to_c in ((r, s), (s, r)):
                if selected_lists[from_c] and unselected_lists[to_c]:
                    take = selected_lists[from_c][0][0]
                    give = unselected_lists[to_c][0][0]
                    answer = max(answer, base_sum - take + give)

            def selected_min(c, mandatory, outside_i, removed):
                candidates = []

                for value, idx in selected_lists[c][:3]:
                    if idx != mandatory and idx != removed:
                        candidates.append(value)

                if outside_i is not None and arg[outside_i] == c:
                    candidates.append(best[outside_i])

                return min(candidates) if candidates else None

            def unselected_max(c, outside_i, removed):
                candidates = []

                for value, idx in unselected_lists[c][:3]:
                    if idx != outside_i:
                        candidates.append(value)

                if outside_i is not None and removed is not None:
                    if arg[removed] == c:
                        candidates.append(best[removed])

                return max(candidates) if candidates else None

            for i in range(n):
                a = arg[i]

                if selected[i]:
                    outside_i = None
                    removed = None
                    subset_sum = base_sum
                    subset_parity = parity
                else:
                    outside_i = i
                    removed = boundary
                    subset_sum = base_sum - best[boundary] + best[i]
                    subset_parity = parity ^ (1 << arg[removed]) ^ (1 << arg[outside_i])

                for b in range(3):
                    if b == a:
                        continue

                    target_parity = (1 << a) | (1 << b)
                    mismatch = subset_parity ^ target_parity
                    reassignment_loss = best[i] - values[i][b]

                    if mismatch == 0:
                        answer = max(answer, subset_sum - reassignment_loss)
                        continue

                    bits = [c for c in range(3) if (mismatch >> c) & 1]
                    if len(bits) != 2:
                        continue

                    r, s = bits
                    for from_c, to_c in ((r, s), (s, r)):
                        take = selected_min(from_c, i, outside_i, removed)
                        give = unselected_max(to_c, outside_i, removed)

                        if take is not None and give is not None:
                            candidate = (
                                subset_sum
                                - take
                                + give
                                - reassignment_loss
                            )
                            answer = max(answer, candidate)

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()