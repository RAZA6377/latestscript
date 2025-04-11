# Vote System
import bascenev1 as bs
import babase as ba
import time
from bascenev1 import chatmessage as cmsg
import yaml


class VoteHandler:
    def __init__(self):
        self.vote_available = ["ffa", "teams", "space", "end"]
        self.started = False
        self.ongoing_vote = None
        self.voters = []
        
    def error(self, msg, cid: int):
        bs.screenmessage(msg, color=(1,0,0), transient=True, clients=[cid])
        
    def success(self, msg, cid: int):
        bs.screenmessage(msg, color=(0,0.5,0.5), transient=True, clients=[cid])
        
    def get_info(self, cid: int):
        info = {}
        for i in bs.get_game_roster():
            if i['client_id'] == clientID:
                info['ds'] = i['display_string']
                info['aid'] = i['account_id']
                info['p'] = i['players']
                break
        return info
        
    def resetvote(self):
        self.started = False
        self.ongoing_vote = None
        self.voters.clear()
        print("Vote Reseted")
        
    def vote_need(self, players):
        if players == 2:
            return 1
        elif players == 3:
            return 2
        elif players == 4:
             return 2
        elif players == 5:
             return 3
        elif players == 6:
             return 3
        elif players == 7:
             return 4
        elif players == 8:
             return 4
        elif players == 10:
             return 5
        else:
             return players - 5

    def get_party_mode(self):
        path = "/home/ubuntu/dead/config.yaml"
        with open(path, "r") as file:
            data = yaml.safe_load(file)
        if "Teams" in data["party_name"]:
            return "teams"
        else:
            return "ffa"
             
    def vote_success(self):
        if self.ongoing_vote == "ffa":
            