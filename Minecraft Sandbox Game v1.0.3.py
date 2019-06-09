#CAMERON WATTS#
#COMP PROG#
#5/29/19#

import pygame, sys, math
from pygame.locals import *
import random
import copy

"""colors"""
black = (0,0,0)
gray = (125,125,125)
bg_color = (30,144,255)
pos_ = (0,0)
""

pygame.mixer.pre_init(44100, 16, 1, 4096)
pygame.mixer.init()
pygame.init()
screen = {'display':pygame.display.set_mode((800,704)),'fps':pygame.time.Clock(),'x_display':672,'y_display':672,'x_end':7680,'y_end':7680} #screen#

theme = pygame.mixer.Sound('minecraft.wav')
theme.play(-1)
sound_var = True
temp_list_sound = [True,False]
temp_list2_sound = ['other/sound_on.png','other/sound_off.png']

player_value = None

font = pygame.font.Font(None, 30)

class Button():
    def __init__(self,typee,x,y,width,height,image):
        self.x = x
        self.y = y
        self.typee = typee
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)
        self.image = self.image.convert_alpha()
        
    def press(self):
        """depending on the "typee" value of the button, differnt things happen"""
        global entitys, entitys_cords, player_pass, temp_list_sound, temp_list2_sound, sound_var, entitys_org, player_pass2, entitys2, player_value
        
        if self.typee == 'HELPP':
            instructions(instructions_img,'EDITOR')


            
        if self.typee == 'HELPP2':
            instructions(instructions2_img,'GAME')


            
        if self.typee == 'PLAY':    #plays game#
            for value in entitys:
                for value2 in entitys[value]:
                    if value2.__class__.__name__ == 'Entity':
                        player_pass = copy.copy(value2)
                        player_pass2 = copy.copy(player_pass)
                        game()


            
        if self.typee == 'EDIT':           #changes to the editor
            scroll['x'] = 0 ; scroll['y'] = 0
            editor()


            
        if self.typee == 'BG':             #changes layer to background#
            bg.image = pygame.image.load('other/bg_select.png')
            fg.image = pygame.image.load('other/fg.png')
            
            for x in objects:
                eval(x).typee = 'PASS'



        if self.typee == 'FG':             #changes layer to foreground#
            bg.image = pygame.image.load('other/bg.png')
            fg.image = pygame.image.load('other/fg_select.png')
            for x in objects:
                eval(x).typee = 'SOLID'



        if self.typee == 'SOUND':           #turns on/off sound#
            sound_var = temp_list_sound[-1]
            self.image = pygame.image.load(temp_list2_sound[-1])
            temp_list_sound = temp_list_sound[::-1]
            temp_list2_sound = temp_list2_sound[::-1]


            
        if self.typee == 'TRASH':#deletes all entitys#
            player_value = None
            for x in entitys:
                entitys[x] = []
                
            entitys_cords_function(scroll['x'],scroll['y'],-1)
                        

            
        if self.typee == 'SAVE':            #saves all entitys to a file#
            file = open('saves/save.txt','w')
            for value in entitys:
                for value2 in entitys[value]:
                    file.write(''+str(value2.name)+ ',' +str(value2.typee)+ ',' +str(value2.x)+ ',' +str(value2.y)+ '\n')
            file.close()


        
        if self.typee == 'LOAD':            #loads save file#
            for x in entitys:
                entitys[x] = []
                
            file = open('saves/save.txt','r')
            file_read = file.read() ; file_split = file_read.split('\n')
            
            for temp_entity in file_split:
                try:
                    temp_entity2 = temp_entity.split(',')
                    
                    temp = (eval(temp_entity2[0]))
                    temp.typee = str(temp_entity2[1])
                    temp.x = int(temp_entity2[2])
                    temp.y = int(temp_entity2[3])
                    if temp_entity2[0] == 'player':
                        player_value = temp
                    pos_chunk_x = int(temp.x / 672)
                    pos_chunk_y = int(temp.y / 672)
                    entitys[str(pos_chunk_x)+','+str(pos_chunk_y)].append(copy.copy(temp))
                except:
                    pass
                
            entitys_cords_function(scroll['x'],scroll['y'],-1)
            
            file.close()


        if self.typee == 'EXIT': #exits instructions to the editor#
            editor()

 
        if self.typee == 'EXIT2': #exits instructions to the game#
            game()


            
class Object():
    def __init__(self,name,typee,invx,invy,x,y,width,height,image):
        self.name = name
        self.typee = typee
        self.invx = invx
        self.invy = invy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.image_transparent_name = ('texture/'+str(self.name)+'_trans.png')
        self.image_transparent = pygame.image.load(self.image_transparent_name)
        self.image_name = ('texture/'+str(self.name)+'.png')
        self.image = pygame.image.load(self.image_name)
        self.image = self.image.convert_alpha()
        self.image_transparent = self.image_transparent.convert_alpha()

        #sets a block type, and depending on the block type later on it will play a specific sound for it.#
        if self.name == 'stone' or 'concrete' in self.name or 'terracotta' in self.name or self.name == 'brick' or 'glass' in self.name:
            self.block_type = 'stone'
        if self.name == 'grass' or self.name == 'dirt' or self.name == 'hay' or self.name == 'leaf' or 'flower' in self.name:
            self.block_type = 'grass'
        if 'log' in self.name or 'wood' in self.name:
            self.block_type = 'wood'
        if 'wool' in self.name:
            self.block_type = 'wool'
        if self.name == 'sand' or self.name == 'cactus':
            self.block_type = 'sand'

    def play_sound(self):
        if sound_var == True:
            random_sound = random.randrange(1,5)
            pygame.mixer.music.load('sound_effects/'+str(self.block_type)+''+str(random_sound)+'.wav')
            pygame.mixer.music.play(0)


   
