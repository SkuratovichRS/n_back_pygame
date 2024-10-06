from gtts import gTTS

from app.constants import LETTERS, SOUNDS_PATH

for letter in LETTERS:
    tts = gTTS(text=letter, lang='en')
    tts.save(f'{SOUNDS_PATH}/{letter}.mp3')
