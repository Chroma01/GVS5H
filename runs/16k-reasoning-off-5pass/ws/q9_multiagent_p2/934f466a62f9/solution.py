import sys

def solve():
    # Read all input from stdin at once for efficiency
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(num_test_cases):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
            
            # We need to collect X, Y, Z values separately
            X = []
            Y = []
            Z = []
            
            for _ in range(N):
                X.append(int(next(iterator)))
                Y.append(int(next(iterator)))
                Z.append(int(next(iterator)))
            
            # Sort each list in descending order to pick the largest values
            X.sort(reverse=True)
            Y.sort(reverse=True)
            Z.sort(reverse=True)
            
            # We need to select 2*K cakes.
            # The optimal strategy is to pick the 2*K cakes with the largest values
            # for a specific attribute (X, Y, or Z) and pair them up.
            # The total price for that attribute would be the sum of the values of these 2*K cakes.
            
            limit = 2 * K
            
            # Calculate sum of top 2*K elements for each attribute
            sum_x = sum(X[:limit])
            sum_y = sum(Y[:limit])
            sum_z = sum(Z[:limit])
            
            # The answer is the maximum of these three sums
            results.append(str(max(sum_x, sum_y, sum_z)))
            
        except StopIteration:
            break
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()