import random
import math
import sys

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
     }

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5,
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3,
        }

cannon = {'shortform': 'CANON',
          'name': 'Cannon',
          'maxHP': 8,
          'min_damage': 3,
          'max_damage': 5,
          'price': 7,
          'active': True
          }

zombie = {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          }

werewolf = {'shortform': 'WWOLF',
            'name': 'Werewolf',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 4,
            'moves' : 2,
            'reward': 3
            }

skeleton = {'shortform': 'SKELE',
            'name': 'Skeleton',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 3,
            'moves' : 1,
            'reward': 2
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None], 
          [None, None, None, None, None, None, None] ]

unit_list = [archer,wall,cannon]
monster_list = [zombie,werewolf,skeleton]
limit = 3                                    
  
#----------------------------------------------------------------------
# draw_field(field)
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#    in the first 3 columns
#----------------------------------------------------------------------

def draw_field(field,limit):
    print()
    num_columns = len(field[0])
    char = 65
    # prints the number for the valid columns
    for i in range(limit):
        if i == 0:
            print(' '*3,i+1,end=' '*5)
        else:
            print(i+1,end=' '*5)
    print()
    for row in field:
        print('','+-----'*num_columns +'+',end='')
        print()
        print(chr(char),end='')
        char += 1

        for i in row:
            if i == None:
                print('|',end='     ')
            else:
                print('|{:^5}'.format(i[0]),end='')
        print('|',end='')
        print()
        print(' ',end='')

        for j in row:
            if j == None:
                print('|',end='     ')
            else:
                print('|{:>2}/{:^2}'.format(j[1],j[2]),end='')
        print('|')
    print('','+-----'*num_columns +'+',end='\n')

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu():
    print()
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")
    
#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print()
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#----------------------------
# show_units_menu()
#
#    Displays the units menu
#----------------------------

def show_units_menu(unit_list):
    print()
    print('What unit do you wish to buy?')
    for i in range(len(unit_list)):
        print('{}. {} ({} gold)'.format(i+1,(unit_list[i])['name'],(unit_list[i])['price']))
    print("{}. Don't buy".format(len(unit_list)+1))

#------------------------------------------------------------------------------------
# update_game_vars()
#
#   After each turn:
#   - gold increases by 1
#   - turn increases by 1
#   - threat increases by a random number between 1 and the danger level, inclusive.
#------------------------------------------------------------------------------------

def update_game_vars(game_vars):
    game_vars['turn'] += 1
    if game_vars['turn'] > 1:
        game_vars['gold'] += 1
        threat_amount = random.randint(1,game_vars.get('danger_level'))
        game_vars['threat'] += threat_amount

#----------------------------
# show_current_turn_info()
# 
#   shows the 
#   - Turn number
#   - Threat Metre
#   - Number of gold left
#   - Danger level
#   - No. of Monsters killed
#----------------------------

def show_current_turn_info(game_vars):
    print('''Turn  {}     Threat = [{}]             Danger Level {}
Gold = {}    Monsters killed = {}/{}'''.format(game_vars.get('turn'),game_vars.get('threat')*'-',game_vars.get('danger_level'),game_vars.get('gold'),game_vars.get('monsters_killed'),game_vars.get('monster_kill_target')))
    
