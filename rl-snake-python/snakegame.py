import pygame
import numpy as np
import random
from enum import Enum
import time

class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    
class Action(Enum):
    RIGHT = 0
    LEFT = 1
    STRAIGHT = 2

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 120, 255)
    
action_name = {Action.RIGHT:'Right', Action.LEFT:'Left', Action.STRAIGHT:'Straight'}

class SnakeGame:
    def __init__(self, width=16, height=16, enable_gui=False, is_human=False):
        self.width, self.height = width, height
        self.enable_gui, self.is_human = enable_gui, is_human
        self.cell_size = 30
        if self.enable_gui:
            pygame.init()
            self.screen = pygame.display.set_mode((width * self.cell_size, height * self.cell_size))
            pygame.display.set_caption('Snake AI Training')
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('arial', 15)
        self.reset()
    
    def reset(self):
        self.direction = Direction.RIGHT
        self.head = [self.width // 2, self.height // 2] # snake head is put in the center
        self.snake = [self.head.copy(), [self.head[0] - 1, self.head[1]], [self.head[0] - 2, self.head[1]]]
        self.score, self.reward, self.total_reward = 0, 0, 0
        self.food = self._place_food()
        self.frame_iteration = 0
        self.game_over = False
        return self._get_state()
    
    def _place_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            food = [x, y]
            if food not in self.snake:
                return food
    
    def _get_state(self):
        head = self.head
        if self.direction == Direction.RIGHT:
            point_straight = [head[0] + 1, head[1]]
            point_left = [head[0], head[1] - 1]
            point_right = [head[0], head[1] + 1]
        elif self.direction == Direction.LEFT:
            point_straight = [head[0] - 1, head[1]]
            point_left = [head[0], head[1] + 1]
            point_right = [head[0], head[1] - 1]
        elif self.direction == Direction.UP:
            point_straight = [head[0], head[1] - 1]
            point_left = [head[0] - 1, head[1]]
            point_right = [head[0] + 1, head[1]]
        else:  # DOWN
            point_straight = [head[0], head[1] + 1]
            point_left = [head[0] + 1, head[1]]
            point_right = [head[0] - 1, head[1]]
        # Danger direction: STRAIGHT, LEFT, RIGHT
        danger_straight = 1 if self._is_collision(point_straight) else 0
        danger_left = 1 if self._is_collision(point_left) else 0
        danger_right = 1 if self._is_collision(point_right) else 0
        # food direction (relative to snake head): LEFT, RIGHT, UP, DOWN
        food_left = 1 if self.food[0] < head[0] else 0
        food_right = 1 if self.food[0] > head[0] else 0
        food_up = 1 if self.food[1] < head[1] else 0
        food_down = 1 if self.food[1] > head[1] else 0
        # current direction
        dir_left = int(self.direction == Direction.LEFT)
        dir_right = int(self.direction == Direction.RIGHT)
        dir_up = int(self.direction == Direction.UP)
        dir_down = int(self.direction == Direction.DOWN)
        state = [danger_straight, danger_left, danger_right, food_left, food_right, food_up, food_down, dir_left, dir_right, dir_up, dir_down]
        return np.array(state, dtype=int)
    
    def _is_collision(self, point=None):
        if point is None:
            point = self.head
        if (point[0] < 0 or point[0] >= self.width or point[1] < 0 or point[1] >= self.height): # hit border
            return True
        if point in self.snake[1:]: # hit itself
            return True
        return False
    
    def move(self, point:list, direction:Direction):
        new_point = point.copy()
        if direction == Direction.RIGHT:
            new_point[0] += 1
        elif direction == Direction.LEFT:
            new_point[0] -= 1
        elif direction == Direction.UP:
            new_point[1] -= 1
        elif direction == Direction.DOWN:
            new_point[1] += 1
        return new_point
    
    def step(self, action):
        if type(action) == int or type(action) == np.int64:
            action = Action(int(action))
        print(f'choosed action {action}, {action_name[action]}')
        self.frame_iteration += 1
        reward = 0
        if self.enable_gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        self._change_direction(action) # action to direction

        # new snake head
        self.head = self.move(self.head, self.direction)

        # check if the game is over
        if self._is_collision() or self.frame_iteration > 100 * len(self.snake):
            self.game_over = True
            reward = -10
            self.reward = reward
            self.total_reward += self.reward
            return self._get_state(), reward, self.game_over
        if self.head == self.food:
            print('eat food')
            self.score += 1
            reward = 10
            if self.enable_gui and self.is_human:
                time.sleep(0.5)
            self.food = self._place_food()
        else:
            self.snake.pop() # remove the tail
            reward = -0.1  # small punishment
        self.snake.insert(0, self.head.copy()) # set snake head
        print(f'snake {self.snake},  food {self.food}')
        if self.enable_gui:
            self._render()
        self.reward = reward
        self.total_reward += self.reward
        return self._get_state(), reward, self.game_over
    
    def _change_direction(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if action == Action.STRAIGHT:
            new_direction = clock_wise[idx]
        elif action == Action.RIGHT:
            new_direction = clock_wise[(idx + 1) % 4]
        else:
            new_direction = clock_wise[(idx - 1) % 4]
        print(f'change direction: {self.direction} -> {new_direction}')
        self.direction = new_direction
        return
    
    def _render(self):
        self.screen.fill(COLOR_BLACK)
        # draw grid
        color = (40, 40, 40)
        for x in range(0, self.width*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height*self.cell_size))
        for y in range(0, self.height*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width*self.cell_size, y))
        
        # draw snake
        for i, segment in enumerate(self.snake):
            color = COLOR_GREEN if i == 0 else COLOR_BLUE  # set color of snake head / body
            x, y, w, h = segment[0] * self.cell_size, segment[1] * self.cell_size, self.cell_size, self.cell_size
            rect = (x, y, w, h)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0,100,0), rect, 1)
        
        # draw food
        color = COLOR_RED
        x, y, w, h = self.food[0] * self.cell_size, self.food[1] * self.cell_size, self.cell_size, self.cell_size
        line_width = 2
        rect = (x, y, w, h)
        pygame.draw.rect(self.screen, COLOR_RED, rect)
        pygame.draw.rect(self.screen, (180,0,0), rect, line_width)
        
        # display score
        score_text = self.font.render(f'Score: {self.score}', True, COLOR_WHITE)
        self.screen.blit(score_text, (5, 10))
        
        # display reward
        score_text = self.font.render(f'Reward: {self.reward}', True, COLOR_RED if self.reward < 0 else COLOR_GREEN)
        self.screen.blit(score_text, (85, 10))
        
        # display total reward
        score_text = self.font.render(f'Total Reward: {round(self.total_reward,2)}', True, COLOR_WHITE)
        self.screen.blit(score_text, (180, 10))
        if self.reward > 0 and self.is_human:
            time.sleep(0.5)
        pygame.display.flip()
        self.clock.tick(30)  # fps (frames per seconds)

