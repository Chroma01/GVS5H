import sys
from bisect import bisect_right

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:1 + q]

    limit = 1_000_000

    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0] = 0
    is_prime[1] = 0

    r = int(limit ** 0.5)
    for i in range(2, r + 1):
        if is_prime[i]:
            start = i * i
            is_prime[start:limit + 1:i] = b"\x00" * (
                (limit - start) // i + 1
            )

    distinct_count = bytearray(limit + 1)
    for p in range(2, limit + 1):
        if is_prime[p]:
            for multiple in range(p, limit + 1, p):
                distinct_count[multiple] += 1

    candidates = [
        x * x
        for x in range(2, limit + 1)
        if distinct_count[x] == 2
    ]

    answers = []
    for a in queries:
        pos = bisect_right(candidates, a) - 1
        answers.append(str(candidates[pos]))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()