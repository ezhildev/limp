from config import *
from level import *
from lib.ui import *
from entities import Player

class MenuScreen:
	def __init__(self, game):
		self.game = game
		self.is_change_screen = False
		self.click_sound = pygame.mixer.Sound('./src/audios/select.ogg')
		self.button_change_sound = pygame.mixer.Sound('./src/audios/button_change.ogg')
		self.new_game_button = Text('New Game', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - 5 * GRID_SIZE))
		self.continue_button = Text('Continue', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - 3.5 * GRID_SIZE))

		self.texts = pygame.sprite.Group(
			Text(TITLE, font=FONT_L, position=WINDOW_CENTER),
			self.new_game_button,
			self.continue_button
		)
		
		if read_game('./src/save.txt')['level_number'] != 0:
			self.current_button = self.continue_button
			self.new_game_button.image.set_alpha(255 * .3)
		else: 
			self.current_button = self.new_game_button
			self.continue_button.image.set_alpha(255 * .3)

	def update(self):
		if INPUT.down.kup or INPUT.up.kup:
			self.button_change_sound.play()
			self.current_button.image.set_alpha(255 * .3)
			if self.current_button == self.new_game_button:
				self.current_button = self.continue_button
			else:
				self.current_button = self.new_game_button
			self.current_button.image.set_alpha(255)

		if INPUT.enter.kup and not self.is_change_screen:
			self.is_change_screen = True
			self.click_sound.play()

		if self.is_change_screen:
			fade_in(SCREEN_FADER, 5)
			if SCREEN_FADER.get_alpha() >= 255:
				if self.current_button == self.new_game_button:
					save_game({'level_number':0}, './src/save.txt')
				self.game.screen = LevelScreen(self.game)
		else:
			fade_out(SCREEN_FADER, 5)

	def draw(self, window):
		self.texts.draw(window)


class LevelScreen:
	def __init__(self, game):
		self.game = game
		self.is_back_menu = False
		self.is_restart_level = False
		self.player = Player()
		self.levels = []
		for num in range(12):
			self.levels.append(Level('./src/levels/{}.tmx'.format(num), self.player, 'Level {}'.format(num+1)))
		data = read_game('./src/save.txt')
		self.level_number = 0 if data == None else data['level_number']
		self.levels[self.level_number].load()

	def update(self):
		if INPUT.restart.kdown or not self.player.is_alive:
			self.is_restart_level = True
		elif INPUT.exit.kdown:
			self.is_back_menu = True

		if self.is_restart_level or self.is_back_menu or self.levels[self.level_number].is_complete:
			fade_in(SCREEN_FADER, 6)
			if SCREEN_FADER.get_alpha() >= 255:
				if self.is_restart_level:
					self.is_restart_level = False
				elif self.levels[self.level_number].is_complete: 
					self.level_number += 1
					if self.level_number >= len(self.levels):
						save_game({'level_number':0}, './src/save.txt')
						self.game.screen = CreditsScreen(self.game)
						return

				elif self.is_back_menu:
					save_game({'level_number':self.level_number}, './src/save.txt')
					self.levels[self.level_number].dispose()
					self.game.screen = MenuScreen(self.game)
					return

				self.levels[self.level_number].load()
		else:
			fade_out(SCREEN_FADER, 5)

		self.levels[self.level_number].update()

	def draw(self, window):
		self.levels[self.level_number].draw(window)


class CreditsScreen:
	def __init__(self, game) -> None:
		self.game = game
		self.is_exit = False
		self.texts = pygame.sprite.Group(
			Text('Code & Game Design', position=(WINDOW_CENTER[0], GRID_SIZE * 2)),
			Text('Ezhilarasan', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 3.5)),

			Text('Graphics', position=(WINDOW_CENTER[0], GRID_SIZE * 6)),
			Text('Anokolisa, penusbmic and bdragon1727', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 7.5)),

			Text('Music & SFX', position=(WINDOW_CENTER[0], GRID_SIZE * 10)),
			Text('AntipodeanWriter, didigameboy and Pixabay', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 11.5)),

			Text('Font', position=(WINDOW_CENTER[0], GRID_SIZE * 14)),
			Text('ThaleahFat', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 15.5)),

			Text('[Press Enter for exit]', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - GRID_SIZE)),
		)

	def update(self):
		if INPUT.enter.kdown:
			self.is_exit = True

		if self.is_exit:
			fade_in(SCREEN_FADER, 5)
			if SCREEN_FADER.get_alpha() >= 255:
				self.game.screen = MenuScreen(self.game)
		else:
			fade_out(SCREEN_FADER, 5)

	def draw(self, window):
		self.texts.draw(window)