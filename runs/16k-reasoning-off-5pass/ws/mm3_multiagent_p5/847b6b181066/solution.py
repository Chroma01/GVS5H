import sys

def main():
    input = sys.stdin.readline
    N_R_C = input().split()
    while len(N_R_C) < 3:
        N_R_C += input().split()
    N, R, C = map(int, N_R_C)
    S = input().strip()
    
    # prefix sums: P[t] = (pr[t], pc[t]) after t steps
    pr = [0] * (N + 1)
    pc = [0] * (N + 1)
    dir_map = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}
    
    for i in range(1, N+1):
        dr, dc = dir_map[S[i-1]]
        pr[i] = pr[i-1] + dr
        pc[i] = pc[i-1] + dc
    
    # Compute generation times G: times t (0 <= t <= N) such that 
    # (pr[t], pc[t]) is a first occurrence among all prefix sums.
    is_generation = [False] * (N + 1)
    seen_prefix = set()
    is_generation[0] = True
    seen_prefix.add((0, 0))
    for t in range(1, N+1):
        p = (pr[t], pc[t])
        if p not in seen_prefix:
            is_generation[t] = True
            seen_prefix.add(p)
    
    # For each t from 1 to N, check if (pr[t]-R, pc[t]-C) is in 
    # the set of prefix sums at generation times g < t.
    seen_gen_prefix = set()
    seen_gen_prefix.add((0, 0))  # from generation time 0
    result = []
    for t in range(1, N+1):
        qr = pr[t] - R
        qc = pc[t] - C
        if (qr, qc) in seen_gen_prefix:
            result.append('1')
        else:
            result.append('0')
        if is_generation[t]:
            seen_gen_prefix.add((pr[t], pc[t]))
    
    print(''.join(result))

if __name__ == "__main__":
    main()