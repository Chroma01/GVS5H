import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        print("Snuke" if all(x % 2 == 0 for x in a) else "Fennec")
    else:
        print("Snuke" if sum(x % 2 for x in a) % 2 == 0 else "Fennec")


if __name__ == "__main__":
    solve()