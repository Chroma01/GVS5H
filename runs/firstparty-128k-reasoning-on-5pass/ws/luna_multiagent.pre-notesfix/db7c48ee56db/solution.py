import sys
from itertools import combinations

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:]

    total_xor = 0
    for value in a:
        total_xor ^= value

    r = min(k, n - k)
    use_complement = k > n - k

    ans = 0

    for comb in combinations(range(n), r):
        subset_xor = 0
        for i in comb:
            subset_xor ^= a[i]

        candidate = total_xor ^ subset_xor if use_complement else subset_xor
        if candidate > ans:
            ans = candidate

    print(ans)

if __name__ == "__main__":
    solve()