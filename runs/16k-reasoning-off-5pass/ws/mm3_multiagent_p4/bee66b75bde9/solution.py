import sys

def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    black_cells = []  # (x, y)
    white_cells = []  # (x, y)
    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'B':
            black_cells.append((x, y))
        else:
            white_cells.append((x, y))
    
    # Sort by y descending
    black_cells.sort(key=lambda p: p[1], reverse=True)
    white_cells.sort(key=lambda p: p[1], reverse=True)
    
    max_row = 0
    i = 0
    nb = len(black_cells)
    nw = len(white_cells)
    
    for x, y in white_cells:
        # Add all black cells with y >= current y
        while i < nb and black_cells[i][1] >= y:
            if black_cells[i][0] > max_row:
                max_row = black_cells[i][0]
            i += 1
        if max_row >= x:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    main()