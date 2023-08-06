import pygame
import random
from score import Score
from sys import exit
from character import RunnerCharacter
from enemies import Monsters





# initilise pygame
pygame.init()





# display surface
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel-Stride")
background = pygame.image.load("Sky.png").convert()

# ground
ground = pygame.image.load("ground.png").convert()
ground_rect = ground.get_rect(midtop=(400, 300))


game_speed = 5

x_pos_bg = ground_rect.x
y_pos_bg = ground_rect.y


def Background():
    global x_pos_bg, y_pos_bg, game_speed
    image_width = ground.get_width()
    screen.blit(ground, (x_pos_bg, y_pos_bg))
    screen.blit(ground, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        screen.blit(ground, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= game_speed


# game_states
in_game = False
start_menu_active = True






player = pygame.sprite.GroupSingle()
player.add(RunnerCharacter())


enemies_sprite_group = pygame.sprite.Group()


score = Score()

# game variables
game_font = pygame.font.Font("Pixeltype.ttf", 50)
score_text = game_font.render(f"Score:{score}", False, (64, 64, 64))
score_text_rect = score_text.get_rect(center=(400, 100))

game_title = game_font.render("PIXEL STRIDE", False, (0, 0, 0))
game_title_rect = game_title.get_rect(center = (400,150))

button = pygame.image.load("button_image.png").convert_alpha()
pygame.transform.rotozoom(button, 0, 0.5)
button_rect = button.get_rect(center = (400,200))

# game_variables
start_time = 0
# vel = 100
# jump = False

keys = pygame.key.get_pressed()


# clock object
clock = pygame.time.Clock()





# Timer
enemy_spawn_time = 1000
enemy_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn_timer, enemy_spawn_time)
enemy_spawn_count = 1

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemies_sprite_group , False):
        score.save_score()
        enemies_sprite_group.empty()
        return False
    return True

while True:

    screen.blit(background, (0, 0))
    screen.blit(ground, ground_rect)

    Background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score.save_score()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and start_menu_active == True:
            if button_rect.collidepoint(event.pos):
                start_menu_active = False
                in_game = True


        if event.type == enemy_spawn_timer:
            # for i in range(enemy_spawn_count):
            if random.choice(["fly","snail","snail"]) == "fly":
                enemies_sprite_group.add(Monsters("fly"))
            else:
                enemies_sprite_group.add(Monsters("snail"))

            # enemy_spawn_count += 1
            #
            # if enemy_spawn_count == 2:
            #     enemy_spawn_count = 1



    if in_game and not start_menu_active:

        score.update_score(start_time)
        screen.blit(score.score_text,score.score_text_rect)



        # # Player
        player.draw(screen)
        player.update()

        # Enemy
        enemies_sprite_group.draw(screen)
        enemies_sprite_group.update()


        # collision
        in_game = collision_sprite()
        if in_game == False:
            start_menu_active = True
            enemy_spawn_count = 0
            score.current_score = 0
            start_time = pygame.time.get_ticks()

    elif start_menu_active and not in_game:
         screen.blit(button, button_rect)
         screen.blit(game_title, game_title_rect)
         score.best_score_text = score.game_font.render(f"Best Score: {score.show_best_score()}", False, (64, 64, 64))
         score.best_score_text_rect = score.best_score_text.get_rect(center=(400, 350))
         screen.blit(score.best_score_text,score.best_score_text_rect)


    pygame.display.update()
    clock.tick(60)




