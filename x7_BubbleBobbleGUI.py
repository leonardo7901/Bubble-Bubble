#progetto eseguito da Leonardo Fiore e Federico Putamorsi

import g2d
from x7_BubbleBobbleGame import BubbleBobbleGame

class BubbleBobbleGUI:
    def __init__(self):
        self._game = BubbleBobbleGame()
        self._total_levels = self._game.total_levels()
        self._sprites = g2d.load_image("https://tomamic.github.io/images/sprites/bubble-bobble.png")
        self._background = g2d.load_image("https://tomamic.github.io/images/sprites/bubble-bobble-maps.png")
        self._ready = g2d.load_image("r-nr.png")
        self._menu = g2d.load_image("BB-main-menu.png")
        self._end = g2d.load_image("BB-end.png")
        self._x_y_background = [(0,0), (0, 0), (512, 0), (0, 0), (0, 0)]
        self._player1_ready, self._player2_ready = False, False
        self._k = 0
        self._numbers_scores = []
        self._x = 8
        g2d.init_canvas(self._game.arena().size())
        g2d.main_loop(self.tick)

    def movement(self):
        player1 = self._game.player1()
        player2 = self._game.player2()
        if g2d.key_pressed("w"):
            player1.go_up()

        if g2d.key_pressed("d"):
            player1.go_right(True)
        elif g2d.key_released("d"):
            player1.go_right(False)

        if g2d.key_pressed("a"):
            player1.go_left(True)
        elif g2d.key_released("a"):
            player1.go_left(False)

        if g2d.key_pressed("q"):
            if self._k == 0:
                self._player1_ready = not self._player1_ready
            player1.attack()

        if g2d.key_pressed("ArrowUp"):
            player2.go_up()

        if g2d.key_pressed("ArrowRight"):
            player2.go_right(True)
        elif g2d.key_released("ArrowRight"):
            player2.go_right(False)

        if g2d.key_pressed("ArrowLeft"):
            player2.go_left(True)
        elif g2d.key_released("ArrowLeft"):
            player2.go_left(False)

        if g2d.key_pressed("Spacebar"):
            if self._k == 0:
                self._player2_ready = not self._player2_ready
            player2.attack()

        if self._k == 0:
            if self._player1_ready or self._player2_ready:
                if g2d.key_pressed("Enter"):
                    self._k = 1
                    self._game.levels(self._k, self._player1_ready, self._player2_ready)          

    def tick(self):
        self.movement()
        arena = self._game.arena()
        arena.move_all()    
        g2d.clear_canvas()
        
        if 0 < self._k < self._total_levels:
            self._x_background, self._y_background = self._x_y_background[self._k]
            g2d.draw_image_clip(self._background, (self._x_background, self._y_background, 512, 424), (0, 32, 512, 424))
        elif self._k == 0:
            g2d.draw_image_clip(self._menu, (0, 0, 512, 424), (0, 32, 512, 424))
            if self._player1_ready:    
                g2d.draw_image_clip(self._ready, (0, 0, 100, 18), (312, 284, 100, 16))
            else:
                g2d.draw_image_clip(self._ready, (0, 20, 174, 18), (312, 284, 174, 16))
            if self._player2_ready:    
                g2d.draw_image_clip(self._ready, (0, 0, 100, 18), (312, 316, 100, 16))
            else:
                g2d.draw_image_clip(self._ready, (0, 20, 174, 18), (312, 316, 174, 16))
        else:
            g2d.draw_image_clip(self._end, (0, 0, 512, 424), (0, 32, 512, 424))
            
        if self._game.game_won():
            self._k += 1
            self._game.levels(self._k, self._player1_ready, self._player2_ready)
        
        if self._game.game_over():
            self._k = 0
            self._game.levels(self._k, self._player1_ready, self._player2_ready)  

        self._numbers_scores = self._game.write_scores()

        self._x = 8
        for i in self._numbers_scores:
            self._x_number, self._y_number = i
            g2d.draw_image_clip(self._sprites, (self._x_number, self._y_number, 8, 8), (self._x, 8, 8, 8))
            self._x += 8

        for a in arena.actors():
            if a.symbol() != (0, 0, 0, 0):
                g2d.draw_image_clip(self._sprites, a.symbol(), a.position())
            #else:
            #   g2d.fill_rect(a.position())       
  
gui = BubbleBobbleGUI()