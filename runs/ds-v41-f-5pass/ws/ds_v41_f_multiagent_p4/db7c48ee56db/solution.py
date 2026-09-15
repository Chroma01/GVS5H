import sys
from itertools import combinations

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    A = [int(x) for x in data[2:2 + N]]

    total_xor = 0
    for v in A:
        total_xor ^= v

    # Enumerate the smaller side: chosen elements directly if K is small,
    # otherwise enumerate excluded elements.
    if K <= N - K:
        best = -1
        for comb in combinations(A, K):
            x = 0
            for v in comb:
                x ^= v
            if x > best:
                best = x
        print(best)
    else:
        excluded_size = N - K
        best = -1
        for comb in combinations(A, excluded_size):
            x = 0
            for v in comb:
                x ^= v
            val = total_xor ^ x
            if val > best:
                best = val
        print(best)

if __name__ == "__main__":
    main()