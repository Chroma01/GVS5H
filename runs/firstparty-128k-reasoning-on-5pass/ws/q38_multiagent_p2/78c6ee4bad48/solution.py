import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1:1 + n]

    even_gaps = []
    odd_gaps = []

    for j in range(n - 1):
        g = x[j + 1] - x[j]
        if j & 1:
            odd_gaps.append(g)
        else:
            even_gaps.append(g)

    even_gaps.sort()
    odd_gaps.sort()

    ans = n * x[0]
    ei = 0
    oi = 0

    for j in range(n - 1):
        weight = n - 1 - j
        if j & 1:
            ans += weight * odd_gaps[oi]
            oi += 1
        else:
            ans += weight * even_gaps[ei]
            ei += 1

    print(ans)

if __name__ == "__main__":
    main()