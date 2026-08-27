import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.count = [0] * (n + 1)
        self.total = [0] * (n + 1)

    def add(self, i, cnt, value):
        while i <= self.n:
            self.count[i] += cnt
            self.total[i] += value
            i += i & -i

    def query(self, i):
        cnt = 0
        value = 0
        while i > 0:
            cnt += self.count[i]
            value += self.total[i]
            i -= i & -i
        return cnt, value


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    mandatory_remove = []
    mandatory_add = []
    optional = []
    initial_weight = 0

    for ai, bi, ci in zip(a, b, c):
        if ai:
            initial_weight += ci

        if ai == 1 and bi == 0:
            mandatory_remove.append(ci)
        elif ai == 0 and bi == 1:
            mandatory_add.append(ci)
        elif ai == 1 and bi == 1:
            optional.append(ci)

    values = sorted(set(c))
    rank = {x: i + 1 for i, x in enumerate(values)}
    m = len(values)

    # T_remove = sum(w * number of removal weights <= w).
    # Removal cost for q removals is q * initial_weight - T_remove.
    remove_tree = Fenwick(m)
    remove_count = 0
    remove_sum = 0
    remove_t = 0

    def insert_removal(x):
        nonlocal remove_count, remove_sum, remove_t

        p = rank[x]
        count_le, sum_le = remove_tree.query(p)
        sum_greater = remove_sum - sum_le

        # x contributes for itself and all existing weights <= x.
        # Existing weights > x gain one coefficient.
        remove_t += x * (count_le + 1) + sum_greater

        remove_tree.add(p, 1, x)
        remove_count += 1
        remove_sum += x

    # T_add = sum(w * number of addition weights >= w).
    # Addition cost for q additions from base active weight S is q*S + T_add.
    add_tree = Fenwick(m)
    add_count = 0
    add_sum = 0
    add_t = 0

    def insert_addition(x):
        nonlocal add_count, add_sum, add_t

        p = rank[x]
        count_less, _ = add_tree.query(p - 1)
        _, sum_le = add_tree.query(p)
        count_ge = add_count - count_less

        # x contributes for itself and all existing weights >= x.
        # Existing weights <= x gain one coefficient.
        add_t += x * (count_ge + 1) + sum_le

        add_tree.add(p, 1, x)
        add_count += 1
        add_sum += x

    for x in mandatory_remove:
        insert_removal(x)
    for x in mandatory_add:
        insert_addition(x)

    optional.sort(reverse=True)
    remaining_optional_weight = sum(optional)

    def cost():
        removal_cost = remove_count * initial_weight - remove_t
        addition_cost = add_count * remaining_optional_weight + add_t
        return removal_cost + addition_cost

    answer = cost()

    # If s correct-one bits are temporarily disabled, choose the s largest.
    for x in optional:
        insert_removal(x)
        insert_addition(x)
        remaining_optional_weight -= x
        answer = min(answer, cost())

    print(answer)


if __name__ == "__main__":
    solve()