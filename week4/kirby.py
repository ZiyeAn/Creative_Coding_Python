import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kirby Fruit Catch")

WHITE = (255, 255, 255)
FPS = 60
VEL = 5
Fruit_vel = 5
Bullet_vel = 7
Kirby_WIDTH, Kirby_HEIGHT = 100, 100
COLLECT_RANGE = 50

#assets
#sounds
poyo_sound = pygame.mixer.Sound(os.path.join('Assets', 'poyo.mp3'))

# bg
background_img = pygame.image.load(os.path.join('Assets', 'kirby_bg.jpg'))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# food
fruit_images = {
    "1": pygame.transform.scale(pygame.image.load(os.path.join('Assets', '1.png')), (50, 50)),
    "2": pygame.transform.scale(pygame.image.load(os.path.join('Assets', '2.png')), (50, 50)),
    "3": pygame.transform.scale(pygame.image.load(os.path.join('Assets', '3.png')), (50, 50)),
    "4": pygame.transform.scale(pygame.image.load(os.path.join('Assets', '4.png')), (50, 50)),
    "5": pygame.transform.scale(pygame.image.load(os.path.join('Assets', '5.png')), (50, 50))
}
fruit_names = list(fruit_images.keys())

# target
target_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'target.png')), (50, 50))
#kirby
KirbyIMG = pygame.image.load(os.path.join('Assets', 'kirby.png'))
KirbyIMG_alt = pygame.image.load(os.path.join('Assets', 'kirby_mouse_open.png'))
KirbyIMG_alt2 = pygame.image.load(os.path.join('Assets', 'kirby-puffy.png'))
Kirby = pygame.transform.scale(KirbyIMG, (Kirby_WIDTH, Kirby_HEIGHT))
Kirby_ALT = pygame.transform.scale(KirbyIMG_alt, (Kirby_WIDTH, Kirby_HEIGHT))
Kirby_ALT2 = pygame.transform.scale(KirbyIMG_alt2, (Kirby_WIDTH, Kirby_HEIGHT))
#define classes
class Fruit:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(50, HEIGHT - 50)
        self.fruit_type = random.choice(fruit_names)
        self.image = fruit_images[self.fruit_type]
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self):
        self.rect.x -= Fruit_vel

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def is_off_screen(self):
        return self.rect.x < -40

class Target:
    def __init__(self):
        self.x = random.randint(400, WIDTH - 100)
        self.y = random.randint(50, HEIGHT - 50)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def draw(self, window):
        window.blit(target_img, (self.rect.x, self.rect.y))

class Bullet:
    def __init__(self, x, y, fruit_type):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = fruit_images[fruit_type]

    def update(self):
        self.rect.x += Bullet_vel

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

def draw_window(kirby, current_kirby_img, fruit_obj, target, bullets):
    WIN.blit(background_img, (0, 0))
    WIN.blit(current_kirby_img, (kirby.x, kirby.y))
    
    if fruit_obj:
        fruit_obj.draw(WIN)
    
    if target:
        target.draw(WIN)
    
    for bullet in bullets:
        bullet.draw(WIN)
    
    pygame.display.update()

def main():
    kirby = pygame.Rect(100, 300, Kirby_WIDTH, Kirby_HEIGHT)
    current_kirby_img = Kirby
    fruit_obj = None
    collected_fruit = None
    target = None
    bullets = []
    space_pressed = False
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        #quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #collect fruit + add bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    if collected_fruit:
                        bullets.append(Bullet(kirby.x + kirby.width, kirby.y + kirby.height // 2, collected_fruit))
                        collected_fruit = None
                        current_kirby_img = Kirby
                        poyo_sound.play()  
                    else:
                        current_kirby_img = Kirby_ALT  
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    if not collected_fruit:
                        current_kirby_img = Kirby  
        # collect fruit logic (make fruit invisible and add a random target)
        if space_pressed and not collected_fruit and fruit_obj and abs(kirby.x + kirby.width - fruit_obj.rect.x) <= COLLECT_RANGE and abs(kirby.y - fruit_obj.rect.y) <= COLLECT_RANGE:
            collected_fruit = fruit_obj.fruit_type
            fruit_obj = None
            target = Target()
            current_kirby_img = Kirby_ALT2 
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and kirby.x - VEL > 0:
            kirby.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and kirby.x + VEL + kirby.width < WIDTH:
            kirby.x += VEL
        if keys_pressed[pygame.K_UP] and kirby.y - VEL > 0:
            kirby.y -= VEL
        if keys_pressed[pygame.K_DOWN] and kirby.y + VEL + kirby.height < HEIGHT:
            kirby.y += VEL
        #generate fruit when there is none
        if not fruit_obj:
            fruit_obj = Fruit()
        elif fruit_obj.is_off_screen():
            fruit_obj = Fruit()
        else:
            fruit_obj.update()
        #bullet target collider
        for bullet in bullets[:]:
            bullet.update()
            if target and bullet.rect.colliderect(target.rect):
                bullets.remove(bullet)
                target = None  # Remove target if hit
            elif bullet.rect.x > WIDTH:
                bullets.remove(bullet)
        
        draw_window(kirby, current_kirby_img, fruit_obj, target, bullets)
    
    pygame.quit()

if __name__ == "__main__": 
    main()
