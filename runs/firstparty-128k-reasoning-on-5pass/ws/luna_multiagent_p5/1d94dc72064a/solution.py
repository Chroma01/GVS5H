import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    odd = sum(x & 1 for x in a)

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        print("Fennec" if 0 < odd < 3 else "Snuke")
    else:
        print("Fennec" if odd % 2 == 1 else "Snuke")

if __name__ == "__main__":
    solve()