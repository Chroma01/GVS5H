import sys
from itertools import combinations

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    A = list(map(int, data[2:2 + n]))

    total = 0
    for a in A:
        total ^= a

    m = min(k, n - k)
    use_complement = (m != k)  # True when we enumerate the complement side

    best = -1
    if m == 0:
        best = total if use_complement else 0
    elif m == 1:
        if not use_complement:
            for a in A:
                if a > best:
                    best = a
        else:
            for a in A:
                cand = total ^ a
                if cand > best:
                    best = cand
    else:
        if not use_complement:
            for combo in combinations(A, m):
                x = 0
                for v in combo:
                    x ^= v
                if x > best:
                    best = x
        else:
            for combo in combinations(A, m):
                x = 0
                for v in combo:
                    x ^= v
                cand = total ^ x
                if cand > best:
                    best = cand

    sys.stdout.write(str(best) + "\n")

main()