import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    half = n // 2
    top = 0
    bottom = half
    pairs = 0

    while top < half and bottom < n:
        if 2 * a[top] <= a[bottom]:
            pairs += 1
            top += 1
        bottom += 1

    print(pairs)

if __name__ == "__main__":
    main()