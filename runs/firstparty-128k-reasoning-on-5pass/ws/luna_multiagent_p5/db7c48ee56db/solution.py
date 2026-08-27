import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:]

    total_xor = 0
    for value in a:
        total_xor ^= value

    r = min(k, n - k)
    use_complement = k > n - k
    best = -1

    def dfs(start, left, current_xor):
        nonlocal best

        if left == 0:
            candidate = total_xor ^ current_xor if use_complement else current_xor
            if candidate > best:
                best = candidate
            return

        if left == 1:
            for i in range(start, n):
                value = current_xor ^ a[i]
                candidate = total_xor ^ value if use_complement else value
                if candidate > best:
                    best = candidate
            return

        last = n - left + 1
        for i in range(start, last):
            dfs(i + 1, left - 1, current_xor ^ a[i])

    dfs(0, r, 0)
    print(best)

if __name__ == "__main__":
    solve()