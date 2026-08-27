import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    top = 0
    pairs = 0

    for bottom in range((n + 1) // 2, n):
        if 2 * a[top] <= a[bottom]:
            pairs += 1
            top += 1
            if top == n // 2:
                break

    print(pairs)

if __name__ == "__main__":
    main()