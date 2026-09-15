import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = [0] + data[1:1 + n]

    INF = n + 1

    # next_minus[i] = next position j > i with a[j] = a[i]-1, or INF if none / a[i]==1
    next_minus = [INF] * (n + 1)
    last_next = [INF] * (n + 2)

    for i in range(n, 0, -1):
        x = a[i]
        if x > 1:
            next_minus[i] = last_next[x - 1]
        last_next[x] = i

    ans = 0
    last = [0] * (n + 2)

    for i in range(1, n + 1):
        x = a[i]

        prev_same = last[x]
        prev_minus = last[x - 1] if x > 1 else 0

        left_bound = prev_same if prev_same > prev_minus else prev_minus
        ans += (i - left_bound) * (next_minus[i] - i)

        last[x] = i

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()