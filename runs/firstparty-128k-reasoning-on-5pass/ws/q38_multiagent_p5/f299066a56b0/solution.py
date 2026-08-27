import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    i = 0
    j = (n + 1) // 2
    ans = 0
    half = n // 2

    while i < half and j < n:
        if 2 * a[i] <= a[j]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1

    print(ans)

if __name__ == "__main__":
    main()