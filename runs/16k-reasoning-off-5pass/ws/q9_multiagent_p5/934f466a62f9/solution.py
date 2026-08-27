import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
            
            # Read N cakes
            # Each cake has X, Y, Z
            # We will store them as a list of tuples
            cakes = []
            for _ in range(N):
                x = int(next(iterator))
                y = int(next(iterator))
                z = int(next(iterator))
                cakes.append((x, y, z))
            
            max_total_price = 0
            
            # The problem asks us to select 2K items and pair them to maximize the sum of max(X_a+X_b, Y_a+Y_b, Z_a+Z_b).
            # A known strategy for this specific problem structure is to iterate over the attribute (X, Y, or Z)
            # that "dominates" the selection. For a fixed attribute, we select the top 2K items with the highest values
            # of that attribute and pair them greedily (largest with second largest, etc.).
            # We calculate the actual total price for this pairing (using max of all three attributes for each pair)
            # and update the global maximum.
            
            # Attributes: 0 -> X, 1 -> Y, 2 -> Z
            for attr_idx in range(3):
                # Create a list of indices to sort
                indices = list(range(N))
                
                # Sort indices based on the attribute value in descending order
                if attr_idx == 0:
                    indices.sort(key=lambda i: cakes[i][0], reverse=True)
                elif attr_idx == 1:
                    indices.sort(key=lambda i: cakes[i][1], reverse=True)
                else:
                    indices.sort(key=lambda i: cakes[i][2], reverse=True)
                
                # Take top 2K
                top_2k_indices = indices[:2*K]
                
                current_total = 0
                # Pair adjacent elements in the sorted list
                for i in range(0, 2*K, 2):
                    idx1 = top_2k_indices[i]
                    idx2 = top_2k_indices[i+1]
                    
                    x1, y1, z1 = cakes[idx1]
                    x2, y2, z2 = cakes[idx2]
                    
                    # Calculate price for this pair based on the actual max rule
                    price = max(x1 + x2, y1 + y2, z1 + z2)
                    current_total += price
                
                if current_total > max_total_price:
                    max_total_price = current_total
            
            print(max_total_price)
            
        except StopIteration:
            break

if __name__ == '__main__':
    solve()