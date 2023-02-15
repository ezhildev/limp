from config import *
from lib.funcs import *
from lib.ui import Text
from entities import *

class Level:
	def __init__(self, level_file, player, title=''):
		self.is_complete = False
		self.level_title = Text(title, FONT_S, position=(WINDOW_CENTER[0], 32))
		self.level_file = level_file
		self.player = player
		pass

	def load(self):
		self.objects = {'platform':[], 'obstacle':[], 'block':[]}
		self.blocks = pygame.sprite.Group()
		self.level_map = load_map(self.level_file)
		for obj in self.level_map.objects:
			if obj.name == 'start':
				self.player.load(obj.x, obj.y, obj.jump_count)

			elif obj.name == 'end':
				self.end_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

			elif obj.name == 'block':
				block = Block(pygame.transform.scale(obj.image, (32, 32)), pygame.Rect(obj.x, obj.y, obj.width, obj.height))
				self.objects['block'].append(block)
				self.blocks.add(block)

			else:
				self.objects[obj.name].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

		for index in self.level_map.visible_tile_layers:
			layer:pytmx.TiledTileLayer = self.level_map.layers[index]
			for x, y, gid in layer.iter_data():
				if self.level_map.images[gid] != None:
					self.level_map.images[gid] = pygame.transform.scale(self.level_map.images[gid], (32, 32))

	def update(self):
		if self.end_rect.colliderect(self.player.body):
			self.is_complete = True
		self.blocks.update(self.objects)
		self.player.update(self.objects)

	def draw(self, window):
		for index in self.level_map.visible_tile_layers:
			layer:pytmx.TiledTileLayer = self.level_map.layers[index]
			for x, y, img in layer.tiles():
				window.blit(img, (x * self.level_map.tilewidth, y * self.level_map.tileheight))

		self.blocks.draw(window)
		self.player.draw(window)

		# for rl in self.objects.values():
		# 	for r in rl:
		# 		if isinstance(r, pygame.Rect):pygame.draw.rect(window, 'white', r, 1)
		# 		else: pygame.draw.rect(window, 'white', r.rect, 1)
				
		window.blit(self.level_title.image, self.level_title.rect.topleft)

	def dispose(self):
		del self.level_map
		del self.objects