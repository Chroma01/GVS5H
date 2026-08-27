import sys

NEG = -(10**30)
INF = 10**30


def regular_sequence(vals, parity):
    n = len(vals)
    if parity > n:
        return None

    base = sum(vals[:parity])
    marginals = []
    for i in range(parity, n - 1, 2):
        marginals.append(vals[i] + vals[i + 1])

    return base, marginals, parity


def special_one_sequence(items, destination, parity):
    n = len(items)
    if n == 0:
        return None

    baseline = [item[0] for item in items]
    target = [item[destination + 1] for item in items]

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + baseline[i]

    prefix_min_loss = [INF] * (n + 1)
    for i in range(n):
        loss = baseline[i] - target[i]
        prefix_min_loss[i + 1] = min(prefix_min_loss[i], loss)

    suffix_max_target = [NEG] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_max_target[i] = max(suffix_max_target[i + 1], target[i])

    best = [NEG] * (n + 1)
    for q in range(1, n + 1):
        value = prefix[q] - prefix_min_loss[q]

        if q < n:
            value = max(value, prefix[q - 1] + suffix_max_target[q])

        best[q] = value

    start = 1 if parity else 2
    if start > n or best[start] == NEG:
        return None

    marginals = []
    for q in range(start, n - 1, 2):
        marginals.append(best[q + 2] - best[q])

    return best[start], marginals, start


def special_two_sequence(items, destination_a, destination_b):
    n = len(items)
    if n < 2:
        return None

    baseline = [item[0] for item in items]
    gain_a = [
        item[destination_a + 1] - baseline[i]
        for i, item in enumerate(items)
    ]
    gain_b = [
        item[destination_b + 1] - baseline[i]
        for i, item in enumerate(items)
    ]

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + baseline[i]

    suffix_a1 = [NEG] * (n + 1)
    suffix_a2 = [NEG] * (n + 1)
    suffix_ai = [-1] * (n + 1)

    suffix_b1 = [NEG] * (n + 1)
    suffix_b2 = [NEG] * (n + 1)
    suffix_bi = [-1] * (n + 1)

    for i in range(n - 1, -1, -1):
        candidates = [
            (gain_a[i], i),
            (suffix_a1[i + 1], suffix_ai[i + 1]),
            (suffix_a2[i + 1], -2),
        ]
        candidates.sort(reverse=True)

        chosen = []
        used = set()
        for value, index in candidates:
            if index >= 0 and index not in used:
                chosen.append((value, index))
                used.add(index)
        while len(chosen) < 2:
            chosen.append((NEG, -1))

        suffix_a1[i], suffix_ai[i] = chosen[0]
        suffix_a2[i] = chosen[1][0]

        candidates = [
            (gain_b[i], i),
            (suffix_b1[i + 1], suffix_bi[i + 1]),
            (suffix_b2[i + 1], -2),
        ]
        candidates.sort(reverse=True)

        chosen = []
        used = set()
        for value, index in candidates:
            if index >= 0 and index not in used:
                chosen.append((value, index))
                used.add(index)
        while len(chosen) < 2:
            chosen.append((NEG, -1))

        suffix_b1[i], suffix_bi[i] = chosen[0]
        suffix_b2[i] = chosen[1][0]

    best = [NEG] * (n + 1)
    best_a = (NEG, -1)
    best_b = (NEG, -1)
    best_pair = NEG

    for q in range(2, n + 1, 2):
        r = q - 2

        if r > 0:
            i = r - 1
            ga = gain_a[i]
            gb = gain_b[i]

            if best_b[1] != i:
                best_pair = max(best_pair, ga + best_b[0])
            if best_a[1] != i:
                best_pair = max(best_pair, gb + best_a[0])

            if ga > best_a[0]:
                best_a = (ga, i)
            if gb > best_b[0]:
                best_b = (gb, i)

        value = NEG

        if r >= 2:
            value = max(value, prefix[r] + best_pair)

        if r >= 1 and r < n:
            value = max(
                value,
                prefix[r] + best_a[0] + suffix_b1[r],
                prefix[r] + best_b[0] + suffix_a1[r],
            )

        if r < n:
            if suffix_ai[r] != suffix_bi[r]:
                outside = suffix_a1[r] + suffix_b1[r]
            else:
                outside = max(
                    suffix_a1[r] + suffix_b2[r],
                    suffix_b1[r] + suffix_a2[r],
                )
            value = max(value, prefix[r] + outside)

        best[q] = value

    if best[2] == NEG:
        return None

    marginals = []
    for q in range(2, n - 1, 2):
        marginals.append(best[q + 2] - best[q])

    return best[2], marginals, 2