class Entity():
    def __init__(self,name,typee,move,invx,invy,x,y,width,height,image):
        self.name = name
        self.typee = typee
        self.move = move
        self.invx = invx
        self.invy = invy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.image_transparent_name = ('texture/'+str(self.name)+'_right_trans.png')
        self.image_transparent = pygame.image.load(self.image_transparent_name)
        self.image_name = ('texture/'+str(self.name)+'_right.png')
        self.image = pygame.image.load(self.image_name)
        self.frame = 0

        #sets a block type, and depending on the block type later on it will play a specific sound for it.#
        if self.name == 'player':
            self.block_type = 'stone'
            
    def update(self):
        #depending on player input, will flip image to face that direction#
        if player.move['right'] == True and player.move['left'] == False:
            self.image_name = ('texture/'+str(self.name)+'_right.png')
            self.image = pygame.image.load(self.image_name)
            self.image_transparent_name = ('texture/'+str(self.name)+'_right_trans.png')
            
            self.image_transparent = pygame.image.load(self.image_transparent_name)
        if player.move['left'] == True and player.move['right'] == False:
            self.image_name = ('texture/'+str(self.name)+'_left.png')
            self.image = pygame.image.load(self.image_name)
            self.image_transparent_name = ('texture/'+str(self.name)+'_left_trans.png')
            self.image_transparent = pygame.image.load(self.image_transparent_name)
        

            
    def play_sound(self):
        if sound_var == True:
            random_sound = random.randrange(1,5)
            pygame.mixer.music.load('sound_effects/'+str(self.block_type)+''+str(random_sound)+'.wav')
            pygame.mixer.music.play(0)
    


#BUTTONS#
trash = Button('TRASH',768,0,32,32,'other/trash.png')
save = Button('SAVE',704,0,32,32,'other/save.png')
load = Button('LOAD',736,0,32,32,'other/load.png')
play = Button('PLAY',672,0,32,32,'other/play.png')
bg = Button('BG',608,0,32,32,'other/bg.png')
fg = Button('FG',640,0,32,32,'other/fg.png')
helpp = Button('HELPP',544,0,32,32,'other/help.png')
helpp2 = Button('HELPP2',544,0,32,32,'other/help.png')
sound = Button('SOUND',576,0,32,32,'other/sound_on.png')
edit = Button('EDIT',672,0,32,32,'other/edit.png')

exit_button = Button('EXIT',32,0,48,32,'other/exit_button.png')
exit_button2 = Button('EXIT2',32,0,48,32,'other/exit_button.png')




#ALL OBJECTS AND ENTITYS#
player = Entity('player','PLAYER',
                {'up':False,'down':False,'left':False,'right':False,'up_org':False,'down_org':False,'left_org':False,'right_org':False,'ground':False,'jump':False,'sprint':False},
                672,640,None,None,8,64,'texture/player.png')

brick = Object('brick','SOLID',736,128,None,None,32,32,'texture/brick.png')
dirt = Object('dirt','SOLID',768,32,None,None,32,32,'texture/dirt.png')
cactus = Object('cactus','SOLID',704,128,None,None,32,32,'texture/cactus.png')

concrete_white = Object('concrete_white','SOLID',672,160,None,None,32,32,'texture/concrete_white.png')
concrete_light_gray = Object('concrete_light_gray','SOLID',672,192,None,None,32,32,'texture/concrete_light_gray.png')
concrete_gray = Object('concrete_gray','SOLID',672,224,None,None,32,32,'texture/concrete_gray.png')
concrete_black = Object('concrete_black','SOLID',672,256,None,None,32,32,'texture/concrete_black.png')
concrete_red = Object('concrete_red','SOLID',672,288,None,None,32,32,'texture/concrete_red.png')
concrete_orange = Object('concrete_orange','SOLID',672,320,None,None,32,32,'texture/concrete_orange.png')
concrete_yellow = Object('concrete_yellow','SOLID',672,352,None,None,32,32,'texture/concrete_yellow.png')
concrete_light_green = Object('concrete_light_green','SOLID',672,384,None,None,32,32,'texture/concrete_light_green.png')
concrete_green = Object('concrete_green','SOLID',672,416,None,None,32,32,'texture/concrete_green.png')
concrete_light_blue = Object('concrete_light_blue','SOLID',672,448,None,None,32,32,'texture/concrete_light_blue.png')
concrete_cyan = Object('concrete_cyan','SOLID',672,480,None,None,32,32,'texture/concrete_cyan.png')
concrete_blue = Object('concrete_blue','SOLID',672,512,None,None,32,32,'texture/concrete_blue.png')
concrete_purple = Object('concrete_purple','SOLID',672,544,None,None,32,32,'texture/concrete_purple.png')
concrete_magenta = Object('concrete_magenta','SOLID',672,576,None,None,32,32,'texture/concrete_magenta.png')
concrete_pink = Object('concrete_pink','SOLID',672,608,None,None,32,32,'texture/concrete_pink.png')

