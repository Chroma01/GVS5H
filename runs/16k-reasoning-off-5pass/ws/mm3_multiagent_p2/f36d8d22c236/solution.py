import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    
    target = [-1] * 26
    # Check consistency and record required target for each letter
    for i in range(N):
        s = ord(S[i]) - 97
        t = ord(T[i]) - 97
        if s == t:
            continue
        if target[s] == -1:
            target[s] = t
        elif target[s] != t:
            print(-1)
            return
    
    # Count edges (letters that must change)
    k = 0
    for c in range(26):
        if target[c] != -1 and target[c] != c:
            k += 1
    
    # Count cycles in the directed graph
    visited = [False] * 26
    cycles = 0
    for start in range(26):
        if visited[start]:
            continue
        cur = start
        path_set = set()
        path_list = []
        while True:
            if visited[cur]:
                # Reached an already processed component
                for node in path_list:
                    visited[node] = True
                break
            if cur in path_set:
                # Found a cycle
                cycles += 1
                for node in path_list:
                    visited[node] = True
                break
            path_set.add(cur)
            path_list.append(cur)
            nxt = target[cur]
            if nxt == -1 or nxt == cur:
                # No outgoing edge or self-loop
                for node in path_list:
                    visited[node] = True
                break
            cur = nxt
    
    print(k + cycles)

if __name__ == "__main__":
    solve()