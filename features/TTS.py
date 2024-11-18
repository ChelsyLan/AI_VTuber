import requests
import urllib.parse
# from utils.katakana import *


def voicevox_tts(text: str, speaker_id=3, output_path="output.wav"):
    # You need to run VoicevoxEngine.exe or voicevox docker first before running this script
    voicevox_url = 'http://localhost:50021'
    # Convert the text to katakana. Example: ORANGE -> オレンジ, so the voice will sound more natural
    # katakana_text = katakana_converter(tts)
    # You can change the voice to your liking. You can find the list of voices on speaker.json
    # or check the website https://voicevox.hiroshiba.jp
    params_encoded = urllib.parse.urlencode({'text': text, 'speaker': speaker_id})
    request = requests.post(f'{voicevox_url}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{voicevox_url}/synthesis?{params_encoded}', json=request.json())

    with open(output_path, "wb") as outfile:
        outfile.write(request.content)

if __name__ == "__main__":
    voicevox_tts()
