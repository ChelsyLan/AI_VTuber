import time
import re

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent


def tiktok_livechat(username, blacklist=["Nightbot", "streamelements"]):
    # Create the TikTokLiveClient with the provided username
    client = TikTokLiveClient(unique_id=username)

    # Event handler for connection
    @client.on(ConnectEvent)
    async def on_connect(event: ConnectEvent):
        print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

    # Event handler for comments
    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        global chat
        try:
            # Ignore chat from blacklisted users
            if event.user.nickname in blacklist:
                return
            # Process and format chat message
            chat_raw = re.sub(r':[^\s]+:', '', event.comment) 
            chat_raw = chat_raw.replace('#', '')
            chat = f'viewer named {event.user.nickname} say {chat_raw}'
            print(chat)
            time.sleep(1)
        except Exception as e:
            print(f"Error processing comment: {e}")

    # Event handler for gifts
    @client.on(GiftEvent)
    async def on_gift(event: GiftEvent):
        global chat
        try:
            gift_message = (
                f"viewer named {event.user.nickname} sent a gift: with {event.gift.name} (worth {event.value} coins)"
            )
            chat = gift_message
            print(chat)
            time.sleep(1)
        except Exception as e:
            print(f"Error processing gift: {e}")

    # Start the client and connect to TikTok live chat
    client.run()
