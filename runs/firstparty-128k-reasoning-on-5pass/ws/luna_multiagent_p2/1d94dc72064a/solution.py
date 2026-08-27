import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    odd = sum(x & 1 for x in a)

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        print("Fennec" if odd > 0 else "Snuke")
    else:
        print("Fennec" if odd & 1 else "Snuke")


if __name__ == "__main__":
    solve()