import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        m_str = next(iterator)
        N = int(n_str)
        M = int(m_str)
        
        # Consume the rest of the input (edges) just in case, 
        # though we don't need to process them for the logic derived.
        # The problem guarantees M edges follow.
        for _ in range(M):
            next(iterator)
            next(iterator)
            
        # The game is equivalent to a Nim pile of size K = floor(N^2 / 4) - M.
        # The maximum number of edges in a bipartite graph with N vertices is floor(N^2 / 4).
        # Since the game must end when the graph becomes a single complete bipartite component,
        # the total number of moves is fixed regardless of strategy.
        
        max_edges = (N * N) // 4
        diff = max_edges - M
        
        if diff % 2 == 1:
            print("Aoki")
        else:
            print("Takahashi")
            
    except StopIteration:
        pass

if __name__ == '__main__':
    solve()