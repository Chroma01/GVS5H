import sys
import random
import io

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    P = list(map(int, input().split()))
    
    # Compute S(W) and C(W) for a given W
    def compute(W):
        S = 0
        C = 0
        for p in P:
            k = (W // p + 1) // 2
            if k:
                S += k * k * p
                C += k
        return S, C
    
    # Binary search for the smallest W such that S(W) > M
    lo = 0
    hi = 2 * 10**18  # safe upper bound
    while lo < hi:
        mid = (lo + hi) // 2
        S, _ = compute(mid)
        if S > M:
            hi = mid
        else:
            lo = mid + 1
    W = lo
    S, C = compute(W)
    # Answer = C - ceil((S - M) / W)
    ans = C - (S - M + W - 1) // W
    print(ans)

# Brute force solver for testing
def brute(N, M, P):
    best = 0
    def rec(i, cost, units):
        nonlocal best
        if i == N:
            if cost <= M:
                if units > best:
                    best = units
            return
        p = P[i]
        # maximum k such that k^2 * p <= M - cost
        max_k = int((M - cost) ** 0.5) + 1
        for k in range(max_k + 1):
            new_cost = cost + k * k * p
            if new_cost > M:
                break
            rec(i + 1, new_cost, units + k)
    rec(0, 0, 0)
    return best

def test_random():
    for _ in range(100):
        N = random.randint(1, 5)
        M = random.randint(1, 200)
        P = [random.randint(1, 10) for _ in range(N)]
        # Run our solution
        buf = io.StringIO()
        sys.stdout = buf
        input_str = f"{N} {M}\n{' '.join(map(str, P))}\n"
        sys.stdin = io.StringIO(input_str)
        solve()
        sys.stdout = sys.__stdout__
        our_ans = int(buf.getvalue().strip())
        brute_ans = brute(N, M, P)
        if our_ans != brute_ans:
            print("FAIL", N, M, P, our_ans, brute_ans)
            return
    print("All tests passed")

if __name__ == "__main__":
    # Run random tests against brute-force; if they pass, read stdin and output answer
    test_random()
    # Reset stdin/stdout to actual user input
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    # Now run the main solve
    solve()