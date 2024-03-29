import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tileMap import *
sys.path.insert(0, r'/PuzzleData')
import PuzzleData.Comp0
import PuzzleData.Comp1
import PuzzleData.Comp2
import PuzzleData.Comp3
import PuzzleData.Comp4
import PuzzleData.Comp5

class ComputerUI(pg.sprite.Sprite):
	def __init__(self, game, oncomputer):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width,height))
		self.image.fill(black)
		self.rect = self.image.get_rect()

		for i in range(len(game.comps)):
			if oncomputer == game.comps[i]:
				self.computer_file = 'Comp{}'.format(i)
				print(self.computer_file)
				self.m = eval('PuzzleData.Comp{}'.format(i))
				print(self.m.CompName)
		self.RightBox = Rightpane(game, oncomputer, self.m)
		self.LeftBox = Leftpane(game, oncomputer, self.m)

class Rightpane(pg.sprite.Sprite):
	def __init__(self, game, oncomputer, CompModule):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.CompModule = CompModule
		self.game = game
		self.image = pg.Surface((int(width*2/3),height))
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.rect.topleft = (0,0)

		#Spawning SubSprites
		self.Monitor = Make_Rect(game, self.rect.width, (self.rect.height*4/5), self.rect.centerx, 0, pastelBlueGreen)
		self.HardDiskBay = Make_Rect(game, self.rect.width, (self.rect.height*1/5), self.rect.centerx, self.Monitor.rect.height, red)
		self.CompScreen = CompScreen(game, (self.rect.width - 4*tileSize), (self.Monitor.rect.height - 4*tileSize), self.rect.centerx, 2*tileSize, black, self.CompModule)

class Leftpane(pg.sprite.Sprite):
	def __init__(self, game, oncomputer, CompModule):
		#Initializing Computer Module
		self.CompModule = CompModule
		self.Buttons = []

		#Initializing Sprite
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((int(width/3),height))
		self.image.fill(pastelBlue)
		self.rect = self.image.get_rect()
		self.rect.topright = (width,0)
		self.Instruction_box = Make_Rect(game, (self.rect.width - 2*tileSize), (self.rect.width - 2*tileSize), self.rect.centerx, tileSize, white)

		#Spawning SubSprites
		for index,linetext in enumerate(self.CompModule.PuzzleLines):
			self.makeButtons(index,linetext)

	def makeButtons(self, index, linetext):
		self.Buttons.append(Make_Rect(self.game, self.rect.width*2/3, tileSize/2, self.rect.centerx, self.Instruction_box.rect.height + tileSize*(len(self.Buttons) + 1) + tileSize/2, black))
		Text_inSprite(self.Buttons[index].image, linetext, 20, white)

	def update(self):
		pass
		#print(self.game.mouse)
		'''clicked_sprites = [button for button in self.Buttons if button.rect.collidepoint(self.game.mouse)]
		for button in clicked_sprites:
			index = self.Buttons.find(button)
			self.game.CompScreen.print_codeline(index, self.CompModule.PuzzleLines[index])'''


class CompScreen(pg.sprite.Sprite):
	def __init__(self, game, width, height, x, y, color, CompModule):
		#Initialize List containing all sprites of code in Monitor
		self.codeLines = []
		print(self.codeLines)

		#Initialize Computer Screen Sprite
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.CompModule = CompModule
		self.game = game
		self.image = pg.Surface((width,height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)
		#Make_Rect(game, self.rect.width, self.rect.height/3, self.rect.centerx, self.rect.centery, red)
		for index,linetext in enumerate(self.CompModule.PuzzleLines):
			self.print_codeline(index,linetext)

	def print_codeline(self,index,linetext):
		self.codeLines.append(Make_Rect(self.game, self.rect.width, tileSize/2, self.rect.centerx, self.rect.y + tileSize/2*len(self.codeLines) + tileSize/2, black))
		Text_inSprite(self.codeLines[index].image, linetext, 20, green)
		#self.codeLines[len(self.codeLines) - 1]

	def pop_codeline(self,index,linetext):
		self.codeLines[len(self.codeLines) - 1].kill()



class Make_Rect(pg.sprite.Sprite):
	def __init__(self, game, width, height, x, y, color):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width,height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

	'''def AAfilledRoundedRect(surface,rect,color,radius=0.4):

	    """
	    AAfilledRoundedRect(surface,rect,color,radius=0.4)

	    surface : destination
	    rect    : rectangle
	    color   : rgb or rgba
	    radius  : 0 <= radius <= 1
	    """

	    rect         = Rect(rect)
	    color        = Color(*color)
	    alpha        = color.a
	    color.a      = 0
	    pos          = rect.topleft
	    rect.topleft = 0,0
	    rectangle    = Surface(rect.size,SRCALPHA)

	    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
	    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
	    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

	    radius              = rectangle.blit(circle,(0,0))
	    radius.bottomright  = rect.bottomright
	    rectangle.blit(circle,radius)
	    radius.topright     = rect.topright
	    rectangle.blit(circle,radius)
	    radius.bottomleft   = rect.bottomleft
	    rectangle.blit(circle,radius)

	    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
	    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

	    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
	    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

	    return surface.blit(rectangle,pos)'''


				
