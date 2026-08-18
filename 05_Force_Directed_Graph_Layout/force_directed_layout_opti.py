### imports ###
import random
import pygame
import time
### ### ### ###

### visualisation ###
if True:
    pygame.init()

    screen_size = 1000
    cam_x = 0
    cam_y = 0
    
    point_size = 5
    
    middle_x = 0
    middle_y = 0
    
    screen = pygame.display.set_mode((screen_size, screen_size))
    clock = pygame.time.Clock()

def draw(positions):
    calc_cam_pos(positions)
    
    for point, position in positions.items():
       for connection in graph[point]:
           pygame.draw.line(screen, (255, 255, 255), (position[0]-cam_x-middle_x, position[1]-cam_y-middle_y), (positions[connection[0]][0]-cam_x-middle_x, positions[connection[0]][1]-cam_y-middle_y), 1)
        
    for point, position in positions.items():
        pygame.draw.circle(screen, (255,0,0), (position[0]-cam_x-middle_x, position[1]-cam_y-middle_y), point_size)

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

def handle_cam_change():
    global middle_x, middle_y
    
    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_a]:
        middle_x -= 10
        
    if keys_pressed[pygame.K_d]:
        middle_x += 10
        
    if keys_pressed[pygame.K_w]:
        middle_y -= 10
        
    if keys_pressed[pygame.K_s]:
        middle_y += 10
### ### ### ### ### #

### graph ###
graph = {
    "N1": [("N2", 3), ("N6", 4), ("N3", 6), ("N16", 8)],
    "N2": [("N1", 3), ("N3", 4), ("N5", 7), ("N19", 4)],
    "N3": [("N2", 4), ("N4", 3), ("N1", 6), ("N6", 5), ("N7", 8), ("N24", 8)],
    "N4": [("N3", 3), ("N5", 5), ("N6", 6), ("N18", 6)],
    "N5": [("N4", 5), ("N6", 3), ("N2", 7), ("N9", 6), ("N20", 4)],
    "N6": [("N5", 3), ("N1", 4), ("N3", 5), ("N4", 6), ("N22", 5)],

    "N7": [("N8", 3), ("N12", 5), ("N9", 6), ("N3", 8)],
    "N8": [("N7", 3), ("N9", 4), ("N11", 7), ("N19", 9)],
    "N9": [("N8", 4), ("N10", 3), ("N7", 6), ("N12", 5), ("N5", 6), ("N23", 5)],
    "N10": [("N9", 3), ("N11", 4), ("N12", 6), ("N13", 8)],
    "N11": [("N10", 4), ("N12", 3), ("N8", 7), ("N21", 4)],
    "N12": [("N11", 3), ("N7", 5), ("N9", 5), ("N10", 6), ("N15", 6), ("N24", 5)],

    "N13": [("N14", 3), ("N18", 5), ("N15", 6), ("N10", 8), ("N22", 8)],
    "N14": [("N13", 3), ("N15", 4), ("N17", 7), ("N20", 9)],
    "N15": [("N14", 4), ("N16", 3), ("N13", 6), ("N18", 5), ("N12", 6)],
    "N16": [("N15", 3), ("N17", 4), ("N18", 6), ("N1", 8), ("N23", 8)],
    "N17": [("N16", 4), ("N18", 3), ("N14", 7), ("N21", 9)],
    "N18": [("N17", 3), ("N13", 5), ("N15", 5), ("N16", 6), ("N4", 6)],

    "N19": [("N2", 4), ("N8", 9), ("N20", 7), ("N24", 7)],
    "N20": [("N5", 4), ("N14", 9), ("N19", 7), ("N21", 7)],
    "N21": [("N11", 4), ("N17", 9), ("N20", 7), ("N22", 7)],
    "N22": [("N6", 5), ("N13", 8), ("N21", 7), ("N23", 7)],
    "N23": [("N9", 5), ("N16", 8), ("N22", 7), ("N24", 7)],
    "N24": [("N12", 5), ("N3", 8), ("N23", 7), ("N19", 7)],
}
### ### ### #

### get data ###
def get_data():
    w1 = float(input("Skrzyżowania: "))
    w2 = float(input("Długość: "))
    w3 = float(input("Odległość punktów od połączeń: "))
    init_iters = int(input("Ilość iteracji początkowych: "))
    
    w1, w2, w3 = normalize_wages(w1, w2, w3)
    
    best = visualise_graph(graph, w1, w2, w3, init_iters)
    return best 
### ### ### ###

### helpers ###
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
    
    length = (direction[0]**2 + direction[1]**2)**0.5 + 0.0001

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

def normalize_wages(cross_wage, len_wage, node_edge_wage):
    cross_range = 10
    len_range = 10
    node_edge_range =  1
    
    return cross_range*cross_wage, len_range*len_wage, node_edge_range*node_edge_wage

