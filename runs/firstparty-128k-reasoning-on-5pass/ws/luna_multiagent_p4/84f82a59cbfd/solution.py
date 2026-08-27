import sys
from bisect import bisect_right
from math import isqrt


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    q = data[0]
    queries = data[1:1 + q]

    max_x = isqrt(max(queries))

    is_prime = bytearray(b"\x01") * (max_x + 1)
    if max_x >= 0:
        is_prime[0] = 0
    if max_x >= 1:
        is_prime[1] = 0

    for i in range(2, isqrt(max_x) + 1):
        if is_prime[i]:
            start = i * i
            is_prime[start:max_x + 1:i] = b"\x00" * (((max_x - start) // i) + 1)

    distinct_count = bytearray(max_x + 1)
    for p in range(2, max_x + 1):
        if is_prime[p]:
            for multiple in range(p, max_x + 1, p):
                distinct_count[multiple] += 1

    candidates = [
        x * x
        for x in range(2, max_x + 1)
        if distinct_count[x] == 2
    ]
    candidates.sort()

    answers = [str(candidates[bisect_right(candidates, a) - 1]) for a in queries]
    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()