def combine(sequences, total_count, incident):
    if any(sequence is None for sequence in sequences):
        return NEG

    for i, sequence in enumerate(sequences):
        if (sequence[2] + incident[i]) & 1:
            return NEG

    base = sum(sequence[0] for sequence in sequences)
    base_count = sum(sequence[2] for sequence in sequences)

    if total_count < base_count:
        return NEG
    if (total_count - base_count) & 1:
        return NEG

    need = (total_count - base_count) // 2
    marginals = []

    for sequence in sequences:
        marginals.extend(sequence[1])

    if need < 0 or need > len(marginals):
        return NEG

    marginals.sort(reverse=True)
    return base + sum(marginals[:need])


def solve_case(n, k, cakes):
    total = 2 * k
    groups = [[], [], []]

    for x, y, z in cakes:
        values = (x, y, z)
        owner = values.index(max(values))
        groups[owner].append((values[owner], x, y, z))

    for group in groups:
        group.sort(reverse=True)

    baseline_values = [
        [item[0] for item in group]
        for group in groups
    ]

    answer = combine(
        [regular_sequence(baseline_values[i], 0) for i in range(3)],
        total,
        (0, 0, 0),
    )

    for source in range(3):
        for destination in range(3):
            if source == destination:
                continue

            incident = [0, 0, 0]
            incident[source] = 1
            incident[destination] = 1

            sequences = []
            for i in range(3):
                if i == source:
                    sequences.append(
                        special_one_sequence(groups[source], destination, 1)
                    )
                elif i == destination:
                    sequences.append(regular_sequence(baseline_values[i], 1))
                else:
                    sequences.append(regular_sequence(baseline_values[i], 0))

            answer = max(answer, combine(sequences, total, tuple(incident)))

    for middle in range(3):
        first, second = [i for i in range(3) if i != middle]

        sequences = [None] * 3
        sequences[first] = special_one_sequence(groups[first], second, 1)
        sequences[middle] = special_one_sequence(groups[middle], second, 1)
        sequences[second] = regular_sequence(baseline_values[second], 0)
        answer = max(answer, combine(sequences, total, (1, 1, 2)))

        sequences = [None] * 3
        sequences[first] = regular_sequence(baseline_values[first], 1)
        sequences[middle] = regular_sequence(baseline_values[middle], 1)
        sequences[second] = special_two_sequence(
            groups[second], first, middle
        )
        answer = max(answer, combine(sequences, total, (1, 1, 2)))

        sequences = [None] * 3
        sequences[first] = special_one_sequence(groups[first], second, 1)
        sequences[middle] = regular_sequence(baseline_values[middle], 1)
        sequences[second] = special_one_sequence(groups[second], middle, 0)
        answer = max(answer, combine(sequences, total, (1, 0, 2)))

        sequences = [None] * 3
        sequences[first] = regular_sequence(baseline_values[first], 1)
        sequences[middle] = special_one_sequence(groups[middle], second, 1)
        sequences[second] = special_one_sequence(groups[second], first, 0)
        answer = max(answer, combine(sequences, total, (1, 0, 2)))

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    t = next(it)
    answers = []

    for _ in range(t):
        n = next(it)
        k = next(it)

        cakes = [
            (next(it), next(it), next(it))
            for _ in range(n)
        ]

        answers.append(str(solve_case(n, k, cakes)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()