def direction_to_action(old_direction:Direction, new_direction:Direction):
    action = Action.STRAIGHT
    if (old_direction == new_direction) or (old_direction == Direction.UP and new_direction == Direction.DOWN) or (old_direction == Direction.RIGHT and new_direction == Direction.LEFT) or (old_direction == Direction.LEFT and new_direction == Direction.RIGHT) or (old_direction == Direction.DOWN and new_direction == Direction.UP):   # 下 -> 上
        action = Action.STRAIGHT
    elif (old_direction == Direction.UP and new_direction == Direction.LEFT) or (old_direction == Direction.RIGHT and new_direction == Direction.UP)  or (old_direction == Direction.DOWN and new_direction == Direction.RIGHT)  or (old_direction == Direction.LEFT and new_direction == Direction.DOWN):
        action = Action.LEFT
    elif (old_direction == Direction.LEFT and new_direction == Direction.UP) or (old_direction == Direction.UP and new_direction == Direction.RIGHT)  or (old_direction == Direction.RIGHT and new_direction == Direction.DOWN)  or (old_direction == Direction.DOWN and new_direction == Direction.LEFT):
        action = Action.RIGHT
    else:
        print(f'error: old direction = {old_direction}, new direction = {new_direction}')
    return action

def play_snake_game():
    game = SnakeGame(width=30, height=20, enable_gui=True, is_human=True)
    state = game.reset()
    game._render()
    
    direction_mapping = {pygame.K_UP: Direction.UP, pygame.K_DOWN: Direction.DOWN, pygame.K_LEFT: Direction.LEFT, pygame.K_RIGHT: Direction.RIGHT}
    print("Game Start!")
    print("Press ESC to exit")
    direction = Direction.RIGHT  # default direction
    running = True
    while running:
        action = Action.STRAIGHT
        for event in pygame.event.get():
            print(f'event {event}')
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in direction_mapping:
                    current_direction = direction_mapping[event.key] # key to direction
                    print(f'event.key {event.key}, direction: {direction}, current_direction: {current_direction}')
                    action = direction_to_action(direction, current_direction) # direction to action
                    direction = current_direction # update direction
                    break
                elif event.key == pygame.K_ESCAPE:
                    running = False
        print(f'!!xxx action: {action_name[action]}')
        state, reward, done = game.step(action) # execute one step
        print(f'state {state}, reward {reward}, done {done}')
        if done:
            print(f"Game Over! Score: {game.score}")
            pygame.time.delay(5000)
            break
        pygame.time.delay(200)  # speed
    pygame.quit()
    print("Game Over!")

if __name__ == '__main__':
    play_snake_game()
