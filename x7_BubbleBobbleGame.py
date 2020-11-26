#progetto eseguito da Leonardo Fiore e Federico Putamorsi

from actor import Actor, Arena
from x7_BB import Wall, Enemy, Dragon, Bubble, Score

class BubbleBobbleGame:
    def __init__(self):
        self._arena = Arena((512, 456))
        self._scores = Score()
        self._cont_enemy = 0
        self._cont_killed = 0
        #self._n = n
        self._win = False
        self._levels = ["BB_level_1.csv", "BB_level_2.csv"]
        #self._current_level = self._levels[self._n]
        self._points = 0
        self._coordinates = []
        self._enemies = []
        self._walls = []
        self._player = []

        with open("BB_config_Dragon.csv", "r") as config_dragon:
            first_line = config_dragon.readline()
            splitted_line = first_line.split(', ')
            self._x_dragon1 = int(splitted_line[0])
            self._y_dragon1 = int(splitted_line[1])
            second_line = config_dragon.readline()
            splitted_line = second_line.split(', ')
            self._x_dragon2 = int(splitted_line[0])
            self._y_dragon2 = int(splitted_line[1])      
            self._player.append(Dragon( self._arena, (self._x_dragon1, self._y_dragon1)) )
            self._player.append(Dragon( self._arena, (self._x_dragon2, self._y_dragon2)) )

        self.levels(0)    

    def levels(self, n):
        self._current_level = self._levels[n]
        
        self._cont_enemy = 0
        self._cont_killed = 0

        for obj in self._enemies:
            obj.death()
        for obj in self._walls:
            obj.remove() 

        with open("BB_config_Enemy.csv", "r") as config_enemy:
            for line in config_enemy:
                splitted_line = line.split(', ')
                self._x_enemy = int(splitted_line[0])
                self._y_enemy = int(splitted_line[1])      
                self._enemies.append( Enemy(self._arena, (self._x_enemy, self._y_enemy)) )
        self._cont_enemy = len(self._enemies)

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
        return self._player[0]

    def player2(self):
        return self._player[1]

    def game_won(self):
        if self._player[0].enemy_killed() or self._player[0].enemy_killed():
            self._cont_killed += 1
            self._points += 500
        else:
            self._points = 0    

        if self._cont_killed == self._cont_enemy:   
            self._win = True
        else:
            self._win = False                     
        
        return self._win

    def write_scores(self):
        self._coordinates = self._scores.score(self._points)

        return self._coordinates

    def total_levels(self):
        return len(self._levels)

BubbleBobbleGame()        