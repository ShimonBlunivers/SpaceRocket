import pygame
import random
import sys
from pygame import color

from pygame.locals import *

pygame.init()

pygame.display.set_caption('SpaceGame')

clock = pygame.time.Clock()

resolution = (567, 720)

screen = pygame.display.set_mode(resolution)

icona = pygame.image.load('files/raketa.png')
pygame.display.set_icon(icona)

planets = []

particles = []

celestialBodies = []

planetParticles = []

font = pygame.font.SysFont(None, 60)

statsFont = pygame.font.SysFont(None, 32)

instructionsFont = pygame.font.SysFont(None, 36)

def slowlyChangeColor(R,G,B, desiredR, desiredG, desiredB, step):
    colors = [R,G,B]
    desiredColors = [desiredR, desiredG, desiredB]
    changedR, changedG, changedB = R, G, B
    changedColors = [changedR, changedG, changedB]
    for i in range(0,3):
        if colors[i] == desiredColors[i]:
            changedColors[i] = desiredColors[i]
        if colors[i] > desiredColors[i]:
            if (colors[i] - step) < desiredColors[i]:
                changedColors[i] = desiredColors[i]
            else:
                changedColors[i] -= step
        if colors[i] < desiredColors[i]:
            if (colors[i] + step) > desiredColors[i]:
                changedColors[i] = desiredColors[i]
            else:
                changedColors[i] += step
    if R == desiredR and G == desiredG and B == desiredB:
        return True, changedColors[0],changedColors[1],changedColors[2]
    return False, changedColors[0],changedColors[1],changedColors[2]



class Planet:
    def __init__(self, name, color, gravitation, atmosphereColor, size):
        self.color = color
        self.usingColorR = color[0]
        self.usingColorG = color[1]
        self.usingColorB = color[2]
        self.getColor = color
        self.name = name
        self.position = [0, (resolution[1] - resolution[1]/3)]
        self.width = resolution[0]
        self.height = resolution[1]/2
        self.size = size
        self.gravitationForce = gravitation
        self.rect = pygame.Rect(self.position[0], self.position[1], self.height, self.width)
        self.rectHitbox = pygame.Rect(self.position[0], self.position[1] + self.height/4, resolution[0], self.height-self.height/4)
        self.active = False
        self.atmosphereColor = atmosphereColor
        self.atmosphereHeight = 7500
        self.landingHeight = False
        planets.append(self)

    def render(self):
        if self.active and Rocket1.interstellar == False:
            self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
            self.rectHitbox = pygame.Rect(self.position[0], self.position[1] + self.height/4, resolution[0], self.height-self.height/4)
            pygame.draw.rect(screen,[self.usingColorR,self.usingColorG,self.usingColorB] , self.rect)
            # pygame.draw.rect(screen, [255,0,0], self.rectHitbox, width=3)
        if self.landingHeight:
            self.position[1] = 800
            self.landingHeight = False

    def move(self):
        self.position[1] += Rocket1.speed

# Planety v pořadí

Earth = Planet('Earth',[0,128,0], 0.4, [96,239,249], 50)

Mars = Planet('Mars',[221,115,15], 0.3, [248,191,122], 225)

Jupiter = Planet('Jupiter',[250,235,215], 0.6, [250,240,230], 400)

Saturn = Planet('Saturn',[222,184,135], 0.5, [255,228,196], 360)

Uranus = Planet('Uranus',[0,128,255], 0.35, [59,255,242], 240)

Neptune = Planet('Neptune',[128,128,255], 0.5, [110,138,249], 180)

#

Mercury = Planet('Mercury',[245,245,245], 0.2 ,[240,248,255], 40)

Venus = Planet('Venus',[255,255,255], 0.375 ,[255,250,250], 160)

