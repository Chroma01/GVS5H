import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]

    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * (n + 1)
    top = 1 << (n.bit_length() - 1)

    for i in range(n, 0, -1):
        k = data[i]
        idx = 0
        step = top
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1
        pos = idx + 1
        ans[pos] = i

        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

if __name__ == "__main__":
    main()