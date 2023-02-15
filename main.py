from config import *
import time
import screens


class Game:
	def __init__(self):
		self.clock = pygame.time.Clock()
		pygame.display.set_caption(TITLE)
		self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.screen = screens.MenuScreen(self)
		self.music = pygame.mixer.Sound('./src/audios/music.ogg')
		self.music.set_volume(.75)
		self.music.play(-1)

	def run(self):
		while True:
			INPUT.reset()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					if isinstance(self.screen, screens.LevelScreen):
						save_game({'level_number': self.screen.level_number}, './src/save.txt')
					return
				INPUT.process_input(event)

			self.window.fill(BG_COLOR)
			self.screen.update()
			self.screen.draw(self.window)
			self.window.blit(SCREEN_FADER, (0, 0))
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()
	pygame.quit()
	sys.exit()