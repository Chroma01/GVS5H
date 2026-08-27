import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:]

    total_xor = 0
    for x in a:
        total_xor ^= x

    r = min(k, n - k)
    use_complement = (k > n - k)

    if r == 0:
        print(total_xor)
        return

    best = 0

    def dfs(start, need, current_xor):
        nonlocal best

        if need == 0:
            value = total_xor ^ current_xor if use_complement else current_xor
            if value > best:
                best = value
            return

        end = n - need + 1
        for i in range(start, end):
            dfs(i + 1, need - 1, current_xor ^ a[i])

    dfs(0, r, 0)
    print(best)

if __name__ == "__main__":
    main()