def wanted_lens_func(graph_points, graph):
    wanted_lens = {}
    
    edges = []       
    for point, values in graph.items():
        for connection in values:
            if (point, connection[0]) not in edges and (connection[0], point) not in edges:
                edges.append((point, connection[0]))
    
    for edge in edges:
        wanted_lens[(edge[0], edge[1])] = dist(graph_points[edge[0]][0], graph_points[edge[0]][1], graph_points[edge[1]][0], graph_points[edge[1]][1])
        
    return wanted_lens, edges
### ### ### ###


### init ###
def visualise_graph(graph, w1, w2, w3, init_iters):
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
    
    cross_wage = w1
    len_wage = w2
    node_edge_wage = w3
    
    const1 = 0.656026936391588293
    const2 = 14.909212144703837
    momentum = 0.6829715910733573
    k_repel = 3352
    iter_span = 500
    node_repel = 1800

    rand_iterations = 5000
    iterations = init_iters
    
    screen_size = 1000
    initial_x = screen_size // 2
    initial_y = screen_size // 2
    max_span = 500
    scale = 25
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
            
            len_need  = int(min(max(0, ( avg_error * (len_wage+1))), iter_span))
            cross_need = int(min(max(0, (  crossings * (cross_wage+1) )), iter_span))
            
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
            best_avg_error, best_crossings, best_node_edge_dist = avg_error, crossings, node_edge_dist_avg
            
        elif score < best_score:
            best_graph = graph_points.copy()
            best_score = score
            best_avg_error, best_crossings, best_node_edge_dist = avg_error, crossings, node_edge_dist_avg
        ### ### ### ### ### ### ###

        ### head ###
        if not headless and length_mode:
            pygame.event.pump()
                        
            screen.fill((0, 0, 0))
            draw(graph_points)
            pygame.display.flip()
            
            clock.tick(60)
            handle_cam_change()
        ### ### ###
    
    ### coordinates clamping ###
    for point, pos in best_graph.items():
        best_graph[point] = (int(pos[0]), int(pos[1]))
    ### ### ### ### ### ### ### 

    print(f'\nBEST SCORE: {best_score}')
    print(f'Avg error: {best_avg_error}')
    print(f'Crossings: {best_crossings}')
    print(f'Avg node-edge dist penalty: {best_node_edge_dist}')
    
    return best_graph    
### ### ### ### #

### force directed layout ###
def force_directed_layout(graph_points, wanted_lens, edges):
    const1 = 0.1
    momentum = 0.9
    k_repel = 600
    
    velocities = {point: (0, 0) for point in graph_points}      
    nodes = list(graph_points.keys())
    changes = {point: (0, 0) for point in graph_points}

    ### length mode ###
    for point, neighbor in edges:
                    
        wanted_len = wanted_lens[(point, neighbor)]
        actual_len = dist(
            graph_points[point][0],
            graph_points[point][1],
            graph_points[neighbor][0],
            graph_points[neighbor][1]
        )

        error = wanted_len - actual_len

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
    ### ### ### ### ###

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

    ### coordinates clamping ###
    for point, pos in graph_points.items():
        graph_points[point] = (int(pos[0]), int(pos[1]))
    ### ### ### ### ### ### ### 
### ### ### ### ### ### ### #

### dragging ###
clicked = False
dragged_point = None

def handle_dragging(graph_points):
    global dragged_point
    
    for point, position in graph_points.items():
        if not clicked:
            return
        else:
            bounding_box = (
                position[0] - 0.5*point_size - cam_x,
                position[0] + 0.5*point_size - cam_x,
                position[1] - 0.5*point_size - cam_y,
                position[1] + 0.5*point_size - cam_y
            )
            
            mouse_pos = pygame.mouse.get_pos()
            
            if (
                bounding_box[0] <= mouse_pos[0] <= bounding_box[1] 
                and bounding_box[2] <= mouse_pos[1] <= bounding_box[3]
            ):
                dragged_point = point
                return
            
def update_positions(graph_points):
    mouse_pos = pygame.mouse.get_pos()
    if clicked and dragged_point:
        graph_points[dragged_point] = (mouse_pos[0]+cam_x, mouse_pos[1]+cam_y)
    
    return graph_points
### ### ### ### #   
        
### main loop ###
ready = False      
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
            dragged_point = None
        
            
    screen.fill((0, 0, 0))    

    if not ready:
        graph_points = get_data()
        wanted_lens, edges = wanted_lens_func(graph_points, graph)
        
        ready = True
        
    handle_dragging(graph_points)
    graph_points = update_positions(graph_points)    
    
    force_directed_layout(graph_points, wanted_lens, edges)
    draw(graph_points)
    handle_cam_change()
    
    pygame.display.flip()
### ### ### ### #
