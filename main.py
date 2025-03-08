import pygame
import random

pygame.init()

# constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GROUND_HEIGHT = 112
GRAVITY = 0.25
JUMP_SPEED = -5
PIPE_SPEED = 3
PIPE_SPAWN_TIME = 1000  # milliseconds
PIPE_GAP = 100

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        
        self.load_assets()
        self.reset_game()
        self.clock = pygame.time.Clock()
        
    def load_assets(self):
        self.bird = pygame.image.load('assets/yellowbird-upflap.png')
        self.pipe = pygame.image.load('assets/pipe-green.png')
        self.background = pygame.image.load('assets/background-night.png')
        self.base = pygame.image.load('assets/base.png')
        self.game_over = pygame.image.load('assets/gameover.png')
        self.get_ready = pygame.image.load('assets/message.png')
        
        # load numbers
        self.numbers = []
        for i in range(10):
            number = pygame.image.load(f'assets/{i}.png')
            self.numbers.append(number)
            
    def reset_game(self):
        self.game_state = "START"
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.score = 0
        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "START":
                        self.game_state = "PLAYING"
                    elif self.game_state == "PLAYING":
                        self.bird_velocity = JUMP_SPEED
                    elif self.game_state == "GAME_OVER":
                        self.reset_game()
        return True

    def update(self):
        if self.game_state == "PLAYING":
            # update bird position
            self.bird_velocity += GRAVITY
            self.bird_y += self.bird_velocity

            # prevent bird from hitting floor/ceiling
            if self.bird_y > SCREEN_HEIGHT - GROUND_HEIGHT - self.bird.get_height() or self.bird_y < 0:
                if self.bird_y > SCREEN_HEIGHT - GROUND_HEIGHT - self.bird.get_height():
                    self.bird_y = SCREEN_HEIGHT - GROUND_HEIGHT - self.bird.get_height()
                if self.bird_y < 0:
                    self.bird_y = 0
                self.bird_velocity = 0
                self.game_state = "GAME_OVER"

            # generate pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_time > PIPE_SPAWN_TIME:
                pipe_y = random.randint(PIPE_GAP + 50, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
                self.pipes.append({"x": SCREEN_WIDTH, "y": pipe_y})
                self.last_pipe_time = current_time
            
            # update pipes
            for pipe in self.pipes[:]:
                pipe["x"] -= PIPE_SPEED
                
                # check collision
                bird_rect = pygame.Rect(50, self.bird_y, self.bird.get_width(), self.bird.get_height())
                top_pipe_rect = pygame.Rect(pipe["x"], 0, self.pipe.get_width(), pipe["y"] - PIPE_GAP)
                bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["y"], self.pipe.get_width(), SCREEN_HEIGHT)
                
                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                    self.game_state = "GAME_OVER"
                
                # score point
                if not pipe.get("scored", False) and pipe["x"] + self.pipe.get_width() < 50:
                    self.score += 1
                    pipe["scored"] = True
                
                # remove off-screen pipes
                if pipe["x"] < -self.pipe.get_width():
                    self.pipes.remove(pipe)

    def draw(self):
        # draw background
        self.screen.blit(self.background, (0, 0))
        
        # draw pipes
        for pipe in self.pipes:
            self.screen.blit(self.pipe, (pipe["x"], pipe["y"]))
            flipped_pipe = pygame.transform.flip(self.pipe, False, True)
            self.screen.blit(flipped_pipe, (pipe["x"], pipe["y"] - PIPE_GAP - self.pipe.get_height()))
        
        # draw bird
        if self.game_state != "START":
            self.screen.blit(self.bird, (50, self.bird_y))
        
        # draw score
        if self.game_state != "START":
            score_str = str(self.score)
            score_width = sum(self.numbers[int(d)].get_width() for d in score_str)
            x = (SCREEN_WIDTH - score_width) // 2
            for digit in score_str:
                num_image = self.numbers[int(digit)]
                self.screen.blit(num_image, (x, 50))
                x += num_image.get_width()
        
        # draw game state screens
        if self.game_state == "START":
            self.screen.blit(self.get_ready, ((SCREEN_WIDTH - self.get_ready.get_width()) // 2, 50))
        elif self.game_state == "GAME_OVER":
            self.screen.blit(self.game_over, ((SCREEN_WIDTH - self.game_over.get_width()) // 2, 200))
        
        # draw the base
        base_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.screen.blit(self.base, (0, base_y))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = FlappyBird()
    game.run()