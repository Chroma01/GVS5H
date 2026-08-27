import sys
from collections import defaultdict

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N-1)]
    
    per_prime = defaultdict(list)
    for a in A:
        x = a
        d = 2
        local = {}
        while d * d <= x:
            while x % d == 0:
                local[d] = local.get(d, 0) + 1
                x //= d
            d += 1
        if x > 1:
            local[x] = local.get(x, 0) + 1
        for p, e in local.items():
            per_prime[p].append(e)
    
    total = 1
    for p, a_list in per_prime.items():
        H = sum(a_list)
        if H == 0:
            continue
        
        pow_p = [1] * (H + 1)
        for h in range(1, H + 1):
            pow_p[h] = pow_p[h-1] * p % MOD
        
        dp_touch = [0] * (H + 1)
        dp_notouch = [0] * (H + 1)
        for h in range(H + 1):
            if h == 0:
                dp_touch[0] = 1
            else:
                dp_notouch[h] = pow_p[h]
        
        for a in a_list:
            new_touch = [0] * (H + 1)
            new_notouch = [0] * (H + 1)
            for h in range(H + 1):
                if dp_touch[h] == 0 and dp_notouch[h] == 0:
                    continue
                # up move
                nh = h + a
                if nh <= H:
                    w = pow_p[nh]
                    if dp_touch[h]:
                        new_touch[nh] = (new_touch[nh] + dp_touch[h] * w) % MOD
                    if dp_notouch[h]:
                        new_notouch[nh] = (new_notouch[nh] + dp_notouch[h] * w) % MOD
                # down move
                nh = h - a
                if nh >= 0:
                    w = pow_p[nh]
                    if dp_touch[h]:
                        new_touch[nh] = (new_touch[nh] + dp_touch[h] * w) % MOD
                    if dp_notouch[h]:
                        if nh == 0:
                            new_touch[nh] = (new_touch[nh] + dp_notouch[h] * w) % MOD
                        else:
                            new_notouch[nh] = (new_notouch[nh] + dp_notouch[h] * w) % MOD
            dp_touch, dp_notouch = new_touch, new_notouch
        
        prime_sum = 0
        for h in range(H + 1):
            prime_sum = (prime_sum + dp_touch[h]) % MOD
        total = total * prime_sum % MOD
    
    print(total)

if __name__ == "__main__":
    solve()