class Rocket:
    def __init__(self, image):
        if '.' in image:
            image = 'files/'+image
        self.originalImage = pygame.image.load(image)
        self.image = self.originalImage
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.originalPosition = [(resolution[0]/2-self.width/2), Earth.rectHitbox.top-self.height]
        self.position = self.originalPosition
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.speed = 0
        self.engineAcceleration = 1
        self.acceleration = self.engineAcceleration
        self.weight = 1
        self.altitude = 0
        self.thrust = False
        self.drag = 0
        self.speedSide = 1
        self.interstellar = False
        self.timer = 0
        self.timerLoop = 0
        self.planetNumber = 0
        self.earthMoon = False
        self.skyChangeFinished = False
        self.lineColor = [100,10,10]

    def render(self):
        if not self.interstellar:
            self.altitude = round(((planets[self.planetNumber].rectHitbox.top) - (self.position[1] + self.height))/100)
            pygame.draw.line(screen, [250,0,0], (resolution[0]-20,resolution[1]-10),(resolution[0]-20,10), width=3)
            try:
                endline = (resolution[1]-10) - (resolution[1])/(planets[self.planetNumber].atmosphereHeight/self.altitude)
            except:
                endline = resolution[1]-10
            if endline <= 10:
                endline = 10
            pygame.draw.line(screen, self.lineColor, (resolution[0]-20,(resolution[1]-10)),(resolution[0]-20,endline), width=6)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        screen.blit(self.image, (self.position[0], self.position[1]))
        # pygame.draw.rect(screen, [255, 0, 0], self.rect, width=1)

    def nextPlanet(self):
        if not self.interstellar:
            keys = pygame.key.get_pressed()
            text = instructionsFont.render(f'Hold W to leave {planets[Rocket1.planetNumber].name} atmosphere', True, [220,20,60])
            text2 = instructionsFont.render('and enter interstellar space', True, [220,20,60])
            if self.timer < 60 and self.timerLoop == 0:
                screen.blit(text, (80, resolution[1]/3))
                screen.blit(text2, (100, resolution[1]/3+40))
                self.timer += 1
            elif self.timer == 60 and self.timerLoop == 0:
                self.timerLoop = 1
                self.lineColor = [100,10,10]
            elif self.timer >= 0 and self.timerLoop == 1:
                self.timer -= 1
            else:
                self.timerLoop = 0
                self.lineColor = [200,100,100]
            if keys[pygame.K_w] and self.thrust:
                for particle in particles:
                    none,particle.colorR,particle.colorG,particle.colorB = slowlyChangeColor(particle.colorR,particle.colorG,particle.colorB,176,224,230,random.randint(20,40))
                self.position[0] = self.originalPosition[0] + random.randint(-1,1)
                self.interstellar,World.color[0],World.color[1],World.color[2] = slowlyChangeColor(World.color[0],World.color[1],World.color[2],24, 32, 48,1)
            if self.interstellar:
                self.timer = 0
                self.timerLoop = 0
                planets[Rocket1.planetNumber].active = False
                planets[Rocket1.planetNumber].landingHeight = True

    def inInterstellar(self):
        if self.interstellar:
            self.speed = 300
            keys = pygame.key.get_pressed()
            if self.timer < 1000 and self.timerLoop == 0:
                self.timer += 1
                if self.timer % 5 == 0:
                    starParticle()
            elif self.timer == 1000 and self.timerLoop == 0:
                planetParticle(planets[self.planetNumber].color)
                self.timerLoop = 1
            elif self.timer >= 0 and self.timerLoop == 1:
                self.timer -= 1
                if self.timer % 5 == 0:
                    starParticle()
            else:
                self.timerLoop = 0
            if planets[Rocket1.planetNumber].active == True:
                text  = instructionsFont.render(f'Press S to enter {planets[Rocket1.planetNumber].name} atmosphere', True, [220,20,60])
                screen.blit(text, (80, resolution[1]/3))
                if keys[K_s]:
                    self.interstellar = False
                
    def move(self):
        self.drag = (self.speed/15) - (self.altitude/50)

        if self.drag >= 0:
            self.acceleration = self.engineAcceleration - self.drag
        else:
            self.acceleration = self.engineAcceleration

        gravitation = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:

            for i in range(10):
                fireParticle()
            self.speed += self.acceleration
            self.thrust = True
        if not keys[pygame.K_SPACE]:
            self.thrust = False
        self.rect = self.rect.move(0, 0)
        # pygame.draw.rect(screen, [255,0,0], (self.position[0], self.position[1]-self.speed-1, self.width, self.height), width=1)
        planet = planets[Rocket1.planetNumber]
        if not pygame.Rect.colliderect(planet.rectHitbox, (self.position[0], self.position[1]+5, self.width, self.height)):
            if keys[pygame.K_a] and self.position[0]-self.speedSide>0:
                self.position[0] -= self.speedSide
            if keys[pygame.K_d] and self.position[0]+self.speedSide+self.width<resolution[0]:
                self.position[0] += self.speedSide
        elif self.interstellar:
            if keys[pygame.K_a] and self.position[0]-self.speedSide>0:
                self.position[0] -= self.speedSide
            if keys[pygame.K_d] and self.position[0]+self.speedSide+self.width<resolution[0]:
                self.position[0] += self.speedSide
        if not self.interstellar:
            if pygame.Rect.colliderect(planet.rectHitbox, (self.position[0], self.position[1], self.width, self.height)):
                if not self.thrust:
                    if self.speed > -15:
                       self.speed = 0
                    planet.position[1] = self.position[1] + planet.height/4 + 15
                gravitation = False
            if pygame.Rect.colliderect(planet.rectHitbox, (self.position[0], self.position[1], self.width, self.height+20)):
                if self.speed < -15:
                    World.death()
        # pygame.draw.rect(screen,[255,0,0], planet.rectHitbox, width= 1)
        # pygame.draw.rect(screen,[255, 255, 0], (self.position[0], self.position[1], self.width, self.height+20), width=1)
        planet.move()
        if not pygame.Rect.colliderect(planet.rectHitbox, (self.position[0], self.position[1], self.width, self.height)):
            gravitation = True
        if gravitation == True and self.interstellar == False:
            self.speed -= self.weight * planets[Rocket1.planetNumber].gravitationForce
        if self.altitude >= 1000 and not self.skyChangeFinished:
            self.skyChangeFinished,World.color[0],World.color[1],World.color[2] = slowlyChangeColor(World.color[0],World.color[1],World.color[2],0,76,153,1)
            if self.earthMoon == False:
                theMoon()
                self.earthMoon = True
        if self.altitude >= planets[self.planetNumber].atmosphereHeight: # Výška potřebná k přechodu do mezihvězdného prostoru.
            self.nextPlanet()
        if self.interstellar:
            self.inInterstellar()

