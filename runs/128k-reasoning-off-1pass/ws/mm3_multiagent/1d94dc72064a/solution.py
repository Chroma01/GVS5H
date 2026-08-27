import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    # A_i for i in 1..n
    total = sum(int(x) for x in data[1:1+n])
    # Fennec moves first; if total is odd, Fennec makes the last move.
    if total % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    main()