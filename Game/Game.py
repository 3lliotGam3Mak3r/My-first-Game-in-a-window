import pygame
import sys


#function to setup the game
def setup_game(window_width=1300, window_height=750):
    
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Boss battle")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    #gets player name
    name = input("Name: ")
    

    #Loads player
    player_image = pygame.image.load('player.png')
    
    player_image = pygame.transform.scale(player_image, 
                                          (int(player_image.get_width() * 0.25), 
                                           int(player_image.get_height() * 0.25)))
    
    player_rect = player_image.get_rect()
    player_rect.x = window_width // 3
    player_rect.y = window_height // 3

    # Set up font 
    font = pygame.font.SysFont("Comic Sans", 48)  # You can also use pygame.font.Font('your_font.ttf', size)
    # Render the text
    text_surface = font.render(name, True, (0, 0, 0))  # Text, anti-aliasing, color
    #centers it
    text_rect = text_surface.get_rect(center=(window_width // 14, window_height // 18))
    

    #creates 2 health bar assets
    player_health = pygame.image.load('health.png')
    player_h_rect = player_health.get_rect()
    player_h_rect.x = window_width // 17
    player_h_rect.y = window_height // 12
    player_health = pygame.transform.scale(player_health, 
                                          (int(player_health.get_width() * 0.3), 
                                           int(player_health.get_height() * 0.3)))
    
    player_health2 = pygame.image.load('health2.png')
    player_h2_rect = player_health2.get_rect()
    player_h2_rect.x = window_width // 7
    player_h2_rect.y = window_height // 12
    player_health2 = pygame.transform.scale(player_health2, 
                                          (int(player_health2.get_width() * 0.3), 
                                           int(player_health2.get_height() * 0.3)))
    player_health_value = 2  # Player starts with 2 health points
    player_damage_cooldown = 0


    #makes the boss and then the boss healthbar and then the code allowing it to move around
    boss_image = pygame.image.load('boss1.png')
    boss_image = pygame.transform.scale(boss_image, 
                                          (int(boss_image.get_width() * 1), 
                                           int(boss_image.get_height() * 1)))
    boss_rect = boss_image.get_rect()
    boss_rect.x = window_width // 2
    boss_rect.y = window_height // 4
    boss_health = 100  # Max health
    boss_damage_cooldown = 0  # A cooldown to prevent damage every single frame

    boss_velocity_x = 5  # horizontal speed
    boss_velocity_y = 3  # vertical speed

    minion_image = pygame.image.load('boss2.png')
    minion_image = pygame.transform.scale(minion_image, 
                                          (int(minion_image.get_width() * 0.25), 
                                           int(minion_image.get_height() * 0.25)))
    minion_rect = minion_image.get_rect()
    minion_rect.x = window_width // 2
    minion_rect.y = window_height // 2
    
    minion_velocity_x = 10  # horizontal speed
    minion_velocity_y = 8  # vertical speed


    boss_bar = pygame.image.load('bossbar.png')
    boss_bar = pygame.transform.scale(boss_bar, 
                                          (int(boss_bar.get_width() * 2), 
                                           int(boss_bar.get_height() * 1)))
    boss_b_rect = boss_bar.get_rect()
    boss_b_rect.x = window_width // 4.5
    boss_b_rect.y = window_height // 1.1


    #creates a speed var for the player
    speed = 15

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player_rect.y -= speed  # Move up
        if keys[pygame.K_s]:
            player_rect.y += speed  # Move down
        if keys[pygame.K_a]:
            player_rect.x -= speed  # Move left
        if keys[pygame.K_d]:
            player_rect.x += speed  # Move right

        # Handle cooldown timer (optional, to avoid damage every frame)
        if boss_damage_cooldown > 0:
            boss_damage_cooldown -= 1

        # Handle cooldown timer for player damage
        if player_damage_cooldown > 0:
            player_damage_cooldown -= 1

        # Check collision between player and minion
        if player_rect.colliderect(minion_rect) and player_damage_cooldown == 0:
            player_health_value -= 1  # Damage player
            player_damage_cooldown = 30  # Cooldown before next damage
            print(f"Player Health: {player_health_value}")

        if player_health_value <= 0:
            minion_image = pygame.image.load('boss1.png')
            print("Player Defeated!")
            running = False

        # Check collision between player and boss
        if player_rect.colliderect(boss_rect) and boss_damage_cooldown == 0:
            boss_health -= 10  # Damage boss
            boss_damage_cooldown = 30  # Prevent instant repeated damage (adjust as needed)
            print(f"Boss Health: {boss_health}")

        if boss_health <= 0:
            boss_velocity_y = 0
            boss_velocity_x = 0
            minion_velocity_y = 0
            minion_velocity_x = 0
            boss_image = pygame.image.load('boss2.png')
            pygame.time.wait(5000)
            print("Boss Defeated!")
            running = False

            # Move the boss
        boss_rect.x += boss_velocity_x
        boss_rect.y += boss_velocity_y

        minion_rect.x += minion_velocity_x
        minion_rect.y += minion_velocity_y


        # Bounce boss off window edges
        if boss_rect.left <= 0 or boss_rect.right >= window_width:
            boss_velocity_x = -boss_velocity_x
        if boss_rect.top <= 0 or boss_rect.bottom >= window_height:
            boss_velocity_y = -boss_velocity_y

        if minion_rect.left <= 0 or minion_rect.right >= window_width:
            minion_velocity_x = -minion_velocity_x
        if minion_rect.top <= 0 or minion_rect.bottom >= window_height:
            minion_velocity_y = -minion_velocity_y



        window.fill(WHITE)

        # draw the boss and minion
        window.blit(boss_image, boss_rect)
        window.blit(minion_image, minion_rect)

        # draw the player 
        window.blit(player_image, player_rect)

        # Draw health bar and name 
        window.blit(text_surface, text_rect)
        if player_health_value == 2:
            window.blit(player_health, player_h_rect)
            window.blit(player_health2, player_h2_rect)
        elif player_health_value == 1:
            window.blit(player_health, player_h_rect)
        # if player_health_value <= 0, don't show any health bar

        # Scale boss health bar based on remaining health
        current_boss_bar = pygame.transform.scale(boss_bar,(int((boss_health / 100) * boss_bar.get_width()), boss_bar.get_height()))
        
        window.blit(current_boss_bar, boss_b_rect)
    

        # Update the display
        pygame.display.update()

        # Frame rate
        pygame.time.Clock().tick(60)  # Limit to 60 FPS


        pygame.display.update()  # Update the display

        pygame.time.wait(10)
    
    pygame.quit()
    sys.exit()

setup_game()


