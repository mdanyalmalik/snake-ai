import pygame as pg

from constants import *
from snake import Snake


class DQSnake(Snake):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.frame_iteration = 0

    def move(self, action):
        if action[0] and not self.vy == V:
            self.vx, self.vy = 0, -V
        elif action[1] and not self.vy == -V:
            self.vx, self.vy = 0, V
        elif action[2] and not self.vx == V:
            self.vx, self.vy = -V, 0
        elif action[3] and not self.vx == -V:
            self.vx, self.vy = V, 0

        head = self.head_pos()

        new_x = head[0] + self.vx
        new_y = head[1] + self.vy

        self.positions.insert(0, (new_x, new_y))
        self.positions.pop()

    def check_collision(self, point=None):
        head = self.head_pos()
        reward = 0
        game_over = False

        if point is None:
            point = head

        if point in self.positions[2:]:
            reward = -100
            game_over = True

        if point[0] >= WIDTH or point[0] < 0 or point[1] >= HEIGHT or point[1] < 0:
            reward = -100
            game_over = True

        if self.frame_iteration > 100 * len(self.positions):
            reward = -200
            game_over = True

        return reward, game_over

    def food_check_eaten(self):
        reward = 0
        if self.food.check_eaten(self):
            reward = 10
        return reward

    def draw_info(self, win, font, game_no, record, fps, max_fps):
        if fps == max_fps:
            text = f'Game: {game_no} | Score: {self.score} | Record: {record} | Max Speed: Unlimited '
        else:
            text = f'Game: {game_no} | Score: {self.score} | Record: {record} | Max Speed: {fps} '

        self.info_render = font.render(text, False, WHITE)
        self.text_width = self.info_render.get_rect().width
        win.blit(self.info_render, (WIDTH-self.text_width, 0))

    def reset(self):
        self.vx, self.vy = V, 0
        x, y = (WIDTH//2, HEIGHT//2)
        self.positions = [(x, y), (x-GRID_DIV, y),
                          (x-2*GRID_DIV, y)]
        self.score = 0
        self.frame_iteration = 0
        self.food.spawn()
