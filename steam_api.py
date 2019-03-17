import requests
from enum import Enum


class Status(Enum):
    Unknown = 0
    Factorio = 1
    Insurgency = 2
    Offline = 3
    Online = 4
    Away = 5

    def __str__(self):
        x = ["未知", "我今晚有事.jpg", "突突.gif", "离线", "在线", "挂机"]
        return x[self.value]


class SteamAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        r = requests.get("https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/",
                         {
                             'key': self.api_key,
                             'appid': 427520
                         })
        if r.status_code != 200:
            raise RuntimeError('Steam API Error, errno:%d' % r.status_code)

    def query_user_status(self, steam64id):
        """

        :param steam64id: 玩家的SteamID64
        :return: None:未找到玩家
        """
        r = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
                         {
                             'key': self.api_key,
                             'steamids': steam64id
                         })
        r.raise_for_status()
        resp = r.json()
        if len(resp['response']['players']) == 0:  # 未找到玩家
            return None
        resp = resp['response']['players'][0]
        if 'gameextrainfo' in resp:  # 正在玩游戏
            if resp['gameid'] == "427520":  # 有事.jpg
                return Status.Factorio
            elif resp['gameid'] == "222880":  # 突突.jpg
                return Status.Insurgency
            else:
                return resp['gameextrainfo']
        if resp['personastate'] in [1, 5, 6]:
            return Status.Online
        elif resp['personastate'] == 0:
            return Status.Offline
        elif resp['personastate'] in [2, 3, 4]:
            return Status.Away
        return Status.Unknown
