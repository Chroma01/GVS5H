import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    # last[x] is the latest position of value x in the processed prefix.
    last = [0] * (n + 2)

    # current is the sum of f(L, R) over all L for the current R.
    current = 0
    answer = 0

    for r, v in enumerate(a, 1):
        old_v = last[v]
        prev_v = last[v - 1]
        next_v = last[v + 1]

        # Only terms for x=v and x=v+1 change.
        # x=v: max(0, last[v]-last[v-1]) -> r-last[v-1]
        # x=v+1: max(0, last[v+1]-last[v]) -> 0
        current += (
            (r - prev_v)
            - max(0, old_v - prev_v)
            - max(0, next_v - old_v)
        )

        last[v] = r
        answer += current

    print(answer)


if __name__ == "__main__":
    solve()