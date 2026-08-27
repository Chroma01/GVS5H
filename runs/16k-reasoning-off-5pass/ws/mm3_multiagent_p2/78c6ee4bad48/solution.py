import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = [int(next(it)) for _ in range(N)]
    
    # Compute gaps between consecutive positions
    gaps = [X[i+1] - X[i] for i in range(N-1)]
    
    # Separate gaps by parity of index
    even_gaps = []
    odd_gaps = []
    for idx, g in enumerate(gaps):
        if idx % 2 == 0:
            even_gaps.append(g)
        else:
            odd_gaps.append(g)
    
    # Sort each parity class in non-decreasing order
    even_gaps.sort()
    odd_gaps.sort()
    
    # Reconstruct the sequence with sorted gaps
    new_X = [0] * N
    new_X[0] = X[0]
    ei = 0
    oi = 0
    for j in range(N-1):
        if j % 2 == 0:
            g = even_gaps[ei]
            ei += 1
        else:
            g = odd_gaps[oi]
            oi += 1
        new_X[j+1] = new_X[j] + g
    
    # Compute and output the sum
    total = sum(new_X)
    print(total)

if __name__ == "__main__":
    solve()