Rocket1 = Rocket('raketa.png')

class World:
    def __init__(self):
        self.color = planets[Rocket1.planetNumber].atmosphereColor
        self.Game = True
        self.Death = False
        self.backgroundChanged = False

    def screenFill(self):
        if not Rocket1.interstellar and not self.backgroundChanged:
            self.backgroundChanged, World.color[0], World.color[1], World.color[2] = slowlyChangeColor(World.color[0],World.color[1],World.color[2],planets[Rocket1.planetNumber].atmosphereColor[0],planets[Rocket1.planetNumber].atmosphereColor[1],planets[Rocket1.planetNumber].atmosphereColor[2],1)
        if Rocket1.interstellar and self.backgroundChanged:
            self.backgroundChanged = False
        screen.fill((self.color))

    def renderStats(self):
        if Rocket1.interstellar:
            text = statsFont.render(('Altitude: Interstellar space'), True, [255,0,0])
        else:
            text = statsFont.render(('Altitude: '+(str(Rocket1.altitude)+'m')), True, [255,0,0])
        screen.blit(text, (10, 10))
        if Rocket1.interstellar:
            X = random.randint(0,23)
            if X == 1:
                text = statsFont.render(('VXlcxty: x̷͂'), True, [255,0,0])
            elif X == 2:
                text = statsFont.render(('VeXoXity: X̶̔͛'), True, [255,0,0])
            elif X == 3:
                text = statsFont.render(('V̷el̵oc̸i̵ty̶: X̵͛̐'), True, [255,0,0])
            elif X == 4:
                text = statsFont.render(('V*xociXx: X̷'), True, [255,0,0])
            elif X == 5:
                text = statsFont.render(('XXxociXx: x̵̊'), True, [255,0,0])
            elif X == 6:
                text = statsFont.render(('V*xxcitx: X̶'), True, [255,0,0])
            elif X == 7:
                text = statsFont.render(('VexociXx: x̵̊'), True, [255,0,0])
            elif X == 8:
                text = statsFont.render(('Error'), True, [255,0,0])
            elif X == 9:
                text = statsFont.render(('N*t available'), True, [255,0,0])
            elif X == 10:
                text = statsFont.render(('death'), True, [255,200,200])
            elif X == 11:
                text = statsFont.render(('system error'), True, [255,0,0])
            elif X == 12:
                text = statsFont.render(('your mom lmao'), True, [255,0,0])
            elif X == 13:
                text = statsFont.render(('ERror'), True, [255,0,0])
            elif X == 14:
                text = statsFont.render(('ErRor'), True, [255,0,0])
            elif X == 15:
                text = statsFont.render(('ErrOr'), True, [255,0,0])
            elif X == 16:
                text = statsFont.render(('ErroR'), True, [255,0,0])
            elif X == 17:
                text = statsFont.render(('ErrOR'), True, [255,0,0])
            elif X == 18:
                text = statsFont.render(('ErRoR'), True, [255,0,0])
            elif X == 19:
                text = statsFont.render(('ErROR'), True, [255,0,0])
            elif X == 20:
                text = statsFont.render(('ERRor'), True, [255,0,0])
            elif X == 21:
                text = statsFont.render(('ERROr'), True, [255,0,0])
            elif X == 22:
                text = statsFont.render(('ERROR'), True, [255,0,0])
            else:
                text = statsFont.render(('xelxxiXy: x'), True, [255,0,0])
        else:
            text = statsFont.render(('Velocity: '+(str(round(Rocket1.speed))+'m/s')), True, [255,0,0])
        screen.blit(text, (10, 40))


    def death(self):
        self.Death = True
        self.Game = False
        self.Earth = False
        text = font.render('destroyed', True, [255,0,0])
        pygame.draw.rect(screen, [0, 0, 0], (0,0,resolution[0],resolution[1]))
        screen.blit(text, (resolution[0]/2-110, resolution[1]/2-50))

