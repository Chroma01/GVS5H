import sys

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        N = int(input())
        A = input().strip()
        B = input().strip()
        a = [i+1 for i, c in enumerate(A) if c == '1']
        b = [i+1 for i, c in enumerate(B) if c == '1']
        m = len(a)
        k = len(b)
        if m < k:
            print(-1)
            continue
        
        def check(D):
            idx = 0  # next uncovered b index
            any_ptr = 0  # pointer for any b >= L
            prev = 0
            for i in range(m):
                L = max(a[i] - D, prev)
                R = a[i] + D
                if L > R:
                    return False
                # try to cover an uncovered b
                while idx < k and b[idx] < L:
                    idx += 1
                if idx < k and b[idx] <= R:
                    chosen = b[idx]
                    idx += 1
                else:
                    # find any b in [L, R]
                    while any_ptr < k and b[any_ptr] < L:
                        any_ptr += 1
                    if any_ptr == k or b[any_ptr] > R:
                        return False
                    chosen = b[any_ptr]
                prev = chosen
            return idx == k
        
        lo, hi = 0, N
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid):
                hi = mid
            else:
                lo = mid + 1
        print(lo)

if __name__ == "__main__":
    solve()