#Jump Platform game
import pygame as pg
import random
import pyglet as pyg
import os
from settings import *
from sprites import *

class Game:
	def __init__(self):
		#initialize game window
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True

	def new(self):
		#start a new game
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player = Player(self)
		self.all_sprites.add(self.player)
		for plat in PLATFORM_LIST:
			p = Platform(*plat)
			self.all_sprites.add(p)
			self.platforms.add(p)
		self.run()

	def run(self):
		#game Loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		#Game Loop Update
		self.all_sprites.update()
		#check if player hits a platform - only if falling
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				self.player.pos.y = hits[0].rect.top
				self.player.vel.y = 0

		#if player reacher top 1/4 of screen
		if self.player.rect.top <= HEIGHT / 4:
			self.player.pos.y += abs(self.player.vel.y)
			for plat in self.platforms:
				plat.rect.y += abs(self.player.vel.y)
				if plat.rect.top >= HEIGHT:
					plat.kill()

		#Die
		if self.player.rect.bottom > HEIGHT:
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vel.y, 10)
				if sprite.rect.bottom < 0:
					sprite.kill()
		if len(self.platforms) == 0:
			self.playing = False
		#spawning new platforms
		while len(self.platforms) < 6:
			width = random.randrange(50,100)
			p = Platform(random.randrange(0, WIDTH-width), random.randrange(-75,-30),width,20)
			self.platforms.add(p)
			self.all_sprites.add(p)

	def events(self):
		# Game Loop Events
		for event in pg.event.get(): 
			#Terminate the program
			if event.type == pg.QUIT: 
				self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()

	def draw(self):
		#Game Loop draw
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		pg.display.flip() #Flips newly rendered frame to the viewer

	def show_start_screen(self):
		# Game splash/start screen
		pass

	def show_go_screen(self):
		#game over/continue
		pass

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()