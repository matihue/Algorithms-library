import random
import pygame
import time

pygame.init()

screen_size = 1000
cam_x = 0
cam_y = 0

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

def generate_graph(rows=8, cols=8, extra_edges=50, seed=42):
    random.seed(seed)

    graph = {}

    for r in range(rows):
        for c in range(cols):
            node = f"{chr(65 + r)}{c + 1}"
            graph[node] = []

    nodes = list(graph.keys())

    def add_edge(a, b, weight=None):
        if a == b:
            return

        if any(neighbor == b for neighbor, _ in graph[a]):
            return

        if weight is None:
            weight = random.randint(2, 10)

        graph[a].append((b, weight))
        graph[b].append((a, weight))

    for r in range(rows):
        for c in range(cols):
            node = f"{chr(65 + r)}{c + 1}"

            if c + 1 < cols:
                add_edge(
                    node,
                    f"{chr(65 + r)}{c + 2}"
                )

            if r + 1 < rows:
                add_edge(
                    node,
                    f"{chr(65 + r + 1)}{c + 1}"
                )

    for r in range(rows - 1):
        for c in range(cols - 1):

            if random.random() < 0.7:
                add_edge(
                    f"{chr(65 + r)}{c + 1}",
                    f"{chr(65 + r + 1)}{c + 2}"
                )

            if random.random() < 0.7:
                add_edge(
                    f"{chr(65 + r)}{c + 2}",
                    f"{chr(65 + r + 1)}{c + 1}"
                )

    for r in range(rows):
        for c in range(cols):
            node = f"{chr(65 + r)}{c + 1}"

            if c + 2 < cols and random.random() < 0.4:
                add_edge(
                    node,
                    f"{chr(65 + r)}{c + 3}"
                )

            if r + 2 < rows and random.random() < 0.4:
                add_edge(
                    node,
                    f"{chr(65 + r + 2)}{c + 1}"
                )

    added = 0

    while added < extra_edges:
        a, b = random.sample(nodes, 2)

        before = len(graph[a])
        add_edge(a, b)

        if len(graph[a]) > before:
            added += 1

    return graph


graph = generate_graph(
    rows=8,
    cols=8,
    extra_edges=0,
    seed=234
)
print(graph)

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
   
def direction_to_closest(A, B, P):
    t = ((P[0]-A[0])*(B[0]-A[0]) + (P[1]-A[1])*(B[1]-A[1])) / (
        (B[0]-A[0])**2 + (B[1]-A[1])**2
    )
    
    t = max(0, min(1, t))
    
    closest = (
        A[0] + t * (B[0]-A[0]),
        A[1] + t * (B[1]-A[1])
    )
    
    distance = dist(P[0], P[1], closest[0], closest[1])
    
    direction = (
        P[0] - closest[0],
        P[1] - closest[1]
    )
    
    length = (direction[0]**2 + direction[1]**2)**0.5

    normalized_direction = (
        direction[0] / length,
        direction[1] / length        
    )
    
    return normalized_direction, distance

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

            
def mst(graph):
    all_points = [point for point, values in graph.items()]
    points_left = all_points.copy()
    new_map = []
    
    starting_point = None
    for point, values_list in graph.items():
        if not starting_point:
            starting_point = point
        elif len(values_list) < len(graph[starting_point]):
            starting_point = point
    
    points = [starting_point]
    while points_left:
        best_move = None
        from_point = None
        for point in points:
            for neighbor_point in graph[point]:
                if neighbor_point[0] in points_left:
                    if not best_move:
                        best_move = neighbor_point
                        from_point = point
                    elif neighbor_point[1] < best_move[1]:
                        best_move = neighbor_point
                        from_point = point
                        
        points.append(best_move[0])
        points_left.remove(best_move[0])
        new_map.append((from_point, best_move[0], best_move[1]))
        
    return new_map



new_map = mst(graph)
def draw(positions):
    calc_cam_pos(positions)
    
    for point, position in positions.items():
       for connection in graph[point]:
           pygame.draw.line(screen, (255, 255, 255), (position[0]-cam_x, position[1]-cam_y), (positions[connection[0]][0]-cam_x, positions[connection[0]][1]-cam_y), 1)
            
    for connection in new_map:
        point1 = (positions[connection[0]][0]-cam_x, positions[connection[0]][1]-cam_y)
        point2 = (positions[connection[1]][0]-cam_x, positions[connection[1]][1]-cam_y)
        
        pygame.draw.line(screen, (0, 255, 0), point1, point2, 1)
        
        
    for point, position in positions.items():
        pygame.draw.circle(screen, (255,0,0), (position[0]-cam_x, position[1]-cam_y), 4)
            