grass = Object('grass','SOLID',736,32,None,None,32,32,'texture/grass.png')

glass = Object('glass','SOLID',768,128,None,None,32,32,'texture/glass.png')
glass_white = Object('glass_white','SOLID',768,160,None,None,32,32,'texture/glass_white.png')
glass_light_gray = Object('glass_light_gray','SOLID',768,192,None,None,32,32,'texture/glass_light_gray.png')
glass_gray = Object('glass_gray','SOLID',768,224,None,None,32,32,'texture/glass_gray.png')
glass_black = Object('glass_black','SOLID',768,256,None,None,32,32,'texture/glass_black.png')
glass_red = Object('glass_red','SOLID',768,288,None,None,32,32,'texture/glass_red.png')
glass_orange = Object('glass_orange','SOLID',768,320,None,None,32,32,'texture/glass_orange.png')
glass_yellow = Object('glass_yellow','SOLID',768,352,None,None,32,32,'texture/glass_yellow.png')
glass_light_green = Object('glass_light_green','SOLID',768,384,None,None,32,32,'texture/glass_light_green.png')
glass_green = Object('glass_green','SOLID',768,416,None,None,32,32,'texture/glass_green.png')
glass_light_blue = Object('glass_light_blue','SOLID',768,448,None,None,32,32,'texture/glass_light_blue.png')
glass_cyan = Object('glass_cyan','SOLID',768,480,None,None,32,32,'texture/glass_cyan.png')
glass_blue = Object('glass_blue','SOLID',768,512,None,None,32,32,'texture/glass_blue.png')
glass_purple = Object('glass_purple','SOLID',768,544,None,None,32,32,'texture/glass_purple.png')
glass_magenta = Object('glass_magenta','SOLID',768,576,None,None,32,32,'texture/glass_magenta.png')
glass_pink = Object('glass_pink','SOLID',768,608,None,None,32,32,'texture/glass_pink.png')

leaf = Object('leaf','SOLID',672,128,None,None,32,32,'texture/leaf.png')
log_oak = Object('log_oak','SOLID',672,64,None,None,32,32,'texture/log_oak.png')
log_spruce = Object('log_spruce','SOLID',704,64,None,None,32,32,'texture/log_spruce.png')
log_birch = Object('log_birch','SOLID',736,64,None,None,32,32,'texture/log_birch.png')
log_acacia = Object('log_acacia','SOLID',768,64,None,None,32,32,'texture/log_acacia.png')
wood_oak = Object('wood_oak','SOLID',672,96,None,None,32,32,'texture/wood_oak.png')
wood_spruce = Object('wood_spruce','SOLID',704,96,None,None,32,32,'texture/wood_spruce.png')
wood_birch = Object('wood_birch','SOLID',736,96,None,None,32,32,'texture/wood_birch.png')
wood_acacia = Object('wood_acacia','SOLID',768,96,None,None,32,32,'texture/wood_acacia.png')

wool_white = Object('wool_white','SOLID',736,160,None,None,32,32,'texture/wool_white.png')
wool_light_gray = Object('wool_light_gray','SOLID',736,192,None,None,32,32,'texture/wool_light_gray.png')
wool_gray = Object('wool_gray','SOLID',736,224,None,None,32,32,'texture/wool_gray.png')
wool_black = Object('wool_black','SOLID',736,256,None,None,32,32,'texture/wool_black.png')
wool_red = Object('wool_red','SOLID',736,288,None,None,32,32,'texture/wool_red.png')
wool_orange = Object('wool_orange','SOLID',736,320,None,None,32,32,'texture/wool_orange.png')
wool_yellow = Object('wool_yellow','SOLID',736,352,None,None,32,32,'texture/wool_yellow.png')
wool_light_green = Object('wool_light_green','SOLID',736,384,None,None,32,32,'texture/wool_light_green.png')
wool_green = Object('wool_green','SOLID',736,416,None,None,32,32,'texture/wool_green.png')
wool_light_blue = Object('wool_light_blue','SOLID',736,448,None,None,32,32,'texture/wool_light_blue.png')
wool_cyan = Object('wool_cyan','SOLID',736,480,None,None,32,32,'texture/wool_cyan.png')
wool_blue = Object('wool_blue','SOLID',736,512,None,None,32,32,'texture/wool_blue.png')
wool_purple = Object('wool_purple','SOLID',736,544,None,None,32,32,'texture/wool_purple.png')
wool_magenta = Object('wool_magenta','SOLID',736,576,None,None,32,32,'texture/wool_magenta.png')
wool_pink = Object('wool_pink','SOLID',736,608,None,None,32,32,'texture/wool_pink.png')

