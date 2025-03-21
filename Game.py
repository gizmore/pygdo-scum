import time
from random import shuffle

from gdo.base.Application import Application
from gdo.base.Cache import Cache
from gdo.base.Trans import t
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDO_User import GDO_User
from gdo.scum.module_scum import module_scum


class Game:

    CARD_ORDER = {'7': 1, '8': 2, '9': 3, '10': 4, 'J': 5, 'Q': 6, 'K': 7, 'A': 8}

    GAMES: dict[str, 'Game'] = {}

    _channel: GDO_Channel
    _players: list[GDO_User]
    _passed: list[GDO_User]
    _finished: list[GDO_User]
    _cards: list[str]
    _hands: dict[str, list[str]]
    _table: list[str]
    _inited: bool
    _started: bool
    _current_player: int
    _last_action_time: float
    _max_players: int
    _num_players: int

    def __init__(self, channel: GDO_Channel):
        self._channel = channel
        self._max_players = module_scum.instance().cfg_max_players()
        self.reset()

    @classmethod
    def instance(cls, channel: GDO_Channel) -> 'Game':
        if game := cls.GAMES.get(channel.get_id()):
            return game
        game = Game(channel)
        cls.GAMES[channel.get_id()] = game
        return game

    def reset(self):
        self._players = []
        self._passed = []
        self._finished = []
        self._cards = []
        self._hands = {}
        self._hands_start = {}
        self._table = []
        self._inited = False
        self._started = False
        self._current_player = -1
        self._last_action_time = 0
        self._num_players = 0

    def current_player(self) -> 'GDO_User':
        return self._players[self._current_player]

    def is_over(self) -> bool:
        return len(self._players) <= 1

    def init(self):
        self._inited = True
        self._last_action_time = Application.TIME
        return self

    async def start(self):
        self._started = True
        types = ['♦', '♥', '♠', '♣'] * ((len(self._players) - 1) // 4 + 1)
        self._cards = []
        for _type in types:
            self._cards.extend(f"{_type}{val}" for val in self.CARD_ORDER.keys())
        shuffle(self._cards)
        shuffle(self._players)
        for _ in range(8):
            for player in self._players:
                self._hands[player.get_id()].append(self._cards.pop())
        for player in self._players:
            self._hands[player.get_id()].sort(
                key=lambda card: self.CARD_ORDER[card[1:]]
            )
            self._hands_start[player.get_id()] = self._hands[player.get_id()].copy()
            await player.send('msg_scum_your_cards', (self.render_cards(self._hands[player.get_id()]),), True)
        self.next_player()
        return self

    def join(self, player: GDO_User):
        self._players.append(player)
        self._hands[player.get_id()] = []
        self._last_action_time = Application.TIME
        self._num_players += 1
        return self

    async def over(self):
        for user in self._finished:
            await self._channel.send(t('msg_scum_game_over_player', (user.render_name(), self.get_rank(user), self.get_points(user), self.render_cards(self._hands_start[user.get_id()]))))

    def play(self, player: GDO_User, cards: list[str]):
        self._last_action_time = time.time()
        self._passed.clear()
        hand = self._hands[player.get_id()]
        for c in cards:
            for cc in hand:
                if c == cc:
                    hand.remove(cc)
        self._table = cards.copy()
        if not hand:
            self._players.remove(player)
            self._finished.append(player)
            if len(self._finished) == 1:
                player.increase_setting('scum_won', 1)
                module_scum.instance().increase_config_val('scum_games', 1)
            player.increase_setting('scum_points', self.get_points(player))
            if len(self._players) == 1:
                player = self._players[0]
                self._players.remove(player)
                self._finished.append(player)
        if cards[0][1] == 'A':
            self._table.clear()
        else:
            self.next_player()
        return self

    def passed(self, player: GDO_User):
        self._passed.append(player)
        self.next_player()
        return self

    def all_passed(self) -> bool:
        if len(self._players) == len(self._passed):
            self._table.clear()
            return True
        return False

    ##########
    # Helper #
    ##########

    async def send_status(self):
        await self._channel.send(self.render_current_state())

    def next_player(self):
        if self._players:
            self._current_player = (self._current_player + 1) % len(self._players)
            self._last_action_time = Application.TIME
        return self

    def is_full(self) -> bool:
        return len(self._players) == self._max_players

    def get_rank(self, user: GDO_User) -> int:
        return self._finished.index(user) + 1

    def get_points(self, user: GDO_User) -> int:
        return self._num_players - self.get_rank(user)

    ##########
    # Render #
    ##########

    def render_players(self) -> list[str]:
        return [user.render_name() for user in self._players]

    def render_cards(self, cards: list[str]) -> str:
        return ", ".join(cards)

    def render_current_state(self) -> str:
        if not self._players:
            return t('msg_scum_game_over')
        elif self._table:
            return t('msg_scum_state_table', (self.current_player().render_name(), self.render_cards(self._table)))
        else:
            return t('msg_scum_state_fresh', (self.current_player().render_name(),))
