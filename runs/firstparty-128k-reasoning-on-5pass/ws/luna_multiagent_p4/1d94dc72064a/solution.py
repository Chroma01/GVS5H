import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    if n == 1:
        print("Fennec")
        return

    if n == 2:
        print("Snuke")
        return

    even_count = sum(x % 2 == 0 for x in a)

    if n == 3:
        print("Snuke" if even_count == 3 else "Fennec")
        return

    print("Fennec" if (n + even_count) % 2 == 1 else "Snuke")


if __name__ == "__main__":
    solve()