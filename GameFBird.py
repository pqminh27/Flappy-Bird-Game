import pygame, sys, random
#function for game
def draw_floor():
    screen.blit(floor,(floor_x_pos, 600)) 
    screen.blit(floor,(floor_x_pos + 432, 600)) 

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 650))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 6
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -80 or bird_rect.bottom >= 675:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_move*1.5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}',True,(0,255,255))
        score_rect = score_surface.get_rect(center = (220,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,640))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512) 
# convert sound file into pygame
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FileGame/04B_19.TTF', 38)
# variables for game
gravity = 0.27
bird_move = 0
game_active = True
score = 0
high_score = 0
 
# backgropund
bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# floor
floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# create bird
bird_down = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

# create timer for bird
birdflap =  pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 1000)

#create pipe
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

#create timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 2000)
pipe_height = [200,300,400]

# create end screen
game_over_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))
# sound
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
point_sound_countdown = 200

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_move = 0 
                bird_move = -10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_move = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg,(0,0))
    if game_active == True:
        # bird
        bird_move += gravity
        Rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_move
        screen.blit(Rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main_game')
        point_sound_countdown -= 1
        if point_sound_countdown <= 0:
            point_sound.play()
            point_sound_countdown = 200
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(20)

