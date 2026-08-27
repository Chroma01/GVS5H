import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    last = [0] * (n + 2)
    current_sum = 0
    answer = 0

    for r, x in enumerate(a, 1):
        prev_x = last[x]

        delta = r - prev_x
        delta -= max(0, last[x - 1] - prev_x)
        delta -= max(0, last[x + 1] - prev_x)

        current_sum += delta
        answer += current_sum
        last[x] = r

    print(answer)

if __name__ == "__main__":
    solve()