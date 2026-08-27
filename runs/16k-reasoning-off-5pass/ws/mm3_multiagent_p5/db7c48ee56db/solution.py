import sys
from itertools import combinations

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    max_xor = 0
    # Since C(N, K) <= 10^6, we can safely enumerate all K-element subsets.
    for comb in combinations(A, K):
        x = 0
        for v in comb:
            x ^= v
        if x > max_xor:
            max_xor = x
    print(max_xor)

if __name__ == "__main__":
    main()