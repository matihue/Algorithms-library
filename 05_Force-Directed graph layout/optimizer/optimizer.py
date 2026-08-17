# imports #
import random
import time
import json
import os

# graph # 
graph = {
    # Rząd A
    "A1": [("A2", 3), ("B1", 5), ("B2", 7)],
    "A2": [("A1", 3), ("A3", 4), ("B2", 2), ("B1", 6)],
    "A3": [("A2", 4), ("A4", 6), ("B3", 5), ("B4", 8)],
    "A4": [("A3", 6), ("A5", 3), ("B4", 4), ("B3", 2)],
    "A5": [("A4", 3), ("A6", 5), ("B5", 6), ("B6", 4)],
    "A6": [("A5", 5), ("A7", 2), ("B6", 3)],
    "A7": [("A6", 2), ("A8", 7), ("B7", 5), ("B8", 9)],
    "A8": [("A7", 7), ("B8", 4), ("B7", 3)],

    # Rząd B
    "B1": [("A1", 5), ("A2", 6), ("B2", 4), ("C1", 3)],
    "B2": [("A1", 7), ("A2", 2), ("B1", 4), ("B3", 5), ("C2", 6)],
    "B3": [("A3", 5), ("A4", 2), ("B2", 5), ("B4", 3), ("C3", 4)],
    "B4": [("A3", 8), ("A4", 4), ("B3", 3), ("B5", 6), ("C4", 5)],
    "B5": [("A5", 6), ("B4", 6), ("B6", 2), ("C5", 7)],
    "B6": [("A5", 4), ("A6", 3), ("B5", 2), ("B7", 5), ("C6", 4)],
    "B7": [("A7", 5), ("A8", 3), ("B6", 5), ("B8", 3), ("C7", 6)],
    "B8": [("A7", 9), ("A8", 4), ("B7", 3), ("C8", 8)],

    # Rząd C
    "C1": [("B1", 3), ("C2", 4), ("D1", 6), ("D2", 5)],
    "C2": [("B2", 6), ("C1", 4), ("C3", 3), ("D2", 2)],
    "C3": [("B3", 4), ("C2", 3), ("C4", 7), ("D3", 5), ("D4", 4)],
    "C4": [("B4", 5), ("C3", 7), ("C5", 2), ("D4", 3)],
    "C5": [("B5", 7), ("C4", 2), ("C6", 6), ("D5", 4)],
    "C6": [("B6", 4), ("C5", 6), ("C7", 3), ("D6", 8), ("D5", 2)],
    "C7": [("B7", 6), ("C6", 3), ("C8", 5), ("D7", 4)],
    "C8": [("B8", 8), ("C7", 5), ("D8", 7), ("D7", 6)],

    # Rząd D
    "D1": [("C1", 6), ("D2", 3), ("E1", 5)],
    "D2": [("C1", 5), ("C2", 2), ("D1", 3), ("D3", 6), ("E2", 4)],
    "D3": [("C3", 5), ("D2", 6), ("D4", 2), ("E3", 7)],
    "D4": [("C3", 4), ("C4", 3), ("D3", 2), ("D5", 5), ("E4", 3)],
    "D5": [("C5", 4), ("C6", 2), ("D4", 5), ("D6", 4), ("E5", 6)],
    "D6": [("C6", 8), ("D5", 4), ("D7", 3), ("E6", 5)],
    "D7": [("C7", 4), ("C8", 6), ("D6", 3), ("D8", 2), ("E7", 8)],
    "D8": [("C8", 7), ("D7", 2), ("E8", 4)],

    # Rząd E
    "E1": [("D1", 5), ("E2", 4)],
    "E2": [("D2", 4), ("E1", 4), ("E3", 3)],
    "E3": [("D3", 7), ("E2", 3), ("E4", 6)],
    "E4": [("D4", 3), ("E3", 6), ("E5", 2)],
    "E5": [("D5", 6), ("E4", 2), ("E6", 5)],
    "E6": [("D6", 5), ("E5", 5), ("E7", 3)],
    "E7": [("D7", 8), ("E6", 3), ("E8", 4)],
    "E8": [("D8", 4), ("E7", 4)]
}

