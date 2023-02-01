import os
import random
import time

# points for each letter
JETONS_PTS = { 
  "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 10, "L": 1, "M": 2, "N": 1, "O": 1, "P": 3, "Q": 8, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 10, "X": 10, "Y": 10, "Z": 10, "_": 0
} 

# displayed lettres 
TILES = [
  "A₁", "B₃", "C₃", "D₂", "E₁", "F₄", "G₂", "H₄", "I₁", "J₈", "K₊",  
  "L₁", "M₂",
  "N₁", "O₁", "P₃", "Q₈", "R₁", "S₁", "T₁", "U₁", "V₄", "W₊", "X₊", 
  "Y₊", "Z₊",
  "_₀"
]

# all the available letters
LETTERS = [key for key in JETONS_PTS.keys()]

# multipliers on the board
MULTIS = {
  (0, 0): ('m', 3), (0, 7): ('m', 3), (0, 14): ('m', 3), (7, 0): ('m', 3), 
  (7, 14): ('m', 3), (14, 0): ('m', 3), (14, 7): ('m', 3), (14, 14): ('m', 3), 
  (1, 1): ('m', 2), (1, 13): ('m', 2), (2, 2): ('m', 2), (2, 12): ('m', 2), 
  (3, 3): ('m', 2), (3, 11): ('m', 2), (4, 4): ('m', 2), (4, 10): ('m', 2), 
  (7, 7): ('m', 2), (10, 4): ('m', 2), (10, 10): ('m', 2), (11, 3): ('m', 2), 
  (11, 11): ('m', 2), (12, 2): ('m', 2), (12, 12): ('m', 2), (13, 1): ('m', 2), 
  (13, 13): ('m', 2), (1, 5): ('l', 3), (1, 9): ('l', 3), (5, 1): ('l', 3), 
  (5, 5): ('l', 3), (5, 9): ('l', 3), (5, 13): ('l', 3), (9, 1): ('l', 3), (9, 5): ('l', 3), 
  (9, 9): ('l', 3), (9, 13): ('l', 3), (13, 5): ('l', 3),(13, 9): ('l', 3), (0, 3): ('l', 2), 
  (0, 11): ('l', 2), (2, 6): ('l', 2), (2, 8): ('l', 2), (3, 0): ('l', 2), (3, 7): ('l', 2), 
  (3, 14): ('l', 2), (6, 2): ('l', 2), (6, 6): ('l', 2), (6, 8): ('l', 2), (6, 12): ('l', 2), 
  (7, 3): ('l', 2), (7, 11): ('l', 2), (8, 2): ('l', 2), (8, 6): ('l', 2), (8, 8): ('l', 2), 
  (8, 12): ('l', 2), (11, 0): ('l', 2), (11, 7): ('l', 2), (11, 14): ('l', 2), (12, 6): ('l', 2), 
  (12, 8): ('l', 2), (14, 3): ('l', 2), (14, 11): ('l', 2)
}

# tutorial: https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# color constants
RED = "\033[48;2;229;108;123m"
END = "\u001b[0m"
LIGHT_BLUE = "\033[48;2;172;203;223m"
BLUE = "\033[48;2;63;148;242m"
PINK = "\033[48;2;237;165;177m"
BOARD_LINES = "\033[38;2;205;197;178m"
EMPTY_BG = "\033[48;2;213;198;165m"
TILE_BG = "\033[48;2;201;171;135m"

# number of each letter
jetons_nbre = {
  "A": 9, "B": 2, "C": 2, "D": 3, "E": 15, "F": 2, "G": 2, "H": 2, "I": 8, "J": 1, "K": 1, "L": 5, "M": 3, "N": 6, "O": 6, "P": 2, "Q": 1, "R": 6, "S": 6, "T": 6, "U": 6, "V": 2, "W": 1, "X": 1, "Y": 1, "Z": 1, "_": 2
}

# global variables - scores and inventories
global inventory1
inventory1 = []
global inventory2
inventory2 = []
global userscore1
userscore1 = 0
global userscore2
userscore2 = 0

global board_arr

# keeps track of whose turn it is
global turn

# start with player 1
turn = 1

# creates bag of scrabble letters
BAG = []
for key, val in jetons_nbre.items():
  for i in range(val):
    BAG.append(key)

