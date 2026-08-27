import sys
from itertools import combinations

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:2 + n]

    r = min(k, n - k)
    use_complement = k > n - k

    total_xor = 0
    if use_complement:
        for value in a:
            total_xor ^= value

    answer = 0
    indices = range(n)

    for chosen in combinations(indices, r):
        current = 0
        for i in chosen:
            current ^= a[i]

        if use_complement:
            current ^= total_xor

        if current > answer:
            answer = current

    print(answer)

if __name__ == "__main__":
    solve()