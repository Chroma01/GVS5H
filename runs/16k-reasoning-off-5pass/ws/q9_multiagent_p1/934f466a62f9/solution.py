import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin at once for efficiency
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
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
            
            # Store cakes as tuples (x, y, z) for slightly better performance than dicts
            cakes = []
            for _ in range(N):
                x = int(next(iterator))
                y = int(next(iterator))
                z = int(next(iterator))
                cakes.append((x, y, z))
                
            # Helper function to calculate score assuming we sort by a specific attribute
            def calculate_score(cakes, key_idx):
                # Sort by the specified key index in descending order
                # key_idx: 0 for X, 1 for Y, 2 for Z
                cakes_sorted = sorted(cakes, key=lambda c: c[key_idx], reverse=True)
                
                total_price = 0
                # We need to form K pairs. The greedy strategy pairs adjacent elements
                # in the sorted list: (0,1), (2,3), ..., (2K-2, 2K-1)
                # We only need to consider the first 2*K elements
                limit = 2 * K
                for i in range(0, limit, 2):
                    c1 = cakes_sorted[i]
                    c2 = cakes_sorted[i+1]
                    
                    sum_x = c1[0] + c2[0]
                    sum_y = c1[1] + c2[1]
                    sum_z = c1[2] + c2[2]
                    
                    total_price += max(sum_x, sum_y, sum_z)
                return total_price

            # Calculate scores for X, Y, and Z dominance scenarios
            ans_x = calculate_score(cakes, 0)
            ans_y = calculate_score(cakes, 1)
            ans_z = calculate_score(cakes, 2)
            
            results.append(str(max(ans_x, ans_y, ans_z)))
            
        except StopIteration:
            break
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()