World = World()

class fireParticle:
    def __init__(self):
        self.size = random.randint(50,100)/10
        self.x = Rocket1.position[0] + Rocket1.width/2
        self.y = Rocket1.position[1] + Rocket1.height - 20
        self.startx = self.x
        self.starty = self.y
        self.colorR = random.randint(0,100)
        self.colorG = 60
        self.colorB = random.randint(100,150)
        self.velocity_side = random.randint(-400,400)/100
        self.velocity_down = random.randint(10000,15000)/1000 + Rocket1.speed / 100
        self.ylimit = self.y + 80 - abs(self.velocity_side*self.velocity_side*4) + self.size + Rocket1.speed
        if Rocket1.interstellar:
            self.colorR = random.randint(25,30)
            self.colorG = random.randint(140,145)
            self.colorB = random.randint(250,255)
            self.ylimit = self.y + 80 - abs(self.velocity_side * self.velocity_side * 4) + self.size
        self.ysmoke = self.y + 100 - abs(self.velocity_side*self.velocity_side*2) + self.size - (random.randint(0,100)/10)
        self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
        particles.append(self)


    def update(self):
        # pygame.draw.rect(screen, [self.colorR, self.colorG, self.colorB], self.rect)
        pygame.draw.circle(screen, [self.colorR, self.colorG, self.colorB],[self.x,self.y], self.size)
        self.y += self.velocity_down
        self.x += self.velocity_side
        self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
        self.size -= 0.5
        if self.colorB - 35 >= 0:
            self.colorB -= 35
        else:
            self.colorB = 0
        if self.colorR + 35 <= 255:
            self.colorR = self.colorR + 35
        else:
            self.colorR = 255
        
        if self.y >= self.ysmoke:
            self.colorR = random.randint(180,255)
            self.colorG = self.colorR
            self.colorB = self.colorR
            self.size += 4
            self.velocity_side = self.velocity_side/1.5
            self.velocity_down += 4
        if self.y >= self.ylimit:
             particles.remove(self)
        

