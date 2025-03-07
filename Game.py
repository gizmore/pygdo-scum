import time
from random import shuffle

from gdo.base.Cache import Cache
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDO_User import GDO_User
from gdo.scum.module_scum import module_scum


class Game:

    MAX_PLAYERS = 8

    _channel: GDO_Channel
    _players: list[GDO_User]
    _passed: list[GDO_User]
    _finished: list[GDO_User]
    _cards: list[str]
    _hands: dict[str, list[str]]
    _inited: bool
    _started: bool
    _current_player: int
    _last_action_time: float

    def __init__(self, channel: GDO_Channel):
        self._channel = channel
        self.reset()

    @classmethod
    def instance(cls, channel: GDO_Channel):
        if game := Cache.get('scum_game', channel.get_id()):
            return game
        game = Game(channel)
        Cache.set('scum_game', channel.get_id(), game)
        return game

    def reset(self):
        self._players = []
        self._passed = []
        self._finished = []
        self._cards = []
        self._hands = {}
        self._inited = False
        self._started = False
        self._current_player = -1
        self._last_action_time = 0

    def current_player(self) -> 'GDO_User':
        return self._players[self._current_player]

    def is_over(self) -> bool:
        return len(self._players) == 0

    def init(self):
        self._inited = True
        return self

    def start(self):
        self._started = True
        types = ['♦', '♥', '♠', '♣'] * ((len(self._players) - 1) // 4 + 1)
        self._cards = []
        for _type in types:
            self._cards.extend(f"{_type}{val}" for val in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
        shuffle(self._cards)
        for _ in range(8):
            for player in self._players:
                self._hands[player.get_id()].append(self._cards.pop())
        self.next_player()
        return self

    def join(self, player: GDO_User):
        self._players.append(player)
        self._hands[player.get_id()] = []
        return self

    def over(self):
        pass

    def play(self, player: GDO_User, cards: list[str]):
        self._last_action_time = time.time()
        hand = self._hands[player.get_id()]
        for c in cards:
            hand.remove(c)
        if not hand:
            self._players.remove(player)
            self._finished.append(player)
            if len(self._finished) == 1:
                player.increase_setting('scum_won', 1)
                player.increase_setting('scum_points', len(self._players))
                module_scum.instance().increase_config_val('scum_games')
        self.next_player()
        return self

    def passed(self, player: GDO_User):
        self._passed.append(player)
        self.next_player()
        return self

    def next_player(self):
        self._current_player = (self._current_player + 1) % len(self._players)
        return self

    def have_all_passed(self) -> bool:
        return len(self._passed) == len(self._players)

    def render_players(self) -> list[str]:
        return [user.render_name() for user in self._players]
