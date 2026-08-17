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
random.seed(seed)

map = []

for y in range(HEIGHT):
    row = []

    for x in range(WIDTH):
        if x == 0 or y == 0 or x == WIDTH - 1 or y == HEIGHT - 1:
            row.append("#")
        else:
            num = random.random()
            if num < 0.35:
                row.append("#")
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

        self.actual_pos_1 = self.start
        self.actual_pos_2 = self.goal

        self.all_moves_1 = []
        self.all_moves_2 = []

        self.to_check_1 = [self.start]
        self.to_check_2 = [self.goal]
        
        self.visited_1 = []
        self.visited_2 = []
        
        self.cost_1 = {
            self.start: 0
        }
        
        self.cost_2 = {
            self.goal: 0
        }
        
        self.parent_1 = {}
        self.parent_2 = {}

        self.path_1 = []
        self.path_2 = []

        self.meeting_point = None  
        self.path_reversed = False
    
    def find_path(self):
        self.to_check_1.sort(key=lambda p: self.cost_1[p])
        best_move = self.to_check_1[0]  
        
        self.actual_pos_1 = best_move
            
        self.to_check_1.remove(best_move)
        self.visited_1.append(best_move)
            
        self.all_moves_1.append(best_move)
                
        moves = [
            (best_move[0]+1, best_move[1]),
            (best_move[0]-1, best_move[1]),
            (best_move[0], best_move[1]+1),
            (best_move[0], best_move[1]-1),
        ]
        
        for move in moves:
            if map[move[0]][move[1]] in ('.', 'G', 'S'):
                terrain = map[move[0]][move[1]]
                cost = 1

                new_cost = self.cost_1[best_move] + cost
                if move not in self.cost_1 or new_cost < self.cost_1[move]:
                    self.cost_1[move] = new_cost
                    self.parent_1[move] = best_move
                
                    if move not in self.visited_1 and move not in self.to_check_1:
                        self.to_check_1.append(move)
            
                if move in self.visited_2:
                    self.meeting_point = move
                    
                    
        self.to_check_2.sort(key=lambda p: self.cost_2[p])
        best_move = self.to_check_2[0]  
        
        self.actual_pos_2 = best_move
            
        self.to_check_2.remove(best_move)
        self.visited_2.append(best_move)
            
        self.all_moves_2.append(best_move)
                
        moves = [
            (best_move[0]+1, best_move[1]),
            (best_move[0]-1, best_move[1]),
            (best_move[0], best_move[1]+1),
            (best_move[0], best_move[1]-1),
        ]
        
        for move in moves:
            if map[move[0]][move[1]] in ('.', 'G', 'S'):
                terrain = map[move[0]][move[1]]
                cost = 1

                new_cost = self.cost_2[best_move] + cost
                if move not in self.cost_2 or new_cost < self.cost_2[move]:
                    self.cost_2[move] = new_cost
                    self.parent_2[move] = best_move
                
                    if move not in self.visited_2 and move not in self.to_check_2:
                        self.to_check_2.append(move)
    
                if move in self.visited_1:
                    self.meeting_point = move
            
            
    def reverse_path(self):
        self.path_1 = []
        self.path_1 = [self.meeting_point]
        self.actual_pos_1 = self.meeting_point
        while self.actual_pos_1 != self.start:
            self.actual_pos_1 = self.parent_1[self.actual_pos_1]
            self.path_1.append(self.actual_pos_1)
        
        self.path_1.reverse()

        self.path_2 = []
        self.path_2 = [self.meeting_point]
        self.actual_pos_2 = self.meeting_point
        while self.actual_pos_2 != self.goal:
            self.actual_pos_2 = self.parent_2[self.actual_pos_2]
            self.path_2.append(self.actual_pos_2)
        

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
            
            rect = pygame.Rect((sign_num * tile_size), (row_num * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)       

    if pathfinder.meeting_point is not None and not pathfinder.path_reversed:
        pathfinder.reverse_path()
            
    elif not pathfinder.meeting_point:
        if pathfinder.to_check_1 != [] and pathfinder.to_check_2 != []:
            pathfinder.find_path()   
            
    for move in pathfinder.all_moves_1:
        rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
        pygame.draw.rect(screen, (255, 255, 0), rect) 
    for move in pathfinder.all_moves_2:
        rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
        pygame.draw.rect(screen, (255, 255, 0), rect) 
    
    
    if pathfinder.path_reversed:
        for move in pathfinder.path_1:
            rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), rect)     
        for move in pathfinder.path_2:
            rect = pygame.Rect((move[1] * tile_size), (move[0] * tile_size), tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), rect)  
            
    if pathfinder.meeting_point:
        rect = pygame.Rect((pathfinder.meeting_point[1] * tile_size), (pathfinder.meeting_point[0] * tile_size), tile_size, tile_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)        
    
           
    pygame.display.flip()
    
