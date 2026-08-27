import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x0 = data[1]

    gaps = [data[i + 2] - data[i + 1] for i in range(n - 1)]

    even = gaps[0::2]
    odd = gaps[1::2]

    even.sort()
    odd.sort()

    ans = n * x0

    for k, g in enumerate(even):
        idx = 2 * k
        ans += (n - 1 - idx) * g

    for k, g in enumerate(odd):
        idx = 2 * k + 1
        ans += (n - 1 - idx) * g

    print(ans)

if __name__ == "__main__":
    main()