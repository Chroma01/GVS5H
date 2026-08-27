import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    e = sum(x & 1 for x in a)  # number of odd A_i

    if n == 1:
        print("Fennec")
        return

    if n == 2:
        print("Snuke")
        return

    if n == 3:
        print("Fennec" if e >= 1 else "Snuke")
        return

    if n == 4:
        print("Fennec" if e == 1 else "Snuke")
        return

    if n == 5:
        print("Fennec" if e == 1 or e >= 3 else "Snuke")
        return

    if n == 6:
        print("Fennec" if e in (1, 3) else "Snuke")
        return

    if n == 7:
        print("Fennec" if e in (1, 3, 5, 6, 7) else "Snuke")
        return

    # For N >= 8, Lucas' theorem gives the criterion:
    # C(N-1, number of even A_i) is odd.
    even_count = n - e
    print("Fennec" if (even_count & ~(n - 1)) == 0 else "Snuke")


if __name__ == "__main__":
    solve()