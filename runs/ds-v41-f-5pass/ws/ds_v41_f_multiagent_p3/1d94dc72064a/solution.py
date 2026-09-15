import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        # Fennec iff there is at least one odd A_i
        if any(a % 2 == 1 for a in A):
            print("Fennec")
        else:
            print("Snuke")
    else:
        odd_count = sum(1 for a in A if a % 2 == 1)
        if odd_count % 2 == 1:
            print("Fennec")
        else:
            print("Snuke")

if __name__ == "__main__":
    solve()