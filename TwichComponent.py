from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import StreamOnlineEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope
import asyncio
import websocket
import _thread
import time
import rel
import Data

async def twitch_example():
	twitch = await Twitch(Data.TwitchClientID, Data.TwichSecretKey)
	user = await first(twitch.get_users(logins=Data.TwichUsersLoggins))
	print(user.id)

TARGET_USERNAME = Data.TwichUsersLoggins
EVENTSUB_URL = 'https://localhost'
APP_ID = Data.TwitchClientID
APP_SECRET = Data.TwichSecretKey
TARGET_SCOPES = [AuthScope.USER_BOT]





async def eventsub_webhook_example():
	twitch = await Twitch(APP_ID, APP_SECRET)
	helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
	await helper.bind()
		
	user = await first(twitch.get_users())
		
	eventsub = EventSubWebsocket(twitch)
	#await eventsub.unsubscribe_all()
	#eventsub.start()
	topic = ""
	
	async def on_stream_online(data: StreamOnlineEvent):
		print(f'Stream is up!')
		#if(topic != ""):
		#	await eventsub.unsubscribe_topic(topic)
		#else:
		#	print("[ERROR] topic is null")
		#await subscribe_stream_online()
	
	async def subscribe_stream_online():
		topic = await eventsub.listen_stream_online(user.id, on_stream_online)
		return topic

	##topic = await subscribe_stream_online()
	websocket.enableTrace(True)
	
	def on_message(ws, message):
		print(message)

	def on_error(ws, error):
		print(error)

	def on_close(ws, close_status_code, close_msg):
		print("### closed ###")

	def on_open(ws):
		print("Opened connection")

	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://eventsub.wss.twitch.tv/ws",
								on_open=on_open,
								on_message=on_message,
								on_error=on_error,
								on_close=on_close)
	
	ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
	rel.signal(2, rel.abort)  # Keyboard Interrupt
	rel.dispatch()

	#try:
	#	input('press Enter to shut down...')
	#finally:
	#	await eventsub.stop()
	#	await twitch.close()
	print('done')



# run this example
def run():
	#asyncio.run(twitch_example())
	asyncio.run(eventsub_webhook_example())