import pygame
import random
import sys
from pyvidplayer import Video

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ANIMAL_WIDTH = 50
ANIMAL_HEIGHT = 50
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
SCORE_FONT_SIZE = 36
GAME_OVER_FONT_SIZE = 48
THEME_PLAYING = False

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monty.py")

# Load images
background_img = pygame.image.load("background.jpg").convert()
loadscreen_img = pygame.image.load("loadscreen.png").convert()
cow_img = pygame.image.load("cow.png").convert_alpha()
goat_img = pygame.image.load("goat.png").convert_alpha()
duck_img = pygame.image.load("duck.png").convert_alpha()
cat_img = pygame.image.load("cat.png").convert_alpha()
grail_img = pygame.image.load("holygrail.PNG").convert_alpha()

# Load Sounds
pygame.mixer.music.load("Theme.mp3")
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play()
PLAYTAUNT=pygame.USEREVENT + 1
# Play french guy taunt
pygame.time.set_timer(PLAYTAUNT, 6000)

# Load player shield images
player_img1 = pygame.transform.smoothscale(pygame.image.load("shield1.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
player_img2 = pygame.transform.smoothscale(pygame.image.load("shield2.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))

# Resize images
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cow_img = pygame.transform.scale(cow_img, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
goat_img = pygame.transform.scale(goat_img, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
duck_img = pygame.transform.scale(duck_img, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
cat_img = pygame.transform.scale(cat_img, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
grail_img = pygame.transform.scale(grail_img, (ANIMAL_WIDTH, ANIMAL_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Variables
clock = pygame.time.Clock()
COUNTDOWN = pygame.USEREVENT +2
pygame.time.set_timer(COUNTDOWN, 1000)
countdown = 30
game_over = False
game_started = False  # Game won't start until spacebar is pressed
animals = []
animal_speeds = [2, 3, 4, 4.5]  # Slower speeds for animals
spinning = [True, False]  # Options for spinning

# Player Class
class Player:
    def __init__(self, x, y, img):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = img  # Use the shield image
        self.score = 0  # Initialize score
    
    def move(self, dx):
        self.rect.x += dx
        # Keep player within screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH
    
    def draw(self):
        # Draw the player's image instead of a rectangle
        screen.blit(self.image, self.rect.topleft)

# Animal Class
class Animal:
    def __init__(self, x, speed, animal_type):
        self.rect = pygame.Rect(x, 0, ANIMAL_WIDTH, ANIMAL_HEIGHT)
        self.speed = speed
        self.animal_type = animal_type  # Store which animal type it is
        self.rotation = random.choice(spinning)  # Randomly choose whether to spin

    def move(self):
        self.rect.y += self.speed
    
    def draw(self):
        if self.rotation:  # If spinning, rotate the image
            angle = (pygame.time.get_ticks() // 10) % 360
            if self.animal_type == 'cow':
                rotated_image = pygame.transform.rotate(cow_img, angle)
                screen.blit(rotated_image, self.rect.topleft)
            elif self.animal_type == 'goat':
                rotated_image = pygame.transform.rotate(goat_img, angle)
                screen.blit(rotated_image, self.rect.topleft)
            elif self.animal_type == 'duck':
                rotated_image = pygame.transform.rotate(duck_img, angle)
                screen.blit(rotated_image, self.rect.topleft)
            elif self.animal_type == 'cat':
                rotated_image = pygame.transform.rotate(cat_img, angle)
                screen.blit(rotated_image, self.rect.topleft)
            elif self.animal_type == 'grail':
                rotated_image = pygame.transform.rotate(grail_img, angle)
                screen.blit(rotated_image, self.rect.topleft)
        else:
            if self.animal_type == 'cow':
                screen.blit(cow_img, self.rect.topleft)
            elif self.animal_type == 'goat':
                screen.blit(goat_img, self.rect.topleft)
            elif self.animal_type == 'duck':
                screen.blit(duck_img, self.rect.topleft)
            elif self.animal_type == 'cat':
                screen.blit(cat_img, self.rect.topleft)
            elif self.animal_type == 'grail':
                screen.blit(grail_img, self.rect.topleft)

# Function to create animals
def create_animal():
    x = random.randint(0, SCREEN_WIDTH - ANIMAL_WIDTH)
    speed = random.choice(animal_speeds)
    animal_type = random.choice(['cow', 'goat', 'duck', 'cat','grail'])  # Randomly choose animal type
    # Randomly choose and play sound effect
    spawn_sfx = pygame.mixer.Sound(random.choice(['Sounds/cow.wav', 'Sounds/pig.wav', 'Sounds/chicken.wav',
                                                  'Sounds/chicken 2.wav', 'Sounds/sheep.wav']))
    spawn_sfx.set_volume(.2)
    spawn_sfx.play()
    return Animal(x, speed, animal_type)

# Function to display scores
def display_scores(player1, player2):
    score_textp1 = f"Player 1 Score: {player1.score}"
    score_textp2 = f"Player 2 Score: {player2.score}"
    score_surfacep1 = pygame.font.Font(None, SCORE_FONT_SIZE).render(score_textp1, True, (255, 255, 0),(0, 0, 0))
    score_surfacep2 = pygame.font.Font(None, SCORE_FONT_SIZE).render(score_textp2, True, (204, 0, 0), (0, 0, 0))
    screen.blit(score_surfacep1, (20, 20))
    screen.blit(score_surfacep2, (575, 20)) # Positioning the score at the top left
    countdown_text = f"{countdown}"
    countdown_message = pygame.font.Font(None, 80).render(countdown_text, True, (255, 255, 255), (0, 0, 0))
    screen.blit(countdown_message, (375, 30))

# Game Loop
def game_loop():
    global game_over, game_started, countdown
    player1 = Player(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, player_img1)
    player2 = Player(600, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, player_img2)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:  # Start the game on spacebar press
                    pygame.mixer.music.stop() # Stop playing theme
                    playintro()
                    game_over = False
                    game_started = True
                    animals.clear()  # Clear animals before starting
                if event.key == pygame.K_r and game_over:
                    # Restart the game
                    game_started = False
                    game_over = False
                    animals.clear()  # Clear animals for a new game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == PLAYTAUNT and not game_over and game_started:
                taunt_sfx=pygame.mixer.Sound(random.choice(['taunts/fart.mp3', 'taunts/french.mp3', 'taunts/hamster.mp3',
                                                            'taunts/taunt.wav', 'taunts/wipe.mp3']))
                taunt_sfx.set_volume(.2)
                taunt_sfx.play()
            if event.type == COUNTDOWN and not game_over and game_started:
                countdown -= 1
                if countdown < 0:
                    game_over = True
                    countdown = 30
                    if player1.score > player2.score:
                        winner_text = "Player 1 Wins!"
                    elif player1.score == player2.score:
                        winner_text = "Tie Score"
                    else:
                        winner_text = "Player 2 Wins!"
        
        keys = pygame.key.get_pressed()
        if game_started and not game_over:
            if keys[pygame.K_a]:  # Player 1 moves left
                player1.move(-5)
            if keys[pygame.K_d]:  # Player 1 moves right
                player1.move(5)
            if keys[pygame.K_LEFT]:  # Player 2 moves left
                player2.move(-5)
            if keys[pygame.K_RIGHT]:  # Player 2 moves right
                player2.move(5)

            # Update the game state
            if random.random() < 0.05:  # Chance to create a new animal
                animals.append(create_animal())

            for animal in animals[:]:
                animal.move()
                if animal.rect.y > SCREEN_HEIGHT:
                    animals.remove(animal)  # Remove off-screen animals

                # Check for collisions and determine the winner
                if animal.rect.colliderect(player1.rect):
                    if animal.animal_type == "grail":
                        animals.remove(animal)
                        player1.score +=1
                    else:
                        animals.remove(animal)
                        if player1.score > 0:
                            player1.score -= 1
                    break
                if animal.rect.colliderect(player2.rect):
                    if animal.animal_type == "grail":
                        animals.remove(animal)
                        player2.score +=1
                    else:
                        animals.remove(animal)
                        if player1.score > 0:
                            player1.score -= 1                      
                    break
            
            # Draw everything
            screen.blit(background_img, (0, 0))  # Draw the background image
            player1.draw()
            player2.draw()
            for animal in animals:
                animal.draw()
            display_scores(player1, player2)  # Display scores

            pygame.display.flip()

        if not game_started:
            if THEME_PLAYING == False:
                THEME_PLAYING == True
            screen.blit(loadscreen_img, (0,0))
            start_text = pygame.font.Font(None, GAME_OVER_FONT_SIZE).render("Press SPACE to Start", True, WHITE)
            text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 460))
            controls_text = pygame.font.Font(None, 25).render("Player 1 Control: A = Left, D = Right. Player 2 Control: LArrow = Left, RArrow = Right.",True, WHITE)
            points_text = pygame.font.Font(None,25).render("Holy Grail = +1 Point   Animal = -1 Point", True, WHITE)
            screen.blit(start_text, text_rect)
            screen.blit(controls_text, (50, 535))
            screen.blit(points_text, (250, 570))
            pygame.display.flip()

        if game_over:
            restart_text = f"Press 'R' to Restart or 'Q' to Quit"
            game_over_text = pygame.font.Font(None, GAME_OVER_FONT_SIZE).render(winner_text, True, BLACK)
            restart_message = pygame.font.Font(None, SCORE_FONT_SIZE).render(restart_text, True, (255, 255, 255),(0, 0, 0))
            # Draw a background rectangle for better readability
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))  # Add padding to the rectangle
            screen.blit(game_over_text, text_rect)
            screen.blit(restart_message, (225, 475 ))
            pygame.display.flip()

        clock.tick(FPS)

def playintro():
    screen.fill((0, 0, 0))
    pygame.display.flip()
    introVid=Video("Montypythonclip.mp4")
    introVid.set_size((800, 450))
    intro_text = pygame.font.Font(None, 30).render("Press SPACE to Skip", True, WHITE)
    intro_text_rect = intro_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
    while True:
        introVid.draw(screen, (0, 75))
        screen.blit(intro_text, intro_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    introVid.close()
                    pygame.mixer.music.play()
                    return
            if event.type == pygame.QUIT:
                sys.exit()
    
# Run the game
if __name__ == "__main__":
    game_loop()