flower_white = Object('flower_white','PASS',704,640,None,None,32,32,'texture/flower_white.png')
flower_red = Object('flower_red','PASS',736,640,None,None,32,32,'texture/flower_red.png')
flower_orange = Object('flower_orange','PASS',768,640,None,None,32,32,'texture/flower_orange.png')
flower_yellow = Object('flower_yellow','PASS',704,672,None,None,32,32,'texture/flower_yellow.png')
flower_light_blue = Object('flower_light_blue','PASS',736,672,None,None,32,32,'texture/flower_light_blue.png')
flower_purple = Object('flower_purple','PASS',768,672,None,None,32,32,'texture/flower_purple.png')

sand = Object('sand','SOLID',704,32,None,None,32,32,'texture/sand.png')
stone = Object('stone','SOLID',672,32,None,None,32,32,'texture/stone.png')

terracotta_white = Object('terracotta_white','SOLID',704,160,None,None,32,32,'texture/terracotta_white.png')
terracotta_light_gray = Object('terracotta_light_gray','SOLID',704,192,None,None,32,32,'texture/terracotta_light_gray.png')
terracotta_gray = Object('terracotta_gray','SOLID',704,224,None,None,32,32,'texture/terracotta_gray.png')
terracotta_black = Object('terracotta_black','SOLID',704,256,None,None,32,32,'texture/terracotta_black.png')
terracotta_red = Object('terracotta_red','SOLID',704,288,None,None,32,32,'texture/terracotta_red.png')
terracotta_orange = Object('terracotta_orange','SOLID',704,320,None,None,32,32,'texture/terracotta_orange.png')
terracotta_yellow = Object('terracotta_yellow','SOLID',704,352,None,None,32,32,'texture/terracotta_yellow.png')
terracotta_light_green = Object('terracotta_light_green','SOLID',704,384,None,None,32,32,'texture/terracotta_light_green.png')
terracotta_green = Object('terracotta_green','SOLID',704,416,None,None,32,32,'texture/terracotta_green.png')
terracotta_light_blue = Object('terracotta_light_blue','SOLID',704,448,None,None,32,32,'texture/terracotta_light_blue.png')
terracotta_cyan = Object('terracotta_cyan','SOLID',704,480,None,None,32,32,'texture/terracotta_cyan.png')
terracotta_blue = Object('terracotta_blue','SOLID',704,512,None,None,32,32,'texture/terracotta_blue.png')
terracotta_purple = Object('terracotta_purple','SOLID',704,544,None,None,32,32,'texture/terracotta_purple.png')
terracotta_magenta = Object('terracotta_magenta','SOLID',704,576,None,None,32,32,'texture/terracotta_magenta.png')
terracotta_pink = Object('terracotta_pink','SOLID',704,608,None,None,32,32,'texture/terracotta_pink.png')


#CREATES A LIST OF BOTH BUTTONS AND OBJECTS#
buttons = [trash,save,load,play,bg,fg,helpp,sound]

objects = {
    'brick':brick,
    'dirt':dirt,
    'cactus':cactus,
    'concrete_white':concrete_white, 
    'concrete_light_gray':concrete_light_gray, 
    'concrete_gray':concrete_gray,
    'concrete_black':concrete_black, 
    'concrete_red':concrete_red,
    'concrete_orange':concrete_orange,
    'concrete_yellow':concrete_yellow,
    'concrete_light_green':concrete_light_green,
    'concrete_green':concrete_green,
    'concrete_light_blue':concrete_light_blue,
    'concrete_cyan':concrete_cyan,
    'concrete_blue':concrete_blue,
    'concrete_purple':concrete_purple,
    'concrete_magenta':concrete_magenta, 
    'concrete_pink':concrete_pink,
    'flower_white':flower_white, 
    'flower_red':flower_red,
    'flower_orange':flower_orange,
    'flower_yellow':flower_yellow,
    'flower_light_blue':flower_light_blue,
    'flower_purple':flower_purple,
    'grass':grass, 
    'glass':glass,
    'glass_white':glass_white, 
    'glass_light_gray':glass_light_gray,
    'glass_gray':glass_gray,
    'glass_black':glass_black,
    'glass_red':glass_red,
    'glass_orange':glass_orange,
    'glass_yellow':glass_yellow, 
    'glass_light_green':glass_light_green, 
    'glass_green':glass_green,
    'glass_light_blue':glass_light_blue,
    'glass_cyan':glass_cyan,
    'glass_blue':glass_blue, 
    'glass_purple':glass_purple,
    'glass_magenta':glass_magenta, 
    'glass_pink':glass_pink, 
    'leaf':leaf, 
    'log_oak':log_oak, 
    'log_spruce':log_spruce, 
    'log_birch':log_birch,
    'log_acacia':log_acacia,
    'sand':sand,
    'stone':stone, 
    'terracotta_white':terracotta_white, 
    'terracotta_light_gray':terracotta_light_gray, 
    'terracotta_gray':terracotta_gray,
    'terracotta_black':terracotta_black,
    'terracotta_red':terracotta_red,
    'terracotta_orange':terracotta_orange,
    'terracotta_yellow':terracotta_yellow,
    'terracotta_light_green':terracotta_light_green,
    'terracotta_green':terracotta_green,
    'terracotta_light_blue':terracotta_light_blue,
    'terracotta_cyan':terracotta_cyan,
    'terracotta_blue':terracotta_blue,
    'terracotta_purple':terracotta_purple,
    'terracotta_magenta':terracotta_magenta,
    'terracotta_pink':terracotta_pink,
    'wool_white':wool_white, 
    'wool_light_gray':wool_light_gray,
    'wool_gray':wool_gray,
    'wool_black':wool_black,
    'wool_red':wool_red,
    'wool_orange':wool_orange,
    'wool_yellow':wool_yellow,
    'wool_light_green':wool_light_green,
    'wool_green':wool_green,
    'wool_light_blue':wool_light_blue,
    'wool_cyan':wool_cyan,
    'wool_blue':wool_blue, 
    'wool_purple':wool_purple,
    'wool_magenta':wool_magenta,
    'wool_pink':wool_pink,
    'wood_oak':wood_oak,
    'wood_spruce':wood_spruce,
    'wood_birch':wood_birch,
    'wood_acacia':wood_acacia,
    'player':player
    }

