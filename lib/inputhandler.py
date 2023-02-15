from config import *

class InputKey:
	def __init__(self):
		self.kdown = False
		self.kpress = False
		self.kup = False
		self.map = []


class InputHandler:
	def __init__(self):
		self.left = InputKey()
		self.right = InputKey()
		self.up = InputKey()
		self.down = InputKey()
		self.enter = InputKey()
		self.exit = InputKey()
		self.restart = InputKey()

		self.__inputkeys = [self.left, self.right, self.up, self.down, self.enter, self.exit, self.restart]

	def reset(self):
		for INPUTkey in self.__inputkeys:
			INPUTkey.kdown = False
			INPUTkey.kup = False

	def process_input(self, event):
		for INPUTkey in self.__inputkeys:
			if event.type == pygame.KEYDOWN:
				INPUTkey.kdown = event.key in INPUTkey.map
				if INPUTkey.kdown: INPUTkey.kpress = True
			if event.type == pygame.KEYUP:
				INPUTkey.kup = event.key in INPUTkey.map
				if INPUTkey.kup: INPUTkey.kpress = False

