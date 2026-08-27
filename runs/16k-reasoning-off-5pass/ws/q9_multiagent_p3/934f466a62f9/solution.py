import sys

def solve():
    # Read all input from stdin at once for efficiency
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        t_str = next(iterator)
    except StopIteration:
        return
        
    T = int(t_str)
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
            
            # We need to store X, Y, Z separately to sort them independently
            # Reading N lines, each having 3 integers
            X = [0] * N
            Y = [0] * N
            Z = [0] * N
            
            for i in range(N):
                X[i] = int(next(iterator))
                Y[i] = int(next(iterator))
                Z[i] = int(next(iterator))
            
            # Helper function to calculate max sum for a specific attribute
            # Strategy: Sort the attribute values in descending order and pair adjacent elements.
            # This maximizes the sum of sums for that specific attribute.
            def get_max_sum(arr):
                # Sort in descending order
                arr.sort(reverse=True)
                current_sum = 0
                # Greedily pair adjacent elements: (0,1), (2,3), ...
                # We need K pairs, so we iterate K times
                for i in range(K):
                    current_sum += arr[2*i] + arr[2*i+1]
                return current_sum
            
            # Calculate max possible sum assuming each attribute is the dominant one
            # The problem property states that the optimal solution is dominated by one of the three attributes globally.
            ans = max(get_max_sum(X), get_max_sum(Y), get_max_sum(Z))
            results.append(str(ans))
            
        except StopIteration:
            break
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()