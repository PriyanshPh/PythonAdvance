import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame  # for more information search on google 'pygame documentation'
from pygame.locals import *  # Basic pygame imports
# Global Variables for the game
FPS = 32
ScreenWidth = 289
ScreenHeight = 555
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
Ground = ScreenHeight*0.8
Game_Sprites = {}
Game_Sounds = {}
Player = 'Manager/sprites/bird.png'
BackGround = 'Manager/sprites/background.png'
Pipe = 'Manager/sprites/pipe.png'


def WelcomeScreen():
    playerX = int(ScreenWidth/5)
    playerY = int((ScreenHeight - Game_Sprites['bird'].get_height())/2)
    messageX = int((ScreenWidth - Game_Sprites['message'].get_width())/2)
    messageY = int(ScreenHeight*0.13)
    baseX = 0
    while True:
        for event in pygame.event.get():
            # if user click on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                Screen.blit(Game_Sprites['background'], (0, 0))
                Screen.blit(Game_Sprites['bird'], (playerX, playerY))
                Screen.blit(Game_Sprites['message'], (messageX, messageY))
                Screen.blit(Game_Sprites['base'], (baseX, Ground))
                pygame.display.update()
                FPS_Clock.tick(FPS)


def MainGame():
    score = 0
    PlayerX = int(ScreenWidth/5)
    PlayerY = int(ScreenWidth/2)
    BaseX = 0
    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # my List of upper pipes
    upperPipes = [
        {'x': ScreenWidth+200, 'y': newPipe1[0]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y': newPipe2[0]['y']}
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': ScreenWidth+200, 'y': newPipe1[1]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y': newPipe2[1]['y']}
    ]
    pipeVelocityX = -4
    playerVelocityY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccelerationY = 1
    playerFlapAccV = -8  # Velocity while Flapping
    playerFlapped = False
    while True:
        for event in pygame.event.get():
            # if user click on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if PlayerY > 0:
                    playerVelocityY = playerFlapAccV
                    playerFlapped = True
                    Game_Sounds['wing'].play()
        # This function will return true if the player is crashed
        crashTest = isCollide(PlayerX, PlayerY, upperPipes, lowerPipes)
        if crashTest:
            return
        playerMidPosition = PlayerX+Game_Sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPosition = pipe['x']+Game_Sprites['pipe'][0].get_width()/2
            if pipeMidPosition <= playerMidPosition < pipeMidPosition+4:
                score += 1
                print(f"Your score is {score}")
                Game_Sounds['point'].play()
        if playerVelocityY < playerMaxVelY and not playerFlapped:
            playerVelocityY += playerAccelerationY
        if playerFlapped:
            playerFlapped = False
        playerHeight = Game_Sprites['player'].get_height()
        PlayerY = PlayerY + min(playerVelocityY, Ground-PlayerY-playerHeight)
        # Moves pipes to left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelocityX
            lowerPipe['x'] += pipeVelocityX
        # Add a new pipe when the first is about to go to the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        # if the pipes are out of the screen then remove it
        if upperPipes[0]['x'] < -Game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        # Lets blit our sprites now
        Screen.blit(Game_Sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screen.blit(Game_Sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            Screen.blit(Game_Sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        Screen.blit(Game_Sprites['base'], (BaseX, Ground))
        Screen.blit(Game_Sprites['player'], (PlayerX, PlayerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Game_Sprites['numbers'][digit].get_width()
        Xoffset = (ScreenWidth - width)/2
        for digit in myDigits:
            Screen.blit(Game_Sprites['numbers'][digit], (Xoffset, ScreenHeight*0.12))
            Xoffset += Game_Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPS_Clock.tick(FPS)


def isCollide(PlayerX, PlayerY, upperPipes, lowerPipes):
    if PlayerY> Ground - 25 or PlayerY<0:
        Game_Sounds['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = Game_Sprites['pipe'][0].get_height()
        if (PlayerY < pipeHeight + pipe['y'] and abs(PlayerX - pipe['x']) < Game_Sprites['pipe'][0].get_width()):
            Game_Sounds['hit'].play()
            return True
    for pipe in lowerPipes:
        if (PlayerY+Game_Sprites['player'].get_height()>pipe['y'])and abs(PlayerX-pipe['x'])<Game_Sprites['pipe'][0].get_width():
            Game_Sounds['hit'].play()
            return True
    return False

def getRandomPipe():
    # Generate opposite positions of two pipes for blitting on the screen
    pipeHeight = Game_Sprites['pipe'][0].get_height()
    offset = ScreenHeight/3
    y2 = offset + random.randrange(0, int(ScreenHeight-Game_Sprites['base'].get_height()-1.2*offset))
    pipeX = ScreenWidth+10
    y1 = pipeHeight-y2+offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipe
        {'x': pipeX, 'y': y2}  # Lower pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()  # init helps to initialize all pygame's modules
    FPS_Clock = pygame.time.Clock()
    pygame.display.set_caption('Bird Game for you')
    Game_Sprites['numbers'] = (  # this is a tuple
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )
    Game_Sprites['message'] = pygame.image.load(
        'sprites/message.png').convert_alpha()
    Game_Sprites['base'] = pygame.image.load(
        'sprites/base.png').convert_alpha()
    Game_Sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load('sprites/pipe.png').convert_alpha(), 180),
        pygame.image.load('sprites/pipe.png').convert_alpha()
    )
    # Game Sounds:->
    Game_Sounds['die'] = pygame.mixer.Sound('audio/die.wav')
    Game_Sounds['hit'] = pygame.mixer.Sound('audio/hit.wav')
    Game_Sounds['point'] = pygame.mixer.Sound('audio/point.wav')
    Game_Sounds['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    Game_Sounds['wing'] = pygame.mixer.Sound('audio/wing.wav')
    Game_Sprites['background'] = pygame.image.load('sprites/background.png').convert()
    Game_Sprites['bird'] = pygame.image.load('sprites/bird.png').convert_alpha()
    while True:
        WelcomeScreen()
        MainGame()
