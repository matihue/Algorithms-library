import random
import pygame

pygame.init()

screen_size = 500

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

WIDTH = 50
HEIGHT = 50

tile_size = screen_size // WIDTH


seed = random.randint(1, 1000000)
random.seed(456)

map = []

for y in range(HEIGHT):
    row = []

    for x in range(WIDTH):
        if x == 0 or y == 0 or x == WIDTH - 1 or y == HEIGHT - 1:
            row.append("#")
        else:
            num = random.random()
            if num < 0.05:
                row.append("#")
            elif num < 0.3:
                row.append("B")
            elif num < 0.45:
                row.append('A')
            else:
                row.append('.')

    map.append(row)

map[1][1] = "S"
map[HEIGHT - 2][WIDTH - 2] = "G"

# żeby start i cel nie były zablokowane
map[1][2] = "."
map[2][1] = "."
map[HEIGHT - 2][WIDTH - 3] = "."
map[HEIGHT - 3][WIDTH - 2] = "."

map = ["".join(row) for row in map]



def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class PathFinder:
    def __init__(self):
        self.start = (1, 1)
        self.goal = (HEIGHT - 2, WIDTH - 2)

        self.actual_pos = self.start

        self.all_moves = []

        self.to_check = [self.start]
        self.visited = []
        self.cost = {
            self.start: 0
        }
        
        self.parent = {}

        self.path = []
        
        self.found = False    
        self.path_reversed = False
    
    def find_path(self):
        if self.actual_pos != self.goal:
            
            self.to_check.sort(key=lambda p: distance(p, self.goal) + self.cost[p])
            best_move = self.to_check[0]  
            
            self.actual_pos = best_move
                
            self.to_check.remove(best_move)
            self.visited.append(best_move)
                
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
                
        
        else:
            self.found = True

    def reverse_path(self):
        self.path = []
        self.path = [self.actual_pos]
        while self.actual_pos != self.start:
            self.actual_pos = self.parent[self.actual_pos]
            self.path.append(self.actual_pos)
        
        self.path.reverse()
        self.path_reversed = True

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
                color = (255, 155, 155)
            
            rect = pygame.Rect((sign_num * tile_size), (row_num * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)       

    if pathfinder.found and not pathfinder.path_reversed:
        pathfinder.reverse_path()
            
    elif not pathfinder.found:
        if pathfinder.to_check:
            pathfinder.find_path()   
                     
    for move in pathfinder.all_moves:
        rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
        pygame.draw.rect(screen, (255, 255, 0), rect) 
    
    if pathfinder.path_reversed:
        for move in pathfinder.path:
            rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), rect)        
           
    pygame.display.flip()
