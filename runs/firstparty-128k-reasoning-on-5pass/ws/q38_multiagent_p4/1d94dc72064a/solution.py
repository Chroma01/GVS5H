import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    odd = sum(x & 1 for x in a)

    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd > 0 else "Snuke"
    else:
        ans = "Fennec" if odd % 2 == 1 else "Snuke"

    print(ans)

if __name__ == "__main__":
    main()