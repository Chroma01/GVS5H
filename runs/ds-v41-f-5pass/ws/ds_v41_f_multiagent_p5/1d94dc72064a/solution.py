import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    odd_count = sum(x & 1 for x in a)

    if n == 1 or (n == 3 and odd_count > 0) or (n >= 4 and odd_count % 2 == 1):
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    main()