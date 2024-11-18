### Python Default ###
import time
import threading

### Audio ###
import sounddevice as sd

### Internal ###
from features.agent import get_openai_answer
from features.vtuber import VTuber
from features.openai_t2t import get_openai_client
from features.streaming.tiktok import tiktok_livechat
from features.streaming.twitch import start_twitch_livechat
from features.streaming.youtube import youtube_livechat

# to help the CLI write unicode characters to the terminal
# sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

client = get_openai_client()

conversation = []
mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
is_Speaking = False
owner_name = "Melting-LLM Admin"
blacklist = ["Nightbot", "streamelements"]

def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:
        # If the assistant is not speaking, and the chat is not empty, and the chat is not the same as the previous chat
        # then the assistant will answer the chat
        chat_now = chat
        if is_Speaking == False and chat_now != chat_prev:
            # Saving chat history
            print('<<processing>>')
            conversation.append({'role': 'user', 'content': chat_now})
            chat_prev = chat_now
            get_openai_answer()
        time.sleep(1)
        # await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep to not block the event loop

def main():
    print(sd.query_devices())
    try:
        mode = input("Mode (1-Mic, 2-Youtube Live, 3-Twitch Live, 4-Tiktok Live, 5-Text): ")
        
        if mode == "1":
            vtuber = VTuber(openai_client=client)
            vtuber.start_voice_conversations()
        
        elif mode == "2":
            live_id = input("Livestream ID: ")
            t = threading.Thread(target=preparation)
            t.start()
            youtube_livechat(live_id)
        
        elif mode == "3":
            print("To use this mode, make sure to change utils/twitch_config.py to your own config")
            t = threading.Thread(target=preparation)
            t.start()
            start_twitch_livechat()
        
        elif mode == "4":
            live_username = input("TikTok Livestream Username: ")
            t = threading.Thread(target=preparation)
            t.start()
            tiktok_livechat(live_username)

        elif mode == "5":
            vtuber = VTuber(openai_client=client)
            vtuber.start_text_conversations()
    
    except KeyboardInterrupt:
        t.join()
        print("Stopped")

if __name__ == "__main__":
    main()
