import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit_count = [0] * (n + 1)
        self.bit_sum = [0] * (n + 1)

    def add(self, i, count, value_sum):
        while i <= self.n:
            self.bit_count[i] += count
            self.bit_sum[i] += value_sum
            i += i & -i

    def query(self, i):
        count = 0
        value_sum = 0
        while i > 0:
            count += self.bit_count[i]
            value_sum += self.bit_sum[i]
            i -= i & -i
        return count, value_sum


def rank_sum_desc(values):
    values.sort(reverse=True)
    return sum((i + 1) * x for i, x in enumerate(values))


def rank_sum_asc(values):
    values.sort()
    return sum((i + 1) * x for i, x in enumerate(values))


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    must_off = []
    must_on = []
    optional = []

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            must_off.append(ci)
        elif ai == 0 and bi == 1:
            must_on.append(ci)
        elif ai == 1 and bi == 1:
            optional.append(ci)

    m = len(must_off)
    q = len(must_on)
    sum_off = sum(must_off)
    sum_on = sum(must_on)

    coords = sorted(set(c))
    pos = {x: i + 1 for i, x in enumerate(coords)}
    k = len(coords)

    off_rank_sum = rank_sum_desc(must_off[:])
    on_rank_sum = rank_sum_asc(must_on[:])

    off_tree = Fenwick(k)
    on_tree = Fenwick(k)

    off_count = 0
    for x in must_off:
        off_tree.add(pos[x], 1, x)
        off_count += 1

    on_count = 0
    on_sum = 0
    for x in must_on:
        on_tree.add(pos[x], 1, x)
        on_count += 1
        on_sum += x

    optional.sort(reverse=True)
    remaining_optional_sum = sum(optional)
    selected_sum = 0

    # t = 0:
    # OffRankSum - sum(D) + (m + q)R
    # + (q + 1)sum(U) - OnRankSum
    best = (
        off_rank_sum - sum_off
        + (q + 1) * sum_on - on_rank_sum
        + (m + q) * remaining_optional_sum
    )

    for t, x in enumerate(optional, 1):
        selected_sum += x
        remaining_optional_sum -= x
        p = pos[x]

        # Insert x into descending order.
        less_count, less_sum = off_tree.query(p - 1)
        ge_count = off_count - less_count
        off_rank_sum += x * (ge_count + 1) + less_sum
        off_tree.add(p, 1, x)
        off_count += 1

        # Insert x into ascending order.
        le_count, le_sum = on_tree.query(p)
        greater_sum = on_sum - le_sum
        on_rank_sum += x * (le_count + 1) + greater_sum
        on_tree.add(p, 1, x)
        on_count += 1
        on_sum += x

        # For T selected optional weights and R unselected optional weights:
        # OffRankSum - sum(D) - sum(T)
        # + (q+t+1)(sum(U)+sum(T)) - OnRankSum
        # + (m+q+2t)R
        total = (
            off_rank_sum - sum_off - selected_sum
            + (q + t + 1) * (sum_on + selected_sum) - on_rank_sum
            + (m + q + 2 * t) * remaining_optional_sum
        )
        if total < best:
            best = total

    print(best)


if __name__ == "__main__":
    main()