from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.scum.Game import Game


class play(Method):

    def gdo_trigger(self) -> str:
        return 'scum'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> [GDT]:
        return [
            GDT_RestOfText('cards').not_null(),
        ]

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if self.param_val('cards')[0] == 'p':
            return self.scum_pass(game)
        user = self._env_user
        if user not in game._players:
            return self.err('err_scum_player_not_in_game')
        if not game._started:
            return self.err('err_scum_not_started')
        if game.current_player() != self._env_user:
            return self.err('err_scum_not_your_turn')
        hand = game._hands[user.get_id()]
        cards = self.param_val('cards').split(' ')
        c = cards[0]
        for card in cards:
            if card != c:
                return self.err('err_scum_need_same_cards')
        if hand.count(c) < len(cards):
            return self.err('err_scum_not_right_cards')
        game.play(user, cards)
        self.msg('msg_scum_played_cards', (user.render_name(), game.render_cards(cards), game.current_player().render_name()))
        return self.empty()

    def scum_pass(self, game: Game):
        game.passed(self._env_user)
        if game.have_all_passed():
            return self.msg('msg_scum_all_passed', (self._env_user.render_name(),))
        return self.msg('msg_scum_passed')