#essential things used#
click = {'choice':grass,'place':False,'destroy':False,'collide':False} #used for clicking#
scroll = {'up':False,'down':False,'left':False,'right':False,'x':0,'y':0} #used for camera#
grid = {'x':[],'y':[]} #used for placing blocks#

#other images#
sky = pygame.image.load('other/sky.png').convert_alpha()
block_select = pygame.image.load('texture/block_select.png')

grid_img = pygame.image.load('other/grid.png').convert_alpha()
grid_block_img = pygame.image.load('other/grid_block.png').convert_alpha()

button_menu = pygame.image.load('other/button_menu.png').convert_alpha()
object_menu_pic = pygame.image.load('other/object_menu_pic.png').convert_alpha()

instructions_img = pygame.image.load('other/instructions.png').convert_alpha()
instructions2_img = pygame.image.load('other/instructions2.png').convert_alpha()



#creates a dictionary of 441 seperate chunks, where entitys get appended to#
#did this along with entitys_cords (explained below) to reduce lag for huge levels#

entitys = {'...':'...'}
for x in range(21):
    for y in range(21):
        entitys[str(x)+ ',' +str(y)] = []
del entitys['...']



def entitys_cords_function(x_value,y_value,value):
    global entitys_cords
    #creates a list of the chunk the scroll (editor), or player (game) is and 1 chunk above in all directions#
    entitys_cords = [] 
    for x in range(3):
        for y in range(3):
            x_render = int((x_value * value) / 672)-1 + x ; y_render = int((y_value * value) / 672)-1 + y
            if x_render > -1 and y_render > -1:
                temp1 = (int(((x_value * value) / 672)-1 + x)) ; temp2 = (int(((y_value * value) / 672)-1 +y))
                entitys_cords.append(entitys[str(temp1)+','+str(temp2)])



def pos_chunk_function_editor():
    global pos_chunk_x, pos_chunk_y, pos_round_x, pos_round_y, pos_, scroll
    pos_chunk_x = int((pos_[0] - scroll['x']) / 672)
    pos_chunk_y = int((pos_[1] - scroll['y']-32) / 672)

    pos_round_x = int((pos_[0]-scroll['x']) / 32) ; pos_round_x = pos_round_x * 32
    pos_round_y = int((pos_[1]-scroll['y']-32) / 32) ; pos_round_y = pos_round_y * 32



def pos_chunk_function_game():
    global pos_chunk_x, pos_chunk_y, player_value, pos_chunk_x2, pos_chunk_y2, player_value2, pos_chunk2_x2, pos_chunk2_y2
    pos_chunk_x = int((player_value.x) / 672) ;  pos_chunk_x2 = int((player_value2.x) / 672)
    pos_chunk_y = int((player_value.y+64) / 672) ;  pos_chunk_y2 = int((player_value2.y+64) / 672)

    pos_round_x = (int(player_value.x / 32) * 32)
    pos_round_y = (int(player_value.y / 32) * 32)

    print (pos_chunk_y2)
    if player_value.x - pos_round_x < 16:
        pos_chunk_x2 = int((player_value2.x-32) / 672)

    else:
        pos_chunk_x2 = int((player_value2.x+32) / 672)

    if player_value.y - pos_round_y < 16:
        pos_chunk_y2 = int((player_value2.y-32) / 672)

    else:
        pos_chunk_y2 = int((player_value2.y+32) / 672)

    

    
    


def instructions(img,location):
    global scroll
    pos_ = (0,0)
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                pos_ = position
                
        if pygame.Rect(pos_[0],pos_[1],1,1).colliderect(pygame.Rect(exit_button.x ,exit_button.y,exit_button.width,exit_button.height)):
            if location == 'EDITOR':
                exit_button.press()
            if location == 'GAME':
                break

        screen['display'].fill((255,255,255))
        screen['display'].blit(img,(0,32))
        screen['display'].blit(button_menu,(0,0))
        screen['display'].blit(exit_button.image,(exit_button.x,exit_button.y))
        pygame.display.update()
        screen['fps'].tick_busy_loop(60)

            
