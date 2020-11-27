#progetto eseguito da Leonardo Fiore e Federico Putamorsi

import g2d
from actor import Actor, Arena
from random import randint

class Wall(Actor):
    def __init__(self, arena, pos, size):
        self._x, self._y = pos
        self._w, self._h = size
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass

    def remove(self):
        self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 0, 0, 0, 0

class Enemy(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._x_symbol, self._y_symbol = 1269, 246
        self._last_x_symbol, self._last_y_symbol = 1269, 246
        self._last_dx = 0
        self._dx, self._dy, self._speed = 0, 0, 9
        self._arena = arena
        self._arena_w, self._arena_h = self._arena.size()
        self._g = 0.4
        self._landed, self._collided = False, False
        self._dead = False
        arena.add(self)

    def move(self): 
        #scelta "casuale" della direzione 
        self._movement = randint(0,3)
        if self._movement == 0:
            self.go_up()
        elif self._movement == 1:
            self.go_right(True)
        elif self._movement == 2:
            self.go_left(True)

        #controlla e decide lo spostamento dell'avversario, in base a se è stato colpito dalla bolla o meno
        if self._collided == True:
            self._dx, self._dy = 0, -1
        else:
            self._dy = self._dy + self._g    

        self._y += self._dy
        if self._y <= 64:
            self._y = 64
            self._dy = 0
        elif self._y > self._arena_h + self._h:
            self.death()    
    
        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > self._arena_w - self._w:
            self._x = self._arena_w - self._w       
        
        #controlla se lo sprite sta saltando
        if self._dy != 0:
            self._landed = False

    def go_up(self):
        if self._landed:            
            self._dy, self._landed = -self._speed, False          
    
    def go_left(self, go: bool):              
        if go:
            self._dx = -self._speed / 2
            self._last_dx = self._dx
        else:
            self._dx = 0                

    def go_right(self, go: bool):                
        if go:
            self._dx = +self._speed / 2
            self._last_dx = self._dx
        else:
            self._dx = 0

    def collide(self, other):
        if isinstance(other, Wall):
            x_d, y_d, w_d, h_d = self.position()
            x_w, y_w, w_w, h_w = other.position()
            
            borders = [(x_d+w_d - x_w, -1, 0), (x_w+w_w - x_d, 1, 0),
                       (y_d+h_d - y_w, 0, -1), (y_w+h_w - y_d, 0, 1)]
            nearest_border = min(borders)
           
            if self._dy > 0:
                self._y += nearest_border[2] * nearest_border[0]
                self._x += nearest_border[1] * nearest_border[0] 
    
                if nearest_border[2] < 0:
                    self._landed = True
                if nearest_border[2] != 0:
                    self._dy = 1
            else:
                self._x += nearest_border[1] * nearest_border[0]
    
        if isinstance(other, Bubble):
            self._collided = True         

        if isinstance(other, Dragon):
            if self._collided == True:
                self.death()    

    #restituisce se l'avversario è stato o meno colpito dalla bolla
    def collided(self):
        return self._collided

    def death(self):
        self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):      
        if self._collided == False:    
            if self._dx < 0:
                self._x_symbol, self._y_symbol = 6, 246
                self._last_x_symbol, self._last_y_symbol = 6, 246
            elif self._dx > 0:
                self._x_symbol, self._y_symbol = 1269, 246
                self._last_x_symbol, self._last_y_symbol = 1269, 246    

            if self._landed == True:
                self._x_symbol, self._y_symbol = self._last_x_symbol, self._last_y_symbol
        else:
            self._x_symbol, self._y_symbol = 376, 246

        return self._x_symbol, self._y_symbol, self._w, self._h      

