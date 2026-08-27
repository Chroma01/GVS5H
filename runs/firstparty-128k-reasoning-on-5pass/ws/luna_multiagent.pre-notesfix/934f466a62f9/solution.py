import sys


def solve_case(n, k, cakes):
    m = 2 * k

    mx = [0] * n
    arg = [0] * n

    for i, vals in enumerate(cakes):
        c = 0
        if vals[1] > vals[c]:
            c = 1
        if vals[2] > vals[c]:
            c = 2
        mx[i] = vals[c]
        arg[i] = c

    order = sorted(range(n), key=lambda i: mx[i], reverse=True)
    selected_list = order[:m]
    unselected_list = order[m:]

    base = sum(mx[i] for i in selected_list)

    parity = 0
    selected_classes = [[] for _ in range(3)]
    for i in selected_list:
        c = arg[i]
        parity ^= 1 << c
        selected_classes[c].append(i)

    best_unsel = []
    for c in range(3):
        ids = sorted(
            unselected_list,
            key=lambda i: cakes[i][c],
            reverse=True
        )
        best_unsel.append(ids[:4])

    best_sel_by_class = []
    for c in range(3):
        ids = sorted(selected_classes[c], key=lambda i: mx[i])
        best_sel_by_class.append(ids[:4])

    operations = []

    # Reassign one selected cake from its baseline coordinate a to b.
    for a in range(3):
        ids = selected_classes[a]
        for b in range(3):
            if a == b:
                continue

            candidates = sorted(
                ids,
                key=lambda i: mx[i] - cakes[i][b]
            )[:4]

            delta = (1 << a) ^ (1 << b)
            for i in candidates:
                loss = mx[i] - cakes[i][b]
                operations.append((loss, delta, 1 << i))

    # Replace one selected cake from baseline class a by one unselected cake,
    # assigning the new cake to coordinate b.
    for a in range(3):
        for b in range(3):
            delta = (1 << a) ^ (1 << b)
            if delta == 0:
                continue

            for i in best_sel_by_class[a]:
                for j in best_unsel[b]:
                    loss = mx[i] - cakes[j][b]
                    operations.append(
                        (loss, delta, (1 << i) | (1 << j))
                    )

    q = len(operations)

    best_loss = 0 if parity == 0 else None

    for loss, delta, _ in operations:
        if delta == parity:
            if best_loss is None or loss < best_loss:
                best_loss = loss

    # Group operations by parity and sort by loss.
    grouped = [[] for _ in range(8)]
    for idx, (loss, delta, mask) in enumerate(operations):
        grouped[delta].append((loss, idx, mask))

    for p in range(8):
        grouped[p].sort()

    ranked_losses = [[] for _ in range(8)]
    for p in range(8):
        ranked_losses[p] = [item[0] for item in grouped[p]]

    # Build globally indexed conflict bitsets.
    # Bit j of conflict_global[i] is set iff operations i and j
    # use at least one common cake.
    conflict_by_cake = {}
    for idx, (_, _, mask) in enumerate(operations):
        bit = 1 << idx
        x = mask
        while x:
            low = x & -x
            cake_id = low.bit_length() - 1
            conflict_by_cake[cake_id] = (
                conflict_by_cake.get(cake_id, 0) | bit
            )
            x ^= low

    conflict_global = [0] * q
    for idx, (_, _, mask) in enumerate(operations):
        conflict = 0
        x = mask
        while x:
            low = x & -x
            cake_id = low.bit_length() - 1
            conflict |= conflict_by_cake[cake_id]
            x ^= low
        conflict_global[idx] = conflict

    # conflict_local[p][i] is a bitset in the local ordering of group p.
    # It contains all operations of parity p conflicting with operation i.
    conflict_local = [[0] * q for _ in range(8)]
    for p in range(8):
        arr = grouped[p]
        for pos, (_, idx, _) in enumerate(arr):
            bit = 1 << pos
            for i in range(q):
                if conflict_global[i] & (1 << idx):
                    conflict_local[p][i] |= bit

    # suffix[p][j] contains group-p operations whose global index is > j.
    # Bits use the local ordering of grouped[p].
    suffix = [[0] * q for _ in range(8)]
    for p in range(8):
        arr = grouped[p]
        cur = 0
        pos = len(arr) - 1

        for j in range(q - 1, -1, -1):
            while pos >= 0 and arr[pos][1] > j:
                cur |= 1 << pos
                pos -= 1
            suffix[p][j] = cur

    # Enumerate all pairs, and for each pair obtain the cheapest compatible
    # third operation with the required parity.
    for i in range(q):
        loss_i, delta_i, mask_i = operations[i]

        for j in range(i + 1, q):
            loss_j, delta_j, mask_j = operations[j]

            if mask_i & mask_j:
                continue

            pair_delta = delta_i ^ delta_j
            pair_loss = loss_i + loss_j

            if pair_delta == parity:
                if best_loss is None or pair_loss < best_loss:
                    best_loss = pair_loss

            need = parity ^ pair_delta
            candidates = suffix[need][j]

            # These bitsets are both expressed in the same local ordering
            # of group `need`.
            forbidden = (
                conflict_local[need][i] |
                conflict_local[need][j]
            )
            candidates &= ~forbidden

            if candidates:
                low = candidates & -candidates
                pos = low.bit_length() - 1
                total_loss = pair_loss + ranked_losses[need][pos]
                if best_loss is None or total_loss < best_loss:
                    best_loss = total_loss

    return base - best_loss


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