import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    A = list(map(int, data[idx:idx+N])); idx += N
    B = list(map(int, data[idx:idx+N])); idx += N
    P = list(map(int, data[idx:idx+N])); idx += N
    Q = list(map(int, data[idx:idx+N])); idx += N

    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]

    def forced_set(perm, balls):
        # Walk the cycle containing X in the permutation `perm`.
        pos = {}
        order = []
        cur = X
        while cur not in pos:
            pos[cur] = len(order)
            order.append(cur)
            cur = perm[cur]
        L = len(order)
        in_cycle = pos  # node -> position, only for nodes in X's cycle

        min_pos = None
        for i in range(N):
            if balls[i] and i != X:
                if i not in in_cycle:
                    return None  # impossible
                p = in_cycle[i]
                if min_pos is None or p < min_pos:
                    min_pos = p
        result = set()
        if min_pos is not None:
            # forced nodes are order[min_pos .. L-1] (X is order[0], excluded)
            for j in range(min_pos, L):
                result.add(order[j])
        return result

    red = forced_set(P, A)
    if red is None:
        print(-1)
        return
    blue = forced_set(Q, B)
    if blue is None:
        print(-1)
        return

    print(len(red | blue))

main()