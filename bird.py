import pygame
import random
import math

pygame.init()

class Bird:
    def __init__(self):
        self.screen = pygame.display.set_mode((576, 1024))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font("04B_19.ttf", 40)

        # Game Variables
        self.gravity = 0.2

        # Setup the background picture
        self.bg_surface = pygame.image.load("assets/background-day.png").convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)

        self.floor_surface = pygame.image.load("assets/base.png").convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_x_pos = -5

        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)

        self.pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface) 

        self.game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
        self.game_over_surface = pygame.transform.scale2x(self.game_over_surface)
        self.game_over_rect = self.game_over_surface.get_rect(center = (288, 512))
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0

        random_pipe_pos = random.randint(400, 800)
        self.bottom_pipe = self.pipe_surface.get_rect(midtop = (700, random_pipe_pos))
        self.top_pipe = self.pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 250))
        self.pipe_list = [self.bottom_pipe, self.top_pipe]
        self.game_active = True

        bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
        bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
        bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()

        bird_downflap = pygame.transform.scale2x(bird_downflap)
        bird_midflap = pygame.transform.scale2x(bird_midflap)
        bird_upflap = pygame.transform.scale2x(bird_upflap)
        self.bird_frames = [bird_downflap, bird_midflap, bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100, 512))

    def jump(self):
        self.bird_movement = 0
        self.bird_movement -= 8

    def create_pipe(self):
        random_pipe_pos = random.randint(400, 800)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 250))
        return bottom_pipe, top_pipe
        
    def run(self):
        if not self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            return (None, self.score, self.game_active)
        # Helper function
        def draw_floor():
            self.screen.blit(self.floor_surface, (self.floor_x_pos, 900))
            self.screen.blit(self.floor_surface, (self.floor_x_pos + 567, 900))

        

        def move_pipes(pipes):
            for pipe in pipes:
                pipe.centerx -= 5
            if pipes:
                if pipes[0].right < self.bird_rect.left:
                    pipes.pop(0)
                    pipes.pop(0)
                self.score += 0.01
            return pipes

        def draw_pipes(pipes):
            for pipe in pipes:
                if pipe.bottom >= 1024:
                    self.screen.blit(self.pipe_surface, pipe)
                else:
                    flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                    self.screen.blit(flip_pipe, pipe)

        def check_collision(pipes):
            for pipe in pipes:
                if self.bird_rect.colliderect(pipe):
                    return False
            if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
                return False
            return True

        def rotate_bird(bird):
            new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 3, 1)
            return new_bird

        def bird_animation():
            new_bird = self.bird_frames[self.bird_index]
            new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
            return new_bird, new_bird_rect

        def score_display(game_state):
            if game_state == "main_game":
                score_surface = self.game_font.render(f"{int(self.score)}", True, (255, 255, 255))
                score_rect = score_surface.get_rect(center = (288, 100))
                self.screen.blit(score_surface, score_rect)
            if game_state == "game_over":
                score_surface = self.game_font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
                score_rect = score_surface.get_rect(center = (288, 100))
                self.screen.blit(score_surface, score_rect)

                high_score_surface = self.game_font.render(f"Highest Score: {int(self.high_score)}", True, (255, 255, 255))
                high_score_rect = high_score_surface.get_rect(center = (288, 850))
                self.screen.blit(high_score_surface, high_score_rect)

        def update_score(score, high_score):
            if score > high_score:
                high_score = score
            return high_score

        

        # create the screen
        if not self.pipe_list:
            self.pipe_list.extend(self.create_pipe())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird_movement = 0
                    self.bird_movement -= 8
                if event.key == pygame.K_SPACE and self.game_active == False:
                    self.reset()
            if event.type == self.BIRDFLAP:
                self.bird_index += 1
                self.bird_index %= 3
                self.bird_surface, self.bird_rect = bird_animation()
        self.screen.blit(self.bg_surface, (0, 0))
        self.game_active = check_collision(self.pipe_list)
        if self.game_active:
            # bird
            self.bird_movement += self.gravity
            rotated_bird = rotate_bird(self.bird_surface)
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(rotated_bird, self.bird_rect)
            
            # pipes
            self.pipe_list = move_pipes(self.pipe_list)
            draw_pipes(self.pipe_list)

            
            score_display("main_game")
        else:
            self.screen.blit(self.game_over_surface, self.game_over_rect)
            self.high_score = update_score(self.score, self.high_score)
            score_display("game_over")
        # floor
        self.floor_x_pos -= 1
        draw_floor()
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0
        pygame.display.update()
        self.clock.tick(100)
        if not self.pipe_list:
            self.pipe_list.extend(self.create_pipe())
        return ((self.pipe_list[0].left, self.pipe_list[0].right, self.pipe_list[0].top, self.pipe_list[1].bottom, self.bird_movement, self.bird_rect.centery, self.bird_rect.centerx), self.score, self.game_active)

    def step(self, action):
        if action == 0:
            self.jump()
        if not self.pipe_list:
            self.pipe_list.extend(self.create_pipe())
        return self.run()

    def reset(self):
        self.bird_movement = 0
        self.score = 0
        self.bird_index = 0
        self.pipe_list = [self.bottom_pipe, self.top_pipe]
        self.game_active = True
        self.bird_rect = self.bird_surface.get_rect(center = (100, 512))
        return (self.pipe_list[0].left, self.pipe_list[0].right, self.pipe_list[0].top, self.pipe_list[1].bottom, self.bird_movement, self.bird_rect.top, self.bird_rect.bottom)

if __name__ == '__main__':
    bird = Bird()
    while True:
        bird.run()
