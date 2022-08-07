import sys
import pygame
pygame.init()
pygame.font.init()

size = width, height = 1000, 700
ballspeed = [5, 5]
player_speed = 8
black = 0, 0, 0
max_speed = 5
game_over = False
hit = False
player_pos_x = width/2
ballrect = [width/2, height/2]
score = 0
win=False
menu =True
a_y=8
a_x=8
gamemode_common=False
gamemode_hard=False
playerhit=False


class WALL():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

    def hit(self, ballrect):
        if self.rect.colliderect(ballrect):
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


walls = []

def generate_walls():
    wall_count = 48
    wall_colums = 6
    wall_rows = 0

    for i in range(wall_count):
        if(i % wall_colums == 0):
            wall_rows += 35
        walls.append(
            WALL(
                (i % wall_colums)*width/wall_colums + width/wall_colums/2 - 45,
                wall_rows, 90, 15
            ))

generate_walls()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

ball = pygame.image.load("pong.png")
ball = pygame.transform.scale(ball, (30, 30))
player_box = pygame.image.load("box.png")
player_box = pygame.transform.scale(player_box, (90, 15))
hitbox = pygame.transform.scale(player_box, (60, 15))

ballrect = ball.get_rect()
ballrect.x = width/2
ballrect.y = height-100

background = pygame.image.load("spacebg.png")


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # ตั้งค่าปุ่มกด
    pressed = pygame.key.get_pressed()
    #โหมดปกติ
    if pressed[pygame.K_o] :
        gamemode_common=True
        menu=False
    elif pressed[pygame.K_h] :
        gamemode_hard=True
        menu=False
    if gamemode_common ==True or gamemode_hard == True :

        playerbox = (player_pos_x, height-55)

        if pressed[pygame.K_r] and game_over == True :
            player_pos_x = (width/2)
            ballrect.x = width/2
            ballrect.y = height-100
            ballspeed = [5, 5]
            score = 0
            generate_walls()
            game_over = False

        if pressed[pygame.K_a]:
            player_pos_x -= player_speed
        if pressed[pygame.K_d]:
            player_pos_x += player_speed
        # ตั้งค่าให้บอลสามารถสะท้อนกับขอบจอได้
        ballrect = ballrect.move(ballspeed)
        if ballrect.left < 0 or ballrect.right > width:
            ballspeed[0] = -ballspeed[0]
        if ballrect.top < 0:
            ballspeed[1] = -ballspeed[1]
        
            
        if ballrect.bottom >= height-55 and (ballrect.left < playerbox[0]+90 and ballrect.right > playerbox[0]):
            ballspeed[1] = -ballspeed[1]
            if gamemode_hard==True:
                #แกนY
                if ballspeed[1]<0:
                    ballspeed[1]=-5
                elif ballspeed[1]>0:
                    ballspeed[1]=-5
                #แกนX
                if ballspeed[0]<0:
                    ballspeed[0]=-5
                elif ballspeed[0]>0:
                    ballspeed[0]=5

                
                
                
        # แพ้(บอลตกพื้น)
        if ballrect.bottom > height:
            ballspeed[1] = 0
            ballspeed[0] = 0
            game_over = True

        screen.fill(black)
        screen.blit(background,(0,0))
        screen.blit(ball, ballrect)
        screen.blit(player_box, (player_pos_x, height-55))
        #screen.blit(hitbox, (0,0))

        for wall in walls:
            if wall.hit(ballrect):
                walls.remove(wall)
                hit=True
                
        if hit==True:
            score+=1
            ballspeed[1] = -ballspeed[1]
            if gamemode_hard==True and ballspeed[0]>-3 and ballspeed[0]<13:
                if ballspeed[0] <0 :
                    ballspeed[0]+=a_x
                elif  ballspeed[0] >0:
                    ballspeed[0]+=a_x
            if gamemode_hard==True and ballspeed[1]>-3 and ballspeed[1]<13:
                if ballspeed[1] <0 :
                        ballspeed[1]-=a_y
                elif  ballspeed[1] >0:
                        ballspeed[1]+=a_y
            hit=False
        if score >= 48:
            ballspeed[1] = 0
            ballspeed[0] = 0
            win=True


        for wall in walls:
            wall.draw()

        myfont = pygame.font.SysFont('Calibri', 30)
        if(game_over):
            GameOverText = myfont.render('Game Over, press R to restart', False, (255, 255, 255))
            screen.blit(
                GameOverText, ((width-GameOverText.get_width())/2, height/2))
        scoreText = myfont.render(f'Score: {score}', False, (255, 255, 255))
        screen.blit(scoreText, (0, 0))
        myfont = pygame.font.SysFont('Calibri', 50)
        if(win):
            wintext=myfont.render('you are winner!', False, (255, 255, 255))
            screen.blit(
                wintext, ((width-wintext.get_width())/2, height/2))
    
    if pressed[pygame.K_h] :
        gamemode_hard=True
        menu=False

    #กดpเพื่อกลับไปหน้าเมนู
    if pressed[pygame.K_p] :
        ballspeed = [5, 5]
        player_speed = 8
        a = 0
        black = 0, 0, 0
        max_speed = 5
        game_over = False
        hitboxs = []
        player_pos_x = width/2
        ballrect = [width/2, height/2]
        score = 0
        win=False
        gamemode_common=False
        gamemode_hard=False
        walls = []

        generate_walls()

        ballrect = ball.get_rect()
        ballrect.x = width/2
        ballrect.y = height-100
    
        menu=True 
    
    if menu == True:
        screen.blit(background,(0,0))
        myfont = pygame.font.SysFont('Calibri', 30)
        menutext = myfont.render('press O to play common mode', False, (255, 255, 255))
        screen.blit(menutext, ((width-menutext.get_width())/2, height/2)) 
        menu=myfont.render('press H to play common mode', False, (255, 255, 255))
        screen.blit(menu, ((width-menutext.get_width())/2, height/2+40)) 
    
    pygame.display.flip()
