import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N]
    B = data[1 + N:1 + 2 * N]

    cntA = {}
    cntB = {}
    nA = 0
    nB = 0
    maxKnown = -1

    for x in A:
        if x != -1:
            nA += 1
            cntA[x] = cntA.get(x, 0) + 1
            if x > maxKnown:
                maxKnown = x

    for x in B:
        if x != -1:
            nB += 1
            cntB[x] = cntB.get(x, 0) + 1
            if x > maxKnown:
                maxKnown = x

    # Minimum number of known-known pairs that must be made.
    L = nA + nB - N

    # If no known-known pair is needed, or only one is needed, it is always possible.
    # For L == 1, both sides have at least one known value; pair the global maximum
    # with any known value from the other side.
    if L <= 1:
        sys.stdout.write("Yes\n")
        return

    # Quick check: one value class pair alone can provide L pairs.
    maxA_big = -1
    for a, c in cntA.items():
        if c >= L and a > maxA_big:
            maxA_big = a

    maxB_big = -1
    for b, c in cntB.items():
        if c >= L and b > maxB_big:
            maxB_big = b

    if maxA_big >= 0 and maxB_big >= 0 and maxA_big + maxB_big >= maxKnown:
        sys.stdout.write("Yes\n")
        return

    maxA = max(cntA) if cntA else -1
    maxB = max(cntB) if cntB else -1

    if maxA < 0 or maxB < 0:
        sys.stdout.write("No\n")
        return

    # Values that cannot form any valid known-known pair with sum >= maxKnown
    # cannot participate in the required matching.
    A_items = [(a, c) for a, c in cntA.items() if a + maxB >= maxKnown]
    B_items = [(b, c) for b, c in cntB.items() if b + maxA >= maxKnown]

    if not A_items or not B_items:
        sys.stdout.write("No\n")
        return

    A_items.sort()
    B_items.sort()

    # Use the smaller side as the outer loop.  This also gives Timsort fewer,
    # longer sorted runs when generating pair sums.
    if len(A_items) <= len(B_items):
        outer = A_items
        inner = B_items
    else:
        outer = B_items
        inner = A_items

    mk = maxKnown

    # If one side has all remaining frequencies equal to 1, every distinct value
    # pair contributes weight 1.  Also, for L == 2, if the quick check failed,
    # no valid pair can have weight >= 2, so all valid weights are 1.
    unit_weight = (
        L == 2
        or all(c == 1 for _, c in A_items)
        or all(c == 1 for _, c in B_items)
    )

    if unit_weight:
        outer_vals = [x for x, _ in outer]
        inner_vals = [y for y, _ in inner]

        arr = [
            s
            for x in outer_vals
            for y in inner_vals
            if (s := x + y) >= mk
        ]

        if len(arr) < L:
            sys.stdout.write("No\n")
            return

        arr.sort()

        it = iter(arr)
        try:
            prev = next(it)
        except StopIteration:
            sys.stdout.write("No\n")
            return

        cnt = 1
        target = L
        for s in it:
            if s == prev:
                cnt += 1
                if cnt >= target:
                    sys.stdout.write("Yes\n")
                    return
            else:
                prev = s
                cnt = 1

        sys.stdout.write("No\n")
        return

    # General case: encode (sum, weight) into one integer.
    # weight <= N, so this many low bits are enough.
    SHIFT = max(1, (N + 1).bit_length())
    MASK = (1 << SHIFT) - 1
    sh = SHIFT

    arr = [
        ((s << sh) | (cx if cx < cy else cy))
        for x, cx in outer
        for y, cy in inner
        if (s := x + y) >= mk
    ]

    # With the quick check already done, a single valid value-pair cannot reach L.
    if len(arr) < 2:
        sys.stdout.write("No\n")
        return

    arr.sort()

    target = L
    mask = MASK
    prev_sum = -1
    total = 0

    for code in arr:
        s = code >> sh
        if s != prev_sum:
            prev_sum = s
            total = 0

        total += code & mask
        if total >= target:
            sys.stdout.write("Yes\n")
            return

    sys.stdout.write("No\n")


if __name__ == "__main__":
    solve()