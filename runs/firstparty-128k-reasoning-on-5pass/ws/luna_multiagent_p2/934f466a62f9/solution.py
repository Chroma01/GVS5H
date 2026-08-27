import sys

ONE_HOT = (1, 2, 4)
MASK_TO_POS = {1: 0, 2: 1, 4: 2}
NEG_INF = -10**30


def keep_best(best, key, score, index):
    first, second = best[key]
    if score > first[0]:
        best[key] = ((score, index), first)
    elif score > second[0]:
        best[key] = (first, (score, index))


def solve_case(n, k, cakes):
    m = 2 * k

    # Each cake is (dominant value, dominant mask, (X, Y, Z)).
    cakes.sort(key=lambda item: item[0], reverse=True)

    dominant = [cake[0] for cake in cakes]
    masks = [cake[1] for cake in cakes]
    values = [cake[2] for cake in cakes]

    pref_sum = [0] * (n + 1)
    pref_xor = [0] * (n + 1)
    for i in range(n):
        pref_sum[i + 1] = pref_sum[i] + dominant[i]
        pref_xor[i + 1] = pref_xor[i] ^ masks[i]

    answer = -1

    # No special cakes: choose the first m cakes with their dominant coordinates.
    if pref_xor[m] == 0:
        answer = pref_sum[m]

    # Exactly one special cake.
    q = m - 1
    base_sum = pref_sum[q]
    base_xor = pref_xor[q]

    for i in range(n):
        if i < q:
            regular_sum = base_sum - dominant[i] + dominant[q]
            regular_xor = base_xor ^ masks[i] ^ masks[q]
        else:
            regular_sum = base_sum
            regular_xor = base_xor

        if regular_xor in MASK_TO_POS:
            special_value = values[i][MASK_TO_POS[regular_xor]]
            answer = max(answer, regular_sum + special_value)

    def new_best():
        return [[(NEG_INF, -1), (NEG_INF, -1)] for _ in range(8)]

    # Exactly two special cakes.
    q = m - 2
    base_sum = pref_sum[q]
    base_xor = pref_xor[q]

    # Both specials are inside [0, q).
    inside_delta = new_best()
    for i in range(q):
        for assigned in ONE_HOT:
            delta = assigned ^ masks[i]
            gain = values[i][MASK_TO_POS[assigned]] - dominant[i]
            keep_best(inside_delta, delta, gain, i)

    target = base_xor ^ masks[q] ^ masks[q + 1]
    for key_a in range(8):
        key_b = key_a ^ target
        for gain_a, index_a in inside_delta[key_a]:
            if index_a < 0:
                continue
            for gain_b, index_b in inside_delta[key_b]:
                if index_b < 0 or index_a == index_b:
                    continue
                answer = max(
                    answer,
                    base_sum
                    + dominant[q]
                    + dominant[q + 1]
                    + gain_a
                    + gain_b,
                )

    # One special is inside [0, q), and the other is q.
    inside_delta = new_best()
    for i in range(q):
        for assigned in ONE_HOT:
            delta = assigned ^ masks[i]
            gain = values[i][MASK_TO_POS[assigned]] - dominant[i]
            keep_best(inside_delta, delta, gain, i)

    target = base_xor ^ masks[q + 1]
    for delta_i in range(8):
        assigned_q = target ^ delta_i
        if assigned_q not in MASK_TO_POS:
            continue
        value_q = values[q][MASK_TO_POS[assigned_q]]
        for gain_i, index_i in inside_delta[delta_i]:
            if index_i < 0:
                continue
            answer = max(
                answer,
                base_sum + dominant[q + 1] + gain_i + value_q,
            )

    # One special is inside [0, q), and the other is greater than q.
    outside_assigned = new_best()
    for j in range(q + 1, n):
        for assigned in ONE_HOT:
            keep_best(
                outside_assigned,
                assigned,
                values[j][MASK_TO_POS[assigned]],
                j,
            )

    target = base_xor ^ masks[q]
    for delta_i in range(8):
        assigned_j = target ^ delta_i
        if assigned_j not in MASK_TO_POS:
            continue
        for gain_i, index_i in inside_delta[delta_i]:
            if index_i < 0:
                continue
            for gain_j, index_j in outside_assigned[assigned_j]:
                if index_j < 0:
                    continue
                answer = max(
                    answer,
                    base_sum
                    + dominant[q]
                    + gain_i
                    + gain_j,
                )

    # Both specials are at least q.
    outside_assigned = new_best()
    for i in range(q, n):
        for assigned in ONE_HOT:
            keep_best(
                outside_assigned,
                assigned,
                values[i][MASK_TO_POS[assigned]],
                i,
            )

    target = base_xor
    for assigned_a in range(8):
        assigned_b = assigned_a ^ target
        for gain_a, index_a in outside_assigned[assigned_a]:
            if index_a < 0:
                continue
            for gain_b, index_b in outside_assigned[assigned_b]:
                if index_b < 0 or index_a == index_b:
                    continue
                answer = max(answer, base_sum + gain_a + gain_b)

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    answers = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = []

        for _ in range(n):
            x = next(it)
            y = next(it)
            z = next(it)

            if x >= y and x >= z:
                cakes.append((x, 1, (x, y, z)))
            elif y >= z:
                cakes.append((y, 2, (x, y, z)))
            else:
                cakes.append((z, 4, (x, y, z)))

        answers.append(str(solve_case(n, k, cakes)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()