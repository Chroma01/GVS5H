import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    odd_count = sum(x & 1 for x in a)

    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd_count >= 1 else "Snuke"
    else:
        ans = "Fennec" if odd_count % 2 == 1 else "Snuke"

    print(ans)

if __name__ == "__main__":
    main()