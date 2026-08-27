import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # positions: 1-indexed
    pos = [[] for _ in range(N + 2)]
    for i, x in enumerate(A, 1):
        pos[x].append(i)
    
    total = 0
    
    for v in range(1, N + 1):
        P = pos[v]
        if not P:
            continue
        Q = pos[v - 1] if v > 1 else []
        
        # Two pointers: pi for P, qi for Q
        pi = 0
        lenP = len(P)
        lenQ = len(Q)
        prev = 1
        qi = 0
        
        while True:
            if qi < lenQ:
                seg_L = prev
                seg_R = Q[qi] - 1
            else:
                seg_L = prev
                seg_R = N
            
            if seg_L <= seg_R:
                # skip v's before segment
                while pi < lenP and P[pi] < seg_L:
                    pi += 1
                if pi < lenP and P[pi] <= seg_R:
                    length = seg_R - seg_L + 1
                    total_sub = length * (length + 1) // 2
                    no_v = 0
                    first_v = P[pi]
                    no_v += (first_v - seg_L) * (first_v - seg_L + 1) // 2
                    prev_v = first_v
                    pi += 1
                    while pi < lenP and P[pi] <= seg_R:
                        cur_v = P[pi]
                        gap = cur_v - prev_v - 1
                        no_v += gap * (gap + 1) // 2
                        prev_v = cur_v
                        pi += 1
                    gap = seg_R - prev_v
                    no_v += gap * (gap + 1) // 2
                    total += total_sub - no_v
            
            if qi < lenQ:
                prev = Q[qi] + 1
                qi += 1
            else:
                break
    
    print(total)

if __name__ == "__main__":
    solve()