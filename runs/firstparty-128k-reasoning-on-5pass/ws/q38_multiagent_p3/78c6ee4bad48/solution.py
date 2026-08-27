import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])
    even_gaps = sorted(gaps[1::2])

    ans = n * x[0]

    for g, k in zip(odd_gaps, range(1, n, 2)):
        ans += (n - k) * g

    for g, k in zip(even_gaps, range(2, n, 2)):
        ans += (n - k) * g

    print(ans)

if __name__ == "__main__":
    main()