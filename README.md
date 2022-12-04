# 🔠 Wordle for the World 🌎
# Table of Contents
1. [About](#about)
2. [Our Mission](#mission)
3. [Installation](#install)
4. [Accessibility Features](#features)
5. [Important Links](#links)
6. [Handsfree Instructions](#handsfree)
7. [File Organization](#files)
8. [Credits](#credits)

## About <div id='about'/>
Welcome to World-le: the S3N1OR SQU4D’s accessible version of the popular New York Times’s word-guessing game. This game was developed in the Fall of 2022 for our CSC 355: Human Computer Interaction final project.

## Our Mission <div id='mission'/>
At the start of our process, we noticed that a number of Wordle’s qualities were inaccessible. First, while versions of Wordle exist in languages other than English online, the New York Times’s game is only available in English, thereby excluding non-English speakers. Second, the color scheme is inaccessible to the color blind community; the high contrast feature is even insufficient. Additionally, there is no way for members of the Blind community to play. Finally, physical impairments deter those unable to use their hands from playing the game. 

With these shortcomings in mind, we set out to make Wordle accessible to the visually and physically impaired communities, as well as non-English speakers. We have done this by implementing a hands-free option for users to play using only their voice, as well as a language option for players to choose which language they would like play in. In addition to our accessibility features, we also added a color picker to allow users customize their gaming experience. With these implementations, we hope that this version of our World-le can truly be “Wordle for the world.”

<br>

***

## Installation Instructions <div id='install'/>

<details>
  <summary> WINDOWS INSTALLATION INSTRUCTIONS </summary>
<p>

***
Install python (Windows installer (64-bit)) using this link :
>https://www.python.org/downloads/release/python-3110/

Ensure you have pygame version 2.1.3 by using the command :

     pip install pygame

- Check the version using :

      pip show pygame

 - To update, use :

       python -m pip install pygame --upgrade --pre

Install pygame-menu using the command :

     pip install pygame-menu -U

Install PyObjC using the command :

     pip install PyObjC

For speech recognition install Google’s Speech Recognition package using the command :

     pip install SpeechRecognition  

For speech generation use Google’s gTTS Python package. To install the Python package type: 

     pip install gTTS 

Install playsound version 1.2.2 using the command :

     pip install playsound==1.2.2

If playsound is already installed use this command first :

     pip uninstall playsound

You must also download the file libmpg123-0.dll from the following link and place it inside your System32 folder :
>Link: https://www.dll-files.com/libmpg123-0.dll.html

>Folder Location: Search "System32" in your C: drive

***

</details>

<br>

<details>
  <summary> MACOS/LINUX INSTALLATION INSTRUCTIONS </summary>
<p>

This is where you write the instructions :P

Ensure you have pygame by using the command:

     pip install pygame

Install pygame-menu using the command :

     pip install pygame-menu

Install PyObjC using the command :

     pip install PyObjC

For speech recognition install Google’s Speech Recognition package using the command :

     pip install SpeechRecognition  

For speech generation use Google’s gTTS Python package. To install the Python package type: 

     pip install gTTS 

Install playsound using the command :

     pip install playsound


</details>


<br>

<details>
  <summary> HOW TO RUN</summary>
<p>

Choose a folder in which you would like to download the program. In a terminal, navagate to this folder.  

Run the command:

     git clone https://github.com/PllewxaM/Wordle-for-the-World.git

Navagate to the source code folder using the command

     cd .\Wordle-for-the-World\src\

Run the program using the command:

     python wordle.py

</details>

***
<br>

## File Organization <div id='files'/>
<details>
  <summary>Click to see all files</summary> 
<p>
  
1. **wordle.py** - main program file that contains the main game function, the main menu and mini menu controls. It also contains the audio interface functions and the user word guess controls:
   - Start up menu - the main control for the menu which opens on running the program. This function uses menu helper functions to draw the sub page content and themes
   - Main game loop - this is the main function of the program which controls how the game functions based on user actions such as input, mouse clicks and button presses
   - User input controls - controls when the user inputs a new letter or word into the program. Controls the removal of letters, and checking the status of the user's guess
   - Audio interface - functions which control the audio interface and the user voice input
   - Mini Menu functionality - controls the mini color menus and the font menu controls
2. **mpg123.exe** - supports the audio interface functionality
   - Used for windows versions to access the mpg123 for audio file generation
3. **helpers** folder - contains additional python program files which contain helper functions used by the main program
   - **draw.py** - contains functions which help to draw the user interface, mini menus (color and font menus) and the user input onto the game board
   - **menu.py** - contains functions which aid in the creation of additional menu pages, the menu themes and drawing of the menu pages 
   - **constants.py** - contains all of the constants which are used accross the different python files in the program. All constants are contained in this file
   - **messages.py** - defines the large chunks of text used in the Instructions and Menus
   - **classes.py** - this file contains the classes used to define the keyboard key objects and the letter objects used in the program
4. **assets** folder - contains program assests such as images used in the UI and the font files used in the program
   - **.png** / **.jpg** files - these .png and .jpg files are images used in the instruction pages and the navigation bar
   - **fonts** folder - this is the folder which contains the font files
     - **.oft** / **.ttf** files - these are the fonts which are used in the program and are used when the user changes the font of the UI contents
5. **sound** folder - contains the sound files used throughout the program
   - **background_music** folder - contains all of the background music files
   - **effects** folder - contains the sounds effects used to indicate correct/semi correct/worng letter placement and other sound effects used throughout the program
   - **untrimmed** - contains unedited sound effects
6. **word_files** folder - contains a list of five letter words for each available language
</details>

<br>

## Accessibility Features <div id='features'/>

* High contrast mode
* Customizable colors, font/font size
* Language selection
* Screen reader
* Speech interpreter

<br>

## Handsfree Game Instructions <div id='handsfree'/>
<details>
  <summary>Click to see how to use our Handsfree Wordle Interface </summary> 
<p>

***
### Activate and Disable

To activate hands-free mode, press the spacebar twice. <br />To disable hand-free mode, say 
> "**Disable**"

***
### Stash
To spell a word, either stash five individual letters, or stash a five-letter word. Below are two ways to stash the word "START":
>“**Stash** S"<br />"**Stash** T"<br />"**Stash**  A"<br />"**Stash** R"<br />"**Stash** T”

>“**Stash** START” 

***
### Replace
Replace command allows the player to exchange one letter in the word for another. 
>"**Replace** x **with** y"

For example, the following command could turn the word “PAILS” to “TAILS”.
>“**Replace** P **with** T” 

The player can also replace a letter at a certain index. For example, the following command could turn "APPLE" to "AMPLE"
>"**Replace** 2 **with** M"

***
### Delete and Clear

The following command deletes the most recently stashed letter:
>"**Delete**"

The following command clears all letters from the stash:
>"**Clear**"

***
### Read
To hear the letters in your current stash, say
>"**Read Guess**"

To hear previous guesses:
>"**Read Guess** (1-5)"

For example, the following command will read out your first guessed word.
>“**Read Guess** 1” 

The following command will read out all letters guessed that are in the correct word, but not in the correct place in one of your guesses:
> "**Read Semi**"

This command will read out all letters guessed that are not in the correct word.
> "**Read Wrong**"

***
### Submit
To submit a stashed guess, say
>"**Submit**"

***
### Play Again
Command used to restart the game after game is complete:
>“**Play Again.**”

***
### Music Control

To change the volume of the background music, say "volume", followed by a number between 0 and 10.
>"**Volume** (1-10)"

To change the background music to find your favorite of the 10 different options, use the following command:
>"**Song** (1-10)"

</details>

<br>

## Credits <div id='credits'/>

This project was developed by [Summer Martin](https://github.com/martis36), [Maxwell Parrone](https://github.com/PllewxaM),
[Kyla Ramos](https://github.com/kyla0509), and [Caroline Francesconi](https://github.com/CarolineFrancesconi). 

Some resources that were helpful in developing this project include: 

* PyGame Templates: https://gist.github.com/MatthewJA/7544830

* PyGame Keydown event example: https://stackoverflow.com/questions/25494726/how-to-use-pygame-keydown-to-execute-something-every-time-through-a-loop-while-t

* PyGame Drawing Shapes: https://www.geeksforgeeks.org/pygame-drawing-objects-and-shapes/

* Wordle Example: https://github.com/plemaster01/LeMasterTechYT

* Wordle Example 2: https://github.com/baraltech/Wordle-PyGame

* PyGame Creating a Menu: https://github.com/russs123/pygame_tutorials/tree/main/Menu 