# helpers #
def crossing_point(l1p1, l1p2, l2p1, l2p2):
    def orientation(a, b, c):
        return (
            (b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0])
        )

    def cross(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    o1 = orientation(l1p1, l1p2, l2p1)
    o2 = orientation(l1p1, l1p2, l2p2)

    o3 = orientation(l2p1, l2p2, l1p1)
    o4 = orientation(l2p1, l2p2, l1p2)

    cross_exists = o1 * o2 < 0 and o3 * o4 < 0

    points = [l1p1, l1p2, l2p1, l2p2]
    cross_at_point = len(points) != len(set(points))

    if not cross_exists or cross_at_point:
        return None

    A = l1p1
    B = l1p2
    C = l2p1
    D = l2p2

    r = (B[0] - A[0], B[1] - A[1])
    s = (D[0] - C[0], D[1] - C[1])

    ca = (C[0] - A[0], C[1] - A[1])

    denominator = cross(r, s)

    if denominator == 0:
        return None

    t = cross(ca, s) / denominator

    cross_x = A[0] + t * r[0]
    cross_y = A[1] + t * r[1]

    return (cross_x, cross_y)
    
def dist(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def min_val(point):
    min_val = None
    for tup in point:
        if not min_val:
            min_val = tup
        elif tup[1] < min_val[1]:
            min_val = tup
            
    return min_val

def clamp_vector(v, limit=3):
    return (
        max(-limit, min(limit, v[0])),
        max(-limit, min(limit, v[1]))
    )

def save_to_file(opti_dict):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    save_data = [
        {
            "values": values,
            "score": score
        }
        for values, score in opti_dict.items()
    ]
    
    path = os.path.join(dir_path, "optimizer_data.json")
    
    with open(path, "w") as f:
        json.dump(save_data, f, indent=4)
    
# optimizer func #
def meta_optimizer(graph):
    optimizer = {}
    last_100 = {}
    iters = 150
    benchmark_size = (1, 3, 8, 12)
    
    mutation = 1
    gamma = mutation / iters
    
    ranges = {
        'const1': (0.1, 3.0),
        'const2': (1, 20),
        'momentum': (0, 0.9),
        'k_repel': (100, 5000),
        'iter_span': (50, 750),
    }
    
    initial_ranges = ranges.copy()
    
    counts = {}
    
    for i in range(iters):
        start = time.time()
        print(f'Iter {i} start')
        
        mutation -= gamma
                
        const1 = random.uniform(*ranges["const1"])   
        const2 = random.uniform(*ranges["const2"])   
        momentum = random.uniform(*ranges["momentum"])   
        k_repel = random.randint(*ranges["k_repel"])   
        iter_span = random.randint(*ranges["iter_span"])
        
        values = (const1, const2, momentum, k_repel, iter_span)
        
        score = visual(graph=graph, values=values)
        
        last_100[values] = score
        optimizer[values] = score
        counts[values] = 1
        save_to_file(optimizer)
         
        if i > 0 and (i+1) % 100 == 0:
            best_50 = dict(sorted(last_100.items(), key=lambda item: item[1])[:30])

            it = 0
            for values, score in best_50.items():
                avg_score = 0
                it+=1
                for b in range(benchmark_size[1]):
                    new_score = visual(graph=graph, values=values)
                    avg_score += new_score**2
                    print(f"Values: {it}/30 Benchmark {b+1}/{benchmark_size[1]}")

                best_50[values] = ((avg_score + optimizer[values]**2*counts[values]) / (benchmark_size[1]+counts[values]))**0.5
                optimizer[values] = best_50[values]
                counts[values] += benchmark_size[1] 
                save_to_file(optimizer)
                
                
            best_25 = dict(sorted(best_50.items(), key=lambda item: item[1])[:10])
            
            it = 0
            for values, score in best_25.items():
                avg_score = 0
                it+=1
                for b in range(benchmark_size[2]):
                    new_score = visual(graph=graph, values=values)
                    avg_score += new_score**2
                    print(f"Values: {it}/10 Benchmark {b+1}/{benchmark_size[2]}")
                  
                  
                best_25[values] = ((avg_score + optimizer[values]**2*counts[values]) / (benchmark_size[2]+counts[values]))**0.5
                optimizer[values] = best_25[values]
                counts[values] += benchmark_size[2]  
                save_to_file(optimizer)
                
 
            last_100 = {}    
                
        if i > 0 and (i+1) % 4 == 0:
            const1 = const2 = momentum = k_repel = iter_span = 0
            d = dict(sorted(optimizer.items(), key=lambda item: item[1]))
            first_10_keys = list(d)[:10]
            for key in first_10_keys:
                const1 += key[0]
                const2 += key[1]
                momentum += key[2]
                k_repel += key[3]
                iter_span += key[4]
                
            means = (const1/10, const2/10, momentum/10, k_repel/10, iter_span/10)
            whole_vals = (
                initial_ranges["const1"][1] - initial_ranges["const1"][0],
                initial_ranges["const2"][1] - initial_ranges["const2"][0],
                initial_ranges["momentum"][1] - initial_ranges["momentum"][0],
                initial_ranges["k_repel"][1] - initial_ranges["k_repel"][0],
                initial_ranges["iter_span"][1] - initial_ranges["iter_span"][0],
                )
            
            ranges = {
                "const1": (means[0] - 0.5*(whole_vals[0] * mutation), means[0] + 0.5*(whole_vals[0] * mutation)),
                "const2": (means[1] - 0.5*(whole_vals[1] * mutation), means[1] + 0.5*(whole_vals[1] * mutation)),
                "momentum": (means[2] - 0.5*(whole_vals[2] * mutation), means[2] + 0.5*(whole_vals[2] * mutation)),
                "k_repel": (int(means[3] - 0.5*(whole_vals[3] * mutation)), int(means[3] + 0.5*(whole_vals[3] * mutation))),
                "iter_span": (int(means[4] - 0.5*(whole_vals[4] * mutation)), int(means[4] + 0.5*(whole_vals[4] * mutation))),
            }
        end = time.time()
        print(f'Iter {i} duration: {end-start:.2f}\n')
           
    best_scores =  dict(sorted(optimizer.items(), key=lambda item: item[1])[:10])
    it = 0
    for values, score in best_scores.items():
        avg_score = 0
        it+=1
        for b in range(benchmark_size[3]):
            new_score = visual(graph=graph, values=values)
            avg_score += new_score**2
            print(f"Final benchmarks: Values: {it}/10 Benchmark {b+1}/{benchmark_size[3]}")
            
            
        optimizer[values] = ((avg_score + optimizer[values]**2*counts[values]) / (benchmark_size[3]+counts[values]))**0.5
        counts[values] += benchmark_size[3]
        save_to_file(optimizer)
        
    x = dict(sorted(optimizer.items(), key=lambda item: item[1]))
    final_best_values = x[0]
    
    return final_best_values
          
# graph func #
def visual(graph, values):
    # Unpacked variables #
    const1, const2, momentum, k_repel, iter_span = values
    
    # Iterations #
    rand_iterations = 7000
    iterations = 1000
    
    # Initial values #
    screen_size = 1000
    initial_x = screen_size // 2
    initial_y = screen_size // 2
    max_span = 600
    scale = 30
    
    # Booleans #
    length_mode = False
    cross_mode = True
    
    # Helpers #
    sorted_graph = dict(sorted(graph.items(), key=lambda item: len(item[1])))
    graph_points = {}
    best_graph = {}
    best_score = 0
    wanted_lens = {}
    temp_graph_points = {}
    temp_error = 0
    
    t_init = 0
    t_len = 0
    t_cross = 0
    t_repel = 0
    
    
    start = time.perf_counter()
    for _ in range(rand_iterations):
        initial_x = screen_size // 2
        initial_y = screen_size // 2

        temp_graph_points = {}
        avg_error = 0
        
        avg_error = 0
        crossings = 0
        for point in sorted_graph.keys():
            new_pos_x = initial_x + random.randint(-max_span, max_span)
            new_pos_y = initial_y + random.randint(-max_span, max_span)
            temp_graph_points[point] = (initial_x, initial_y)
            initial_x, initial_y = new_pos_x, new_pos_y
        
        for point, values in sorted_graph.items():
            for connection in values:
                actual_len = dist(temp_graph_points[point][0], temp_graph_points[point][1], temp_graph_points[connection[0]][0], temp_graph_points[connection[0]][1])
                wanted_len = connection[1] * scale

                error = abs(wanted_len - actual_len)
                avg_error += error
        
        if not temp_error:
            temp_error = avg_error
            graph_points = temp_graph_points.copy()
        elif avg_error < temp_error:
            graph_points = temp_graph_points.copy()
            temp_error = avg_error
    t_init += time.perf_counter() - start
            
    edges = []       
    for point, values in sorted_graph.items():
        for connection in values:
            if (point, connection[0]) not in edges and (connection[0], point) not in edges:
                edges.append((point, connection[0]))
                wanted_lens[(point, connection[0])] = connection[1] * scale
    
    edge_pairs = []

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            edge1 = edges[i]
            edge2 = edges[j]

            if edge1[0] in edge2 or edge1[1] in edge2:
                continue

            edge_pairs.append((edge1, edge2))
    
    velocities = {point: (0, 0) for point in graph_points}      
    nodes = list(graph_points.keys())
    
    for iteration in range(iterations):
        changes = {point: (0, 0) for point in graph_points}

        start = time.perf_counter()
        ### length mode ###
        avg_error = 0
        for point, neighbor in edges:
                        
            wanted_len = wanted_lens[(point, neighbor)]
            actual_len = dist(
                graph_points[point][0],
                graph_points[point][1],
                graph_points[neighbor][0],
                graph_points[neighbor][1]
            )

            error = wanted_len - actual_len

            avg_error += abs(error)
            

            if length_mode:
                x_comp_point = graph_points[point][0] - graph_points[neighbor][0]
                y_comp_point = graph_points[point][1] - graph_points[neighbor][1]
                l = (x_comp_point**2 + y_comp_point**2)**0.5
                point_direction = (x_comp_point/l, y_comp_point/l)
                
                neigh_direction = (-point_direction[0], -point_direction[1])
                
                x_change_point = error * point_direction[0] * const1
                y_change_point = error * point_direction[1] * const1
                
                x_change_neigh = error * neigh_direction[0] * const1
                y_change_neigh = error * neigh_direction[1] * const1

                changes[point] = (
                    changes.get(point, (0, 0))[0] + x_change_point,
                    changes.get(point, (0, 0))[1] + y_change_point
                )
                changes[neighbor] = (
                    changes.get(neighbor, (0, 0))[0] + x_change_neigh,
                    changes.get(neighbor, (0, 0))[1] + y_change_neigh
                )
        avg_error /= len(edges)
        ### ### ### ### ###
        t_len += time.perf_counter() - start

        edge_boxes = {}
        for edge in edges:
            A = graph_points[edge[0]]
            B = graph_points[edge[1]]

            edge_boxes[edge] = (
                min(A[0], B[0]),
                max(A[0], B[0]),
                min(A[1], B[1]),
                max(A[1], B[1]),
            )


        start = time.perf_counter()
        ### cross mode ###
        crossings = 0
        for edge_pair in edge_pairs:
            edge1 = edge_pair[0]
            edge2 = edge_pair[1]
            
            if edge_boxes[edge1][1] < edge_boxes[edge2][0]:
                continue

            if edge_boxes[edge2][1] < edge_boxes[edge1][0]:
                continue

            if edge_boxes[edge1][3] < edge_boxes[edge2][2]:
                continue

            if edge_boxes[edge2][3] < edge_boxes[edge1][2]:
                continue
                         
            cross_point = crossing_point(graph_points[edge1[0]], graph_points[edge1[1]], graph_points[edge2[0]], graph_points[edge2[1]])

            if cross_point:
                crossings += 1
            
            if cross_mode and cross_point:
                A = graph_points[edge1[0]]
                B = graph_points[edge1[1]]
                C = graph_points[edge2[0]]
                D = graph_points[edge2[1]]
                
                ab_len = dist(A[0], A[1], B[0], B[1])
                cd_len = dist(C[0], C[1], D[0], D[1])
                
                mid1 = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
                mid2 = ((C[0] + D[0]) / 2, (C[1] + D[1]) / 2)
                
                strenght_compA = dist(A[0], A[1], cross_point[0], cross_point[1]) / ab_len + 0.0001
                strenght_compB = dist(B[0], B[1], cross_point[0], cross_point[1]) / ab_len + 0.0001
                strenght_compC = dist(C[0], C[1], cross_point[0], cross_point[1]) / cd_len + 0.0001
                strenght_compD = dist(D[0], D[1], cross_point[0], cross_point[1]) / cd_len + 0.0001

                direction = (mid1[0]-mid2[0], mid1[1]-mid2[1])
                d = (direction[0]**2 + direction[1]**2)**0.5 + 0.0001
                direction = (direction[0]/d * const2, direction[1]/d * const2)
                        
                A_change = (direction[0]*strenght_compA, direction[1]*strenght_compA)
                B_change = (direction[0]*strenght_compB, direction[1]*strenght_compB)
                C_change = (-direction[0]*strenght_compC, -direction[1]*strenght_compC)
                D_change = (-direction[0]*strenght_compD, -direction[1]*strenght_compD)
                
                changes[edge1[0]] = (changes[edge1[0]][0] + A_change[0], changes[edge1[0]][1] + A_change[1])
                changes[edge1[1]] = (changes[edge1[1]][0] + B_change[0], changes[edge1[1]][1] + B_change[1])
                changes[edge2[0]] = (changes[edge2[0]][0] + C_change[0], changes[edge2[0]][1] + C_change[1])
                changes[edge2[1]] = (changes[edge2[1]][0] + D_change[0], changes[edge2[1]][1] + D_change[1])
        ### ### ### ### ##   
        t_cross += time.perf_counter() - start

        start = time.perf_counter()
        ### coulomb law ###
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                p1, p2 = nodes[i], nodes[j]
                
                dx = graph_points[p1][0] - graph_points[p2][0]
                dy = graph_points[p1][1] - graph_points[p2][1]
                
                dist_sq = dx**2 + dy**2 + 0.1
                d = dist_sq ** 0.5
                
                force = k_repel / dist_sq
                fx = (dx/d) * force
                fy = (dy/d) * force
                
                changes[p1] = (changes[p1][0] + fx, changes[p1][1]+fy)
                changes[p2] = (changes[p2][0] - fx, changes[p2][1]-fy)
        ### ### ### ### ###
        t_repel += time.perf_counter() - start
        
        ### applying changes ###
        for point, position in graph_points.items():
            clamped = clamp_vector(changes[point])
            
            vx = velocities[point][0] * momentum + clamped[0]
            vy = velocities[point][1] * momentum + clamped[1]
            
            velocities[point] = (vx, vy)
            
            graph_points[point] = (
                graph_points[point][0] + vx,
                graph_points[point][1] + vy
            )
        ### ### ### ### ### ### 
        
        ### iterations asignment ###
        if iteration % iter_span == 0:
            
            len_need  = int(min(max(0, ( avg_error * 30)), iter_span))
            cross_need = int(min(max(0, (  crossings**2 )), iter_span))
            
            total = len_need  + cross_need
            
            if total > 0:
                len_ratio = len_need / total
                len_iters = int(len_ratio * iter_span)
            else:
                len_iters = iter_span // 2
        own_iter = iteration % iter_span
        if own_iter < len_iters:
            length_mode = True
            cross_mode = False
        else:
            length_mode = False
            cross_mode = True
        ### ### ### ### ### ### ###
                    
        ### best graph asignment ###
        score = avg_error + crossings * 2
        if not best_graph:
            best_graph = graph_points.copy()
            best_score = score
        elif score < best_score:
            best_graph = graph_points.copy()
            best_score = score
        ### ### ### ### ### ### ###
    
    ### coordinates clamping ###
    for point, pos in best_graph.items():
        best_graph[point] = (int(pos[0]), int(pos[1]))
    ### ### ### ### ### ### ### 
    
    print("")
    print("init:", t_init)
    print("init:", t_len)
    print("cross:", t_cross)
    print("repel:", t_repel)
    
    return best_score     

best = meta_optimizer(graph)
print(best)