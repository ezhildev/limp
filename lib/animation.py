import pygame, os
from lib.funcs import *

class AnimatedSprite(pygame.sprite.Sprite):
	'''AnimatedSprite class used for sprite animation.'''
	def __init__(self) -> None:
		super().__init__()
		self.__animations = {}
		self.__current_animation = None
		self.__index = 0
		self.__horizontal_flip = False
		self.__vertical_flip = False

	def load_frames(self, anim_name, file_path, anim_time, scale = 1, repeat = True) -> None:
		'''This method used to load all sprite images in given file path.'''
		frames = []
		for frame in os.listdir(file_path):
			image = pygame.image.load(file_path + frame)
			size = image.get_rect().size
			image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
			frames.append(image)
		self.__animations[anim_name] = {'frames': frames, 'time': anim_time, 'repeat': repeat}

	def load_spritesheet(self, anim_name, file, size, anim_time = 0.0, scale = 1.0, repeat = True) -> None:
		'''This method used to load spritesheet. All sprite images are extracted from spritesheet and saved in list.'''
		sheet = pygame.image.load(file)
		frames = []
		rows, columns = sheet.get_rect().height // size[1], sheet.get_rect().width // size[0]
		for y in range(rows):
			for x in range(columns):
				image = image_at(sheet, (x * size[0], y * size[1], size[0], size[1]))
				image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
				frames.append(image)
		self.__animations[anim_name] = {'frames': frames, 'time': anim_time, 'repeat': repeat}

	def set_anim(self, anim_name) -> None:
		'''This used to set current animation state.'''
		if self.__current_animation != anim_name:
			self.__current_animation = anim_name
			self.play_anim()
			self.__index = 0

	def set_anim_index(self, index = 0):
		'''This method set the current index of animation.'''
		self.__index = index

	def add_frame(self, anim_name, frame) -> None:
		'''This method added the frame based on given animation name'''
		frame = pygame.transform.scale(frame, self.__animations[anim_name]['frames'][0].get_rect().size)
		self.__animations[anim_name]['frames'].append(frame)

	def set_direction(self, horizontal_flip, vertical_flip) -> None:
		'''method used to flip the image based on given boolean value.'''
		self.__horizontal_flip = horizontal_flip 
		self.__vertical_flip = vertical_flip

	def get_anim_length(self, anim_name) -> int:
		'''This will return a length of given animation'''
		return len(self.__animations[anim_name]['frames'])

	def get_anim_index(self) -> int:
		'''This will return a current animation\'s index value'''
		return int(self.__index)

	def play_anim(self) -> None:
		'''This method used for assigning currect frame to image variable'''
		no_of_frames = len(self.__animations[self.__current_animation]['frames'])
		if int(self.__index) >= no_of_frames:
			if self.__animations[self.__current_animation]['repeat']:
				self.__index = 0
			else: self.__index = no_of_frames - 1
		self.image = self.__animations[self.__current_animation]['frames'][int(self.__index)]
		self.image = pygame.transform.flip(self.image, self.__horizontal_flip, self.__vertical_flip)
		self.__index += self.__animations[self.__current_animation]['time']

	def play_anim_reverse(self)  -> None:
		'''This method used for assigning currect frame to image variable in reverse order'''
		no_of_frames = len(self.__animations[self.__current_animation]['frames'])
		if int(self.__index) >= no_of_frames:
			if self.__animations[self.__current_animation]['repeat']:
				self.__index = 0
			else: self.__index = no_of_frames - 1
		self.image = self.__animations[self.__current_animation]['frames'][-int(self.__index+1)]
		self.image = pygame.transform.flip(self.image, self.__horizontal_flip, self.__vertical_flip)
		self.__index += self.__animations[self.__current_animation]['time']
