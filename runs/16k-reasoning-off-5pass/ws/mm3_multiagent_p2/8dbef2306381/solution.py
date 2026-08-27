import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    bad = []
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        bad.append((L, R))
    
    right = 1
    for i, (L, R) in enumerate(bad):
        # Try to extend right to L-1 if we are before the bad zone
        if right < L:
            # We can reach L-1 only if the gap is large enough
            if right + A <= L - 1:
                right = L - 1
            # else: right remains, we will try to jump over from current position
        
        # Determine the start of the next bad zone to clamp our landing
        if i + 1 < M:
            L_next = bad[i + 1][0]
        else:
            L_next = N + 1
        
        # Check if we can clear the current bad zone
        if right + B < R + 1:
            print("No")
            return
        
        # Land at the farthest safe square: max(R+1, ...), but clamped to before next bad zone
        # Actually we can land anywhere in [max(right+A, R+1), min(right+B, L_next-1)]
        # The maximum possible is min(right+B, L_next-1)
        new_right = min(right + B, L_next - 1)
        # Ensure we don't land inside the current bad zone (should be guaranteed by R+1 condition and L_next > R)
        if new_right < R + 1:
            # This would mean we cannot land past the bad zone without entering the next one,
            # but we can still try to land further if possible? Actually if new_right < R+1, we are stuck.
            # However, with the condition right+B >= R+1, new_right >= R+1 always if L_next-1 >= R+1.
            # If L_next-1 < R+1, that means the next bad zone starts before R+1, impossible since bad zones are disjoint.
            pass
        right = new_right
    
    # After processing all bad zones, check if we can reach N
    if right >= N:
        print("Yes")
    elif right + A <= N:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()