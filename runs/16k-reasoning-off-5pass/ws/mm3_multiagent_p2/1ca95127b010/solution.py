import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = list(data[3].strip())
    T = list(data[4].strip())
    
    # Run-length encode S
    runs = []
    for c in S:
        c = int(c)
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    
    pos = 0
    ri = 0
    off = 0
    
    while pos < N:
        if S[pos] == T[pos]:
            pos += 1
            off += 1
            while ri < len(runs) and off >= runs[ri][1]:
                off -= runs[ri][1]
                ri += 1
            continue
        
        if ri + 1 >= len(runs):
            print("No")
            return
        
        # Split current run at pos to align window with run start
        if off > 0:
            cur_val, cur_len = runs[ri]
            runs.insert(ri+1, [cur_val, cur_len - off])
            runs[ri][1] = off
            ri += 1
            off = 0
        
        cur_val, cur_len = runs[ri]
        next_val, next_len = runs[ri+1]
        
        # Operation A: 0^X 1^Y -> 1^Y 0^X
        if cur_val == 0 and next_val == 1 and cur_len >= X and next_len >= Y:
            L = cur_len
            M = next_len
            new_runs = [[1, Y], [0, L - Y], [1, M]]
            runs[ri:ri+2] = new_runs
            # Merge with left neighbor
            if ri > 0 and runs[ri-1][0] == runs[ri][0]:
                runs[ri-1][1] += runs[ri][1]
                del runs[ri]
                ri -= 1
            # Merge with right neighbor (the one after the three new runs)
            if ri + 3 < len(runs) and runs[ri+2][0] == runs[ri+3][0]:
                runs[ri+2][1] += runs[ri+3][1]
                del runs[ri+3]
            pos += 1
            off = 1
            if off >= runs[ri][1]:
                off -= runs[ri][1]
                ri += 1
            continue
        
        # Operation B: 1^Y 0^X -> 0^X 1^Y
        if cur_val == 1 and next_val == 0 and cur_len >= Y and next_len >= X:
            M = cur_len
            L = next_len
            new_runs = [[0, X], [1, M], [0, L - X]]
            runs[ri:ri+2] = new_runs
            # Merge with left neighbor
            if ri > 0 and runs[ri-1][0] == runs[ri][0]:
                runs[ri-1][1] += runs[ri][1]
                del runs[ri]
                ri -= 1
            # Merge with right neighbor
            if ri + 3 < len(runs) and runs[ri+2][0] == runs[ri+3][0]:
                runs[ri+2][1] += runs[ri+3][1]
                del runs[ri+3]
            pos += 1
            off = 1
            if off >= runs[ri][1]:
                off -= runs[ri][1]
                ri += 1
            continue
        
        print("No")
        return
    
    # Verify final string matches T
    s_reconstructed = []
    for val, length in runs:
        s_reconstructed.extend([str(val)] * length)
    if ''.join(s_reconstructed) == ''.join(T):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()