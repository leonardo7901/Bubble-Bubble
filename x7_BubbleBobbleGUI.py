#progetto eseguito da Leonardo Fiore(322767) e Federico Putamorsi(320041)

import g2d
from x7_BubbleBobbleGame import BubbleBobbleGame

class BubbleBobbleGUI:
    def __init__(self):
        self._game = BubbleBobbleGame()
        self._total_levels = self._game.total_levels()
        self._sprites = g2d.load_image("bubble-bobble.png")
        self._background = g2d.load_image("bubble-bobble-maps.png")
        self._menu = g2d.load_image("BB_main_menu.png")
        self._end = g2d.load_image("BB_end.png")
        self._ready = g2d.load_image("BB_ready_not-ready.png")
        self._x_y_background = [(0,0), (0, 0), (512, 0), (0, 0), (0, 0)]
        self._player1_ready, self._player2_ready = False, False
        self._time_of_win, self._time_of_lost = 0, 0
        self._current_level = 0
        self._numbers_scores1 = []
        self._numbers_scores2 = []
        self._x1, self._x2 = 2, 450
        self._win, self._lost = True, True
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

        if self._current_level == 0:
            if g2d.key_pressed("q"):   #il giocatore 1 viene evidenziato pronto o non pronto quando viene premuto il tasto 
                self._player1_ready = not self._player1_ready

            if g2d.key_pressed("Spacebar"):   #il giocatore 2 viene evidenziato pronto o non pronto quando viene premuto il tasto 
                self._player2_ready = not self._player2_ready

            if self._player1_ready or self._player2_ready:   #invoca il metodo che cambia livello, se almeno un giocatore è pronto
                if g2d.key_pressed("Enter"):
                    self._current_level = 1
                    self._game.levels(self._current_level, self._player1_ready, self._player2_ready)          

    def tick(self):
        self.movement()
        arena = self._game.arena()
        arena.move_all()    
        g2d.clear_canvas()
        
        if 0 < self._current_level < self._total_levels:   #se il livello attuale è un livello di gioco, disegna il background inerente
            self._x_background, self._y_background = self._x_y_background[self._current_level]
            g2d.draw_image_clip(self._background, (self._x_background, self._y_background, 512, 424), (0, 32, 512, 424))

            if self._game.game_won():
                if self._win:   #condizioni che peremettono di conoscere il momento in cui si vince
                    self._time_of_win = arena.count()
                self._win = False
                if arena.count() - self._time_of_win > 90:   #se sono passati almeno 90 frame dalla vittoria, cambia livello
                    self._current_level += 1
                    self._game.levels(self._current_level, self._player1_ready, self._player2_ready)
                    self._win = True           
            
            if self._game.game_over():
                if self._lost:   #condizioni che peremettono di conoscere il momento in cui si perde
                    self._time_of_win = arena.count()
                self._lost = False
                if arena.count() - self._time_of_lost > 90:   #se sono passati almeno 90 frame dalla sconfitta, ritorna al menu
                    self._current_level = 0
                    self._game.levels(self._current_level, self._player1_ready, self._player2_ready)
                    self._lost = True
        elif self._current_level == 0:   #se si è nel menu, disegna il background inerente e se e quale giocatore è pronto  
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
            g2d.draw_image_clip(self._end, (0, 0, 512, 424), (0, 32, 512, 424))   #disegna il background finale  

        g2d.set_color((0, 0, 0))
        g2d.fill_rect((0, 0, 512, 48))

        #parte di codice che scrive il punteggio del player 1 e 2
        self._numbers_scores1, self._numbers_scores2 = self._game.write_scores()                                                                           
        self._x1 = 2
        for i in self._numbers_scores1:
            self._x_number1, self._y_number1 = i
            g2d.draw_image_clip(self._sprites, (self._x_number1, self._y_number1, 8, 7), (self._x1, 32, 12, 12))
            g2d.draw_image_clip(self._sprites, (107, 1280, 37, 24), (2, 2, 37, 24))
            self._x1 += 12

        self._x2 = 450
        for h in self._numbers_scores2:
            self._x_number2, self._y_number2 = h
            g2d.draw_image_clip(self._sprites, (self._x_number2, self._y_number2, 8, 7), (self._x2, 32, 12, 12))
            g2d.draw_image_clip(self._sprites, (267, 1280, 49, 24), (450, 2, 49, 24))
            self._x2 += 12    

        for a in arena.actors():
            if a.symbol() != (0, 0, 0, 0):
                g2d.draw_image_clip(self._sprites, a.symbol(), a.position())
            #else:
            #   g2d.fill_rect(a.position())
            
            a.check_actors()       
  
gui = BubbleBobbleGUI()