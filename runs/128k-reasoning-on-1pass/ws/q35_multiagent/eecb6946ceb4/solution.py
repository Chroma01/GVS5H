import sys
import numpy as np

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = list(map(int, input_data[1:]))
    
    if N < 3:
        print(0)
        return

    max_val = max(S)
    size = 1
    while size <= 2 * max_val:
        size *= 2
        
    a = np.zeros(size, dtype=np.float64)
    for x in S:
        a[x] = 1.0
        
    fa = np.fft.fft(a)
    fa *= fa
    res = np.fft.ifft(fa).real
    
    ans = 0
    for b in S:
        cnt = int(round(res[2 * b]))
        ans += (cnt - 1) // 2
        
    print(ans)

if __name__ == '__main__':
    solve()