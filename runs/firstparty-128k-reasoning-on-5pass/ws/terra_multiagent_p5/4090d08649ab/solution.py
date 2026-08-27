import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    positions = [[] for _ in range(n + 1)]
    for i, x in enumerate(a, 1):
        positions[x].append(i)

    total_subarrays = n * (n + 1) // 2

    # Sum over values: number of subarrays containing that value.
    value_sum = 0
    for x in range(1, n + 1):
        prev = 0
        absent_subarrays = 0
        for p in positions[x]:
            gap = p - prev - 1
            absent_subarrays += gap * (gap + 1) // 2
            prev = p
        gap = n - prev
        absent_subarrays += gap * (gap + 1) // 2
        value_sum += total_subarrays - absent_subarrays

    # Sum over adjacent value pairs: number of subarrays containing both x and x+1.
    adjacent_pair_sum = 0
    for x in range(1, n):
        px = positions[x]
        py = positions[x + 1]

        i = 0
        j = 0
        last_x = 0
        last_y = 0
        pair_count = 0

        while i < len(px) or j < len(py):
            if j == len(py) or (i < len(px) and px[i] < py[j]):
                p = px[i]
                last_x = p
                i += 1
            else:
                p = py[j]
                last_y = p
                j += 1

            next_p = n + 1
            if i < len(px):
                next_p = min(next_p, px[i])
            if j < len(py):
                next_p = min(next_p, py[j])

            if last_x and last_y:
                pair_count += min(last_x, last_y) * (next_p - p)

        adjacent_pair_sum += pair_count

    print(value_sum - adjacent_pair_sum)


if __name__ == "__main__":
    solve()