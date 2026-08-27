import sys
import threading
import heapq
from collections import defaultdict

def main():
    sys.setrecursionlimit(1 << 25)
    H, W = map(int, sys.stdin.readline().split())
    F = [list(map(int, sys.stdin.readline().split())) for _ in range(H)]
    Q = int(sys.stdin.readline())
    queries = []
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, sys.stdin.readline().split())
        queries.append((A-1, B-1, Y, C-1, D-1, Z))
    
    # Preprocessing: component history
    # Sort cells by height descending
    cells = []
    for i in range(H):
        for j in range(W):
            cells.append((F[i][j], i, j))
    cells.sort(reverse=True)  # descending by height
    
    # Union-Find with persistent component IDs
    parent = {}
    rank = {}
    root_to_compid = {}  # root -> current component ID
    compid_to_root = {}  # component ID -> root
    cell_list = {}  # root -> list of cells in component
    history = [[] for _ in range(H*W)]  # cell -> list of (height, comp_id) in decreasing order
    active = set()
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    next_comp_id = 0
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(r1, r2, h):
        nonlocal next_comp_id
        r1 = find(r1)
        r2 = find(r2)
        if r1 == r2:
            return
        # Union by rank
        if rank[r1] < rank[r2]:
            r1, r2 = r2, r1
        parent[r2] = r1
        if rank[r1] == rank[r2]:
            rank[r1] += 1
        # Assign new component ID
        new_cid = next_comp_id
        next_comp_id += 1
        # Update compid_to_root and root_to_compid
        old_cid1 = root_to_compid[r1]
        old_cid2 = root_to_compid[r2]
        if old_cid1 in compid_to_root:
            del compid_to_root[old_cid1]
        if old_cid2 in compid_to_root:
            del compid_to_root[old_cid2]
        compid_to_root[new_cid] = r1
        root_to_compid[r1] = new_cid
        if r2 in root_to_compid:
            del root_to_compid[r2]
        # Merge cell lists
        cells_to_move = cell_list[r2]
        for cell in cells_to_move:
            cell_list[r1].append(cell)
            history[cell[0]*W + cell[1]].append((h, new_cid))
        del cell_list[r2]
    
    # Process cells in decreasing height
    idx = 0
    n = len(cells)
    while idx < n:
        h = cells[idx][0]
        # Process all cells with height h
        while idx < n and cells[idx][0] == h:
            _, i, j = cells[idx]
            # Create new component for this cell
            parent[(i,j)] = (i,j)
            rank[(i,j)] = 0
            cid = next_comp_id
            next_comp_id += 1
            root_to_compid[(i,j)] = cid
            compid_to_root[cid] = (i,j)
            cell_list[(i,j)] = [(i,j)]
            active.add((i,j))
            history[i*W + j].append((h, cid))
            # Union with active neighbors
            for di, dj in dirs:
                ni, nj = i+di, j+dj
                if 0 <= ni < H and 0 <= nj < W and (ni,nj) in active:
                    union((i,j), (ni,nj), h)
            idx += 1
    
    # Reverse history lists to have increasing order
    for lst in history:
        lst.reverse()
    
    # Function to get component ID of a cell at a given floor
    def get_comp(i, j, f):
        lst = history[i*W+j]
        # Binary search for largest height <= f
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo+hi)//2
            if lst[mid][0] <= f:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return None
        return lst[lo-1][1]
    
    # For each query, run Dijkstra on component graph
    def solve_query(A, B, Y, C, D, Z):
        if (A,B,Y) == (C,D,Z):
            return 0
        min_f = min(Y, Z)
        max_f = max(Y, Z)
        start_comp = get_comp(A, B, Y)
        end_comp = get_comp(C, D, Z)
        if start_comp is None or end_comp is None:
            return -1
        # Dijkstra
        dist = {}
        start_state = (start_comp, Y)
        dist[start_state] = 0
        heap = [(0, start_comp, Y)]
        while heap:
            cost, comp, f = heapq.heappop(heap)
            if (comp, f) == (end_comp, Z):
                return cost
            if cost > dist.get((comp, f), float('inf')):
                continue
            # Horizontal moves (cost 0)
            root = compid_to_root.get(comp)
            if root is not None and root in cell_list:
                cells_in_comp = cell_list[root]
                visited_neigh = set()
                for ci, cj in cells_in_comp:
                    for di, dj in dirs:
                        ni, nj = ci+di, cj+dj
                        if 0 <= ni < H and 0 <= nj < W and F[ni][nj] >= f:
                            comp2 = get_comp(ni, nj, f)
                            if comp2 != comp and comp2 not in visited_neigh:
                                visited_neigh.add(comp2)
                                new_state = (comp2, f)
                                if cost < dist.get(new_state, float('inf')):
                                    dist[new_state] = cost
                                    heapq.heappush(heap, (cost, comp2, f))
            # Vertical up (cost 1)
            if f < max_f:
                root = compid_to_root.get(comp)
                if root is not None and root in cell_list:
                    cells_in_comp = cell_list[root]
                    next_comps = set()
                    for ci, cj in cells_in_comp:
                        if F[ci][cj] >= f+1:
                            comp2 = get_comp(ci, cj, f+1)
                            next_comps.add(comp2)
                    for comp2 in next_comps:
                        new_state = (comp2, f+1)
                        new_cost = cost + 1
                        if new_cost < dist.get(new_state, float('inf')):
                            dist[new_state] = new_cost
                            heapq.heappush(heap, (new_cost, comp2, f+1))
            # Vertical down (cost 1)
            if f > min_f:
                root = compid_to_root.get(comp)
                if root is not None and root in cell_list:
                    cells_in_comp = cell_list[root]
                    next_comps = set()
                    for ci, cj in cells_in_comp:
                        comp2 = get_comp(ci, cj, f-1)
                        next_comps.add(comp2)
                    for comp2 in next_comps:
                        new_state = (comp2, f-1)
                        new_cost = cost + 1
                        if new_cost < dist.get(new_state, float('inf')):
                            dist[new_state] = new_cost
                            heapq.heappush(heap, (new_cost, comp2, f-1))
        return -1
    
    out_lines = []
    for query in queries:
        A, B, Y, C, D, Z = query
        ans = solve_query(A, B, Y, C, D, Z)
        out_lines.append(str(ans))
    print('\n'.join(out_lines))

threading.Thread(target=main).start()