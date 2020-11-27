#progetto eseguito da Leonardo Fiore(322767) e Federico Putamorsi(320041)

from actor import Actor, Arena
from x7_BB import Wall, Enemy, Dragon, Bubble, Score

class BubbleBobbleGame:
    def __init__(self):
        self._arena = Arena((512, 456))
        self._scores = Score()
        self._levels = ["BB_main_menu.csv", "BB_level_1.csv", "BB_level_2.csv", "BB_end.csv"]
        self._config_Enemy, self._config_Dragon = "BB_config_Enemy_out_of_map.csv", "BB_config_Dragon_out_of_map.csv"
        self._game_length = (len(self._levels) - 1)
        self._cont_enemy, self._cont_killed = 0, 0
        self._points1, self._points2 = 0, 0
        self._coordinates1 = []
        self._coordinates2 = []
        self._enemies = []
        self._walls = []
        self._player = []
        self._win = False
        self._player1_ready, self._player2_ready = False, False
        self.levels(0, True, True)    

    def levels(self, n, player1_ready, player2_ready):   #metodo che gestisce i livelli
        self._current_level = self._levels[n]
        self._player1_ready, self._player2_ready = player1_ready, player2_ready 
        self._cont_enemy = 0
        self._cont_killed = 0

        if 0 < n < self._game_length:   #in base al livello corrente, cambia la configurazione dei vari oggetti
            self._config_Enemy, self._config_Dragon = "BB_config_Enemy.csv", "BB_config_Dragon.csv"
        else:
            self._config_Enemy, self._config_Dragon = "BB_config_Enemy_out_of_map.csv", "BB_config_Dragon_out_of_map.csv"   

        #parte di codice che ripulisce l'arena dai vari oggetti, utile nel cambio livello
        for obj in self._player:
            obj.remove_bubbles()
            obj.remove()
        for obj in self._enemies:
            obj.death()
        for obj in self._walls:
            obj.remove() 

        with open(self._config_Dragon, "r") as config_dragon:   #legge file configurazione giocatori
                first_line = config_dragon.readline()
                splitted_line = first_line.split(', ')
                self._x_dragon1 = int(splitted_line[0])
                self._y_dragon1 = int(splitted_line[1])
    
                second_line = config_dragon.readline()
                splitted_line = second_line.split(', ')
                self._x_dragon2 = int(splitted_line[0])
                self._y_dragon2 = int(splitted_line[1])      

        #viene deciso, in base a quale giocatore è pronto, chi è player 1 e 2
        if self._player1_ready and self._player2_ready:
            self._player1 = Dragon(self._arena, (self._x_dragon1, self._y_dragon1), 0)
            self._player2 = Dragon(self._arena, (self._x_dragon2, self._y_dragon2), 1)
            self._player.append(self._player1)
            self._player.append(self._player2)
        elif self._player1_ready and not(self._player2_ready):
            self._player1 = Dragon(self._arena, (self._x_dragon1, self._y_dragon1), 0)
            self._player.append(self._player1)
        elif self._player2_ready and not(self._player1_ready):
            self._player2 = Dragon(self._arena, (self._x_dragon2, self._y_dragon2), 1)
            self._player.append(self._player2)       

        with open(self._config_Enemy, "r") as config_enemy:   #legge file configurazione nemici e crea tali oggetti
            for line in config_enemy:
                splitted_line = line.split(', ')
                self._x_enemy = int(splitted_line[0])
                self._y_enemy = int(splitted_line[1])      
                self._enemies.append( Enemy(self._arena, (self._x_enemy, self._y_enemy)) )
                self._cont_enemy += 1

        with open(self._current_level, "r") as config_wall:   #legge file configurazione muri e crea tali oggetti
            for line in config_wall:
                splitted_line = line.split(', ')
                self._x_wall = int(splitted_line[0])
                self._y_wall = int(splitted_line[1])
                self._w_wall = int(splitted_line[2])
                self._h_wall = int(splitted_line[3])
                self._walls.append( Wall(self._arena, (self._x_wall, self._y_wall), (self._w_wall, self._h_wall)) )         

    def arena(self):
        return self._arena

    def player1(self):
        return self._player1

    def player2(self):
        return self._player2 

    def game_won(self):   #metodo che controlla se si ha vinto
        if self._player1.enemy_killed():
            self._cont_killed += 1
            self._points1 += 500

        if self._player2.enemy_killed():
            self._cont_killed += 1
            self._points2 += 500     

        if self._cont_killed == self._cont_enemy:   
            self._win = True
        else:
            self._win = False                        
        
        return self._win

    def game_over(self):   #metodo che controlla se si ha perso
        if self._player1_ready and self._player2_ready:
            if self._player1.dead() and self._player1.dead():
                self._lost = True
                self._scores.reset(1)
                self._scores.reset(2)
            else:
                self._lost = False
        else:        
            if self._player1_ready:
                if self._player1.dead():
                    self._lost = True
                    self._scores.reset(1)
                else:
                    self._lost = False
            elif self._player2_ready:
                if self._player2.dead():
                    self._lost = True
                    self._scores.reset(2)
                else:
                    self._lost = False   
            else:
                self._lost = False        

        return self._lost                  

    def write_scores(self):   #metodo che controlla restituisce le coordinate dei simboli dei punteggi, tramite la classe Score
        self._coordinates1, self._coordinates2 = self._scores.score(self._points1, self._points2)
        
        return self._coordinates1, self._coordinates2

    def total_levels(self):
        return self._game_length

BubbleBobbleGame()        