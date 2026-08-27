import sys
from bisect import bisect_right

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        queries = []
        for i in range(Q):
            R = int(next(iterator))
            X = int(next(iterator))
            # Store as (R, X, original_index)
            queries.append((R, X, i))
            
    except StopIteration:
        return

    # Sort queries by R (1-based index in problem)
    # This allows us to process the array A linearly and answer queries offline
    queries.sort(key=lambda x: x[0])
    
    # 'tails' list will store the smallest ending element of an increasing subsequence of length k+1 at index k.
    # This list is always sorted in strictly increasing order.
    tails = []
    
    # Array to store answers for each query in the original order
    answers = [0] * Q
    
    query_idx = 0
    num_queries = len(queries)
    
    # Process array A from left to right (index i from 0 to N-1)
    # The prefix length corresponding to index i is R = i + 1
    for i in range(N):
        val = A[i]
        
        # Update the 'tails' array for the current element 'val'
        # We want to find the longest increasing subsequence we can extend with 'val'.
        # bisect_right returns the index of the first element > val.
        # This index represents the length of the longest increasing subsequence 
        # ending with a value <= val.
        pos = bisect_right(tails, val)
        
        if pos < len(tails):
            # If we found a smaller ending value for a subsequence of length (pos+1), update it.
            # This maintains the property that tails[k] is the smallest ending value for length k+1.
            tails[pos] = val
        else:
            # If pos == len(tails), it means 'val' extends the longest increasing subsequence found so far.
            tails.append(val)
            
        # Answer all queries that have R = i + 1
        while query_idx < num_queries and queries[query_idx][0] == i + 1:
            R, X, original_idx = queries[query_idx]
            
            # The problem asks for the max length of an increasing subsequence in A[1...R]
            # where all elements are <= X.
            # Since 'tails' stores the smallest ending values for each length,
            # if tails[k] <= X, it implies there exists an increasing subsequence of length k+1
            # where the last element is <= X. Because the subsequence is strictly increasing,
            # all preceding elements are also < tails[k] <= X.
            # Thus, the answer is the count of elements in 'tails' that are <= X.
            # Since 'tails' is sorted, we use bisect_right to find this count.
            ans = bisect_right(tails, X)
            answers[original_idx] = ans
            
            query_idx += 1
            
    # Print all answers in the original order
    for ans in answers:
        print(ans)

if __name__ == '__main__':
    solve()