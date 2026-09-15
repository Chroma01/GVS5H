import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = gaps[0::2]
    even_gaps = gaps[1::2]

    odd_gaps.sort()
    even_gaps.sort()

    ans = n * x[0]

    oi = 0
    ei = 0

    for j in range(n - 1):
        if j % 2 == 0:
            g = odd_gaps[oi]
            oi += 1
        else:
            g = even_gaps[ei]
            ei += 1

        ans += g * (n - 1 - j)

    print(ans)

if __name__ == "__main__":
    main()