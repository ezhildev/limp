from config import *
from lib.ui import Text
from lib.animation import AnimatedSprite

class Player(AnimatedSprite):
	def __init__(self):
		super().__init__()
		self.load_frames('idle', './src/graphics/player/idle/', .1, 2)
		self.load_frames('run', './src/graphics/player/run/', .15, 2)
		self.load_frames('jump', './src/graphics/player/jump/', .2, 2, False)
		self.load_frames('fall', './src/graphics/player/fall/', .2, 2, False)
		self.load_frames('dead', './src/graphics/player/dead/', .2, 2, False)
		self.set_anim('idle')
		self.sound = {
			'jump': pygame.mixer.Sound('./src/audios/jump.ogg'),
			'dead': pygame.mixer.Sound('./src/audios/dead.ogg')
		}
		self.sound['dead'].set_volume(.2)
		self.body = pygame.Rect(0, 0, 20, GRID_SIZE)
		self.direction = pygame.Vector2(0, 1)
		self.acceleration = pygame.Vector2(1, 1)
		self.velocity = pygame.Vector2(0, 0)
		self.gravity = 8
		self.jump_speed = -9
		self.max_speed = 5
		self.load(0, 0)

	def load(self, x, y, jump_count = 0):
		self.body.x, self.body.y = x, y
		self.is_jump = False
		self.on_ground = False
		self.jump_count = jump_count
		self.is_alive = True
		self.jump_count_img = Text(str(self.jump_count), FONT_S)

	def animation(self):
		if self.velocity.x > 0:
			self.set_direction(False, False)
		elif self.velocity.x < 0:
			self.set_direction(True, False)
		if self.is_alive:
			if self.velocity.y == 0:
				if self.velocity.x == 0:
					self.set_anim('idle')
				else:
					self.set_anim('run')
			elif self.velocity.y < 0:
				self.set_anim('jump')
			elif self.velocity.y > 0:
				self.set_anim('fall')
		else:
			self.set_anim('dead')
		self.play_anim()

	def horizontal_move(self):
		if self.is_alive: 
			self.direction.x = INPUT.right.kpress - INPUT.left.kpress
			self.velocity.x = lerp(self.velocity.x, self.max_speed * self.direction.x, self.acceleration.x)
			self.body.x += int(self.velocity.x)

	def vertical_move(self):
		if self.is_alive and INPUT.up.kdown and self.on_ground and self.jump_count > 0:
			self.jump_count -= 1
			self.is_jump = True
			self.on_ground = False
			self.velocity.y = self.jump_speed
			self.jump_count_img = Text(str(self.jump_count), FONT_S)
			self.sound['jump'].play()

		if self.is_jump:
			self.velocity.y = lerp(self.velocity.y, 0, .5)
			self.direction.y = -1
			if self.velocity.y == 0:
				self.is_jump = False
		else:
			self.velocity.y = lerp(self.velocity.y, self.gravity, self.acceleration.y)
			self.direction.y = 1

		self.body.y += int(self.velocity.y)

	def obstacle_hit(self, objects):
		if not self.is_alive or objects.get('obstacle') == None: return
		for rect in objects['obstacle']:
			if self.body.colliderect(rect):
				self.is_alive = False
				self.sound['dead'].play()
				break

	def vertical_collision(self, objects):
		for _name, _list in objects.items():
			if _name in ('platform', 'block'):
				for rect in _list:
					if _name == 'block': rect = rect.rect
					if self.body.colliderect(rect):
						if self.velocity.y > 0:
							self.body.bottom = rect.top
							self.velocity.y = 0
							self.direction.y = 0
							self.on_ground = True
						elif self.velocity.y < 0:
							self.body.top = rect.bottom
							self.velocity.y = 0
							self.direction.y = 1
							self.is_jump = False

	def horizontal_collision(self, objects):
		for _name, _list in objects.items():
			if _name in ('platform', 'block'):
				for obj in _list:
					if _name == 'block': rect = obj.rect
					else: rect = obj
					if self.body.colliderect(rect):
						if self.velocity.x > 0:
							if _name == 'block': obj.move(objects, 1)
							self.body.right = rect.left
							self.velocity.x =  0
						elif self.velocity.x < 0:
							if _name == 'block': obj.move(objects, -1)
							self.body.left = rect.right
							self.velocity.x =  0

	def update(self, objects):
		self.obstacle_hit(objects)
		self.vertical_move()
		self.vertical_collision(objects)
		self.horizontal_move()
		self.horizontal_collision(objects)
		self.animation()

	def draw(self, window):
		window.blit(self.jump_count_img.image, (
			self.jump_count_img.rect.centerx + self.body.x + 10, 
			self.jump_count_img.rect.y + self.body.top - 20
		))
		window.blit(self.image, (self.body.x - 39, self.body.y - self.body.height))
		# pygame.draw.rect(window, 'green', self.body, 1)


class Block(pygame.sprite.Sprite):
	def __init__(self, img, rect):
		super().__init__()
		self.image = img
		self.rect = rect
		self.gravity = 10
		self.speed = 1
		self.velocity = pygame.math.Vector2()
		self.direction_x = 0
		self.top_block = None
		
	def horizontal_collision(self, objects):
		for _name, _list in objects.items():
			if _name in ('platform', 'block'):
				for rect in _list:
					if rect == self: continue
					if _name == 'block': rect = rect.rect
					if self.rect.colliderect(rect):
						if self.direction_x > 0:
							self.rect.right = rect.left
							self.velocity.x =  0
							self.direction_x = 0
						elif self.direction_x < 0:
							self.rect.left = rect.right
							self.velocity.x =  0
							self.direction_x = 0

	def vertical_collision(self, objects):
		if self.top_block != None and not self.rect.colliderect(self.top_block.rect) and self.top_block.rect.bottom == self.rect.top:
			self.top_block = None

		for _name, _list in objects.items():
			if _name in ('platform', 'block'):
				for obj in _list:
					if _name == 'block':
						if obj == self: continue
						rect = obj.rect
					else: rect = obj
					if self.rect.colliderect(rect):
						if self.velocity.y > 0:
							self.rect.bottom = rect.top
							self.on_ground = True
							self.velocity.y = 0
							if _name == 'block' and obj.top_block == None: 
								obj.top_block = self
								self.rect.bottom = obj.rect.top

	def horizontal_move(self, objects, direction):
		self.direction_x = direction
		self.velocity.x = self.speed * direction
		self.rect.x += int(self.velocity.x)
		if self.direction_x != 0:
			if self.top_block != None:
				self.top_block.move(objects, direction)
		self.horizontal_collision(objects)

	def vertical_move(self, objects):
		self.velocity.y = lerp(self.velocity.y, self.gravity , 4)
		self.rect.y += int(self.velocity.y)
		self.vertical_collision(objects)

	def move(self, objects, direction=0):
		self.vertical_move(objects)
		self.horizontal_move(objects, direction)


	def update(self, objects:dict):
		self.move(objects)