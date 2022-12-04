import pygame
import sys


def main():
    pygame.init()
    pygame.display.set_caption("test_room")
    screen = pygame.display.set_mode((600, 600))
    running = True
    player = pygame.image.load("girl_w.png").convert()
    player.set_colorkey((255, 255, 255))
    print(player.get_rect())

    block = pygame.Rect(60, 400, 200, 30)
    block2 = pygame.Rect(240, 400, 100, 30)
    block3 = pygame.Rect(300, 250, 100, 30)
    block4 = pygame.draw.circle(screen, (255, 255, 255), (40, 80), 10)
    player_move = [50, 0]
    player_is_move = [False, False, False, False]
    clock = pygame.time.Clock()
    player_flip = False
    player_stay = True
    player_jump_up = []
    player_jump_down = False
    jump_speed = 3
    jump_rect = pygame.Rect(0, 0, 0, 0)
    while running:
        clock.tick(60)
        blocks = [block, block2, block3, block4]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_flip = False
                    player_is_move[0] = True
                if event.key == pygame.K_LEFT:
                    player_flip = True
                    player_is_move[1] = True
                if event.key == pygame.K_DOWN:
                    player_is_move[2] = True
                if event.key == pygame.K_UP:
                    player_is_move[3] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player_is_move[0] = False
                if event.key == pygame.K_LEFT:
                    player_is_move[1] = False
                if event.key == pygame.K_DOWN:
                    player_is_move[2] = False
                if event.key == pygame.K_UP:
                    player_is_move[3] = False
        if player_is_move[0]:
            m = [player_move[0] + 4, player_move[1]]
            col = player.get_rect().move(m).collidelist(blocks)
            if col == -1:
                player_move = m
            else:
                player_move = [blocks[col].left - player.get_width(), m[1]]
        if player_is_move[1]:
            m = [player_move[0] - 4, player_move[1]]
            col = player.get_rect().move(m).collidelist(blocks)
            if col == -1:
                player_move = m
            else:
                player_move = [blocks[col].right, m[1]]
        if player_is_move[2]:
            m = [player_move[0], player_move[1] + 4]
            col = player.get_rect().move(m).collidelist(blocks)
            if col == -1:
                player_move = m
            else:
                player_move = [m[0], blocks[col].top - player.get_height()]
        if player_is_move[3] and player_stay:
            jump_speed = 1.3
            m = [player_move[0], player_move[1]]
            player_jump_up = m   
            player_stay = False
        if player_jump_down and player_jump_up == []:
            if jump_speed + 0.1 <= 2.6:
                jump_speed += 0.1
            else:
                jump_speed = 2.6
            if player.get_rect().move(player_move[0], player_move[1] + (4 * jump_speed)).collidelist(blocks) == -1:
                player_move[1] += (4 * jump_speed)
                player_stay = False
            else:
                col = player.get_rect().move(player_move[0], player_move[1] + (4 * jump_speed)).collidelist(blocks)
                player_move[1] = blocks[col].top - player.get_height()
                player_stay = True
            #player_move[1] += (4 * jump_speed)

        if player_jump_up != []:
            if jump_speed == 0:
                #player_move[1] = player_jump_up[1]
                player_jump_up = []
                #player_stay = True
                jump_speed = 0
                player_jump_down = True
                
            else:
                jump_speed -= 0.04
                if jump_speed < 0:
                    jump_speed = 0
                col = player.get_rect().move(player_move[0], player_move[1] - (8 * jump_speed)).collidelist(blocks)
                if col != -1:
                    jump_speed = 0
                    player_move[1] = blocks[col].bottom
                    
                    #player_move[1] = player_jump_up[1]
                player_move[1] -= (8 * jump_speed)
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), jump_rect, 0)
        if player.get_rect().move(player_move).collidelist(blocks) == -1:
            block = pygame.draw.rect(screen, (255, 255, 255), block, 0)
            block2 = pygame.draw.rect(screen, (255, 255, 255), block2, 0)
            block3 = pygame.draw.rect(screen, (255, 255, 255), block3, 0)
            block4 = pygame.draw.circle(screen, (255, 255, 255), (block4.x + 10, block4.y + 10), 10)
        else:
            col = player.get_rect().move(player_move).collidelist(blocks)
            blocks[col] = pygame.draw.rect(screen, (255, 255, 255), blocks[col], 0)
        if player_move[1] > player.get_height() + screen.get_size()[1]:
            player_move[1] = 0 - player.get_height()
        screen.blit(pygame.transform.flip(player, player_flip, False), player_move)
        pygame.display.flip()


if __name__ == '__main__':
    main()
