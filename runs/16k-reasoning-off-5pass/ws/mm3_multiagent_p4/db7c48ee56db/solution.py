import sys
import itertools

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    max_xor = 0
    # Enumerate all K-element subsets; C(N,K) <= 10^6
    for combo in itertools.combinations(A, K):
        val = 0
        for x in combo:
            val ^= x
        if val > max_xor:
            max_xor = val
    print(max_xor)

if __name__ == "__main__":
    solve()