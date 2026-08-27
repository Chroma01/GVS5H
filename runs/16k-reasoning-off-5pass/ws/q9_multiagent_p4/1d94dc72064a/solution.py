import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Count the number of elements equal to 1
    cnt1 = 0
    for x in A:
        if x == 1:
            cnt1 += 1
            
    # Logic derived from game theory analysis:
    # 1. If N is even, Snuke always wins.
    # 2. If N is odd:
    #    a. If N == 1, Fennec always wins (game ends in 1 move).
    #    b. If N > 1:
    #       i. If there is at least one A_i == 1, Fennec wins.
    #       ii. If all A_i >= 2, Snuke wins.
    
    if N % 2 == 0:
        print("Snuke")
    else:
        if N == 1:
            print("Fennec")
        else:
            if cnt1 > 0:
                print("Fennec")
            else:
                print("Snuke")

if __name__ == '__main__':
    solve()