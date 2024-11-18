import time
import re

import pytchat

# function to capture livechat from youtube
def youtube_livechat(video_id, chat="", blacklist=["Nightbot", "streamelements"]):
        # global chat

        live = pytchat.create(video_id=video_id)
        while live.is_alive():
        # while True:
            try:
                for c in live.get().sync_items():
                    # Ignore chat from the streamer and Nightbot, change this if you want to include the streamer's chat
                    if c.author.name in blacklist:
                        continue
                    # if not c.message.startswith("!") and c.message.startswith('#'):
                    if not c.message.startswith("!"):
                        # Remove emojis from the chat
                        chat_raw = re.sub(r':[^\s]+:', '', c.message)
                        chat_raw = chat_raw.replace('#', '')
                        # chat_author makes the chat look like this: "Nightbot: Hello". So the assistant can respond to the user's name
                        chat = 'viewer named ' + c.author.name + ' say ' + chat_raw
                        
                        print(chat)
                        
                    time.sleep(1)
            except Exception as e:
                print("Error receiving chat: {0}".format(e))
