import sys
from bisect import bisect_left, bisect_right

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    Q = int(next(iterator))
    
    A = [int(next(iterator)) for _ in range(N)]
    
    queries = []
    for i in range(Q):
        R = int(next(iterator))
        X = int(next(iterator))
        queries.append((R, X, i))
        
    # Sort queries by R to process them offline
    queries.sort(key=lambda x: x[0])
    
    tails = []
    answers = [0] * Q
    
    q_idx = 0
    for i in range(N):
        x = A[i]
        # Update tails for strictly increasing LIS
        # bisect_left finds the first element >= x, which we replace
        pos = bisect_left(tails, x)
        if pos < len(tails):
            tails[pos] = x
        else:
            tails.append(x)
            
        # Answer all queries ending at current position
        while q_idx < Q and queries[q_idx][0] == i + 1:
            _, X, orig_idx = queries[q_idx]
            # tails[k] is the smallest ending element of an increasing subsequence of length k+1.
            # Since tails is strictly increasing, the number of elements <= X 
            # gives the maximum length L such that there exists an increasing subsequence 
            # of length L ending with a value <= X. All previous elements are smaller, 
            # so they are also <= X.
            answers[orig_idx] = bisect_right(tails, X)
            q_idx += 1
            
    print('\n'.join(map(str, answers)))

if __name__ == '__main__':
    solve()