#progetto eseguito da Leonardo Fiore e Federico Putamorsi

from actor import Actor, Arena
from x7_BB import Wall, Enemy, Dragon, Bubble, Score

class BubbleBobbleGame:
    def __init__(self):
        self._arena = Arena((512, 456))
        self._scores = Score()
        self._cont_enemy = 0
        self._cont_killed = 0
        self._win = False
        self._levels = ["BB_main_menu.csv", "BB_level_1.csv", "BB_level_2.csv", "BB_end.csv"]
        self._config_Enemy, self._config_Dragon = "BB_config_Enemy_out_of_map.csv", "BB_config_Dragon_out_of_map.csv"
        self._points = 0
        self._coordinates = []
        self._enemies = []
        self._walls = []
        self._player = []
        self._player1_ready, self._player2_ready = False, False
        self.levels(0, True, True)    

    def levels(self, n, player1_ready, player2_ready):
        self._current_level = self._levels[n]
        self._player1_ready, self._player2_ready = player1_ready, player2_ready 

        if 0 < n < (len(self._levels) - 1) :
            self._config_Enemy, self._config_Dragon = "BB_config_Enemy.csv", "BB_config_Dragon.csv"
        else:
            self._config_Enemy, self._config_Dragon = "BB_config_Enemy_out_of_map.csv", "BB_config_Dragon_out_of_map.csv"   
        self._cont_enemy = 0
        self._cont_killed = 0

        for obj in self._player:
            obj.remove_bubbles()
            #if n == (len(self._levels) - 1):
            obj.remove()
        for obj in self._enemies:
            obj.death()
        for obj in self._walls:
            obj.remove() 

        with open(self._config_Dragon, "r") as config_dragon:
            if self._player1_ready:
                first_line = config_dragon.readline()
                splitted_line = first_line.split(', ')
                self._x_dragon1 = int(splitted_line[0])
                self._y_dragon1 = int(splitted_line[1])
                self._player.append(Dragon( self._arena, (self._x_dragon1, self._y_dragon1)) )
            if self._player2_ready:    
                second_line = config_dragon.readline()
                splitted_line = second_line.split(', ')
                self._x_dragon2 = int(splitted_line[0])
                self._y_dragon2 = int(splitted_line[1])      
                self._player.append(Dragon( self._arena, (self._x_dragon2, self._y_dragon2)) )
        self._player.reverse()
        self._player1 = self._player[0]
        self._player2 = self._player[1]
        self._player.reverse()   

        with open(self._config_Enemy, "r") as config_enemy:
            for line in config_enemy:
                splitted_line = line.split(', ')
                self._x_enemy = int(splitted_line[0])
                self._y_enemy = int(splitted_line[1])      
                self._enemies.append( Enemy(self._arena, (self._x_enemy, self._y_enemy)) )
                self._cont_enemy += 1

        with open(self._current_level, "r") as config_wall:
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

    def game_won(self):
        if self._player1.enemy_killed() or self._player2.enemy_killed():
            self._cont_killed += 1
            self._points += 500
        else:
            self._points = 0    

        if self._cont_killed == self._cont_enemy:   
            self._win = True
        else:
            self._win = False                         
        
        return self._win

    def game_over(self):
        if self._player1_ready:
            if self._player1.dead() and self._player2_ready == False:
                self._lost = True
            else:
                self._lost = False
        elif self._player2_ready:
            if self._player2.dead():
                self._lost = True
            else:
                self._lost = False

        print(self._lost)
        return self._lost                  

    def write_scores(self):
        self._coordinates = self._scores.score(self._points)

        return self._coordinates

    def total_levels(self):
        return (len(self._levels) - 1)

BubbleBobbleGame()        