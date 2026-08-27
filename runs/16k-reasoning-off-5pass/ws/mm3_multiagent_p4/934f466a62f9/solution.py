import sys
from itertools import permutations

def solve():
    import sys
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        N, K = map(int, input().split())
        cakes = []
        for i in range(N):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        best = 0
        # Try all 6 permutations of (0,1,2) for (X,Y,Z)
        for perm in permutations((0,1,2)):
            # Sort by the permuted dimensions, all descending
            # perm is a tuple of indices, e.g., (0,1,2) means sort by X, then Y, then Z
            # We need to sort in descending order for each key
            sorted_cakes = sorted(cakes, key=lambda c: (c[perm[0]], c[perm[1]], c[perm[2]]), reverse=True)
            # Take the first 2K cakes
            selected = sorted_cakes[:2*K]
            
            # Strategy 1: adjacent pairing
            total_adj = 0
            for i in range(0, 2*K, 2):
                a = selected[i]
                b = selected[i+1]
                price = max(a[0]+b[0], a[1]+b[1], a[2]+b[2])
                total_adj += price
            if total_adj > best:
                best = total_adj
            
            # Strategy 2: extreme pairing (i with i+K)
            total_ext = 0
            for i in range(K):
                a = selected[i]
                b = selected[i+K]
                price = max(a[0]+b[0], a[1]+b[1], a[2]+b[2])
                total_ext += price
            if total_ext > best:
                best = total_ext
        
        print(best)

if __name__ == "__main__":
    solve()