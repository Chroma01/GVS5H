import sys


def main() -> None:
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # gap indices 1, 3, 5, ...
    even_gaps = sorted(gaps[1::2])  # gap indices 2, 4, 6, ...

    answer = n * x[0]
    odd_ptr = 0
    even_ptr = 0

    for j in range(1, n):
        if j % 2 == 1:
            gap = odd_gaps[odd_ptr]
            odd_ptr += 1
        else:
            gap = even_gaps[even_ptr]
            even_ptr += 1
        answer += (n - j) * gap

    print(answer)


if __name__ == "__main__":
    main()