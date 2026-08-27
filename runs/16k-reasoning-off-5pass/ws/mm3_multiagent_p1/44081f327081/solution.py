import sys
import math

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    MAX_A = 10**6
    cnt = [0] * (MAX_A + 1)
    for v in A:
        cnt[v] += 1
    multCnt = [0] * (MAX_A + 1)
    # compute number of array elements divisible by each v
    # for v from MAX_A down to 1
    for v in range(MAX_A, 0, -1):
        # add own count
        s = cnt[v]
        step = v
        # we will accumulate from multiples, but we can compute by adding cnt at multiples
        # we need to sum cnt[m] for m multiples of v.
        # We can do this by iterating multiples and adding, total O(MAX_A log MAX_A)
        m = v * 2
        while m <= MAX_A:
            s += cnt[m]
            m += v
        multCnt[v] = s
    # For each index, find largest divisor d of A[i] with multCnt[d] >= K
    out_lines = []
    # precompute nothing else
    for idx in range(N):
        x = A[idx]
        best = 1
        # enumerate divisors in decreasing order
        # We'll find all divisors, then sort descending, and take first with multCnt[d] >= K
        # but we can also iterate from sqrt downwards and push pairs
        # To stop early, we collect divisors and sort once
        # However sorting for each i is costly. Better: generate divisors and check large ones first.
        # We'll generate all divisors into a list, then sort descending.
        # Number of divisors is small (<~240), so this is fine.
        divs = []
        r = int(math.isqrt(x))
        for d in range(1, r + 1):
            if x % d == 0:
                d1 = d
                d2 = x // d
                divs.append(d1)
                if d2 != d1:
                    divs.append(d2)
        # sort descending
        divs.sort(reverse=True)
        ans = 1
        for d in divs:
            if multCnt[d] >= K:
                ans = d
                break
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()