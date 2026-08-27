import sys
from bisect import bisect_left, bisect_right

def main():
    input = sys.stdin.buffer.readline

    N, Q = map(int, input().split())
    A = list(map(int, input().split()))

    queries_by_r = [[] for _ in range(N + 1)]
    for qi in range(Q):
        r, x = map(int, input().split())
        queries_by_r[r].append((x, qi))

    tails = []
    answers = [0] * Q

    for i, value in enumerate(A, 1):
        pos = bisect_left(tails, value)
        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value

        for x, qi in queries_by_r[i]:
            answers[qi] = bisect_right(tails, x)

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    main()