def editor():
    object_menu = pygame.Rect(672,32,132,673)
    buttons = [trash,save,load,play,bg,fg,helpp,sound]
    global place,grass,player,grid,clock,scroll,click,grid,entitys,pos_,entitys_cords,objects, sound_var,player_value
    #creates a list of cordinates on the grid#
    for x in range(int((screen['x_end']/32))): 
        grid['x'].append((x * 32)) 
    for y in range(int((screen['y_end']/32))):
        grid['y'].append((y * 32))
  
    while True:
        #used for sound#
        if sound_var != True:
            pygame.mixer.pause()
            pygame.mixer.music.pause()
        else:
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()

            
        entitys_cords_function(scroll['x'],scroll['y'],-1)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == 273 or event.key == K_w: #up#
                    scroll['up'] = True
                if event.key == 274 or event.key == K_s: #down#
                    scroll['down'] = True
                if event.key == 275 or event.key == K_d: #right#
                    scroll['right'] = True
                if event.key == 276 or event.key == K_a: #left#
                    scroll['left'] = True
                    
            if event.type == pygame.KEYUP:
                if event.key == 273 or event.key == K_w: #up#
                    scroll['up'] = False
                if event.key == 274 or event.key == K_s: #down#
                    scroll['down'] = False
                if event.key == 275 or event.key == K_d: #right#
                    scroll['right'] = False
                if event.key == 276 or event.key == K_a: #left#
                    scroll['left'] = False
                    


            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                pos_ = position

                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for value in buttons: #presses buttons#
                    if pygame.Rect(position[0],position[1],1,1).colliderect(pygame.Rect(value.x ,value.y,value.width,value.height)):
                        value.press()

                    
                if position[0] > 672 or position[1] > 706 or position[0] < 0 or position[1] < 33: #checks if the player is outside the editor area, if so it makes values false#
                    click['place'] = False
                    click['destroy'] = False


                if event.button == 3: #if they right click#
                    if position[0] > 672 or position[1] > 706 or position[0] < 0 or position[1] < 33: #checks if the player is outside the editor area, if so it makes values false#
                        pass
                    else:
                        click['place'] = True     
                    for value in objects:
                        if pygame.Rect(position[0],position[1],1,1).colliderect(pygame.Rect(eval(value).invx ,eval(value).invy,32,32)): #makes whatever the player selects their choice#
                            click['choice'] = eval(value)
                            
                        
                if event.button == 1:
                    click['place'] = False #if they left click#
                    click['destroy'] = True


            if event.type == pygame.MOUSEBUTTONUP: #if mouse button is up, cancel both#
                click['place'] = False ; click['destroy'] = False

                
        #scrolling#
        if scroll['up'] == True: 
            scroll['y'] += 32
            if scroll['y'] + screen['y_end'] > screen['y_end']:
                scroll['y'] -= 32
     
        if scroll['down'] == True: 
            scroll['y'] -= 32
            if scroll['y']+ screen['y_end'] < screen['y_display']:
                scroll['y'] += 32

        if scroll['right'] == True:
            scroll['x'] -= 32
            if scroll['x'] + screen['x_end'] < screen['x_display']:
                scroll['x'] += 32
        
        if scroll['left'] == True:
            scroll['x'] += 32
            if scroll['x'] + screen['x_end'] > screen['x_end']:
                scroll['x'] -= 32
                

            

        #sets the x and y values of the selected block#
        for x in grid['x']:
            if pos_[0] < (x + 32):
                for value in objects:
                    eval(value).x = grid['x'][int((x / 32))]-scroll['x']
                break
            
        for y in grid['y']:
            if pos_[1] < (y + 32):
                for value in objects:
                    eval(value).y = grid['y'][int((y / 32))]-scroll['y']-32
                break


            
        if click['place'] == True:
            click['collide'] = False
            pos_chunk_function_editor()
            
            for value in entitys[str(pos_chunk_x)+','+str(pos_chunk_y)]:
                if pygame.Rect(pos_[0]-scroll['x'],pos_[1]-scroll['y'],1,1).colliderect(pygame.Rect(value.x,value.y+32,32,32)):
                    click['collide'] = True
                    break
                else:
                    pass
                        
            #if there isn't already a block in certain location, add a block#
            if click['collide'] != True:
                if click['choice'].x >= 0 and click['choice'].x < 672 - scroll['x'] and click['choice'].y >= 0 and click['choice'].y < 672 - scroll['y']:
                    if click['choice'].name == 'player' and player_value == None:
                        player_value = value
                        entitys[str(pos_chunk_x)+','+str(pos_chunk_y)].append(copy.copy(click['choice']))
                        click['choice'].play_sound()
                    if click['choice'].name != 'player':
                        entitys[str(pos_chunk_x)+','+str(pos_chunk_y)].append(copy.copy(click['choice']))
                        click['choice'].play_sound()
                        
        if click['destroy'] == True:
            pos_chunk_function_editor()
            temp_list = entitys[str(pos_chunk_x)+','+str(pos_chunk_y)]
            
            for value in entitys[str(pos_chunk_x)+','+str(pos_chunk_y)]:
                if value.x + scroll['x'] > 671 or value.x + scroll['x'] < 0 or value.y + scroll['y'] > 671 or value.y + scroll['y'] < 0:
                    pass
                else:
                    if pygame.Rect(pos_[0]-scroll['x'],pos_[1]-scroll['y']-32,0,0).colliderect(pygame.Rect(value.x,value.y,32,32)): #if mouse doesn't collide with block, dont destroy it#
                        if value.name == 'player':
                            player_value = None
                        entitys[str(pos_chunk_x)+','+str(pos_chunk_y)].remove(value)
                        value.play_sound()
                
            entitys[str(pos_chunk_x)+','+str(pos_chunk_y)] = temp_list
            
        screen['display'].blit(sky,(0,32))

        for value in entitys_cords:
            for value2 in value:
                if value2.x + scroll['x'] > 671 or value2.x + scroll['x'] < 0 or value2.y + scroll['y'] > 671 or value2.y + scroll['y'] < 0:
                    pass
                else:
                    offset_var = 0
                    if value2.name == 'player':
                        offset_var = -12
                    if value2.typee != 'PASS':
                        screen['display'].blit(value2.image ,(value2.x + scroll['x'] + offset_var, value2.y + scroll['y']+32))
                    if value2.typee == 'PASS':
                        screen['display'].blit(value2.image_transparent,(value2.x + scroll['x'] + offset_var, value2.y + scroll['y']+32))


                
        screen['display'].blit(grid_img, (0,32))
        screen['display'].blit(object_menu_pic, (672,32))
        screen['display'].blit(button_menu,(0,0))



        for value in objects:
            screen['display'].blit(eval(value).image ,(eval(value).invx, eval(value).invy)) #displays objects in the object menu#
        for value in buttons:
            screen['display'].blit(value.image ,(value.x, value.y)) #displays buttons#

        if pos_[1] < 32 or pos_[0] > 671: #if mouse is in editor, display image that follows the mouse#
            pass
        else:
            offset_var = 0
            if click['choice'].name == 'player':
                offset_var = -12
            screen['display'].blit(click['choice'].image ,(click['choice'].x + scroll['x'] + offset_var, click['choice'].y + scroll['y']+32))

        screen['display'].blit(grid_block_img, (672 ,32))
        screen['display'].blit(block_select, (click['choice'].invx, click['choice'].invy))
        fps = font.render(str(int(screen['fps'].get_fps()))+ ' FPS', True, pygame.Color('black'))

        
        pos_x = font.render('X: ' +str((int(pos_[0]/32)*32)-scroll['x'])+ '/' +str(screen['x_end']), True, pygame.Color('black'))
        pos_y = font.render('Y: ' +str((int((pos_[1]-32)/32)*32)-scroll['y'])+ '/' +str(screen['y_end']), True, pygame.Color('black'))

        
        screen['display'].blit(fps, (10,8))
        screen['display'].blit(pos_x, (178,8))
        screen['display'].blit(pos_y, (346,8))
        
        pygame.display.update()
        screen['fps'].tick_busy_loop(60)
                
