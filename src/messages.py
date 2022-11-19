
ABOUT = ["", 
         "Welcome to World-le: the S3N1OR SQU4D’s accessible version of the",
         "popular New York Times’s word-guessing game. This game was developed",
         "in the Fall of 2022 for our CSC 355: Human Computer Interactions final project.",
         " ",
         "Our Mission",
         "At the start of our process, we noticed that a number of Wordle’s qualities",
         "were inaccessible. First, while versions of Wordle exist in languages",
         "other than English online, the New York Times’s game is only available in",
         "English, thereby excluding non-English speakers. Second, the color scheme is",
         "inaccessible to the color blind community; the high contrast feature is even",
         "insufficient. Additionally, there is no way for members of the Blind community",
         "to play. Finally, physical impairments deter those unable to use their hands",
         "from playing the game.",
         " ",
         "With these shortcomings in mind, we set out to make Wordle accessible to the",
         "visually and physically impaired communities, as well as non-English speakers.",
         "We have done this by implementing a hands-free option for users to play using",
         "only their voice, as well as a language option for players to choose which",
         "language they would like play in. In addition to our accessibility features,", 
         "we also added a color picker to allow users customize their gaming experience.",
         "With these implementations, we hope that this version of our World-le can truly",
         "be “Wordle for the world.”",
         " ",
         "Meet the S3N1OR SQU4D",
         "Summer Martin is a ",
         " ",
         "Max Parrone is a ",
         " ",
         "Kyla Ramos is a ",
         " ",
         "Caroline Francesconi is a senior at The College of New Jersey majoring in",
         "statistics and minoring in Women’s, Gender, and Sexuality Studies. She has", 
         "really enjoyed learning about accessible design in HCI, and hopes that her", 
         "team’s final project engages individuals with differing abilities in a", 
         "positive way. Caroline’s favorite five-letter word is “pasta.”"]

INSTRUCTIONS = ["How to Play Using a Keyboard:",
                "- Using your computer’s keyboard or the one on the screen, guess a five letter word.",
                "- Press the delete key to remove a letter.",
                "- Press the enter key to submit a guess.",
                "- Letters in the correct position will appear green, as show here:"] 

INSTRUCTIONS2 = ["- Letters in the word, but in the incorrect position will appear yellow, as shown here:"]
                
INSTRUCTIONS3 = ["- Incorrect letters will appear gray, as shown above." ,
                 "- You have six attempts to guess the secret word."]
                
AUDIO_INSTRUCTIONS = [" ",
                    "How to Play Hands-Free:",
                    "- To activate hands-free mode, say <command>.",
                    "- To disable hand-free mode, say “disable.”",
                    "- To spell a word, you can either stash five individual letters,", 
                    "  or stash a five-letter word. For example, “stash s, stash t, stash a,",
                    "  stash r, stash t” and “stash start” both stash the word, start.",
                    "- To submit a stashed word, say “submit.”",
                    "- To delete the most recently stashed letter, say “delete.”",
                    "- To clear your stash, say “clear.”",
                    "- To replace a letter, say “replace,” followed by the character you want to replace,",
                    "  the word “with,” and the new character. For example, “replace p with t” would turn",
                    "  the word “pails” to “tails”.",
                    "- To hear a particular guessed word, say “read guess” followed by the number of the",
                    "  guessed word. For example, “read guess one” will read out your first guessed word.",
                    "- To hear your semi-correct letters, say “read semi.”",
                    "- To hear your previous wrong guessed words, say “read wrong.”",
                    "- To play again after finishing a game, say “play again.”",]    

COLOR_INSTRUCTIONS = ["On this screen you can input colors using their hexidecimal code.", 
                    "Don't worry if you're not sure how to do this, you can also change the colors from",  
                    "the main game screem by clicking on the color key.", 
                    "From there you can pick from assorted pre-set colors and themes.", "", "", ""]

SPACES = [" ", " "]

# Long sections of text used for instructing hands-free user
STARTUP = "Welcome to wordle for the world, to activate the hands free version of the program, press " \
          "the space bar twice"
ACTIVATED = "Audio interface activated, if you need help with playing the game, say: tutorial. " \
            "To disable audio mode say disable."
WORDLE_TUTORIAL = "Insert wordle tutorial here"
HANDSFREE_TUTORIAL = "Insert handsfree tutorial here"
STASH_TUTORIAL = "Insert stash tutorial/example here"
CLEAR_TUTORIAL = "The command clear will delete all the letters in your current guess stash"
READ_TUTORIAL = "Insert read tutorial/example here"
REPLACE_TUTORIAL = "Insert replace tutorial/example here"
SUBMIT_TUTORIAL = "Insert submit tutorial/example here"

volume_warning = "handsfree mode hears best with low background noise. If you're wearing headphones, repeat " \
                 "your volume command to confirm."
