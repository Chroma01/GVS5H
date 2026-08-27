import sys

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        N, K = map(int, input().split())
        X = [0]*N
        Y = [0]*N
        Z = [0]*N
        for i in range(N):
            x, y, z = map(int, input().split())
            X[i] = x
            Y[i] = y
            Z[i] = z
        R = 2 * K
        items = []
        for i in range(N):
            x, y, z = X[i], Y[i], Z[i]
            m = x
            c = 0
            if y > m:
                m = y
                c = 1
            if z > m:
                m = z
                c = 2
            items.append((m, c, i))
        items.sort(key=lambda t: -t[0])
        S_indices = set()
        S_items = items[:R]
        T_sum = 0
        cnt = [0, 0, 0]
        for m, c, i in S_items:
            S_indices.add(i)
            if c == 0:
                T_sum += X[i]
            elif c == 1:
                T_sum += Y[i]
            else:
                T_sum += Z[i]
            cnt[c] += 1
        parity = [cnt[0] % 2, cnt[1] % 2, cnt[2] % 2]
        if parity == [0, 0, 0]:
            print(T_sum)
            continue
        odd = []
        for c in range(3):
            if parity[c] == 1:
                odd.append(c)
        a, b = odd[0], odd[1]
        INF = 10**18
        min1 = INF
        min2 = INF
        min_v_a = INF
        min_v_b = INF
        vals = [X, Y, Z]
        for m, c, i in S_items:
            if c == a:
                loss = vals[a][i] - vals[b][i]
                if loss < min1:
                    min1 = loss
                if vals[a][i] < min_v_a:
                    min_v_a = vals[a][i]
            elif c == b:
                loss = vals[b][i] - vals[a][i]
                if loss < min2:
                    min2 = loss
                if vals[b][i] < min_v_b:
                    min_v_b = vals[b][i]
        max_a_notS = -1
        max_b_notS = -1
        for i in range(N):
            if i not in S_indices:
                if vals[a][i] > max_a_notS:
                    max_a_notS = vals[a][i]
                if vals[b][i] > max_b_notS:
                    max_b_notS = vals[b][i]
        min3 = INF
        min4 = INF
        if min_v_a != INF and max_b_notS != -1:
            min3 = min_v_a - max_b_notS
        if min_v_b != INF and max_a_notS != -1:
            min4 = min_v_b - max_a_notS
        best_loss = min(min1, min2, min3, min4)
        print(T_sum - best_loss)

if __name__ == "__main__":
    solve()