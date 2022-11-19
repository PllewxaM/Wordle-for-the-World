# 🔠 Wordle for the World 🌎

## About
Welcome to World-le: the S3N1OR SQU4D’s accessible version of the popular New York Times’s word-guessing game. This game was developed in the Fall of 2022 for our CSC 355: Human Computer Interaction final project.

### Our Mission
At the start of our process, we noticed that a number of Wordle’s qualities were inaccessible. First, while versions of Wordle exist in languages other than English online, the New York Times’s game is only available in English, thereby excluding non-English speakers. Second, the color scheme is inaccessible to the color blind community; the high contrast feature is even insufficient. Additionally, there is no way for members of the Blind community to play. Finally, physical impairments deter those unable to use their hands from playing the game. 

With these shortcomings in mind, we set out to make Wordle accessible to the visually and physically impaired communities, as well as non-English speakers. We have done this by implementing a hands-free option for users to play using only their voice, as well as a language option for players to choose which language they would like play in. In addition to our accessibility features, we also added a color picker to allow users customize their gaming experience. With these implementations, we hope that this version of our World-le can truly be “Wordle for the world.”
<br></br>
## Important links:

* [Lucid Chart](https://lucid.app/lucidchart/4735d828-7099-46f1-9da6-7ea53dc85e6f/edit?viewport_loc=107%2C-53%2C2208%2C1298%2C0_0&invitationId=inv_0f5a4729-5154-41bb-9f9f-4aaded83f005)

* [Assignment PDF](FinalProjectAssignment.pdf)

* [Shared Google Drive](https://drive.google.com/drive/folders/0ABLGOc9WOIvZUk9PVA?ths=true)
<br></br>
## Handsfree Instructions
To activate hands-free mode, press the spacebar twice. <br />To disable hand-free mode, say 
> "*Disable*"

### Stash
To spell a word, either stash five individual letters, or stash a five-letter word. Below are two ways to stash the word "start":
>“*Stash* S"<br />"*Stash* T"<br />"*Stash*  A"<br />"*Stash* R"<br />"*Stash* T”

>“*Stash* START” 

### Replace
Replace command allows the player to exchange one letter in the word for another. 
>"*Replace* x *with* y"

For example, the following command could turn the word “pails” to “tails”.
>“*Replace* P *with* T” 

The player can also replace a letter at a certain index. For example, the following command could turn "APPLE" to "AMPLE"
>"*Replace* 2 *with* M"

### Delete and Clear
The following command deletes the most recently stashed letter:
>"*Delete*"

The following command clears all letters from the stash:
>"*Clear*"

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

### Submit
To submit a stashed guess, say
>"*Submit*"

### Play Again
Command used to restart the game after game is complete:
>“*Play Again.*”

### Music Control

To change the volume of the background music, say "volume", followed by a number between 0 and 10.
>"*Volume **(1-10)***"

To change the background music to find your favorite of the 5 different options, use the following command:
>"*Song **(1-5)***"

