import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    even_count = sum(1 for x in a if x % 2 == 0)

    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Snuke" if even_count == 3 else "Fennec"
    else:
        ans = "Fennec" if (n + even_count) % 2 == 1 else "Snuke"

    print(ans)

if __name__ == "__main__":
    main()