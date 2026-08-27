import sys

def solve():
    # Read all input from stdin at once for efficiency
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
        except StopIteration:
            break
            
        X = []
        Y = []
        Z = []
        
        for _ in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            z = int(next(iterator))
            X.append(x)
            Y.append(y)
            Z.append(z)
            
        # Helper function to calculate max score for a specific attribute
        def calculate_max_score(arr, k):
            # Sort in descending order to pick the largest elements
            arr.sort(reverse=True)
            
            # We only consider the top 2*K elements
            limit = 2 * k
            total = 0
            
            # Pair the largest with the second largest, third with fourth, etc.
            # Since the array is sorted descending, arr[i] + arr[i+1] is the optimal
            # pairing for the subset of top 2*K elements to maximize the sum of sums.
            for i in range(0, limit, 2):
                total += arr[i] + arr[i+1]
            return total

        ans_x = calculate_max_score(X, K)
        ans_y = calculate_max_score(Y, K)
        ans_z = calculate_max_score(Z, K)
        
        # The answer is the maximum of the scores obtained by considering each attribute independently
        results.append(str(max(ans_x, ans_y, ans_z)))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()