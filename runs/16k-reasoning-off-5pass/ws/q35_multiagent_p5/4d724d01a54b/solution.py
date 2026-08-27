import sys

def solve():
    # Increase recursion depth just in case, though not needed here
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    P = list(map(int, data[1:]))
    
    # If N is 1, cost is 0
    if N <= 1:
        print(0)
        return

    # We need to compute C_k for k from 1 to N-1.
    # C_k is the number of elements in P[0...k-1] (0-indexed) that are > k.
    # Using 1-based indexing for logic:
    # For boundary k (between position k and k+1, 1-based),
    # C_k = count of i in 1..k such that P[i] > k.
    
    # We can use a Fenwick Tree (Binary Indexed Tree) to count elements <= k
    # among the first k elements of P.
    
    # BIT implementation (1-indexed)
    bit = [0] * (N + 1)
    
    def update(idx, val):
        """Add val to element at idx (1-based)"""
        while idx <= N:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        """Return sum from 1 to idx (1-based)"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
    
    total_cost = 0
    
    # Iterate k from 1 to N-1
    # At step k, we have processed P[0]...P[k-1] (which are the first k elements)
    # We add P[k-1] to the BIT before computing C_k for boundary k?
    # Wait, let's align indices carefully.
    
    # P is 0-indexed in our list: P[0], P[1], ..., P[N-1]
    # Boundary k (1-based) is between position k and k+1.
    # The first k positions are P[0], ..., P[k-1].
    # We need to count how many of these are > k.
    
    # So, for k from 1 to N-1:
    # 1. Add P[k-1] to BIT (since P[k-1] is the k-th element, 1-based index k)
    # 2. Query BIT for count of numbers <= k in the first k elements.
    # 3. C_k = k - query(k)
    # 4. Add C_k * k to total_cost
    
    for k in range(1, N):
        # The element at 1-based position k is P[k-1]
        val = P[k-1]
        update(val, 1)
        
        # Count how many of the first k elements are <= k
        count_le_k = query(k)
        
        # C_k is the number of elements in first k positions that are > k
        C_k = k - count_le_k
        
        total_cost += C_k * k
        
    print(total_cost)

if __name__ == '__main__':
    solve()