from gtts import gTTS
import speech_recognition as sr
import os

# Initializers
r = sr.Recognizer()
mic = sr.Microphone()

# Adjust based on current environment, start high and reduce
# until good results found, good values between 50 and 4000
r.energy_threshold = 500

# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0


# Uses gTTS to say the string 'response' in language 'language'
def say(response, language):
    obj = gTTS(text=response, lang=language, slow=False)
    obj.save("audio.mp3")
    os.system("mpg123 audio.mp3")


# Uses SpeechRecognition to translate a user response to text. Returns text
# from user response
def listen():
    with mic as source:
        # r.energy_threshold = 2500
        audio = r.listen(source)

    cur_text = r.recognize_google(audio)
    return cur_text


while 1:

    try:
        command = listen()
        print(command)

        if "tutorial" in command:   # Starts tutorial
            say("tutorial", languages[current_language])
        elif "stash" in command:    # Places character(s) into current guess
            say("stash", languages[current_language])
        elif "delete" in command:   # Deletes all characters from stash
            say("delete", languages[current_language])
        elif "read" in command:
            if "guess" in command or "gas" in command or "guest" in command:
                if "one" in command or "won" in command or "1" in command:
                    say("read first guess", languages[current_language])
                elif "two" in command or "to" in command or "2" in command or "too" in command:
                    say("read second guess", languages[current_language])
                elif "three" in command or "3" in command:
                    say("read third guess", languages[current_language])
                elif "four" in command or "for" in command or "4" in command:
                    say("read fourth guess", languages[current_language])
                elif "five" in command or "5" in command:
                    say("read fifth guess", languages[current_language])
                else:
                    say("Read current guess not yet submitted", languages[current_language])
            elif "semi" in command:
                say("read semi correct guesses by character", languages[current_language])
            elif "wrong" in command:
                say("read incorrect guesses by character", languages[current_language])
            else:
                say("invalid command", languages[current_language])
        elif "submit" in command:
            say("submit", languages[current_language])
        else:
            say("invalid command", languages[current_language])

    except Exception as e:
        print("exception: " + repr(e))

