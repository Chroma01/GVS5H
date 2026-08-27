import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    x = list(map(int, data[1:1+n]))
    # The first n-1 pieces can be permuted arbitrarily; sort them ascending to minimize sum.
    # The last piece remains at the rightmost position.
    first_part = x[:-1]
    first_part.sort()
    total = sum(first_part) + x[-1]
    print(total)

if __name__ == "__main__":
    main()