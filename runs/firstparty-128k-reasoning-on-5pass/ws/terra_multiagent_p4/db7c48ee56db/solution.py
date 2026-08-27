import sys

def main():
    input = sys.stdin.buffer.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    total_xor = 0
    for x in a:
        total_xor ^= x

    if k == n:
        print(total_xor)
        return

    if k <= n - k:
        r = k
        base = 0
    else:
        r = n - k
        base = total_xor

    best = 0

    def dfs(start, remaining, current_xor):
        nonlocal best

        if remaining == 0:
            value = base ^ current_xor
            if value > best:
                best = value
            return

        end = n - remaining + 1
        for i in range(start, end):
            dfs(i + 1, remaining - 1, current_xor ^ a[i])

    dfs(0, r, 0)
    print(best)

if __name__ == "__main__":
    main()