#-------------------------------------------------------------------
# buy_and_place_unit()
#
#    Allows player to buy a unit and place it 
#    Places a unit at the given position
#    Asks the user to give another input if the position is invalid
#
#    Position is invalid if 
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#
#-------------------------------------------------------------------
def buy_and_place_unit(field,unit_list,game_vars,limit):
    while True:

        while True:
            try:
                unit_choice = int(input('Your choice? '))
                break
            except ValueError:
                print('Enter a number please!!!')

        if unit_choice <= len(unit_list):
            if game_vars['gold'] < (unit_list[unit_choice-1])['price']:
                print()
                print('You only have {} gold'.format(game_vars['gold']))
                print('You do not have enough gold to purchase {}!!!'.format((unit_list[unit_choice-1])['name']))
                print()
                for i in range(len(unit_list)):
                    print('{}. {} ({} gold)'.format(i+1,(unit_list[i])['name'],(unit_list[i])['price']))
                print("{}. Don't buy".format(len(unit_list)+1)) 
            else:
                game_vars['gold'] -= (unit_list[unit_choice-1])['price']
                print()
                print('You have successfully bought {}'.format((unit_list[unit_choice-1])['name']))
                print('You have a remaining of {} gold now'.format(game_vars['gold']))   
                
                while True:
                    print()
                    position = input('Where do you want to place the {}? '.format((unit_list[unit_choice-1])['name']))
                    if len(position) == 2 and position[0].isalpha() and position[1].isdigit():
                        position = position.capitalize()
                        row = ord(position[0]) - 65
                        column = int(position[1])-1
                        if (row+1) > len(field):
                            print('''Position is not on the field of play!!!''')
                        elif column >= limit:
                            print('You cannot place the {} past the first {} columns!!!'.format((unit_list[unit_choice-1])['name'],limit))
                        elif field[row][column] != None:
                            print('Position is occupied!!!')  
                        else:
                            field[row][column] = [(unit_list[unit_choice-1])['shortform'],(unit_list[unit_choice-1])['maxHP'],(unit_list[unit_choice-1])['maxHP'],(unit_list[unit_choice-1]).get('active')]  
                            break               
                    else:
                        print('Type the position in the correct format e.g D1')
                return game_vars, field             
        elif unit_choice == (len(unit_list)+1):
            print()
            print('No units are bought')
            break
        else:
            print('Enter a number from 1 to 3')
            
        
#-----------------------------------------------------------------
# archer_attack()
#
#    - archer unit attacks.
#    - archer can only hit one monster 
#    - archer can only shoot from left to right
#    - if health of monster goes below or equal to 0, monster dies
#
#-----------------------------------------------------------------
 
def archer_attack(field,row,game_vars,monster_list):
    for i in range(len(row)):
        if row[i] == None: pass
        elif row[i][0] == archer['shortform']:
            first_monster = False
            # Searches for monster after the position of the archer
            for j in range(len(row)-len(row[:i+1])):
                if first_monster == True: continue
                elif row[j+i+1] != None: 
                    for monster in monster_list:
                        if row[j+i+1] == None: pass
                        elif row[j+i+1][0] == monster['shortform']:
                            # makes sure that archer attack 1 monster at a time
                            first_monster = True
                            # Skeleton takes half damage
                            if monster['shortform'] == 'SKELE':
                                 damage_on_monster = (random.randint(archer['min_damage'],archer['max_damage']))
                                 row[j+i+1][1] -= math.ceil(damage_on_monster/2)
                                 print('{} in lane {} shoots {} for {} damage!'.format(archer['name'],chr(field.index(row)+65),monster['name'],damage_on_monster))
                                 if damage_on_monster == 1: pass
                                 else:print('{} takes only {} damage instead of {} damage'.format(monster['name'],math.ceil(damage_on_monster/2),damage_on_monster))                                    
                            else: 
                                 damage_on_monster = (random.randint(archer['min_damage'],archer['max_damage']))
                                 row[j+i+1][1] -= damage_on_monster
                                 print('{} in lane {} shoots {} for {} damage!'.format(archer['name'],chr(field.index(row)+65),monster['name'],damage_on_monster))      
                            if row[j+i+1][1] <= 0:
                                row[j+i+1] = None
                                print('{} dies'.format(monster['name']))
                                game_vars['gold'] += monster['reward']
                                print('You gain {} gold as a reward.'.format(monster['reward']))
                                game_vars['monsters_killed'] += 1
                                game_vars['threat'] += monster['reward']
                                if game_vars['monsters_killed'] >= 20:
                                    print('You have protected the city! You win!')
                                    sys.exit()
                                game_vars['num_monsters'] -= 1
                                     
