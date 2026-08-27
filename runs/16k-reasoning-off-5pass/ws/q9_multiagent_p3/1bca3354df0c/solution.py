import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list for the graph
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # We need to find the bipartition sizes for each connected component.
    # Since the graph has no odd cycles, it is bipartite.
    # We will use BFS to traverse each component and count the sizes of the two partitions.
    
    visited = [False] * (N + 1)
    colors = [0] * (N + 1)
    
    t_count = 0  # Count of components with odd total size (Type T)
    s_count = 0  # Count of components with even total size and odd partitions (Type S)
    
    for i in range(1, N + 1):
        if not visited[i]:
            # BFS to find component and partition sizes
            q = deque([i])
            visited[i] = True
            colors[i] = 0
            c0 = 0
            c1 = 0
            
            while q:
                u = q.popleft()
                if colors[u] == 0:
                    c0 += 1
                else:
                    c1 += 1
                
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        colors[v] = 1 - colors[u]
                        q.append(v)
            
            total = c0 + c1
            if total % 2 == 1:
                # Component size is odd -> Type T
                t_count += 1
            else:
                # Component size is even
                # If partitions are (odd, odd), it's Type S.
                # If partitions are (even, even), it's Type U.
                if c0 % 2 == 1:
                    s_count += 1
                # Else it's Type U (c0 even, c1 even)

    # Game Logic:
    # If N is odd, the final state must be a complete bipartite graph with partitions (odd, even) or (even, odd).
    # The number of edges in such a graph is even.
    # Total moves = Final Edges - M = Even - M.
    # Aoki wins if moves is odd => Even - M is odd => M is odd.
    # Wait, my previous derivation for N odd was:
    # If N is odd, Final Edges is always Even.
    # Moves = Even - M.
    # Aoki wins if Moves is Odd => M is Odd.
    # Takahashi wins if Moves is Even => M is Even.
    # BUT, looking at Sample 3 (N=9, M=5 -> Aoki), M is odd.
    # Sample 1 (N=4, M=3 -> Aoki), N is even.
    # Let's re-verify the N odd case logic.
    # If N is odd, can the final state be something else?
    # The game ends when the graph is a complete bipartite graph K_{X,Y}.
    # X+Y = N (odd). So one is odd, one is even. Product X*Y is even.
    # So Final Edges is always Even.
    # Moves = Even - M.
    # If M is odd, Moves is Odd -> Aoki wins.
    # If M is even, Moves is Even -> Takahashi wins.
    # So for N odd: Aoki wins if M is odd, Takahashi if M is even.
    #
    # HOWEVER, there is a nuance. Is it possible to have a terminal state that is NOT a complete bipartite graph?
    # No, because if it's not complete bipartite, there exists a pair (u,v) in different partitions that is not connected.
    # Adding that edge creates an even cycle (since they are in different partitions).
    # So the game MUST end at a complete bipartite graph.
    #
    # Wait, I might have missed a case where the game ends earlier?
    # "A player who cannot perform this operation loses".
    # Operation: Add edge (u,v) if no odd cycle created.
    # If graph is K_{X,Y}, adding any edge creates an odd cycle (triangle or larger odd cycle).
    # So K_{X,Y} is indeed a terminal state.
    #
    # So for N odd:
    #   If M % 2 == 1: Aoki
    #   Else: Takahashi
    #
    # But wait, Sample 3: N=9, M=5. Output Aoki. (Matches M odd).
    # What if N=3, M=0?
    #   N=3 (odd), M=0 (even). Logic says Takahashi.
    #   My manual trace for N=3, M=0 earlier concluded Takahashi.
    #   So this logic holds.
    #
    # Now for N even:
    #   If t_count > 0: Aoki wins. (Because Aoki can force the final parity to match her need).
    #   If t_count == 0:
    #     Final parity is determined by s_count parity.
    #     If s_count is odd -> Final Edges is Odd.
    #     If s_count is even -> Final Edges is Even.
    #     Moves = Final - M.
    #     Aoki wins if Moves is Odd.
    #     If s_count odd (Final Odd): Moves = Odd - M. Odd if M even.
    #     If s_count even (Final Even): Moves = Even - M. Odd if M odd.
    #     So Aoki wins if (s_count % 2) != (M % 2).
    
    if N % 2 == 1:
        if M % 2 == 1:
            print("Aoki")
        else:
            print("Takahashi")
    else:
        if t_count > 0:
            print("Aoki")
        else:
            if (s_count % 2) != (M % 2):
                print("Aoki")
            else:
                print("Takahashi")

if __name__ == '__main__':
    solve()