import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        x = []
        for _ in range(n):
            x.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem asks to minimize the sum of coordinates.
    # The operation allows us to swap the differences d_i and d_{i+2} (where d_k = x_{k+1} - x_k)
    # if d_i > d_{i+2}. This operation reduces the total sum.
    # Since the operation only affects d_i and d_{i+2} and leaves d_{i+1} unchanged,
    # we can independently sort the subsequence of differences at odd indices (1-based)
    # and the subsequence of differences at even indices (1-based).
    
    # Calculate initial differences
    # d[i] corresponds to x[i+1] - x[i] for i from 0 to n-2
    # In 1-based indexing logic: d_1, d_2, ..., d_{N-1}
    # Here we use 0-based list d where d[i] is the difference between x[i+1] and x[i]
    # So d[0] is d_1, d[1] is d_2, etc.
    
    d = []
    for i in range(n - 1):
        d.append(x[i+1] - x[i])
    
    # Separate into odd and even positions (1-based)
    # 1-based odd positions (1, 3, 5...) correspond to 0-based indices (0, 2, 4...)
    # 1-based even positions (2, 4, 6...) correspond to 0-based indices (1, 3, 5...)
    
    odd_pos_d = [] # Stores d_1, d_3, d_5...
    even_pos_d = [] # Stores d_2, d_4, d_6...
    
    for i in range(len(d)):
        # i is 0-based index. 1-based index is i+1.
        if (i + 1) % 2 == 1: 
            odd_pos_d.append(d[i])
        else:
            even_pos_d.append(d[i])
            
    # Sort both lists in ascending order to satisfy d_i <= d_{i+2} for all i
    odd_pos_d.sort()
    even_pos_d.sort()
    
    # Reconstruct the difference array with sorted values
    new_d = []
    idx_odd = 0
    idx_even = 0
    
    for i in range(len(d)):
        if (i + 1) % 2 == 1:
            new_d.append(odd_pos_d[idx_odd])
            idx_odd += 1
        else:
            new_d.append(even_pos_d[idx_even])
            idx_even += 1
            
    # Calculate the final sum of coordinates efficiently
    # Sum = N * x[0] + sum_{j=0}^{N-2} (N - 1 - j) * new_d[j]
    # Explanation:
    # x[0] is the first element.
    # x[k] = x[0] + sum(new_d[0]...new_d[k-1])
    # Sum = sum_{k=0}^{N-1} x[k]
    #     = N * x[0] + sum_{j=0}^{N-2} new_d[j] * (number of times new_d[j] contributes to the sum)
    #     = N * x[0] + sum_{j=0}^{N-2} new_d[j] * (N - 1 - j)
    
    total_sum = n * x[0]
    for j in range(len(new_d)):
        total_sum += new_d[j] * (n - 1 - j)
        
    print(total_sum)

if __name__ == '__main__':
    solve()