#-----------------------------------------------------------------
# cannon_attack()
#
#    - cannon unit attacks every other turn
#    - cannon can only hit one monster 
#    - cannon can only shoot from left to right
#    - cannon has 50% chance to push monster back
#    - if health of monster goes below or equal to 0, monster dies
#
#-----------------------------------------------------------------

def cannon_attack(field,row,game_vars,monster_list):
    for i in range(len(row)):
        if row[i] == None: pass
        elif row[i][0] == cannon['shortform'] and row[i][3] == False:
            row[i][3] = True
        elif row[i][0] == cannon['shortform'] and row[i][3] == True:
            row[i][3] = False
            first_monster = False

            # Searches for monster after the position of the archer
            for j in range(len(row)-len(row[:i+1])):
                if first_monster == True: continue
                elif row[j+i+1] != None: 
                    for monster in monster_list:
                        if row[j+i+1] == None: pass
                        elif row[j+i+1][0] == monster['shortform']:
                            # makes sure that cannon attack 1 monster at a time
                            first_monster = True
                            damage_on_monster = (random.randint(cannon['min_damage'],cannon['max_damage']))
                            row[j+i+1][1] -= damage_on_monster
                            print('{} in lane {} shoots {} for {} damage!'.format(cannon['name'],chr(field.index(row)+65),monster['name'],damage_on_monster))  
                            if row[j+i+1] == None: pass
                            elif row[j+i+1][1] <= 0:
                                row[j+i+1] = None
                                print('{} dies'.format(monster['name']))
                                game_vars['gold'] += monster['reward']
                                print('You gain {} gold as a reward.'.format(monster['reward']))
                                game_vars['monsters_killed'] += 1
                                game_vars['threat'] += monster['reward']
                                if game_vars['monsters_killed'] >= 20:
                                    print('You have protected the city! You win!')
                                    sys.exit()
                                game_vars['num_monsters'] -= 1
                                break
                            push = random.choice([True, False])
                            if push == True:
                                if (j+i+1)+1 >= (len(row)-1): pass
                                elif row[(j+i+1)+1] == None:
                                    row[(j+i+1)+1] = row[j+i+1]
                                    row[j+i+1] = None
                                    print('{} in lane {} pushed {} backwards by 1 square'.format(cannon['name'],chr(field.index(row)+65),monster['name']))

#-------------------------------------------------------------
# monster_advance()
#
#       - If there is nothing in front of monster, it advances
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#       - Skeleton and Zombie has 1 action but Werewolf has 2
#-------------------------------------------------------------

def monster_advance(field,row,monster_list,unit_list):
    for i in range(len(row)):
        for monster in monster_list:
            if row[i] == None: pass
            elif row[i][0] == monster['shortform']:

                position = i
                # checks if user lost the game
                if position == 1 and (monster)['shortform'] == 'WWOLF' and row[position-1] == None:
                    print('{} in lane {} advances!'.format(monster['name'],chr(field.index(row)+65)))    
                if position == 0 or (position == 1 and monster['shortform'] == 'WWOLF' and row[position-1] == None):
                    print('A {} has reached the city! All is lost!'.format(monster['name']))
                    print('You have lost the game. :(') 
                    sys.exit()

                no_of_actions = monster['moves']
                for action in range(no_of_actions):
                    for unit in unit_list:
                        # monster moves
                        if row[position-1] == None:
                            row[position-1] = row[position]
                            row[position] = None
                            print('{} in lane {} advances!'.format(monster['name'],chr(field.index(row)+65)))
                            position -= 1
                            break
                        # monster attacks unit
                        elif row[position-1][0] == unit['shortform']:
                            damage_on_unit = random.randint(monster['min_damage'],(monster['max_damage']))
                            row[position-1][1] -= damage_on_unit
                            print('{} in lane {} hits {} for {} damage'.format(monster['name'],chr(field.index(row)+65),unit['name'],damage_on_unit))                
                            if row[position-1][1] <= 0:
                                row[position-1] = None
                                print('{} dies'.format(unit['name']))
                            break
                        # monster gets blocked by another monster
                        elif row[position-1][0] == 'ZOMBI' or row[position-1][0] == 'SKELE' or row[position-1][0] == 'WWOLF':
                            print('{} is blocked from from advancing'.format(monster['name']))
                            break

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Spawns monster if there are 0 monsters in field
#---------------------------------------------------------------------
def spawn_monster(field, game_vars,monster_list):
    if game_vars['num_monsters'] == 0:
        monster = monster_list[random.randrange(len(monster_list))]
        field[random.randrange(len(field))][-1] = [monster['shortform'],monster['maxHP'],monster['maxHP'], None]
        game_vars['num_monsters'] += 1
    return field

