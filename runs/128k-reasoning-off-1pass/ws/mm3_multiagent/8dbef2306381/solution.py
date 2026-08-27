from collections import deque
import sys
from math import gcd

def main():
    input = sys.stdin.readline
    N, M, A, B = map(int, input().split())
    L = []
    R = []
    for _ in range(M):
        l, r = map(int, input().split())
        L.append(l)
        R.append(r)

    # Precompute representable distances
    max_check = 5000
    rep = [False] * (max_check + B + 1)
    rep[0] = True
    q = deque([0])
    while q:
        x = q.popleft()
        for d in range(A, B + 1):
            y = x + d
            if y <= max_check and not rep[y]:
                rep[y] = True
                q.append(y)
    # Find threshold T: smallest index such that all rep[T:T+B] are True
    T = None
    for i in range(max_check + 1):
        if i + B <= len(rep) and all(rep[i:i + B]):
            T = i
            break
    if T is None:
        T = max_check + 1

    def is_representable(D):
        if D < 0:
            return False
        if D <= max_check:
            return rep[D]
        return D >= T

    if M == 0:
        if is_representable(N - 1):
            print("Yes")
        else:
            print("No")
        return

    # Build good intervals
    goods = []
    goods.append((1, L[0] - 1))
    for i in range(M - 1):
        goods.append((R[i] + 1, L[i + 1] - 1))
    goods.append((R[M - 1] + 1, N))

    # Step 0: compute reachable positions in the tail of goods[0]
    wi_start = max(goods[0][0], goods[1][0] - B)
    wi_end = goods[0][1]
    cur = set()
    for x in range(wi_start, wi_end + 1):
        if is_representable(x - 1):
            cur.add(x)
    if not cur:
        print("No")
        return

    # Process intermediate good intervals
    for i in range(1, M):
        gi_start, gi_end = goods[i]
        wi_start = max(gi_start, goods[i + 1][0] - B)
        wi_end = gi_end

        # Compute entry positions into goods[i] from cur
        entry = set()
        for x in cur:
            for d in range(A, B + 1):
                y = x + d
                if gi_start <= y <= gi_end:
                    entry.add(y)
        if not entry:
            print("No")
            return

        # Compute reachable positions in the tail of goods[i]
        next_cur = set()
        for y in range(wi_start, wi_end + 1):
            found = False
            for s in entry:
                if y >= s and is_representable(y - s):
                    found = True
                    break
            if found:
                next_cur.add(y)
        if not next_cur:
            print("No")
            return
        cur = next_cur

    # Process the last good interval
    gm_start, gm_end = goods[M]
    entry = set()
    for x in cur:
        for d in range(A, B + 1):
            y = x + d
            if gm_start <= y <= gm_end:
                entry.add(y)
    if not entry:
        print("No")
        return
    if N in entry:
        print("Yes")
        return
    check_start = max(gm_start, N - B)
    for y in range(check_start, N):
        for s in entry:
            if y >= s and is_representable(y - s):
                print("Yes")
                return
    print("No")

if __name__ == "__main__":
    main()