def player_input(player_value):
    global event, scroll, org_y, gravity_var, player, bypass, player_value2
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                player.move['sprint'] = True
            if event.key == K_a or event.key == K_LEFT:
                player.move['left'] = True ; player.move['left_org'] = True
            if event.key == K_d or event.key == K_RIGHT:
                player.move['right'] = True ; player.move['right_org'] = True
            if event.key == K_SPACE:
                if player.move['jump'] != True:
                    if player.move['ground'] == True: #if the player is on the ground, then allow them to jump if not, do nothing#
                        gravity_var = False
                        player.move['jump'] = True
                        player.move['ground'] = False
                        org_y = player_value.y
                        player_value2 = copy.copy(player_value)
            player_value2.update()
            
        if event.type == pygame.KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                player.move['sprint'] = False
            if event.key == K_a or event.key == K_LEFT:
                player.move['left'] = False ; player.move['left_org'] = False
                scroll['left'] = False
            if event.key == K_d or event.key == K_RIGHT:
                player.move['right'] = False ; player.move['right_org'] = False
                scroll['right'] = False
            player_value2.update()
    except:
        pass
    
def scroll_center():
    global scroll, player_value2, player_value
    scroll['x'] = 384 - player_value.x 
    scroll['y'] = 320 - player_value.y

