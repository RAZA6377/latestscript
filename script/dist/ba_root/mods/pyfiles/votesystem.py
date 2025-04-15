import bascenev1 as bs
import babase as ba
import time
from bascenev1 import chatmessage as cmsg
from bascenev1 import broadcastmessage as bmsg
import yaml


class VoteHandler:
    def __init__(self):
        self.vote_available = ["ffa", "teams", "space", "end"]
        self.started = False
        self.ongoing_vote = []
        self.voters = []
        self.start_time = time.time()

    def success(self, msg, dm=False, cid=None):
        if dm:
            bmsg(msg, transient=True, color=(0, 1, 1), clients=[cid])
        else:
            bmsg(msg, color=(0, 1, 1))

    def error(self, msg, dm=False, cid=None):
        if dm:
            bmsg(msg, transient=True, color=(1, 0, 1), clients=[cid])
        else:
            bmsg(msg, color=(1, 0, 1))

    def get_info(self, cid: int):
        info = {}
        for i in bs.get_game_roster():
            if i['client_id'] == cid:
                info['ds'] = i['display_string']
                info['pb'] = i['account_id']
                info['p'] = i['players']
                break
        return info

    def resetvote(self):
        self.started = False
        self.ongoing_vote.clear()
        self.voters.clear()
        self.start_time = time.time()
        print("Vote Reseted")

    def vote_need(self, players):
        if players <= 2:
            return 1
        elif players <= 4:
            return 2
        elif players <= 6:
            return 3
        elif players <= 8:
            return 4
        elif players == 10:
            return 5
        else:
            return players - 5

    def get_party_mode(self):
        path = "config.yaml"
        with open(path, "r") as file:
            data = yaml.safe_load(file)
        if "Teams" in data.get("party_name", ""):
            return "teams"
        else:
            return "ffa"

    def vote_success(self):
        if not self.ongoing_vote:
            self.error("No ongoing vote to process")
            return

        vote = self.ongoing_vote[-1]
        if vote == "ffa":
            if self.get_party_mode() == "ffa":
                self.error("Party Mode Is Already FFA")
            else:
                cmsg("/ffa")
        elif vote == "teams":
            if self.get_party_mode() == "teams":
                self.error("Party Mode Is Already Teams")
            else:
                cmsg("/teams")
        elif vote == "space":
            mp = int(bs.get_foreground_host_session().max_players)
            size = mp + 1
            cmsg(f"/mp {size}")
        elif vote == "end":
            with bs.get_foreground_host_activity().context:
                bs.get_foreground_host_activity().end_game()
                bs.broadcastmessage("Ending Current Activity", color=(0, 0.5, 0.5))
        self.resetvote()

    def end_vote(self):
        if not self.ongoing_vote:
            self.error("No ongoing vote to end")
            return
        vote_name = self.ongoing_vote[-1]
        self.error(f"Timer For {vote_name} Vote Has Expired")
        self.resetvote()

    def handle_vote(self, msg, client_id: int):
        current_time = time.time()
        player_info = self.get_info(client_id)
        if msg.lower() in self.vote_available:
            if self.started:
                self.error(f"Vote For {self.ongoing_vote[-1]} Is Already Started. Vote Using 'y'", dm=True, cid=client_id)
                return
            elif len(bs.get_game_roster()) < 2:
                self.error("Not Enough Players To Start Vote", dm=True, cid=client_id)
                return
            else:
                self.started = True
                self.start_time = current_time
                self.ongoing_vote.append(msg.lower())
                self.voters.append(str(player_info["pb"]))
                self.success(f"Vote For {msg} Started.\nPress 'y' To Vote", dm=True, cid=client_id)
                with bs.get_foreground_host_activity().context:
                   bs.timer(60, self.end_vote, False)
        else:
            if msg.lower() == "y":
                if str(player_info["pb"]) in self.voters:
                    self.error("You Have Already Voted", dm=True, cid=client_id)
                else:
                    self.voters.append(str(player_info["pb"]))
                    self.success(f"You Have Voted For {self.ongoing_vote[-1]}", dm=True, cid=client_id)
                    if len(self.voters) >= self.vote_need(len(bs.get_game_roster())):
                        self.vote_success()
                    else:
                        self.success(f"{self.vote_need(len(bs.get_game_roster() - 1)) - len(self.voters)} More Votes Needed")
                        