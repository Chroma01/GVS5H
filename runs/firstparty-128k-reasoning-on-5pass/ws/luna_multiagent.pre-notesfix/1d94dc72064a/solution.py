import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        print("Fennec" if any(x & 1 for x in a) else "Snuke")
    else:
        odd_count = sum(x & 1 for x in a)
        print("Fennec" if odd_count & 1 else "Snuke")


if __name__ == "__main__":
    solve()