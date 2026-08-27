import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    Y = int(next(it))
    S = list(next(it).strip())
    T = next(it).strip()
    
    # Count zeros and ones
    if S.count('0') != T.count('0') or S.count('1') != T.count('1'):
        print("No")
        return
    
    # Deques to track current positions of zeros and ones
    q0 = deque()
    q1 = deque()
    
    # We process from left to right
    for i in range(N):
        # Add current index to appropriate deque based on current S
        if S[i] == '0':
            q0.append(i)
        else:
            q1.append(i)
        
        # Remove indices that are behind the current position
        while q0 and q0[0] < i:
            q0.popleft()
        while q1 and q1[0] < i:
            q1.popleft()
        
        # Determine current character at i
        curr = S[i]
        
        # If matches, continue
        if curr == T[i]:
            continue
        
        # Mismatch: need to apply operation
        if curr == '0' and T[i] == '1':
            # Operation A: X zeros followed by Y ones -> X ones followed by Y zeros
            if len(q0) < X:
                print("No")
                return
            if q0[X-1] != i + X - 1:
                print("No")
                return
            
            if i + X + Y > N:
                print("No")
                return
            if len(q1) < Y:
                print("No")
                return
            if q1[Y-1] != i + X + Y - 1:
                print("No")
                return
            
            # Apply operation A
            for _ in range(X):
                q0.popleft()
            for k in range(Y):
                q0.append(i + X + k)
            for k in range(X):
                q1.append(i + k)
            for k in range(X):
                S[i+k] = '1'
            for k in range(Y):
                S[i+X+k] = '0'
            
        elif curr == '1' and T[i] == '0':
            # Operation B: Y ones followed by X zeros -> Y zeros followed by X ones
            if len(q1) < Y:
                print("No")
                return
            if q1[Y-1] != i + Y - 1:
                print("No")
                return
            
            if i + Y + X > N:
                print("No")
                return
            if len(q0) < X:
                print("No")
                return
            if q0[X-1] != i + Y + X - 1:
                print("No")
                return
            
            # Apply operation B
            for _ in range(Y):
                q1.popleft()
            for k in range(X):
                q1.append(i + Y + k)
            for k in range(Y):
                q0.append(i + k)
            for k in range(Y):
                S[i+k] = '0'
            for k in range(X):
                S[i+Y+k] = '1'
        else:
            print("No")
            return
    
    if ''.join(S) == T:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()