indicators = ["① ","② ","③ ", "④ ", "⑤ ","⑥ ","⑦ ", "⑧ ", "⑨ ", "⑩ ", "⑪ ", "⑫ ", "⑬ ", "⑭ ", "⑮ "]
def print_board():#prints the board with the right colors and placement
  '''prints the board with the correct colors'''
  global board_arr, userscore1, userscore2
  
  board_str = '  ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮\n'
  
  for i in range(len(board_arr)):
    board_str += indicators[i]
    
    for j in range(len(board_arr[i])):
      
      if (i, j) in MULTIS.keys() and (board_arr[i][j] == "  " or board_arr[i][j] == "★ "):
        if MULTIS[(i, j)] == ('m', 3):
          # red for m3 multiplier
          board_str += RED + board_arr[i][j] + END
          
        elif MULTIS[(i, j)] == ('m', 2):
          # pink for m2 multiplier
          board_str += PINK + board_arr[i][j] + END
          
        elif MULTIS[(i, j)] == ('l', 2):
          # light blue for l2 multiplier
          board_str += LIGHT_BLUE + board_arr[i][j] + END
          
        else:
          # dark blue for l3 multiplier
          board_str += BLUE + board_arr[i][j] + END
          
      else:
        if board_arr[i][j] != "  ":
          # if the tile has a letter, add the tile color
          board_str += TILE_BG + board_arr[i][j] + END
          
        else:
          # regular background color
          board_str += EMPTY_BG + board_arr[i][j] + END

    board_str += "\n"
  print(board_str)

  print("Player 1 Score: ", userscore1)
  print("Player 2 Score: ", userscore2)
  print("\n")

#creates board
def board_init():
  global board
  global board_arr

  print(BOARD_LINES + "                      Welcome to Scrabble!")
  print("Multipliers: \n \033[48;2;237;165;177mPink is 2x word\u001b[0m \n \033[48;2;229;108;123mRed is 3x word\u001b[0m \n \033[48;2;172;203;223mLight blue is 2x letter\u001b[0m \n \033[48;2;63;148;242mBlue is 3x letter\u001b[0m \033[38;2;205;197;178m"+ END)
  board_arr = [["  "] * 15 for i in range(15)]

  # places a star in the middle of the board - only to emulate real scrabble
  board_arr[7][7] = "★ "

#returns inventories to be printed
def invprint(v, n):
  # n = player number
  # v = inventory
  printed = f"Letters for Player {n}:\n"

  for letter in v:
    printed = printed + TILES[LETTERS.index(letter)] + " | "
    
  return printed

#scores the words
def score(placement, player):
  global userscore1
  global userscore2
  global board_arr

  score = 0
  multiply_word = 1
  
  for place, let in placement.items():
    r, c = place
    if place in MULTIS.keys():
      #case 1: it's on a multiplier
      type, num = MULTIS[place]
      
      if type == 'l':
        # multiplies the letter by the amount necessary
        
        if board_arr[r][c][1] != "₀":
          score += JETONS_PTS[let] * num
          
      else:
        # it adds to the word multiplier, adds regular amount to score
        if board_arr[r][c][1] != "₀":
          multiply_word *= num
          score += JETONS_PTS[let]
          
    else:
      # it's not on a multiplier - add regular amount
      if board_arr[r][c][1] != "₀":
        score += JETONS_PTS[let]
  
  if player == 1:
    print("adding "+ str(score*multiply_word) + " to score")
    userscore1 += score * multiply_word
  
  else:
    userscore2 += score * multiply_word

  print_board()
  return (True, score * multiply_word)

#transfers letters from the bag to the inventory
def give_letters(player):
  #num = number of letter, player = 1 is for player1(inventory1) and for player 2(inventory2)
  if len(BAG) == 0:
    print('Bag is now empty, no new letters will be given.')
    return None
  if player == 1:
    for i in range(7 - len(inventory1)):
      if len(BAG) >= 1:
        letter = random.choice(BAG)
        BAG.remove(letter)
        inventory1.append(letter)
  else:
    for i in range(7 - len(inventory2)):
      if len(BAG) >= 1:
        letter = random.choice(BAG)
        BAG.remove(letter)
        inventory2.append(letter)

def get_input():
  global GAME

  global turn

  print("\n")
  print_board()
  #checks who turn it is
  give_letters(turn)
  if turn == 1:
    print(invprint(inventory1, 1))
  else:
    print(invprint(inventory2, 2))
  #ask for word, location, and direction
  word = input('Input a word you can make with your letters. \n')
  word = word.upper()
  row = input('Input row number of the first letter in word.\n')
  column = input('Input column number of the first letter in word\n')
  direction = input('Input "H" for horizontal or "V" for vertical\n')

  try:
    row = int(row)
    row -= 1
    column = int(column)
    column -= 1
  except:
    print("Your input was invalid. Please try again.")
    return word, -1, -1, direction
    
  return word, row, column, direction