def calc_cam_pos(points):
    avg_x = 0
    avg_y = 0
    pos_len = 0
    
    for point, pos in points.items():
        pos_len += 1
        avg_x += pos[0]
        avg_y += pos[1]    

    global cam_x, cam_y, screen_size
    
    cam_x = int(avg_x / pos_len) - screen_size // 2
    cam_y = int(avg_y / pos_len) - screen_size // 2
         
def visualise_graph(graph):
    headless = False
    
    sorted_graph = dict(sorted(graph.items(), key=lambda item: len(item[1])))
    graph_points = {}
    best_graph = {}
    best_score = 0

    wanted_lens = {}
    
    temp_graph_points = {}
    temp_error = 0
    
    global cam_x, cam_y
    
    cam_x = 0
    cam_y = 0
    
    cross_wage = 3
    len_wage = 2 
    node_edge_wage = 1
    
    const1 = 0.656026936391588293
    const2 = 14.909212144703837
    momentum = 0.6829715910733573
    k_repel = 3352
    iter_span = 500
    node_repel = 1800

    rand_iterations = 15000
    iterations = 2000
    
    screen_size = 1000
    initial_x = screen_size // 2
    initial_y = screen_size // 2
    max_span = 500
    scale = 30
    min_node_edge_dist = 40
    
    length_mode = False
    cross_mode = True

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

        ### length mode ###
        avg_error = 0
        summ = 0
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
            summ += 1
            

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
        avg_error /= summ
        ### ### ### ### ###

        ### edge boxes ###
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
        ### ### ### ### ###

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
                
                strenght_compA = dist(A[0], A[1], cross_point[0], cross_point[1]) / ab_len 
                strenght_compB = dist(B[0], B[1], cross_point[0], cross_point[1]) / ab_len
                strenght_compC = dist(C[0], C[1], cross_point[0], cross_point[1]) / cd_len
                strenght_compD = dist(D[0], D[1], cross_point[0], cross_point[1]) / cd_len 

                direction = (mid1[0]-mid2[0], mid1[1]-mid2[1])
                d = (direction[0]**2 + direction[1]**2)**0.5
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
    
        ### points/edges dist ###
        node_edge_dist_avg = 0
        summ = 0
        for node in nodes:
            for edge in edges:
                if node in edge:
                    continue
                
                direct, distance = direction_to_closest(graph_points[edge[0]], graph_points[edge[1]], graph_points[node])
                
                force = node_repel / distance ** 2
                
                cx = direct[0] * force
                cy = direct[1] * force
                
                changes[node] = (changes[node][0]+cx, changes[node][1]+cy)
                
                penalty = max(0, min_node_edge_dist-distance)**2
                
                node_edge_dist_avg += penalty
                summ += 1
                
        node_edge_dist_avg /= summ
        node_edge_dist_avg **= 0.5
        ### ### ### ### ### ### #
        
        
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
        score = (avg_error * len_wage) + (crossings * cross_wage) + (node_edge_dist_avg * node_edge_wage)
        
        if not best_graph:
            best_graph = graph_points.copy()
            best_score = score
        elif score < best_score:
            best_graph = graph_points.copy()
            best_score = score
        ### ### ### ### ### ### ###

        ### head ###
        if not headless and length_mode:
            pygame.event.pump()
                        
            screen.fill((0, 0, 0))
            draw(graph_points)
            pygame.display.flip()
            
            clock.tick(60)
        ### ### ###
    
    ### coordinates clamping ###
    for point, pos in best_graph.items():
        best_graph[point] = (int(pos[0]), int(pos[1]))
    ### ### ### ### ### ### ### 

    print(best_score)
    
    return best_graph    
      
positioned = False      
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))    

    if not positioned:
        start = time.time()
        positions = visualise_graph(graph)
        end = time.time()
        print(f'Time: {end-start:.2f} seconds')
        positioned = True
    elif positioned:  
        draw(positions)

    pygame.display.flip()
    