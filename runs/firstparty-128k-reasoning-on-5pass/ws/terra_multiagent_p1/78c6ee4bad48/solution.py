import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    odd_gaps = []
    even_gaps = []

    for i in range(n - 1):
        gap = x[i + 1] - x[i]
        if i % 2 == 0:  # Gap position is i+1, which is odd.
            odd_gaps.append(gap)
        else:
            even_gaps.append(gap)

    odd_gaps.sort()
    even_gaps.sort()

    answer = n * x[0]
    odd_index = 0
    even_index = 0

    for j in range(1, n):
        if j % 2 == 1:
            gap = odd_gaps[odd_index]
            odd_index += 1
        else:
            gap = even_gaps[even_index]
            even_index += 1

        answer += (n - j) * gap

    print(answer)

if __name__ == "__main__":
    main()