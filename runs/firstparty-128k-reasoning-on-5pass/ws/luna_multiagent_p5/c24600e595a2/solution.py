import sys
from bisect import bisect_left, bisect_right


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, value):
        i += 1
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def prefix_sum(self, i):
        """Returns the sum over indices [0, i)."""
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result


def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    initial_cost = sum(x * y for x, y in zip(a, c))

    downs = []
    ups = []
    optional = []

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            downs.append(ci)
        elif ai == 0 and bi == 1:
            ups.append(ci)
        elif ai == 1 and bi == 1:
            optional.append(ci)

    downs.sort(reverse=True)
    ups.sort()
    optional.sort(reverse=True)

    m = len(downs)
    k = len(ups)

    sum_down = sum(downs)
    sum_up = sum(ups)

    weighted_down = sum(value * (m - i) for i, value in enumerate(downs))
    weighted_up = sum(value * (k - i) for i, value in enumerate(ups))

    all_values = sorted(set(c))
    index = {value: i for i, value in enumerate(all_values)}
    size = len(all_values)

    count_down = Fenwick(size)
    weight_down = Fenwick(size)
    count_up = Fenwick(size)
    weight_up = Fenwick(size)

    for value in downs:
        p = index[value]
        count_down.add(p, 1)
        weight_down.add(p, value)

    for value in ups:
        p = index[value]
        count_up.add(p, 1)
        weight_up.add(p, value)

    def total_cost():
        down_cost = m * initial_cost - weighted_down
        up_cost = k * (initial_cost - sum_down) + weighted_up
        return down_cost + up_cost

    answer = total_cost()

    for value in optional:
        p = index[value]

        # Insert into the descending down sequence.
        # Only weights strictly greater than value shift their coefficient.
        greater_end = bisect_right(all_values, value)
        greater_weight = (
            sum_down - weight_down.prefix_sum(greater_end)
        )
        greater_count = (
            m - count_down.prefix_sum(greater_end)
        )

        weighted_down += greater_weight + value * (m + 1 - greater_count)
        m += 1
        sum_down += value
        count_down.add(p, 1)
        weight_down.add(p, value)

        # Insert into the ascending up sequence.
        # Only weights strictly smaller than value shift their coefficient.
        smaller_begin = bisect_left(all_values, value)
        smaller_weight = weight_up.prefix_sum(smaller_begin)
        smaller_count = count_up.prefix_sum(smaller_begin)

        weighted_up += smaller_weight + value * (k + 1 - smaller_count)
        k += 1
        sum_up += value
        count_up.add(p, 1)
        weight_up.add(p, value)

        answer = min(answer, total_cost())

    print(answer)


if __name__ == "__main__":
    main()