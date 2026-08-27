import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    half = n // 2
    left = 0
    right = half
    ans = 0

    while left < half and right < n:
        if a[left] * 2 <= a[right]:
            ans += 1
            left += 1
        right += 1

    print(ans)

if __name__ == "__main__":
    main()