#progetto eseguito da Leonardo Fiore e Federico Putamorsi

import g2d
from x7_BubbleBobbleGame import BubbleBobbleGame

class BubbleBobbleGUI:
    def __init__(self):
        self._game = BubbleBobbleGame()
        self._sprites = g2d.load_image("https://tomamic.github.io/images/sprites/bubble-bobble.png")
        self._background = g2d.load_image("https://tomamic.github.io/images/sprites/bubble-bobble-maps.png")
        self._x_y_background = [(0, 0), (512, 0)]
        self._k = 0
        self._numbers_scores = []
        self._x = 8
        self._waiting = -165
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
            player2.attack()               

    def tick(self):
        self.movement()
        arena = self._game.arena()
        arena.move_all()    
        g2d.clear_canvas()
        
        self._x_background, self._y_background = self._x_y_background[self._k]
        g2d.draw_image_clip(self._background, (self._x_background, self._y_background, 512, 424), (0, 32, 512, 424))
       
        if self._game.game_won():
            if self._waiting >= 0:
                self._k += 1
                if self._k >= self._game.total_levels():
                    g2d.clear_canvas()
                    g2d.alert("Game Won!")
                else:
                    self._game.levels(self._k) 
            else:
                self._waiting += 1 
            print(self._waiting)

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