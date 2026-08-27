import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A_str = ''.join(data[1:])
    length = 3 ** N
    A = A_str[:length]
    # convert to list of ints
    leaves = [int(c) for c in A]
    # initial DP for each leaf: (cost_to_output_0, cost_to_output_1)
    current = [(v, 1 - v) for v in leaves]
    
    INF = 10 ** 9
    # iteratively reduce the list by merging triples
    while len(current) > 1:
        new = []
        for i in range(0, len(current), 3):
            l, m, r = current[i], current[i+1], current[i+2]
            best0 = INF
            best1 = INF
            # enumerate 8 combinations of child outputs
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        cnt1 = a + b + c
                        # cost to achieve this combination
                        cost = (l[0] if a == 0 else l[1]) + \
                               (m[0] if b == 0 else m[1]) + \
                               (r[0] if c == 0 else r[1])
                        if cnt1 >= 2:  # majority 1
                            if cost < best1:
                                best1 = cost
                        else:  # majority 0
                            if cost < best0:
                                best0 = cost
            new.append((best0, best1))
        current = new
    
    root0, root1 = current[0]
    # determine current value (the one with zero cost)
    current_val = 0 if root0 == 0 else 1
    desired = 1 - current_val
    ans = root0 if desired == 0 else root1
    print(ans)

if __name__ == "__main__":
    solve()