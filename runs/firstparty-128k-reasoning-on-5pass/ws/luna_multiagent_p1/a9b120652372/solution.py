import sys


def feasible(L, x, y, gaps):
    m = len(x)
    k = len(y)
    if k > m:
        return False

    lo = [0] * k
    hi = [0] * k

    left = 0
    right = 0
    for q, target in enumerate(y):
        low_value = target - L
        high_value = target + L

        while left < m and x[left] < low_value:
            left += 1
        if right < left:
            right = left
        while right < m and x[right] <= high_value:
            right += 1

        lo[q] = left
        hi[q] = right - 1

        if lo[q] > hi[q]:
            return False

    # The first target must contain the first source piece.
    if lo[0] != 0:
        return False

    previous_cut = -1

    # Select the source-piece boundary for every transition between targets.
    # Choosing the earliest valid cut is optimal for all later targets.
    for q in range(k - 1):
        lower = previous_cut + 1
        need_next_start = lo[q + 1] - 1
        if need_next_start > lower:
            lower = need_next_start

        upper = hi[q]
        required_gap = y[q + 1] - y[q]

        cut = lower
        while cut <= upper and (
            cut >= m - 1 or gaps[cut] < required_gap
        ):
            cut += 1

        if cut > upper:
            return False
        previous_cut = cut

    # All remaining source pieces must form the last target group.
    return (
        previous_cut + 1 >= lo[-1]
        and m - 1 <= hi[-1]
    )


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    answers = []

    for _ in range(t):
        n = int(data[pos])
        a = data[pos + 1].decode()
        b = data[pos + 2].decode()
        pos += 3

        source = [i for i, ch in enumerate(a) if ch == "1"]
        target = [i for i, ch in enumerate(b) if ch == "1"]

        m = len(source)
        gaps = [source[i + 1] - source[i] for i in range(m - 1)]

        low = 0
        high = n - 1
        while low < high:
            mid = (low + high) // 2
            if feasible(mid, source, target, gaps):
                high = mid
            else:
                low = mid + 1

        if feasible(low, source, target, gaps):
            answers.append(str(low))
        else:
            answers.append("-1")

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()