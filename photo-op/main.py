import sys
import math

sys.setrecursionlimit(300000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        T = int(next(iterator))
        X = int(next(iterator))
        Y = int(next(iterator))
    except StopIteration:
        return

    cows = []
    for i in range(N):
        s = int(next(iterator))
        x = int(next(iterator))
        y = int(next(iterator))
        cows.append({'s': s, 'x': x, 'y': y, 'id': i})
    
    cows.append({'s': T + 1, 'x': X, 'y': 0, 'id': -1})
    
    points = sorted(cows, key=lambda p: p['x'])
    num_points = len(points)
    
    cow_id_to_idx = {p['id']: i for i, p in enumerate(points) if p['id'] != -1}
    
    size = 1
    while size < num_points:
        size *= 2
    
    tree_len = 2 * size
    
    L_max = [0] * tree_len
    L_min = [0] * tree_len
    R_max = [float('inf')] * tree_len
    R_min = [float('inf')] * tree_len
    
    min_val = [float('inf')] * tree_len
    
    lazy_L = [-1] * tree_len
    lazy_R = [-1] * tree_len
    
    node_x_best = [0] * tree_len
    
    INF = float('inf')
    
    def calc_cost(x, l_val, r_val):
        if l_val > r_val:
            return INF
        if l_val <= Y <= r_val:
            return abs(X - x) + math.sqrt(x*x + Y*Y)
        if l_val > Y:
            return abs(X - x) + math.sqrt(x*x + l_val*l_val) + l_val - Y
        if r_val < Y:
            return abs(X - x) + math.sqrt(x*x + r_val*r_val) + Y - r_val
        return INF

    leaf_x = [p['x'] for p in points]
    
    def build(u, l, r):
        R_max[u] = INF
        R_min[u] = INF
        lazy_L[u] = -1
        lazy_R[u] = -1
        
        if l == r:
            x = leaf_x[l]
            node_x_best[u] = x
            L_max[u] = 0
            L_min[u] = 0
            min_val[u] = calc_cost(x, 0, INF)
            return
        
        mid = (l + r) // 2
        build(2*u, l, mid)
        build(2*u+1, mid+1, r)
        
        x1 = node_x_best[2*u]
        x2 = node_x_best[2*u+1]
        if abs(X - x1) <= abs(X - x2):
            node_x_best[u] = x1
        else:
            node_x_best[u] = x2
            
        pull(u)

    def apply_L_node(u, val):
        L_max[u] = val
        L_min[u] = val
        lazy_L[u] = val
        
        if val > R_max[u]:
            min_val[u] = INF
        elif val > Y:
            min_val[u] = calc_cost(node_x_best[u], val, INF)

    def apply_R_node(u, val):
        R_max[u] = val
        R_min[u] = val
        lazy_R[u] = val
        
        if L_min[u] > val:
            min_val[u] = INF
        elif val < Y:
            min_val[u] = calc_cost(node_x_best[u], 0, val)

    def push(u):
        if lazy_L[u] != -1:
            apply_L_node(2*u, lazy_L[u])
            apply_L_node(2*u+1, lazy_L[u])
            lazy_L[u] = -1
        
        if lazy_R[u] != -1:
            apply_R_node(2*u, lazy_R[u])
            apply_R_node(2*u+1, lazy_R[u])
            lazy_R[u] = -1

    def pull(u):
        L_max[u] = max(L_max[2*u], L_max[2*u+1])
        L_min[u] = min(L_min[2*u], L_min[2*u+1])
        R_max[u] = max(R_max[2*u], R_max[2*u+1])
        R_min[u] = min(R_min[2*u], R_min[2*u+1])
        min_val[u] = min(min_val[2*u], min_val[2*u+1])

    def update_L(u, l, r, ql, qr, val):
        if L_min[u] >= val: return 
        if ql > r or qr < l: return
            
        if ql <= l and r <= qr:
            is_valid = (val <= R_min[u])
            is_invalid = (val > R_max[u])
            
            if is_valid or is_invalid:
                if L_min[u] > Y:
                    apply_L_node(u, val)
                    return
                if L_max[u] <= Y and val <= Y:
                    apply_L_node(u, val)
                    return
                if L_max[u] <= Y and val > Y:
                    apply_L_node(u, val)
                    return

        if l == r:
            apply_L_node(u, val)
            return

        push(u)
        mid = (l + r) // 2
        update_L(2*u, l, mid, ql, qr, val)
        update_L(2*u+1, mid+1, r, ql, qr, val)
        pull(u)

    def update_R(u, l, r, ql, qr, val):
        if R_max[u] <= val: return
        if ql > r or qr < l: return

        if ql <= l and r <= qr:
            is_valid = (L_max[u] <= val)
            is_invalid = (L_min[u] > val)
            
            if is_valid or is_invalid:
                if R_max[u] < Y: 
                    apply_R_node(u, val)
                    return
                if R_min[u] >= Y and val >= Y: 
                    apply_R_node(u, val)
                    return
                if R_min[u] >= Y and val < Y: 
                    apply_R_node(u, val)
                    return
        
        if l == r:
            apply_R_node(u, val)
            return

        push(u)
        mid = (l + r) // 2
        update_R(2*u, l, mid, ql, qr, val)
        update_R(2*u+1, mid+1, r, ql, qr, val)
        pull(u)
        
    def find_first_L_ge(u, l, r, ql, qr, val):
        if L_max[u] < val: return -1
        if ql > r or qr < l: return -1
        if l == r: return l
        push(u)
        mid = (l + r) // 2
        res = find_first_L_ge(2*u, l, mid, ql, qr, val)
        if res != -1: return res
        return find_first_L_ge(2*u+1, mid+1, r, ql, qr, val)

    def find_first_R_gt(u, l, r, ql, qr, val):
        if R_max[u] <= val: return -1
        if ql > r or qr < l: return -1
        if l == r: return l
        push(u)
        mid = (l + r) // 2
        res = find_first_R_gt(2*u, l, mid, ql, qr, val)
        if res != -1: return res
        return find_first_R_gt(2*u+1, mid+1, r, ql, qr, val)

    build(1, 0, num_points-1)
    
    cows_by_time = sorted([c for c in cows if c['id'] != -1], key=lambda x: x['s'])
    cow_idx = 0
    output_buffer = []
    
    for t in range(T):
        while cow_idx < len(cows_by_time) and cows_by_time[cow_idx]['s'] <= t:
            c = cows_by_time[cow_idx]
            idx = cow_id_to_idx[c['id']]
            y_val = c['y']
            
            if idx + 1 < num_points:
                k = find_first_L_ge(1, 0, num_points-1, idx+1, num_points-1, y_val)
                end = k - 1 if k != -1 else num_points - 1
                if end >= idx + 1:
                    update_L(1, 0, num_points-1, idx+1, end, y_val)
            
            if idx - 1 >= 0:
                k = find_first_R_gt(1, 0, num_points-1, 0, idx-1, y_val)
                if k != -1:
                    update_R(1, 0, num_points-1, k, idx - 1, y_val)
                
            cow_idx += 1
            
        ans = min_val[1]
        output_buffer.append(str(math.floor(ans)))
    
    sys.stdout.write('\n'.join(output_buffer) + '\n')

if __name__ == '__main__':
    solve()