def collision_detection(value_collision):
    global player_value2, temp_gravity_var, temp_gravity_value,gravity_var,player,temp_collide_value, temp_lr_collide,temp_l_collide, temp_r_collide, player_value
    
    if pygame.Rect(player_value2.x,player_value2.y+8,player_value2.width,player_value2.height).colliderect(
        pygame.Rect(value_collision.x,value_collision.y,value_collision.width,value_collision.height)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_gravity_var = value_collision
        temp_gravity_value = True
        player.move['ground'] = True
        gravity_var = False
        
    if pygame.Rect(player_value2.x,player_value2.y,player_value2.width,player_value2.height+8).colliderect(
        pygame.Rect(value_collision.x,value_collision.y+value_collision.height,value_collision.width,-1)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        player.move['jump'] = False
        gravity_var = True

    if pygame.Rect(player_value2.x+8,player_value2.y,player_value2.width,player_value2.height).colliderect(
        pygame.Rect(value_collision.x,value_collision.y,value_collision.width,value_collision.height)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_r_collide = ((player_value2.x+player_value2.width)-value_collision.x)
        
    if pygame.Rect(player_value2.x-8,player_value2.y,player_value2.width,player_value2.height).colliderect(
        pygame.Rect(value_collision.x,value_collision.y,value_collision.width,value_collision.height)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_l_collide = ((player_value2.x)-(value_collision.x+value_collision.width))
        
    if pygame.Rect(player_value2.x+1,player_value2.y,player_value2.width,player_value2.height).colliderect(
        pygame.Rect(value_collision.x,value_collision.y,value_collision.width,value_collision.height)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_r_collide = True

    if pygame.Rect(player_value2.x-1,player_value2.y,player_value2.width,player_value2.height).colliderect(
        pygame.Rect(value_collision.x,value_collision.y,value_collision.width,value_collision.height)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_l_collide = True

    #might not be 100% smooth looking, but something i put in last minuite to correct the y value for a specific glitch i found#
    if pygame.Rect(player_value.x,player_value.y,player_value.width,player_value.height).colliderect(
        pygame.Rect(value_collision.x+3,value_collision.y+3,value_collision.width-3,value_collision.height-3)) and value_collision.typee == 'SOLID' and value_collision.name != 'player':
        temp_y = player_value2.y / 32 ; temp_y = int(temp_y) ; temp_y = temp_y * 32
        player_value2.y = temp_y
        
def game():
    global event, scroll, org_y, gravity_var, entitys, player_pass, player_value, value2, temp_collide, temp_value, gravity_var, player, pos_chunk_x2, pos_chunk_y2, player_value2
    global temp_gravity_var, temp_gravity_value, temp_list, temp_list2, temp_l_collide, temp_r_collide, temp_collide_value

    buttons = [edit,helpp2,sound]
    
    player_value = player_pass
    entitys_cords_function(scroll['x'],scroll['y'],-1)
    player_value2 = copy.copy(player_value)
    gravity_var = True

    while True:
        
        if sound_var != True:
            pygame.mixer.pause()
            pygame.mixer.music.pause()
        else:
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()
            
        entitys_cords_function(player_value2.x,player_value2.y,1)
        pos_chunk_function_game()
        
        temp_list = entitys[str(pos_chunk_x)+','+str(pos_chunk_y)]
        temp_list2 = entitys[str(pos_chunk_x2)+','+str(pos_chunk_y2)]
        
        screen['display'].blit(sky,(0,32))
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player_input(player_value)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                for value in buttons: #presses buttons#
                    if pygame.Rect(position[0],position[1],1,1).colliderect(pygame.Rect(value.x ,value.y,value.width,value.height)):
                        value.press()
                        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        temp_collide_value = False
        temp_gravity_value = False
        temp_l_collide = False
        temp_r_collide = False
        player.move['ground'] = False
        player.move['left'] = player.move['left_org']
        player.move['right'] = player.move['right_org']

        if player.move['jump'] != True:
            gravity_var = True
            
        for value_2 in temp_list:
            collision_detection(value_2)
                
        for value_2 in temp_list2:
            collision_detection(value_2)

        if temp_l_collide != True:
            if player.move['left'] == True:
                if temp_l_collide != False:
                    player_value2.x -= (temp_l_collide)
                else:
                    player_value2.x -= 4
                    if player.move['sprint'] == True:
                        player_value2.x -= 4

        if temp_r_collide != True:
            if player.move['right'] == True:
                if temp_r_collide != False:
                    player_value2.x -= (temp_r_collide)
                else:
                    player_value2.x += 4
                    if player.move['sprint'] == True:
                        player_value2.x += 4

        if gravity_var == True:
            if temp_gravity_value == True:
                player_value2.y += ((player_value2.y + player_value2.height) - temp_gravity_var.y)
            else:
                player_value2.y += 8

                                
        if temp_collide_value != True:
            player_value = copy.copy(player_value2)



        if player.move['jump'] == True:
            if org_y > player_value2.y + 116: #if player reaches a certain height then stop#
                player_value2.y = int(player_value2.y)
                gravity_var = True
                player.move['jump'] = False
                player.move['ground'] = False
                
            else:
                gravity_var = False
                player_value2.y -= 8 ; player_value2.y = round((player_value2.y),2) #rounded because python no like math, and gave me wonky numbers#
            

        scroll_center()



        for value in entitys_cords:
            for value2 in value:
                if value2.x + scroll['x'] < -64 or value2.x + scroll['x'] > 800 or value2.y + scroll['y'] < -64 or value2.y + scroll['y'] > 704:
                    pass
                
                else:
                    if value2.name != 'player':
                        screen['display'].blit(value2.image ,(value2.x + scroll['x'], value2.y + scroll['y']+32))

                        
        screen['display'].blit(player_value.image ,(player_value.x + scroll['x']-12, player_value.y + scroll['y']+32))
        
        fps = font.render(str(int(screen['fps'].get_fps()))+ ' FPS', True, pygame.Color('black'))
        pos_x = font.render('X: ' +str(player_value2.x)+ '/' +str(screen['x_end']), True, pygame.Color('black'))
        pos_y = font.render('Y: ' +str(player_value2.y)+ '/' +str(screen['y_end']), True, pygame.Color('black'))

        
        screen['display'].blit(button_menu,(0,0))
        for value in buttons:
            screen['display'].blit(value.image,(value.x,value.y))
            
        screen['display'].blit(pos_x, (178,8))
        screen['display'].blit(pos_y, (346,8))
        screen['display'].blit(fps, (10,8))
        
        pygame.display.update()
        screen['fps'].tick_busy_loop(60)
        
editor()