#--------------------------------------------------------------------------------------
# threat_metre()
#
#    The threat metre that contains 10 spaces and shows the current threat amount.
#    When it fills up, a new monster is spawned and the threat amount is reduced by 10. 
#    
#--------------------------------------------------------------------------------------
def threat_metre(field,game_vars):
    if game_vars['threat'] >= game_vars['max_threat']:
        for i in range(1, game_vars['threat']+1):
            if i % 10 == 0:
                game_vars['threat'] -= 10
                monster = monster_list[random.randrange(len(monster_list))]
                field[random.randrange(len(field))][-1] = [monster['shortform'],monster['maxHP'],monster['maxHP'], None]
                game_vars['num_monsters'] += 1
    return field

#--------------------------------------------------------------------------------------------
# danger_level()
#
#     - Every 12 turns, the danger level is increased by 1. 
#     - This causes the minimum damage, maximum damage, maximum hit points and reward for all 
#       monsters to increase by 1.
#--------------------------------------------------------------------------------------------
def danger_level(game_vars,field,monster_list):
    if game_vars['turn'] == 0:pass 
    elif (game_vars['turn'])%12 == 0:
        game_vars['danger_level'] += 1
        for row in field:
            for i in range(len(row)):
                for j in range(len(monster_list)):
                    if row[i] == None:pass 
                    elif row[i][0] == (monster_list[j])['shortform']:
                        row[i][2] += 1
        for monster in monster_list:
            monster['maxHP'] += 1
            monster['min_damage'] += 1
            monster['max_damage'] += 1
            monster['reward'] += 1
    return field

#-------------------------------------------------------------------------
# save_game()
#
#    Saves the important data in a text file called 'game.txt'
#    Important data are
#      - index of monster and archer
#      - current HP, max HP, of monster and archer
#      - game variables 
#      - information of monster like the max damage, min damage and reward
#-------------------------------------------------------------------------

def save_game(field,game_vars,monster_list):
    game_file = open('game.txt', 'w')
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != None:
                game_file.write(str(i)+' ')                 # row of the monster/unit
                game_file.write(str(j)+' ')                 # column of the monster/unit
                game_file.write(field[i][j][0]+' ')         # shortform of the monster/unit
                game_file.write(str(field[i][j][1])+' ')    # current HP of the monster/unit
                game_file.write(str(field[i][j][2])+' ')    # max HP of the monster/unit
                game_file.write(str(field[i][j][3]))        # activeness of the cannon
                game_file.write(',')

    game_file.write('\n')
    for key in game_vars:
        game_file.write(key+':')
        game_file.write(str(game_vars[key])+' ')

    game_file.write('\n')
    for monster in monster_list:
        for key in monster:
            game_file.write(key+':')
            game_file.write(str(monster[key])+' ')
        game_file.write(',')

    game_file.close()
    print()
    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Reads the info from 'game.txt'
