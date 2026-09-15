import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    else:
        c = sum(1 for x in a if x % 2 == 1)  # number of odd A_i (= number of even rewards)
        if n == 3:
            print("Fennec" if c >= 1 else "Snuke")
        else:
            print("Fennec" if c % 2 == 1 else "Snuke")

main()