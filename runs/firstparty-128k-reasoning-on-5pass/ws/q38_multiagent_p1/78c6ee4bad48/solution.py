import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    first = int(data[1])

    gaps = []
    prev = first
    for i in range(2, n + 1):
        cur = int(data[i])
        gaps.append(cur - prev)
        prev = cur

    odd_gaps = gaps[0::2]
    even_gaps = gaps[1::2]

    odd_gaps.sort()
    even_gaps.sort()

    ans = n * first

    for w, g in zip(range(n - 1, 0, -2), odd_gaps):
        ans += w * g

    for w, g in zip(range(n - 2, 0, -2), even_gaps):
        ans += w * g

    print(ans)

if __name__ == "__main__":
    main()