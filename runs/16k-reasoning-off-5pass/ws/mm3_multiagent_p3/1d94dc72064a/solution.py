import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:1+N]))
    total = sum(A)
    if total % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    main()