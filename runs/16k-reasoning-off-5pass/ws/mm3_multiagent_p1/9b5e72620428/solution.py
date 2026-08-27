import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    
    known_sums = set()
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            known_sums.add(A[i] + B[i])
    
    if not known_sums:
        # No fully known pair, we can always choose S large enough.
        print("Yes")
        return
    
    if len(known_sums) > 1:
        print("No")
        return
    
    S = next(iter(known_sums))
    
    # Check all known values are <= S
    for i in range(N):
        if A[i] != -1 and A[i] > S:
            print("No")
            return
        if B[i] != -1 and B[i] > S:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    solve()