import sys

def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]

    if n == 1:
        fennec_wins = True
    elif n == 2:
        fennec_wins = False
    elif n == 3:
        fennec_wins = any(x & 1 for x in a)
    else:
        fennec_wins = (sum(x & 1 for x in a) & 1) == 1

    print("Fennec" if fennec_wins else "Snuke")

if __name__ == "__main__":
    main()