import random
import pygame

pygame.init()

screen_size = 500

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

# map = [
#     "##################################################",
#     "#S....#..............#.............#.............#",
#     "#####.#.############.#.###########.#.###########.#",
#     "#.....#......A.......#.....#.......#.....B.......#",
#     "#.##########.#############.#.###########.#######.#",
#     "#..........#.......#.......#.......#.....#.......#",
#     "#.########.#######.#.#############.#.###.#.#####.#",
#     "#.#......#.......#.#.........A.....#.#...#.....#.#",
#     "#.#.####.#######.#.###############.#.#.#######.#.#",
#     "#.#.#..#.......#.#.....#...........#.#.......#.#.#",
#     "#.#.#.########.#.#####.#.###########.#######.#.#.#",
#     "#...#........#.#.....#.#.....B.............#.#...#",
#     "############.#.#####.#.###################.#.#####",
#     "#............#.....#.#.......#.............#.....#",
#     "#.################.#.#######.#.#################.#",
#     "#.....A............#.......#.#.........#.........#",
#     "#.########################.#.#########.#.#########",
#     "#.#......................#.#.......#...#.........#",
#     "#.#.####################.#.#######.#.###########.#",
#     "#.#.......#............#.#.#.......#.....A.......#",
#     "#.#######.#.##########.#.#.#.###################.#",
#     "#.......#.#.#........#.#.#.#.............#.......#",
#     "#######.#.#.#.######.#.#.#.#############.#.#######",
#     "#.......#...#.#....#.#...#.....B.........#.......#",
#     "#.############.#.##.###########.################.#",
#     "#..............#.#............#.#................#",
#     "#.##############.#.##########.#.#.##############.#",
#     "#.#..............#.#........#.#.#..........A.....#",
#     "#.#.##############.#.######.#.#.################.#",
#     "#.#................#......#.#.#..................#",
#     "#.########################.#.#.#################.#",
#     "#........A.................#.#.........#.........#",
#     "############################.#########.#.#########",
#     "#............................#.........#.........#",
#     "#.############################.#################.#",
#     "#.#...............B............#.................#",
#     "#.#.############################.###############.#",
#     "#.#..............................#...............#",
#     "#.################################.#############.#",
#     "#.........................A........#.............#",
#     "###############################.####.###########.#",
#     "#...............................#....#.....B.....#",
#     "#.###############################.###########.####",
#     "#.#.............................#.............#..#",
#     "#.#.###########################.#############.#.##",
#     "#.#..............A............#.............#...G#",
#     "#.#############################.###############..#",
#     "#................................................#",
#     "##################################################",
# ]

# HEIGHT = len(map)
# WIDTH = len(map[0])
# tile_size = screen_size // WIDTH

HEIGHT = 50
WIDTH = 50
tile_size = screen_size // WIDTH

seed = random.randint(1, 1000000)
random.seed(seed)

map = []

for y in range(HEIGHT):
    row = []

    for x in range(WIDTH):
        if x == 0 or y == 0 or x == WIDTH - 1 or y == HEIGHT - 1:
            row.append("#")
        else:
            num = random.random()
            if num < 0.001:
                row.append('G')
            elif num < 0.05:
                row.append("#")
            elif num < 0.3:
                row.append("B")
            elif num < 0.45:
                row.append('A')
            else:
                row.append('.')

    map.append(row)

map[1][1] = "S"
map[23][45] = "G"

# żeby start i cel nie były zablokowane
map[1][2] = "."
map[2][1] = "."
map[HEIGHT - 2][WIDTH - 3] = "."
map[HEIGHT - 3][WIDTH - 2] = "."

map = ["".join(row) for row in map]



class PathFinder:
    def __init__(self):
        self.start = (1, 1)

        self.goals = []

        for y, row in enumerate(map):
            for x, sign in enumerate(row):
                if sign == "G":
                    self.goals.append((y, x))

        self.actual_pos = self.start

        self.all_moves = []

        self.to_check = [self.start]
        self.visited = []
        self.cost = {
            self.start: 0
        }
        
        self.parent = {}

        self.paths = []
        
        self.found = []
        self.path_reversed = False
    
    def find_path(self):
        self.to_check.sort(key=lambda p: self.cost[p])
        best_move = self.to_check[0]  
        
        self.actual_pos = best_move
            
        self.to_check.remove(best_move)
        self.visited.append(best_move)
            
        if best_move in self.goals and best_move not in self.found:
            self.found.append(best_move)
            self.reverse_path(best_move)
            
        self.all_moves.append(best_move)
                
        moves = [
            (best_move[0]+1, best_move[1]),
            (best_move[0]-1, best_move[1]),
            (best_move[0], best_move[1]+1),
            (best_move[0], best_move[1]-1),
        ]
        
        for move in moves:
            if map[move[0]][move[1]] in ('.', 'G', 'A', 'B'):
                terrain = map[move[0]][move[1]]
                if terrain == '.':
                    cost = 1
                elif terrain == 'A':
                    cost = 3
                elif terrain == 'B':
                    cost = 6
                else:
                    cost = 1

                new_cost = self.cost[best_move] + cost
                if move not in self.cost or new_cost < self.cost[move]:
                    self.cost[move] = new_cost
                    self.parent[move] = best_move
                
                    if move not in self.visited and move not in self.to_check:
                        self.to_check.append(move)

    def reverse_path(self, goal):
        path = [goal]
        current = goal
        
        while current != self.start:
            current = self.parent[current]
            path.append(current)
        
        path.reverse()
        self.paths.append(path)

    def draw_best_path(self):
        if self.paths != []:
            best_path = max(
                self.paths,
                key=lambda path: self.cost[path[-1]]
            )
         
            for move in best_path:
                rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
                pygame.draw.rect(screen, (0, 255, 0), rect)        

        


pathfinder = PathFinder()

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for row_num, row in enumerate(map):
        for sign_num, sign in enumerate(row):
            if sign == '#':
                color = (0, 0, 0)
            elif sign == '.':
                color = (0, 255, 255)
            elif sign == 'S':
                color = (0, 255, 0)
            elif sign == 'G':
                color = (0, 0, 255)
            elif sign == 'A':
                color = (155, 155, 0)
            elif sign == 'B':
                color = (255, 155, 0)
                
            rect = pygame.Rect((sign_num * tile_size), (row_num * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)       

    if pathfinder.to_check:
        pathfinder.find_path()              
        for move in pathfinder.all_moves:
            rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, (255, 255, 0), rect)  
    
    for path in pathfinder.paths:
        for move in path:
            rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), rect)        
          
    pathfinder.draw_best_path()
           
    for row_num, row in enumerate(map):
        for sign_num, sign in enumerate(row):
            if sign == 'G':
                rect = pygame.Rect((sign_num * tile_size), (row_num * tile_size), tile_size, tile_size)
                pygame.draw.rect(screen, (0, 0, 255), rect)      
            elif sign == 'S':
                rect = pygame.Rect((sign_num * tile_size), (row_num * tile_size), tile_size, tile_size)
                pygame.draw.rect(screen, (0, 255, 0), rect) 

         
    
           
    pygame.display.flip()
