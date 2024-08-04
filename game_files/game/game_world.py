"""game_world.py, the main state that runs the game, generates the map and objects etc.

Contains:
 - Game_world class
 - Level classes
Links to:
 - pause state
"""

from game.state import State
from game.sub_states import Pause_champ, Transition
from game.sprites import *
from game.elements import *
from random import randint # NOTE for testing

class Game_World(State):
    """A class used to manage the actual game world state for the game, i.e. the one
    the player plays in."""
    def __init__(self, game):
        State.__init__(self, game)

        # Level management:
        
        self.game = game
        self.level_num = game.saved_level # Number which acts as the key to the level classes in the dictionary
        self.levels = {"0": Level_0(game), "1": Level_1(game), "2": Level_2(game), "3": Level_3(game), 
                       "4": Level_4(game), "5": Level_5(game), "6": Level_6(game), "7": Level_7(game),
                       "8": Test_Level(game)} 
        self.current_level = self.levels[f"{self.level_num}"] # Change level_num into a string and use it as key for dict
        self.radius = 100 # radius for end point
        self.exit_game = False
        
        # For testing purposes:
        #self.current_level = Test_Level(game)

    def go_next_level(self):
        if (self.current_level.end_point[0] - self.radius <= self.current_level.player.rect.center[0] <= self.current_level.end_point[0] + self.radius and 
            self.current_level.end_point[1] - self.radius <= self.current_level.player.rect.center[1] <= self.current_level.end_point[1] + self.radius):  
            if (self.level_num == 7): # Last level
                print("game over")
                trans_state = Transition(self.game, "GAME COMPLETED")
                trans_state.enter_state()
                self.exit_game = True
            elif (self.level_num == 8): # Test level, does not go to any next level
                print("go next")
            else:
                self.level_num += 1
                self.current_level = self.levels[f"{self.level_num}"]
                self.game.saved_level = self.level_num # Update the current level game-wide

    def update(self, delta_time, actions): 
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()
        self.current_level.update(delta_time, actions)
        # print(self.current_level.player.rect.center)

        if self.exit_game:
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop() # pop states until we reach back to the title screen
        self.go_next_level()
    
    def render(self, display):
        self.current_level.render(display)


"""Level classes:"""

