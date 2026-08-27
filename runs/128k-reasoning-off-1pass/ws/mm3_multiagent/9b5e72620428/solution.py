import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    
    fixedA = []
    fixedB = []
    x = 0  # count of -1 in A
    y = 0  # count of -1 in B
    
    for a in A:
        if a == -1:
            x += 1
        else:
            fixedA.append(a)
    for b in B:
        if b == -1:
            y += 1
        else:
            fixedB.append(b)
    
    # Special case: no flexibility at all
    if x == 0 and y == 0:
        s = A[0] + B[0]
        for i in range(1, N):
            if A[i] + B[i] != s:
                print("No")
                return
        print("Yes")
        return
    
    # We have flexibility (can rearrange A and/or fill -1)
    fixedA.sort()
    fixedB.sort()
    
    # Pair up to min(len(fixedA), len(fixedB))
    k = min(len(fixedA), len(fixedB))
    if k == 0:
        # No fixed values to compare; always possible
        print("Yes")
        return
    
    target = fixedA[0] + fixedB[0]
    for i in range(1, k):
        if fixedA[i] + fixedB[i] != target:
            print("No")
            return
    print("Yes")

if __name__ == "__main__":
    solve()