class Dragon(Actor):
    def __init__(self, arena, pos, player):
        self._x, self._y = pos
        self._spawn = pos
        self._player = player
        self._w, self._h = 16, 16
        self._lives = 3
        if self._player == 1:
            self._x_symbol, self._y_symbol = 1268, 16
            self._last_x_symbol, self._last_y_symbol = 1268, 16
        elif self._player == 2:
            self._x_symbol, self._y_symbol = 329, 16
            self._last_x_symbol, self._last_y_symbol = 329,16    
        self._last_dx = 0
        self._dx, self._dy, self._speed = 0, 0, 10
        self._arena = arena
        self._arena_w, self._arena_h = self._arena.size()
        self._g = 0.4
        self._time_of_attack = 0
        self._bubbles = []
        self._landed = False
        self._enemy_killed = False
        self._enemy_dead = False
        self._dead = False
        arena.add(self)

    def move(self):
        self._dy = self._dy + self._g
        self._y += self._dy
        if self._y <= 64:
            self._y = 64
            self._dy = 0
        elif self._y > self._arena_h + self._h:
            self.death()

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > self._arena_w - self._w:
            self._x = self._arena_w - self._w

        if self._dy != 0:
            self._landed = False

    def go_up(self):
        if self._landed:            
            self._dy, self._landed = -self._speed, False          
    
    def go_left(self, go: bool):              
        if go:
            self._dx = -self._speed
            self._last_dx = self._dx
        else:
            self._dx = 0                

    def go_right(self, go: bool):                
        if go:
            self._dx = +self._speed
            self._last_dx = self._dx
        else:
            self._dx = 0       

    #metodo che crea oggetti bolla ogni volta che viene invocato
    def attack(self):
        if self._lives > 0:
            if self._last_dx < 0:
                self._bubbles.append(Bubble(self._arena, (self._x, self._y), -5, self._player))
            else:
                self._bubbles.append(Bubble(self._arena, (self._x, self._y), 5, self._player))
        
        if len(self._bubbles) > 32:
            self._bubbles[0].death()
            self._bubbles.pop(0)
                            
    def collide(self, other):
        if isinstance(other, Wall):
            x_d, y_d, w_d, h_d = self.position()
            x_w, y_w, w_w, h_w = other.position()
            
            borders = [(x_d+w_d - x_w, -1, 0), (x_w+w_w - x_d, 1, 0),
                       (y_d+h_d - y_w, 0, -1), (y_w+h_w - y_d, 0, 1)]
            nearest_border = min(borders)
           
            if self._dy > 0:
                self._y += nearest_border[2] * nearest_border[0]
                self._x += nearest_border[1] * nearest_border[0] 
    
                if nearest_border[2] < 0:
                    self._landed = True
                if nearest_border[2] != 0:
                    self._dy = 1
            else:
                self._x += nearest_border[1] * nearest_border[0]    
        
        if isinstance(other, Enemy):
            self._bubbled = other.collided()  #chiede alla classe Enemy se l'avversario è stato colpito dalla bolla
            if self._bubbled == False:    
                self.death()
            else:
                self._enemy_killed = True    

    def enemy_killed(self):
        self._enemy_dead = self._enemy_killed
        self._enemy_killed = False

        return self._enemy_dead           

    def death(self):
        self._lives -= 1
        if self._lives == 0:
            self._arena.remove(self)
            self._dead = True
        else:
            self._x, self._y = self._spawn
            self._dead = False    

    def dead(self):
        return self._dead        

    def remove(self):
        self._arena.remove(self)

    def remove_bubbles(self):
        for obj in self._bubbles:
            obj.death()

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):     
        if self._player == 1: 
            if self._dx < 0:
                self._x_symbol, self._y_symbol = 6, 16
                self._last_x_symbol, self._last_y_symbol = 6,16
            elif self._dx > 0:
                self._x_symbol, self._y_symbol = 1268, 16
                self._last_x_symbol, self._last_y_symbol = 1268,16    

            if self._dy < 0:
                if self._last_dx < 0:
                    self._x_symbol, self._y_symbol = 217, 36
                else:    
                    self._x_symbol, self._y_symbol = 1058, 36
            elif self._dy > 0:
                if self._last_dx < 0:
                    self._x_symbol, self._y_symbol = 238, 36
                else:    
                    self._x_symbol, self._y_symbol = 1037, 36       
            
            if self._landed == True:
                self._x_symbol, self._y_symbol = self._last_x_symbol, self._last_y_symbol
        
        elif self._player == 2:
            if self._dx < 0:
                self._x_symbol, self._y_symbol = 329, 16
                self._last_x_symbol, self._last_y_symbol = 329,16
            elif self._dx > 0:
                self._x_symbol, self._y_symbol = 946, 16
                self._last_x_symbol, self._last_y_symbol = 946,16    

            if self._dy < 0:
                if self._last_dx < 0:
                    self._x_symbol, self._y_symbol = 541, 36
                else:    
                    self._x_symbol, self._y_symbol = 714, 36
            elif self._dy > 0:
                if self._last_dx < 0:
                    self._x_symbol, self._y_symbol = 562, 36
                else:    
                    self._x_symbol, self._y_symbol = 736, 36       
            
            if self._landed == True:
                self._x_symbol, self._y_symbol = self._last_x_symbol, self._last_y_symbol

        return self._x_symbol, self._y_symbol, self._w, self._h

