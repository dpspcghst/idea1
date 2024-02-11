import pygame

class InteractiveElement(pygame.sprite.Sprite):

    def __init__(self, position, size, player):

        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = position)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4

        self.player = player

    def move(self, direction):

        print(direction)
        if direction == False:

            self.direction.x = -1
            self.rect.x += self.direction.x

        elif direction == True:
    
            self.direction.x = 1
            self.rect.x += self.direction.x

        else:

            self.direction.x = 0
            self.rect.x += self.direction.x
    
    def interactions(self):

        player = self.player.sprite
    
        if self.rect.colliderect(player.rect):
            
            keys = pygame.key.get_pressed()
    
            if keys[pygame.K_LEFT] and keys[pygame.K_LCTRL]:
                
                self.direction.x = -1  # Move left
            
            elif keys[pygame.K_RIGHT] and keys[pygame.K_LCTRL]:
                
                self.direction.x = 1  # Move right

            else:

                self.velocity_x = 0
    
    def collisions(self):

        self.rect.x += self.direction.x * self.speed
    
    def update(self, x_shift, y_shift):

        self.rect.x += x_shift
        self.rect.y += y_shift
        self.collisions()
        self.interactions()
