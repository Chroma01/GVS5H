import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    s = sum(a)
    m = max(a)
    # The correct condition: Fennec wins iff 2 * max(A) > sum(A) + 1
    if 2 * m > s + 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    main()