class Bubble(Actor):
    def __init__(self, arena, pos, dx, player):
        self._x, self._y = pos
        self._player = player
        self._w, self._h = 16, 16
        self._dx, self._dy = dx, 0
        self._direction = self._dx
        self._frame = 20
        self._arena = arena
        self._arena_w, self._arena_h = self._arena.size()
        self._time_of_spawn = self._arena.count()
        arena.add(self)

    def move(self):
        #movimento lungo asse x per tot frame
        if self._frame > 0:
            self._frame -= 1

            self._x += self._dx
            if self._x < 0:
                self._arena.remove(self)
            elif self._x > self._arena_w - self._w:
                self._arena.remove(self)

            if self._y == 32:
                self._y = 32
                self._dy = 0    
        else:
            self._dy = -1
            self._y += self._dy
            if self._y <= 64:
                self._y = 64
                self._dy = 0
            elif self._y > self._arena_h - self._h:
                self._y = self._arena_h - self._h                  

    def collide(self, other):
        if isinstance(other, Wall):
            x_d, y_d, w_d, h_d = self.position()
            x_w, y_w, w_w, h_w = other.position()
            
            borders = [(x_d+w_d - x_w, -1, 0), (x_w+w_w - x_d, 1, 0),
                       (y_d+h_d - y_w, 0, -1), (y_w+h_w - y_d, 0, 1)]
            nearest_border = min(borders)
           
            if self._dy > 0:
                self._y += nearest_border[2] * nearest_border[0]
                self._x += nearest_border[1] * nearest_border[0] 
    
                if nearest_border[2] != 0:
                    self._dy = 1
            else:
                self._x += nearest_border[1] * nearest_border[0]
        
        if isinstance(other, Enemy):
            self.death()   

    def death(self):
        self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self): 
        if self._player == 1:
            if self._dx < 0:
               self._x_symbol, self._y_symbol = 78, 1050 
            elif self._dx > 0:
                self._x_symbol, self._y_symbol = 1198, 1050

            if self._dy < 0:
                if self._direction < 0:
                    self._x_symbol, self._y_symbol = 8, 1071
                    self._last_x_symbol, self._last_y_symbol = self._x_symbol, self._y_symbol
                elif  self._direction > 0:
                    self._x_symbol, self._y_symbol = 1270, 1071
                    self._last_x_symbol, self._last_y_symbol = self._x_symbol, self._y_symbol    
            elif self._y == 64:
                self._x_symbol, self._y_symbol = self._last_x_symbol, self._last_y_symbol

        if self._player == 2:
            if self._dx < 0:
                self._x_symbol, self._y_symbol = 293, 1050
            elif self._dx > 0:
                self._x_symbol, self._y_symbol = 983, 1050

            if self._dy < 0:
                if self._direction < 0:
                    self._x_symbol, self._y_symbol = 62, 1071
                    self._last_x_symbol, self._last_y_symbol = self._x_symbol, self._y_symbol
                elif  self._direction > 0:
                    self._x_symbol, self._y_symbol = 1216, 1071
                    self._last_x_symbol, self._last_y_symbol = self._x_symbol, self._y_symbol
            elif self._y == 64:
                self._x_symbol, self._y_symbol = self._last_x_symbol, self._last_y_symbol


        return self._x_symbol, self._y_symbol, self._w, self._h

class Score():
    def __init__(self):
        self._score1 = 0
        self._score2 = 0
        self._x_symbol = 148
        self._numbers_white = []
        self._numbers_blue = []
        self._symbol_list1 = []
        self._symbol_list2 = []
        for i in range(10):
            self._numbers_white.append((self._x_symbol, 1608))
            self._numbers_blue.append((self._x_symbol, 1620))
            self._x_symbol += 9

    def score(self, n, m):
        self._symbol_list1 = []
        self._symbol_list2 = []
        self._score1 = n
        self._score2 = m 

        self._score1 = str(self._score1)
        for h in self._score1:
            self._symbol_list1.append(self._numbers_white[int(h)])
            str(h)
        self._score1 = int(self._score1)

        self._score2 = str(self._score2)
        for h in self._score2:
            self._symbol_list2.append(self._numbers_blue[int(h)])
            str(h)
        self._score2 = int(self._score2)

        return self._symbol_list1, self._symbol_list2

    def reset(self, c):
        if c == 1:
            self._score1 = 0
        else:  
            self._score2 = 0  