def validate(word, row, col, dir):#makes sure that the letters used where in the inventory of the player, makes sure that the word fits and that it intersects proprely and ask for the letter that is going to replace the blank. And its last thing it does is placing the letters on the board
  global board_arr
  global turn
  count_inter = 0
  dir = dir.upper()
  letters = [l for l in word]

  if dir == 'H':
    coordinates = [(row, col + y) for y in range(len(word))]
  elif dir == 'V':
    coordinates = [(row + x, col) for x in range(len(word))]
  else:
    return (False,'Not vertical or horizontal.')
  # condition 1: the word must fit
  for array in coordinates:
    for pos in array:
      if pos > 14 or pos < 0:
        print("Your word does not fit on the board.")
        return (False, "Word does not fit.")

  placement = dict(zip(coordinates, letters))
  used_letters = []
  inter_letters = []
  
  if turn == 1:
    inv_copy = inventory1.copy()
  else:
    inv_copy = inventory2.copy()
  
  for cord in coordinates:
    row = cord[0]
    col = cord[1]
    if board_arr[row][col] == "  " or board_arr[row][col] == "★ ":
      # current spot is empty - user MUST have a letter to place
      if turn == 1:
        if placement[cord] not in inv_copy:
          print("You used a letter you did not have. Please try again.")
          return (False, 'incorrect letter')
        else:
          # its in the inventory and its valid
          if board_arr[row][col] == "★ ":
            count_inter += 1
          used_letters.append(placement[cord])
          inv_copy.remove(placement[cord])
      else:
        # then player 2
        if placement[cord] not in inv_copy:
          print("You used a letter you did not have. Please try again.")
          return (False, "incorrect letter")
        else:
          if board_arr[row][col] == "★ ":
            count_inter += 1
          used_letters.append(placement[cord])
          inv_copy.remove(placement[cord])
    else:
      if placement[cord] == board_arr[row][col][0]:
        count_inter += 1
        inter_letters.append(placement[cord])
      else:
        print("Your word does not properly intersect. Double check your coordinates.")
        return (False, "Letter does not properly intersect. Recheck your coordinates.")

  if count_inter == 0:
    print("Your word does not intersect. Please try again.")
    return (False, "no intersection")

  for letter in used_letters:#check letter is in inv
    if turn == 1:
      inventory1.remove(letter)
    else:
      inventory2.remove(letter)

  # this places the letters
  for cord, letter in placement.items():
    if letter == "_":
      blank_replace = input('What letter you would like your blank to replace: ')
      blank_replace = blank_replace.upper()
      placement[cord] = blank_replace
      board_arr[cord[0]][cord[1]] = blank_replace + "₀"
    else:
      if board_arr[cord[0]][cord[1]][1] != "₀":
        board_arr[cord[0]][cord[1]] = TILES[LETTERS.index(letter)]
      else: 
        board_arr[cord[0]][cord[1]] = TILES[LETTERS.index(letter)][0] + "₀"

  return (True, placement)


global GAME
GAME = "RUNNING"

def main():#the function that runs the game and that holds everything in the gamer
  global turn, inventory1, inventory2, BAG, GAME
  
  GAME = " "
  
  board_init()
  give_letters(1)
  give_letters(2)

  while GAME != "DONE":
    print(BOARD_LINES + "\nHello Player " + str(turn) + ".")
    if turn == 1:
      print(END)
      print(invprint(inventory1, turn))
    else:
      print(END)
      print(invprint(inventory2, turn))

    valid = False
    valid_move = False
    
    while valid_move == False:
      if (len(BAG) == 0 and len(inventory1) == 0) or (len(BAG) == 0 and len(inventory2) == 0):
        print("A user has reached an empty inventory. The game is now over.")
        if userscore1 > userscore2:
          print(f"Player 1 won with {userscore1} points.")
        elif userscore2 > userscore1:
          print(f"Player 2 won with {userscore2} points.")
        else:
          print(f"Both players tied with {userscore1} points.")
        valid_move = True
        GAME = "DONE"
       
      move = input(BOARD_LINES + "\nPlease pick an action:\n \
    1: Play a word\n \
    2: Skip turn.\n \
    3: Get new letters. \n \
    4: End Game\n\n"+ END)
      if move == "1":
        while valid == False:
          word, row, col, dir = get_input()
          validity = validate(word, row, col, dir)
          
          if validity[0] == False:
            valid = False
        
          else:
            score(validity[1], turn)
            valid = True
       
        valid_move = True
     
      elif move == "2":
        valid_move = True
        pass
    
      elif move == "3":
        if turn == 1:
          inventory1 = []
          give_letters(1)
          print(invprint(inventory1, 1))
      
        else:
          inventory2 = []
          give_letters(2)
          print(invprint(inventory2, 2))
        valid_move = True
    
      elif move == "4":
        if userscore1 < userscore2:
          print(f'Player 2 won with {userscore2} points.')
       
        elif userscore2 < userscore1:
          print(f'Player 1 won with {userscore1} points.')
       
        else:
          print(f'The game was a tie: each player had {userscore1} points.')
        # game ends here
        GAME = "DONE"
        valid_move = True
        break
      
      else:
        valid_move = False
    
    # next turn    
    if turn == 1:
      if len(BAG) >= 1:
        give_letters(1)
        turn = 2
      else:
        print("There are no more letters. The bag is now empty.")
        
    else:
      if len(BAG) >= 1:
        give_letters(2)
        turn = 1
      else:
        print("There are no more letters. The bag is now empty.")


if __name__ == "__main__":
  # if statement taken from: https://realpython.com/python-main-function/
  main()
