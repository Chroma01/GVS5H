import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:2 + n]

    total_xor = 0
    for value in a:
        total_xor ^= value

    r = min(k, n - k)
    enumerate_excluded = k > n // 2

    if r == 0:
        print(total_xor if enumerate_excluded else 0)
        return

    best = -1

    if enumerate_excluded:
        def dfs(start, remaining, current_xor):
            nonlocal best
            if remaining == 0:
                candidate = total_xor ^ current_xor
                if candidate > best:
                    best = candidate
                return

            last = n - remaining
            for i in range(start, last + 1):
                dfs(i + 1, remaining - 1, current_xor ^ a[i])

        dfs(0, r, 0)
    else:
        def dfs(start, remaining, current_xor):
            nonlocal best
            if remaining == 0:
                if current_xor > best:
                    best = current_xor
                return

            last = n - remaining
            for i in range(start, last + 1):
                dfs(i + 1, remaining - 1, current_xor ^ a[i])

        dfs(0, r, 0)

    print(best)

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    solve()