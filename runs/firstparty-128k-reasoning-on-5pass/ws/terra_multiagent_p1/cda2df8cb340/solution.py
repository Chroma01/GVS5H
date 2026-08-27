import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total_sum = sum(a)
    answer = (n + 1) * total_sum

    max_a = max(a)
    mod = 2

    while mod <= 2 * max_a:
        mask = mod - 1
        groups = {}

        for x in a:
            r = x & mask
            entry = groups.get(r)
            if entry is None:
                groups[r] = [1, x]
            else:
                entry[0] += 1
                entry[1] += x

        ordered_weight = 0
        for r, (cnt, value_sum) in groups.items():
            other = groups.get((-r) & mask)
            if other is not None:
                other_cnt, other_sum = other
                ordered_weight += other_cnt * value_sum + cnt * other_sum

        diagonal_weight = 2 * groups.get(0, [0, 0])[1]
        half = mod >> 1
        diagonal_weight += 2 * groups.get(half, [0, 0])[1]

        unordered_weight = (ordered_weight + diagonal_weight) // 2
        answer -= unordered_weight // mod

        mod <<= 1

    print(answer)

if __name__ == "__main__":
    solve()