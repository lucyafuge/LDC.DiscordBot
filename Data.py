from decouple import config

TokenDiscord = config('TokenDiscord',default='')
TwitchAccessToken = config('TwitchAccessToken',default='')
TwitchClientID = config('TwitchClientID',default='')
TwitchSecretKey = config('TwitchSecretKey',default='')
TwitchUsersLoggins = config('TwitchUsersLoggins',default='')
TwitcGeneralChannelID = config('TwitcGeneralChannelID',default=0)

TwitchStreamUpTitle = f"<@&1196904223800033360>, Стрим начался <:lostdice:1196896851811647549>, кубики, ждем вас!"
TwitchStreamUpMessage = f"{TwitchStreamUpTitle} Трансляция доступна по ссылке: https://www.twitch.tv/lostdiceclub"