import requests
import Data
 
class Stream:
 
    def __init__(self, title, streamer, game, viewer_count):
        self.title = title
        self.streamer = streamer
        self.viewer_count = viewer_count
        self.game = game
        
# getting the auth token from the twitch API
def getOAuthToken():
    body = {
        'client_id': Data.TwitchClientID,
        'client_secret': Data.TwitchSecretKey,
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
 
    #data output
    keys = r.json()
    return keys['access_token']
 
def checkIfLive(channel):
    # Calling the twitch api to check if a specific is live
    url = "https://api.twitch.tv/helix/streams?user_login=" + channel
    token = getOAuthToken()
 
    HEADERS = {
        'Client-ID': Data.TwitchClientID,
        'Authorization': 'Bearer ' + token
    }
 
    try:
        
        req = requests.get(url, headers=HEADERS)
        
        res = req.json()
 
        if len(res['data']) > 0: # the twitch channel is live
            data = res['data'][0]
            title = data['title']
            streamer = data['user_name']
            game = data['game_name']
            viewer_count = data['viewer_count']
            stream = Stream(title, streamer, game, viewer_count)
            return stream
        else:
            return "OFFLINE"
    except Exception as e:
        return "An error occured: " + str(e)