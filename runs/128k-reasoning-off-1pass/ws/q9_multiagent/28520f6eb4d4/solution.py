import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    X = []
    H = []
    
    for _ in range(N):
        X.append(int(next(iterator)))
        H.append(int(next(iterator)))

    # If N=1, building 1 is always visible from any h>=0 because there are no buildings in between.
    # So at h=0, it is visible. Thus answer is -1.
    if N == 1:
        print("-1")
        return

    # We need to find the minimum height h such that ALL buildings are visible.
    # Let this be H_min_all. If H_min_all <= 0, output -1.
    # Otherwise, the answer is H_min_all.
    # The problem asks for the maximum height from which it is NOT possible to see all buildings.
    # This is exactly H_min_all (the threshold). If h < H_min_all, not all are visible.
    # If h >= H_min_all, all are visible.
    # So the max h where not all are visible is H_min_all (exclusive of the "all visible" state? 
    # Actually, the question implies the boundary. "From which it is not possible".
    # If at height T, all are visible, then at T-epsilon, not all are visible.
    # The critical value is T. The answer is T.
    # If T <= 0, then at h=0, all are visible -> -1.
    
    # Algorithm:
    # For each building i, we need to find the minimum h such that building i is visible.
    # Building i is visible if for all j < i, the line from (0, h) to (X_i, H_i) passes above (X_j, H_j).
    # This gives a lower bound on h for each j < i: h >= (H_j * X_i - H_i * X_j) / (X_i - X_j).
    # Let this bound be B(i, j). We need h >= max_{j < i} B(i, j).
    # Let M_i = max_{j < i} B(i, j). If M_i <= 0, then building i is visible at h=0.
    # The condition "all buildings visible" requires h >= max_i M_i.
    # Let Global_M = max_i M_i.
    # If Global_M <= 0, output -1.
    # Else output Global_M.
    
    # To compute M_i efficiently for all i:
    # We maintain the "upper convex hull" of the buildings seen so far.
    # The function representing the intercept is unimodal on the upper convex hull, allowing us to use ternary search.
    
    hull = [] # stores indices
    G_num = 0
    G_den = 1
    
    for i in range(N):
        # Ternary search on hull to find max intercept
        L, R = 0, len(hull) - 1
        best_j = -1
        best_num = -1
        best_den = 1
        
        if len(hull) == 0:
            # Should not happen for i > 0 if we push i at end of loop
            # But for i=0, hull is empty. M_0 = 0.
            pass
        elif len(hull) == 1:
            best_j = hull[0]
            best_num = H[best_j] * X[i] - H[i] * X[best_j]
            best_den = X[i] - X[best_j]
        else:
            # Ternary search
            while R - L > 2:
                m1 = L + (R - L) // 3
                m2 = R - (R - L) // 3
                # Compare f(m1) and f(m2)
                # f(j) = num / den
                # num1 * den2 vs num2 * den1
                num1 = H[hull[m1]] * X[i] - H[i] * X[hull[m1]]
                den1 = X[i] - X[hull[m1]]
                num2 = H[hull[m2]] * X[i] - H[i] * X[hull[m2]]
                den2 = X[i] - X[hull[m2]]
                
                # We want to maximize.
                # If f(m1) > f(m2), then peak is in [m1, R]
                # If f(m1) < f(m2), then peak is in [L, m2]
                if num1 * den2 > num2 * den1:
                    L = m1
                else:
                    R = m2
            
            # Check range [L, R]
            for j in range(L, R + 1):
                idx = hull[j]
                num = H[idx] * X[i] - H[i] * X[idx]
                den = X[i] - X[idx]
                if best_j == -1:
                    best_j = idx
                    best_num = num
                    best_den = den
                else:
                    # Compare num/den with best_num/best_den
                    if num * best_den > best_num * den:
                        best_j = idx
                        best_num = num
                        best_den = den
        
        if best_j != -1:
            # M_i = best_num / best_den
            # We need to update G if M_i > G
            # M_i > G <=> best_num/best_den > G_num/G_den
            # <=> best_num * G_den > G_num * best_den
            # Also, if M_i <= 0, it doesn't increase the required h (since h>=0).
            # But G starts at 0. If M_i < 0, it's not > 0.
            # So we only update if best_num * G_den > G_num * best_den.
            
            if best_num * G_den > G_num * best_den:
                G_num = best_num
                G_den = best_den
        
        # Update hull
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            # slope(a, b) >= slope(b, i)
            # (H[b]-H[a])/(X[b]-X[a]) >= (H[i]-H[b])/(X[i]-X[b])
            # (H[b]-H[a]) * (X[i]-X[b]) >= (H[i]-H[b]) * (X[b]-X[a])
            if (H[b] - H[a]) * (X[i] - X[b]) >= (H[i] - H[b]) * (X[b] - X[a]):
                hull.pop()
            else:
                break
        hull.append(i)
    
    if G_num <= 0:
        print("-1")
    else:
        print(f"{G_num / G_den:.20f}")

if __name__ == '__main__':
    solve()