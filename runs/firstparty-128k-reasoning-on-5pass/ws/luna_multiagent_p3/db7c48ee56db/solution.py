import sys
from itertools import combinations


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    total_xor = 0
    for value in a:
        total_xor ^= value

    r = min(k, n - k)

    if r == 0:
        print(total_xor)
        return

    use_complement = k > n - k
    answer = 0

    for indices in combinations(range(n), r):
        subset_xor = 0
        for index in indices:
            subset_xor ^= a[index]

        candidate = total_xor ^ subset_xor if use_complement else subset_xor
        if candidate > answer:
            answer = candidate

    print(answer)


if __name__ == "__main__":
    solve()