class Level_0():
    """A class used to create an instance of level 0.

     Location: IO island
     Programming concepts: Basics of C, IO, types in C
     Hint NPCs: Professor Floofington, Dennis Scratchie, Brian Fur-nighan, Cat Thompson
     Task NPCs: SoC freshman, Luke Manu, Desmon Chungus
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "io_island") #TODO: Change this to take in the correct tmx map
        self.player_coords = (656, 1700) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (2533, 588)

        # Welcome chat box
        self.show_chat = [1]        
        self.welcome_chatbox = Chatbox(game, "Developer No. 2",
                               ("Welcome to Catopia.","Use W, A, S and D to move around.","Press E while standing near NPCs to talk tothem."))

        # NPCs
        self.prof_floof_texts = ("Greetings!", 
                                 "Everyone here is cat themed because        Developer No. 1 likes cats.",
                                 "Some strange things are happening around   here,",
                                 "And somehow everyone has become incompetent"
                                 "We need your help to fix them!", 
                                 "Pick up all the knowledge you can from the Hint NPCs,",
                                 "Then fix the problems posed by Task NPCs.",
                                 "Good luck!")
        self.prof_floof_pos = (700, 1244) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.prof_floof = Hint_NPC(game, self.all_sprites, "Prof. Floofington", "prof_floof", self.prof_floof_pos, self.prof_floof_texts)
        
        self.dennis_texts = ("C is a powerful programming language       developed by Dennis Ritchie in the 1970s.",
                             "It is known for its efficiency and control over hardware and memory.",
                             "It has different variable types that must  be defined such as int, char and float.",
                             "The entry point of any C program is the    'int main()' function.",
                             "Here's an example of a program in C:       int main() {                               printf(\"Hello\");                           }")
        self.dennis_pos = (1048, 1292)
        self.dennis = Hint_NPC(game, self.all_sprites, "Dennis Scratchie", "dennis", self.dennis_pos, self.dennis_texts)

        self.brian_texts = ("Printing and scanning to the terminal can  be done using the printf() and scanf()     functions.",
                            f"printf takes a format string and a variablenumber of arguments, with placeholders like'%d' for integers, '%f' for floats,        '%c' for chars and '%s' for strings",
                            f"For example,                               int num = 5;                               printf(\"The number is %d\", num);           prints 'The number is 5'",
                            f"scanf reads formatted input from standard  input using the same placeholders, it takesin a format string and pointers to the     variables where the data will be stored",
                            f"For example,                               int num;                                   scanf(\"%d\", &num);                         reads in an integer and stores it in num")
        self.brian_pos = (1548, 1222)
        self.brian = Hint_NPC(game, self.all_sprites, "Brian Fur-nighan", "brian", self.brian_pos, self.brian_texts)

        self.soc_freshman_texts = ("The words in my book disappeared", "It's like someone messed up the printf     statement!", )
        self.soc_freshman_correct = ("Wow! Thanks for the help!", )
        self.soc_freshman_wrong = ("Man! It still doesn't work...", )
        self.soc_freshman_pos = (2007, 520)
        self.soc_freshman = Task_NPC(game, self.all_sprites, "SoC Freshman", "soc_freshman", self.soc_freshman_pos, self.soc_freshman_texts, self.soc_freshman_correct, self.soc_freshman_wrong)
        self.soc_freshman.task_state = Freshman_Task(game, self.soc_freshman.text_pointer)

        self.luke_texts = ("... .... .. .....", 
                           "<The difficulty of the CS1010 PE has left   Lyuke unable to converse>",
                           "<We need to reprogram his brain's input and output to fix him>")
        self.luke_correct = ("I should have studied business instead.", )
        self.luke_wrong = (". .... ......", "<He still cannot speak>")
        self.luke_pos = (605, 179)
        self.luke = Task_NPC(game, self.all_sprites, "Lyuke ManU", "luke", self.luke_pos, self.luke_texts, self.luke_correct, self.luke_wrong)
        self.luke.task_state = Luke_Task(game, self.luke.text_pointer)

        self.desmon_texts = ("I hate decimals, they're too complicated!", "Change them into integers for me!")
        self.desmon_correct = ("That's right! For honour and glory!", )
        self.desmon_wrong = ("Wrong... For tonner and lorry!", )
        self.desmon_pos = (1281, 617)
        self.desmon = Task_NPC(game, self.all_sprites, "Desmon Chungus", "desmon", self.desmon_pos, self.desmon_texts, self.desmon_correct, self.desmon_wrong)
        self.desmon.task_state = Desmon_Task(game, self.desmon.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering IO Island, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
        self.welcome_chatbox.update(actions, self.show_chat)
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)
        if self.show_chat[0] == 1:
            self.welcome_chatbox.print()
        self.prof_floof.chatters()
        self.dennis.chatters()
        self.brian.chatters()
        self.soc_freshman.chatters()
        self.luke.chatters()
        self.desmon.chatters()

class Level_1():
    """A class used to create an instance of level 1.

     Location: Arithmetic Acres
     Programming concepts: Basic math operations
     Hint NPCs: John Catmack
     Task NPCs: MacOS Fanboy, Coffee Drinker, Disgruntled Student
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "arithmetic_acres") #TODO: Change this to take in the correct tmx map
        self.player_coords = (69, 579) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (2537, 880)

        # NPCs
        self.john_texts = (f"Basic arithmetic in C uses operators such  as +, -, *, /, % for addition, subtraction,multiplication, division and modulus       (remainder).",
                           "These operators can be used with variables and constants.")
        self.john_pos = (465, 401) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.john = Hint_NPC(game, self.all_sprites, "John Catmack", "john", self.john_pos, self.john_texts)
        
        self.macOS_texts = ("I love collecting apples!", "But I have no idea how to count how many   apples I have!")
        self.macOS_correct = ("Wow! Thanks for the help!", )
        self.macOS_wrong = ("Man! That can't be right...", )
        self.macOS_pos = (1473, 611)
        self.macOS = Task_NPC(game, self.all_sprites, "MacOS Fanboy", "macOS", self.macOS_pos, self.macOS_texts, self.macOS_correct, self.macOS_wrong)
        self.macOS.task_state = MacOS_Task(game, self.macOS.text_pointer)

        self.coffee_texts = ("My coffee mug keeps refilling itself!", 
                             "Not that I'm complaining but,",
                             "Wonder how much free coffee I've gotten?")
        self.coffee_correct = ("Glitches in this world can be pretty usefulif I do say so myself!", )
        self.coffee_wrong = ("Hmm I don't remember drinking that much...",)
        self.coffee_pos = (261, 1377)
        self.coffee = Task_NPC(game, self.all_sprites, "Coffee Drinker", "coffee", self.coffee_pos, self.coffee_texts, self.coffee_correct, self.coffee_wrong)
        self.coffee.task_state = Coffee_Task(game, self.coffee.text_pointer)

        self.student_texts = ("I have no idea how to solve quadratic      equations.",)
        self.student_correct = ("That makes sense!", )
        self.student_wrong = ("I'm even more lost now...", )
        self.student_pos = (2067, 847)
        self.student = Task_NPC(game, self.all_sprites, "Disgruntled Student", "student", self.student_pos, self.student_texts, self.student_correct, self.student_wrong)
        self.student.task_state = Student_Task(game, self.student.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Arithmetic Acres, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.john.chatters()
        self.macOS.chatters()
        self.coffee.chatters()
        self.student.chatters()

class Level_2():
    """A class used to create an instance of level 2.

     Location: Logic Links
     Programming concepts: Basic conditional operations
     Hint NPCs: Markus Fursson
     Task NPCs: Jamie, Windows User, Young Punk
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "logic_links_2") #TODO: Change this to take in the correct tmx map
        self.player_coords = (81, 811) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (2365, 821)

        # NPCs
        self.mark_texts = (f"If-else statements in C let you to execute different blocks of code based on whether acondition is true or false",
                           "The syntax involves using                  'if (condition) {<code>} else {code}'",
                           "Conditional operators such as '==', '!=',  '<', '>', '<=' and '>=', meaning equal to, not equal to, less than, more than, less   than or equal to, more than or equal to",
                           "can be used to form the conditions for the if else statement.")
        self.mark_pos = (219, 563) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.mark = Hint_NPC(game, self.all_sprites, "Markus Fursson", "mark", self.mark_pos, self.mark_texts)
        
        self.jamie_texts = ("I just got back my DTK results,", "Wonder what grade I got?")
        self.jamie_correct = ("Wow! Thanks for the help!", )
        self.jamie_wrong = ("Time to SU this...", )
        self.jamie_pos = (1067, 721)
        self.jamie = Task_NPC(game, self.all_sprites, "Jamie", "jamie", self.jamie_pos, self.jamie_texts, self.jamie_correct, self.jamie_wrong)
        self.jamie.task_state = Jamie_Task(game, self.jamie.text_pointer)

        self.windows_texts = ("I love Windows but,", "Every update introduces new glitches...", "What should I do to sieve them out?")
        self.windows_correct = ("Thanks! Now I don't have to change to Mac!", )
        self.windows_wrong = ("Maybe Mac is better...",)
        self.windows_pos = (1013, 1319)
        self.windows = Task_NPC(game, self.all_sprites, "Windows User", "windows", self.windows_pos, self.windows_texts, self.windows_correct, self.windows_wrong)
        self.windows.task_state = Windows_Task(game, self.windows.text_pointer)

        self.punk_texts = ("I hate rules!", "Fighting is my way of life!")
        self.punk_correct = ("I'm gonna mess them up", )
        self.punk_wrong = ("Guess I'll die :/", )
        self.punk_pos = (2131, 831)
        self.punk = Task_NPC(game, self.all_sprites, "Young Punk", "punk", self.punk_pos, self.punk_texts, self.punk_correct, self.punk_wrong)
        self.punk.task_state = Punk_Task(game, self.punk.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Logic Links, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.mark.chatters()
        self.jamie.chatters()
        self.windows.chatters()
        self.punk.chatters()

class Level_3():
    """A class used to create an instance of level 3.

     Location: Loop Lake
     Programming concepts: For and while loops
     Hint NPCs: Cat Thompson, Alan Purring
     Task NPCs: Bensen, Local Fisherman, Notepad User
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "loop_lake_final") #TODO: Change this to take in the correct tmx map
        self.player_coords = (399, 957) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (1975, 137)

        # NPCs
        self.thomp_texts = (f"Loops can be used to repeatedly execute    lines of code while a condition is met.",
                           "While loops take in a condition and        repeatedly execute the block of code while the condition is true."
                           "While loops can be used for indeterminate  iteration."
                           "For loops specify initialisation, conditionand increment or decrement in one line."
                           "For loops are more suitable for known      iteration counts.")
        self.thomp_pos = (445, 695) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.thomp = Hint_NPC(game, self.all_sprites, "Cat Thompson", "thomp", self.thomp_pos, self.thomp_texts)
        
        self.bensen_texts = ("Hi I'm Bensen!", "Counting to 69 is my favourite passtime!")
        self.bensen_correct = ("69 :)", )
        self.bensen_wrong = ("68 :(", )
        self.bensen_pos = (383, 95)
        self.bensen = Task_NPC(game, self.all_sprites, "Bensen", "bensen", self.bensen_pos, self.bensen_texts, self.bensen_correct, self.bensen_wrong)
        self.bensen.task_state = Bensen_Task(game, self.bensen.text_pointer)

        self.fisher_texts = ("My fish these days seem to be glitching out", 
                             "I need a way to sort out which fish out of all the fish I caught are glitched.")
        self.fisher_correct = ("Great! No more selling glitched fish!", )
        self.fisher_wrong = ("How am I supposed to sort them now...",)
        self.fisher_pos = (829, 719)
        self.fisher = Task_NPC(game, self.all_sprites, "Local Fisherman", "fisher", self.fisher_pos, self.fisher_texts, self.fisher_correct, self.fisher_wrong)
        self.fisher.task_state = Fisher_Task(game, self.fisher.text_pointer)

        self.alan_texts = (f"Recursion is when a function calls itself  to solve a smaller instance of the same    problem.",
                           "It continues this process until it reaches a base case, which stops the recursion.",
                           "While the concept sounds similar to loops, recursion can be more useful for solving   problems like tree or graph traversal.")
        self.alan_pos = (1579, 251) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.alan = Hint_NPC(game, self.all_sprites, "Alan Purring", "alan", self.alan_pos, self.alan_texts)

        self.notepad_texts = ("I am a notepad. I print things on myself.", "Help me never stop printing.")
        self.notepad_correct = ("Notes are a lifestyle", )
        self.notepad_wrong = ("No notes, no life...", )
        self.notepad_pos = (1839, 103)
        self.notepad = Task_NPC(game, self.all_sprites, "Notepad User", "notepad", self.notepad_pos, self.notepad_texts, self.notepad_correct, self.notepad_wrong)
        self.notepad.task_state = Notepad_Task(game, self.notepad.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Loop Lake, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.thomp.chatters()
        self.bensen.chatters()
        self.fisher.chatters()
        self.alan.chatters()
        self.notepad.chatters()

class Level_4():
    """A class used to create an instance of level 4.

     Location: Pointer Peaks
     Programming concepts: Pointers
     Hint NPCs: Linus Pawvalds
     Task NPCs: Linux Enjoyer, Tian Duck, Most Sane CEG Student
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "pointer_peaks") 
        self.player_coords = (379, 855) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (3213, 1363)

        # NPCs
        self.linus_texts = ("Pointers in C are variables that store     memory address of other variables.",
                           "Pointers can be used by declaring them with the '*' symbol, assigning them the address of a variable using '&'.",
                           "Accessing or modifying the value at the    address they point to is done with the     dereference operator, '*'.")
        self.linus_pos = (861, 713) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.linus = Hint_NPC(game, self.all_sprites, "Linus Pawvalds", "linus", self.linus_pos, self.linus_texts)
        
        self.linux_texts = ("My memory is all over the place...", "I need something to point to my memory     addresses properly.")
        self.linux_correct = ("I remember!", )
        self.linux_wrong = ("I forgor...", )
        self.linux_pos = (1501, 625)
        self.linux = Task_NPC(game, self.all_sprites, "Linux Enjoyer", "linux", self.linux_pos, self.linux_texts, self.linux_correct, self.linux_wrong)
        self.linux.task_state = Linux_Task(game, self.linux.text_pointer)

        self.tian_texts = ("I found my grandma's pho recipe!", 
                           "But I'm not sure how much water to add...")
        self.tian_correct = ("So that's how much!", )
        self.tian_wrong = ("That can't be right...",)
        self.tian_pos = (2129, 1143)
        self.tian = Task_NPC(game, self.all_sprites, "Tian Duck", "tian", self.tian_pos, self.tian_texts, self.tian_correct, self.tian_wrong)
        self.tian.task_state = Tian_Task(game, self.tian.text_pointer)

        self.sane_texts = ("I have an exam at COM 1 but I'm not sure where to go,",
                           "Could you help print the address?")
        self.sane_correct = ("Oh! That's where it is", )
        self.sane_wrong = ("I'm going to get lost...", )
        self.sane_pos = (2939, 1389)
        self.sane = Task_NPC(game, self.all_sprites, "Most Sane CEG Student", "sane", self.sane_pos, self.sane_texts, self.sane_correct, self.sane_wrong)
        self.sane.task_state = Sane_Task(game, self.sane.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Pointer Peaks, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.linus.chatters()
        self.linux.chatters()
        self.tian.chatters()
        self.sane.chatters()

class Level_5():
    """A class used to create an instance of level 5.

     Location: Array Arena
     Programming concepts: Static Arrays
     Hint NPCs: Mark Zucatberg
     Task NPCs: Json K, Local Rascal, Chad Ko
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "array_arena") #TODO: Change this to take in the correct tmx map
        self.player_coords = (331, 1363) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (2537, 880)

        # NPCs
        self.zuck_texts = ("Arrays are collections of elements of the  same type stored in contiguous memory      locations.",
                           "To declare an array, specify the type, nameand size. For example,                     int numbers[10];", 
                           "Access elements using the index notation.  For example,                               numbers[0]; for the first element")
        self.zuck_pos = (381, 1049) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.zuck = Hint_NPC(game, self.all_sprites, "Mark Zucatberg", "zuck", self.zuck_pos, self.zuck_texts)
        
        self.json_texts = ("This arena has a semi-rich history!", "It was of slight importance in the past,", 
                           "I'm making a list of the number of people  who died over the years.")
        self.json_correct = ("Wow! Thanks for the help!", )
        self.json_wrong = ("Man! That can't be right...", )
        self.json_pos = (903, 1081)
        self.json = Task_NPC(game, self.all_sprites, "Json K", "json", self.json_pos, self.json_texts, self.json_correct, self.json_wrong)
        self.json.task_state = Json_Task(game, self.json.text_pointer)

        self.rascal_texts = ("I've got a list of important numbers here,", 
                             "But I can't read")
        self.rascal_correct = ("Much thanks.", )
        self.rascal_wrong = ("What! Useless...",)
        self.rascal_pos = (1289, 371)
        self.rascal = Task_NPC(game, self.all_sprites, "Local Rascal", "rascal", self.rascal_pos, self.rascal_texts, self.rascal_correct, self.rascal_wrong)
        self.rascal.task_state = Rascal_Task(game, self.rascal.text_pointer)

        self.chad_texts = ("Hey there", "I'm collecting data on the occurences of   glitches in Catopia.", "Need some help storing the data!")
        self.chad_correct = ("Thanks!", )
        self.chad_wrong = ("The data was lost...", )
        self.chad_pos = (2023, 875)
        self.chad = Task_NPC(game, self.all_sprites, "Chad Ko", "chad", self.chad_pos, self.chad_texts, self.chad_correct, self.chad_wrong)
        self.chad.task_state = Chad_Task(game, self.chad.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Array Arena, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.zuck.chatters()
        self.json.chatters()
        self.rascal.chatters()
        self.chad.chatters()

class Level_6():
    """A class used to create an instance of level 6.

     Location: Memory Meadows
     Programming concepts: Memory management
     Hint NPCs: Terry Pawvis
     Task NPCs: Microsoft Mike, Vim User, Robert
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "memory_meadows") #TODO: Change this to take in the correct tmx map
        self.player_coords = (339, 121) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (2581, 641)

        # NPCs
        self.terry_texts = ("Sometimes while programming in C, we do notwant to hard code how much memory is used.",
                             "For example, when creating an array, users may require different array sizes. In this case, we dynamically allocate the memory to the array using malloc.",
                             "To determine the size of the data type, we can use 'sizeof'.",
                             "An example of using malloc:                int *list = (int*)malloc(n * sizeof(int)); where n is the desired size of the array.",
                             "We can also use calloc:                    int *list = (int*)calloc(n, sizeof(int));",
                             "To reallocate the memory, one can use:     list = (int*)realloc(list, n*sizeof(int));",
                             "To free the allocated memory before the    program ends, use free(). Continuing the   previous example: free(list);")
        self.terry_pos = (385, 395) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.terry = Hint_NPC(game, self.all_sprites, "Terry Pawvis", "terry", self.terry_pos, self.terry_texts)

        self.mike_texts = ("I'm detecting strange energy sources aroundthe meadows,", "I need a way to create containers that can store the energy and vary in size based on how much energy is scanned!")
        self.mike_correct = ("Wow! Thanks for the help!", )
        self.mike_wrong = ("Man! That can't be right...", )
        self.mike_pos = (685, 1019)
        self.mike = Task_NPC(game, self.all_sprites, "Microsoft Mike", "mike", self.mike_pos, self.mike_texts, self.mike_correct, self.mike_wrong)
        self.mike.task_state = Mike_Task(game, self.mike.text_pointer)

        self.vim_texts = ("Vim is the best text editor!", "But there's too many shortcuts and macros  to remember...", "I gotta reallocate my memory to fit in all the Vim knowledge!")
        self.vim_correct = ("I love Vim!", )
        self.vim_wrong = ("I might have to swap to VSC...")
        self.vim_pos = (1629, 1111)
        self.vim = Task_NPC(game, self.all_sprites, "Vim User", "vim", self.vim_pos, self.vim_texts, self.vim_correct, self.vim_wrong)
        self.vim.task_state = Vim_Task(game, self.vim.text_pointer)

        self.robert_texts = ("Memory leaks are occuring all over the     island!", "I bet the developers forgot to free the    memory!")
        self.robert_correct = ("All fixed now!", )
        self.robert_wrong = ("It's all still a mess...", )
        self.robert_pos = (2123, 641)
        self.robert = Task_NPC(game, self.all_sprites, "Robert", "robert", self.robert_pos, self.robert_texts, self.robert_correct, self.robert_wrong)
        self.robert.task_state = Robert_Task(game, self.robert.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Memory Meadows, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.terry.chatters()
        self.mike.chatters()
        self.vim.chatters()
        self.robert.chatters()

class Level_7():
    """A class used to create an instance of level 7.

     Location: Struct Shores
     Programming concepts: Structs
     Hint NPCs: Bill Cats
     Task NPCs: Avid Leetcoder, Developer No.2
    """

    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "struct_shores") #TODO: Change this to take in the correct tmx map
        self.player_coords = (661, 1235) #TODO: Change this to extract the player coordinates from the tmx map
        self.player = Player(game, self.player_coords, self.all_sprites)
        self.end_point = (1781, 1261)

        # NPCs
        self.bill_texts = ("Structs in C are user-defined data types   that group data under a single name,      allowing for organisation of related      variables.",
                           "They are defined using the struct keyword, and members are accessed using the dot     operator.",
                           "Structs are useful for creating complex    data structures like records or objects.")
        self.bill_pos = (665, 659) #TODO: Change all the NPC coords to be extracted from the tmx map
        self.bill = Hint_NPC(game, self.all_sprites, "Bill Cats", "bill", self.bill_pos, self.bill_texts)
        
        self.leet_texts = ("I love leet code!", "I keep tabs on all the best leet coders!")
        self.leet_correct = ("One day I'll be the best leetcoder!", )
        self.leet_wrong = ("I'll never be the best leetcoder...", )
        self.leet_pos = (655, 299)
        self.leet = Task_NPC(game, self.all_sprites, "Avid Leetcoder", "leet", self.leet_pos, self.leet_texts, self.leet_correct, self.leet_wrong)
        self.leet.task_state = Leet_Task(game, self.leet.text_pointer)

        self.dev_texts = ("Have you ever heard of drunk programming?", "Been trying it out while making this world!", "Might explain all the glitches...")
        self.dev_correct = ("The world should be fixed now!", )
        self.dev_wrong = ("Back to the alcohol...",)
        self.dev_pos = (1819, 635)
        self.dev = Task_NPC(game, self.all_sprites, "Coffee Drinker", "dev", self.dev_pos, self.dev_texts, self.dev_correct, self.dev_wrong)
        self.dev.task_state = Dev_Task(game, self.dev.text_pointer)

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Struct Shores, Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)

        self.bill.chatters()
        self.leet.chatters()
        self.dev.chatters()

class Test_Level():
    """A class used to create an instance of the test level.

    Location: Test map
    Programming concepts: Nil
    Hint NPCs: test_hint_NPC
    Task NPC: test_task_NPC

    ### NOTE:
    Uses temporary map, player and NPC designs. Used for milestone 1 to show proof of concept.

    At the time this class was made, there the map and characters etc were all imported from image files. 
    This level may not work once the sprite logic etc is changed to handle tmx files and maybe spritesheets.
    """
    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game, "logic_links_2")
        self.player = Player(game, (900,500), self.all_sprites)

        # NPCs
        self.test_hint_NPC_texts = ("Hi there. I am a test hint NPC.", "I give no hints, except...", "Vim is the best text editor.")
        self.test_hint_NPC = Hint_NPC(game, self.all_sprites, "test hint NPC", "linus", (600,350), self.test_hint_NPC_texts)
        self.test_task_NPC_texts = ("Hi there. I am a test task NPC.", )
        self.test_hint_NPC_correct = ("Yes it's true!", "They are quite good looking!")
        self.test_hint_NPC_wrong = ("Hmm you seem to be wrong...", "Walk away and come back to try again...")
        self.test_task_NPC = Task_NPC(game, self.all_sprites, "test task NPC", "alan", (800,350), self.test_task_NPC_texts, self.test_hint_NPC_correct, self.test_hint_NPC_wrong)
        self.test_task_NPC.task_state = Vim_Task(game, self.test_task_NPC.text_pointer)

        # Misc
        """
        for i in range(20):
            random_x = randint(1000,2000)
            random_y = randint(1000,2000)
            Tree((random_x, random_y), self.all_sprites)
        """
        self.end_point = (2392, 818)
        self.show_chat = [1]        
        self.welcome_chatbox = Chatbox(game, "Developer No. 2",
                               ("Welcome to Catopia.","Use W, A, S and D to move around.","Press E while standing near NPCs to talk tothem."))

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
        self.welcome_chatbox.update(actions, self.show_chat)
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)
        self.test_hint_NPC.chatters()
        self.test_task_NPC.chatters()
        if self.show_chat[0] == 1:
            self.welcome_chatbox.print()