import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    odd_count = sum(x & 1 for x in a)

    if n == 1:
        answer = "Fennec"
    elif n == 2:
        answer = "Snuke"
    elif n == 3:
        answer = "Fennec" if odd_count > 0 else "Snuke"
    else:
        answer = "Fennec" if odd_count % 2 == 1 else "Snuke"

    print(answer)

if __name__ == "__main__":
    main()