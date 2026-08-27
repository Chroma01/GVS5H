import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    last = [0] * (n + 2)
    sum_last = 0
    sum_adj = 0
    answer = 0

    for r, x in enumerate(a, 1):
        # Remove contributions of pairs involving x using its old last occurrence.
        if x > 1:
            sum_adj -= min(last[x - 1], last[x])
        if x < n:
            sum_adj -= min(last[x], last[x + 1])

        old = last[x]
        last[x] = r
        sum_last += r - old

        # Add contributions of the same pairs after updating x.
        if x > 1:
            sum_adj += min(last[x - 1], last[x])
        if x < n:
            sum_adj += min(last[x], last[x + 1])

        answer += sum_last - sum_adj

    print(answer)

if __name__ == "__main__":
    solve()