class starParticle:
    def __init__(self):
        self.size = random.randint(5,30)/10
        self.x = random.randint(0,resolution[0]*10000)/10000
        self.y = - self.size
        self.startx = self.x
        self.starty = self.y
        self.color = [random.randint(240,255),random.randint(240,255),random.randint(240,255)]
        self.firstVelocity = random.randint(0,300)/100
        celestialBodies.append(self)
        # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
    def update(self):
        if Rocket1.interstellar:
            self.velocity_down = self.firstVelocity + (Rocket1.speed/50)
            pygame.draw.circle(screen, self.color,[self.x,self.y], self.size)
            # pygame.draw.rect(screen, self.color, self.rect)
            self.y += self.velocity_down
            # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
        if self.y > resolution[1]:
            celestialBodies.remove(self)
        if not Rocket1.interstellar:
            delete,self.color[0],self.color[1],self.color[2]=slowlyChangeColor(self.color[0],self.color[1],self.color[2],World.color[0],World.color[1],World.color[2],10)
            if delete:
                celestialBodies.remove(self)


class planetParticle:
    def __init__(self, color):
        Rocket1.planetNumber += 1
        try:
            planets[Rocket1.planetNumber].active = True
        except:
            Rocket1.planetNumber = 0
            planets[Rocket1.planetNumber].active = True
        self.size = planets[Rocket1.planetNumber].size
        self.x = random.randint(self.size,(resolution[0]-self.size)*10)/10
        self.y = - self.size
        self.startx = self.x
        self.starty = self.y
        self.usedColor = planets[Rocket1.planetNumber].getColor
        self.Velocity = 1
        planetParticles.append(self)
        # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)

    def update(self):
        if planets[Rocket1.planetNumber].active == True and Rocket1.interstellar:
            pygame.draw.circle(screen, self.usedColor,[self.x,self.y], self.size)
            # pygame.draw.rect(screen, self.color, self.rect)
            self.y += self.Velocity
            # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
            if self.y > resolution[1] + self.size:
                celestialBodies.remove(self)
                planets[Rocket1.planetNumber].active = False
        if not Rocket1.interstellar:
            pygame.draw.circle(screen, self.usedColor,[self.x,self.y], self.size)
            self.size += self.Velocity
            self.y += self.Velocity/10
        if self.size >= resolution[1]:
            deletee,self.usedColor[0],self.usedColor[1],self.usedColor[2]=slowlyChangeColor(self.usedColor[0],self.usedColor[1],self.usedColor[2],World.color[0],World.color[1],World.color[2],10)
            if deletee:
                planetParticles.remove(self)

class theMoon:
    def __init__(self):
        self.size = 60
        self.x = resolution[0]/2
        self.y = - self.size
        self.startx = self.x
        self.starty = self.y
        self.color = [240,255,255]
        self.craterColor = [230,238,245]
        self.Velocity = 0.8
        self.VelocitySide = 0.6
        celestialBodies.append(self)
        # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)

    def update(self):
        pygame.draw.circle(screen, self.color,[self.x,self.y], self.size)
        pygame.draw.circle(screen, self.craterColor ,[self.x+20,self.y +20], 10)
        pygame.draw.circle(screen, self.craterColor,[self.x-15,self.y -10], 20)
        pygame.draw.circle(screen, self.craterColor,[self.x+26,self.y -24], 14)
        # pygame.draw.rect(screen, self.color, self.rect)
        self.y += self.Velocity
        self.x -= self.VelocitySide
        # self.rect = pygame.Rect(self.x,self.y, self.size,self.size)
        if self.y > resolution[1] + self.size:
            celestialBodies.remove(self)


planets[Rocket1.planetNumber].active = True


while World.Game:
    World.screenFill()
    delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            World.Game = False
            pygame.quit()
            sys.exit()

    for body in celestialBodies:
        body.update()
    for planet in planets:
        planet.render()
    for partic in planetParticles:
        partic.update()
    for partic in particles:
        partic.update()
        
    Rocket1.render()
    Rocket1.move()
    World.renderStats()
    pygame.display.update()

while World.Death:
    for event in pygame.event.get():
        if event.type == QUIT:
            death = False
            pygame.quit()
            sys.exit()
    World.death()
    pygame.display.update()