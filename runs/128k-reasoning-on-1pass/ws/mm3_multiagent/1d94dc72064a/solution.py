import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:1+N]))
    
    if N == 1:
        print("Fennec")
        return
    if N == 2:
        print("Snuke")
        return
    if N % 2 == 0:
        # Even N >= 4
        sum_v = sum(a - 1 for a in A)
        if sum_v % 2 == 0:
            print("Snuke")
        else:
            print("Fennec")
    else:
        # Odd N >= 3
        if all(a % 2 == 0 for a in A):
            print("Snuke")
        else:
            print("Fennec")

if __name__ == "__main__":
    solve()