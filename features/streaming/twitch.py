import asyncio
from dotenv import dotenv_values

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent, TwitchAPIException
from twitchAPI.chat import Chat, ChatMessage, EventData


def start_twitch_livechat():
    twitch = asyncio.run(authenticate_twitch_browser())
    asyncio.run(listen_twitch_chat(twitch))


async def listen_twitch_chat(twitch: Twitch):
    # create chat instance
    chat = await Chat(twitch)
    
    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    
    # start the bot
    chat.start()
    
    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


async def authenticate_twitch_browser():
    target_scope = [AuthScope.BITS_READ, AuthScope.CHAT_EDIT, AuthScope.CHAT_READ]
    
    config = dotenv_values(".env")
    twitch_app_id = config.get("TWITCH_APP_ID")
    twitch_app_secret = config.get("TWITCH_APP_SECRET")
    token = config.get("TWITCH_APP_TOKEN")
    refresh_token = config.get("TWITCH_REFRESH_TOKEN")
    
    # initialize the twitch instance
    # this will by default also create a app authentication for you
    twitch = await Twitch(twitch_app_id, twitch_app_secret)
    
    print("Authenticating Twitch with the token...")
    try:
        # add User authentication
        await twitch.set_user_authentication(token, target_scope, refresh_token)
        
        return twitch
    except Exception as e:
        print("Twitch authentication by token in `.env` failed. Trying with the secret key.")
        print(e)
    
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    
    # this will open your default browser and prompt you with the twitch verification website
    print("Redirecting to browser for authenticate Twitch...")
    print("This does not work in a server that cannot open a browser.")
    token, refresh_token = await auth.authenticate()
    
    # add User authentication
    await twitch.set_user_authentication(token, target_scope, refresh_token)
    
    return twitch


async def on_ready(ready_event: EventData):
    # TARGET_CHANNEL = 'teekeks42'
    TARGET_CHANNEL = "#grapplr"
    
    print(f'Bot is ready for work, joining channel: {TARGET_CHANNEL}')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


if __name__ == "__main__":
    twitch = asyncio.run(authenticate_twitch_browser())
    asyncio.run(listen_twitch_chat(twitch))
