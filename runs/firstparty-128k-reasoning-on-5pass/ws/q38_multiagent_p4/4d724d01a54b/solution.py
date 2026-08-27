import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    pos = [0] * (n + 1)

    for i in range(1, n + 1):
        pos[data[i]] = i

    bit = [0] * (n + 1)
    ans = 0

    for x in range(1, n + 1):
        i = pos[x]

        s = 0
        j = i - 1
        while j:
            s += bit[j]
            j -= j & -j

        a = s + 1
        ans += (x - 1) * x // 2 - (a - 1) * a // 2

        j = i
        while j <= n:
            bit[j] += 1
            j += j & -j

    print(ans)

if __name__ == "__main__":
    main()