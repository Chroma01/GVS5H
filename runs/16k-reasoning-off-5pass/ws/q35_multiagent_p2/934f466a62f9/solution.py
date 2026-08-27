import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
        except StopIteration:
            break
            
        cakes = []
        for i in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            z = int(next(iterator))
            cakes.append((x, y, z))
            
        # Calculate sum of attributes for each cake
        # We want to select the best 2K cakes.
        # Heuristic: Sort by total sum X+Y+Z descending.
        
        # Store original indices or just the values? We just need values.
        # Let's store tuples (sum, x, y, z)
        cakes_with_sum = []
        for (x, y, z) in cakes:
            s = x + y + z
            cakes_with_sum.append((s, x, y, z))
            
        # Sort by sum descending
        cakes_with_sum.sort(key=lambda p: p[0], reverse=True)
        
        # Take top 2K
        top_2k = cakes_with_sum[:2*K]
        
        # Now pair the i-th largest with the i-th smallest among these 2K
        # top_2k is sorted descending: [0] is largest, [2K-1] is smallest
        # Pair index i with index 2K - 1 - i
        
        total_price = 0
        for i in range(K):
            # Cake a
            s_a, x_a, y_a, z_a = top_2k[i]
            # Cake b
            s_b, x_b, y_b, z_b = top_2k[2*K - 1 - i]
            
            pair_price = max(x_a + x_b, y_a + y_b, z_a + z_b)
            total_price += pair_price
            
        results.append(str(total_price))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()