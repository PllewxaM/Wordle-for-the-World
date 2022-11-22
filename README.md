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

## Installation Instructions <div id='install'/>


## Accessibility Features <div id='features'/>

* High contrast mode
* Customizable colors, font/font size
* Language selection
* Screen reader
* Speech interpreter

## Important links: <div id='links'/>

* [Lucid Chart](https://lucid.app/lucidchart/4735d828-7099-46f1-9da6-7ea53dc85e6f/edit?viewport_loc=107%2C-53%2C2208%2C1298%2C0_0&invitationId=inv_0f5a4729-5154-41bb-9f9f-4aaded83f005)

* [Assignment PDF](FinalProjectAssignment.pdf)

* [Shared Google Drive](https://drive.google.com/drive/folders/0ABLGOc9WOIvZUk9PVA?ths=true)

<div id='handsfree'/>

## Handsfree Game Instructions
<details>
  <summary>Click to see how to use our Handsfree Wordle Interface </summary> 
<p>

***
### Activate and Disable

To activate hands-free mode, press the spacebar twice. <br />To disable hand-free mode, say 
> "*Disable*"

***
### Stash
To spell a word, either stash five individual letters, or stash a five-letter word. Below are two ways to stash the word "start":
>“*Stash* S"<br />"*Stash* T"<br />"*Stash*  A"<br />"*Stash* R"<br />"*Stash* T”
>“*Stash* START” 

***
### Replace
Replace command allows the player to exchange one letter in the word for another. 
>"*Replace* x *with* y"

For example, the following command could turn the word “pails” to “tails”.
>“*Replace* P *with* T” 

The player can also replace a letter at a certain index. For example, the following command could turn "APPLE" to "AMPLE"
>"*Replace* 2 *with* M"

***
### Delete and Clear

The following command deletes the most recently stashed letter:
>"*Delete*"

The following command clears all letters from the stash:
>"*Clear*"

***
### Read
To hear the letters in your current stash, say
>"*Read Guess*"

To hear previous guesses:
>"*Read Guess* x"

For example, the following command will read out your first guessed word.
>“*Read Guess **(1-5)***” 

The following command will read out all letters guessed that are in the correct word, but not in the correct place in one of your guesses:
> "*Read Semi*"

This command will read out all letters guessed that are not in the correct word.
> "*Read Wrong*"

***
### Submit
To submit a stashed guess, say
>"*Submit*"

***
### Play Again
Command used to restart the game after game is complete:
>“*Play Again.*”

***
### Music Control

To change the volume of the background music, say "volume", followed by a number between 0 and 10.
>"*Volume **(1-10)***"

To change the background music to find your favorite of the 10 different options, use the following command:
>"*Song **(1-10)***"

</details>
</details>

## File Organization <div id='files'/>
<details>
  <summary>Click to see all files</summary> 
<p>
  
1. wordle.py - main file that contains game functions:
   - Audio interface
   - Text interface
   - Drawing Elements of the UI
   - Menu functionality
2. mpg123.exe - supports the audio interface functionality
   - Used for windows versions
3. messages.py - defines the large chunks of text used in the Instructions and Menus
	@@ -143,4 +147,4 @@ The main file of this program is wordle.py. It houses all of the game functions
</details>


## Credits <div id='credits'/>

This project was developed by [Summer Martin](https://github.com/martis36), [Max Perrone](https://github.com/PllewxaM), [Kyla Ramos](https://github.com/kyla0509), and [Caroline Francesconi](https://github.com/CarolineFrancesconi). 

Some resources that were helpful in developing this project include: 

* PyGame Templates: https://gist.github.com/MatthewJA/7544830

* PyGame Keydown event example: https://stackoverflow.com/questions/25494726/how-to-use-pygame-keydown-to-execute-something-every-time-through-a-loop-while-t

* PyGame Drawing Shapes: https://www.geeksforgeeks.org/pygame-drawing-objects-and-shapes/

* Wordle Example: https://github.com/plemaster01/LeMasterTechYT

* Other Wordle Example: https://github.com/baraltech/Wordle-PyGame

* PyGame Creating a Menu: https://github.com/russs123/pygame_tutorials/tree/main/Menu 
