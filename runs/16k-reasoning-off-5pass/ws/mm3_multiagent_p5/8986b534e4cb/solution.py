import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Q = int(next(it))
    # Store original (S_i, T_i) and normalized (L, R, dir)
    # dir = 0 if S < T (left-to-right), dir = 1 if S > T (right-to-left)
    people = []
    for i in range(M):
        s = int(next(it))
        t = int(next(it))
        if s < t:
            L, R, dir = s, t, 0
        else:
            L, R, dir = t, s, 1
        people.append((L, R, dir, s, t))
    queries = []
    for k in range(Q):
        l = int(next(it))
        r = int(next(it))
        queries.append((l, r))
    # For now, just output placeholder; will implement full algorithm next.
    # But we need to parse and store correctly.
    # We'll store people as list of tuples: (L, R, dir, orig_idx)
    # And queries as list of (L, R)
    # The next step is to build the forbidden adjacency graph.
    # Since we are only asked to parse input and store data structures, we stop here.
    # However, the problem requires solving the queries. Since the task says "Parse input and store data structures", we will just read and store, then exit.
    # But to be safe, we will output nothing or a dummy? The instruction says "Complete this task: Parse input and store data structures."
    # So we just parse and store, no output needed.
    pass

if __name__ == "__main__":
    solve()