#-----------------------------------------
def load_game(field,zombie,werewolf,skeleton):
    new_zombie = {}
    new_werewolf = {}
    new_skeleton = {}
    game_vars = {}

    game_file = open('game.txt','r')
    data = game_file.read()
    data = data.split('\n')

    # game variables
    game_vars_list = data[1]
    game_vars_list = game_vars_list.split(' ')
    for i in game_vars_list:
        i = i.split(':')
        if len(i) < 2:
            pass
        else:
            if i[1].isdigit(): i[1] = int(i[1])
            elif i[1] == 'False': i[1] = False
            elif i[1] == 'True': i[1] = True
            game_vars[i[0]] = i[1]
    
    # monster information 
    monsters_list = data[2]
    monsters_list = monsters_list.split(',')
    monsters_list.remove('')
    for i in range(len(monsters_list)):
        monsters_list[i] = monsters_list[i].split(' ')
    for i in range(len(monsters_list)):
        for j in range(len(monsters_list[i])):
            monsters_list[i][j] = monsters_list[i][j].split(':')
            if len(monsters_list[i][j]) < 2:pass
            else:
                if monsters_list[i][j][1].isdigit():
                    monsters_list[i][j][1] = int(monsters_list[i][j][1])
        monsters_list[i].remove(monsters_list[i][-1])
    for i in range(len(monsters_list)):
        for j in range(len(monsters_list[i])):
            if i == 0: new_zombie[(monsters_list[i][j][0])] = monsters_list[i][j][1]
            elif i == 1: new_werewolf[(monsters_list[i][j][0])] = monsters_list[i][j][1]
            elif i == 2: new_skeleton[(monsters_list[i][j][0])] = monsters_list[i][j][1]

    zombie.update(new_zombie)
    werewolf.update(new_werewolf)
    skeleton.update(new_skeleton)

    # field information
    field_info = data[0]
    field_info = field_info.split(',')
    field_info.remove('')
    for i in range(len(field_info)):
        field_info[i] = field_info[i].split(' ')
        field_info[i][0] = int(field_info[i][0])
        field_info[i][1] = int(field_info[i][1])
        field_info[i][3] = int(field_info[i][3])
        field_info[i][4] = int(field_info[i][4])
        if field_info[i][5] == 'True':
            field_info[i][5] = True
        elif field_info[i][5] == 'False':
            field_info[i][5] = False
        field[field_info[i][0]][field_info[i][1]] = [field_info[i][2],field_info[i][3],field_info[i][4],field_info[i][5]]
   
    game_file.close()
    return field,game_vars
   
#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")

while True:
    show_main_menu()
    while True:
        try:
            main_menu_choice = int(input('Your choice? '))
            break
        except ValueError:
            print('Enter a number please!!!')  
    if main_menu_choice == 2:
        try:
            field,game_vars = load_game(field,zombie,werewolf,skeleton)
        except FileNotFoundError:
            print()
            print('There is no saved game!!!')
            break
    if main_menu_choice == 1 or main_menu_choice == 2:
        while True:
            update_game_vars(game_vars)
            field = danger_level(game_vars,field,monster_list)
            threat_metre(field,game_vars)
            spawn_monster(field,game_vars,monster_list)
            draw_field(field,limit)
            show_current_turn_info(game_vars)
            show_combat_menu()
            while True:
                try:
                    combat_menu_choice = int(input('Your choice? '))
                    break
                except ValueError:
                    print('Enter a number please!!!')
            if combat_menu_choice == 1:
                show_units_menu(unit_list)
                buy_and_place_unit(field,unit_list,game_vars,limit)
                print()
                for row in field:
                    archer_attack(field,row,game_vars,monster_list)
                    cannon_attack(field,row,game_vars,monster_list)
                    monster_advance(field, row, monster_list,unit_list)
            elif combat_menu_choice == 2:
                print()
                for row in field:
                    archer_attack(field,row,game_vars,monster_list)
                    cannon_attack(field,row,game_vars,monster_list)
                    monster_advance(field, row, monster_list,unit_list)
            elif combat_menu_choice == 3:
                save_game(field,game_vars,monster_list)
                sys.exit()
            elif combat_menu_choice == 4:
                print()
                print('See you next time!')
                sys.exit()
            else:
                print('Enter a number between 1 to 4')      
    elif main_menu_choice == 3:
        print()
        print('See you next time!')
        break
    else:
        print('Enter a number between 1 to 3')