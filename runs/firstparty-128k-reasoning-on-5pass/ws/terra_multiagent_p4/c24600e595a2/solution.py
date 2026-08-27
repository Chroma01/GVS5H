import sys
from bisect import bisect_left, bisect_right

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit_count = [0] * (n + 1)
        self.bit_sum = [0] * (n + 1)

    def add(self, i, count, value_sum):
        n = self.n
        while i <= n:
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


def ranked_weight_sum_desc(values):
    values.sort(reverse=True)
    return sum(v * (i + 1) for i, v in enumerate(values))


def ranked_weight_sum_asc(values):
    values.sort()
    return sum(v * (i + 1) for i, v in enumerate(values))


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    initial_sum = sum(ai * ci for ai, ci in zip(a, c))

    down = []      # mandatory 1 -> 0
    up = []        # mandatory 0 -> 1
    stable_one = []  # 1 -> 1, optionally turn off and back on

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            down.append(ci)
        elif ai == 0 and bi == 1:
            up.append(ci)
        elif ai == 1:
            stable_one.append(ci)

    coords = sorted(set(c))
    mcoord = len(coords)

    def index(v):
        return bisect_left(coords, v) + 1

    # Down phase: weights sorted decreasing.
    down_count = len(down)
    down_sum = sum(down)
    down_ranked = ranked_weight_sum_desc(down[:])

    # Up phase: weights sorted increasing.
    up_count = len(up)
    up_sum = sum(up)
    up_ranked = ranked_weight_sum_asc(up[:])

    fw_down = Fenwick(mcoord)
    fw_up = Fenwick(mcoord)

    for v in down:
        fw_down.add(index(v), 1, v)
    for v in up:
        fw_up.add(index(v), 1, v)

    def total_cost():
        # For descending down weights:
        # sum after each removal =
        # m*S - sum(weight * (m-rank+1))
        down_cost = down_count * initial_sum - (
            (down_count + 1) * down_sum - down_ranked
        )

        remaining = initial_sum - down_sum

        # For ascending up weights:
        # sum after each addition =
        # m*remaining + sum(weight * (m-rank+1))
        up_cost = up_count * remaining + (
            (up_count + 1) * up_sum - up_ranked
        )
        return down_cost + up_cost

    ans = total_cost()

    # For a fixed number of temporarily disabled stable-one positions,
    # choosing the largest weights is optimal. Add them in descending order.
    stable_one.sort(reverse=True)

    for v in stable_one:
        pos = index(v)

        # Insert into descending down order, before equal weights.
        cnt_le, sum_le = fw_down.query(pos)
        cnt_gt = down_count - cnt_le
        rank_down = cnt_gt + 1
        down_ranked += v * rank_down + sum_le
        down_count += 1
        down_sum += v
        fw_down.add(pos, 1, v)

        # Insert into ascending up order, before equal weights.
        cnt_lt, sum_lt = fw_up.query(pos - 1)
        rank_up = cnt_lt + 1
        sum_ge = up_sum - sum_lt
        up_ranked += v * rank_up + sum_ge
        up_count += 1
        up_sum += v
        fw_up.add(pos, 1, v)

        ans = min(ans, total_cost())

    print(ans)


if __name__ == "__main__":
    main()