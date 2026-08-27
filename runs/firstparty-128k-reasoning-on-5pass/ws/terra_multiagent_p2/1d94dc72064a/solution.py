import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    even_count = sum(x % 2 == 0 for x in a)

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